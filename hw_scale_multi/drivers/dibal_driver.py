
import time
import os
import serial
from .abstract_driver import AbstractDriver


class DibalDriver(AbstractDriver):
    def __init__(self, params):
        super(DibalDriver, self).__init__()
        self.device_path = params.get('device_path', '/dev/ttyUSB0')
        self.baudrate = int(params.get('baudrate', 9600))
        self.bytesize = int(params.get('bytesize', 8))
        self.stopbits = int(params.get('stopbits', 1))
        self.parity = params.get('parity', 'E')
        self.timeout = float(params.get('timeout', 20)) / 1000
        self.weight_string = ""
        for c in params.get('read_weight', 5).split(','):
            self.weight_string += chr(int(c))
        self.weight_start_integer = int(params.get('weight_start_integer', 8))
        self.weight_integer = int(params.get('weight_integer', 2))
        self.weight_start_decimal = int(params.get('weight_start_decimal', 10))
        self.weight_decimal = int(params.get('weight_decimal', 3))

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
                    self.device.write(self.weight_string)
                    time.sleep(0.2)

                    answer = []
                    while True:
                        char = self.device.read(1)
                        if not char:
                            break
                        else:
                            answer.append(char)

                    if answer:
                        integer_weight = ''.join(answer[self.weight_start_integer:
                                                    (self.weight_start_integer + self.weight_integer)]).replace(' ','')
                        decimal_weight = ''.join(answer[self.weight_start_decimal:
                                                    (self.weight_start_decimal + self.weight_decimal)]).replace(' ','')
                        self.weight = self.convert_float(integer_weight + '.' + decimal_weight)
                    else:
                        self.set_status('error', 'No data Received, please power-cycle the scale')

                except Exception as e:
                    self.set_status('error', str(e))
                    self.device = None

    def convert_float(self, weight):
        try:
            return float(weight)
        except ValueError:
            return 0
