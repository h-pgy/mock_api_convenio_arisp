from pydantic import BaseModel, Field
from enum import Enum

class EstadoCivil(str, Enum):
    SOLTEIRO = 'solteiro'
    CASADO = 'casado'


class Proprietario(BaseModel):

    nome: str = Field(..., description="Nome completo do proprietário")
    cpf: str = Field(..., description="CPF do proprietário")
    rg: str = Field(..., description="RG do proprietário")
    profissao: str = Field(..., description="Profissão do proprietário")
    endereco: str = Field(..., description="Endereço do proprietário")
    estado_civil: EstadoCivil = Field(..., description="Estado civil do proprietário")


class ProprietarioFull(Proprietario):

    id: int = Field(..., description="ID do proprietário")
    cartorio_num: str = Field(..., description="Número do cartório onde o imóvel está registrado")
    matricula: str = Field(..., description="Matrícula do imóvel")
    cnm: str = Field(..., description="Código Nacional de Matrícula (CNM) do imóvel")
