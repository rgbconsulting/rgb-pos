# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_auto_reconcile = fields.Boolean(string='Auto-Reconcile Invoices',
                                          help='Automatically reconcile invoices created from POS')

    @api.onchange('iface_invoicing')
    def _onchange_invoicing(self):
        if not self.iface_invoicing:
            self.iface_auto_reconcile = False
