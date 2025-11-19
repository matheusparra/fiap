import sqlite3
import uuid
import random
from datetime import datetime, timedelta

DB_FILE = "farm.db"

def get_conn():
    return sqlite3.connect(DB_FILE)

def populate():
    conn = get_conn()
    cur = conn.cursor()
    
    print("Gerando dados simulados...")
    
    # --- 1. Workstations ---
    workstations = [
        {"id": str(uuid.uuid4()), "name": "Open Space A", "location": "Andar 1", "desc": "Área colaborativa"},
        {"id": str(uuid.uuid4()), "name": "Sala de Foco", "location": "Andar 2", "desc": "Silêncio absoluto"},
        {"id": str(uuid.uuid4()), "name": "Cafeteria", "location": "Térreo", "desc": "Área de descompressão"}
    ]
    
    for w in workstations:
        cur.execute("INSERT INTO workstations (id, name, location, description) VALUES (?, ?, ?, ?)",
                   (w["id"], w["name"], w["location"], w["desc"]))
    
    # --- 2. Sensors per Workstation ---
    sensors = []
    for w in workstations:
        # Temp
        s_temp = str(uuid.uuid4())
        cur.execute("INSERT INTO sensors (id, workstation_id, name, type, unit) VALUES (?, ?, ?, ?, ?)",
                   (s_temp, w["id"], f"Temp - {w['name']}", "temperatura", "°C"))
        sensors.append({"id": s_temp, "type": "temperatura", "base": 22 if "Foco" in w["name"] else 24})
        
        # Noise
        s_noise = str(uuid.uuid4())
        cur.execute("INSERT INTO sensors (id, workstation_id, name, type, unit) VALUES (?, ?, ?, ?, ?)",
                   (s_noise, w["id"], f"Ruído - {w['name']}", "ruido", "dB"))
        sensors.append({"id": s_noise, "type": "ruido", "base": 40 if "Foco" in w["name"] else 65})
        
        # CO2
        s_co2 = str(uuid.uuid4())
        cur.execute("INSERT INTO sensors (id, workstation_id, name, type, unit) VALUES (?, ?, ?, ?, ?)",
                   (s_co2, w["id"], f"CO2 - {w['name']}", "co2", "ppm"))
        sensors.append({"id": s_co2, "type": "co2", "base": 400})

    # --- 3. Employees ---
    employees = [
        {"id": str(uuid.uuid4()), "name": "Ana Silva", "role": "Dev", "dept": "Tech"},
        {"id": str(uuid.uuid4()), "name": "Carlos Souza", "role": "Designer", "dept": "Produto"},
        {"id": str(uuid.uuid4()), "name": "Beatriz Costa", "role": "HR", "dept": "RH"},
    ]
    
    for e in employees:
        cur.execute("INSERT INTO employees (id, name, role, department) VALUES (?, ?, ?, ?)",
                   (e["id"], e["name"], e["role"], e["dept"]))

    # --- 4. Historical Readings (Last 24h) ---
    now = datetime.now()
    readings_count = 0
    
    for hour in range(24):
        time_base = now - timedelta(hours=24-hour)
        
        for s in sensors:
            # Generate variations
            val = 0
            if s["type"] == "temperatura":
                val = s["base"] + random.uniform(-1.5, 1.5)
            elif s["type"] == "ruido":
                # More noise during work hours (9-18)
                is_work_hour = 9 <= time_base.hour <= 18
                noise_add = random.uniform(0, 20) if is_work_hour else random.uniform(0, 5)
                val = s["base"] + noise_add
            elif s["type"] == "co2":
                is_work_hour = 9 <= time_base.hour <= 18
                co2_add = random.uniform(100, 400) if is_work_hour else random.uniform(0, 50)
                val = s["base"] + co2_add
            
            cur.execute("INSERT INTO sensor_readings (sensor_id, value, recorded_at) VALUES (?, ?, ?)",
                       (s["id"], val, time_base.isoformat()))
            readings_count += 1

    # --- 5. Wellbeing Events ---
    events = ["estresse", "foco_total", "fadiga", "satisfeito"]
    for e in employees:
        # 2 events per employee
        for _ in range(2):
            evt = random.choice(events)
            score = random.randint(1, 10)
            t = now - timedelta(hours=random.randint(1, 24))
            cur.execute("INSERT INTO wellbeing_events (employee_id, event_type, score, created_at) VALUES (?, ?, ?, ?)",
                       (e["id"], evt, score, t.isoformat()))

    conn.commit()
    conn.close()
    print(f"Simulação concluída! {readings_count} leituras geradas.")

if __name__ == "__main__":
    populate()
