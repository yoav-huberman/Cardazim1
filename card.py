from __future__ import annotations
from os import PathLike
import struct
from crypt_image import CryptImage
from PIL import Image


# fmt: off
class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, sol : str | None = None):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.sol = sol
#fmt: on

    def __repr__(self):
        return f"<Card name={self.name}, creator = {self.creator}>"

    def __str__(self):
        st = f"Card {self.name} by {self.creator}\nriddle: {self.riddle}\nsolution: "
        st += f"{self.sol}" if self.sol else f"unsolved"
        return st

    @classmethod
    def create_from_path(
        cls, name: str, creator: str, path: str | PathLike, riddle: str, solution: str) -> Card:
        """return: a Card object with the image from the path and the given other info"""
        cryptIm = CryptImage.create_from_path(path)
        return cls(name, creator, cryptIm, riddle, solution)

    def serialize(self) -> bytes:
        name_bytes = self.name.encode()
        name_size = struct.pack("!I", len(name_bytes))
        name_part = name_size + name_bytes
        creator_bytes = self.creator.encode()
        creator_size = struct.pack("!I", len(creator_bytes))
        creator_part = creator_size + creator_bytes
        height = struct.pack("!I", self.image.height)
        width = struct.pack("!I", self.image.width)
        content = self.image.to_bytes()
        key_hash = self.image.key_hash if self.image.key_hash else b'\x00' * 32
        image_part = height + width + content + key_hash
        riddle_bytes = self.riddle.encode()
        riddle_size = struct.pack("!I", len(riddle_bytes))
        riddle_part = riddle_size + riddle_bytes
        return name_part + creator_part + image_part + riddle_part

    @classmethod
    def deserialize(cls, data: bytes):
        curr_index = 0
        name_size_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        name_size: int = struct.unpack("!I", name_size_enc)[0]
        name_enc: bytes = data[curr_index: curr_index + name_size]
        curr_index += name_size
        name = name_enc.decode()

        creator_size_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        creator_size: int = struct.unpack("!I", creator_size_enc)[0]
        creator_enc: bytes = data[curr_index: curr_index + creator_size]
        curr_index += creator_size
        creator = creator_enc.decode()

        height_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        height: int = struct.unpack("!I",height_enc)[0]

        width_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        width: int = struct.unpack("!I",width_enc)[0]

        image_size: int = 3*width*height
        image_enc: bytes = data[curr_index: curr_index + image_size]
        curr_index += image_size
        size = (width, height)
        image = Image.frombytes("RGB", size, image_enc)

        key_hash = data[curr_index : curr_index + 32]
        curr_index += 32 

        if key_hash!=b'\x00' * 32:
            image = CryptImage(image,key_hash)
        else: image =  CryptImage(image) #if hash_key is only zeros this means my picture isn't hashed

        riddle_size_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        riddle_size: int = struct.unpack("!I", riddle_size_enc)[0]
        riddle_enc: bytes = data[curr_index: curr_index + riddle_size]
        curr_index += riddle_size
        riddle = riddle_enc.decode()
        
        return Card(name,creator,image,riddle)
