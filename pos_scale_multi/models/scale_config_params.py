# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from odoo import fields, models


class ScaleConfigParams(models.Model):
    _name = "pos.scale.config.params"

    name = fields.Char(required=True)
    value = fields.Char()
    scale_config_id = fields.Many2one(comodel_name='pos.scale.config')
