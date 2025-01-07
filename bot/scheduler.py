import asyncio

from bot.utils import get_bot_runable
from .client import get_client
from .config import get_config
from .message_handler import process_channel
from .logger import logger
from .db import add_run_history


async def run_bot() -> None:
    """Run bot process"""
    config = get_config()

    if not config.is_active:
        logger.info("Bot is not active, skipping run")
        return

    client = await get_client()
    try:
        for channel in config.source_channels:
            await process_channel(client, channel)

        add_run_history(
            "success",
            f"Scheduled run completed. Processed channels: {', '.join(config.source_channels)}",  # noqa: E501
            type="process",
        )
        logger.info("Scheduled run completed successfully")

    except Exception as e:
        error_msg = f"Scheduled run failed: {str(e)}"
        add_run_history("error", error_msg)
        logger.error(error_msg)

    finally:
        await client.disconnect()


async def scheduler() -> None:
    """Main scheduler loop"""
    logger.info("Starting scheduler")

    while True:
        try:
            if await get_bot_runable():
                await run_bot()
            else:
                logger.info("Bot is not runable, skipping run")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        await asyncio.sleep(60)
