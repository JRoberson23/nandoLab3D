# test_tudo.py (crie na raiz do projeto)
from dotenv import load_dotenv
load_dotenv()

import os

print("🔐 TESTE DO SISTEMA DE AUTENTICAÇÃO")
print("=" * 60)

# Teste 1: Verificar se as variáveis foram carregadas
print("\n1️⃣  VARIÁVEIS DE AMBIENTE:")
print("-" * 40)

# Listar todas as variáveis que começam com HASH_SENHA_
env_vars = {k: v for k, v in os.environ.items() if k.startswith('HASH_SENHA_')}

if env_vars:
    print("✅ Variáveis carregadas do .env:")
    for var_name, var_value in env_vars.items():
        print(f"   {var_name}: {var_value[:20]}...")
else:
    print("❌ NENHUMA variável HASH_SENHA_ encontrada!")
    print("\n⚠️  Possíveis problemas:")
    print("   1. Arquivo .env não existe")
    print("   2. .env não está na raiz do projeto")
    print("   3. Variáveis com nomes diferentes")
    
    # Mostrar o que está no .env
    try:
        with open('.env', 'r') as f:
            print(f"\n📄 Conteúdo do arquivo .env:")
            print("-" * 40)
            print(f.read())
            print("-" * 40)
    except FileNotFoundError:
        print("\n❌ Arquivo .env NÃO encontrado!")
    except Exception as e:
        print(f"\n⚠️  Erro ao ler .env: {e}")

print("\n2️⃣  TESTE DO MÓDULO auth.py:")
print("-" * 40)

try:
    from config.auth import verificar_admin, verificar_hash_senha
    
    print("✅ Módulo auth.py importado com sucesso!")
    
    # Testar se as funções existem
    print(f"   Função verificar_admin: {'✅' if callable(verificar_admin) else '❌'}")
    print(f"   Função verificar_hash_senha: {'✅' if callable(verificar_hash_senha) else '❌'}")
    
    # Pegar hashes
    hash_nando = os.getenv("HASH_SENHA_NANDO")
    hash_jroberson = os.getenv("HASH_SENHA_JROBERSON")
    
    if hash_nando and hash_jroberson:
        print("\n3️⃣  TESTE DE VERIFICAÇÃO DE SENHA:")
        print("-" * 40)
        
        # Testar senha do Nando
        senha_correta_nando = "LokiLocao@07012026"
        senha_errada = "senha_qualquer"
        
        resultado_correto = verificar_hash_senha(senha_correta_nando, hash_nando, "NANDO")
        resultado_errado = verificar_hash_senha(senha_errada, hash_nando, "NANDO")
        
        print(f"   Senha do Nando correta: {'✅ Aceita' if resultado_correto else '❌ Rejeitada (PROBLEMA!)'}")
        print(f"   Senha do Nando errada: {'❌ Aceita (PROBLEMA!)' if resultado_errado else '✅ Rejeitada (correto)'}")
        
        # Testar função completa
        print("\n4️⃣  TESTE DA FUNÇÃO COMPLETA:")
        print("-" * 40)
        
        resultado = verificar_admin("3498937985", senha_correta_nando)
        print(f"   Login do Nando (senha correta): {'✅ Sucesso' if resultado else '❌ Falhou (PROBLEMA!)'}")
        
        resultado = verificar_admin("3498937985", senha_errada)
        print(f"   Login do Nando (senha errada): {'❌ Sucesso (PROBLEMA!)' if resultado else '✅ Falhou (correto)'}")
        
    else:
        print("❌ Hashes não encontrados nas variáveis de ambiente!")
        
except ImportError as e:
    print(f"❌ Erro ao importar config.auth: {e}")
    print("\n⚠️  Verifique se o arquivo config/auth.py existe e está correto.")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("📝 RESUMO:")
print("=" * 60)

# Verificar arquivos importantes
arquivos_importantes = [
    ('.env', 'Arquivo de variáveis'),
    ('config/auth.py', 'Configuração de autenticação'),
    ('app.py', 'Arquivo principal')
]

print("\n📁 VERIFICAÇÃO DE ARQUIVOS:")
for arquivo, descricao in arquivos_importantes:
    existe = os.path.exists(arquivo)
    print(f"   {arquivo} ({descricao}): {'✅ Existe' if existe else '❌ FALTANDO!'}")

print("\n🔧 PRÓXIMOS PASSOS:")
if os.path.exists('.env'):
    print("   1. ✅ .env existe")
    print("   2. ⏳ Verifique se load_dotenv() está no app.py")
    print("   3. ⏳ Teste o login no navegador")
else:
    print("   1. ❌ Crie o arquivo .env")
    print("   2. ⏳ Adicione os hashes gerados")
    print("   3. ⏳ Adicione load_dotenv() no app.py")

print("=" * 60)