# Sistema de Gestão Agrícola – Fase 7

## Visão geral

Este repositório consolida todas as fases do projeto **FarmTech Solutions** em uma única solução.  As fases 1 a 6 foram desenvolvidas em repositórios e linguagens diferentes; aqui, elas são integradas por meio de módulos Python e um dashboard interativo em Streamlit, além de scripts de mensageria na AWS para envio de alertas.

### Estrutura do projeto

```
farmtech_fase7/
├── fase1/            # Cálculos de área e insumos agrícolas
│   ├── calculator.py
│   └── insumos.csv
├── fase2/            # Banco de dados relacional
│   ├── schema.sql
│   ├── db_utils.py
│   └── insert_data.py
├── fase3/            # IoT e automação
│   ├── esp32/        # Código para o microcontrolador (não incluso aqui)
│   ├── simulador.py
│   └── control.py
├── fase4/            # Dashboard e Machine Learning
│   ├── streamlit_app.py
│   ├── train_model.py
│   └── model.pkl     # modelo preditivo (placeholder)
├── fase6/            # Visão computacional
│   └── inferencia.py
├── aws_alerts/       # Mensageria na AWS
│   ├── send_alert.py
│   └── check_sensors.py
├── requirements.txt  # dependências do projeto
└── README.md         # este documento
```

## Como executar

1. **Instalar dependências**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # no Windows use venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configurar o banco de dados** (Fase 2):

   ```bash
   python fase2/insert_data.py
   ```

   Isso cria o arquivo `farm.db` e popula tabelas básicas.

3. **Executar a simulação de sensores** (Fase 3):

   ```bash
   python fase3/simulador.py
   ```

4. **Iniciar o dashboard** (Fase 4):

   ```bash
   streamlit run fase4/streamlit_app.py
   ```

   Use a barra lateral do Streamlit para navegar entre as funcionalidades das fases.

5. **Configurar as credenciais AWS** (Fase 5):

   Crie um tópico SNS na AWS e configure as variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `AWS_REGION` no seu ambiente.  Em seguida, edite `aws_alerts/send_alert.py` para incluir o ARN do tópico.

6. **Executar a verificação de alertas** (Fase 5):

   ```bash
   python aws_alerts/check_sensors.py
   ```

## Fase 1 – Cálculo de insumos

O módulo `fase1/calculator.py` implementa funções para calcular a área de plantio e estimar a quantidade de insumos (mudas, calcário, fertilizantes etc.) por cultura a partir das definições apresentadas na fase 1.  Os dados de referência estão no arquivo `insumos.csv`.

## Fase 2 – Banco de dados

O script `fase2/schema.sql` define as tabelas para armazenar leituras de sensores, eventos de irrigação e logs.  O módulo `db_utils.py` contém funções para criar o banco de dados SQLite e executar operações básicas.  O arquivo `insert_data.py` cria o banco (caso não exista) e insere registros iniciais.

## Fase 3 – IoT e automação

`fase3/simulador.py` gera leituras de sensores simuladas (umidade, pH, nutrientes) e grava no banco de dados.  Já `fase3/control.py` consulta as leituras mais recentes e imprime mensagens de controle das bombas de irrigação dependendo dos limites configurados.  O código do microcontrolador, se necessário, pode ser adicionado em `fase3/esp32/`.

## Fase 4 – Dashboard e Machine Learning

O aplicativo Streamlit localizado em `fase4/streamlit_app.py` centraliza a interface com o usuário.  Ele utiliza os módulos das fases anteriores para realizar cálculos, consultar o banco de dados, visualizar leituras e exibir predições de irrigação com base em um modelo de aprendizado de máquina (arquivo `model.pkl`, que pode ser treinado utilizando `train_model.py`).

## Fase 6 – Visão computacional

O script `fase6/inferencia.py` serve como ponto de entrada para integrar modelos de visão computacional treinados na fase 6.  Por padrão ele apenas imprime uma mensagem informando que o módulo deve ser implementado, mas você pode adaptar o código do notebook da fase 6 para carregar pesos do YOLOv5 ou de uma CNN.

## Fase 5 – Mensageria na AWS

Os scripts em `aws_alerts/` demonstram como enviar e‑mails ou SMS via Amazon SNS quando determinados limites são ultrapassados.  Configure o ARN do tópico SNS no arquivo `send_alert.py` e execute `check_sensors.py` para monitorar periodicamente as leituras de sensores e disparar alertas.

## Contribuições

Este repositório é acadêmico e foi consolidado a partir das fases anteriores do projeto FarmTech Solutions.  Sinta‑se livre para propor melhorias e completar as implementações pendentes.