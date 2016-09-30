# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api
from openerp.exceptions import ValidationError


class Users(models.Model):
    _inherit = 'res.users'

    pos_security_pin = fields.Char(string='Security PIN', size=12, help='Security PIN for the point of sale')

    @api.constrains('pos_security_pin')
    def _check_security_pin(self):
        for user in self:
            if user.pos_security_pin and not user.pos_security_pin.isdigit():
                raise ValidationError('Security PIN can only contain digits')
