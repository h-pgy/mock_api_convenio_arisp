from .models import Model


def get_all_matriculas(data:Model)->list[dict]:

    return data.query_full_table('matriculas')


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

def get_sqls_by_matricula(data:Model, cartorio_num:str, matricula:str)->list[dict]:

    return data.query_table_where('sqls', {'cartorio_num' : cartorio_num, 'matricula': matricula})

def get_sqls_by_cnm(data:Model, cnm:str)->list[dict]:

    return data.query_table_where('sqls', {'cnm': cnm})

def get_ccirs_by_matricula(data:Model, cartorio_num:str, matricula:str)->list[dict]:

    return data.query_table_where('ccirs', {'cartorio_num' : cartorio_num, 'matricula': matricula})

def get_ccirs_by_cnm(data:Model, cnm:str)->list[dict]:

    return data.query_table_where('ccirs', {'cnm': cnm})


def get_transacoes_by_matricula(data:Model, cartorio_num:str, matricula:str)->list[dict]:

    return data.query_table_where('transacoes', {'cartorio_num' : cartorio_num, 'matricula': matricula})

def get_transacoes_by_cnm(data:Model, cnm:str)->list[dict]:

    return data.query_table_where('transacoes', {'cnm': cnm})


def get_pages_by_matricula(data:Model, cartorio_num:str, matricula:str)->list[dict]:

    return data.query_table_where('ocrs', {'cartorio_num' : cartorio_num, 'matricula': matricula})

def get_pages_by_cnm(data:Model, cnm:str)->list[dict]:

    return data.query_table_where('ocrs', {'cnm': cnm})