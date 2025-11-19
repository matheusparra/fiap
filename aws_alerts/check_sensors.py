"""
Monitoramento de sensores e disparo de alertas (Fase 5).

Este script consulta periodicamente o banco de dados em busca de leituras
críticas e dispara alertas através do Amazon SNS, utilizando o módulo
send_alert.py.
"""
import time
from datetime import datetime

from ..fase2 import db_utils
from . import send_alert
from ..fase3 import control


INTERVALO_SEGUNDOS = 60  # frequência de verificação


def verificar_leituras() -> None:
    # Assume sensor_id 1 para umidade
    leitura = db_utils.get_last_reading(1)
    if leitura is None:
        return
    timestamp, moisture, ph, nutrients = leitura
    mensagens = []
    if moisture < control.UMIDADE_MIN:
        mensagens.append(
            f"Umidade baixa ({moisture:.1f}%), recomenda-se acionar a irrigação."
        )
    if not (control.PH_MIN <= ph <= control.PH_MAX):
        mensagens.append(
            f"pH fora da faixa ideal ({ph:.2f}). É necessário corrigir a acidez."
        )
    if mensagens:
        texto = f"Alerta gerado em {datetime.now()}:\n" + "\n".join(mensagens)
        send_alert.enviar_alerta(texto, "Alerta de Sensores FarmTech")


def main() -> None:
    print("Iniciando monitoramento de sensores para alertas...")
    try:
        while True:
            verificar_leituras()
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("Monitoramento de alertas encerrado.")


if __name__ == "__main__":
    main()