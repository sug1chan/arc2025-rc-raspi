# タイマー割り込み用のプログラム
# データ取得と、データ保存は別のプログラムで分ける？
# コールバック関数内で取得回数でデータの送信を決定する？
import datetime
import select
import socket
import threading
import time
import signal

import mpu


# import numpy as np
# import pandas
# import smbus  # import SMBus module of I2C

# シグナル受信時に終了処理実施
def handler(signum, frame):
    raise SystemExit("SIGNAL REVICE! PROCESS SHUTTING!")

signal.signal(signal.SIGINT, handler)
interrupt_event = threading.Event()

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
        try:
            while not interrupt_event.is_set() :
                self.sock.settimeout(1.0)
                try:
                    message, clt_addr = self.sock.recvfrom(self.bufsize)
                    message = message.decode(encoding='utf-8')
                    # messageの内訳
                    #   get: 位置情報の受け取り
                    #   shut: プロセスの停止
                    #   reset: 位置情報の初期化
                    print(message)
                    if message == "get":
                        if bus.timer < mpu.STAY_TIME:
                            print("静止状態のデータ収集中です。")
                            # print(bus.x, bus.y, bus.x, bus.rad)
                            result = "{}, {}, {}, {}".format(bus.x, bus.y, bus.rad, bus.v)
                            # print(bus.x, bus.y, bus.x, bus.rad)
                            self.sock.sendto(result.encode(), clt_addr)
                        else:
                            print("位置情報送信")
                            result = "{}, {}, {}, {}".format(bus.x, bus.y, bus.rad, bus.v)
                            # print(bus.x, bus.y, bus.x, bus.rad)
                            self.sock.sendto(result.encode(), clt_addr)
                    elif message == "shut":
                        print("プロセスの停止")
                    elif message == "reset":
                        print("位置情報の初期化")
                    else:
                        print("予期せぬメッセージ")
                        pass
                except socket.timeout:
                    continue
        finally:
            print("!!Socket CLosing!!")
            self.sock.close()

# Ctrl + c (SIGINT)で終了できるようにしている。
# シグナルハンドラによって、終了処理を出せるように設定済み
# 対応シグナルを増やす場合は、以下の内容は上に記載してある。
#  signal.signal(signal.SIGINT, handler)
#  handler() を実行することで、SystemExit()例外を送信している。
# UDPソケットは現在、
#       ローカルホスト
#       6050ポート
# で作成している。
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
    try:
        while True:
            tm = threading.Thread(target=bus.tm_callback)
            tm.start()
            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)
    except SystemExit:
        # プロセス終了処理
        print("!!PROCESS SHUTTING!!")
        interrupt_event.set()
        tm.join()