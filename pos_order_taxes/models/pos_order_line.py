# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, fields, api

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.multi
    def _compute_taxes(self):
        res = {
            'total': 0,
            'total_included': 0,
            'taxes': [],
        }
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(
                price, line.qty, product=line.product_id,
                partner=line.order_id.partner_id)
            res['total'] += taxes['total']
            res['total_included'] += taxes['total_included']
            res['taxes'] += taxes['taxes']
        return res

    @api.one
    @api.depends('tax_ids', 'qty', 'price_unit', 'product_id', 'discount', 'order_id.partner_id')
    def _amount_line_all(self):
        taxes = self._compute_taxes()
        self.price_subtotal = taxes['total']
        self.price_subtotal_incl = taxes['total_included']

    tax_ids = fields.Many2many(
        'account.tax', 'pline_tax_rel', 'pos_line_id', 'tax_id',
        "Taxes", domain=[('type_tax_use', '=', 'sale')])
    price_subtotal = fields.Float(compute="_amount_line_all", store=True)
    price_subtotal_incl = fields.Float(compute="_amount_line_all", store=True)
