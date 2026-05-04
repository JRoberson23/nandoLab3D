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
    """
    Faz upload de uma imagem para o S3
    conteudo_arquivo: bytes do arquivo (já lido com await read())
    nome_arquivo: nome do arquivo
    content_type: tipo do arquivo (image/jpeg, image/png, etc)
    """
    client = get_s3_client()
    
    try:
        # Faz o upload dos bytes para o S3
        client.upload_fileobj(
            conteudo_arquivo,  # ← agora é bytes, não UploadFile
            S3_BUCKET,
            f"projetos/{nome_arquivo}",
            ExtraArgs={'ContentType': content_type}
        )
        
        # Monta a URL pública
        url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/projetos/{nome_arquivo}"
        print(f"✅ Upload OK: {url}")
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