# import asyncore
import socket
import math
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ADDR = ("localhost", 6050)

# 送信データ:3種類を予定？
#   get:文字列:位置情報の取得要請
# 帰り値
#   文字列:"x, y, v, ras"
#   x: 位置情報x(m)
#   y: 位置情報y(m)
#   rad: 角度(radian)
#   v: 速度(m/s)
# 返り値は文字列の為、encode()後、
# split()などで分割することを想定している。
data = "get"

try:
    while True:
        sock.sendto(data.encode('utf-8'), ADDR)
            # if not data:
            #     break
        result, srv_addr = sock.recvfrom(1024)
        x, y, rad, v = result.decode().split(", ")
        # print("位置x:{}, 位置y:{}\n角度deg:{}, 速度v:{}".format(x,y,math.degrees(float(rad)), v))
        print("位置x:{}, 位置y:{}\n角度rad:{}, 速度v:{}".format(x,y,rad, v))
        time.sleep(1)
except KeyboardInterrupt:
    sock.close()
