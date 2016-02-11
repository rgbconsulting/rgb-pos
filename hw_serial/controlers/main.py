# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import http
from ..drivers import serial_driver
import openerp.addons.hw_proxy.controllers.main as hw_proxy


hw_proxy.drivers['serial'] = serial_driver.SerialDriver()


class SerialProxy(http.Controller):
    def __init__(self):
        self.serial_proxy = hw_proxy.drivers['serial']

    @http.route('/hw_proxy/serial_read', type='json', auth='none', cors='*')
    def serial_read(self, params):
        params = eval(params)
        result = self.serial_proxy.serial_do_operation('read', params)
        return result

    @http.route('/hw_proxy/serial_write', type='json', auth='none', cors='*')
    def serial_write(self, params):
        params = eval(params)
        result = self.serial_proxy.serial_do_operation('write', params)
        return result
