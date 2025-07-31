from pydantic import BaseModel, Field
from enum import Enum

from .proprietario import Proprietario

class TipoTransacao(str, Enum):
    COMPRA = 'Compra e Venda'
    DOACAO = 'Doação'
    PERMUTA = 'Permuta'


class Transacao(BaseModel):

    matricula: str = Field(..., description="Número da matrícula")
    cartorio_num: int = Field(..., description="Número do cartório")
    cnm: str = Field(..., description="Número do CNM")
    num_averbacao: str = Field(..., description="Número da averbação")
    comprador: Proprietario = Field(..., description="Nome do comprador")
    vendedor: Proprietario = Field(..., description="Nome do vendedor")
    tipo_transacao: TipoTransacao = Field(..., description="Tipo da transação")
    valor_transacao: float = Field(..., description="Valor da transação", gt=0)
    data_transacao: str = Field(..., description="Data da transação")