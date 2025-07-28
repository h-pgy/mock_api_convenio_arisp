from file_io import read_binary_file, read_json_file, get_file
import json


class FakeDB:

    def __init__(self, db_path: str, tables=list[str], lazy_init=False) -> None:

        self.db_path = db_path
        self.data = {}
        self.tables = tables
        self.lazy_init = lazy_init
        if not self.lazy_init:
            self.initialize_db()


    def initialize_db(self) -> None:

        for table in self.tables:
            self.load_table(table)

    def get_table_file_path(self, table_name: str, raise_if_not_exists:bool=True) -> str:
        return get_file(f"{table_name}.json", self.db_path, raise_if_not_exists)

    def load_table(self, table_name:str)->None:

        print('Loading table:', table_name)
        table_file = self.get_table_file_path(table_name)
        try:
            self.data[table_name] = read_json_file(table_file, self.db_path)
        except ValueError as e:
            raise ValueError(f"Failed to load table {table_name}: {e}")

    def check_table_exists(self, table_name: str) -> bool:

        exists = table_name in self.data
        if not exists and not self.lazy_init:
            raise ValueError(f"Table {table_name} does not exist in the database.")
        return exists
    
    def solve_table(self, table_name: str) -> None:

        exists = self.check_table_exists(table_name)
        if not exists:
            self.load_table(table_name)
    
    def save_table(self, table_name:str) -> None:

        self.solve_table(table_name)

        file_path = self.get_table_file_path(table_name, raise_if_not_exists=False)
        with open(file_path, 'w') as file:
            json.dump(self.data[table_name], file, indent=4)

    def update_table(self, table_name: str, row:int, new_data: dict) -> None:

        self.solve_table(table_name)

        if row < 0 or row >= len(self.data[table_name]):
            raise ValueError(f"Row {row} does not exist in table {table_name}.")

        self.data[table_name][row] = new_data
        self.save_table(table_name)

    def append_table(self, table_name: str, new_data: dict) -> None:

        if not isinstance(new_data, dict):
            raise ValueError("New data must be a dictionary.")

        self.solve_table(table_name)
        new_data = [new_data]

        self.data[table_name].extend(new_data)
        self.save_table(table_name)

    def append_table_multiple(self, table_name: str, new_data: list[dict]) -> None:

        if not isinstance(new_data, list):
            raise ValueError("New data must be a list of dictionaries.")

        self.solve_table(table_name)

        for item in new_data:
            if not isinstance(item, dict):
                raise ValueError("Each item in new data must be a dictionary.")

        self.data[table_name].extend(new_data)
        self.save_table(table_name)
    

    def query_full_table(self, table_name: str) -> list[dict]:

        self.solve_table(table_name)
        return self.data[table_name]
    
    def query_table_index(self, table_name: str, index: int) -> dict:

        self.solve_table(table_name)
        if index < 0 or index >= len(self.data[table_name]):
            raise ValueError(f"Index {index} is out of bounds for table {table_name}.")

        return self.data[table_name][index]
    
    def query_table_where(self, table_name:str, condition: dict) -> list[dict]:

        self.solve_table(table_name)

        results = []
        for row in self.data[table_name]:
            if all(row.get(key) == value for key, value in condition.items()):
                results.append(row)
        
        return results
        