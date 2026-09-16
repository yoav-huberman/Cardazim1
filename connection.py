import socket
import struct


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self):
        my_ip, my_port = self.connection.getsockname()
        target_ip, target_port = self.connection.getpeername()
        return f"<Connection from {my_ip}:{my_port} to {target_ip}:{target_port}>"

    def send_message(self, message: bytes):
        """sends a message to the target of the connection in the given protocol"""
        message_size = struct.pack("<I", len(message))
        self.sock.sendall(message_size)
        self.sock.sendall(message)

    def receive_message(self):
        """receives a message in the given protocol"""
        size_data = self.receive_this(4)  # get the meta data
        if len(size_data) != 4:
            return
        message_size = struct.unpack("<I", size_data)[0]
        data = self.receive_this(message_size)
        return data

    def receive_this(self, size: int):
        """receives a message of given size"""
        data = b""
        while len(data) < size:
            chunk = self.connection.recv(size - len(data))
            if not chunk:
                raise Exception("Connection severed")
            data += chunk
        return data

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return cls(sock)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
