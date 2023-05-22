# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_('You can delete expense report state is draft only'))
        return super(HrExpenseSheet, self).unlink()
