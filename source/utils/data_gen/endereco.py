from faker import Faker
import random


class EnderecoGen:

    def __init__(self):
        self.faker = Faker('pt-br')

    @property
    def cidade(self) -> str:
        return 'São Paulo'
    
    @property
    def estado(self) -> str:
        return 'SP'
    
    @property
    def rua(self) -> str:
        return self.faker.street_name()
    
    @property
    def numero(self) -> str:
        return str(random.randint(1, 999))
    
    @property
    def bairro(self) -> str:
        return self.faker.bairro()

    @property
    def cep(self) -> str:
        return self.faker.postcode()
    

    @property
    def endereco_completo(self) -> str:
        return f"{self.rua}, {self.numero}, {self.bairro}, cidade de {self.cidade} - {self.estado}, CEP: {self.cep}"