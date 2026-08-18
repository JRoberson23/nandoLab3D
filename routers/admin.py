from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException # type: ignore
from fastapi.responses import HTMLResponse, RedirectResponse # type: ignore
from sqlalchemy.orm import Session
import os
from sqlalchemy import func
from datetime import datetime
from typing import Optional, List
import shutil

from models.database import get_db
from models.models import Projeto, Pedido, Produto, Depoimento, Cliente
from config.auth import verificar_admin
from s3_storage import upload_para_s3

router = APIRouter(prefix="/admin", tags=["Administração"])
from config.templates import templates

# ========== FUNÇÃO DE VERIFICAÇÃO DE AUTENTICAÇÃO ==========

def verificar_autenticacao(request: Request):
    """Verifica se o usuário está autenticado"""
    return request.session.get("admin_logged_in", False)

# ========== ROTAS DE LOGIN/LOGOUT ==========

@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Página de login do admin"""
    # Se já está logado, redireciona para dashboard
    if verificar_autenticacao(request):
        return RedirectResponse("/admin/dashboard")
    
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )


@router.post("/login")
async def admin_login(
    request: Request,
    telefone: str = Form(...),
    senha: str = Form(...)
):
    """Processar login do admin"""
    # Verificar credenciais
    resultado = verificar_admin(telefone, senha)  
    
    if resultado:
        # Armazenar dados na sessão
        request.session.update(resultado)
        return RedirectResponse("/admin/dashboard", status_code=303)
    else:
        return templates.TemplateResponse(
            "admin/login.html",  
            {
                "request": request, 
                "error": "Usuario ou senha incorretos"
            }
        )

@router.get("/logout")
async def admin_logout(request: Request):
    """Logout do admin"""
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)

# ========== ÁREA ADMINISTRATIVA PROTEGIDA ==========

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard administrativo"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    try:
        # Estatísticas básicas
        total_projetos = db.query(Projeto).count()
        total_pedidos = db.query(Pedido).count()
        total_depoimentos = db.query(Depoimento).count()
        total_clientes = db.query(Cliente).count()
        
        # Pedidos por status
        pedidos_pendentes = db.query(Pedido).filter(Pedido.status == "pendente").count()
        pedidos_aprovados = db.query(Pedido).filter(Pedido.status == "aprovado").count()
        pedidos_concluidos = db.query(Pedido).filter(Pedido.status == "concluido").count()
        
        # Últimos projetos (limite 5)
        ultimos_projetos = db.query(Projeto)\
            .order_by(Projeto.created_at.desc())\
            .limit(5)\
            .all()
        
        # Últimos pedidos (limite 5)
        ultimos_pedidos = db.query(Pedido)\
            .order_by(Pedido.data_pedido.desc())\
            .limit(5)\
            .all()
        
        # Projetos por categoria (para gráfico futuro)
        projetos_por_categoria = db.query(
            Projeto.categoria,
            func.count(Projeto.id).label('total')
        ).filter(Projeto.categoria.isnot(None))\
         .group_by(Projeto.categoria)\
         .all()
        
        return templates.TemplateResponse(
            "admin/dashboard.html",
            {
                "request": request,
                "total_projetos": total_projetos,
                "total_pedidos": total_pedidos,
                "total_depoimentos": total_depoimentos,
                "total_clientes": total_clientes,
                "pedidos_pendentes": pedidos_pendentes,
                "pedidos_aprovados": pedidos_aprovados,
                "pedidos_concluidos": pedidos_concluidos,
                "ultimos_projetos": ultimos_projetos,
                "ultimos_pedidos": ultimos_pedidos,
                "projetos_por_categoria": projetos_por_categoria,
                "titulo": "Dashboard - Admin"
            }
        )
        
    except Exception as e:
        # Em caso de erro, retorna com valores padrão
        print(f"Erro no dashboard: {e}")
        return templates.TemplateResponse(
            "admin/dashboard.html",
            {
                "request": request,
                "total_projetos": 0,
                "total_pedidos": 0,
                "total_depoimentos": 0,
                "total_clientes": 0,
                "pedidos_pendentes": 0,
                "pedidos_aprovados": 0,
                "pedidos_concluidos": 0,
                "ultimos_projetos": [],
                "ultimos_pedidos": [],
                "projetos_por_categoria": [],
                "titulo": "Dashboard - Admin"
            }
        )

@router.get("/projetos", response_class=HTMLResponse)
async def admin_projetos(request: Request, db: Session = Depends(get_db)):
    """Gerenciar projetos"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    projetos = db.query(Projeto).order_by(Projeto.created_at.desc()).all()
    
    return templates.TemplateResponse(
        "admin/projetos.html",
        {
            "request": request,
            "projetos": projetos,
            "titulo": "Gerenciar Projetos"
        }
    )

