import argparse
import sys
import socket
import struct
from connection import Connection
from card import Card
from crypt_image import CryptImage

###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data):
    """sends data to the given server"""
    with Connection.connect(server_ip, server_port) as connection:
        if not isinstance(data, bytes):
            data = data.encode()
        connection.send_message(data)


# fmt: off
def send_card(server_ip, server_port, name:str, creator:str, riddle:str, solution:str, path:str):
    card = Card.create_from_path(name,creator,path,riddle,solution)
    card.image.encrypt("my key")
    message = card.serialize()
    send_data(server_ip,server_port,message)
# fmt: on

###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the servers ip")
    parser.add_argument("server_port", type=int, help="the servers port")
    parser.add_argument("name", type=str, help="the name of the Cardaz")
    parser.add_argument("creator", type=str, help="the creator of the Cardaz")
    parser.add_argument("riddle", type=str, help="the riddle")
    parser.add_argument("solution", type=str, help="the solution")
    parser.add_argument("path", type=str, help="the path to the photo")

    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_card(
            args.server_ip,
            args.server_port,
            args.name,
            args.creator,
            args.riddle,
            args.solution,
            args.path,
        )
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
