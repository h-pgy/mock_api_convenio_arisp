from .proprietario import ProprietarioGen
from .endereco import EnderecoGen
from .registro import RegistroGen
from .transacao import TransacaoGen
from .document_ids import DocumentIDGen
from ..file_io import solve_path
from typing import List
import random


class DataPointGen:


    def __init__(self):


        self.documents = DocumentIDGen()


        self.criar_imovel()
        self.registrar()
        self.vincular_sqls()

        self.total_transacoes = random.randint(1, 50)
        self.averbar_transacoes()

        self.num_pdf_matricula = random.randint(1, 3)
        self.path_matriculas = solve_path('matriculas', '../mock_data/static')


    def criar_imovel(self)->None:

        self.proprietario_inicial = ProprietarioGen()
        self.endereco_imovel = EnderecoGen()

        self.proprietario_atual = self.proprietario_inicial


    def registrar(self) -> None:

        self.num_cartorio = random.randint(1, 10)
        self.registro = RegistroGen(self.proprietario_inicial, self.endereco_imovel, self.num_cartorio)
        self.data_escritura = self.registro.data_escritura

    def vincular_sqls(self) -> None:
        """
        Vincula os IDs de documentos SQL aos registros e transações.
        """
        self.sqls: List[str] = []

        num_sqls = random.randint(0, 3)

        if num_sqls > 0 and self.registro.tipo_imovel == 'Urbano':
            self.sqls.append(self.registro.sql)

            for _ in range(num_sqls-1):
                self.sqls.append(self.documents.sql)

    def vincular_ccirs(self) -> None:
        """
        Vincula os CCIRs aos registros e transações.
        """ 

        self.ccirs: List[str] = []

        num_ccirs = random.randint(0, 2)

        if num_ccirs > 0 and self.registro.tipo_imovel == 'Rural':
            self.ccirs.append(self.registro.ccir)

            for _ in range(num_ccirs-1):
                self.ccirs.append(self.documents.ccir)


    def make_transacao(self) -> TransacaoGen:

        comprador = ProprietarioGen()
        transacao = TransacaoGen(self.proprietario_atual, comprador, self.registro)
        self.proprietario_atual = comprador
        return transacao
    
    def averbar_transacoes(self) -> None:

        self.transacoes: List[TransacaoGen] = []
        for _ in range(self.total_transacoes):
            self.transacoes.append(self.make_transacao())

    def quebrar_em_laudas(self, texto:str, tamanho_lauda=1400)->list[str]:
        laudas = []
        while len(texto) > tamanho_lauda:
            # Tenta quebrar no último espaço antes do limite de 1400
            corte = texto.rfind(' ', 0, tamanho_lauda)
            if corte == -1:  # Não encontrou espaço, quebra no limite
                corte = tamanho_lauda
            laudas.append(texto[:corte].strip())
            texto = texto[corte:].lstrip()  # Remove espaço à esquerda da próxima lauda
        if texto:
            laudas.append(texto.strip())  # Adiciona o restante
        return laudas
    

    @property
    def matricula_estruturada(self) -> dict:
        """
        Retorna a matrícula estruturada como um dicionário.
        """
        parsed = {
                "matricula": self.registro.matricula_num,
                "cartorio_num": self.registro.num_cartorio,
                "cnm": self.registro.cnm,
                "endereco": self.registro.endereco,
                "proprietario": self.proprietario_inicial.dados_estruturados,
                "data_escritura": self.registro.data_escritura.strftime('%d/%m/%Y'),
                "area_terreno": self.registro.area_terreno,
                "area_construida": self.registro.area_construida,
                "ano_construcao": self.registro.ano_construcao,
                "tipo_imovel": self.registro.tipo_imovel,
                "matricula_pdf_file": self.matricula_pdf_filepath,
            }
        
        return parsed

    @property
    def matricula_ocr(self)->str:

        registro_str = self.registro.registro_str
        transacoes_str = "\n".join([transacao.transacao_str for transacao in self.transacoes])

        return f"{registro_str}\n\n{transacoes_str}"
    
    @property
    def paginas(self) -> List[str]:
        """
        Retorna as páginas do documento, quebrando o texto em laudas de 1400 caracteres.
        """
        texto_completo = self.matricula_ocr
        return self.quebrar_em_laudas(texto_completo, tamanho_lauda=1400)
    
    @property
    def num_paginas(self) -> int:
        """
        Retorna o número total de páginas do documento.
        """
        return len(self.paginas)
    
    @property
    def matricula_pdf_filepath(self) -> str:
        """
        Retorna o caminho do PDF da matrícula.
        """
        file_name = f"{self.documents.matricula}.pdf"
        file_path = solve_path(file_name, self.path_matriculas)
        return file_path
    