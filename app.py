from typing import List
from urllib import response
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
        },
    docs_url="/"
    )

@app.get("/matriculas", response_model=List[schemas.MatriculaSearchData], tags=['Matrículas'])
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

@app.get("/matriculas/data", response_model=schemas.MatriculaReturn, tags=['Matrículas'])
def get_matricula_by_cnm(cnm:str) -> schemas.MatriculaReturn:

    try:
        search  = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    matricula = queries.get_matricula_data_by_cnm(data, search.cnm)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    return schemas.MatriculaReturn(**matricula)

@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/data", response_model=schemas.MatriculaReturn, tags=['Matrículas'])
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


@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/transacoes", response_model=List[schemas.Transacao], tags=['Transações'])
def get_transacoes_by_matricula(cartorio_num: int, matricula: str) -> List[schemas.Transacao]:
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(cartorio_num)
    transacoes = queries.get_transacoes_by_matricula(data, cartorio_num, matricula)
    if not transacoes:
        raise HTTPException(status_code=404, detail="Transações não encontradas")

    return [schemas.Transacao(**transacao) for transacao in transacoes]


@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/ocr/metadados", response_model=schemas.OCRMetadata, tags=['OCR'])
def get_metadados_by_matricula(cartorio_num: int, matricula:str):

    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    cartorio_num = str(cartorio_num)
    ocr = queries.get_pages_by_matricula(data, cartorio_num, matricula)
    if not ocr:
        raise HTTPException(status_code=404, detail="Metados do OCR não encontrados")
    
    parsed = {
        'page_count': ocr['num_paginas'],
        'ocr_available': True
    }

    return schemas.OCRMetadata(**parsed)

@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/ocr/{page_num}", response_model=schemas.Page, tags=['OCR'])
def get_paginas_by_matricula(cartorio_num: int, matricula: str, page_num: int) -> schemas.Page:
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(cartorio_num)
    paginas = queries.get_pages_by_matricula(data, cartorio_num, matricula)
    if not paginas:
        raise HTTPException(status_code=404, detail="Páginas não encontradas")
    paginas_ocr = paginas['ocr']
    if page_num < 0 or page_num > len(paginas_ocr):
        raise HTTPException(status_code=404, detail="Número da página inválido")
    page_num = page_num-1
    pagina_ocr_content = paginas_ocr[page_num]

    parsed = {
        'page_number' : page_num+1,
        'ocr_content' : pagina_ocr_content,
        'size' : len(pagina_ocr_content),
        "page_count" : len(paginas_ocr)
    }

    return schemas.Page(**parsed)

