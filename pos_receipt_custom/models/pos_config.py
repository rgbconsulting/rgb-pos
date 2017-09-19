# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    receipt_use_logo = fields.Boolean('Logo in receipt', default=False)
    logo = fields.Binary('Logo')
