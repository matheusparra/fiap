from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Leitura, LeituraCreate
from app.services import sensor_service

router = APIRouter()

@router.post("/registrar", response_model=Leitura)
def registrar_leitura_endpoint(payload: LeituraCreate):
    return sensor_service.registrar_leitura(payload)

@router.get("/ultimas", response_model=List[Leitura])
def ultimas_leituras_endpoint(campo_id: int, limit: int = 20):
    return sensor_service.get_ultimas_leituras(campo_id, limit)

@router.get("/serie")
def serie_temporal_endpoint(campo_id: int, limit: int = 100):
    return sensor_service.get_serie_temporal(campo_id, limit)