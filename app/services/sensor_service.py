import sqlite3
from datetime import datetime
from typing import List
from app.models import Leitura, LeituraCreate
from app.database import get_connection

def registrar_leitura(payload: LeituraCreate) -> Leitura:
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
    
    # Retorna o objeto criado
    cur.execute("""
        SELECT id, campo_id, umidade, ph, nutrientes, temperatura, timestamp
        FROM leituras_sensores WHERE id = ?
    """, (leitura_id,))
    row = cur.fetchone()
    conn.close()
    
    return Leitura(
        id=row[0], campo_id=row[1], umidade=row[2],
        ph=row[3], nutrientes=row[4], temperatura=row[5],
        timestamp=row[6]
    )

def get_ultimas_leituras(campo_id: int, limit: int = 20) -> List[Leitura]:
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
        ) for r in rows
    ]

def get_serie_temporal(campo_id: int, limit: int = 100):
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
    
    # Inverte para o gráfico (antigo -> recente)
    return {
        "campo_id": campo_id,
        "pontos": [
            {
                "timestamp": r[0], "umidade": r[1], "ph": r[2],
                "nutrientes": r[3], "temperatura": r[4]
            } for r in rows[::-1]
        ]
    }