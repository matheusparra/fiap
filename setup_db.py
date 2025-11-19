import sqlite3

def init_db():
    conn = sqlite3.connect("farm.db")
    cur = conn.cursor()
    
    print("Criando tabela leituras_sensores...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leituras_sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campo_id INTEGER,
            umidade REAL,
            ph REAL,
            nutrientes REAL,
            temperatura REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
