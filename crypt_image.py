from __future__ import annotations
from PIL.Image import Image
from PIL import Image
from os import PathLike
from Crypto.Cipher import AES
import hashlib
import io


class CryptImage:
    def __init__(self, image: Image, key_hash: bytes | None = None):
        self.image = image
        self.key_hash = key_hash
        self.width = image.width
        self.height = image.height
        self.size = image.size  # redundant but easier to work with

    def show(self):
        self.image.save("debug_image.png")

    @classmethod
    def create_from_path(cls, path: str | PathLike) -> CryptImage:
        image = Image.open(path)
        image = image.convert("RGB")
        return cls(image)

    def encrypt(self, key: str):
        """encrypts the image attribute using the key"""
        hash_obj = hashlib.sha256(key.encode())
        enc_key = hash_obj.digest()
        cipher = AES.new(enc_key, AES.MODE_EAX, nonce=b"arazim")
        hash_obj = hashlib.sha256(enc_key)  # not the same hash obj
        self.key_hash = hash_obj.digest()
        self.image = self.image.convert("RGB")
        image_bytes = self.image.tobytes()
        encrypted = cipher.encrypt(image_bytes)
        self.image = Image.frombytes("RGB", self.size, encrypted)

    def decrypt(self, key: str) -> bool:
        """decrypts the image if the key is correct"""
        hash_obj = hashlib.sha256(key.encode())
        enc_key = hash_obj.digest()
        hash_obj = hashlib.sha256(enc_key)
        is_key_correct = hash_obj.digest() == self.key_hash
        if is_key_correct:
            self.image = self.image.convert("RGB")
            image_bytes = self.image.tobytes()
            cipher = AES.new(enc_key, AES.MODE_EAX, nonce=b"arazim")
            decrypted = cipher.decrypt(image_bytes)
            self.image = Image.frombytes("RGB", self.size, decrypted)
            self.key_hash = None
            return True

        else:
            return False
