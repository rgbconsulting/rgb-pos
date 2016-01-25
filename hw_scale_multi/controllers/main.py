# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import logging

from openerp import http
import openerp.addons.hw_proxy.controllers.main as hw_proxy
from ..drivers import dibal_driver, mettler_driver

_logger = logging.getLogger(__name__)
# TODO - Recharge the last scale configuration if the PosBox restarts
# TODO - fix global variable scale_thread declaration

try:
    import serial
except ImportError:
    _logger.error('Odoo module hw_scale_multi depends on the pyserial python module')
    serial = None


scale_thread = None


class ScaleProxy(hw_proxy.Proxy):
    @http.route('/hw_proxy/scale_read/', type='json', auth='none', cors='*')
    def scale_read(self):
        if scale_thread:
            return {'weight': scale_thread.get_weight(), 'unit': 'kg', 'info': scale_thread.get_weight_info()}
        return None

    @http.route('/hw_proxy/scale_zero/', type='json', auth='none', cors='*')
    def scale_zero(self):
        if scale_thread:
            scale_thread.set_zero()
        return True

    @http.route('/hw_proxy/scale_tare/', type='json', auth='none', cors='*')
    def scale_tare(self):
        if scale_thread:
            scale_thread.set_tare()
        return True

    @http.route('/hw_proxy/scale_clear_tare/', type='json', auth='none', cors='*')
    def scale_clear_tare(self):
        if scale_thread:
            scale_thread.clear_tare()
        return True

    @http.route('/hw_proxy/scale_config', type='json', auth='none', cors='*')
    def scale_config(self, params):
        global scale_thread
        params = eval(params)
        driver = params.get('driver')
        if scale_thread:
            if scale_thread.isAlive():
                scale_thread.stop()
        if driver == 'mettler':
            scale_thread = mettler_driver.MettlerDriver(params)
            hw_proxy.drivers['scale'] = scale_thread
            return True
        elif driver == 'dibal':
            scale_thread = dibal_driver.DibalDriver(params)
            hw_proxy.drivers['scale'] = scale_thread
            return True
        else:
            self.set_status('error', 'Scale driver not defined!, please review scale configuration')
