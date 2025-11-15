# src/totp.py
import base64
import hashlib
import hmac
import struct
import time
from typing import Optional


def generate_totp(
    secret: str,
    interval: int = 30,
    digits: int = 6,
    for_time: Optional[int] = None,
) -> str:
    """
    Generate a TOTP code from a base32 secret (RFC 6238-style).
    This is a generic helper, not tied to any specific service.
    """
    if for_time is None:
        for_time = int(time.time())

    # Normalize secret
    cleaned = secret.replace(" ", "").upper()
    key = base64.b32decode(cleaned)

    counter = for_time // interval
    msg = struct.pack(">Q", counter)
    hmac_digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac_digest[19] & 0x0F
    code_int = (
        struct.unpack(">I", hmac_digest[offset : offset + 4])[0] & 0x7FFFFFFF
    ) % (10**digits)

    return f"{code_int:0{digits}d}"
