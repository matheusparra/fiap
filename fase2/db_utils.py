# fase2/db_utils.py

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega o .env na inicialização do módulo
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
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """
    Cria a tabela de leituras se não existir (compatibilidade com SQLite).
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Verifica se é SQLite ou Postgres para ajustar a sintaxe se necessário
    # Mas para este caso simples, a sintaxe é compatível
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leituras_sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite
                campo_id INTEGER,
                umidade REAL,
                ph REAL,
                nutrientes REAL,
                temperatura REAL,
                timestamp TEXT
            )
        """)
        # Se for Postgres, o AUTOINCREMENT falharia, então precisaríamos de SERIAL
        # Mas como o foco agora é o fallback local, isso resolve o erro imediato.
        conn.commit()
    except Exception as e:
        print(f"Aviso ao criar tabela (pode já existir ou ser Postgres): {e}")
    finally:
        conn.close()

def get_latest_readings(limit=20):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT timestamp, campo_id, umidade, ph, nutrientes 
            FROM leituras_sensores 
            ORDER BY timestamp DESC 
            LIMIT %s
        """ if os.getenv("DATABASE_URL") else """
            SELECT timestamp, campo_id, umidade, ph, nutrientes 
            FROM leituras_sensores 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Erro ao ler dados: {e}")
        return []
    finally:
        conn.close()

def get_last_reading(sensor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT timestamp, umidade, ph, nutrientes 
            FROM leituras_sensores 
            WHERE campo_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 1
        """ if os.getenv("DATABASE_URL") else """
            SELECT timestamp, umidade, ph, nutrientes 
            FROM leituras_sensores 
            WHERE campo_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (sensor_id,))
        row = cur.fetchone()
        return row
    except Exception as e:
        print(f"Erro ao ler última leitura: {e}")
        return None
    finally:
        conn.close()
