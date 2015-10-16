# -*- coding: utf-8 -*-
##############################################################################
#
#   POS Product Pack
#   Copyright 2015 RGB Consulting, SL
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
    'name': "POS Product Pack",
    'version': '1.0',
    'depends': ['point_of_sale'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',

    'summary': """Custom Packs In Pos""",

    'description': """
Create packs of products for POS
================================
* Create a pack with groups of products
* Sell it in POS with a custom price
    """,

    'data': [
        'views/product_pack.xml',
        'views/js.xml',
    ],

    'demo': [

    ],

    'qweb': [
        'static/src/xml/pos.xml',
    ],
}
