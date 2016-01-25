# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    iface_scale_config = fields.Many2one(string='Scale Config', comodel_name='pos.scale.config')
