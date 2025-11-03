import numpy as np
import cv2
from ultralytics import YOLO

DEFAULT_THRESHOLD = .9

class BB():
    def __init__(self,
                 bbox):
        self.bbox = bbox
        sx, sy, ex, ey = map(float, self.bbox)
        self._start = np.array([sx, sy])
        self._end   = np.array([ex, ey])

        self.center = (self._start + self._end) / 2
        self.area   = (self._end - self._start).prod()

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
        # yield from self.get_bboxes()
        self._bbox_iter = iter(self.get_bboxes())
        return self

    def __next__(self, ):
        return BB(self._bbox_iter.__next__())

class DetectEGP():
    def __init__(self,
                 weights,
                 threshold = DEFAULT_THRESHOLD,
                 logger    = None,
                 verbose   = False,):
        self.weights   = weights
        self.threshold = threshold
        self.verbose   = verbose

        # setup
        self.log       = logger.getChild(self.__class__.__name__) \
                         if not logger is None else None
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
    MODEL  = "../data/model.pt"
    # VIDEO  = "../data/win/eggplant.mp4"
    #VIDEO  = "../data/win/eggplant_under.mp4"
    #VIDEO  = "../data/win/front_camera.mp4"
    VIDEO = None
    OUTPUT = "../data/result_front_camera.mp4"

    model  = DetectEGP(weights = MODEL, threshold = .35)
    cam    = Camera(path = VIDEO)

    width   = cam.width
    height  = cam.height
    fps     = cam.fps

    out     = MP4_Saver(OUTPUT,
                        width,
                        height,
                        fps)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT, fourcc, fps, (width, height))

    print(f"front: {cam.size}")
    print(f"front: {cam.center}")
    while cam.isOpened():
        try:
            frame = cam.read()
            res = model.detect(frame, save = False)
            # res = model.track(frame)

            if res.isNone():
                break

            max_bbox = None
            for bbox in res:
                if (max_bbox is None) or \
                   (max_bbox.area < bbox.area):
                    max_bbox = bbox

            if not max_bbox is None:
                print(bbox.center, bbox.area)


            annotated_frame = res.plot()

            cv2.imshow('test camera', annotated_frame)
            out.write(annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(e)
            break

    cam.release()
        
if __name__ == "__main__":
    from camera import Camera, MP4_Saver
    test()

