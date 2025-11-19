"""
Script para criação do banco de dados e inserção de dados iniciais.
"""
from pathlib import Path

from . import db_utils


def main() -> None:
    # Cria o banco e tabelas
    db_utils.create_db()
    # Insere alguns sensores genéricos
    sensors = [
        ("Sensor Umidade", "moisture", "Sensor de umidade do solo"),
        ("Sensor pH", "ph", "Sensor de pH do solo"),
        ("Sensor Nutrientes", "nutrients", "Sensor de nutrientes do solo"),
    ]
    for name, tipo, desc in sensors:
        sensor_id = db_utils.insert_sensor(name, tipo, desc)
        print(f"Sensor inserido: {sensor_id} – {name}")


if __name__ == "__main__":
    main()