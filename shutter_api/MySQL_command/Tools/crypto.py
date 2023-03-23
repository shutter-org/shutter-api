from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from base64 import b64decode, b64encode

def encrypt(raw:str,key:bytes) -> str:
        raw = pad(raw.encode(),16)
        cipher = AES.new(key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw)).decode("utf-8")

def decrypt(enc:str, key:bytes) -> str:
        enc = b64decode(enc.encode("utf-8"))
        cipher = AES.new(key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16).decode("utf-8")
