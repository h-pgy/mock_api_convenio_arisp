from pydantic import BaseModel, field_validator, Field
import re
from enum import Enum

from .proprietario import Proprietario as SchemaProprietario

class MatriculaSearch(BaseModel):

    matricula: str
    cartorio_num: int

    @field_validator('matricula')
    def validate_matricula(cls, value):
        if not value:
            raise ValueError('Matricula cannot be empty')
        
        patt = r'\d{2}\.\d{3}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro matriculo deve estar no formato {patt}. Exemplo: 12.345')

        return value
    
    @field_validator('cartorio_num')
    def validate_cartorio_num(cls, value):
        if not value:
            raise ValueError('Parametro cartorio_num não pode ser vazio')

        if not isinstance(value, int) or value <= 0 or value > 100:
            raise ValueError('Parametro cartorio_num deve ser um número inteiro positivo entre 1 e 100')

        return value
    
class CNMSearch(BaseModel):

    cnm: str = Field(..., description="Código CNM no formato 123456.1.1234567-12")

    @field_validator('cnm')
    def validate_cnm(cls, value):
        if not value:
            raise ValueError('Parametro cnm não pode ser vazio')
        
        patt = r'\d{6}\.\d{1}\.\d{7}-\d{2}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro cnm deve estar no formato {patt}. Exemplo: 123456.1.1234567-12')

        return value
    
class MatriculaSearchData(MatriculaSearch, CNMSearch):
    """
    Model for searching matricula with CNM.
    Combines MatriculaSearch and CNMSearch.
    """
    pass


class TipoImovel(str, Enum):
    URBANO = 'Urbano'
    RURAL = 'Rural'


class MatriculaReturn(BaseModel):
    """
    Model for the return of matricula queries.
    """
    matricula: str= Field(..., description="Número da matrícula no formato XX.XXX")
    cartorio_num: int= Field(..., description="Número do cartório (1-100)", ge=0, le=100)
    cnm: str= Field(..., description="Código CNM")
    endereco: str= Field(..., description="Endereço do imóvel")
    proprietario: SchemaProprietario
    data_escritura: str= Field(..., description="Data da escritura")
    area_terreno: float= Field(..., description="Área do terreno em m²", gt=0)
    area_construida: float= Field(..., description="Área construída em m²", ge=0)
    ano_construcao: int= Field(..., description="Ano de construção", gt=1400, lt=2026)
    tipo_imovel: TipoImovel = Field(..., description="Tipo do imóvel (Urbano ou Rural)")

    @field_validator('matricula')
    def validate_matricula(cls, value):
        if not value:
            raise ValueError('Matricula cannot be empty')
        
        patt = r'\d{2}\.\d{3}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro matricula deve estar no formato {patt}. Exemplo: 12.345')

        return value

    @field_validator('cnm')
    def validate_cnm(cls, value):
        if not value:
            raise ValueError('Parametro cnm não pode ser vazio')
        
        patt = r'\d{6}\.\d{1}\.\d{7}-\d{2}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro cnm deve estar no formato {patt}. Exemplo: 123456.1.1234567-12')

        return value
    
    @field_validator('data_escritura')
    def validate_data_escritura(cls, value):
        if not value:
            raise ValueError('Parametro data_escritura não pode ser vazio')

        patt = r'\d{2}/\d{2}/\d{4}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro data_escritura deve estar no formato {patt}. Exemplo: 12/12/2020')

        return value
