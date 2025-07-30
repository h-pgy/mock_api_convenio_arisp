import random
from .proprietario import ProprietarioGen
from .document_ids import DocumentIDGen
from .endereco import EnderecoGen
from faker import Faker

class RegistroGen:

    def __init__(self, proprietario: ProprietarioGen, endereco: EnderecoGen, num_cartorio:int)->None:

        self.faker = Faker('pt-br')

        self.proprietario: ProprietarioGen = proprietario
        self.endereco_obj: EnderecoGen = endereco
        self.document_ids = DocumentIDGen()

        self.tipo_imovel = random.choices(['Rural', 'Urbano'], weights=[0.15, 0.85], k = 1)[0]

        self.largura = random.randint(1, 100)
        self.comprimento = random.randint(1, 100)
        self.area_terreno = self.largura * self.comprimento
        self.area_construida = round(self.area_terreno * random.uniform(0, 1), 0)
        self.ano_construcao = random.randint(1900, 2023)
        self.data_escritura = self.faker.date_between(start_date='-100y', end_date='today')
        self.num_cartorio = str(num_cartorio)

        self.matricula_num = self.document_ids.matricula
        self.ccir = self.document_ids.ccir
        self.sql = self.document_ids.sql
        self.cnm = self.document_ids.cnm


    @property
    def endereco(self) -> str:
        return self.endereco_obj.endereco_completo


    @property
    def registro_str(self)->str:

        frase = (
                f'São Paulo, {self.data_escritura.strftime("%d de %B de %Y")}. {self.num_cartorio}º Registro de Imóveis, '
                f'UM {self.tipo_imovel}, sito à {self.endereco}, ' 
                f', com área total de {self.area_terreno} m², medindo {self.largura} metros de largura por {self.comprimento} metros de comprimento, '
                f'confinando de um lado com o lote {random.randint(1, 120)} de outro lado com o lote {random.randint(1, 120)}, e nos fundos com o lote {random.randint(1, 120)}')
        
        if self.tipo_imovel == 'Urbano':
            frase += f', dotada de uma edificação com {self.area_construida} m² de área construída, construída no ano de {self.ano_construcao}'

        if self.tipo_imovel == 'Rural':
            cadastro = f', cadastro no Cadastro de Imóveis Rurais(CCIR) sob o número {self.ccir}'
        else:
            cadastro = f', cadastro sob o número de contribuinte {self.sql}'

        registro  = f' e registrado neste Cartório de Registro de Imóveis de número {self.num_cartorio}, da Comarca de São Paulo, sob o número {self.matricula_num}. Cadastro CNM: {self.cnm}'

        frase += cadastro + registro + '.'


        frase += 'PROPRIETÁRIO: ' + self.proprietario.string_proprietario + '.'

        frase += ' Registro efetuado em ' + self.data_escritura.strftime("%d de %B de %Y") + '.'

        return frase
