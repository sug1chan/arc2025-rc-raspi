import numpy as np
import cv2
import logging
from logging import getLogger

class Camera():
    run = False

    def __init__(self,
                 dev_id = 0,
                 path   = None,
                 logger = None, ):

        self.logger = logger.getChild(self.__class__.__name__) \
                      if not logger is None else None

        _tmp = dev_id if path is None else path
        self.cap = cv2.VideoCapture(_tmp)

        self.run = True

        self.width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps    = float(self.cap.get(cv2.CAP_PROP_FPS))

        self.wcenter = self.width / 2
        self.hcenter = self.height / 2
        self.center  = np.array([self.wcenter, self.hcenter])
        self.size    = np.array([self.width, self.height])

        self.log(logging.INFO, "初期化に成功しました。")

    def read(self, ):
        if self.run and self.isOpened():
            ret, frame = self.cap.read()

            if ret:
                return frame
            else:
                # TODO: Error Handling
                self.run = None
        else:
            # TODO: Error Handling
            self.run = None

        return None

    def isOpened(self, ):
        if not self.run:
            # TODO: Error Handling
            return False
        return self.cap.isOpened()

    def release(self, ):
        if self.run:
            self.cap.release()
            self.run = False
        else:
            # TODO: Error Handling
            pass

    def log(self,
            level,
            message):
        if self.logger is None:
            return
        return self.logger.log(level, message)

class MP4_Saver():
    def __init__(self,
                 save_path,
                 width,
                 height,
                 fps,
                 logger = None, ):
        self.save_path = save_path
        self.width     = width
        self.height    = height
        self.fps       = fps

        self.logger = logger.getChild(self.__class__.__name__) \
                      if not logger is None else None

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(self.save_path,
                                      self.fourcc,
                                      self.fps, 
                                      (self.width,
                                       self.height))

        self.log(logging.INFO, "初期化に成功しました。")

    def write(self,
              img):
       return self.writer.write(img)
    
    def log(self,
            level,
            message):
        if self.logger is None:
            return
        return self.logger.log(level, message)

def test(mp4 = None):
    logger = getLogger("test")
    logger.setLevel(logging.DEBUG)
    cam = Camera(dev_id = cv2.CAP_V4L2,
                 path = mp4,
                 logger = logger)
    cam.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    width  = cam.width
    height = cam.height
    fps    = cam.fps
    count  = cam.cap.get(cv2.CAP_PROP_FRAME_COUNT)

    mp4 = MP4_Saver("../data/win/test_camera.mp4",
                    width,
                    height,
                    fps,
                    logger = logger, )

    print("frame size  : {}x{}", height, width)
    print("frame FPS   : {}", fps)
    print("frame count : {}", count)

    while cam.isOpened():
        try:
            frame = cam.read()
            frame = cv2.resize(frame, None, fx=.5, fy=.5)
            # cv2.imshow('test camera', frame)
            mp4.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
            break
        
    cam.release()

if __name__ == "__main__":
    #mp4_path = "../data/win/data/eggplant.mp4"
    mp4_path = "../data/win/eggplant.mp4"
    test(mp4_path)