@router.get("/pedidos")
async def admin_pedidos(
    request: Request, 
    db: Session = Depends(get_db),
    status: str = None
):
    """Página de gerenciamento de pedidos"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    # Construir query base
    query = db.query(Pedido)
    
    # Filtrar por status se fornecido
    if status:
        query = query.filter(Pedido.status == status)
    
    # Ordenar pela data do pedido
    pedidos = query.order_by(Pedido.data_pedido.desc()).all()
    
    # Contadores
    total_pedidos = db.query(Pedido).count()
    pedidos_pendentes = db.query(Pedido).filter(Pedido.status == "pendente").count()
    pedidos_aprovados = db.query(Pedido).filter(Pedido.status == "aprovado").count()
    pedidos_concluidos = db.query(Pedido).filter(Pedido.status == "concluido").count()
    
    return templates.TemplateResponse(
        "admin/pedidos.html",
        {
            "request": request,
            "pedidos": pedidos,
            "total_pedidos": total_pedidos,
            "pedidos_pendentes": pedidos_pendentes,
            "pedidos_aprovados": pedidos_aprovados,
            "pedidos_concluidos": pedidos_concluidos,
            "filtro_status": status
        }
    )

@router.get("/clientes")
async def admin_clientes(request: Request, db: Session = Depends(get_db)):
    """Página de gerenciamento de clientes"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    clientes = db.query(Cliente).order_by(Cliente.data_cadastro.desc()).all()
    
    return templates.TemplateResponse(
        "admin/clientes.html",
        {
            "request": request,
            "clientes": clientes
        }
    )

@router.get("/depoimentos")
async def admin_depoimentos(request: Request, db: Session = Depends(get_db)):
    """Página de gerenciamento de depoimentos"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    depoimentos = db.query(Depoimento).order_by(Depoimento.created_at.desc()).all()
    
    total = len(depoimentos)
    aprovados = sum(1 for d in depoimentos if d.aprovado)
    pendentes = total - aprovados
    media_avaliacao = sum(d.avaliacao for d in depoimentos) / total if total > 0 else 0
    
    return templates.TemplateResponse(
        "admin/depoimentos.html",
        {
            "request": request,
            "depoimentos": depoimentos,
            "total_depoimentos": total,
            "aprovados_count": aprovados,
            "pendentes_count": pendentes,
            "media_avaliacao": round(media_avaliacao, 1)
        }
    )

@router.get("/configuracoes")
async def admin_configuracoes(request: Request, db: Session = Depends(get_db)):
    """Página de configurações do sistema"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    return templates.TemplateResponse(
        "admin/configuracoes.html",
        {"request": request}
    )


# ========== CONFIGURAÇÕES DO SISTEMA ==========

