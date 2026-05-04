import boto3
import os
from io import BytesIO  # ← ADICIONE ESTA IMPORTAÇÃO

S3_BUCKET = "nandolab3d-imagens"
S3_REGION = "us-east-1"

def get_s3_client():
    return boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

def upload_para_s3(conteudo_arquivo, nome_arquivo, content_type):
    """
    Faz upload de uma imagem para o S3
    conteudo_arquivo: bytes do arquivo
    """
    client = get_s3_client()
    
    try:
        # Converte bytes para um objeto file-like que o boto3 entende
        arquivo_bytes = BytesIO(conteudo_arquivo)
        
        client.upload_fileobj(
            arquivo_bytes,  # ← agora é um objeto file-like!
            S3_BUCKET,
            f"projetos/{nome_arquivo}",
            ExtraArgs={'ContentType': content_type}
        )
        
        url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/projetos/{nome_arquivo}"
        print(f"✅ Upload OK: {url}")
        return url
        
    except Exception as e:
        print(f"❌ Erro detalhado no upload: {type(e).__name__}: {e}")
        return None

def deletar_do_s3(nome_arquivo):
    """Deleta uma imagem do S3"""
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