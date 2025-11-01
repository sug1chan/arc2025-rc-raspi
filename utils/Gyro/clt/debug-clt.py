import numpy as np
import socket

ADDR = "127.0.0.1"
PORT = 6050

METER_TO_MILLIMETER = 1000

class GyroSensor():
    def __init__(self,
                 timeout = 1024, ):
        self.sfd  = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.ADDR = ADDR
        self.PORT = PORT
        self.addr = (self.ADDR, self.PORT)

        self.TIMEOUT = timeout

        self.GET  = "get"

    def get(self, ):
        """
        input:
        output:
            x : 水平軸
            y : 垂直軸
        speed : 現在の速度
        theta : 角度
        """
        self.sfd.sendto(self.GET.encode('utf-8'),
                        self.addr)

        result, srv_addr = self.sfd.recvfrom(self.TIMEOUT)

        return self.parse(result.decode())

    def get_xy(self, ):
        return self.get()[0]

    def get_theta(self, ):
        return self.get()[2]

    def parse(self, data):
        # x, y, speed, theta
        x, y, sleed, theta = map(lambda x: float(x) * METER_TO_MILLIMETER,
                                 data.split(" "))

        return np.array([x, y]), sleed, theta

def debug():
    pass

if __name__ == "__main__":
    debug()