# -*- coding: utf-8 -*-

from openerp import fields, models

class UsersExtend(models.Model):
    _inherit = 'res.users'

    pos_cashier = fields.Many2one(comodel_name='pos.config', ondelete='cascade')


class CashierConfigExtend(models.Model):
    _inherit = 'pos.config'

    cashier_list = fields.One2many('res.users', 'pos_cashier', help="List of cashiers")
