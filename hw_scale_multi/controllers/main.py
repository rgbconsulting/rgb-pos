# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import logging

from openerp import http
import openerp.addons.hw_proxy.controllers.main as hw_proxy
from ..drivers import dibal_driver, mettler_driver, abstract_driver

_logger = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    _logger.error('Odoo module hw_scale_multi depends on the pyserial python module')
    serial = None

if serial:
    hw_proxy.drivers['scale'] = abstract_driver.AbstractDriver()


class ScaleProxy(hw_proxy.Proxy):
    def __init__(self):
        self.scale_thread = hw_proxy.drivers['scale']

    @http.route('/hw_proxy/scale_read/', type='json', auth='none', cors='*')
    def scale_read(self):
        if self.scale_thread:
            return {'weight': self.scale_thread.get_weight(), 'unit': 'kg', 'info': self.scale_thread.get_weight_info()}
        return None

    @http.route('/hw_proxy/scale_zero/', type='json', auth='none', cors='*')
    def scale_zero(self):
        if self.scale_thread:
            self.scale_thread.set_zero()
        return True

    @http.route('/hw_proxy/scale_tare/', type='json', auth='none', cors='*')
    def scale_tare(self):
        if self.scale_thread:
            self.scale_thread.set_tare()
        return True

    @http.route('/hw_proxy/scale_clear_tare/', type='json', auth='none', cors='*')
    def scale_clear_tare(self):
        if self.scale_thread:
            self.scale_thread.clear_tare()
        return True

    @http.route('/hw_proxy/scale_config', type='json', auth='none', cors='*')
    def scale_config(self, params):
        params = eval(params)
        if self.scale_thread:
            if self.scale_thread.isAlive():
                self.scale_thread.stop()
        driver = params.get('driver')
        if driver == 'mettler':
            self.scale_thread = mettler_driver.MettlerDriver(params)
            hw_proxy.drivers['scale'] = self.scale_thread
            return True
        elif driver == 'dibal':
            self.scale_thread = dibal_driver.DibalDriver(params)
            hw_proxy.drivers['scale'] = self.scale_thread
            return True
        else:
            self.scale_thread = dibal_driver.AbstractDriver()
            self.set_status('error', 'Scale driver not defined!, please review scale configuration')
