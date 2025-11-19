# scripts/init_db.py

from fase2.db_utils import get_connection

DDL_SQL = """
CREATE TABLE IF NOT EXISTS sensors (
    id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name        text NOT NULL,
    type        text NOT NULL,
    location    text NOT NULL,
    created_at  timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id           bigserial PRIMARY KEY,
    sensor_id    uuid REFERENCES sensors(id),
    value        numeric(10, 2) NOT NULL,
    unit         text NOT NULL,
    recorded_at  timestamptz DEFAULT now()
);
"""

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(DDL_SQL)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabelas criadas/atualizadas com sucesso no Supabase!")
