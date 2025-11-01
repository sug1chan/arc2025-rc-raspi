from gpiozero import MotionSensor

class IRSensor:
    def __init__(self, pin):
        self.sensor = MotionSensor(pin)

    def is_detected(self):
        return self.sensor.motion_detected  # True: 動きを検知中, False: 検知なし

    def close(self):
        self.sensor.close()
