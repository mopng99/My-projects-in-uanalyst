# -*- coding: utf-8 -*-

{
    'name': 'UAnalyst payroll',
    'version': '1.0.0',
    'category': 'UAnalyst payroll',
    'summary': 'UAnalyst payroll',
    'description': """
    UAnalyst payroll.
    """,
    'sequence': '-100',
    'depends': ['base',
                'hr_work_entry_contract',
                ],
    'data': [
        'views/hr_work_entry_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
