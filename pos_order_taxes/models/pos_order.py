# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = "pos.order"

    taxes = fields.One2many(comodel_name='pos.order.tax',
                            inverse_name='pos_order', readonly=True)

    @api.model
    def _amount_line_tax(self, line):
        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        taxes = line.tax_ids.compute_all(
            price, line.qty, product=line.product_id,
            partner=line.order_id.partner_id)['taxes']
        val = 0.0
        for c in taxes:
            val += c.get('amount', 0.0)
        return val

    @api.multi
    def _tax_list_get(self):
        agg_taxes = {}
        tax_lines = []
        for order in self:
            for line in order.lines:
                tax_lines.append({
                    'base': line.price_subtotal,
                    'taxes': line._compute_taxes()['taxes']
                })

        for tax_line in tax_lines:
            base = tax_line['base']
            for tax in tax_line['taxes']:
                tax_id = str(tax['id'])
                if tax_id in agg_taxes:
                    agg_taxes[tax_id]['base'] += base
                    agg_taxes[tax_id]['amount'] += tax['amount']
                else:
                    agg_taxes[tax_id] = {
                        'tax_id': tax_id,
                        'name': tax['name'],
                        'base': base,
                        'amount': tax['amount'],
                    }
        return agg_taxes

    @api.multi
    def compute_tax_detail(self):
        taxes_to_delete = False
        for order in self:
            taxes_to_delete = self.env['pos.order.tax'].search(
                [('pos_order', '=', order.id)])
            # Update order taxes list
            for key, tax in order._tax_list_get().iteritems():
                current = taxes_to_delete.filtered(
                    lambda r: r.tax.id == tax['tax_id'])
                if current:
                    current.write({
                        'base': tax['base'],
                        'amount': tax['amount'],
                    })
                    taxes_to_delete -= current
                else:
                    self.env['pos.order.tax'].create({
                        'pos_order': order.id,
                        'tax': tax['tax_id'],
                        'name': tax['name'],
                        'base': tax['base'],
                        'amount': tax['amount'],
                    })
        if taxes_to_delete:
            taxes_to_delete.unlink()

    @api.multi
    def action_paid(self):
        result = super(PosOrder, self).action_paid()
        self.compute_tax_detail()
        return result

    @api.model
    def create(self, vals):
        rec = super(PosOrder, self).create(vals)
        rec.compute_tax_detail()
        return rec
