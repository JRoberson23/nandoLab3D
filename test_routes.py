# test_routes.py (na raiz do projeto)
from app import app

print("=" * 60)
print("🔗 ROTAS REGISTRADAS NO NANDOLAB 3D")
print("=" * 60)

# Listar todas as rotas
routes_by_path = {}

for route in app.routes:
    if hasattr(route, 'path'):
        path = route.path
        methods = ', '.join(route.methods) if hasattr(route, 'methods') else 'ALL'
        
        if path not in routes_by_path:
            routes_by_path[path] = []
        routes_by_path[path].append(methods)

# Ordenar e mostrar
for path in sorted(routes_by_path.keys()):
    methods = routes_by_path[path]
    print(f"\n{path}")
    for method in methods:
        print(f"  → {method}")

print("\n" + "=" * 60)
print(f"Total de rotas: {len(routes_by_path)}")

# Filtrar rotas do admin
print("\n📋 ROTAS DO ADMIN (deve começar com /admin):")
print("-" * 40)
admin_routes = {k: v for k, v in routes_by_path.items() if '/admin' in k}
for path in sorted(admin_routes.keys()):
    methods = admin_routes[path]
    print(f"\n{path}")
    for method in methods:
        print(f"  → {method}")

if not admin_routes:
    print("❌ NENHUMA rota do admin encontrada!")
else:
    print(f"\n✅ Total de rotas do admin: {len(admin_routes)}")
print("=" * 60)