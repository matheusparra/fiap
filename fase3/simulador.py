"""
Simulador de sensores IoT (Fase 3).

Este script gera leituras de sensores de umidade, pH e nutrientes de forma
aleatória e grava os valores no banco de dados.  Útil para testes da
automação e visualização em tempo real.
"""
import random
import time

from ..fase2 import db_utils


def gerar_leitura() -> tuple[float, float, float]:
    """Gera valores aleatórios de umidade, pH e nutrientes."""
    umidade = random.uniform(10, 80)  # %
    ph = random.uniform(5.5, 7.5)  # pH
    nutrientes = random.uniform(0.5, 3.0)  # índice fictício
    return umidade, ph, nutrientes


def main() -> None:
    # Garante que banco existe
    db_utils.create_db()
    # Recupera ou cria sensor genérico para id 1
    moisture_id = db_utils.insert_sensor("Sensor Umidade", "moisture", "Simulador")
    ph_id = db_utils.insert_sensor("Sensor pH", "ph", "Simulador")
    nut_id = db_utils.insert_sensor("Sensor Nutrientes", "nutrients", "Simulador")
    try:
        while True:
            umidade, ph, nutrients = gerar_leitura()
            db_utils.insert_reading(moisture_id, umidade, ph, nutrients)
            print(
                f"Leitura registrada – Umidade: {umidade:.1f}%, pH: {ph:.2f}, Nutrientes: {nutrients:.2f}"
            )
            time.sleep(10)  # envia nova leitura a cada 10 segundos
    except KeyboardInterrupt:
        print("Simulação encerrada.")


if __name__ == "__main__":
    main()