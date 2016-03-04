# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import os
import logging

_logger = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    _logger.error('Odoo module hw_serial depends on the pyserial python module')
    serial = None


class SerialDriver(object):
    def serial_do_operation(self, operation, params):
        result = {}
        ser = self.serial_open(params)
        if ser:
            try:
                if operation == 'read':
                    data = ser.readline()
                    result['data'] = data
                else:
                    data = params.get('data', '')
                    encoding = params.get('encoding', None)
                    if encoding:
                        data = data.decode(encoding)
                    ser.write(data)
                result['status'] = 'ok'
            except serial.SerialException, message:
                result['status'] = 'error'
                result['message'] = str(message)
            finally:
                ser.close()
        else:
            result['status'] = 'error'
            result['message'] = 'The serial port was not found!'
        return result

    def serial_open(self, params):
        try:
            port = params.get('port', '/dev/ttyUSB0')
            if not os.path.exists(port):
                _logger.error('Serial port not found')
                return None
            return serial.Serial(port,
                                 baudrate=int(params.get('baudrate', 9600)),
                                 bytesize=int(params.get('bytesize', 8)),
                                 stopbits=int(params.get('stopbits', 1)),
                                 parity=params.get('parity', 'E'),
                                 timeout=float(params.get('timeout', 20)) / 1000,
                                 writeTimeout=float(params.get('timeout', 20)) / 1000)
        except Exception as e:
            _logger.error(str(e))
            return None
