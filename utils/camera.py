import cv2

class Camera():
    run = False

    def __init__(self,
                 dev_id = 0, ):
        self.cap = cv2.VideoCapture(dev_id)
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

def test():
    cam = Camera()

    while cam.isOpened():
        try:
            frame = cam.read()
            cv2.imshow('test camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break
        
    cam.release()

if __name__ == "__main__":
    test()

