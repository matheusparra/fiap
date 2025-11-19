# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa os Roteadores (que contêm as rotas)
from app.routers import sensores, irrigacao
# IMPORTANTE: Certifique-se de ter criado 'app/routers/campos.py' também.
# from app.routers import campos 

app = FastAPI(
    title="FarmTech API",
    description="API refatorada para Global Solution FIAP 2025.2",
    version="2.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, restrinja para o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#                 REGISTRO DE ROTAS
# ============================================================
# O prefixo define a URL base (ex: /api/sensores/registrar)
app.include_router(sensores.router, prefix="/api/sensores", tags=["Sensores"])
app.include_router(irrigacao.router, prefix="/api/irrigacao", tags=["Irrigação (ML)"])

# Descomente abaixo quando tiver o arquivo routers/campos.py pronto
# app.include_router(campos.router, prefix="/api/campos", tags=["Campos"])

# Health Check simples
@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "online", "arquitetura": "microservices-ready"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)