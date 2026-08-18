import asyncio
import httpx # pyright: ignore[reportMissingImports]
import logging
from datetime import datetime
from fastapi import APIRouter # pyright: ignore[reportMissingImports]

logger = logging.getLogger(__name__)
router = APIRouter()

# URL do backend
BASE_URL = "https://nandolab3d.onrender.com/helth"

async def ping_backend():
    """Ping automático para manter o servidor ativo"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/", timeout=10.0)
            logger.info(f"✅ Ping realizado com sucesso às {datetime.now()} - Status: {response.status_code}")
            return {"status": "success", "message": "Ping realizado com sucesso"}
    except Exception as e:
        logger.error(f"❌ Erro no ping às {datetime.now()}: {str(e)}")
        return {"status": "error", "message": str(e)}

# Rota para ping manual
@router.get("/ping")
async def ping():
    """Rota para testar o ping manualmente"""
    return await ping_backend()