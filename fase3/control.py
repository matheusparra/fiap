"""
Módulo de controle de irrigação (Fase 3).

Consulta as leituras mais recentes dos sensores e determina se as
bombas de irrigação devem ser ativadas.  O módulo apenas imprime a ação
recomendada; em uma implementação real, ele se comunicaria com atuadores.
"""
from __future__ import annotations

from time import sleep

from fase2 import db_utils


# Configurações de limites
UMIDADE_MIN = 30.0  # %
PH_MIN = 6.0
PH_MAX = 7.0


def avaliar_irrigacao(sensor_id: int) -> None:
    """Avalia a última leitura do sensor e imprime decisão."""
    leitura = db_utils.get_last_reading(sensor_id)
    if leitura is None:
        print("Nenhuma leitura encontrada.")
        return
    timestamp, moisture, ph, nutrients = leitura
    acionar = moisture is not None and moisture < UMIDADE_MIN
    problema_ph = ph is not None and not (PH_MIN <= ph <= PH_MAX)
    if acionar:
        print(f"[!] {timestamp} – Umidade {moisture:.1f}%: ativar bomba de irrigação.")
    else:
        print(f"[ ] {timestamp} – Umidade {moisture:.1f}%: irrigação desligada.")
    if problema_ph:
        print(
            f"[!] pH fora da faixa ({ph:.2f}). Recomenda-se ajustar a acidez do solo."
        )


def main() -> None:
    # identifica o primeiro sensor cadastrado (assumindo ID 1)
    sensor_id = 1
    try:
        while True:
            avaliar_irrigacao(sensor_id)
            sleep(15)
    except KeyboardInterrupt:
        print("Monitoramento encerrado.")


if __name__ == "__main__":
    main()