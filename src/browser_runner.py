# src/browser_runner.py
import os
from typing import Optional, Dict, Any

from playwright.async_api import async_playwright


async def run_browser_job(
    target_url: str,
    screenshot: bool = True,
    screenshot_name: str = "page.png",
) -> Dict[str, Any]:
    """
    Run a single browser job:
    - open target_url
    - wait for network idle
    - return page title
    - optionally save screenshot to /tmp
    """
    screenshot_path: Optional[str] = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(target_url, wait_until="networkidle")

        title = await page.title()

        if screenshot:
            # In Lambda, /tmp is the writeable directory
            screenshot_path = os.path.join("/tmp", screenshot_name)
            await page.screenshot(path=screenshot_path, full_page=True)

        await browser.close()

    result: Dict[str, Any] = {
        "target_url": target_url,
        "title": title,
    }
    if screenshot_path:
        result["screenshot_path"] = screenshot_path

    return result
