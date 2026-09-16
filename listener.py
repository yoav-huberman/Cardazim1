import socket

from connection import Connection


class Listener:
    def __init__(self, host, port, backlog=1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.sock = None

    def __repr__(self):
        return f"Listener(host={self.host}, port={self.port}, backlog={self.backlog})"

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self):
        self.sock.close()
        self.sock = None

    def accept(self):
        connection, addr = self.sock.accept()
        return Connection(connection)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
