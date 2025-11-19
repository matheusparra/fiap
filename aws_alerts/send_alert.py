"""
Envio de alertas via Amazon SNS (Fase 5).

Para utilizar este script, configure as credenciais AWS no ambiente (AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY e AWS_REGION) e defina o ARN do tópico SNS abaixo.
"""
import os
from typing import Optional
import boto3

# ARN do tópico SNS criado na AWS.  Substitua pelo seu próprio ARN.
TOPIC_ARN: Optional[str] = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:FarmTechAlerts")


def enviar_alerta(mensagem: str, subject: str = "Alerta FarmTech") -> None:
    """Publica uma mensagem no tópico SNS.

    Args:
        mensagem: conteúdo do alerta.
        subject: título do e‑mail/SMS.
    """
    if not TOPIC_ARN:
        raise ValueError("TOPIC_ARN não configurado")
    sns = boto3.client("sns")
    response = sns.publish(TopicArn=TOPIC_ARN, Message=mensagem, Subject=subject)
    print(f"Mensagem enviada: {response['MessageId']}")


if __name__ == "__main__":
    enviar_alerta("Teste de alerta do FarmTech", "Alerta de Teste")