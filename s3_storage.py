import boto3
import os

S3_BUCKET = "nandolab3d-imagens"
S3_REGION = "us-east-1"

def get_s3_client():
    """Cria e retorna um cliente S3 configurado"""
    return boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

def upload_para_s3(conteudo_arquivo, nome_arquivo, content_type):
    """Faz upload para o S3"""
    
    # ===== LOG DE DEPURAÇÃO =====
    print(f"🔍 Tipo de conteudo_arquivo: {type(conteudo_arquivo)}")
    print(f"🔍 Tamanho: {len(conteudo_arquivo) if hasattr(conteudo_arquivo, '__len__') else 'sem tamanho'}")
    print(f"🔍 Content-Type: {content_type}")
    print(f"🔍 Nome do arquivo: {nome_arquivo}")
    # ============================
    
    client = get_s3_client()
    
    try:
        # Verifica se é bytes, se não for, tenta converter
        if isinstance(conteudo_arquivo, bytes):
            print("✅ É bytes, enviando...")
            client.upload_fileobj(
                conteudo_arquivo,
                S3_BUCKET,
                f"projetos/{nome_arquivo}",
                ExtraArgs={'ContentType': content_type}
            )
        else:
            print(f"❌ Não é bytes! Tipo: {type(conteudo_arquivo)}")
            return None
        
        url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/projetos/{nome_arquivo}"
        print(f"✅ Upload OK: {url}")
        return url
        
    except Exception as e:
        print(f"❌ Erro detalhado no upload: {type(e).__name__}: {e}")
        return None

def deletar_do_s3(nome_arquivo):
    """Deleta uma imagem do S3 (útil para edição/exclusão)"""
    client = get_s3_client()
    
    try:
        client.delete_object(
            Bucket=S3_BUCKET,
            Key=f"projetos/{nome_arquivo}"
        )
        return True
    except Exception as e:
        print(f"❌ Erro ao deletar do S3: {e}")
        return False