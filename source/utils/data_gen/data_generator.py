from typing import List, Callable
from .data_point import DataPointGen
import os
from ..file_io import read_json_file, save_json_file, solve_path

class DataGenerator:
    
    def __init__(self, num_matriculas: int = 100) -> None:

        self.data_points = [DataPointGen() for _ in range(num_matriculas)]
        
        
        self.matriculas = self.build_matriculas_table()
        self.transactions = self.build_transactions_table()
        self.sqls = self.build_sqls_table()
        self.ocrs = self.build_ocrs_table()

    def build_matriculas_table(self) -> list[dict]:

        matriculas = []
        for i, data_point in enumerate(self.data_points):
            dados = data_point.matricula_estruturada
            dados['id'] = i + 1
            matriculas.append(dados)

        return matriculas

    def build_transactions_table(self) -> list[dict]:

        transactions = []
        i = 0
        for data_point in self.data_points:
            for transacao in data_point.transacoes:
                dados = transacao.dados_estruturados
                dados['id'] = i + 1
                i += 1
                transactions.append(dados)

        return transactions
    
    def build_sqls_table(self) -> list[dict]:

        dados_tabela = []
        i = 0
        for data_point in self.data_points:
            dados = {
                'id': i + 1,
                'sqls': data_point.sqls,
                'matricula': data_point.matricula_estruturada['matricula'],
                'cnm' : data_point.matricula_estruturada['cnm'],
            }
            i += 1
            dados_tabela.append(dados)

        return dados_tabela
    
    def build_ocrs_table(self) -> list[dict]:

        ocrs = []
        i = 0
        for data_point in self.data_points:
            dados = {
                'id': i + 1,
                'ocr': data_point.paginas,
                'num_paginas': data_point.num_paginas,
                'matricula': data_point.matricula_estruturada['matricula'],
                'cnm' : data_point.matricula_estruturada['cnm'],
            }
            i += 1
            ocrs.append(dados)

        return ocrs
    
    def solve_table(self, table_name: str) -> list[dict]:

        if not hasattr(self, table_name):
            raise ValueError(f"Table {table_name} does not exist in the data generator.")
        
        table = getattr(self, table_name)
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





