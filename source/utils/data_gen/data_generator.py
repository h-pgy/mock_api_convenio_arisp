from typing import List, Callable
from .data_point import DataPointGen
import os
from tqdm import tqdm
from ..file_io import read_json_file, save_json_file, solve_path

class DataGenerator:
    
    def __init__(self, qtd_imoveis: int = 100) -> None:

        self.qtd_imoveis = qtd_imoveis
        self.generate_data()

    def generate_data(self)->None:

        print(f'Gerando dados para {self.qtd_imoveis} imóveis...')

        self.data_points = []

        for i in tqdm(range(self.qtd_imoveis)):
            self.data_points.append(DataPointGen())

        print('Construindo tabela de matrículas')
        self.matriculas = self.build_matriculas_table()
        print('Construindo tabela de transações')
        self.transacoes = self.build_transactions_table()
        print('Construindo tabela de SQLs')
        self.sqls = self.build_sqls_table()
        print('Construindo tabela de CCIRs')
        self.ccirs = self.build_ccirs_table()
        print('Construindo tabela de OCRs')
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
                'cartorio_num' : data_point.matricula_estruturada['cartorio_num'],
                'matricula': data_point.matricula_estruturada['matricula'],
                'cnm' : data_point.matricula_estruturada['cnm'],
            }
            i += 1
            dados_tabela.append(dados)

        return dados_tabela
    
    def build_ccirs_table(self) -> list[dict]:

        ccirs = []
        i = 0
        for data_point in self.data_points:
            dados = {
                'id': i + 1,
                'ccirs': data_point.ccirs,
                'cartorio_num' : data_point.matricula_estruturada['cartorio_num'],
                'matricula': data_point.matricula_estruturada['matricula'],
                'cnm' : data_point.matricula_estruturada['cnm'],
            }
            i += 1
            ccirs.append(dados)

        return ccirs
    
    def build_ocrs_table(self) -> list[dict]:

        ocrs = []
        i = 0
        for data_point in self.data_points:
            dados = {
                'id': i + 1,
                'ocr': data_point.paginas,
                'num_paginas': data_point.num_paginas,
                'matricula': data_point.matricula_estruturada['matricula'],
                'cartorio_num' : data_point.matricula_estruturada['cartorio_num'],
                'cnm' : data_point.matricula_estruturada['cnm'],
            }
            i += 1
            ocrs.append(dados)

        return ocrs
    






