# -*- coding: utf-8 -*-
##############################################################################
#
#   POS Receipt Custom
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
    'name': "POS Receipt Custom",
    'version': '1.0',
    'depends': ['pos_sequence_ref_number'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'POS',
    'summary': """Custom POS receipt""",
    'description': """
Customizing the POS receipt
===========================
* Add company/custom logo to the POS receipt.
* Add simplified invoice information

TODO
----
* Customize XML Receipt (posbox)
    """,

    'data': [
        'views/logo.xml',
    ],

    'qweb': [
        'static/src/pos.xml',
    ],
}
