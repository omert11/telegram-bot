import re
from typing import Final, Set
import aiohttp
from telethon.tl.types import Message
from .config import get_config
from .logger import logger

FEE_FLAGS: Final[Set[str]] = {"tl", "₺"}
GEMINI_URL: Final[str] = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
)


def add_fee_to_price(price_text: str) -> str:
    """Add fee to the price and return formatted string"""
    try:
        config = get_config()
        match = re.search(r"(\d+)", price_text)
        if match is None:
            return price_text
        price = int(match.group(1))
        total_price = price + config.add_fee
        return f"{total_price} TL"
    except (AttributeError, ValueError):
        return price_text


async def parse_price_with_gemini(text: str) -> str:
    """Parse price using Gemini AI"""
    prompt = f"""
    Extract only the TL/₺ price from this text and format it as 'X TL': {text}
    Example input: "250₺=7.30$=6.75€"
    Example output: "250 TL"
    Only return the formatted price, nothing else.
    """

    async with aiohttp.ClientSession() as session:
        try:
            config = get_config()
            async with session.post(
                f"{GEMINI_URL}?key={config.gemini_api_key}",
                json={"contents": [{"parts": [{"text": prompt}]}]},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if "candidates" in data:
                        price = data["candidates"][0]["content"]["parts"][0][
                            "text"
                        ].strip()
                        return add_fee_to_price(price)

        except Exception as e:
            logger.error(f"Error parsing price with Gemini: {e}")

    # Fallback: Basic regex parsing if Gemini fails
    match = re.search(r"(\d+)(?:TL|₺)", text)
    if match:
        price = f"{match.group(1)} TL"
        return add_fee_to_price(price)
    return text


def is_fee_message(text: str) -> bool:
    """Check if message contains price indicators"""
    text = text.lower()
    for flag in FEE_FLAGS:
        if flag in text:
            return True
    return False


async def parse_message_text(message: Message) -> str | None:
    """Parse message text and return formatted price with fee"""
    text = message.text
    if not text or not is_fee_message(text):
        return None
    return await parse_price_with_gemini(text.lower().replace("\n", "").strip())
