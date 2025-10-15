import cv2
from camera import Camera
from ultralytics import YOLO

DEFAULT_THRESHOLD = .9

class BBoxes():
    def __init__(self,
                 result, ):

        self.result = result[0] if not result is None else None

        if not self.result is None:
            self.img    = self.result.orig_img
            self.label  = self.result.names
            self.shape  = self.result.orig_shape
    
    def get_bboxes(self, ):
        return self.result.boxes.xyxy

    def plot(self,
             *args,
             **kwargs, ):
        return self.result.plot(*args,
                                **kwargs)

    def isNone(self, ):
        return self.result is None

    def __iter__(self, ):
        yield from self.get_bboxes()

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
               save = False, ):
        return BBoxes(self.yolo(frame,
                                conf    = self.threshold,
                                verbose = self.verbose,
                                save    = save))

    def track(self, frame):
        return BBoxes(self.yolo.track(frame,
                                      conf    = self.threshold, 
                                      verbose = self.verbose, ))

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
            res = model.detect(frame, save = False)
            # res = model.track(frame)

            if res.isNone():
                break

            annotated_frame = res.plot()

            # cv2.imshow('test camera', annotated_frame)
            out.write(annotated_frame)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        except Exception as e:
            print(e)
            break

    cam.release()
        
if __name__ == "__main__":
    test()

