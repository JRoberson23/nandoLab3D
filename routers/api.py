# routers/api.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
import uuid

from models.database import get_db
from models.models import Projeto, Pedido, Produto

router = APIRouter(tags=["API Pública"])


class OrcamentoFormRequest(BaseModel):
    """Modelo para o formulário de orçamento"""
    nome: str
    email: str
    telefone: str = ""
    tipo_projeto: str
    projeto: str
    prazo: str = ""


# ========== API PÚBLICA PARA O SITE ==========

@router.get("/status")
async def api_status():
    """Status da API"""
    return {
        "api": "online",
        "service": "NandoLab 3D",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@router.get("/portfolio")
async def get_portfolio(
    db: Session = Depends(get_db),
    categoria: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """API para listar projetos do portfólio"""
    query = db.query(Projeto).filter(Projeto.publicado == True)
    
    if categoria:
        query = query.filter(Projeto.categoria == categoria)
    
    projetos = query.order_by(Projeto.destaque.desc(), Projeto.created_at.desc()).limit(limit).all()
    
    return {
        "count": len(projetos),
        "projetos": [
            {
                "id": p.id,
                "titulo": p.titulo,
                "descricao": p.descricao,
                "categoria": p.categoria,
                "material": p.material,
                "imagens": p.imagens.split(",") if p.imagens else [],
                "data_conclusao": p.data_conclusao.isoformat() if p.data_conclusao else None,
                "destaque": p.destaque
            }
            for p in projetos
        ]
    }

@router.get("/projeto/{projeto_id}")
async def get_projeto_detalhe(projeto_id: int, db: Session = Depends(get_db)):
    """API para detalhes de um projeto específico"""
    projeto = db.query(Projeto).filter(Projeto.id == projeto_id, Projeto.publicado == True).first()
    
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    return {
        "id": projeto.id,
        "titulo": projeto.titulo,
        "descricao": projeto.descricao,
        "categoria": projeto.categoria,
        "material": projeto.material,
        "imagens": projeto.imagens.split(",") if projeto.imagens else [],
        "data_conclusao": projeto.data_conclusao.isoformat() if projeto.data_conclusao else None,
        "cliente": projeto.cliente,
        "created_at": projeto.created_at.isoformat() if projeto.created_at else None
    }

@router.get("/servicos")
async def get_servicos(db: Session = Depends(get_db)):
    """API para listar serviços/produtos disponíveis"""
    produtos = db.query(Produto).filter(Produto.ativo == True).order_by(Produto.nome).all()
    
    return {
        "servicos": [
            {
                "id": p.id,
                "nome": p.nome,
                "descricao": p.descicao,  # Note: no seu models.py está "descicao" (com i)
                "tipo": p.tipo,
                "preco_base": p.preco_base,
                "imagem": p.imagem
            }
            for p in produtos
        ]
    }

@router.post("/orcamento")
async def criar_orcamento(
    nome: str,
    email: str,
    telefone: str,
    descricao: str,
    projeto_titulo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """API para criar um novo orçamento"""
    # Aqui você pode adicionar validações
    if not nome or not email or not descricao:
        raise HTTPException(
            status_code=400, 
            detail="Nome, email e descrição são obrigatórios"
        )
    
    # Criar novo pedido
    novo_pedido = Pedido(
        nome_cliente=nome,
        email=email,
        telefone=telefone,
        titulo_projeto=projeto_titulo or "Orçamento sem título",
        descricao=descricao,
        status="pendente"
    )
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    
    return {
        "success": True,
        "message": "Orçamento recebido com sucesso!",
        "pedido_id": novo_pedido.id,
        "next_step": "Entraremos em contato em até 24h."
    }

@router.get("/categorias")
async def get_categorias(db: Session = Depends(get_db)):
    """API para listar categorias disponíveis"""
    categorias = db.query(Projeto.categoria).filter(
        Projeto.publicado == True,
        Projeto.categoria.isnot(None)
    ).distinct().all()
    
    return {
        "categorias": [cat[0] for cat in categorias if cat[0]]
    }


@router.post("/salvar-orcamento")
async def salvar_orcamento_form(
    request: OrcamentoFormRequest,
    db: Session = Depends(get_db)
):
    """
    Salva orçamento do formulário web no banco de dados
    (Para ser chamado pelo JavaScript do formulário - VERSÃO SEM IMAGEM)
    """
    try:
        # Criar novo pedido
        novo_pedido = Pedido(
            nome_cliente=request.nome,
            email=request.email,
            telefone=request.telefone,
            titulo_projeto=f"[{request.tipo_projeto}] - Orçamento via site",
            descricao=f"""Tipo: {request.tipo_projeto}
Prazo: {request.prazo}
Descrição:
{request.projeto}""",
            status="pendente"
        )
        
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)
        
        return {
            "success": True,
            "message": "Orçamento salvo no banco de dados",
            "pedido_id": novo_pedido.id
        }
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao salvar orçamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao salvar orçamento")


@router.post("/salvar-orcamento-com-imagem")
async def salvar_orcamento_com_imagem(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    tipo_projeto: str = Form(...),
    projeto: str = Form(...),
    prazo: str = Form(""),
    imagem: UploadFile = File(None),  # Campo opcional
    db: Session = Depends(get_db)
):
    """
    Salva orçamento com imagem opcional
    (Para ser chamado pelo JavaScript do formulário - VERSÃO COM IMAGEM)
    """
    try:
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
        
        # Processar imagem se foi enviada
        if imagem and imagem.filename:
            try:
                # Criar diretório para uploads se não existir
                upload_dir = "static/uploads/orcamentos"
                os.makedirs(upload_dir, exist_ok=True)
                
                # Gerar nome único para o arquivo
                file_ext = os.path.splitext(imagem.filename)[1]
                unique_filename = f"{uuid.uuid4().hex}{file_ext}"
                file_path = os.path.join(upload_dir, unique_filename)
                
                # Salvar arquivo
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(imagem.file, buffer)
                
                # Salvar caminho no banco
                novo_pedido.arquivos_referencia = f"/{file_path}"
                print(f"✅ Imagem salva: {file_path}")
                
            except Exception as img_error:
                print(f"⚠️ Erro ao salvar imagem: {img_error}")
                # Não falhar o pedido se a imagem der erro
        
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)
        
        return {
            "success": True,
            "message": "Orçamento salvo com sucesso",
            "pedido_id": novo_pedido.id,
            "tem_imagem": bool(imagem and imagem.filename)
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao salvar orçamento com imagem: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erro interno ao salvar orçamento"
        )