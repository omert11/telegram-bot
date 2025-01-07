from telethon import TelegramClient
from telethon.tl.types import Message
import asyncio
from typing import List
from .config import get_config
from .price_parser import parse_message_text, is_fee_message
from .logger import logger
from .db import get_last_message_id, update_last_message_id


async def send_media_group(client: TelegramClient, messages: List[Message]) -> None:
    """Send media group with price message to target channel"""
    if not messages:
        return

    message = messages.pop()
    text = await parse_message_text(message)
    if not text:
        return

    try:
        config = get_config()
        await client.send_message(
            config.target_channel, message=text, file=[msg.media for msg in messages]
        )
        logger.info(f"Sent message group to {config.target_channel}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

    await asyncio.sleep(5)


async def process_channel(client: TelegramClient, channel: str) -> None:
    """Process messages from a single channel"""
    try:
        logger.info(f"Processing channel: {channel}")
        last_message_id = get_last_message_id(channel)

        kwargs = {
            "limit": 20,
        }

        if last_message_id != -1:
            kwargs["min_id"] = last_message_id

        messages: List[Message] = await client.get_messages(channel, **kwargs)

        if not messages:
            logger.info(f"No new messages in channel: {channel}")
            return

        first_media_seen = False
        media_group_messages: List[Message] = []
        newest_message_id = last_message_id

        for msg in messages:
            # Track the newest message ID
            if msg.id > newest_message_id:
                newest_message_id = msg.id

            if not first_media_seen and not msg.media:
                continue

            first_media_seen = True

            if msg.text and is_fee_message(msg.text):
                media_group_messages.append(msg)
                await send_media_group(client, media_group_messages)
                media_group_messages.clear()
            elif msg.media:
                media_group_messages.append(msg)

        # Update the last processed message ID
        if newest_message_id > last_message_id:
            update_last_message_id(channel, newest_message_id)

        logger.info(f"Finished processing channel: {channel}")

    except Exception as e:
        logger.error(f"Error processing channel {channel}: {e}")
