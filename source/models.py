from .utils.data_gen import DataGenerator

class Model:

    def __init__(self, qtd_imoveis:int=100):

        self.data = DataGenerator(qtd_imoveis)

    def solve_table(self, table_name: str) -> list[dict]:

        if not hasattr(self.data, table_name):
            raise ValueError(f"Table {table_name} does not exist in the data generator.")

        table = getattr(self.data, table_name)
        if not isinstance(table, list):
            raise ValueError(f"Table {table_name} is not a list.")
        
        return table
    
    def query_table_where(self, table_name:str, condition: dict) -> list[dict]:

        table = self.solve_table(table_name)
        results = []
        for row in table:
            if all(row.get(key) == value for key, value in condition.items()):
                results.append(row)
        return results

    def query_full_table(self, table_name: str) -> list[dict]:

        table = self.solve_table(table_name)
        return table
    
    def query_table_index(self, table_name: str, index: int) -> dict:

        table = self.solve_table(table_name)
        if index < 0 or index >= len(table):
            raise ValueError(f"Index {index} is out of bounds for table {table_name}.")
        return table[index]