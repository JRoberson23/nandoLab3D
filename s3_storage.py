import boto3
import os
from io import BytesIO
from botocore.config import Config
from botocore.exceptions import ClientError

# Configurações - usando o endpoint correto do bucket!
S3_BUCKET = "nandolab-imagens"
S3_ENDPOINT = "https://s3.filebase.io"  # ← mudou para .io
URL_EXPIRATION = 3600

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
    client = get_s3_client()
    try:
        arquivo_bytes = BytesIO(conteudo_arquivo)
        
        # 🔍 LOGs de debug
        print(f"🔍 Bucket: {S3_BUCKET}")
        print(f"🔍 Endpoint: {S3_ENDPOINT}")
        print(f"🔍 Arquivo: {nome_arquivo}")
        print(f"🔍 Tamanho: {len(conteudo_arquivo)} bytes")
        
        # Tenta fazer o upload
        client.upload_fileobj(
            arquivo_bytes,
            S3_BUCKET,
            f"projetos/{nome_arquivo}",
            ExtraArgs={'ContentType': content_type}
        )
        
        chave_objeto = f"projetos/{nome_arquivo}"
        print(f"✅ Upload OK: {chave_objeto}")
        return chave_objeto
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        print(f"❌ Erro ClientError: {error_code} - {error_msg}")
        return None
    except Exception as e:
        print(f"❌ Erro geral: {type(e).__name__}: {e}")
        return None

def deletar_do_s3(nome_arquivo):
    client = get_s3_client()
    try:
        client.delete_object(
            Bucket=S3_BUCKET,
            Key=f"projetos/{nome_arquivo}"
        )
        return True
    except Exception as e:
        print(f"❌ Erro ao deletar: {e}")
        return None