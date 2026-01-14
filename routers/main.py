# routers/main.py
from datetime import datetime
import os
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from flask import app
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func  # IMPORTANTE: Adicionar esta linha!

from models.database import get_db
from models.models import Projeto, Pedido  # Adicionar Pedido também

router = APIRouter(tags=["Páginas Públicas"])
templates = Jinja2Templates(directory="templates")

# ========== ROTAS PÚBLICAS DO SITE ==========

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Página inicial"""
    try:
        # ===== PROJETOS EM DESTAQUE =====
        projetos_destaque = db.query(Projeto).filter(
            Projeto.publicado == True,
            Projeto.destaque == True
        ).order_by(Projeto.created_at.desc()).limit(3).all()
        
        # ===== ESTATÍSTICAS DO SITE =====
        total_projetos = db.query(Projeto).filter(Projeto.publicado == True).count()
        total_destaque = len(projetos_destaque)
        
        # Contar projetos por categoria
        categorias_count = db.query(
            Projeto.categoria,
            func.count(Projeto.id).label('total')
        ).filter(
            Projeto.publicado == True,
            Projeto.categoria.isnot(None)
        ).group_by(Projeto.categoria).all()
        
        # Converter para dicionário
        categorias_dict = {cat: total for cat, total in categorias_count}
        
        # ===== OUTROS DADOS (se necessário) =====
        # Todos projetos (limitado) - para outras seções se precisar
        todos_projetos = db.query(Projeto).filter(
            Projeto.publicado == True
        ).order_by(Projeto.created_at.desc()).limit(6).all()
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "projetos_destaque": projetos_destaque,
                "todos_projetos": todos_projetos,
                "total_projetos": total_projetos,
                "total_destaque": total_destaque,
                "categorias_count": categorias_dict,
                "titulo": "NandoLab 3D - Arte em Modelagem Tridimensional"
            }
        )
        
    except Exception as e:
        print(f"Erro na página inicial: {e}")
        # Em caso de erro, retorna valores padrão
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "projetos_destaque": [],
                "todos_projetos": [],
                "total_projetos": 0,
                "total_destaque": 0,
                "categorias_count": {},
                "titulo": "NandoLab 3D - Arte em Modelagem Tridimensional"
            }
        )

# ... (o resto do seu código permanece igual)
@router.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request, db: Session = Depends(get_db)):
    """Página do portfólio"""
    projetos = db.query(Projeto).filter(Projeto.publicado == True).all()
    
    # Pegar categorias únicas
    categorias = db.query(Projeto.categoria).filter(
        Projeto.publicado == True,
        Projeto.categoria.isnot(None)
    ).distinct().all()
    
    return templates.TemplateResponse(
        "portfolio.html",
        {
            "request": request,
            "projetos": projetos,
            "categorias": [cat[0] for cat in categorias if cat[0]],
            "titulo": "Portfólio - NandoLab 3D"
        }
    )

@router.get("/servicos", response_class=HTMLResponse)
async def servicos(request: Request):
    """Página de serviços"""
    return templates.TemplateResponse(
        "servicos.html",
        {
            "request": request,
            "titulo": "Serviços - NandoLab 3D"
        }
    )

@router.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request):
    """Página sobre"""
    return templates.TemplateResponse(
        "sobre.html",
        {
            "request": request,
            "titulo": "Sobre - NandoLab 3D"
        }
    )

@router.get("/orcamento", response_class=HTMLResponse)
async def orcamento_form(request: Request):
    """Formulário de orçamento"""
    return templates.TemplateResponse(
        "orcamento.html",
        {
            "request": request,
            "titulo": "Solicitar Orçamento - NandoLab 3D"
        }
    )


@router.post("/enviar-orcamento")
async def enviar_orcamento(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(default=""),
    projeto: str = Form(...),
    tipo_projeto: str = Form(...),
    prazo: str = Form(default=""),
    db: Session = Depends(get_db)
):
    """Processa formulário de orçamento"""
    from models.models import Pedido
    
    # Criar novo pedido
    novo_pedido = Pedido(
        nome_cliente=nome,
        email=email,
        telefone=telefone,
        titulo_projeto=f"[{tipo_projeto}] - Orçamento via site",
        descricao=f"""Tipo: {tipo_projeto}
Prazo: {prazo}
Descrição:
{projeto}""",
        status="pendente"
    )
    
    db.add(novo_pedido)
    db.commit()
    
    # Redirecionar com mensagem de sucesso
    return RedirectResponse(
        "/?success=Orçamento enviado com sucesso!", 
        status_code=303
    )


@router.get("/obrigado", response_class=HTMLResponse)
async def obrigado(request: Request):
    """Página de agradecimento após envio de orçamento"""
    return templates.TemplateResponse(
        "obrigado.html",
        {
            "request": request,
            "titulo": "Obrigado! - NandoLab 3D"
        }
    )

@app.get("/render-check")
async def render_check():
    """Endpoint ESPECIAL para verificar configuração do Render"""
    return {
        "service": "NandoLab 3D",
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "not_set"),
        "render": True,
        "database_tables_created": True if os.getenv("ENVIRONMENT") == "development" else "checking",
        "timestamp": datetime.now().isoformat()
    }