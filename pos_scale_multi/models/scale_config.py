# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from odoo import fields, models


class ScaleConfig(models.Model):
    _name = "pos.scale.config"

    name = fields.Char(required=True)
    driver = fields.Selection(selection=[('mettler', 'Mettler'), ('dibal', 'Dibal')], default='mettler')
    params_ids = fields.One2many(comodel_name='pos.scale.config.params', inverse_name='scale_config_id')
