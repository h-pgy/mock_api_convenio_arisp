from typing import List
from fastapi import FastAPI

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
