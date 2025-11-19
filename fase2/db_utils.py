# fase2/db_utils.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega o .env na inicialização do módulo
load_dotenv()

def get_connection():
    """
    Retorna uma conexão com o Postgres do Supabase.
    Usa a variável DATABASE_URL definida no .env.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL não encontrado no .env")

    sslmode = os.getenv("SUPABASE_DB_SSLMODE", "require")

    conn = psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor,
        sslmode=sslmode,  # Supabase exige SSL
    )
    return conn
