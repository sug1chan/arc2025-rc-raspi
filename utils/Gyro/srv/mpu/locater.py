from . import config
import math
import numpy as np
import pandas as pd
import scipy

# 引数から位置情報を推定する。
# クラスではなく、関数で実装？
# 計算方法
# 停止時情報の記録
# 停止の確認

# 停止状態かの確認
# 現在の加速度、角速度から計算する。
# 引数:
#       現在の時間t: 
#       現在の加速度a(g*m/s^2): 
#       現在の角速度phi(deg/s)
#       加速度の最大、最低値
#       角速度の最大、最低値
# 返り値:
#       停止フラグ: 動作中: 0, 停止状態: 1, データ処理中: 2
#       加速度の最大、最低値
#       角速度の最大、最低値
def is_stay(t, a, rad, max_acc, min_acc, max_rad, min_rad):
    result = 0
    if t < config.STAY_TIME:
        if (a > max_acc):
            max_acc = a * 1.1
        if (a < min_acc):
            min_acc = a * 1.1
        if (rad > max_rad):
            max_rad = rad * 1.1
        if (rad < min_rad):
            min_rad = rad * 1.1
        result = 2
    else:
        # 動作中か判別：true->動作中 false->停止中
        if ((a < min_acc or a > max_acc) or (rad < min_rad or rad > max_rad)):
            result = 0
        else:
            result = 1
    return result, max_acc, min_acc, max_rad, min_rad
    

# localization_calculation:自己位置推定関数にデータを渡す。
# 引数：
#       現在の位置x(m): 
#       現在の位置y(m): 
#       現在の角度(rad): radian 
#       現在の速度v(m/s):
#       加速度acccerate(g*m/s^2): Ax
#       角速度phi(dig): Gz
# 返り値:
#       最新の位置x(m): x
#       最新の位置y(m): y
#       最新の角度rad(rad)): rad
#       最新の速度verocity(m/s): v
def localization_calculation(current_x, current_y, current_rad, current_v, current_a, current_g):
    # 運動量u
    # [加速度a], 
    # [角速度phi(dig -> rad)] 
    current_u = np.array([
            [current_a],
            [math.radians(current_g)]
        ]
    )
    # 位置情報localeまたはx
    # [位置x],
    # [位置y],
    # [速度v],
    # [角度rad]
    current_locale = np.array([
            [current_x],
            [current_y],
            [current_rad],
            [current_v]
        ]
    )
    new_locale, new_u = observation(current_locale, current_u, config.INTERVAL)

    return new_locale[0, 0], new_locale[1, 0], new_locale[2, 0], new_locale[3, 0]

# 運動量、位置情報の実計算
def observation(xd, u, DT):
    # add noise to input
    # ud = u + INPUT_NOISE @ np.random.randn(2, 1)
    ud = u
    xd = motion_model(xd, ud, DT)
    return xd, ud     

def motion_model(x, u, DT):
    F = np.array([
        [1.0, 0.0, 0.0, 0.0], # x
        [0.0, 1.0, 0.0, 0.0], # y
        [0.0, 0.0, 1.0, 0.0], # radian
        [0.0, 0.0, 0.0, 0.0] # verocity
    ])
    # [x, y, phi, v] * [acceleration, omega]
    # B = [ v * cos(rad) * dt, 0.0]
    #     [ v * sin(rad) * dt, 0.0]
    #     [0.0                      ,  dt]
    #     [9.8 * dt                 , 0.0]
    B = np.array([ 
        [math.cos(x[2, 0]) * DT, 0.0],  # x = x + cos(rad)*dt*acc
        [math.sin(x[2, 0]) * DT, 0.0],  # y = y + sin(rad)*dt*acc
        [0.0, 7.47 * DT],                      # radian = rad + phi*dt
        [9.8 * DT, 0.0]                 # verocity = 9.8 * DT * acc
    ])

    x = F @ x + B @ u

    return x