import argparse
import sys
import socket
import struct
import threading
import time
from listener import Listener
from connection import Connection


def handle_connection(conn):
    """handles a specific connection"""
    with conn:
        conn.receive_message()


def run_server(ip, port):
    """runs the server and does threading"""
    with Listener(ip, port) as serv:
        while True:
            conn = serv.accept()
            threading.Thread(target=handle_connection, args=(conn,)).start()


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
