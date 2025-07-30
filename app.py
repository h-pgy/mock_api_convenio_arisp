from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from source import queries, schemas, models


data = models.Model()

app = FastAPI(
    title="Mock API para Convênio com ARISP",
    description="Documentação interativa de MockAPI no padrão OpenAPI 3.0 (swagger ui) para integração de dados entre a PMSP e a ARISP.",
    version="0.0.1",
    contact={
        "name": "Henrique Pougy",
        "email": "hpougy@prefeitura.sp.gov.br"
        }
    )

@app.get("/matriculas", response_model=List[schemas.MatriculaSearchData], tags=['Matrícula'])
def get_matriculas():

    matriculas = queries.get_all_matriculas(data)
    dados = []
    for matricula in matriculas:
        parsed = {
            'matricula' : matricula['matricula'],
            'cartorio_num' : matricula['cartorio_num'],
            'cnm' : matricula['cnm']
        }

        dados.append(schemas.MatriculaSearchData(**parsed))

    return dados

@app.get("/matriculas/", response_model=schemas.MatriculaReturn, tags=['Matrícula'])
def get_matricula_by_cnm(cnm:str) -> schemas.MatriculaReturn:

    try:
        search  = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    matricula = queries.get_matricula_data_by_cnm(data, search.cnm)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    return schemas.MatriculaReturn(**matricula)

@app.get("/matriculas/{cartorio_num}/{matricula}", response_model=schemas.MatriculaReturn, tags=['Matrícula'])
def get_matricula_by_matricula(cartorio_num: int, matricula: str) -> schemas.MatriculaReturn:
    
    try:
        search  = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(cartorio_num)
    matricula = queries.get_matricula_data_by_matricula(data, cartorio_num, matricula)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    return schemas.MatriculaReturn(**matricula)
