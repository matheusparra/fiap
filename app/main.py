# app/main.py
# Backend FastAPI completo para o projeto FarmTech

import os
import pickle
from pathlib import Path
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# MODELOS
from app.models import (
    CampoCreate, Campo,
    LeituraCreate, Leitura,
    IrrigacaoRequest, IrrigacaoResponse
)

# BD
from fase2.db_utils import get_connection

# AWS Alerts opcional
try:
    from aws_alerts.send_alert import send_alert
except:
    send_alert = None


# ============================================================
#              CONFIGURAÇÃO DO APP FASTAPI
# ============================================================

app = FastAPI(
    title="FarmTech API",
    description="API integrada para agricultura inteligente – FIAP – Fase 7",
    version="1.0.0"
)

FRONTEND_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    # adicione o domínio do Firebase quando deployar
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
#                    MODEL DE MACHINE LEARNING
# ============================================================

MODEL_PATH = Path("fase4/model.pkl")
ml_model = None

if MODEL_PATH.exists():
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)


# ============================================================
#                  HEALTHCHECK
# ============================================================

@app.get("/health")
def health_check():
    return {"status": "ok", "api": "FarmTech"}


# ============================================================
#                    CRUD de CAMPOS
# ============================================================

@app.post("/api/campos", response_model=Campo)
def criar_campo(payload: CampoCreate):

    conn = get_connection()
    cur = conn.cursor()

    area = payload.largura * payload.comprimento

    cur.execute("""
        INSERT INTO campos (nome, cultura, largura, comprimento, area_m2)
        VALUES (?, ?, ?, ?, ?)
    """, (payload.nome, payload.cultura, payload.largura, payload.comprimento, area))

    campo_id = cur.lastrowid
    conn.commit()

    cur.execute("""
        SELECT id, nome, cultura, largura, comprimento, area_m2
        FROM campos WHERE id = ?
    """, (campo_id,))

    row = cur.fetchone()
    conn.close()

    return Campo(
        id=row[0], nome=row[1], cultura=row[2],
        largura=row[3], comprimento=row[4], area_m2=row[5]
    )


@app.get("/api/campos", response_model=List[Campo])
def listar_campos():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome, cultura, largura, comprimento, area_m2
        FROM campos ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        Campo(
            id=r[0], nome=r[1], cultura=r[2],
            largura=r[3], comprimento=r[4], area_m2=r[5]
        )
        for r in rows
    ]


# ============================================================
#               LEITURAS DE SENSORES
# ============================================================

@app.post("/api/sensores/registrar", response_model=Leitura)
def registrar_leitura(payload: LeituraCreate):

    conn = get_connection()
    cur = conn.cursor()

    timestamp = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO leituras_sensores (campo_id, umidade, ph, nutrientes, temperatura, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        payload.campo_id, payload.umidade, payload.ph,
        payload.nutrientes, payload.temperatura, timestamp,
    ))

    leitura_id = cur.lastrowid
    conn.commit()

    cur.execute("""
        SELECT id, campo_id, umidade, ph, nutrientes, temperatura, timestamp
        FROM leituras_sensores
        WHERE id = ?
    """, (leitura_id,))

    row = cur.fetchone()
    conn.close()

    return Leitura(
        id=row[0], campo_id=row[1], umidade=row[2],
        ph=row[3], nutrientes=row[4], temperatura=row[5],
        timestamp=row[6]
    )


@app.get("/api/sensores/ultimas", response_model=List[Leitura])
def ultimas_leituras(campo_id: int, limit: int = 20):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, campo_id, umidade, ph, nutrientes, temperatura, timestamp
        FROM leituras_sensores
        WHERE campo_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (campo_id, limit))

    rows = cur.fetchall()
    conn.close()

    return [
        Leitura(
            id=r[0], campo_id=r[1], umidade=r[2],
            ph=r[3], nutrientes=r[4], temperatura=r[5],
            timestamp=r[6]
        )
        for r in rows
    ]


# ============================================================
#             SÉRIE TEMPORAL PARA GRÁFICOS
# ============================================================

@app.get("/api/sensores/serie")
def serie_temporal(campo_id: int, limit: int = 100):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, umidade, ph, nutrientes, temperatura
        FROM leituras_sensores
        WHERE campo_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (campo_id, limit))

    rows = cur.fetchall()
    conn.close()

    # inverter ordem para gráfico do mais antigo → mais recente
    rows = rows[::-1]

    return {
        "campo_id": campo_id,
        "pontos": [
            {
                "timestamp": r[0],
                "umidade": r[1],
                "ph": r[2],
                "nutrientes": r[3],
                "temperatura": r[4],
            }
            for r in rows
        ]
    }


# ============================================================
#                  RECOMENDAÇÃO (ML)
# ============================================================

@app.post("/api/irrigacao/recomendacao", response_model=IrrigacaoResponse)
def recomendacao_irrigacao(payload: IrrigacaoRequest):

    if ml_model is None:
        return IrrigacaoResponse(
            recomendacao="modelo_nao_treinado",
            probabilidade=None
        )

    try:
        features = [[payload.umidade, payload.ph, payload.nutrientes]]
        pred = ml_model.predict(features)[0]

        prob = None
        if hasattr(ml_model, "predict_proba"):
            prob = float(ml_model.predict_proba(features)[0].max())

        recomendacao = "irrigar" if pred == 1 else "nao_irrigar"

        return IrrigacaoResponse(
            recomendacao=recomendacao,
            probabilidade=prob
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
#                  ALERTA AWS SNS
# ============================================================

@app.post("/api/alertas/teste")
def alerta_teste():

    if send_alert is None:
        raise HTTPException(status_code=500, detail="AWS SNS não configurado")

    try:
        send_alert("🔔 Alerta de teste enviado pela API FarmTech")
        return {"status": "enviado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
#             RUN LOCAL (App Hosting / Cloud Run)
# ============================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
