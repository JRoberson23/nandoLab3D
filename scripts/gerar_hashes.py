# scripts/gerar_hashes.py
print("🔐 GERADOR DE HASHES - NandoLab 3D")
print("=" * 60)
print("\n⚠️  IMPORTANTE: As senhas devem ter no máximo 72 caracteres")
print("-" * 60)

# Senhas atuais (modifique aqui se necessário)
SENHAS = {
    'NANDO': 'LokiLocao@07012026',          # Senha do Nando
    'JROBERSON': 'CastielPotye@23'          # Senha do JRoberson
}

print("\n📝 SENHAS CONFIGURADAS:")
print("-" * 40)
for usuario, senha in SENHAS.items():
    print(f"👤 {usuario}: {'*' * len(senha)} ({len(senha)} caracteres)")

print("\n⏳ Gerando hashes seguros...")

import hashlib
import base64

print("\n📋 CONTEÚDO PARA O ARQUIVO .env:")
print("=" * 60)
print("\n# =========================================")
print("# HASHS DE SENHA - NANDOLAB 3D")
print("# NUNCA COMPARTILHE ESTE ARQUIVO!")
print("# =========================================")

hashes_gerados = {}

for usuario, senha in SENHAS.items():
    # Usar SHA-256 com salt único para cada usuário
    salt = f"nandolab_salt_{usuario.lower()}_2026_secure"
    hash_input = senha + salt
    
    # Gerar hash SHA-256
    hash_bytes = hashlib.sha256(hash_input.encode()).digest()
    
    # Converter para base64 (mais fácil de armazenar)
    hash_b64 = base64.b64encode(hash_bytes).decode()
    
    hashes_gerados[usuario] = hash_b64
    
    print(f"\n# {usuario} - {SENHAS[usuario][:3]}...")
    print(f"HASH_SENHA_{usuario}={hash_b64}")

print("\n# =========================================")
print("=" * 60)

# Perguntar se quer salvar automaticamente
import os

env_existe = os.path.exists('.env')
print(f"\n📁 Arquivo .env {'já existe' if env_existe else 'não existe'}")

salvar = input("\n💾 Deseja salvar automaticamente no .env? (s/n): ").lower().strip()

if salvar == 's':
    try:
        modo = 'a' if env_existe else 'w'
        
        with open('.env', modo, encoding='utf-8') as f:
            if not env_existe:
                f.write("# =========================================\n")
                f.write("# ARQUIVO DE CONFIGURAÇÃO - NANDOLAB 3D\n")
                f.write("# NUNCA COMPARTILHE OU COMITE NO GIT!\n")
                f.write("# =========================================\n\n")
            
            f.write("# =========================================\n")
            f.write("# HASHS DE SENHA (gerados automaticamente)\n")
            f.write("# =========================================\n")
            
            for usuario in SENHAS:
                f.write(f"\n# {usuario}\n")
                f.write(f"HASH_SENHA_{usuario}={hashes_gerados[usuario]}\n")
            
            f.write("\n# =========================================\n")
        
        print(f"✅ Hashes salvos no arquivo .env!")
        
        # Mostrar preview do arquivo
        print("\n📄 Preview do arquivo .env:")
        print("-" * 40)
        with open('.env', 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            for linha in linhas[-15:]:  # Mostrar últimas 15 linhas
                print(linha.rstrip())
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        print("\n📝 Copie manualmente os hashes acima para o arquivo .env")
else:
    print("\n📝 INSTRUÇÕES MANUAIS:")
    print("1. Crie/abra o arquivo .env na raiz do projeto")
    print("2. Adicione as linhas mostradas acima")
    print("3. Certifique-se de que .env está no .gitignore")

print("\n🔧 PRÓXIMOS PASSOS:")
print("1. ✅ Hashes gerados")
print("2. ⏳ Atualize o config/auth.py para usar os hashes")
print("3. ⏳ Adicione load_dotenv() no app.py")
print("4. ✅ Teste o login")
print("=" * 60)

print("\n🔐 HASHES GERADOS (cópia rápida):")
print("-" * 40)
for usuario in SENHAS:
    print(f"HASH_SENHA_{usuario}={hashes_gerados[usuario]}")
print("=" * 60)