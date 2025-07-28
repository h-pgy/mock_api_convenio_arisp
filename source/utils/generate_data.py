from .file_io import save_json_file, get_file
from typing import Union, Optional
import os
import random
import faker import Faker

class DataGen:

    def __init__(self, data_folder: str, static_folder:str) -> None:
        self.data_folder = data_folder
        self.static_folder = static_folder

        if not os.path.exists(self.data_folder):
            raise ValueError(f"The data folder {self.data_folder} does not exist.")
        if not os.path.exists(self.static_folder):
            raise ValueError(f"The static folder {self.static_folder} does not exist.")
        
        self.faker = Faker('pt-br')

        self.matricula_folder = os.path.join(self.static_folder, "matriculas")

    def json_fname(self, file_name: str) -> str:
        if not file_name.endswith('.json'):
            file_name += '.json'
        return get_file(file_name, self.data_folder, raise_if_not_exists=False)

    def save_data(self, data: Union[list, dict], file_name: str) -> None:
        file_path = save_json_file(data, file_name, self.data_folder)
        print(f"Data saved to {file_path}")

    def random_int_string(self, lengths: list[int], separator: str = '.', final_separator:Optional[str]=None) -> str:

        if final_separator is not None:
            final_length = lengths[-1]
            lengths = lengths[:-1]
            generated_string = separator.join(str(random.randint(0, length*10)).zfill(length) for length in lengths)
            generated_string += final_separator + str(random.randint(0, final_length*10)).zfill(final_length)
        else:
            generated_string = separator.join(str(random.randint(0, length*10)).zfill(length) for length in lengths)

        return generated_string

    def gen_matricula(self) -> str:
        return self.random_int_string([2, 3], separator='.')
    
    def gen_sql(self) -> str:
        return self.random_int_string([3, 3, 4, 2], separator='.', final_separator='-')
    
    def gen_cnm(self) -> str:
        return self.random_int_string([6, 1, 7, 2], separator='.', final_separator='-')
    
    def gen_ccir(self) -> str:
        return self.random_int_string([3, 3, 3, 3, 1], separator='.', final_separator='-')
    
    def gen_cpf(self) -> str:
        return self.random_int_string([3, 3, 3, 2], separator='.', final_separator='-')
    
    def gen_rg(self) -> str:
        return self.random_int_string([2, 3, 3, 1], separator='.', final_separator='-')
    
    def gen_num_registro(self) -> str:
        return self.random_int_string([2, 3, 3], separator='.', final_separator='/')

    def path_matricula_file(self) -> str:

        num = random.randint(1, 3)
        fname = f"matricula_{num}.json"
        path = os.path.join(self.matricula_folder, fname)

        return path
    

    def fake_endereco(self) -> str:

        rua = self.faker.street_name()
        numero = self.faker.building_number()
        bairro = self.faker.bairro()

        cidade = 'São Paulo'
        estado = 'SP'

        return f"{rua}, {numero}, {bairro}, cidade de {cidade} - {estado}"
    
    def proprietario_fake_estruturado(self) -> dict:

        nome = self.faker.name()
        cpf = self.gen_cpf()
        rg = self.gen_rg()
        profissao = self.faker.job()

        return {
            "nome": nome,
            "cpf": cpf,
            "rg": rg,
            "profissao": profissao,
            "endereco": self.fake_endereco()
        }
    
    def proprietario_fake_str(self, proprietario:dict) -> str:
        
        solteiro_ou_casado = random.choice(['solteiro', 'casado'])

        if solteiro_ou_casado == 'casado':
            conjuge = self.proprietario_fake_estruturado()

            conjuge_str = f" e seu cônjuge {conjuge['nome']}, CPF {conjuge['cpf']}, RG {conjuge['rg']}, profissão {conjuge['profissao']}"
        else:
            conjuge_str = ''

        return f"{proprietario['nome'].upper()}, CPF {proprietario['cpf']}, RG {proprietario['rg']}, {proprietario['profissao']}{conjuge_str}, residente e domiciliado em {proprietario['endereco']}"
    
    def registro_fake(self, proprietario:dict, data_escritura, endereco:str, rural_ou_urbano:str, sql:str, ccir:str, 
                      numero_cartorio:str, numero_matricula:str) -> str:

        terreno_ou_imovel = random.choices(['Terreno', 'Imóvel'], weights=[0.1, 0.9], k=1)[0]

        largura = random.randint(5, 50)
        comprimento = random.randint(10, 100)
        area_do_terreno = (largura * comprimento)-random.randint(0, 10)
        area_construida = area_do_terreno * 0.9

        frase = (
                f'São Paulo, {data_escritura.strftime("%d de %B de %Y")}. Registro de Imóveis, '
                f'UM {terreno_ou_imovel}, sito à {endereco}, ' 
                 f', com área total de {area_do_terreno} m², medindo {largura} metros de largura por {comprimento} metros de comprimento, '
                 f'confinando de um lado com o lote {random.randint(1, 120)} de outro lado com o lote {random.randint(1, 120)}, e nos fundos com o lote {random.randint(1, 120)}')

        if terreno_ou_imovel == 'Imóvel':
            frase += f', com {area_construida} m² de área construída'

        if rural_ou_urbano == 'Rural':
            cadastro = f', cadastro no Cadastro de Imóveis Rurais(CCIR) sob o número {ccir}'
        else:
            cadastro = f', cadastro sob o número de contribuinte {sql}'

        registro  = f' e registrado neste Cartório de Registro de Imóveis de número {numero_cartorio}, da Comarca de São Paulo, sob o número {numero_matricula}'

        frase += cadastro + registro + '.'

        frase += 'PROPRIETÁRIO: ' + self.proprietario_fake_str(proprietario) + '.'

        frase += ' Registro efetuado em ' + self.faker.date() + '.'

        return frase
    
    def transacao_fake_estruturada(self, comprador:dict, vendedor:dict)->dict:

        
        return {
            "comprador": comprador,
            "vendedor": vendedor,
            "valor" : random.randint(10000, 1000000),
            "data_escritura": self.faker.date_time_this_decade(),
        }


    def transacao_fake_str(self, transacao:dict, num_cartorio:int, endereco_imovel:str)->str:

        data = self.faker.date()
        num_registro = self.gen_num_registro()
        comprador = transacao['comprador']
        vendedor = transacao['vendedor']
        valor = transacao['valor']
        data_escritura = transacao['data_escritura']
        
        frase = (
            f"R. {num_registro} - São Paulo, {data}\n"
            f"Pela escritura pública lavrada em {data_escritura.strftime('%d de %B de %Y')}, no Livro {random.randint(1, 5)}, folhas {random.randint(1, 152)}, "
            f"do {num_cartorio}, {vendedor}, "
            f"**vende** a {comprador}, "
            f"o imóvel situado à {endereco_imovel}, pelo valor de R$ {valor:,.2f}, pagos nesta data.\n"
            f"A aquisição foi feita com recursos próprios do(a) comprador(a), conforme declaração. Registrado sem ônus ou gravames.\n"
            f"O Oficial\n{self.faker.name()}"
        )
        
        return frase
    

        
    def build_main_table(self, n: int, save_data=True) -> list[dict]:

        dados = []
        for _ in range(n):
            numero_cartorio = random.randint(1, 30)
            numero_matricula = self.gen_matricula()
            numeros_sql = [self.gen_sql() for _ in range(random.randint(0, 15))]
            numero_ccir = self.gen_ccir()
            numero_cnm = self.gen_cnm()
            quantidade_paginas = random.randint(1, 50)
            path_matricula_file = self.path_matricula_file()

            rural_urbano = random.choices(['Rural', 'Urbano'], weights=[0.2, 0.8], k=1)[0]
            data_escritura = self.faker.date_time_last_decade()
            endereco_imovel = self.fake_endereco()
            
            proprietario_inicial = self.proprietario_fake_estruturado()

            registro = self.registro_fake(
                proprietario=proprietario_inicial,
                data_escritura=data_escritura,
                endereco=endereco_imovel,
                rural_ou_urbano=rural_urbano,
                sql=numeros_sql[0] if numeros_sql else '',
                ccir=numero_ccir if rural_urbano == 'Rural' else '',
                numero_cartorio=str(numero_cartorio),
                numero_matricula=numero_matricula
            )


            qtd_transacoes = random.randint(0, 50)
            transacoes = [self.transacao_fake_estruturada(comprador=proprietario_inicial, vendedor=self.proprietario_fake_estruturado()) 
                          for _ in range(qtd_transacoes)]
            
            proprietario_final = transacoes[-1]['comprador'] if transacoes else proprietario_inicial

            dados.append({
                "numero_cartorio": numero_cartorio,
                "numero_matricula": numero_matricula,
                "sqls_associados": numeros_sql if rural_urbano == 'Urbano' else None,
                "ccir_associado" : numero_ccir if rural_urbano == 'Rural' else None,
                "numero_cnm": numero_cnm,
                "quantidade_paginas": quantidade_paginas,
                "arquivo_matricula": path_matricula_file,
                "transacoes": transacoes,
                "registro": registro,
                "proprietario" : proprietario_final,
            })

        if save_data:
            self.save_data(dados, self.json_fname("matricula_iptu"))

        return dados