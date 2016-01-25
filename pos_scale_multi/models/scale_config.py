# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class ScaleConfig(models.Model):
    _name = "pos.scale.config"

    name = fields.Char(required=True)
    driver = fields.Selection([
        ('mettler', 'Mettler'),
        ('dibal', 'Dibal')
    ], default='mettler')
    params_ids = fields.One2many('pos.scale.config.params', 'scale_config_id')
