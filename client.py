import argparse
import sys
import socket
import struct

###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data):
    data = data.encode()
    message_size = struct.pack("<I", len(data))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    sock.sendall(message_size)
    sock.sendall(data)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the servers ip")
    parser.add_argument("server_port", type=int, help="the servers port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
