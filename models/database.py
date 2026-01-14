# models/database.py - VERSÃO PARA RENDER.COM
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Obter DATABASE_URL do ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

# IMPORTANTE: Render fornece URL no formato postgres://
# SQLAlchemy precisa de postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Se não houver DATABASE_URL (desenvolvimento local), usa SQLite
if not DATABASE_URL:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "nandolab.db")
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    
    # Criar pasta instance se não existir
    instance_dir = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

# Criar engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False 
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Função para obter conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()