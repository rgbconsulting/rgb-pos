# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.
{
    'name': "POS Cache Enhanced",
    'version': '1.0',
    'depends': ['point_of_sale'],
    'license': 'LGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'Point Of Sale',
    'summary': """Enable product cache for a lower POS loading time""",
    'description': """
POS Cache Enhanced
==================
Create a cache of products per pos config to improve the loading time of sessions
with lots of products.\n
The caches automatically update through a cron job.
    """,

    'data': [
        'data/cache_cron.xml',
        'security/ir.model.access.csv',
        'views/pos_config.xml',
        'views/templates.xml',
    ],

    'demo': [
    ],
}
