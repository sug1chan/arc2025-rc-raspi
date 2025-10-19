import config as cfg
from utils import *

from utils.ac_util import State, get_mode

from utils.connection import *
from utils.socket_utils import *

import cv2

DEFAULT_EPSILON = 64

class AutoControl():
    def __init__(self,
                 mode = 0,
                 epsilon = DEFAULT_EPSILON):
        self.model  = None
        self.camera = 
        self.sfd    = ClientSocketCom(cfg.IP_ADDR,
                                      cfg.TCP_PORT)
        self.gyro   = None
        self.ir1    = None
        self.ir2    = None

        # --- INIT MODE SETTINGS ---
        self.init_mode = get_mode(mode)

        self.func = [_finish,
                     _init,
                     _detection,
                     _approach,
                     _adjustment,
                     _cutting,
                     _comeback, ]

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


def main():
    pass

if __name__ == "__main__":
    main()

