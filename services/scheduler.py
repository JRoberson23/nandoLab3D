import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from services.ping import ping_backend

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

async def scheduled_ping():
    """Função agendada para ping automático"""
    logger.info(f"🔄 Ping agendado às {datetime.now()}")
    await ping_backend()

def start_scheduler():
    """Inicia o agendador - APENAS seg-sex, 8h-20h"""
    scheduler.add_job(
        scheduled_ping,
        trigger=CronTrigger(
            day_of_week='mon-fri',  # ✅ Segunda a sexta
            hour='8-20',            # ✅ Das 8h às 20h
            minute='0,14,28,42'     # ✅ A cada 14 minutos
        ),
        id="ping_job"
    )
    scheduler.start()
    logger.info("⏰ Agendador iniciado (seg-sex, 8h-20h)")

def stop_scheduler():
    """Para o agendador"""
    scheduler.shutdown()
    logger.info("⏰ Agendador parado")