import json
import requests
from base64 import b64decode
from hashlib import md5
from Cryptodome.Cipher import AES

def generate_key(salt: bytes, *, output=48):
    r = requests.get("https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt")
    SECRET = bytes(r.text, "utf-8")
    key = md5(SECRET + salt).digest()
    current_key = key
    while len(current_key) < output:
        key = md5(key + SECRET + salt).digest()
        current_key += key
    return current_key[:output]


def decipher(encoded_url: str):
    s1 = b64decode(encoded_url.encode("utf-8"))
    key = generate_key(s1[8:16])
    decrypted = AES.new(key[:32], AES.MODE_CBC, key[32:]).decrypt(s1[16:])
    decrypted = decrypted[: -decrypted[-1]].decode("utf-8", "ignore").lstrip(" ")
    return json.loads(decrypted)

def main(url: str):
    decrypted_urls = decipher(url)
    return decrypted_urls
