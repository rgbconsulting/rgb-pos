# -*- coding: utf-8 -*-
##############################################################################
#
#   POS Order Line Notes
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
    'name': "POS Order Line Notes",
    'version': '1.0',
    'depends': ['point_of_sale'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',
    'summary': """Add notes to pos order lines""",
    'description': """
POS Order Line Notes
====================

Add notes to order lines. The notes are printed on the POS ticket.
    """,

    'data': [
        'views/pos_order_view.xml',
        'views/report_reciept.xml',
        'views/templates.xml',
    ],

    'qweb': [
        'static/src/xml/pos.xml',
    ],
}
