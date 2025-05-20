# from typing import Optional
from pydantic import BaseModel 

class Serie(BaseModel):
    titulo: str
    descricao: str | None
    ano_lancamento: int | None
    id_categoria: int

class Ator(BaseModel):
    nome: str

class Motivo(BaseModel):
    id_serie: int
    motivo: str

class Avaliacao(BaseModel):
    id_serie: int
    nota: int
    comentario: str | None

class Categoria(BaseModel):
    nome: str