# fase2/db_utils.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    """
    Abre e retorna uma conexão com o banco de dados PostgreSQL.
    Usa variáveis de ambiente para não expor credenciais no código.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        dbname=os.getenv("DB_NAME", "farmtech_fase2"),
        cursor_factory=RealDictCursor
    )
    return conn
