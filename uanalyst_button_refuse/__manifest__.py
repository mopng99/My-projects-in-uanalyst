# -*- coding: utf-8 -*-

{
    'name': 'UAnalyst Button Refuse Expense',
    'version': '1.2',
    'category': 'UAnalyst Button Refuse Expense',
    'summary': 'UAnalyst Adding Button Refuse For Expense',
    'description': """
    UAnalyst Button Refuse Expense.
    """,
    'sequence': '-100',
    'depends': ['base',
                'hr_expense',
                ],
    'data': [
        'views/hr_expense_sheet_views.xml',
        'views/hr_expense_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
