import argparse
import sys
import socket
import struct
import threading
import time


def handle(conn):
    try:
        size_data = conn.recv(4)  # get the meta data
        if len(size_data) != 4:
            return
        message_size = struct.unpack("<I", size_data)[0]
        data = b""
        while len(data) < message_size:
            chunk = conn.recv(message_size - len(data))
            if not chunk:
                return
            data += chunk
        message = data.decode()
        print(message)
    finally:
        conn.close()


def run_server(ip, port):
    """runs the server and prints the data it receive's"""
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    serv.listen()
    while True:
        conn, adrr = serv.accept()
        threading.Thread(target=handle, args=(conn,)).start()


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the servers ip")
    parser.add_argument("server_port", type=int, help="the servers port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
