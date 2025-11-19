# app/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==============================
#    MODELOS DE CAMPOS
# ==============================

class CampoCreate(BaseModel):
    nome: str
    cultura: str
    largura: float
    comprimento: float


class Campo(BaseModel):
    id: int
    nome: str
    cultura: str
    largura: float
    comprimento: float
    area_m2: float


# ==============================
#    MODELOS DE LEITURAS
# ==============================

class LeituraCreate(BaseModel):
    campo_id: int
    umidade: float
    ph: float
    nutrientes: float
    temperatura: float


class Leitura(BaseModel):
    id: int
    campo_id: int
    umidade: float
    ph: float
    nutrientes: float
    temperatura: float
    timestamp: datetime


# ==============================
#    MODELOS ML / IA
# ==============================

class IrrigacaoRequest(BaseModel):
    umidade: float
    ph: float
    nutrientes: float
    temperatura: Optional[float] = None


class IrrigacaoResponse(BaseModel):
    recomendacao: str
    probabilidade: Optional[float] = None
