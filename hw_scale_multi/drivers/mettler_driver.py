import time
import os
import serial
from .abstract_driver import AbstractDriver


class MettlerDriver(AbstractDriver):
    def __init__(self, params):
        super(MettlerDriver, self).__init__()
        self.device_path = params.get('device_path', '/dev/ttyUSB0')
        self.baudrate = int(params.get('baudrate', 9600))
        self.bytesize = int(params.get('bytesize', 7))
        self.stopbits = int(params.get('stopbits', 1))
        self.parity = params.get('parity', 'E')
        self.timeout = float(params.get('timeout', 20)) / 1000
        self.weight_string = params.get('read_weight', 'W')

    def get_device(self):
        try:
            if not os.path.exists(self.device_path):
                self.set_status('disconnected', 'Scale Not Found')
                return None

            self.set_status('connected', 'Connected to '+self.device_path)
            return serial.Serial(self.device_path,
                        baudrate = self.baudrate,
                        bytesize = self.bytesize,
                        stopbits = self.stopbits,
                        parity   = self.parity,
                        timeout  = self.timeout,
                        writeTimeout= self.timeout)

        except Exception as e:
            self.set_status('error', str(e))
            return None

    def read_weight(self):
        with self.scalelock:
            if self.device:
                try:
                    self.device.write('W')
                    time.sleep(0.2)
                    answer = []

                    while True:
                        char = self.device.read(1)
                        if not char:
                            break
                        else:
                            answer.append(char)

                    if '?' in answer:
                        stat = ord(answer[answer.index('?')+1])
                        if stat == 0:
                            self.weight_info = 'ok'
                        else:
                            self.weight_info = []
                            if stat & 1 :
                                self.weight_info.append('moving')
                            if stat & 1 << 1:
                                self.weight_info.append('over_capacity')
                            if stat & 1 << 2:
                                self.weight_info.append('negative')
                                self.weight = 0.0
                            if stat & 1 << 3:
                                self.weight_info.append('outside_zero_capture_range')
                            if stat & 1 << 4:
                                self.weight_info.append('center_of_zero')
                            if stat & 1 << 5:
                                self.weight_info.append('net_weight')
                    else:
                        answer = answer[1:-1]
                        if 'N' in answer:
                            answer = answer[0:-1]
                        try:
                            self.weight = float(''.join(answer))
                        except ValueError as v:
                            self.set_status('error','No data Received, please power-cycle the scale');
                            self.device = None

                except Exception as e:
                    self.set_status('error',str(e))
                    self.device = None
