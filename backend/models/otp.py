#
# FileName: otp.py
# Author: Shihab Hassan
# Created:   11/01/2024
# Modified: 03/29/2026
#

import secrets, hashlib
from datetime import datetime, timedelta, timezone

class OTP:
    def __init__(self):
        pass

    @staticmethod
    def generate(expires_in_seconds: int = 600):
        otp = f"{secrets.randbelow(1000000):06}"
        hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
        expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)
        return otp, hashed_otp, expires

    @staticmethod
    def hashed(hashed_otp: str):
        return hashlib.sha256(hashed_otp.encode()).hexdigest()
