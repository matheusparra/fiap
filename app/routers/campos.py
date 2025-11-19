# app/routes/campos.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Campo, CampoCreate
# Importar o service que contém a lógica do banco
from app.services import campo_service 

router = APIRouter()

@router.post("/", response_model=Campo)
def criar_campo(payload: CampoCreate):
    return campo_service.create_campo(payload)

@router.get("/", response_model=List[Campo])
def listar_campos():
    return campo_service.get_all_campos()