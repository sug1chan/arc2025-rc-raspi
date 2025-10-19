import array, socket, struct

class Cmd_No:
    CAT_MOVE       = 1
    CAT_SLOW_MODE  = 2
    HEATER_MODE    = 3
    ARM_MODE       = 4
    EMERGENCY_STOP = 5
    SERVO_DO       = 6

# option
class CAT_MOVE_OPT():
    l_up   = 0x08
    l_down = 0x04
    l_rest = 0x00
    l_stop = 0x0C
    r_up   = 0x02
    r_down = 0x01
    r_rest = 0x00
    r_stop = 0x03

    fwd    = l_up   | r_up
    bwd    = l_down | r_down
    rtrn   = l_up   | r_down
    ltrn   = l_down | r_up
    stop   = l_stop | r_stop
    rest   = l_rest | r_rest

    dbg_list = [fwd,
                bwd,
                rtrn,
                ltrn,
                stop,
                rest,]

class CAT_SLOW_OPT():
    on  = 0x01
    off = 0x00

    dbg_list = [on,
                off]

class HTR_MODE_OPT():
    on  = 0x01
    off = 0x00

    dbg_list = [on,
                off]

class ARM_OPT():
    rest  = 0x00
    lower = 0x01
    upper = 0x02
    stop  = 0x03

    dbg_list = [rest,
                lower,
                upper,
                stop, ]

class E_STOP_OPT():
    do = 0

    dbg_list = [do, ]

class SERVO_OPT():
    do = 0

    dbg_list = [do, ]

class Cmd_Class():
    def __init__(self,
                 name, ):
        self.name   = name
        self.cmd_no = Cmd_No.__dict__[self.name]
        self.struct = struct.Struct(">ii")

    def pack(self, opt_arg):
        return self.struct.pack(self.cmd_no, opt_arg)

# Command
CAT_MOVE       = Cmd_Class("CAT_MOVE")
CAT_SLOW_MODE  = Cmd_Class("CAT_SLOW_MODE")
HEATER_MODE    = Cmd_Class("HEATER_MODE")
ARM_MODE       = Cmd_Class("ARM_MODE")
EMERGENCY_STOP = Cmd_Class("EMERGENCY_STOP")
SERVO_DO       = Cmd_Class("SERVO_DO")


# ------- debug function ------------------------


def debug():
    debug_list = [CAT_MOVE,
                  CAT_SLOW_MODE,
                  HEATER_MODE,
                  ARM_MODE,
                  EMERGENCY_STOP,
                  SERVO_DO,]

    for cmd in debug_list:
        # opt = cmd.opt

        print("Name:", cmd.name)
        print("No  :", cmd.cmd_no)
        print("Cmd :")

        # for key in opt:
        #     print(f"  {key} = {cmd.opt[key]}")

if __name__ == "__main__":
    debug()

