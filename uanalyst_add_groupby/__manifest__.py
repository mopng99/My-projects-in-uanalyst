# -*- coding: utf-8 -*-

{
    'name': 'UAnalyst Adding Group By',
    'version': '1.2',
    'category': 'UAnalyst Adding Group By',
    'summary': 'UAnalyst Adding Group By in Inventory And Journal',
    'description': """
    UAnalyst Adding Group By in Inventory And Journal.
    """,
    'sequence': '-100',
    'depends': ['base',
                'account',
                'stock',
                ],
    'data': [
        'views/stock_quant_views.xml',
        'views/account_move_line_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
