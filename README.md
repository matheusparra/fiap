# 🤠 CAPATAZ – Inteligência de Campo
## Global Solution FIAP 2025.2 – O Futuro do Trabalho no Agronegócio

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Status](https://img.shields.io/badge/Status-MVP_Funcional-success)

---

## 📋 Índice

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Desafio Proposto](#desafio-proposto)
3. [Nossa Solução](#nossa-solução)
4. [Integração de Disciplinas](#integração-de-disciplinas)
5. [Arquitetura do Sistema](#arquitetura-do-sistema)
6. [Funcionalidades](#funcionalidades)
7. [Como Executar](#como-executar)
8. [Estrutura do Projeto](#estrutura-do-projeto)
9. [Tecnologias Utilizadas](#tecnologias-utilizadas)
10. [Equipe](#equipe)

---

## 🎯 Sobre o Projeto

**CAPATAZ** é uma plataforma de inteligência artificial desenvolvida para transformar o trabalho no agronegócio, tornando-o mais **humano, inclusivo e sustentável**. Modelado a partir da **Fazenda Nova Piratininga** (135.000 hectares em Goiás/Tocantins), o sistema monitora em tempo real:

- **Emissões de CO2** (Gestão de Carbono)
- **Produtividade de Soja** (NDVI, Altura de Planta)
- **Produção Leiteira** (Volume, Qualidade)
- **Inteligência Ambiental** (Sustentabilidade ESG)

O projeto responde à pergunta central:

> **"Como a tecnologia pode tornar o trabalho mais humano, inclusivo e sustentável no futuro?"**

---

## 🌍 Desafio Proposto

### Tema da Global Solution 2025.2

O futuro do trabalho já começou. A FIAP propôs o desafio de criar soluções que preparem pessoas e organizações para um mundo onde:

- Inteligência Artificial substitui tarefas repetitivas
- A sustentabilidade é mandatória
- O trabalhador precisa de **ferramentas inteligentes** para tomar decisões complexas

### Eixos Temáticos Abordados

✅ **Bots e agentes inteligentes como parceiros de produtividade**  
✅ **Modelos de trabalho verde e sustentável**  
✅ **Recrutamento e inclusão ética apoiados por dados**

---

## 💡 Nossa Solução

### O Conceito

Transformamos o **capataz da fazenda** (cargo tradicional de supervisão) em um **Gestor Ambiental 4.0**, equipado com:

1. **Dashboard Interativo (Streamlit)**: Visualização em tempo real de 135.000 hectares
2. **Agente de IA**: Análise automática de padrões e alertas críticos
3. **Gestão de Carbono**: Balanço de emissões (GEE) e créditos CBIO
4. **Monitoramento de Safra**: Previsão de produtividade (sacas/ha) com comparativo YoY

### Impacto Social

- **Valorização do Trabalhador Rural**: Leva tecnologia de ponta ao campo
- **Emprego Verde**: Capacita profissionais para a economia de baixo carbono
- **Inclusão Digital**: Interface simplificada para capataz com baixa escolaridade

---

## 🎓 Integração de Disciplinas

### 1. AICSS (Arquitetura de Inteligência Artificial)

- **Agente Capataz**: Sistema baseado em regras que analisa 6 tipos de sensores simultaneamente
- **Arquitetura Multi-Modal**: Integra dados de satélite (NDVI), solo (umidade), clima (temperatura)

### 2. Cybersecurity

- **Autenticação**: Sistema de login com hash de senha
- **Controle de Acesso**: Apenas usuários autorizados visualizam dados sensíveis da fazenda
- **API Segura**: Backend FastAPI com CORS configurado

### 3. Machine Learning

- **Previsão de Produtividade**: Estimativa de sacas/ha baseada em NDVI e altura de planta
- **Detecção de Anomalias**: Alertas quando CO2 ou NDVI fogem do padrão histórico
- **Dataset**: 90 dias de leituras para treinamento de modelos

### 4. Redes Neurais

- **Simulação de Crescimento**: Curva sigmoide para modelar NDVI e altura da soja
- **Camadas de Análise**: Agente processa múltiplas variáveis (temperatura, umidade, CO2) simultaneamente

### 5. Linguagem R

- **Análise Estatística**: Script `analysis.R` para correlação entre luminosidade e CO2
- **Exportação de Dados**: Função dedicada para gerar CSV compatível com R

### 6. Python

- **Backend**: FastAPI com endpoints para registro e consulta de sensores
- **Frontend**: Streamlit para visualização interativa
- **Simulação de Dados**: Scripts de população realista do banco de dados

### 7. Computação em Nuvem

- **Arquitetura Híbrida**: SQLite local com fallback para Supabase (PostgreSQL)
- **Escalabilidade**: Preparado para deployment em AWS/Azure com Docker
- **Monitoramento**: API REST disponível 24/7

### 8. Banco de Dados

- **Schema Normalizado**: 
  - `sectors` (setores da fazenda)
  - `sensors` (6 tipos: CO2, NDVI, Umidade, Temperatura, Leite, Altura)
  - `sensor_readings` (histórico temporal)
- **Query Optimization**: Índices em `recorded_at` para análise temporal

### 9. Formação Social

- **Impacto**: Valoriza o trabalho rural, transformando o capataz em gestor ambiental
- **Inclusão**: Interface acessível para baixa escolaridade
- **Sustentabilidade**: Foco em ESG e créditos de carbono
- **Economia Circular**: Reaproveitamento de dados para otimização de recursos

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────┐
│           CAPATAZ - Camada de Apresentação       │
│  ┌──────────────────────────────────────────┐   │
│  │  Streamlit Dashboard (localhost:8501)    │   │
│  │  - Visão Geral (Mapa com Folium)         │   │
│  │  - Análise Soja (NDVI + YoY)             │   │
│  │  - Gestão Leiteira (Tanque de Expansão)  │   │
│  │  - Gestão de Carbono (Waterfall Chart)   │   │
│  │  - Integração R (Exportação CSV)         │   │
│  └──────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           CAPATAZ - Camada de Negócio            │
│  ┌──────────────────────────────────────────┐   │
│  │  FastAPI Backend (localhost:8000)        │   │
│  │  - /sensores/registrar (POST)            │   │
│  │  - /sensores/ultimas (GET)               │   │
│  │  - /irrigacao/recomendacao (POST)        │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  Agente de IA (Rule-Based)               │   │
│  │  - run_agent_analysis()                  │   │
│  │  - Monitoramento: CO2, NDVI, Umidade     │   │
│  └──────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           CAPATAZ - Camada de Dados              │
│  ┌──────────────────────────────────────────┐   │
│  │  SQLite (farm.db) - Local                │   │
│  │  - Tabelas: sectors, sensors, readings   │   │
│  │  - Histórico: 90 dias de dados           │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  Supabase (PostgreSQL) - Cloud (Fallback)│   │
│  │  - Sincronização futura                  │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Funcionalidades

### 🗺️ Visão Geral (Piratininga)

- Mapa topográfico (OpenTopoMap) da região de São Miguel do Araguaia
- Polígonos coloridos por emissão de CO2 (Verde = Floresta, Vermelho = Gado)
- KPIs: Emissão CO2 (24h), Área Produtiva, Rebanho
- **Métricas YoY**: Comparação com ano passado (-5% de emissão)

### 🌱 Análise Soja (NDVI)

- **Produtividade**: 72.5 sc/ha (+8.5 sc/ha YoY)
- **Área Plantada**: 25.000 hectares
- **Previsão de Colheita**: 85 dias restantes (15/Fev/2026)
- **Gráficos**:
  - Curva de Crescimento (NDVI vs Altura) com comparativo 2024 vs 2025
  - Linha sólida: Ano atual | Linha tracejada: Ano passado

### 🐄 Gestão Leiteira

- **Produção Total**: Litros no tanque de expansão
- **Média/Vaca**: 18.5 L/dia
- **Qualidade**: Gordura 3.8%, CCS 180 mil
- **Gráfico**: Curva de lactação dos últimos 7 dias

### 🌍 Gestão de Carbono (ESG)

- **Balanço Líquido**: Emissões - Sequestro
- **Waterfall Chart**: Visualização de fluxo de carbono por atividade
- **Receita Potencial**: Créditos CBIO (USD/ton)
- **Plano de Mitigação**: Recomendações de IA (ex: ILPF, Dieta do Gado)

### 🤖 Agente Capataz (IA)

- Botão na barra lateral: "Rodar Análise IA"
- Insights automáticos:
  - "⚠️ Emissões altas detectadas no Pasto"
  - "✅ Soja com vigor excelente (NDVI > 0.7)"

### 📊 Integração R

- Exportação de dados para CSV
- Script R: Correlação entre Luminosidade e CO2

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- R 4.0+ (opcional, para análise estatística)

### 1. Clone o Repositório

```bash
git clone [URL_DO_REPOSITORIO_PRIVADO]
cd farmtech_fase7-main
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o Banco de Dados

```bash
python fase2/setup_agro_db.py
python fase2/populate_agro_data.py
```

### 4. Inicie os Serviços

#### Backend (API)
```bash
python -m uvicorn app.main:app --port 8000
```

#### Frontend (Dashboard)
```bash
python -m streamlit run fase4/streamlit_app.py
```

### 5. Acesse o Sistema

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

**Credenciais de Acesso**:
- Usuário: `admin`
- Senha: `fiap2025`

---

## 📁 Estrutura do Projeto

```
farmtech_fase7-main/
├── app/
│   ├── main.py                 # FastAPI App
│   ├── database.py             # Conexão DB (SQLite/Supabase)
│   ├── routers/
│   │   ├── sensores.py         # Endpoints de sensores
│   │   └── irrigacao.py        # Endpoint de ML
│   └── services/
│       ├── sensor_service.py   # Lógica de negócio
│       └── irrigacao_service.py
├── fase2/
│   ├── setup_agro_db.py        # Schema do banco
│   ├── populate_agro_data.py   # Dados simulados (90 dias)
│   └── db_utils.py             # Utilitários de conexão
├── fase4/
│   ├── streamlit_app.py        # Dashboard Streamlit
│   ├── analysis.R              # Script R (correlação)
│   └── export_r_data.py        # Exportação CSV para R
├── farm.db                     # Banco SQLite local
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web assíncrono
- **SQLAlchemy**: ORM para banco de dados
- **psycopg2**: Driver PostgreSQL
- **SQLite3**: Banco de dados local

### Frontend
- **Streamlit**: Dashboard interativo
- **Plotly**: Visualizações de dados
- **Folium**: Mapas topográficos
- **Pandas**: Manipulação de dados

### Machine Learning
- **scikit-learn**: Modelos preditivos
- **NumPy**: Computação numérica

### Análise Estatística
- **R**: Linguagem para análise de dados
- **ggplot2**: Visualizações em R

### Cloud & DevOps
- **Supabase**: PostgreSQL gerenciado
- **Docker**: Containerização (futuro)

---

## 👥 Equipe

- **Matheus Parra** - RM561907
- **Otavio Custodio de Oliveira** - RM565606
- **Tiago Alves Cordeiro** (Líder do Repositório) - RM561791
- **Thiago Henrique Pereira de Almeida Santos** - RM563327
- **Leandro Arthur Marinho Ferreira** - RM565240

---

## 📹 Vídeo de Apresentação

**[Link do YouTube (não listado)]**

> ⚠️ **Importante**: O vídeo contém a frase "QUERO CONCORRER" nos primeiros segundos para participação no pódio.

---

## 🔗 Links Úteis

- **GitHub (Privado)**: [Adicionar depois de criar repositório privado]
- **Documentação da API**: http://localhost:8000/docs
- **Fazenda Nova Piratininga**: [Referência Real](https://www.novapiratininga.com)

---

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos na **FIAP - Global Solution 2025.2**.

---

## 🙏 Agradecimentos

- **FIAP**: Pela proposta do desafio
- **Fazenda Nova Piratininga**: Inspiração para os dados simulados
- **Comunidade Open Source**: Ferramentas utilizadas

---

**Desenvolvido com ❤️ para o Futuro do Trabalho**