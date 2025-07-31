from pydantic import BaseModel, Field, field_validator
import re


class Page(BaseModel):
    page_number: int = Field(..., description="Número da página", gt=0)
    ocr_content: str = Field(..., description="Conteúdo OCR da página")
    size: int = Field(..., description="Tamanho da página em caracteres", gt=0)
    page_count: int = Field(..., description="Número total de páginas", gt=0)


class FileMetadata(BaseModel):

    file_id: int = Field(..., description="ID do arquivo", gt=0)
    file_name: str = Field(..., description="Nome do arquivo")
    file_size: int = Field(..., description="Tamanho do arquivo em bytes", gt=0)
    page_count: int = Field(..., description="Número de páginas", gt=0)

