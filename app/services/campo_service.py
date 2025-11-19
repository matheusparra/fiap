# app/services/campo_service.py
from fase2.db_utils import get_connection # Ajuste o import conforme sua estrutura real
from app.models import Campo, CampoCreate

def create_campo(payload: CampoCreate) -> Campo:
    conn = get_connection()
    cur = conn.cursor()
    area = payload.largura * payload.comprimento
    
    cur.execute("""
        INSERT INTO campos (nome, cultura, largura, comprimento, area_m2)
        VALUES (?, ?, ?, ?, ?)
    """, (payload.nome, payload.cultura, payload.largura, payload.comprimento, area))
    
    campo_id = cur.lastrowid
    conn.commit()
    
    # Recuperar o objeto criado
    cur.execute("SELECT id, nome, cultura, largura, comprimento, area_m2 FROM campos WHERE id = ?", (campo_id,))
    row = cur.fetchone()
    conn.close()
    
    return Campo(id=row[0], nome=row[1], cultura=row[2], largura=row[3], comprimento=row[4], area_m2=row[5])

def get_all_campos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, cultura, largura, comprimento, area_m2 FROM campos ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [Campo(id=r[0], nome=r[1], cultura=r[2], largura=r[3], comprimento=r[4], area_m2=r[5]) for r in rows]