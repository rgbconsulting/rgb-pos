# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

import time
from openerp import models, api
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PosPicking(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def create_picking(self):
        try:
            super(PosPicking, self).create_picking()
        except:
            if self.picking_id.state != 'done':
                for move in self.picking_id.move_lines:
                    if move.quant_ids:
                        # We pass this move to done because the quants were already moved
                        move.write({'state': 'done', 'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
                    else:
                        # If there are no moved quants we pass the move to Waiting Availability
                        move.do_unreserve()
        return True
