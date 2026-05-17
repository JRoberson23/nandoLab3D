import boto3
import os
from io import BytesIO
from botocore.config import Config

# Configurações do Filebase (pegam das variáveis de ambiente no Render)
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "nandolab-imagens")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "https://s3.filebase.com")
URL_EXPIRATION = 3600  # URL válida por 1 hora

def get_s3_client():
    """Cria conexão com o Filebase"""
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=os.environ.get("FILEBASE_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("FILEBASE_SECRET_KEY"),
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

def upload_para_s3(conteudo_arquivo, nome_arquivo, content_type):
    """Faz upload e retorna a CHAVE do objeto (não a URL)"""
    client = get_s3_client()
    try:
        arquivo_bytes = BytesIO(conteudo_arquivo)
        
        # Upload do arquivo
        client.upload_fileobj(
            arquivo_bytes,
            S3_BUCKET,
            f"projetos/{nome_arquivo}",
            ExtraArgs={'ContentType': content_type}
        )
        
        # Retorna a CHAVE do objeto (caminho dentro do bucket)
        # Isso será salvo no banco de dados
        chave_objeto = f"projetos/{nome_arquivo}"
        print(f"✅ Upload OK: {chave_objeto}")
        return chave_objeto
        
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return None

def deletar_do_s3(nome_arquivo):
    """Deleta uma imagem do Filebase"""
    client = get_s3_client()
    try:
        client.delete_object(
            Bucket=S3_BUCKET,
            Key=f"projetos/{nome_arquivo}"
        )
        return True
    except Exception as e:
        print(f"❌ Erro ao deletar: {e}")
        return False