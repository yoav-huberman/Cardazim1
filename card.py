from __future__ import annotations
from os import PathLike
import struct
from crypt_image import CryptImage


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
        st = f"Card {self.name} by {self.creator}\nriddle: {self.riddle}\n solution: "
        st += f"{self.sol}" if self.sol else f"unsolved"
        return st

    @classmethod
    def create_from_path(
        cls, name: str, creator: str, path: str | PathLike, riddle: str, solution: str) -> Card:
        """return: a Card object with the image from the path and the given other info"""
        cryptIm = CryptImage(path)
        return cls(name, creator, cryptIm, riddle, solution)

    def serialize(self) -> bytes:
        name_bytes = self.name.encode()
        name_size = struct.pack("!I", len(name_bytes))
        name_part = name_size + name_bytes
        creator_bytes = self.creator.encode()
        creator_size = struct.pack("!I", len(creator_bytes))
        creator_part = creator_size + creator_bytes
        height = struct.pack("!I", self.image.hight)
        width = struct.pack("!I", self.image.width)
        content = b""
        key_hash = self.image.key_hash
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
        name_size: int = struct.unpack("!I", name_size_enc)
        name_enc: bytes = data[curr_index, curr_index + name_size]
        curr_index += name_size
        name = name_enc.decode()
        creator_size_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        creator_size: int = struct.unpack("!I", creator_size_enc)
        creator_enc: bytes = data[curr_index, curr_index + creator_size]
        curr_index += creator_size
        creator = creator_enc.decode()
        # image part
        image = CryptImage()
        riddle_size_enc: bytes = data[curr_index : curr_index + 4]
        curr_index += 4
        riddle_size: int = struct.unpack("!I", riddle_size_enc)
        riddle_enc: bytes = data[curr_index, curr_index + riddle_size]
        curr_index += riddle_size
        riddle = riddle_enc.decode()
        return Card(name,creator,image,riddle)