@router.get("/configuracoes/dados")
async def get_configuracoes(db: Session = Depends(get_db)):
    """Retorna todas as configurações do sistema"""
    try:
        # Você pode criar uma tabela Configuracao no futuro
        # Por enquanto, retornamos valores padrão
        configuracoes = {
            "geral": {
                "site_nome": "NandoLab 3D",
                "site_slogan": "Inovação em impressão 3D",
                "site_descricao": "Impressão 3D de alta qualidade para projetos arquitetônicos, peças personalizadas e protótipos.",
                "timezone": "America/Sao_Paulo",
                "idioma": "pt-BR",
                "manutencao": False
            },
            "site": {
                "logo": "/static/imagens/Logo.png",
                "favicon": "/static/imagens/favicon.ico",
                "cor_primaria": "#2A5C8B",
                "cor_secundaria": "#F8B400",
                "keywords": "impressão 3D, protótipos, arquitetura, maquetes, personalizado"
            },
            "seo": {
                "title": "NandoLab 3D | Impressão 3D Profissional",
                "description": "Impressão 3D de alta qualidade, maquetes arquitetônicas, protótipos e peças personalizadas. Tecnologia e inovação para seu projeto.",
                "keywords": "impressão 3D, protótipos, maquetes, arquitetura, impressão 3D serviços, peças personalizadas",
                "google_analytics": "",
                "og_image": "/static/imagens/og-image.jpg"
            },
            "social": {
                "instagram": "nandolab3d",
                "instagram_url": "https://instagram.com/nandolab3d",
                "facebook": "",
                "whatsapp": "(11) 95076-8793",
                "whatsapp_link": "https://wa.me/5511950768793",
                "show_feed": "sim",
                "embed_code": ""
            }
        }
        
        return {"success": True, "configuracoes": configuracoes}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/configuracoes/salvar")
