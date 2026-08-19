import asyncio
import random
import os
from playwright.async_api import Page
from dotenv import load_dotenv

load_dotenv()

HUMAN_DELAY_MIN_MS = int(os.getenv("HUMAN_DELAY_MIN_MS", "60"))
HUMAN_DELAY_MAX_MS = int(os.getenv("HUMAN_DELAY_MAX_MS", "180"))

async def human_delay(min_ms: int = HUMAN_DELAY_MIN_MS, max_ms: int = HUMAN_DELAY_MAX_MS) -> None:
    await asyncio.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

async def human_type(page: Page, selector: str, text: str) -> None:
    loc = page.locator(selector).first
    await loc.click()
    await loc.fill("")  # Ensure the field is cleared to avoid double typing
    await human_delay(100, 300)
    for char in text:
        await loc.type(char, delay=random.uniform(50, 150))
    await human_delay(80, 200)

async def human_click(page: Page, selector: str) -> None:
    element = page.locator(selector).first
    box = await element.bounding_box()
    if box:
        x = box["x"] + box["width"]  * random.uniform(0.3, 0.7)
        y = box["y"] + box["height"] * random.uniform(0.3, 0.7)
        await page.mouse.move(x, y)
        await human_delay(50, 150)
        await page.mouse.click(x, y)
    else:
        await element.click()
    await human_delay(100, 250)
