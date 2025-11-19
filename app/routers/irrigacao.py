from fastapi import APIRouter, HTTPException
from app.models import IrrigacaoRequest, IrrigacaoResponse
from app.services import irrigacao_service

router = APIRouter()

@router.post("/recomendacao", response_model=IrrigacaoResponse)
def recomendacao_endpoint(payload: IrrigacaoRequest):
    return irrigacao_service.predizer_irrigacao(payload)