# import asyncore
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ADDR = ("localhost", 6050)

# while True:
data = "get"
sock.sendto(data.encode('utf-8'), ADDR)
    # if not data:
    #     break
result, srv_addr = sock.recvfrom(1024)
print(result.decode())

sock.close()



# class MpuClient(asyncore.dispatcher):
#     def __init__(self, host):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket()
#         self.connect((host, 6050))
#         self.buffer = bytes("LoacateionGet", 'ascii')

#     def handle_connect(self):
#         pass

#     def handle_close(self):
#         self.close()
    
#     def handle_read(self):
#         print(self.recv(8192))

#     def writable(self):
#         return (len(self.buffer) > 0)
    
#     def handle_write(self):
#         sent = self.send(self.buffer)
#         self.buffer = self.buffer[sent:]

# if __name__ == "__main__":
#     client = MpuClient("localhost")
#     asyncore.loop()