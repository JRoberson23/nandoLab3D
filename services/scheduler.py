import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler # pyright: ignore[reportMissingImports]
from apscheduler.triggers.interval import IntervalTrigger # pyright: ignore[reportMissingImports]
from services.ping import ping_backend

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def scheduled_ping():
    """Função agendada para ping automático"""
    logger.info(f"🔄 Ping automático iniciado às {datetime.now()}")
    await ping_backend()

def start_scheduler():
    """Inicia o agendador de ping"""
    # Ping a cada 14 minutos (segunda a sexta, das 8h às 20h)
    scheduler.add_job(
        scheduled_ping,
        trigger=IntervalTrigger(minutes=14),
        id="ping_job",
        next_run_time=datetime.now()  # Executa imediatamente na primeira vez
    )
    scheduler.start()
    logger.info("⏰ Agendador de ping iniciado!")

def stop_scheduler():
    """Para o agendador de ping"""
    scheduler.shutdown()
    logger.info("⏰ Agendador de ping parado!")