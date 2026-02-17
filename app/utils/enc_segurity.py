from abc import ABC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os

from dotenv import load_dotenv

# from models.schemas import M_CRUD

load_dotenv()
class DataEncryptionService:
    KEY_HEX = os.getenv("KEY_HEX")
    AES = AESGCM(bytes.fromhex(KEY_HEX))

    @staticmethod
    def encrypt(data: str) -> str:
        if not data:
            return data
        nonce = os.urandom(12)
        ct = DataEncryptionService.AES.encrypt(nonce, data.encode(), None)
        return base64.b64encode(nonce + ct).decode("utf-8")

    @staticmethod
    def decrypt(token: str) -> str:
        raw = base64.b64decode(token.encode("utf-8"))
        nonce, ct = raw[:12], raw[12:]
        pt = DataEncryptionService.AES.decrypt(nonce, ct, None)
        return pt.decode("utf-8")
