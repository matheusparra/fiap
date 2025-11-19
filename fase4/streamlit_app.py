import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import time

# Configuração da Página
st.set_page_config(page_title="CAPATAZ - Inteligência de Campo", page_icon="🤠", layout="wide")

# --- Simulação de Segurança (Cybersecurity) ---
def check_password():
    """Retorna True se o usuário estiver logado."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if st.session_state["logged_in"]:
        return True

    st.title("🤠 CAPATAZ - Acesso ao Sistema")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        user = st.text_input("Usuário")
        pwd = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            # Em produção, usar hash e banco de dados!
            if user == "admin" and pwd == "fiap2025":
                st.session_state["logged_in"] = True
                st.success("Bem-vindo, Capataz!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
    return False

if not check_password():
    st.stop()

# --- Fim da Segurança ---

def get_data(query):
    conn = sqlite3.connect("farm.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Função para exportar dados para o R
def export_for_r():
    df = get_data("""
        SELECT s.name as sector, sens.type, r.value 
        FROM sensor_readings r
        JOIN sensors sens ON r.sensor_id = sens.id
        JOIN sectors s ON sens.sector_id = s.id
    """)
    df.to_csv("fase4/sensor_data.csv", index=False)
    return "Dados exportados para 'fase4/sensor_data.csv'"

# --- Sidebar ---
st.sidebar.title("🤠 CAPATAZ")
st.sidebar.markdown(f"Logado como: **Admin**")

# --- AGENTE CAPATAZ AI ---
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Agente Capataz")
ai_status = st.sidebar.empty()

def run_agent_analysis():
    """Simula uma análise de IA sobre os dados atuais."""
    insights = []
    
    # Checar CO2
    df_co2 = get_data("SELECT AVG(value) as v FROM sensor_readings r JOIN sensors s ON r.sensor_id=s.id WHERE s.type='co2_emission'")
    avg_co2 = df_co2['v'].iloc[0] if not df_co2.empty else 0
    if avg_co2 > 1000: insights.append("⚠️ Emissões altas detectadas no Pasto.")
    
    # Checar Soja
    df_soy = get_data("SELECT AVG(value) as v FROM sensor_readings r JOIN sensors s ON r.sensor_id=s.id WHERE s.type='ndvi'")
    avg_ndvi = df_soy['v'].iloc[0] if not df_soy.empty else 0
    if avg_ndvi > 0.7: insights.append("✅ Soja com vigor vegetativo excelente (NDVI > 0.7).")
    elif avg_ndvi < 0.4: insights.append("⚠️ Alerta: Baixo vigor na Soja. Verificar pragas.")
    
    return insights

if st.sidebar.button("Rodar Análise IA"):
    with st.spinner("Analisando 135.000 hectares..."):
        time.sleep(1.5)
        results = run_agent_analysis()
        for msg in results:
            st.sidebar.info(msg)
        if not results:
            st.sidebar.success("Tudo operando dentro da normalidade.")

st.sidebar.markdown("---")
if st.sidebar.button("Sair"):
    st.session_state["logged_in"] = False
    st.rerun()

page = st.sidebar.radio("Menu", ["Visão Geral (Piratininga)", "🌱 Análise Soja (NDVI)", "🐄 Gestão Leiteira", "🌍 Gestão de Carbono (ESG)", "Integração R"])

# --- Página 1: Visão Geral ---
if page == "Visão Geral (Piratininga)":
    st.title("🚜 Fazenda Nova Piratininga - Dashboard Geral")
    st.markdown("**Área Total:** 135.000 Hectares | **Foco:** Integração Lavoura-Pecuária")
    
    # KPIs Globais com YoY (Year Over Year)
    col1, col2, col3 = st.columns(3)
    
    # Total CO2
    df_co2 = get_data("""
        SELECT SUM(r.value) as total 
        FROM sensor_readings r 
        JOIN sensors s ON r.sensor_id = s.id 
        WHERE s.type='co2_emission' 
        AND r.recorded_at > date('now', '-1 day')
    """)
    total_co2 = df_co2['total'].iloc[0] if not df_co2.empty and df_co2['total'].iloc[0] else 0
    
    # Simulação YoY
    yoy_val = total_co2 * 1.05 
    
    col1.metric("Emissão CO2 (24h)", f"{total_co2:,.0f} kg", f"-5% YoY ({yoy_val:,.0f})", delta_color="normal")
    col2.metric("Área Produtiva", "135.000 ha", "+2% 2YoY (Expansão)")
    col3.metric("Rebanho Monitorado", "120.000 Cabeças", "Estável YoY")
    
    st.divider()
    
    col_map, col_graph = st.columns([1, 1])
    
    with col_graph:
        # Mapa de Calor
        st.subheader("🔥 Emissões por Setor (kg CO2/ha)")
        df_sector_co2 = get_data("""
            SELECT sec.name, sec.crop_type, AVG(r.value) as avg_co2
            FROM sensor_readings r
            JOIN sensors s ON r.sensor_id = s.id
            JOIN sectors sec ON s.sector_id = sec.id
            WHERE s.type = 'co2_emission'
            GROUP BY sec.name
            ORDER BY avg_co2 DESC
        """)
        fig = px.bar(df_sector_co2, x="name", y="avg_co2", color="crop_type", 
                     title="Ranking de Emissões",
                     color_discrete_map={"Floresta": "green", "Soja": "yellow", "Pecuária": "red", "Milho": "orange", "Recursos Hídricos": "blue"})
        st.plotly_chart(fig, use_container_width=True)

    with col_map:
        st.markdown("### 🗺️ Visão de Satélite (Piratininga/GO)")
        import folium
        from streamlit_folium import st_folium

        # Coordenadas: São Miguel do Araguaia (Região da Fazenda)
        center = [-13.27, -50.16]
        
        m = folium.Map(location=center, zoom_start=10, tiles="OpenTopoMap")

        # Polígonos Simulados (Escala Maior)
        coords = {
            "Talhão Soja Norte (Piratininga)": [[-13.20, -50.20], [-13.20, -50.10], [-13.25, -50.10], [-13.25, -50.20]],
            "Pasto Rotacionado (Gado)":        [[-13.25, -50.20], [-13.25, -50.10], [-13.35, -50.10], [-13.35, -50.20]],
            "Reserva Legal Araguaia":          [[-13.20, -50.30], [-13.20, -50.20], [-13.35, -50.20], [-13.35, -50.30]],
        }

        for _, row in df_sector_co2.iterrows():
            name = row['name']
            val = row['avg_co2']
            color = "green"
            if val > 1000: color = "red"
            elif val > 300: color = "orange"
            elif val > 0: color = "yellow"
            
            if name in coords:
                folium.Polygon(
                    locations=coords[name], color=color, fill=True, fill_color=color, fill_opacity=0.6,
                    popup=f"{name}: {val:.0f} kg CO2"
                ).add_to(m)

        st_folium(m, width=600, height=450)

# --- Página Nova: Análise Soja ---
elif page == "🌱 Análise Soja (NDVI)":
    st.title("🌱 Monitoramento de Safra: Soja")
    st.markdown("Análise de produtividade, previsão de colheita e crescimento vegetativo.")
    
    # 1. Dados de Área
    df_area_soy = get_data("SELECT SUM(area_hectares) as total FROM sectors WHERE crop_type='Soja'")
    total_area_soy = df_area_soy['total'].iloc[0] if not df_area_soy.empty else 0
    
    # 2. Dados de Sensores
    df_soy = get_data("""
        SELECT s.type, r.value, r.recorded_at
        FROM sensor_readings r
        JOIN sensors s ON r.sensor_id = s.id
        JOIN sectors sec ON s.sector_id = sec.id
        WHERE sec.crop_type = 'Soja'
        ORDER BY r.recorded_at
    """)
    
    if not df_soy.empty:
        # Métricas de Produção (Simulação)
        current_yield_est = 72.5 # Sacas/ha (Estimativa atual)
        last_year_yield = 64.0   # Sacas/ha (Ano passado)
        delta_yield = current_yield_est - last_year_yield
        
        # Previsão de Colheita
        days_to_harvest = 85 # Dias restantes
        harvest_date = "15/Fev/2026"
        
        # Linha 1 de KPIs: Produção
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Área Plantada", f"{total_area_soy:,.0f} ha", "Talhão Norte")
        kpi2.metric("Produtividade Est.", f"{current_yield_est} sc/ha", f"{delta_yield:+.1f} sc/ha (YoY)")
        kpi3.metric("Previsão Colheita", f"{days_to_harvest} Dias", f"Data: {harvest_date}")
        kpi4.metric("Produção Total Est.", f"{(total_area_soy * current_yield_est):,.0f} sc", "Safra Recorde")
        
        st.divider()
        
        # Linha 2: Sensores (NDVI e Altura)
        ndvi_data = df_soy[df_soy['type'] == 'ndvi']
        height_data = df_soy[df_soy['type'] == 'plant_height']

        ndvi = ndvi_data['value'].iloc[-1] if not ndvi_data.empty else 0
        height = height_data['value'].iloc[-1] if not height_data.empty else 0
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("### 🌿 Status Vegetativo")
            st.metric("NDVI (Vigor)", f"{ndvi:.2f}", "Ótimo (> 0.7)")
            st.metric("Altura de Planta", f"{height:.0f} cm", "+2 cm (24h)")
            st.info("Estágio: **R1 - Início do Florescimento**")
            
        with c2:
            st.markdown("### 📈 Curva de Crescimento")
            
            # Preparar dados de comparação YoY
            df_plot = df_soy[df_soy['type'].isin(['ndvi', 'plant_height'])].copy()
            df_plot['year'] = '2025 (Atual)'
            
            # Simular dados do ano passado (10% menor em performance)
            df_last_year = df_plot.copy()
            df_last_year['value'] = df_last_year['value'] * 0.90  # 10% menor
            df_last_year['year'] = '2024 (Ano Passado)'
            
            # Combinar dados
            df_comparison = pd.concat([df_plot, df_last_year])
            
            fig = px.line(df_comparison, 
                          x="recorded_at", y="value", color="type", 
                          line_dash="year",
                          title="Evolução: NDVI vs Altura (Comparativo YoY)",
                          color_discrete_map={"ndvi": "green", "plant_height": "blue"})
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("Dados de Soja não encontrados.")

# --- Página Nova: Gestão Leiteira ---
elif page == "🐄 Gestão Leiteira":
    st.title("🐄 Gestão da Produção Leiteira")
    st.markdown("Monitoramento diário do tanque de expansão e produtividade do rebanho.")
    
    # Dados de Leite
    df_milk = get_data("""
        SELECT r.value, r.recorded_at
        FROM sensor_readings r
        JOIN sensors s ON r.sensor_id = s.id
        WHERE s.type = 'milk_production'
        ORDER BY r.recorded_at
    """)
    
    if not df_milk.empty:
        # KPIs
        last_prod = df_milk['value'].iloc[-1]
        avg_prod = df_milk['value'].mean()
        
        quality_ccs = 180 
        fat_perc = 3.8 
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Produção Hoje", f"{last_prod:,.0f} L", f"{last_prod - avg_prod:,.0f} L vs Média")
        kpi2.metric("Média/Vaca (Est.)", "18.5 L", "Rebanho: 80 cabeças")
        kpi3.metric("Gordura do Leite", f"{fat_perc}%", "Qualidade Premium")
        kpi4.metric("CCS (Células)", f"{quality_ccs} mil", "Baixo Risco Mastite")
        
        st.divider()
        
        st.subheader("📈 Curva de Lactação do Rebanho (7 Dias)")
        fig_milk = px.area(df_milk, x="recorded_at", y="value", 
                           title="Volume Diário no Tanque (Litros)",
                           labels={"value": "Litros", "recorded_at": "Data"},
                           color_discrete_sequence=["#ADD8E6"]) 
        st.plotly_chart(fig_milk, use_container_width=True)
        
        if last_prod < 1200:
            st.warning("⚠️ **Atenção:** Queda brusca na produção! Verificar nutrição ou estresse térmico.")
        else:
            st.success("✅ Produção estável e dentro da meta.")
            
    else:
        st.info("Nenhum sensor de leite ativo encontrado. Verifique se o setor 'Pecuária' está monitorado.")

# --- Página: Gestão de Carbono (ESG) ---
elif page == "🌍 Gestão de Carbono (ESG)":
    st.title("🌍 Gestão de Carbono & ESG")
    st.markdown("Balanço de Emissões (GEE) e Potencial de Créditos de Carbono.")
    
    # Dados de CO2 Agrupados por Cultura
    df_carbon = get_data("""
        SELECT sec.crop_type, SUM(r.value) as total_co2, AVG(r.value) as avg_co2_ha, COUNT(DISTINCT sec.id) as num_sectors
        FROM sensor_readings r
        JOIN sensors s ON r.sensor_id = s.id
        JOIN sectors sec ON s.sector_id = sec.id
        WHERE s.type = 'co2_emission'
        GROUP BY sec.crop_type
    """)
    
    if not df_carbon.empty:
        # Cálculos de Balanço
        emissions = df_carbon[df_carbon['total_co2'] > 0]['total_co2'].sum()
        sequestration = df_carbon[df_carbon['total_co2'] < 0]['total_co2'].sum() # Valor negativo
        net_balance = emissions + sequestration
        
        # KPIs Principais
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Emissão Bruta", f"{emissions/1000:,.1f} t", "Fontes: Gado, Maquinário")
        kpi2.metric("Sequestro (Remoção)", f"{abs(sequestration)/1000:,.1f} t", "Fontes: Floresta, Solo")
        
        balance_color = "normal" if net_balance < 0 else "inverse"
        balance_label = "🟢 CARBONO NEGATIVO (Crédito)" if net_balance < 0 else "🔴 CARBONO POSITIVO (Débito)"
        kpi3.metric("Balanço Líquido", f"{net_balance/1000:,.1f} t", balance_label, delta_color=balance_color)
        
        # Simulação Financeira (Crédito de Carbono ~ $10 USD/ton)
        carbon_price = 10 
        potential_revenue = (abs(net_balance)/1000) * carbon_price if net_balance < 0 else 0
        kpi4.metric("Receita Potencial (CBIO)", f"USD {potential_revenue:,.0f}", "Cotação: $10/ton")
        
        st.divider()
        
        # Gráfico Waterfall (Cascata) de Carbono
        st.subheader("📉 Composição da Pegada de Carbono")
        
        # Preparar dados para Waterfall
        measures = []
        x_labels = []
        y_values = []
        
        for _, row in df_carbon.iterrows():
            x_labels.append(row['crop_type'])
            y_values.append(row['total_co2'])
            measures.append("relative")
            
        # Adicionar Total
        x_labels.append("Balanço Final")
        y_values.append(None)
        measures.append("total")
        
        fig_waterfall = go.Figure(go.Waterfall(
            name = "2025", orientation = "v",
            measure = measures,
            x = x_labels,
            textposition = "outside",
            text = [f"{v/1000:.0f}t" if v is not None else "" for v in y_values],
            y = y_values,
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        
        fig_waterfall.update_layout(title = "Fluxo de Carbono por Atividade (Toneladas)", showlegend = True)
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        # Detalhamento e Ações
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### 🚨 Maiores Emissores")
            emitters = df_carbon[df_carbon['total_co2'] > 0].sort_values('total_co2', ascending=False)
            st.dataframe(emitters[['crop_type', 'total_co2']], use_container_width=True)
            
        with c2:
            st.markdown("### 💡 Plano de Mitigação (IA)")
            if emissions > abs(sequestration):
                st.warning("A fazenda está emitindo mais do que sequestrando.")
                st.markdown("""
                **Ações Recomendadas:**
                1.  **Pecuária:** Implementar dieta com aditivos para reduzir metano entérico (-15%).
                2.  **Solo:** Adotar Plantio Direto na Soja/Milho para aumentar retenção de carbono no solo.
                3.  **ILPF:** Integrar árvores nas áreas de pastagem degradada.
                """)
            else:
                st.success("Parabéns! A fazenda é um sumidouro de carbono.")
                st.markdown("""
                **Oportunidades:**
                1.  **Certificação:** Emitir CBIOs (Créditos de Descarbonização).
                2.  **Marketing Verde:** Rotular produtos como "Carbon Free".
                """)
                
    else:
        st.info("Dados insuficientes para cálculo de carbono.")

# --- Página 4: Integração R ---
elif page == "Integração R":
    st.title("📈 Integração com Linguagem R")
    st.write("Exporte os dados atuais para serem analisados pelo script `fase4/analysis.R`.")
    
    if st.button("Exportar CSV para R"):
        msg = export_for_r()
        st.success(msg)
        st.code("Rscript fase4/analysis.R", language="bash")