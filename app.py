from typing import List
from urllib import response
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError
from source import queries, schemas, models


data = models.Model(qtd_imoveis=10)

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


@app.get("/matriculas/cartorios", tags=['Matrículas'])
def get_numeros_cartorios() -> List[int]:
    matriculas = queries.get_all_matriculas(data)
    cartorios = list(set(matricula['cartorio_num'] for matricula in matriculas))
    return cartorios

@app.get("/matriculas/cartorios/{cartorio_num}", response_model=List[schemas.MatriculaSearchData], tags=['Matrículas'])
def get_matriculas_by_cartorio(cartorio_num: int) -> List[schemas.MatriculaSearchData]:

    if not isinstance(cartorio_num, int) or cartorio_num < 0 or cartorio_num > 100:
        raise HTTPException(status_code=422, detail="Cartório inválido")

    cartorio_num = str(cartorio_num)
    matriculas = queries.get_matriculas_by_cartorio(data, cartorio_num)
    if not matriculas:
        raise HTTPException(status_code=404, detail="Cartório não encontrado")

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


@app.get('/matriculas/transacoes', response_model=List[schemas.Transacao], tags=['Transações'])
def get_transacoes_by_cnm(cnm: str) -> List[schemas.Transacao]:
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    transacoes = queries.get_transacoes_by_cnm(data, search.cnm)
    if not transacoes:
        raise HTTPException(status_code=404, detail="Transações não encontradas")

    return [schemas.Transacao(**transacao) for transacao in transacoes]


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


@app.get("/matriculas/sqls", response_model=List[schemas.SQL], tags=['SQL'])
def get_sqls_by_cnm(cnm: str) -> List[schemas.SQL]:
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    dados_bd= queries.get_sqls_by_cnm(data, search.cnm)
    if not dados_bd:
        raise HTTPException(status_code=404, detail="SQLs não encontrados")
    sql_data = dados_bd['sqls']
    
    dados_final = []
    for sql in sql_data:
        parsed = {
            'cartorio_num': dados_bd['cartorio_num'],
            'matricula': dados_bd['matricula'],
            'cnm': dados_bd['cnm'],
            'sql' : sql,
            'setor' : sql[:3],
            'quadra' : sql[4:7],
            'lote' : sql[8:12],
            'condominio' : sql[13:15]
        }
        dados_final.append(parsed)

    return [schemas.SQL(**parsed_data) for parsed_data in dados_final]


@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/sqls", response_model=List[schemas.SQL], tags=['SQL'])
def get_sqls_by_matricula(cartorio_num: int, matricula: str) -> List[schemas.SQL]:
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(search.cartorio_num)
    dados_bd= queries.get_sqls_by_matricula(data, cartorio_num, search.matricula)
    if not dados_bd:
        raise HTTPException(status_code=404, detail="SQLs não encontrados")
    sql_data = dados_bd['sqls']
    


    dados_final = []
    for sql in sql_data:
        parsed = {
            'cartorio_num': dados_bd['cartorio_num'],
            'matricula': dados_bd['matricula'],
            'cnm': dados_bd['cnm'],
            'sql' : sql,
            'setor' : sql[:3],
            'quadra' : sql[4:7],
            'lote' : sql[8:12],
            'condominio' : sql[13:15]
        }
        dados_final.append(parsed)

    return [schemas.SQL(**parsed_data) for parsed_data in dados_final]

@app.get("/matriculas/ccirs", response_model=List[schemas.CCIR], tags=['CCIR'])
def get_ccirs_by_cnm(cnm: str) -> List[schemas.CCIR]:
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    dados_bd = queries.get_ccirs_by_cnm(data, search.cnm)
    if not dados_bd:
        raise HTTPException(status_code=404, detail="CCIRs não encontrados")
    
    ccirs_data = dados_bd['ccirs']
    
    dados_final = []
    for ccir in ccirs_data:
        parsed = {
            'cartorio_num': dados_bd['cartorio_num'],
            'matricula': dados_bd['matricula'],
            'cnm': dados_bd['cnm'],
            'ccir' : ccir
        }
        dados_final.append(parsed)

    return [schemas.CCIR(**parsed_data) for parsed_data in dados_final]

@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/ccirs", response_model=List[schemas.CCIR], tags=['CCIR'])
def get_ccirs_by_matricula(cartorio_num: int, matricula: str) -> List[schemas.CCIR]:
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(search.cartorio_num)
    dados_bd = queries.get_ccirs_by_matricula(data, cartorio_num, search.matricula)
    if not dados_bd:
        raise HTTPException(status_code=404, detail="CCIRs não encontrados")

    ccirs_data = dados_bd['ccirs']

    dados_final = []
    for ccir in ccirs_data:
        parsed = {
            'cartorio_num': dados_bd['cartorio_num'],
            'matricula': dados_bd['matricula'],
            'cnm': dados_bd['cnm'],
            'ccir': ccir
        }
        dados_final.append(parsed)

    return [schemas.CCIR(**parsed_data) for parsed_data in dados_final]


