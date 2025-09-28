import socket, time
from threading import Thread, Event

SOCK_TIMEOUT = 3.

class Socket():
    sfd = None

    def __init__(self,
                 addr: str,
                 port: int,
                 sock_timeout: int = SOCK_TIMEOUT):
        self.addr         = addr
        self.port         = port
        self.sock_timeout = sock_timeout

    def connect(self, ):
        self.sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sfd.settimeout(self.sock_timeout)
        self.sfd.connect()
        pass

    def send(self,
             msg):  # TODO: 型が何なのか調べる。
        if self.sfd is None:
            # TODO: Error Handling
            pass
        pass

    def close(self, ):
        if self.sfd is None:
            # TODO: Error Handling
            pass
        pass

