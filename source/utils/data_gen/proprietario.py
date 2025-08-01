import random
from .document_ids import DocumentIDGen
from .endereco import EnderecoGen
from faker import Faker

class ProprietarioGen:

    def __init__(self):

        self.faker = Faker('pt-br')
        self.documents = DocumentIDGen()
        self.endereco_gen = EnderecoGen()

        self.nome = self.faker.name()
        self.cpf = self.documents.cpf
        self.rg = self.documents.rg
        self.profissao = self.faker.job()
        self.endereco = self.endereco_gen.endereco_completo

        self.estado_civil = random.choice(['solteiro', 'casado'])


        if self.estado_civil == 'casado':
            self.conjuge = ProprietarioGen()
            self.conjuge.estado_civil = 'casado'

    @property
    def dados_estruturados(self) -> dict:

        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "rg": self.rg,
            "profissao": self.profissao,
            "endereco": self.endereco,
            "estado_civil": self.estado_civil
        }
    
    
    @property
    def string_proprietario(self) -> str:

        if self.estado_civil == 'casado':
            conjuge = self.conjuge
            conjuge_str = f" e seu cônjuge {conjuge.nome}, CPF {conjuge.cpf}, RG {conjuge.rg}, profissão {conjuge.profissao}"
        else:
            conjuge_str = ''

        return f"{self.nome.upper()}, CPF {self.cpf}, RG {self.rg}, {self.profissao}{conjuge_str}, residente e domiciliado em {self.endereco}"