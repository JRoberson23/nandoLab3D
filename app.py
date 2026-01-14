from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware  
from starlette.responses import Response  
from dotenv import load_dotenv
import os

load_dotenv()

# Importar database e models
from models.database import engine, Base
from models import models

# Importar routers
from routers import main, admin, api

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa o banco de dados ao iniciar o app"""
    # Cria a pasta instance se não existir
    instance_dir = os.path.join(os.path.dirname(__file__), "instance")
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    # Criar tabelas apenas se não for produção
    if os.getenv("ENVIRONMENT") != "production":
        print("🔧 Criando tabelas do banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("✅ Banco de dados inicializado com sucesso!")
    else:
        print("⚡ Ambiente de produção - usando migrações existentes")
    
    # Criar pastas de upload:
    upload_dirs = [
        "static/uploads",
        "static/uploads/projetos", 
        "static/uploads/orcamentos"
    ]
    
    for dir_path in upload_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 Criada pasta: {dir_path}")
    
    # Criar todas as tabelas
    print("🔧 Criando tabelas do banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado com sucesso!")

    yield

    print("🔴 Aplicação encerrada")

# Criar app FastAPI
app = FastAPI(
    title="NandoLab 3D",
    description="Sistema de portfólio e vendas para modelagem 3D",
    version="1.0.0",
    docs_url="/api/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
    lifespan=lifespan
)

# === 1. PRIMEIRO: Middleware do Ngrok ===
if os.getenv("ENVIRONMENT") != "development":
    class AddNgrokHeaderMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Processa a requisição normalmente
            response = await call_next(request)
            
            # Adiciona o cabeçalho especial do ngrok
            response.headers["ngrok-skip-browser-warning"] = "true"
            
            return response
        
    app.add_middleware(AddNgrokHeaderMiddleware)

# Registre o middleware do ngrok PRIMEIRO
app.add_middleware(AddNgrokHeaderMiddleware)

# === 2. SEGUNDO: Session Middleware ===
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SESSION_SECRET", "chave_secreta_muito_forte_mude_isso_123"),
    session_cookie="nandolab_admin_session",
    max_age=3600,  # 1 hora de sessão
    same_site="lax"
)

# === 3. TERCEIRO: CORS Middleware ===
allowed_origins = ["*"] if os.getenv("ENVIRONMENT") == "development" else [
    "https://seu-app.onrender.com",  # URL do Render
    "https://www.nandolab3d.com.br"     # Ainda não tenho dominio mas vai ser esse mesmo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["ngrok-skip-browser-warning"] if os.getenv("ENVIRONMENT") == "development" else []
)

# Configurar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar templates
from config.templates import templates

# Registrar routers
app.include_router(main.router)
app.include_router(admin.router)
app.include_router(api.router, prefix="/api")

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da aplicação"""
    return {
        "status": "healthy",
        "service": "NandoLab 3D",
        # MODIFIQUE para:
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "PostgreSQL" if os.getenv("DATABASE_URL") else "SQLite"
    }

# Favicon para evitar erro 404 no Render
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imagens/Fav.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)