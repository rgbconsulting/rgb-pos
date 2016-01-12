# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, fields
from openerp.addons import decimal_precision as dp

class PosOrderTax(models.Model):
    _name = 'pos.order.tax'

    pos_order = fields.Many2one('pos.order', string='POS Order',
                                ondelete='cascade', index=True)
    tax = fields.Many2one('account.tax', string='Tax')
    name = fields.Char(string='Tax Description', required=True)
    base = fields.Float(string='Base', digits=dp.get_precision('Account'))
    amount = fields.Float(string='Amount', digits=dp.get_precision('Account'))
