from socket_utils.command import *

import socket, time
from threading import Thread, Event

CMD_FLD_DLMTR = ' '
CMD_PRM_DLMTR = ','
CMD_TRMNT = '\r'

class ClientSocketCom():
        
    def __init__(self, ip_addr, port_num):
        self.client_sock = None
        self.ip_addr = ip_addr
        self.port_num = port_num
        self.th_event = Event()
        self.th_event.clear()
        self.th = Thread(target=self.recvcmd_th, daemon=True)
        self.th.start()

    def getCmd(self, cmdName, cmdParams):
        paramfld = ''
        if len(cmdParams) > 0:
            for i, p in enumerate(cmdParams):
                if i==0:
                    paramfld = paramfld + p
                else:
                    paramfld = paramfld + CMD_PRM_DLMTR + p
        
        msg = 'SET' + CMD_FLD_DLMTR + cmdName
        if paramfld != '':
            msg = msg + CMD_FLD_DLMTR + paramfld
        msg = msg + CMD_TRMNT
        return msg
    
    def connect(self):
        rtn = True
        try:
            self.client_sock.connect((self.ip_addr, self.port_num))
            print('Connected.')
            self.th_event.set()
        except Exception as error:
            print("Failed to connect.")
            print(error)
            self.th_event.clear()
            rtn = False
        return rtn

    def sendMsg(self, msg):
        try:
            self.client_sock.sendall(msg)
            #self.client_sock.sendall(msg.encode('UTF-8'))
            #print('Send: ' + msg)              
        except Exception as error:
            print('Failed to send, exception has occurred.')
            print(error)
            self.stop();
            self.start();

    def recvcmd_th(self):
        while True:
            time.sleep(0.2)
            if not self.th_event.wait(0.1):
                continue
            try:
                recv_msg  = self.client_sock.recv(1024)
                if len(recv_msg) > 0:
                    print('Recv: ' + recv_msg)
            except Exception as error:    
                print(error)

    def start(self):
        if self.client_sock is None:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.settimeout(3.0)
            self.connect()

    def stop(self):
        self.th_event.clear()
        if self.client_sock is not None:
            self.client_sock.close()
            self.client_sock = None

def debug():
    test_addr = "127.0.0.1"
    test_port = 8000
    command = [(CAT_MOVE, CAT_MOVE_OPT),
               (CAT_SLOW_MODE, CAT_SLOW_OPT),
               (HEATER_MODE, HTR_MODE_OPT),
               (ARM_MODE, ARM_OPT),
               (EMERGENCY_STOP, E_STOP_OPT),
               (SERVO_DO, SERVO_OPT), ]

    sock = ClientSocketCom(test_addr, test_port)
    
    sock.start()

    for cmd, opts in command:
        for opt in opts.dbg_list:
            msg = cmd.pack(opt)
            sock.sendMsg(msg)


if __name__ == "__main__":
    debug()
