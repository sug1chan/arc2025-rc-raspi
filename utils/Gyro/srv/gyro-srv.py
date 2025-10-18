# タイマー割り込み用のプログラム
# データ取得と、データ保存は別のプログラムで分ける？
# コールバック関数内で取得回数でデータの送信を決定する？
import asyncore
import datetime
import select
import socket
import threading
import time

import mpu
import numpy as np
import pandas
import smbus  # import SMBus module of I2C


def MyException(Exception):
    pass

# Threading Socket
class MpuServer(threading.Thread):
    def __init__(self):
        super(MpuServer, self).__init__()
        
        self.host = "localhost"
        self.port = 6050
        # self.backlog = 10
        self.bufsize = 1024
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
                print(bus.gyro_data)
                # if message == "AAA":
                #     raise MyException(None)
            except MyException as e:
                print("Socket CLosing")
                self.sock.close()
                break


# class MpuServer(asyncore.dispatcher):
#     def __init__(self):
#         print("Socket Ceating!!")
#         asyncore.dispatcher.__init__(self)
#         # ポート番号6050にバインド
#         self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.bind(("localhost", 6050))
#         print("Socket Binding!!")

#     def handle_connect(self):
#         print("UDP Server Started...")

#     def handle_read(self):
#         data = self.recv(8192)
#         if data:
#             print(data)
#             raise asyncore.ExitNow("Server is quitting") 
    

#     def handle_write(self):
#         pass       

# def run():
#     instanse = MpuServer()
#     try:
#         asyncore.loop()
#     except asyncore.ExitNow:
#         print("Warning!!!")

if __name__ == "__main__":
    bus = mpu.Mpu()
    base_time = time.time()
    next_time = 0
    # Interval = 0.0.1 = 100Hz
    interval = 0.01

    # ソケット作成
    # run()

    # スレッドによるソケット作成
    MPUsrv = MpuServer()
    MPUsrv.setDaemon(True)
    MPUsrv.start()

 
    # スレッドによるタイマー割り込みでのデータ取得
    while True:
        tm = threading.Thread(target=bus.tm_callback)
        tm.start()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)
