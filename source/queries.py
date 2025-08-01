from .models import Model
import os
from PyPDF2 import PdfReader
from .utils.file_io import read_binary_file

def get_all_matriculas(data:Model)->list[dict]:

    return data.query_full_table('matriculas')


def get_matriculas_by_cartorio(data:Model, cartorio_num:str)->list[dict]:

    return data.query_table_where('matriculas', {'cartorio_num': cartorio_num})


def get_matricula_data_by_matricula(data:Model, cartorio_num:str, matricula:str)->dict:

    results = data.query_table_where('matriculas', {'cartorio_num': cartorio_num, 'matricula': matricula})
    if results:
        return results[0]
    return {}

def get_matricula_data_by_cnm(data:Model, cnm:str)->dict:

    results = data.query_table_where('matriculas', {'cnm': cnm})
    if results:
        return results[0]
    return {}

def get_sqls_by_matricula(data:Model, cartorio_num:str, matricula:str)->dict:

    results = data.query_table_where('sqls', {'cartorio_num' : cartorio_num, 'matricula': matricula})

    if not results:
        return {}
    
    return results[0]

def get_sqls_by_cnm(data:Model, cnm:str)->dict:

    results = data.query_table_where('sqls', {'cnm': cnm})

    if not results:
        return {}
    
    return results[0]

def get_ccirs_by_matricula(data:Model, cartorio_num:str, matricula:str)->dict:

    results = data.query_table_where('ccirs', {'cartorio_num' : cartorio_num, 'matricula': matricula})
    if not results:
        return {}
    return results[0]

def get_ccirs_by_cnm(data:Model, cnm:str)->dict:

    results = data.query_table_where('ccirs', {'cnm': cnm})
    if not results:
        return {}
    return results[0]


def get_transacoes_by_matricula(data:Model, cartorio_num:str, matricula:str)->list[dict]:

    return data.query_table_where('transacoes', {'cartorio_num' : cartorio_num, 'matricula': matricula})

def get_transacoes_by_cnm(data:Model, cnm:str)->list[dict]:

    return data.query_table_where('transacoes', {'cnm': cnm})


def get_pages_by_matricula(data:Model, cartorio_num:str, matricula:str)->dict:

    results = data.query_table_where('ocrs', {'cartorio_num' : cartorio_num, 'matricula': matricula})
    if results:
        return results[0]
    return {}

def get_pages_by_cnm(data:Model, cnm:str)->dict:

    results = data.query_table_where('ocrs', {'cnm': cnm})
    if results:
        return results[0]
    return {}

def get_proprietarios_by_matricula(data:Model, cartorio_num:str, matricula:str)->list[dict]:

    return data.query_table_where('proprietarios', {'cartorio_num' : cartorio_num, 'matricula': matricula})

def get_proprietarios_by_cnm(data:Model, cnm:str)->list[dict]:

    return data.query_table_where('proprietarios', {'cnm': cnm})



def get_file_metadata_by_matricula(data:Model, cartorio_num:str, matricula:str, return_file_path:bool=False)->dict:

    dados = get_matricula_data_by_matricula(data, cartorio_num, matricula)
    if not dados:
        return {}

    file_path = dados['matricula_pdf_file']
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    id_ = file_path.split('/')[-1].split('.')[0]
    dados = {
        'file_id' : id_,
        'file_name': file_name,
        'file_size': file_size,
        'page_count': num_pages
    }

    if return_file_path:
        dados['file_path'] = file_path

    return dados

def get_file_metadata_by_cnm(data:Model, cnm:str, return_file_path:bool=False)->dict:

    dados = get_matricula_data_by_cnm(data, cnm)
    if not dados:
        return {}

    file_path = dados['matricula_pdf_file']
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    id_ = file_path.split('/')[-1].split('.')[0]
    dados = {
        'file_id' : id_,
        'file_name': file_name,
        'file_size': file_size,
        'page_count': num_pages
    }

    if return_file_path:
        dados['file_path'] = file_path

    return dados


