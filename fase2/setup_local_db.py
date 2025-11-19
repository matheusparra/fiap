import sqlite3
import os

DB_FILE = "farm.db"

def init_local_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE) # Reset db for clean simulation
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    print("Criando tabelas do EcoWork (SQLite)...")
    
    # 1. Colaboradores
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT,
            department TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Estações de Trabalho
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workstations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. Sensores
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id TEXT PRIMARY KEY,
            workstation_id TEXT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            unit TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(workstation_id) REFERENCES workstations(id)
        )
    """)
    
    # 4. Leituras
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            value REAL NOT NULL,
            recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sensor_id) REFERENCES sensors(id)
        )
    """)
    
    # 5. Eventos de Bem-estar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wellbeing_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            event_type TEXT NOT NULL,
            score INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Banco de dados EcoWork inicializado localmente!")

if __name__ == "__main__":
    init_local_db()
