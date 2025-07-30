from .proprietario import ProprietarioGen
from .document_ids import DocumentIDGen
from .endereco import EnderecoGen
from .registro import RegistroGen
import random
from datetime import date
from faker import Faker

class TransacaoGen:

    def __init__(self, proprietario: ProprietarioGen, comprador: ProprietarioGen, 
                 registro: RegistroGen) -> None:


        self.faker = Faker('pt-br')

        self.vendedor: ProprietarioGen = proprietario
        self.comprador: ProprietarioGen = comprador
        self.registro: RegistroGen = registro
        self.data_escritura = self.registro.data_escritura
        self.endereco_imovel: EnderecoGen = self.registro.endereco_obj
        self.document_ids = DocumentIDGen()

        self.tipo_transacao = random.choice(['Compra e Venda', 'Doação', 'Permuta'])
        self.valor_transacao = random.randint(100000, 1000000)
        self.data_transacao = Faker('pt-br').date_between(start_date='-100y', end_date='today')
        self.num_cartorio = str(self.registro.num_cartorio)
        self.num_registro = self.document_ids.num_registro

    @property
    def dados_estruturados(self) -> dict:
        return {
            "matricula": self.registro.matricula_num,
            "cartorio_num": self.num_cartorio,
            "ccir" : self.registro.ccir,
            "num_averbacao": self.num_registro,
            "comprador": self.comprador.dados_estruturados,
            "vendedor": self.vendedor.dados_estruturados,
            "tipo_transacao": self.tipo_transacao,
            "valor_transacao": self.valor_transacao,
            "data_transacao": self.data_transacao.strftime('%d/%m/%Y'),
        }
    
    @property
    def transacao_str(self) -> str:

        frase = (
            f"Registro Nº {self.num_registro} - São Paulo, {self.data_transacao.strftime('%d de %B de %Y')}\n"
            f"Pela escritura pública lavrada em {self.data_escritura.strftime('%d de %B de %Y')}, no Livro {random.randint(1, 5)}, folhas {random.randint(1, 152)}, "
            f"do {self.num_cartorio}, o {self.vendedor.string_proprietario}, "
            f"**vende** a {self.comprador.string_proprietario}, "
            f"o imóvel situado à {self.endereco_imovel.endereco_completo}, pelo valor de R$ {self.valor_transacao:,.2f}, pagos nesta data.\n"
            f"A aquisição foi feita com recursos próprios do(a) comprador(a), conforme declaração. Registrado sem ônus ou gravames.\n"
            f"O Oficial\n{self.faker.name()}"
        )

        return frase