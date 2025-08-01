from .random_strings import random_int_string
from typing import Optional

class DocumentIDGen:

    def __init__(self):

        self.random_int_string = random_int_string

    @property
    def matricula(self) -> str:
        return self.random_int_string([2, 3], separator='.')

    @property
    def sql(self) -> str:
        return self.random_int_string([3, 3, 4, 2], separator='.', final_separator='-')

    @property
    def cnm(self) -> str:
        return self.random_int_string([6, 1, 7, 2], separator='.', final_separator='-')

    @property
    def ccir(self) -> str:
        return self.random_int_string([3, 3, 3, 3, 1], separator='.', final_separator='-')

    @property
    def cpf(self) -> str:
        return self.random_int_string([3, 3, 3, 2], separator='.', final_separator='-')

    @property
    def rg(self) -> str:
        return self.random_int_string([2, 3, 3, 1], separator='.', final_separator='-')

    @property
    def num_registro(self) -> str:
        return self.random_int_string([2, 3, 3], separator='.', final_separator='/')

    
    