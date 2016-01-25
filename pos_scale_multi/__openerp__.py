# -*- coding: utf-8 -*-
##############################################################################
#
#   POS Scale Multi
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
    'name': "POS Scale Multi",
    'version': '1.0',
    'depends': ['point_of_sale'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',
    'summary': """Multiple Scales in POS""",
    'description': """
POS Scale Multi
===============
This module allows defining and configuring scales to be used in the point of sale.\n
This module is designed to be installed on the *main Odoo server*. On the *PosBox*, you should install the module *hw_scale_multi*.
    """,

    'data': [
        'views/pos_config.xml',
        'views/scale_config.xml',
        'views/js.xml',
        'data/data.xml',
    ],

    'demo': [
    ],

    'qweb': [
    ],
}
