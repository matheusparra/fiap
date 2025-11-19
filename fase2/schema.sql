-- Esquema de banco de dados para o sistema FarmTech (Fase 2)
-- Tabela de sensores
CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT
);

-- Leituras de sensores
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    moisture REAL,
    ph REAL,
    nutrients REAL,
    FOREIGN KEY(sensor_id) REFERENCES sensors(id)
);

-- Eventos de irrigação e alertas
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL,
    description TEXT
);