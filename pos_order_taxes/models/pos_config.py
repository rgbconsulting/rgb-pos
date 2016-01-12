# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    display_price_with_taxes = fields.Boolean(
        string='Price With Taxes',
        help="Display Prices with taxes on POS"
    )
