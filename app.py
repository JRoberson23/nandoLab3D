from fastapi import FastAPI, Request # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.responses import FileResponse, HTMLResponse # type: ignore
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from starlette.middleware.sessions import SessionMiddleware # type: ignore
from starlette.middleware.base import BaseHTTPMiddleware # type: ignore
from starlette.responses import Response # type: ignore
from datetime import datetime
from dotenv import load_dotenv # type: ignore
from sqlalchemy import inspect, text
from config.templates import templates
from fastapi.responses import PlainTextResponse # type: ignore
from services.scheduler import start_scheduler, stop_scheduler

import os

load_dotenv()

# Importar database e models
from models.database import engine, Base, SessionLocal
from models import models

# Importar routers
from routers import main, admin, api, sitemap

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa o banco de dados ao iniciar o app - VERSÃO CORRIGIDA"""
    print(f"🚀 Iniciando NandoLab 3D | Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    
    # 1. Criar pasta instance se não existir
    instance_dir = os.path.join(os.path.dirname(__file__), "instance")
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"📁 Pasta 'instance' criada")

    # 2. ✅✅✅ CORREÇÃO: Criar tabelas SEM condição de ambiente
    print("🔧 Verificando/Criando tabelas do banco de dados...")
    
    try:
        # Verificar se tabela 'projetos' já existe
        from sqlalchemy import inspect, text
        
        inspector = inspect(engine)
        tabelas_existentes = inspector.get_table_names()
        
        if "projetos" not in tabelas_existentes:
            print("📦 Criando todas as tabelas...")
            Base.metadata.create_all(bind=engine)
            print(f"✅ Criadas {len(Base.metadata.tables)} tabelas")
        else:
            print(f"✅ Banco já tem {len(tabelas_existentes)} tabelas")
            
        # Testar conexão com a tabela projetos
        with engine.connect() as conn:
            # Tentar contar projetos
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM projetos"))
                count = result.scalar()
                print(f"📊 Total de projetos: {count}")
            except:
                print("⚠️ Tabela 'projetos' existe mas não pode ser acessada")
                # Recriar tabelas se houver problema
                Base.metadata.drop_all(bind=engine)
                Base.metadata.create_all(bind=engine)
                print("🔄 Tabelas recriadas devido a erro de acesso")
                
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        print("🔄 Tentando criar tabelas de qualquer forma...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas após erro")
    
    # 3. Criar pastas de upload (com caminhos absolutos)
    print("📁 Criando pastas de upload...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    upload_dirs = [
        os.path.join(base_dir, "static/uploads"),
        os.path.join(base_dir, "static/uploads/projetos"), 
        os.path.join(base_dir, "static/uploads/orcamentos")
    ]
    
    for dir_path in upload_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            rel_path = os.path.relpath(dir_path, base_dir)
            print(f"   ✅ {rel_path}")
        else:
            rel_path = os.path.relpath(dir_path, base_dir)
            print(f"   ✓ {rel_path} (já existe)")
    
    print("🌈 Inicialização completa! Aplicação pronta para receber requisições.")

    # ✅Iniciar scheduler para evitar sleep
    try:
        start_scheduler()
        print("⏰ Scheduler de ping iniciado!")
    except Exception as e:
        print(f"⚠️ Erro ao iniciar scheduler: {e}")

    yield

    # ✅Parar scheduler
    try:
        stop_scheduler()
        print("⏰ Scheduler de ping parado!")
    except Exception as e:
        print(f"⚠️ Erro ao parar scheduler: {e}")
    
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

# === 1. PRIMEIRO: Middleware do Ngrok (apenas desenvolvimento) ===
if os.getenv("ENVIRONMENT") == "development":  # ← CORRIGIDO: "==" development
    class AddNgrokHeaderMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response = await call_next(request)
            response.headers["ngrok-skip-browser-warning"] = "true"
            return response
    
    app.add_middleware(AddNgrokHeaderMiddleware)  # ← OK, só aqui

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
    "https://nandolab3d.onrender.com",  # ← Altere para SUA URL do Render
    "https://www.nandolab3d.com.br"
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
app.include_router(sitemap.router)

from services.ping import router as ping_router
app.include_router(ping_router, prefix="/api")

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da aplicação"""
    return {
        "status": "healthy",
        "service": "NandoLab 3D",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "PostgreSQL" if os.getenv("DATABASE_URL") else "SQLite"
    }

@app.get("/robots.txt", response_class=PlainTextResponse)
async def get_robots():
    """Serve o arquivo robots.txt"""
    robots_content = """User-agent: *
Allow: /
Sitemap: https://nandolab3d.onrender.com/sitemap.xml
Disallow: /admin/
Disallow: /api/
Disallow: /static/uploads/"""
    return robots_content

# Favicon para evitar erro 404
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imagens/Fav.ico")

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/debug/db")
async def debug_database():
    """Endpoint para debug do banco de dados - VERSÃO CORRIGIDA"""
    try:
        # 1. Verificar tabelas
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # 2. Contar projetos
        projeto_count = 0
        sample_projects = []
        
        if "projetos" in tables:
            with engine.connect() as conn:
                # Contar
                result = conn.execute(text("SELECT COUNT(*) FROM projetos"))
                projeto_count = result.scalar()
                
                # Pegar alguns exemplos
                if projeto_count > 0:
                    result = conn.execute(text("SELECT id, titulo, categoria FROM projetos LIMIT 5"))
                    sample_projects = [dict(row._mapping) for row in result]
        
        # 3. Verificar variáveis de ambiente
        env = os.getenv("ENVIRONMENT", "not_set")
        db_url = os.getenv("DATABASE_URL", "sqlite:///instance/nandolab.db")
        
        # 4. Verificar arquivo do banco
        import sqlite3
        from pathlib import Path
        db_path = Path("instance/nandolab.db")
        db_exists = db_path.exists()
        db_size = db_path.stat().st_size if db_exists else 0
        
        return {
            "status": "ok",
            "environment": env,
            "database_url": db_url,
            "database_file_exists": db_exists,
            "database_size_bytes": db_size,
            "tables": tables,
            "tables_count": len(tables),
            "projetos_table_exists": "projetos" in tables,
            "projetos_count": projeto_count,
            "sample_projects": sample_projects,
            "render_service": True,
            "message": f"Ambiente configurado como: {env}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "environment": os.getenv("ENVIRONMENT", "not_set"),
            "traceback": True
        }