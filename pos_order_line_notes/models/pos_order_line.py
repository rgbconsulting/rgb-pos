# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, fields


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    line_note = fields.Char(string='Note')
