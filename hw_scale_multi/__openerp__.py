# -*- coding: utf-8 -*-
##############################################################################
#
#   Hardware Scale Multi Driver
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
    'name': "Scale Multi Hardware Driver",
    'version': '1.0',
    'depends': ['hw_proxy'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',
    'summary': """Hardware Driver for POS Scale Multi""",
    'description': """
Scale Multi Hardware Driver
===========================
This module allows the point of sale to connect with the scales:\n
* Mettler Toledo Ariva\n
* Dibal\n
This module is designed to be installed on the *PosBox*. On the
*main Odoo server*, you should install the module *pos_scale_multi*.
    """,

    'data': [

    ],

    'demo': [
    ],

    'qweb': [
    ],
}
