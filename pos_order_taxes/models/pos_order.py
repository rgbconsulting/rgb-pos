# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.order"

    taxes = fields.One2many(comodel_name='pos.order.tax',
                            inverse_name='pos_order', readonly=True)

    @api.multi
    def _tax_list_get(self):
        agg_taxes = {}
        for order in self:
            for line in order.lines:
                line_base = line.price_subtotal
                line_taxes = line.tax_ids
                if order.fiscal_position_id:
                    line_taxes = order.fiscal_position_id.map_tax(line_taxes)
                for tax in line_taxes:
                    tax_amount = tax._compute_amount(line_base, line.price_unit)
                    if tax.id in agg_taxes:
                        agg_taxes[tax.id]['base'] += line_base
                        agg_taxes[tax.id]['amount'] += tax_amount
                    else:
                        agg_taxes[tax.id] = {
                            'tax_id': tax.id,
                            'name': tax.name,
                            'base': line_base,
                            'amount': tax_amount,
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
