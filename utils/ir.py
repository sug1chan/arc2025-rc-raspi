from gpiozero import MotionSensor

class IRSensor:
    def __init__(self, pin):
        self.sensor = MotionSensor(pin,
                                   pull_up = True)

    def is_detected(self):
        return self.sensor.motion_detected  # True: 動きを検知中, False: 検知なし

    def close(self):
        self.sensor.close()

def debug():
    IRdebug1 = IRSensor(22)
    IRdebug2 = IRSensor(23)
    while True:
        print('IR1：', IRdebug1.is_detected())
        print('IR2：', IRdebug2.is_detected())

if __name__ == "__main__":
    debug()
