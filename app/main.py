# main.py
# Ponto de entrada da API FarmTech integrada
# Pensado para ser consumido por um frontend hospedado no Firebase Hosting

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

import uvicorn
import os

# ====== IMPORTS DAS FASES (ajustar conforme seus módulos) ======
# Fase 1 – Cálculos de área e insumos
try:
    from fase1.calculator import calcular_area, calcular_insumos  # EXEMPLO – ajuste se os nomes forem outros
except ImportError:
    calcular_area = None
    calcular_insumos = None

# Fase 2 – Banco de dados
try:
    from fase2.db_utils import get_connection  # EXEMPLO – ajuste para suas funções reais
except ImportError:
    get_connection = None

# Fase 3 – Simulação / controle
# (opcionalmente você pode expor alguma função do simulador aqui)
# from fase3.simulador import algo...

# Fase 4 – ML (modelo de irrigação)
import pickle
from pathlib import Path

MODEL_PATH = Path("fase4/model.pkl")
ml_model = None
if MODEL_PATH.exists():
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)

# Fase AWS Alerts
try:
    from aws_alerts.send_alert import send_alert  # ajuste nome da função se for diferente
except ImportError:
    send_alert = None

# ================================================================
# MODELOS DE ENTRADA/SAÍDA (schemas da API)
# ================================================================

class CampoRequest(BaseModel):
    largura: float
    comprimento: float
    cultura: str


class InsumoResponse(BaseModel):
    area_m2: float
    insumos: dict


class IrrigacaoRequest(BaseModel):
    umidade: float
    ph: float
    nutrientes: float
    temperatura: Optional[float] = None


class IrrigacaoResponse(BaseModel):
    recomendacao: str
    probabilidade: Optional[float] = None


# ================================================================
# CRIAÇÃO DO APP FASTAPI
# ================================================================

app = FastAPI(
    title="FarmTech API",
    description="Backend da solução agrícola integrada (Fase 7) para consumo por frontend Firebase.",
    version="0.1.0",
)

# CORS – libera o frontend do Firebase
FRONTEND_ORIGINS = [
    "http://localhost:3000",  # desenvolvimento local
    "http://localhost:5173",
    # Adicione aqui a URL do seu app no Firebase Hosting, ex:
    # "https://farmtech-web.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================================================
# ENDPOINTS BÁSICOS
# ================================================================

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "FarmTech API rodando"}


# ---------- FASE 1: CÁLCULO DE INSUMOS ----------

@app.post("/api/insumos/calcular", response_model=InsumoResponse)
def api_calcular_insumos(payload: CampoRequest):
    if calcular_area is None or calcular_insumos is None:
        raise HTTPException(status_code=500, detail="Módulo de cálculo (fase1) não está configurado.")

    # Exemplo: calcular área e depois insumos com base na cultura
    area = calcular_area(payload.largura, payload.comprimento)
    insumos = calcular_insumos(area, payload.cultura)

    return InsumoResponse(area_m2=area, insumos=insumos)


# ---------- FASE 2 / 3: LEITURAS DE SENSORES ----------

@app.get("/api/sensores/ultimas")
def api_ultimas_leituras(limit: int = 10):
    """
    Retorna as últimas leituras de sensores armazenadas no BD (fase2/fase3).
    Ajuste o SQL conforme seu schema.
    """
    if get_connection is None:
        raise HTTPException(status_code=500, detail="Módulo de banco de dados (fase2) não está configurado.")

    conn = get_connection()
    cur = conn.cursor()

    # Exemplo de tabela: leituras_sensores (ajuste para o seu schema real)
    cur.execute(
        """
        SELECT id, campo_id, umidade, ph, nutrientes, temperatura, timestamp
        FROM leituras_sensores
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    colunas = ["id", "campo_id", "umidade", "ph", "nutrientes", "temperatura", "timestamp"]
    leituras = [dict(zip(colunas, row)) for row in rows]

    return {"leituras": leituras}


# ---------- FASE 4: RECOMENDAÇÃO DE IRRIGAÇÃO (ML) ----------

@app.post("/api/irrigacao/recomendacao", response_model=IrrigacaoResponse)
def api_recomendacao_irrigacao(payload: IrrigacaoRequest):
    if ml_model is None:
        # Aqui você pode optar por uma lógica simples caso o modelo não exista
        recomendacao = "modelo_nao_treinado"
        return IrrigacaoResponse(recomendacao=recomendacao, probabilidade=None)

    # Exemplo: montar o vetor de features esperado pelo modelo
    # Ajuste a ordem e número de features conforme seu train_model.py
    features = [[payload.umidade, payload.ph, payload.nutrientes]]

    try:
        pred = ml_model.predict(features)[0]
        # Se tiver predict_proba:
        prob = None
        if hasattr(ml_model, "predict_proba"):
            prob = float(ml_model.predict_proba(features)[0].max())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar recomendação: {e}")

    # Exemplo: mapear 0/1 pra texto
    if pred == 1:
        recomendacao = "irrigar"
    else:
        recomendacao = "nao_irrigar"

    return IrrigacaoResponse(recomendacao=recomendacao, probabilidade=prob)


# ---------- AWS ALERTS: DISPARO DE ALERTA ----------

@app.post("/api/alertas/teste")
def api_alerta_teste():
    if send_alert is None:
        raise HTTPException(status_code=500, detail="Módulo de alerta da AWS não configurado.")

    try:
        send_alert("Alerta de teste da API FarmTech")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar alerta: {e}")

    return {"status": "enviado"}


# ================================================================
# PONTO DE ENTRADA (para rodar localmente)
# ================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
