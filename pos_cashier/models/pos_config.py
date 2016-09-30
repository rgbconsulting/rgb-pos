# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    cashier_ids = fields.Many2many(string='Cashiers', comodel_name='res.users', help="List of cashiers")