async def salvar_configuracoes(
    request: Request,
    tipo: str = Form(...),  # "geral", "site", "seo", "social"
    dados: str = Form(...)  # JSON string com os dados
):
    """Salva as configurações do sistema"""
    # Verificar autenticação
    if not verificar_autenticacao(request):
        return {"success": False, "error": "Não autenticado"}
    
    try:
        import json
        dados_dict = json.loads(dados)
        
        # Aqui você salvaria no banco de dados
        # Por enquanto, apenas simula o salvamento
        
        print(f"Configurações salvas - Tipo: {tipo}, Dados: {dados_dict}")
        
        return {
            "success": True, 
            "message": "Configurações salvas com sucesso!",
            "tipo": tipo
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== BACKUP ==========

@router.get("/backup/exportar/{tipo}")
async def exportar_backup(
    request: Request,
    tipo: str,  # "projetos", "clientes", "tudo"
    db: Session = Depends(get_db)
):
    """Exporta dados para backup"""
    if not verificar_autenticacao(request):
        return {"success": False, "error": "Não autenticado"}
    
    try:
        from datetime import datetime
        import json
        from fastapi.responses import FileResponse # type: ignore
        import tempfile
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if tipo == "projetos":
            # Exportar projetos como JSON
            projetos = db.query(Projeto).all()
            dados = [{
                "id": p.id,
                "titulo": p.titulo,
                "descricao": p.descricao,
                "categoria": p.categoria,
                "status": p.status,
                "created_at": p.created_at.isoformat() if p.created_at else None
            } for p in projetos]
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
                temp_path = f.name
            
            return FileResponse(
                temp_path,
                filename=f"backup_projetos_{timestamp}.json",
                media_type="application/json"
            )
            
        elif tipo == "clientes":
            # Exportar clientes como CSV
            clientes = db.query(Cliente).all()
            csv_lines = ["Nome,Email,Telefone,Data Cadastro"]
            for c in clientes:
                csv_lines.append(f'"{c.nome}","{c.email}","{c.telefone}","{c.data_cadastro}"')
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write("\n".join(csv_lines))
                temp_path = f.name
            
            return FileResponse(
                temp_path,
                filename=f"backup_clientes_{timestamp}.csv",
                media_type="text/csv"
            )
            
        elif tipo == "tudo":
            # Exportar tudo (simplificado)
            projetos = db.query(Projeto).all()
            clientes = db.query(Cliente).all()
            pedidos = db.query(Pedido).all()
            depoimentos = db.query(Depoimento).all()
            
            dados = {
                "projetos": [{"id": p.id, "titulo": p.titulo} for p in projetos],
                "clientes": [{"id": c.id, "nome": c.nome} for c in clientes],
                "pedidos": [{"id": pd.id, "cliente": pd.cliente_nome} for pd in pedidos],
                "depoimentos": [{"id": d.id, "cliente": d.cliente_nome} for d in depoimentos],
                "exportado_em": datetime.now().isoformat()
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
                temp_path = f.name
            
            return FileResponse(
                temp_path,
                filename=f"backup_completo_{timestamp}.json",
                media_type="application/json"
            )
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    finally:
        # Limpar arquivo temporário após enviar
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)

@router.post("/backup/agendar")
async def agendar_backup(
    request: Request,
    frequencia: str = Form(...),
    manter_dias: int = Form(...)
):
    """Agenda backup automático"""
    if not verificar_autenticacao(request):
        return {"success": False, "error": "Não autenticado"}
    
    # Aqui você implementaria um agendador real
    # Por enquanto, apenas registra a preferência
    
    request.session["backup_config"] = {
        "frequencia": frequencia,
        "manter_dias": manter_dias,
        "agendado_em": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "message": f"Backup {frequencia} agendado. Serão mantidos os últimos {manter_dias} dias."
    }

# ========== ROTAS PARA GERENCIAR PROJETOS ==========

@router.get("/projetos/novo", response_class=HTMLResponse)
async def novo_projeto_form(request: Request, db: Session = Depends(get_db)):
    """Exibe formulário para criar novo projeto"""
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    return templates.TemplateResponse(
        "admin/novo_projeto.html",
        {
            "request": request,
            "titulo": "Novo Projeto"
        }
    )

@router.post("/projetos/novo")
async def criar_projeto(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    material: str = Form(...),
    data_conclusao: Optional[str] = Form(None),
    publicado: bool = Form(False),
    destaque: bool = Form(False),
    imagem: UploadFile = File(...),
    imagens_extra: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    """Cria um novo projeto com upload de imagem para S3"""
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    try:
        # ===== 1. VALIDAR IMAGEM =====
        if not imagem.content_type.startswith('image/'):
            return templates.TemplateResponse(
                "admin/novo_projeto.html",
                {"request": request, "error": "Arquivo não é uma imagem válida", "titulo": "Novo Projeto"}
            )
        
        # Verificar tamanho (5MB max)
        contents = await imagem.read()
        if len(contents) > 5 * 1024 * 1024:
            return templates.TemplateResponse(
                "admin/novo_projeto.html",
                {"request": request, "error": "Imagem muito grande! Tamanho máximo: 5MB", "titulo": "Novo Projeto"}
            )
        
        # Criar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(imagem.filename)[1]
        filename = f"projeto_{timestamp}{file_extension}"
        
        # ===== 2. ENVIAR PARA O S3 =====
        await imagem.seek(0)
        conteudo_imagem = await imagem.read()
        # ===== LOG DE DEPURAÇÃO =====
        print(f"🔍 Tipo do conteúdo após read: {type(conteudo_imagem)}")
        print(f"🔍 Tamanho: {len(conteudo_imagem)} bytes")
        print(f"🔍 Content-Type: {imagem.content_type}")
        # ============================
        url_imagem = upload_para_s3(conteudo_imagem, filename, imagem.content_type)

        if not url_imagem:
            return templates.TemplateResponse(
                "admin/novo_projeto.html",
                {"request": request, "error": "Erro ao enviar imagem para o S3. Tente novamente.", "titulo": "Novo Projeto"}
            )
        
        # ===== 3. IMAGENS EXTRAS =====
        imagens_extra_urls = []
        if imagens_extra:
            for i, img in enumerate(imagens_extra):
                if img and img.content_type.startswith('image/'):
                    extra_filename = f"galeria_{timestamp}_{i}{os.path.splitext(img.filename)[1]}"
                    await img.seek(0)
                    conteudo_extra = await img.read()
                    url_extra = upload_para_s3(conteudo_extra, extra_filename, img.content_type)
                    if url_extra:
                        imagens_extra_urls.append(url_extra)
        
        # ===== 4. CRIAR PROJETO COM AS URLs DO S3 =====
        projeto = Projeto(
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            material=material,
            data_conclusao=datetime.strptime(data_conclusao, '%Y-%m-%d') if data_conclusao else None,
            publicado=publicado,
            destaque=destaque,
            imagem_principal=url_imagem,
            imagens_extra=",".join(imagens_extra_urls) if imagens_extra_urls else None,
        )
        
        db.add(projeto)
        db.commit()
        db.refresh(projeto)
        
        return RedirectResponse("/admin/projetos", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar projeto: {e}")
        return templates.TemplateResponse(
            "admin/novo_projeto.html",
            {"request": request, "error": f"Erro ao criar projeto: {str(e)}", "titulo": "Novo Projeto"}
        )
    

# ========== ROTAS PARA GERENCIAR PEDIDOS ==========

@router.get("/pedidos/{pedido_id}/detalhes")
async def detalhes_pedido(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes de um pedido específico"""
    if not verificar_autenticacao(request):
        return HTMLResponse("<div class='alert alert-danger'>Não autenticado</div>")
    
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        # Retorna HTML SIMPLES de erro
        return HTMLResponse(
            """
            <div class='alert alert-warning'>
                <i class='fas fa-exclamation-triangle me-2'></i>
                Pedido não encontrado
            </div>
            """
        )
    
    return templates.TemplateResponse("admin/partials/detalhes_pedido.html", {
        "request": request,
        "pedido": pedido
    })

@router.post("/pedidos/{pedido_id}/aprovar")
async def aprovar_pedido(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    """Aprova um pedido"""
    if not verificar_autenticacao(request):
        return {"success": False, "error": "Não autenticado"}
    
    try:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            pedido.status = "aprovado"
            pedido.data_aprovacao = datetime.now()
            db.commit()
            return {"success": True, "message": "Pedido aprovado"}
        return {"success": False, "error": "Pedido não encontrado"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@router.post("/pedidos/{pedido_id}/rejeitar")
async def rejeitar_pedido(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    """Rejeita um pedido"""
    if not verificar_autenticacao(request):
        return {"success": False, "error": "Não autenticado"}
    
    try:
        from pydantic import BaseModel # type: ignore
        
        class RejeitarData(BaseModel):
            motivo: str
        
        data = await request.json()
        motivo = data.get("motivo", "")
        
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            pedido.status = "rejeitado"
            # Adiciona o motivo na descrição
            pedido.descricao = f"{pedido.descricao}\n\n--- REJEITADO ---\nMotivo: {motivo}\nData: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            db.commit()
            return {"success": True, "message": "Pedido rejeitado"}
        return {"success": False, "error": "Pedido não encontrado"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@router.post("/pedidos/{pedido_id}/concluir")
async def concluir_pedido(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    """Marca um pedido como concluído"""
    if not verificar_autenticacao(request):
        return {"success": False, "error": "Não autenticado"}
    
    try:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            pedido.status = "concluido"
            pedido.data_conclusao = datetime.now()
            db.commit()
            return {"success": True, "message": "Pedido concluído"}
        return {"success": False, "error": "Pedido não encontrado"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@router.get("/pedidos/editar/{pedido_id}")
async def editar_pedido_form(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    """Formulário para editar pedido"""
    if not verificar_autenticacao(request):
        return RedirectResponse("/admin/login")
    
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        return RedirectResponse("/admin/pedidos")
    
    return templates.TemplateResponse("admin/editar_pedido.html", {
        "request": request,
        "pedido": pedido,
        "titulo": f"Editar Pedido #{pedido.id}"
    })