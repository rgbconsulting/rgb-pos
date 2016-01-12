# -*- coding: utf-8 -*-
##############################################################################
#
#   POS Order Taxes
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
    'name': "POS Order Taxes",
    'version': '1.0',
    'depends': ['point_of_sale'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',

    'summary': """Taxes in POS order""",

    'description': """
Include taxes in the POS order
==============================
* Include taxes into the POS order
* Add option in the POS config to include taxes in prices
    """,

    'data': [
        'views/js.xml',
        'views/pos_config.xml',
        'views/pos_order.xml',
        "security/ir.model.access.csv",
    ],

    'demo': [
    ],

    'qweb': [
        'static/src/xml/pos.xml'
    ],

}
