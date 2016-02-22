# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api


class PosPicking(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def create_picking(self):
        super(PosPicking, self).create_picking()
        if self.picking_id.state == 'confirmed':
            self.picking_id.action_assign()
            if self.picking_id.state == 'assigned':
                self.picking_id.do_prepare_partial()
                self.picking_id.do_transfer()
                return True
            return False