@app.get("/matriculas/proprietarios/", response_model=List[schemas.ProprietarioFull], tags=['Proprietários'])
def get_proprietarios_by_cnm(cnm: str) -> List[schemas.ProprietarioFull]:

    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


    proprietarios = queries.get_proprietarios_by_cnm(data, search.cnm)
    if not proprietarios:
        raise HTTPException(status_code=404, detail="Proprietários não encontrados")

    return [schemas.ProprietarioFull(**proprietario) for proprietario in proprietarios]

@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/proprietarios/", response_model=List[schemas.ProprietarioFull], tags=['Proprietários'])
def get_proprietarios_by_matricula(cartorio_num: int, matricula: str) -> List[schemas.ProprietarioFull]:
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(cartorio_num)
    proprietarios = queries.get_proprietarios_by_matricula(data, cartorio_num, matricula)
    if not proprietarios:
        raise HTTPException(status_code=404, detail="Proprietários não encontrados")

    return [schemas.ProprietarioFull(**proprietario) for proprietario in proprietarios]


@app.get("/matriculas/ocr/{page_num}", response_model=schemas.Page, tags=['OCR'])
def get_paginas_by_cnm(cnm: str, page_num: int) -> schemas.Page:
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    ocr = queries.get_pages_by_cnm(data, search.cnm)
    if not ocr:
        raise HTTPException(status_code=404, detail="Páginas não encontradas")
    
    paginas_ocr = ocr['ocr']
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


@app.get("/matriculas/metadados/ocr", response_model=schemas.OCRMetadata, tags=['OCR'])
def get_metadados_by_cnm(cnm: str):
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    ocr = queries.get_pages_by_cnm(data, search.cnm)
    if not ocr:
        raise HTTPException(status_code=404, detail="Metados do OCR não encontrados")
    
    parsed = {
        'page_count': ocr['num_paginas'],
        'ocr_available': True
    }

    return schemas.OCRMetadata(**parsed)

@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/metadados/ocr/", response_model=schemas.OCRMetadata, tags=['OCR'])
def get_metadados_by_matricula(cartorio_num: int, matricula:str):

    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    cartorio_num = str(search.cartorio_num)
    ocr = queries.get_pages_by_matricula(data, cartorio_num, search.matricula)
    if not ocr:
        raise HTTPException(status_code=404, detail="Metados do OCR não encontrados")
    
    parsed = {
        'page_count': ocr['num_paginas'],
        'ocr_available': True
    }

    return schemas.OCRMetadata(**parsed)

@app.get("/matriculas/files/metadados", response_model=schemas.FileMetadata, tags=['Files'])
def get_file_metadados_by_cnm(cnm: str):
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    file_metadata = queries.get_file_metadata_by_cnm(data, search.cnm)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="Metadados do arquivo não encontrados")

    return schemas.FileMetadata(**file_metadata)

@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/files/metadados", response_model=schemas.FileMetadata, tags=['Files'])
def get_file_metadados_by_matricula(cartorio_num: int, matricula: str):
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(search.cartorio_num)
    file_metadata = queries.get_file_metadata_by_matricula(data, cartorio_num, search.matricula)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="Metadados do arquivo não encontrados")

    return schemas.FileMetadata(**file_metadata)

@app.get("/matriculas/files/content", response_model=bytes, tags=['Files'])
def get_file_content_by_cnm(cnm: str):
    try:
        search = schemas.CNMSearch(cnm=cnm)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    file_metadata = queries.get_file_metadata_by_cnm(data, search.cnm, return_file_path=True)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="Metadados do arquivo não encontrados")

    file_path = file_metadata['file_path']

    return FileResponse(path=file_path, filename=file_path, media_type="application/pdf")


@app.get("/matriculas/cartorios/{cartorio_num}/{matricula}/files/content", response_model=bytes, tags=['Files'])
def get_file_content_by_matricula(cartorio_num: int, matricula: str):
    try:
        search = schemas.MatriculaSearch(matricula=matricula, cartorio_num=cartorio_num)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    cartorio_num = str(search.cartorio_num)
    file_metadata = queries.get_file_metadata_by_matricula(data, cartorio_num, search.matricula, return_file_path=True)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="Metadados do arquivo não encontrados")
    
    file_path = file_metadata['file_path']

    return FileResponse(path=file_path, filename=file_path, media_type="application/pdf")
