# fase2/init_db.py
# Script de criação das tabelas principais no Supabase Postgres
# Alinhado ao projeto GS: monitoramento de ambiente de trabalho e bem-estar

from db_utils import get_connection

DDL_SQL = """
-- Habilita extensão para gerar UUID (normalmente já existe no Supabase)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- 1) Tabela de colaboradores
-- =========================
CREATE TABLE IF NOT EXISTS employees (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name        text NOT NULL,
    role        text,            -- cargo ou função
    department  text,            -- setor
    created_at  timestamptz DEFAULT now()
);

-- =========================
-- 2) Tabela de estações de trabalho / ambientes
-- =========================
CREATE TABLE IF NOT EXISTS workstations (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name        text NOT NULL,
    location    text NOT NULL,        -- ex: "Escritório 1", "Galpão A"
    description text,                 -- descrição livre
    created_at  timestamptz DEFAULT now()
);

-- =========================
-- 3) Tabela de sensores
-- =========================
CREATE TABLE IF NOT EXISTS sensors (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workstation_id uuid REFERENCES workstations(id) ON DELETE SET NULL,
    name           text NOT NULL,       -- ex: "Sensor Temp Estação 1"
    type           text NOT NULL,       -- ex: "temperatura", "ruido", "umidade"
    unit           text NOT NULL,       -- ex: "°C", "dB", "%"
    created_at     timestamptz DEFAULT now()
);

-- Índice para facilitar busca por estação
CREATE INDEX IF NOT EXISTS idx_sensors_workstation_id
    ON sensors (workstation_id);

-- =========================
-- 4) Leituras dos sensores
-- =========================
CREATE TABLE IF NOT EXISTS sensor_readings (
    id           bigserial PRIMARY KEY,
    sensor_id    uuid REFERENCES sensors(id) ON DELETE CASCADE,
    value        numeric(10, 2) NOT NULL,
    recorded_at  timestamptz DEFAULT now()
);

-- Índices para query por sensor e tempo
CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_id
    ON sensor_readings (sensor_id);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_recorded_at
    ON sensor_readings (recorded_at);

-- =========================
-- 5) Eventos de bem-estar (auto-relato)
-- =========================
CREATE TABLE IF NOT EXISTS wellbeing_events (
    id           bigserial PRIMARY KEY,
    employee_id  uuid REFERENCES employees(id) ON DELETE SET NULL,
    event_type   text NOT NULL,       -- ex: "pausa", "estresse", "fadiga", "feedback_positivo"
    score        int,                 -- escala 0-100, opcional
    notes        text,                -- observações livres
    created_at   timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_wellbeing_employee_id
    ON wellbeing_events (employee_id);

CREATE INDEX IF NOT EXISTS idx_wellbeing_created_at
    ON wellbeing_events (created_at);
"""

def init_db():
    """
    Cria/atualiza as tabelas principais no banco Supabase.
    """
    conn = get_connection()
    cur = conn.cursor()
    print("[init_db] Criando/atualizando tabelas...")
    cur.execute(DDL_SQL)
    conn.commit()
    cur.close()
    conn.close()
    print("[init_db] Tabelas criadas/atualizadas com sucesso!")

if __name__ == "__main__":
    init_db()
