from pydantic import BaseModel, Field, field_validator
import re

class SQL(BaseModel):

    sql: str = Field(..., description="Numero SQL no formato XXX.XXX.XXXX-XX")
    setor: int = Field(..., description="Setor do lote", gt=0)
    quadra: int = Field(..., description="Quadra do lote", gt=0)
    lote: int = Field(..., description="Lote do imóvel", gt=0)
    condominio: int = Field(..., description="Código de condomínio do imóvel", ge=0)

    @field_validator('sql')
    def validate_sql(cls, value):
        if not value:
            raise ValueError('Parametro sql não pode ser vazio')

        patt = r'\d{3}\.\d{3}\.\d{4}-\d{2}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro sql deve estar no formato {patt}. Exemplo: 123.456.7890-12')

        return value
    
class CCIR(BaseModel):

    ccir: str = Field(..., description="Numero CCIR no formato XXX.XXX.XXX.XXX-X")

    @field_validator('ccir')
    def validate_ccir(cls, value):
        if not value:
            raise ValueError('Parametro ccir não pode ser vazio')

        patt = r'\d{3}\.\d{3}\.\d{3}\.\d{3}-\d{1}'

        if not re.match(patt, value):
            raise ValueError(f'Parametro ccir deve estar no formato {patt}. Exemplo: 123.456.789.012-3')

        return value