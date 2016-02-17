# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api


class PosPicking(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def create_picking(self):
        try:
            super(PosPicking, self).create_picking()
        except:
            # Cancel move lines
            if self.picking_id.state != 'done':
                for move in self.picking_id.move_lines:
                    move.do_unreserve()
        return True
