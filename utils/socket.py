class socket, time
from threading import Thread, Event

class Socket():
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port

