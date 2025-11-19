-- Tabela de sensores instalados na fazenda
CREATE TABLE IF NOT EXISTS sensors (
    id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name        text NOT NULL,
    type        text NOT NULL,      -- ex: "umidade", "temperatura", "bem-estar"
    location    text NOT NULL,      -- ex: "estufa 1", "curral A"
    created_at  timestamptz DEFAULT now()
);

-- Leituras de cada sensor
CREATE TABLE IF NOT EXISTS sensor_readings (
    id           bigserial PRIMARY KEY,
    sensor_id    uuid REFERENCES sensors(id),
    value        numeric(10, 2) NOT NULL,
    unit         text NOT NULL,    -- ex: "%", "°C", "pontos"
    recorded_at  timestamptz DEFAULT now()
);
