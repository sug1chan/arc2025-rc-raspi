import numpy as np

class State():
    FINISH     = 0
    INIT       = 1
    DETECTION  = 2
    APPROACH   = 3
    ADJUSTMENT = 4
    CUTTING    = 5
    COMEBACK   = 6
    STATE_MAX  = 7

class Direction():
    FRONT = 0
    RTURN = 1
    BACK  = 2
    LTURN = 3

"""
    # format
        ( 方向(現在の方向から見た), 距離 )

        方向:
            0 : 直進
            1 : 右ターン
            2 : 後進
            3 : 左ターン

    # mode 0
        step 1: 直進      500 mm

    # mode 1
        step 1: 直進     3000 mm
        step 2: 右ターン 1000 mm

    # mode 2
        step 1: 直進     3000 mm
        step 2: 左ターン 1000 mm
"""
mode_0 = { (0, 500) }
mode_1 = { (0, 3000), (1, 1000) }
mode_2 = { (0, 3000), (3, 1000) }

mode_data = { 0: mode_0,
              1: mode_1,
              2: mode_2, }

def get_mode(mode):
    if not mode in mode_data:
        raise Exception(f"モードが不正です: {mode}")
    return mode_data[mode]

direc_lst = {Direction.FRONT: 0,
             Direction.RTURN: -np.pi / 2,
             Direction.LTURN:  np.pi / 2,
             Direction.BACK:   np.pi, }

