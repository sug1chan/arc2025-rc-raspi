class State():
    FINISH     = 0
    INIT       = 1
    DETECTION  = 2
    APPROACH   = 3
    ADJUSTMENT = 4
    CUTTING    = 5
    COMEBACK   = 6
    STATE_MAX  = 7

"""
    # format
        ( 方向(現在の方向から見た), 距離 )

        方向:
            0 : 直進
            1 : 右ターン
            2 : 後進
            3 : 左ターン

    # mode 0
        step 1: 直進     100 cm

    # mode 1
        step 1: 直進     300 cm
        step 2: 右ターン 100 cm

    # mode 2
        step 1: 直進     300 cm
        step 2: 左ターン 100 cm
"""
mode_0 = { (0, 100) }
mode_1 = { (0, 300), (1, 100) }
mode_2 = { (0, 300), (3, 100) }

mode_data = { 0: mode_0,
              1: mode_1,
              2: mode_2, }


def get_mode(mode):
    if not mode in mode_data:
        raise Exception(f"モードが不正です: {mode}")
    return mode_data[mode]

