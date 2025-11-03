import numpy as np
import socket
import math
import time

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
        theta : 角度
        speed : 現在の速度
        """
        self.sfd.sendto(self.GET.encode('utf-8'),
                        self.addr)

        result, srv_addr = self.sfd.recvfrom(self.TIMEOUT)

        return self.parse(result.decode())

    def get_xy(self, ):
        return self.get()[0]

    def get_theta(self, ):
        return self.get()[1]

    def parse(self, data):
        # x, y, speed, theta
        x, y, theta, speed = map(lambda x: float(x),
                                 data.split(","))
        print(x,y,math.degrees(theta), speed)
        return np.array([x * METER_TO_MILLIMETER, y * METER_TO_MILLIMETER]), theta, speed

def debug():
    pass

if __name__ == "__main__":
    gyro = GyroSensor()
    while True:
        theta = gyro.get_theta()
        print(math.degrees(theta))
        time.sleep(1)
    debug()