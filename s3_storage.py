import boto3
import os
from datetime import datetime

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

def upload_para_s3(arquivo, nome_arquivo):
    """
    Faz upload de uma imagem para o S3
    Retorna a URL pública da imagem
    """
    client = get_s3_client()
    
    try:
        # Faz o upload do arquivo
        client.upload_fileobj(
            arquivo,
            S3_BUCKET,
            f"projetos/{nome_arquivo}",
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        
        # Monta a URL pública
        url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/projetos/{nome_arquivo}"
        
        return url
        
    except Exception as e:
        print(f"❌ Erro no upload para S3: {e}")
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