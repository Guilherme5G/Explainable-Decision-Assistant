from pydantic import BaseModel, Field
from typing import Literal

class EntradaPredicao(BaseModel):
    renda: float = Field(gt=0)
    divida: float = Field(ge=0)
    numero_atrasos: int = Field(ge=0)

class ExplicacaoDecisao(BaseModel):
    regras: list[str]
    folha: int = Field(ge=0)

class SaidaPredicao(BaseModel):
    classe: Literal[0, 1]
    probabilidade_classe_0: float = Field(ge=0, le=1)
    probabilidade_classe_1: float = Field(ge=0, le=1)
    explicacao: ExplicacaoDecisao