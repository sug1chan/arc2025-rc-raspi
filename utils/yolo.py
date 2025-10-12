import cv2
from camera import Camera
from ultralytics import YOLO

DEFAULT_THRESHOLD = .9

class DetectEGP():
    def __init__(self,
                 weights,
                 threshold = DEFAULT_THRESHOLD,
                 verbose   = False):
        self.weights   = weights
        self.threshold = threshold
        self.verbose   = verbose

        # setup
        self.yolo      = YOLO(self.weights)

    def detect(self,
               frame,
               save = False,):
        return self.yolo(frame,
                         conf    = self.threshold,
                         verbose = self.verbose,
                         save    = save)

    def track(self, frame):
        return self.yolo.track(frame,
                               conf    = self.threshold, 
                               verbose = self.verbose, )

def test():
    MODEL  = "../data/win/data/first_model.pt"
    VIDEO  = "../data/win/data/eggplant.mp4"
    OUTPUT = "../data/win/data/result.mp4"

    model  = DetectEGP(weights = MODEL, threshold = .8)
    cam    = Camera(path = VIDEO)

    width   = int(cam.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height  = int(cam.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps     = float(cam.cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT, fourcc, fps, (width, height))

    while cam.isOpened():
        try:
            frame = cam.read()
            #res = model.detect(frame, save = False)
            res = model.track(frame)

            if res is None:
                break

            annotated_frame = res[0].plot()

            # cv2.imshow('test camera', annotated_frame)
            out.write(annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(e)
            break

    cam.release()
        
if __name__ == "__main__":
    test()

