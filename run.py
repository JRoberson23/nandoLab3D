# run.py
import os
import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 INICIANDO NANDOLAB 3D")
    print("=" * 50)
    print("📁 Diretório: ", os.getcwd())
    print("🗄️ Banco: SQLite (instance/nandolab.db)")
    print("🌐 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )