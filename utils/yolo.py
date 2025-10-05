from camera import Camera
from ultralytics import YOLO

class DetectEGP():
    def __init__(self,
                 weights):
        self.weights = weights

        # setup
        self.yolo    = YOLO(self.weights)

    def detect(self,
               frame):
        return self.yolo(frame)

    def track(self, frame):
        pass

def test():
    MODEL = "../data/first_model.pt"
    VIDEO = "../data/"

    model = DetectEGP(model = MODEL)
    cam = Camera()

    while cam.isOpened():
        frame = cam.read()

        try:
            frame = cam.read()
            frame = model.detect(frame)
            cv2.imshow('test camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break

    cam.release()
        
if __name__ == "__main__":
    test()

