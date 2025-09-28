class Camera():
    run = False

    def __init__(self,
                 dev_id = 0, ):
        self.cap = cv2.VideoCapture(dev_id)
        self.run = True

    def read(self):
        if self.run and self.isOpened():
            return self.cap.read()
        else:
            # TODO: Error Handling
            self.run = False

    def isOpened(self, ):
        if !self.run:
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

