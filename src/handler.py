# src/handler.py
import asyncio
import json
import os
from typing import Any, Dict

from .browser_runner import run_browser_job
from .totp import generate_totp


def _get_target_url(event: Dict[str, Any]) -> str:
    # Priority: event["target_url"] > env var > default
    if isinstance(event, dict) and "target_url" in event and event["target_url"]:
        return str(event["target_url"])

    env_url = os.environ.get("TARGET_URL")
    if env_url:
        return env_url

    # Default demo URL
    return "https://example.com"


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda entrypoint.
    Runs a single Playwright/Chromium session and returns metadata.
    """
    target_url = _get_target_url(event)

    # OPTIONAL: Generate a TOTP code if TOTP_SECRET is present (demo only)
    totp_secret = os.environ.get("TOTP_SECRET")
    totp_code = None
    if totp_secret:
        try:
            totp_code = generate_totp(totp_secret)
        except Exception as exc:
            # Don't fail the whole job if TOTP is misconfigured
            totp_code = f"error: {exc}"

    # Run the async Playwright job
    result = asyncio.run(run_browser_job(target_url))

    response: Dict[str, Any] = {
        "status": "ok",
        "target_url": target_url,
        "browser_result": result,
    }

    if totp_code is not None:
        response["totp_code_demo"] = totp_code

    # Lambda expects a JSON-serializable dict
    return response
