import config as cfg
from utils import *

from utils.ac_util import State, get_mode

from utils.connection import *
from utils.socket_utils import *

import cv2, argparse

DEFAULT_EPSILON = 64
LOGCONF = "./logconf.json"

class AutoControl():
    def __init__(self,
                 mode = 0,
                 epsilon = DEFAULT_EPSILON,
                 logconf = LOGCONF):
        # --- LOGGER SETTINGS ---
        self.log    = get_logger(self.__class__.__name__,
                                 logconf, )

        # --- MODULE SETTINGS ---
        self.model   = DetectEGP(cfg.YOLO_MODEL_PATH,
                                 threshold = cfg.YOLO_THRESHOLD,
                                 logger    = self.log,
                                 verbose   = False)
        self.fcamera = Camera(dev_id = cfg.FRONT_ID)
        self.bcamera = Camera(dev_id = cfg.BIRDS_EYE_ID)

        self.sfd     = ClientSocketCom(cfg.IP_ADDR,
                                       cfg.TCP_PORT, )
        self.gyro    = GyroSensor()
        self.ir1     = IRSensor()
        self.ir2     = IRSensor()

        # --- INIT MODE SETTINGS ---
        self.init_mode = get_mode(mode)

        self.func = [self._finish,
                     self._init,
                     self._detection,
                     self._approach,
                     self._adjustment,
                     self._cutting,
                     self._comeback, ]

    def init(self, ):
        self.mode   = State.INIT
        self.target = None

        # --- socket settings ---
        self.sfd.connect()
        
    def loop(self, ):
        self.init()

        while True:
            try:
                _f = self.func[self.mode]

                self.mode = _f()

                if self.mode is None:
                    break

                if self.mode == State.FINISH:
                    # 終了したことをログする。
                    return

            except Exception as e:
                print(e)
                break

        # 何かしらの理由で終了したことをログする。(エラー終了)
        pass

    # --- utils ---

    # - socket
    # データを Arduino に送信する
    def sendmsg(self, cmd, opt):
        _msg = cmd.pack(opt)
        self.sfd.sendMsg(self, _msg)

    # - yolo and camera
    # カメラからナスを検知し、BBox インスタンスを返す
    def detect(self, ):
        if self.camera.isOpened():
            _frame = self.camera.read()
            return self.model.detect(frame, )
        # TODO:
        raise Exception("カメラが起動していません。")

    # BBox からバウンディングボックスの中心が中央であるかを判定する。
    def is_center(self,
                  bbox, ):
        return False

    # --- robot behavior ---
        def _finish(self, ):
            pass

        def _init(self, ):
            pass

        def _detection(self, ):
            pass

        def _approach(self, ):
            pass

        def _adjustment(self, ):
            pass

        def _cutting(self, ):
            pass

        def _comeback(self, ):
            pass

def get_parser():
    parser = argparse.ArgumentParser(
            prog = "ARC Robot AutoController",
            add_help = True,
            )

    parser.add_argument("-m",
                        "--mode",
                        type = int,
                        help = "動作モードを指定。デフォルト0。というか現状0しか使わん。",
                        default = 0)

    return parser.parse_args()

def main():
    arg = get_parser()
    print(arg.mode)
    robot = AutoControl(mode = arg.mode,
                        logconf = None, )

if __name__ == "__main__":
    main()

