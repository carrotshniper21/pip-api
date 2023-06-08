import json
import httpx
from base64 import b64decode
from hashlib import md5
from Cryptodome.Cipher import AES

async def generate_key(salt: bytes, *, output=48) -> bytes:
    async with httpx.AsyncClient() as client:
        key = await client.get(
            "https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt",
            timeout=10
        )
        SECRET = bytes(key.text, "utf-8")
        key = md5(SECRET + salt).digest()
        current_key = key
        while len(current_key) < output:
            key = md5(key + SECRET + salt).digest()
            current_key += key
        return current_key[:output]

async def dechiper(encrypted_url: str):
    s1 = b64decode(encrypted_url.encode("utf-8"))
    key = await generate_key(s1[8:16])
    decrypted = AES.new(key[:32], AES.MODE_CBC, key[32:]).decrypt(s1[16:])
    decrypted = decrypted[: -decrypted[-1]].decode("utf-8", "ignore").lstrip(" ")
    return json.loads(decrypted)
