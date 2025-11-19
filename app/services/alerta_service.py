# Importa a função existente na pasta aws_alerts
# Certifique-se de que a pasta aws_alerts tem um __init__.py
try:
    from aws_alerts.send_alert import enviar_alerta as send_aws_msg
except ImportError:
    send_aws_msg = None

def enviar_teste_alerta() -> dict:
    if send_aws_msg is None:
        raise Exception("Módulo AWS SNS não encontrado ou não configurado")
    
    send_aws_msg("🔔 Alerta de teste enviado pela API FarmTech Refatorada")
    return {"status": "enviado", "service": "AWS SNS"}