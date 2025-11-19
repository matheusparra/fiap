import sqlite3
import os

DB_FILE = "farm.db"

def init_agro_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE) # Reset for the new context
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    print("Criando tabelas Agro-Sustentável (SQLite)...")
    
    # 1. Setores / Talhões (Hectares)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sectors (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,       -- Ex: "Talhão Norte", "Setor A"
            crop_type TEXT,           -- Ex: "Soja", "Milho", "Pasto", "Floresta"
            area_hectares REAL,       -- Tamanho da área
            status TEXT               -- Ex: "Ativo", "Em Recuperação"
        )
    """)
    
    # 2. Sensores (Foco em CO2, Densidade, Luminosidade)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id TEXT PRIMARY KEY,
            sector_id TEXT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,       -- "co2_emission", "luminosity", "crop_density"
            unit TEXT NOT NULL,       -- "kg/ha", "lux", "plants/m2"
            FOREIGN KEY(sector_id) REFERENCES sectors(id)
        )
    """)
    
    # 3. Leituras
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            value REAL NOT NULL,
            recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sensor_id) REFERENCES sensors(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Banco Agro-Sustentável inicializado!")

if __name__ == "__main__":
    init_agro_db()
