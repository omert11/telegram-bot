# cspell:disable

from .config import get_config, BotConfig
from .db import get_db_now, get_last_run_by_type
from .client import is_bot_logged
from datetime import datetime, timedelta


def get_status_message(config: BotConfig | None = None) -> str:
    if not config:
        config = get_config(True)

    last_run_time = get_last_run_time_message()
    next_run_str = get_next_run_time_message(config)
    channels = ", ".join(config.source_channels)

    return (
        f"Bot {'aktif' if config.is_active else 'pasif'} durumda.\n"
        f"Her {config.interval_minutes} dakikada bir çalışıyor.\n"
        f"Son çalışma: {last_run_time}\n"
        f"Sonraki çalışma: {next_run_str}\n"
        f"İzlenen kanallar: {channels}\n"
        f"Komisyon: {config.add_fee} TL"
    )


def get_last_run_time_message() -> str:
    last_run = get_last_run_by_type("process")
    if last_run:
        last_run_datetime = datetime.strptime(
            last_run["created_at"], "%Y-%m-%d %H:%M:%S"
        )
        return last_run_datetime.strftime("%d.%m.%Y %H:%M:%S")
    return "Henüz çalışmadı"


def get_next_run_time_message(config: BotConfig) -> str:
    last_run = get_last_run_by_type("process")
    if last_run:
        last_run_datetime = datetime.strptime(
            last_run["created_at"], "%Y-%m-%d %H:%M:%S"
        )
        return (
            last_run_datetime + timedelta(minutes=config.interval_minutes)
        ).strftime("%d.%m.%Y %H:%M:%S")

    if config.is_active:
        return "Yakında çalışacak"
    return "Bot aktif değil"


async def get_bot_runable() -> bool:
    """Check if bot should run now"""
    config = get_config(force=True)

    if not config.is_active:
        return False

    if not await is_bot_logged():
        return False

    last_run = get_last_run_by_type("process")
    if not last_run:
        return True

    now = get_db_now()
    last_run_time = datetime.strptime(last_run["created_at"], "%Y-%m-%d %H:%M:%S")

    return now > (last_run_time + timedelta(minutes=config.interval_minutes))
