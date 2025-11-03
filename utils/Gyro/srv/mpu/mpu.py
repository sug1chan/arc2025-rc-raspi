from . import config
from . import locater
import numpy as np
import smbus
import math

class Mpu:

    def __init__(self):
        # some MPU6050 Registers and their Address
        self.PWR_MGMT_1 = 0x6B
        self.SMPLRT_DIV = 0x19
        self.CONFIG = 0x1A
        self.GYRO_CONFIG = 0x1B
        self.INT_ENABLE = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H = 0x43
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47

        self.bus = smbus.SMBus(1)
        self.Device_Address = 0x68

        # write to sample rate register
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)

        # Write to power management register
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)

        # Write to Configuration register
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)

        # Write to Gyro configuration register
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)

        # Write to interrupt enable register
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)

        self.ACCEL_RATE = 16384.0
        self.GYRO_RATE = 131.0
        self.interval = config.INTERVAL
        self.timer = 0.0
        # self.gyro_data = []
        self.x = config.LOCATE_X
        self.y = config.LOCATE_Y
        self.rad = config.LOCATE_RADIAN
        self.v = config.LOCATE_VEROCITY
        # 移動中かの判断
        self.max_acc = config.MAX_ACC
        self.min_acc = config.MIN_ACC
        self.max_rad = config.MAX_RADIAN
        self.min_rad = config.MIN_RADIAN
        self.stay_flag = config.STAY_FLAG
        # 重力加速度の補正
        self.grabity_acc = config.GRABITY_ACC
        self.grabity_gyro = config.GRABITY_GYRO

    # 生データ取得
    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr+1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if (value > 32768):
            value = value - 65536
        return value

    # スレッドによるデータ取得
    def tm_callback(self):
        # Read Accelerometer raw value
        acc_x = self.read_raw_data(self.ACCEL_XOUT_H) / self.ACCEL_RATE
        acc_y = self.read_raw_data(self.ACCEL_YOUT_H) / self.ACCEL_RATE
        acc_z = self.read_raw_data(self.ACCEL_ZOUT_H) / self.ACCEL_RATE
        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        # Accerarator : +/- 2g  -> 65536 * 4

        # Read Gyroscope raw value
        gyro_x = self.read_raw_data(self.GYRO_XOUT_H) / self.GYRO_RATE
        gyro_y = self.read_raw_data(self.GYRO_YOUT_H) / self.GYRO_RATE
        gyro_z = self.read_raw_data(self.GYRO_ZOUT_H) / self.GYRO_RATE
        # Gyro : +/- 250 -> 65536 * 500

        # self.gyro_data.append([acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])
        # print ("Gx=%.2f" %gyro_x, u'\u00b0'+ "/s", "\tGy=%.2f" %gyro_y, u'\u00b0'+ "/s", "\tGz=%.2f" %gyro_z, u'\u00b0'+ "/s", "\tAx=%.2f g" %acc_x, "\tAy=%.2f g" %acc_y, "\tAz=%.2f g" %acc_z)
        # print ("\tAx=%.2f g" %acc_x, "\tGz=%.2f" %gyro_z, u'\u00b0'+ "/s")

        # 重力加速度の補正
        acc_x, self.grabity_gyro = locater.grabity_calibration(acc_x, acc_z, self.grabity_acc, self.grabity_gyro)
        # 停止状態の確認および停止判定の値を保持する。
        self.stay_flag, self.max_acc, self.min_acc, self.max_rad, self.min_rad = locater.is_stay(self.timer, acc_x, gyro_z, self.max_acc, self.min_acc, self.max_rad, self.min_rad)
        # 動作中なら、自己位置推定関数にデータを渡す。
        # 引数：
        #       現在の位置x(m): 
        #       現在の位置y(m): 
        #       現在の角度(rad): radian 
        #       現在の速度v(m/s):
        #       加速度acccerate(g*m/s^2): Ax
        #       角速度phi(deg): Gz
        # 返り値:
        #       最新の位置x(m): x
        #       最新の位置y(m): y
        #       最新の角度rad(rad)): rad
        #       最新の速度verocity(m/s): v
        if self.stay_flag == 0:  
            # if(0.01 >= math.fabs(acc_z - self.grabity_acc)):
            #acc_x, self.grabity_gyro = locater.grabity_calibration(acc_x, gyro_y, self.grabity_acc, self.grabity_gyro) 
            #print ("\tAx=%.2f g" %acc_x, "\tGy=%.2f" %self.grabity_gyro, u'\u00b0'+ "/s", "\tAz=%.2f g" %acc_z)
            self.x, self.y, self.rad, self.v = locater.localization_calculation(self.x, self.y, self.rad, self.v, acc_x, gyro_z)
        elif self.stay_flag == 1:
            self.v = 0.0
        self.timer += self.interval
