# config/auth.py 
from typing import Dict, Optional
import hashlib
import base64
import os

def verificar_hash_senha(senha_digitada: str, hash_armazenado: str, usuario: str) -> bool:
    """Verifica se a senha digitada corresponde ao hash armazenado"""
    if not hash_armazenado:
        return False
    
    # Recriar o mesmo salt usado na geração
    salt = f"nandolab_salt_{usuario.lower()}_2026_secure"
    
    # Combinar senha + salt
    senha_com_salt = senha_digitada + salt
    
    # Gerar hash SHA-256
    hash_calculado_bytes = hashlib.sha256(senha_com_salt.encode()).digest()
    hash_calculado = base64.b64encode(hash_calculado_bytes).decode()
    
    # Comparação segura
    return hash_calculado == hash_armazenado

# Carregar hashes do ambiente
HASH_SENHA_NANDO = os.getenv("HASH_SENHA_NANDO")
HASH_SENHA_JROBERSON = os.getenv("HASH_SENHA_JROBERSON")

# Credenciais dos administradores
ADMIN_USERS = {
    '553498937985': {
        'nome': 'Nando',
        'usuario_key': 'NANDO',
        'senha_hash': HASH_SENHA_NANDO,
        'telefone_formatado': '(34) 9893-7985'
    },
    '5511950768793': {
        'nome': 'JRoberson',
        'usuario_key': 'JROBERSON',
        'senha_hash': HASH_SENHA_JROBERSON,
        'telefone_formatado': '(11) 95076-8793'
    }
}

def verificar_admin(telefone_input: str, senha: str) -> Optional[Dict]:
    """Verifica as credenciais do admin"""
    telefone_limpo = ''.join(filter(str.isdigit, telefone_input))
    
    if telefone_limpo.startswith('55'):
        telefone_key = telefone_limpo
    else:
        telefone_key = '55' + telefone_limpo
    
    user_data = ADMIN_USERS.get(telefone_key)
    
    if user_data and user_data['senha_hash']:
        if verificar_hash_senha(senha, user_data['senha_hash'], user_data['usuario_key']):
            return {
                'admin_logged_in': True,
                'admin_telefone': telefone_key,
                'admin_nome': user_data['nome'],
                'admin_telefone_formatado': user_data['telefone_formatado']
            }
    
    return None