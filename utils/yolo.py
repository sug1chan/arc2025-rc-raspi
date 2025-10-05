from camera import Camera
class DetectEGP():
    def __init__(self, model):
        self.model = model

def test():
    MODEL = "../data/first_model"

    model = DetectEGP(model = MODEL)
    cam = Camera()

    while cam.isOpened():
        frame = cam.read()

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

