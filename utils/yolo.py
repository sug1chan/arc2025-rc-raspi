from camera import Camera
from ultralytics import YOLO

class DetectEGP():
    def __init__(self,
                 weights):
        self.weights = weights

        # setup
        self.yolo    = YOLO(self.weights)

    def detect(self,
               frame,
               save = False,):
        return self.yolo(frame, save=save)

    def track(self, frame):
        pass

def test():
    MODEL  = "../data/first_model.pt"
    VIDEO  = "../data/test.mp4"
    OUTPUT = "../data/result.mp4"

    model = DetectEGP(weights = MODEL)
    cam = Camera(path = VIDEO)

    while cam.isOpened():
        frame = cam.read()

        try:
            frame = cam.read()
            res   = model.detect(frame, save = False)
            annotated_frame = res[0].plot()

            cv2.imshow('test camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break

    cam.release()
        
if __name__ == "__main__":
    test()

