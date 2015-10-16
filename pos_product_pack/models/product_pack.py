# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api

class ProductPack(models.Model):
    _inherit = 'product.template'

    is_pack = fields.Boolean(string="Is pack")

    @api.onchange('is_pack')
    def onchange_pack(self):
        if self.is_pack:
            self.type = 'service'


class ProductGroups(models.Model):
    _name = 'product.pack.group'

    name = fields.Char(translate=True)


class ProductPackLines(models.Model):
    _name = 'product.pack.line'

    group_id = fields.Many2one(comodel_name='product.pack.group', string='Group', required = True)
    product_ids = fields.Many2one(comodel_name='product.product')
    line_product_ids = fields.Many2many('product.product', relation='product_pack_line_product_rel', string='Products')


class ProductExtend(models.Model):
    _inherit = 'product.product'

    pack_lines_ids = fields.One2many('product.pack.line', 'product_ids')

    @api.onchange('is_pack')
    def onchange_pack(self):
        if self.is_pack:
            self.type = 'service'
