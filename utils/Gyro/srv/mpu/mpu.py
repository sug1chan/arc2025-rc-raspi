import smbus


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

        self.ACCEL_RATE = 16384.0
        self.GYRO_RATE = 131.0

        self.bus = smbus.SMBus(1)
        self.Device_Address = 0x68

        self.gyro_data = []

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

        self.counter = 0

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
        # print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
        # self.counter += self.counter
        # if self.counter == 1000:
        #     # データ転送処理？
        #     data_sender(self.gyro_data)

        # 計算処理
        self.gyro_data = [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]        


# def data_sender(gyro_data):
#     aaa = 1
#     print(len(gyro_data))



