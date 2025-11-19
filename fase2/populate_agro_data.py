import sqlite3
import uuid
import random
from datetime import datetime, timedelta

DB_FILE = "farm.db"

def populate_agro():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    print("Gerando dados da Fazenda Nova Piratininga...")
    
    # --- 1. Setores (Baseado na Fazenda Nova Piratininga - 135k ha) ---
    sectors = [
        {"id": str(uuid.uuid4()), "name": "Talhão Soja Norte (Piratininga)", "crop": "Soja", "area": 25000.0, "status": "Crescimento Vegetativo"},
        {"id": str(uuid.uuid4()), "name": "Talhão Milho Safrinha", "crop": "Milho", "area": 15000.0, "status": "Maturação"},
        {"id": str(uuid.uuid4()), "name": "Pasto Rotacionado (Gado)", "crop": "Pecuária", "area": 60000.0, "status": "Engorda Intensiva"},
        {"id": str(uuid.uuid4()), "name": "Reserva Legal Araguaia", "crop": "Floresta", "area": 30000.0, "status": "Preservação Permanente"},
        {"id": str(uuid.uuid4()), "name": "Represa Principal", "crop": "Recursos Hídricos", "area": 5000.0, "status": "Monitoramento Nível"},
    ]
    
    for s in sectors:
        cur.execute("INSERT INTO sectors (id, name, crop_type, area_hectares, status) VALUES (?, ?, ?, ?, ?)",
                   (s["id"], s["name"], s["crop"], s["area"], s["status"]))
        
    # --- 2. Sensores e Leituras ---
    now = datetime.now()
    
    for s in sectors:
        # Configuração base
        base_co2 = 0
        base_dens = 0
        base_lux = 50000
        base_moisture = 60
        base_milk = 0
        base_ndvi = 0.0 # Índice de Vegetação (0-1)
        base_height = 0 # Altura planta (cm)
        
        if s["crop"] == "Soja":
            base_co2 = 120
            base_dens = 35
            base_moisture = 50
            base_ndvi = 0.75 # Soja vigorosa
            base_height = 45 # cm
        elif s["crop"] == "Milho":
            base_co2 = 350
            base_dens = 7
            base_moisture = 55
            base_ndvi = 0.80
            base_height = 120
        elif s["crop"] == "Pecuária":
            base_co2 = 1500 # Alta emissão
            base_dens = 1.5
            base_milk = 25000 # Alta produção (escala industrial)
            base_ndvi = 0.40 # Pasto
        elif s["crop"] == "Floresta":
            base_co2 = -800 # Alto sequestro
            base_dens = 150
            base_lux = 10000
            base_moisture = 85
            base_ndvi = 0.90
        elif s["crop"] == "Recursos Hídricos":
            base_co2 = 0
            base_dens = 0
            base_lux = 60000
            base_moisture = 100
            
        # Criar Sensores
        sensors = [
            {"type": "co2_emission", "name": "Sensor CO2", "unit": "kg/ha/ano", "base": base_co2},
            {"type": "luminosity", "name": "Luminosidade", "unit": "lux", "base": base_lux},
            {"type": "temperature", "name": "Temperatura", "unit": "°C", "base": 30},
        ]
        
        # Sensores Específicos
        if s["crop"] in ["Soja", "Milho"]:
            sensors.append({"type": "soil_moisture", "name": "Umidade Solo", "unit": "%", "base": base_moisture})
            sensors.append({"type": "crop_density", "name": "Densidade", "unit": "pl/m2", "base": base_dens})
            sensors.append({"type": "ndvi", "name": "NDVI (Satélite)", "unit": "idx", "base": base_ndvi})
            sensors.append({"type": "plant_height", "name": "Altura Planta", "unit": "cm", "base": base_height})
            
        if s["crop"] == "Pecuária":
            sensors.append({"type": "milk_production", "name": "Tanque Expansão", "unit": "L/dia", "base": base_milk})
            sensors.append({"type": "crop_density", "name": "Cabeças/ha", "unit": "cab/ha", "base": base_dens})
            
        if s["crop"] == "Floresta":
            sensors.append({"type": "crop_density", "name": "Densidade Arbórea", "unit": "arv/ha", "base": base_dens})
            sensors.append({"type": "ndvi", "name": "NDVI (Floresta)", "unit": "idx", "base": base_ndvi})

        for sens in sensors:
            s_id = str(uuid.uuid4())
            cur.execute("INSERT INTO sensors (id, sector_id, name, type, unit) VALUES (?, ?, ?, ?, ?)",
                       (s_id, s["id"], sens["name"], sens["type"], sens["unit"]))
            
            # Gerar histórico (últimos 90 dias - Ciclo Vegetativo Completo)
            days_history = 90
            for day in range(days_history):
                t = now - timedelta(days=days_history-day)
                
                # Variação aleatória base
                noise = random.uniform(0.95, 1.05)
                val = sens["base"] * noise
                
                # Lógica de Crescimento (Curva Sigmoide/Linear)
                progress = day / days_history # 0 a 1
                
                if sens["type"] == "plant_height":
                    # Crescimento de 5cm até a altura base (ex: 80cm)
                    # Fórmula simplificada de crescimento logístico
                    start_h = 5
                    target_h = sens["base"]
                    val = start_h + (target_h - start_h) * (progress ** 1.2) # Crescimento levemente exponencial
                    
                elif sens["type"] == "ndvi":
                    # NDVI começa em 0.2 (solo exposto) e vai até base (0.8)
                    # Cresce rápido no início (V1-V4) e estabiliza
                    start_ndvi = 0.25
                    target_ndvi = sens["base"]
                    if progress < 0.6:
                        val = start_ndvi + (target_ndvi - start_ndvi) * (progress / 0.6)
                    else:
                        val = target_ndvi # Estabiliza no fechamento do dossel
                        
                elif sens["type"] == "crop_density":
                    # Densidade cai levemente (perda natural de plantas)
                    val = sens["base"] * (1 - (0.05 * progress))
                
                # Adicionar ruído final
                val = val * random.uniform(0.98, 1.02)
                
                cur.execute("INSERT INTO sensor_readings (sensor_id, value, recorded_at) VALUES (?, ?, ?)",
                           (s_id, val, t.isoformat()))

    conn.commit()
    conn.close()
    print("Dados Piratininga gerados com sucesso!")

if __name__ == "__main__":
    populate_agro()
