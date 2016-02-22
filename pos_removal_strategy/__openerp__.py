# -*- coding: utf-8 -*-
##############################################################################
#
#   POS Removal Strategy
#   Copyright 2016 RGB Consulting, SL
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "POS Removal Strategy",
    'version': '1.0',
    'depends': ['pos_picking_state_fix'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',
    'summary': """Removal strategy support for POS pickings""",
    'description': """
POS Removal Strategy
====================
This module extends the pickings created from POS orders to correctly process
products with serial numbers and specific removal strategies.
    """,

    'data': [
    ],

    'demo': [
    ],
}
