# -*- coding: utf-8 -*-

{
    'name': 'UAnalyst Default Tags Contact',
    'version': '1.2',
    'category': 'UAnalyst Default Tags Contact',
    'summary': 'UAnalyst Default Tags Contact',
    'description': """
    UAnalyst Default Tags Contact.
    """,
    'sequence': '-100',
    'depends': ['hr',
                'contacts',
                ],
    'data': [
        'views/res_partner_category_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
