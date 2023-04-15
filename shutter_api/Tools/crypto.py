from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt(raw: str, key: bytes) -> str:
    """
        Function that encrypt a string with a key
        Encrypt algorith AES_ECB

        Args:
            raw (str): string to encrypt
            key (bytes): encryption key in bytes

        Returns:
            str: encrypted message
        """
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return b64encode(cipher.encrypt(raw)).decode("utf-8")


def decrypt(enc: str, key: bytes) -> str:
    """
        Function that decrypt a encrypted message with a key
        Encryption algorith AES_ECB

        Args:
            enc (str): encrypted message
            key (bytes): encryption key in bytes

        Returns:
            str: raw message
        """
    enc = b64decode(enc.encode("utf-8"))
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16).decode("utf-8")
