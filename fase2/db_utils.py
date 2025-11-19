"""
Utilitários de banco de dados para a Fase 2.

Este módulo fornece funções para criar o banco de dados SQLite a partir
do esquema SQL, inserir sensores e leituras e consultar dados.
"""

import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional


DB_PATH = Path(__file__).resolve().parent / ".." / "farm.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def create_db(db_path: Path = DB_PATH) -> None:
    """Cria o banco de dados e as tabelas definidas em schema.sql.

    Args:
        db_path: caminho para o arquivo SQLite.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()


def insert_sensor(name: str, tipo: str, description: Optional[str] = None) -> int:
    """Insere um novo sensor.

    Returns o ID do sensor criado.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sensors (name, type, description) VALUES (?, ?, ?)",
            (name, tipo, description),
        )
        conn.commit()
        return cursor.lastrowid


def insert_reading(sensor_id: int, moisture: float, ph: float, nutrients: float) -> None:
    """Insere uma nova leitura de sensor."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO readings (sensor_id, moisture, ph, nutrients) VALUES (?, ?, ?, ?)",
            (sensor_id, moisture, ph, nutrients),
        )
        conn.commit()


def get_latest_readings(limit: int = 10) -> List[Tuple]:
    """Obtém as últimas leituras registradas."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT r.timestamp, s.name, r.moisture, r.ph, r.nutrients "
            "FROM readings r JOIN sensors s ON r.sensor_id = s.id "
            "ORDER BY r.timestamp DESC LIMIT ?",
            (limit,),
        )
        return cursor.fetchall()


def get_last_reading(sensor_id: int) -> Optional[Tuple]:
    """Retorna a última leitura para um sensor específico."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, moisture, ph, nutrients FROM readings "
            "WHERE sensor_id = ? ORDER BY timestamp DESC LIMIT 1",
            (sensor_id,),
        )
        return cursor.fetchone()


if __name__ == "__main__":
    # cria banco e insere um sensor teste
    create_db()
    sensor_id = insert_sensor("Sensor 1", "umidade")
    insert_reading(sensor_id, moisture=40.0, ph=6.5, nutrients=1.0)
    print("Última leitura:", get_last_reading(sensor_id))