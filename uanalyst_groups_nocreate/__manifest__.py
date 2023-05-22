# -*- coding: utf-8 -*-

{
    'name': 'UAnalyst Groups NoCreate',
    'version': '1.2',
    'category': 'UAnalyst Groups NoCreate',
    'summary': 'UAnalyst Groups NoCreate',
    'description': """
    UAnalyst Groups NoCreate.
    """,
    'author': "Mohamed Nagy",
    'sequence': '-100',
    'depends': ['base', 'product', ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
