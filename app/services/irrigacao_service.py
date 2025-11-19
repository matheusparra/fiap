# app/services/irrigacao_service.py
import pickle
from pathlib import Path
from app.models import IrrigacaoRequest, IrrigacaoResponse

# Caminho relativo ao local de execução (raiz do projeto)
MODEL_PATH = Path("fase4/model.pkl")
ml_model = None

# Carrega o modelo uma única vez na inicialização
if MODEL_PATH.exists():
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)
else:
    print(f"AVISO: Modelo não encontrado em {MODEL_PATH}")

def predizer_irrigacao(payload: IrrigacaoRequest) -> IrrigacaoResponse:
    """
    Recebe os dados do sensor, aplica no modelo ML e retorna a recomendação.
    """
    if ml_model is None:
        return IrrigacaoResponse(
            recomendacao="modelo_nao_carregado",
            probabilidade=None
        )

    try:
        # Prepara features conforme o treinamento (Umidade, pH, Nutrientes)
        features = [[payload.umidade, payload.ph, payload.nutrientes]]
        
        # Realiza a predição (0 ou 1)
        pred = ml_model.predict(features)[0]
        
        # Tenta obter a probabilidade (confiança), se o modelo suportar
        prob = 0.0
        if hasattr(ml_model, "predict_proba"):
            prob = float(ml_model.predict_proba(features)[0].max())

        # Traduz a classe (1 = Irrigar, 0 = Não Irrigar)
        recomendacao = "irrigar" if pred == 1 else "nao_irrigar"

        return IrrigacaoResponse(
            recomendacao=recomendacao,
            probabilidade=prob
        )

    except Exception as e:
        print(f"Erro na inferência ML: {e}")
        return IrrigacaoResponse(
            recomendacao="erro_interno",
            probabilidade=0.0
        )