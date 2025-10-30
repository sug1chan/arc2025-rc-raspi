import config as cfg
from utils import *

from utils.ac_util import State, get_mode

from utils.connection import *
from utils.socket_utils import *

import numpy as np
import cv2, argparse

DEFAULT_EPSILON = 32

DEFAULT_THE_EPSILON = .05
DEFAULT_DST_EPSILON = .05
LOGCONF = "./logconf.json"

class AutoControl():
    def __init__(self,
                 mode = 0,
                 epsilon     = DEFAULT_EPSILON,
                 rad_epsilon = DEFAULT_THE_EPSILON,
                 dst_epsilon = DEFAULT_DST_EPSILON,
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

        self.epsilon = epsilon
        self.rad_epsilon = 2 * np.pi * rad_epsilon
        self.dst_epsilon = dst_epsilon

    def init(self, ):
        self.mode   = State.INIT

        # --- socket settings ---
        self.sfd.connect()

        # --- init ---
        # camera
        # self.fcam_center = self.fcamera.width / 2
        # self.bcam_center = self.bcamera.width / 2

        # gyro
        self.gyro_position = self.gyro.get_xy()

        # yolo
        self.egp_target = None
        
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
    def detect(self,
               camera = self.fcamera):
        if camera.isOpened():
            _frame = camera.read()
            return self.model.detect(frame, )
        # TODO:
        raise Exception("カメラが起動していません。")

    # BBox からバウンディングボックスの中心が中央であるかを判定する。
    # return:
    #    -1 : 左
    #     0 : 中央
    #     1 : 右

    def is_center(self,
                  bbox,
                  center):
        bp = 0
        _diff = bp - center

        if _diff <= self.epsilon:
            return -1
        elif _diff < self.epsilon:
            return 0
        else:
            return 1

    # --- robot behavior ---
    def _finish(self, ):
        pass

    def _init(self, ):
        for direction, distance in self.init_mode:
            if direction != Direction.FRONT:
                _direc_rad = direc_lst[direction]
                self._turn(_direc_red)

            self._forward(distance)

        return State.DETECTION

    def _detection(self, ):
        self.egp_target = None
        _count = 10
        _move_mode = False
        

        while self.egp_target is None:
            detected = self.detect(self.bcamera)

            if detected.isNone():
                if _count > 0:
                    _count -= 1
                else:
                    _move_mode = True
                
                continue

            size = 0
            target = np.array([0, 0])
            for bbox in detected:
                # if bbox.size > size:
                #     size = bbox
                pass

        return State.APPROACH

    def _approach(self, ):
        # NOTE: INIT モードでナスに決め打ちで近づくため今回は不要。
        return State.ADJUSTMENT

    def _adjustment(self, ):
        pass

    def _cutting(self, ):
        opt = SERVO_OPT.do
        self.sendmsg(SERVO_DO, opt)

        sleep(self.servo_interval)

        return State.COMEBACK

    def _comeback(self, ):
        self._backward(300)

        _first_pos, _, _first_theta = self.gyro.get()

        # turn
        _start_pos_theta = np.arctan2(_first_pos[1], _first_pos[0])
        _theta = np.pi + _first_theta - _start_pos_theta
        _theta = (_first_theta + np.pi) % (2 * np.pi) - np.pi

        self._turn(self, _theta)

        # fwd
        distance = np.linalg(_first_pos)
        self._forward(distance)

        return State.FINISH

    # - Control function

    def _turn(self,
              theta, ):

        def _get_opt(is_lturn):
            if is_lturn:
                return CAT_MOVE_OPT.ltrn
            else:
                return CAT_MOVE_OPT.rtrn

        _start_theta = self.gyro.get_theta()
        goal_theta  = _start_theta + theta

        is_lturn = (goal_theta > _start_theta)
        opt = _get_opt(is_lturn)
        self.sendmsg(CAT_MOVE, opt)

        while True:
            _now_theta = self.gyro.get_theta()
            diff = goal_theta - _now_theta

            if np.abs(diff) < self.rad_epsilon:
                # stop
                opt = CAT_MOVE_OPT.stop
                self.sendmsg(CAT_MOVE, opt)
                break

            if not ((is_lturn     and diff > 0) or \
                    (not is_lturn and diff < 0)):
                is_lturn = False if is_lturn else True
                opt = _get_opt(is_lturn)
                self.sendmsg(CAT_MOVE, opt)

    def _forward(self,
                 distance):
        return self._move_fb(Direction.FRONT,
                             distance)

    def _backward(self,
                  distance):
        return self._move_fb(Direction.BACK,
                             distance)

    def _move_fb(self,
                 direction,
                 distance):

        if distance <= 0:
            return False

        if direction == Direction.FRONT:
            opt = CAT_MOVE_OPT.fwd
        elif direction == Direction.BACK:
            opt = CAT_MOVE_OPT.bwd
        else:
            return False

        _start_pos = self.gyro.get_xy()
        _epsilon = distance * self.dst_epsilon

        self.sendmsg(CAT_MOVE, opt)


        while True:
            _now_pos = self.gyro.get_xy()
            diff = np.linalg(_now_pos - _start_pos)

            if diff > distance - _epsilon:
                opt = CAT_MOVE_OPT.stop
                self.sendmsg(CAT_MOVE, opt)
                
                break


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

