from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

#Usuários do sistema(Nando e clientes se fizerem login)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column (Integer,primary_key=True, index=True)
    email = Column(String(100),unique=True, index=True,nullable=False)
    nome = Column(String(100),nullable=False)
    senha_hash = Column(String(200))
    telefone = Column(String(20))
    is_admin = Column(Boolean, default=False)
    is_cliente = Column(Boolean, default=True)
    data_cadastro = Column(DateTime,default=func.now())
    ultimo_login = Column(DateTime)

#Clientes (podem fazer pedidos)
class Cliente(Base):
    __tablename__="clientes"

    id = Column(Integer,primary_key=True, index=True)
    nome_completo = Column(String(200),nullable=False)
    email = Column(String(200), unique=True,index=True)
    telefone = Column(String(20))
    endereco = Column(Text)
    data_cadastro = Column(DateTime, default=func.now())

    #Relacionamento com pedidos
    pedidos = relationship("Pedido",back_populates="cliente")

#Projetos do portfólio
class Projeto(Base):
    __tablename__ ="projetos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200),nullable=False)
    descricao = Column(Text)
    categoria = Column(String(100))
    material = Column(String(100))
    imagem_principal = Column(String(500), nullable=True)
    imagens_extra = Column(Text, nullable=True)
    data_conclusao = Column(Date)
    publicado = Column(Boolean, default=True)
    destaque = Column(Boolean, default=False)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime,default=func.now(),onupdate=func.now())

    # ===== PROPRIEDADES ÚTEIS =====
    @property
    def url_imagem(self):
        """Retorna a URL completa da imagem principal"""
        if self.imagem_principal:
            return f"/static/uploads/projetos/{self.imagem_principal}"
        return "/static/imagens/projeto-default.jpg"  # Você pode criar uma imagem padrão
    
    @property
    def url_imagem(self):
        """Retorna a URL completa da imagem principal (suporta S3 e local)"""
        if not self.imagem_principal:
            return "/static/imagens/projeto-default.jpg"
        
        # Se já for uma URL completa (começa com http), retorna diretamente
        if self.imagem_principal.startswith('http'):
            return self.imagem_principal
        
        # Caso contrário, assume que é arquivo local (projetos antigos)
        return f"/static/uploads/projetos/{self.imagem_principal}"

#Pedido/Orçamentos
class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"),nullable=True)
    nome_cliente = Column(String(200),nullable=False)
    email = Column(String(200),nullable=False)
    telefone = Column(String(20))

    #Detalhes do pedido
    titulo_projeto = Column(String(200),nullable=False)
    descricao = Column(Text, nullable=False)
    material_desejado = Column(String(100))
    dimensoes = Column(String(100))
    prazo_desejado = Column(Integer)

    #Status e valores
    status = Column(String(50),default="pendente")
    valor_orcamento = Column(Float)
    valor_pago = Column(Float, default=0)
    forma_pagamento = Column(String(50))

    #Datas importantes
    data_pedido = Column(DateTime, default=func.now())
    data_orcamento = Column(DateTime)
    data_aprovacao = Column(DateTime)
    data_conclusao = Column(DateTime)

    #Arquivos
    arquivos_referencia = Column(Text)

    #Relacionamentos
    cliente = relationship("Cliente", back_populates="pedidos")

#Produtos/Serviços para venda
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    tipo =Column(String(50))
    preco_base = Column(Float)
    imagem = Column(String(500))
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


# ========== NOVAS TABELAS PARA O CMS ==========

class SiteConfig(Base):
    """Configurações gerais do site"""
    __tablename__ = "site_config"
    
    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String(100), unique=True, index=True, nullable=False)
    valor = Column(Text)
    tipo = Column(String(50), default='text')  # text, number, color, boolean, image
    categoria = Column(String(50))  # general, contact, social, appearance
    descricao = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Depoimento(Base):
    """Depoimentos dos clientes para a página inicial"""
    __tablename__ = "depoimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    empresa = Column(String(200))
    cargo = Column(String(100))
    texto = Column(Text, nullable=False)
    avaliacao = Column(Integer, default=5)  # 1-5 estrelas
    foto = Column(String(500))  # URL da foto
    aprovado = Column(Boolean, default=True)
    ordem = Column(Integer, default=0)  # Para ordenar na exibição
    created_at = Column(DateTime, default=func.now())

class Material(Base):
    """Materiais para tabela de preços (página Serviços)"""
    __tablename__ = "materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    caracteristicas = Column(Text)
    aplicacoes = Column(Text)
    durabilidade = Column(Integer)  # 1-100 para a barra de progresso
    preco_base = Column(Float)
    badge = Column(String(50))  # eco, resistente, versátil, etc
    ativo = Column(Boolean, default=True)
    ordem = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

class CategoriaProjeto(Base):
    """Categorias para organizar projetos (Arquitetura, Escultura, etc)"""
    __tablename__ = "categorias_projeto"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), unique=True)  # arquitetura, escultura, etc
    icone = Column(String(50))  # fas fa-building, fas fa-monument, etc
    descricao = Column(Text)
    ativa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())