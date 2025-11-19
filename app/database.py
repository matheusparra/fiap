import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Retorna uma conexão com o banco de dados.
    Prioridade: DATABASE_URL (.env) -> Postgres
    Fallback: SQLite (farm.db)
    """
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        try:
            conn = psycopg2.connect(
                database_url,
                cursor_factory=RealDictCursor,
                sslmode=os.getenv("SUPABASE_DB_SSLMODE", "require")
            )
            return conn
        except Exception as e:
            print(f"Erro ao conectar no Postgres: {e}")
            print("Usando SQLite como fallback...")
    
    # Fallback para SQLite
    conn = sqlite3.connect("farm.db")
    conn.row_factory = sqlite3.Row  # Permite acesso por nome das colunas
    return conn
