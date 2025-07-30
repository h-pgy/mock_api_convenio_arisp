from pydantic import BaseModel


class MatriculaReturn(BaseModel):
    """
    Model for the return of matricula queries.
    """
    matricula: str
    cartorio_num: str
    cnm: str
    endereco: str
    proprietario: str
    data_escritura: str
    area_terreno: float
    area_construida: float
    ano_construcao: int
    tipo_imovel: str
