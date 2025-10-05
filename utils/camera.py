import cv2

class Camera():
    run = False

    def __init__(self,
                 dev_id = 0,
                 path   = None):

        _tmp = dev_id if path is None else path
        self.cap = cv2.VideoCapture(_tmp)

        self.run = True

    def read(self, ):
        if self.run and self.isOpened():
            ret, frame = self.cap.read()

            if ret:
                return frame
            else:
                # TODO: Error Handling
                self.run = False
        else:
            # TODO: Error Handling
            self.run = False

    def isOpened(self, ):
        if not self.run:
            # TODO: Error Handling
            pass
        return self.cap.isOpened()

    def release(self, ):
        if self.run:
            self.cap.release()
            self.run = False
        else:
            # TODO: Error Handling
            pass

def test(mp4 = None):
    cam = Camera(dev_id = cv2.CAP_V4L2, path = mp4)
    cam.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    height = cam.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width  = cam.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps    = cam.cap.get(cv2.CAP_PROP_FPS)
    count  = cam.cap.get(cv2.CAP_PROP_FRAME_COUNT)

    print("frame size  : {}x{}", height, width)
    print("frame FPS   : {}", fps)
    print("frame count : {}", count)

    while cam.isOpened():
        try:
            frame = cam.read()
            frame = cv2.resize(frame, None, fx=.5, fy=.5)
            cv2.imshow('test camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break
        
    cam.release()

if __name__ == "__main__":
    mp4_path = "../data/eggplant.mp4"
#    mp4_path = None
    test(mp4_path)

