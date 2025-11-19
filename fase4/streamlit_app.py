"""
Dashboard unificado para todas as fases (Fase 4).

Utiliza Streamlit para apresentar uma interface interativa que permite ao
usuário executar funções de cálculo (fase 1), visualizar e manipular o
banco de dados (fase 2), monitorar leituras de sensores (fase 3),
visualizar predições (fase 4) e enviar imagens para análise de visão
computacional (fase 6).
"""
import streamlit as st
import pandas as pd

from ..fase1 import calculator
from ..fase2 import db_utils
from ..fase3 import control


def pagina_fase1() -> None:
    st.header("Fase 1 – Cálculo de Insumos")
    st.write("Informe as dimensões da área e selecione a cultura para calcular os insumos.")
    comprimento = st.number_input("Comprimento (m)", min_value=0.0, step=1.0)
    largura = st.number_input("Largura (m)", min_value=0.0, step=1.0)
    cultura = st.selectbox("Cultura", ["cafe", "soja"])
    if st.button("Calcular"):
        area = calculator.calcular_area(comprimento, largura)
        insumos = calculator.calcular_insumos(cultura, area)
        st.success(f"Área total: {area:.2f} m²")
        df = pd.DataFrame.from_dict(insumos, orient="index", columns=["Quantidade"])
        st.table(df)


def pagina_fase2() -> None:
    st.header("Fase 2 – Banco de Dados")
    st.write("Visualize as últimas leituras registradas.")
    db_utils.create_db()
    leituras = db_utils.get_latest_readings(limit=20)
    if leituras:
        df = pd.DataFrame(
            leituras,
            columns=["Timestamp", "Sensor", "Umidade", "pH", "Nutrientes"],
        )
        st.dataframe(df)
    else:
        st.info("Nenhuma leitura encontrada.")


def pagina_fase3() -> None:
    st.header("Fase 3 – Monitoramento IoT")
    st.write("Avalie a necessidade de irrigação com base nas leituras.")
    if st.button("Avaliar Irrigação"):
        # assume sensor_id=1 para umidade
        st.text("Consultando última leitura...")
        leitura = db_utils.get_last_reading(1)
        if leitura:
            timestamp, moisture, ph, nutrients = leitura
            st.write(f"Última leitura em {timestamp}")
            st.write(f"Umidade: {moisture:.1f}%")
            st.write(f"pH: {ph:.2f}")
            st.write(f"Nutrientes: {nutrients:.2f}")
            # tomar decisão
            acionar = moisture < control.UMIDADE_MIN
            problema_ph = not (control.PH_MIN <= ph <= control.PH_MAX)
            if acionar:
                st.error("Umidade baixa – ativar irrigação!")
            else:
                st.success("Umidade adequada – irrigação desligada.")
            if problema_ph:
                st.warning("pH fora da faixa ideal – avaliar correção do solo.")
        else:
            st.info("Nenhuma leitura encontrada no banco.")


def pagina_fase4() -> None:
    st.header("Fase 4 – Predição de Irrigação (Demo)")
    st.write("Esta seção demonstra uma predição simples de necessidade de irrigação.")
    umidade = st.slider("Umidade do solo (%)", 0.0, 100.0, 50.0)
    # modelo simplificado: se umidade < 30% então irrigar
    if st.button("Predizer"):
        if umidade < 30.0:
            st.error("Predição: Necessário irrigar.")
        else:
            st.success("Predição: Não é necessário irrigar.")


def pagina_fase6() -> None:
    st.header("Fase 6 – Visão Computacional")
    st.write(
        "Envie uma imagem para classificação.  Esta é uma versão simplificada; "
        "a integração com o modelo YOLO será realizada posteriormente."
    )
    arquivo = st.file_uploader("Escolha uma imagem", type=["jpg", "png", "jpeg"])
    if arquivo and st.button("Classificar"):
        st.info(
            "Módulo de visão computacional não implementado nesta demonstração. "
            "Integre o modelo da Fase 6 aqui."
        )


def main() -> None:
    st.set_page_config(page_title="FarmTech Fase 7", page_icon="🌾")
    st.sidebar.title("FarmTech – Fase 7")
    pagina = st.sidebar.selectbox(
        "Selecione a fase:",
        [
            "Fase 1 – Cálculo",
            "Fase 2 – Banco de Dados",
            "Fase 3 – Monitoramento",
            "Fase 4 – Predição",
            "Fase 6 – Visão Computacional",
        ],
    )
    if pagina.startswith("Fase 1"):
        pagina_fase1()
    elif pagina.startswith("Fase 2"):
        pagina_fase2()
    elif pagina.startswith("Fase 3"):
        pagina_fase3()
    elif pagina.startswith("Fase 4"):
        pagina_fase4()
    elif pagina.startswith("Fase 6"):
        pagina_fase6()


if __name__ == "__main__":
    main()