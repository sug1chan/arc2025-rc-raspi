# タイマー割り込み用のプログラム
# データ取得と、データ保存は別のプログラムで分ける？
# コールバック関数内で取得回数でデータの送信を決定する？
import datetime
import select
import socket
import threading
import time

import mpu


# import numpy as np
# import pandas
# import smbus  # import SMBus module of I2C


def MyException(Exception):
    pass

# Threading Socket
class MpuServer(threading.Thread):
    def __init__(self):
        super(MpuServer, self).__init__()
        
        self.host = mpu.MPU_HOST
        self.port = mpu.MPU_PORT
        # self.backlog = 10
        self.bufsize = mpu.MPU_BUF_SIZE
        print("!!! Socket Creating !!!")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("!!! Socket Binding !!!")
        self.sock.bind((self.host, self.port))
    
    def run(self):
        print("!!! Socket Waiting !!!")
        while True:
            try:
                message, clt_addr = self.sock.recvfrom(self.bufsize)
                message = message.decode(encoding='utf-8')
                print(message)
                print(bus.x, bus.y, bus.x, bus.rad)
                # if message == "AAA":
                #     raise MyException(None)
            except MyException as e:
                print("Socket CLosing")
                self.sock.close()
                break

if __name__ == "__main__":
    bus = mpu.Mpu()
    # timer config
    # Interval = 0.01 = 100Hz
    base_time = time.time()
    next_time = 0
    interval = mpu.INTERVAL
    # スレッドによるソケット作成
    MPUsrv = MpuServer()
    MPUsrv.start()

 
    # スレッドによるタイマー割り込みでのデータ取得
    while True:
        tm = threading.Thread(target=bus.tm_callback)
        tm.start()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
