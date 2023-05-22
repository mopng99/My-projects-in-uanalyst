# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    expense_line_ids = fields.One2many('hr.expense', 'sheet_id', string='Expense Lines', copy=True, tracking=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('reported', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Paid'),
        ('refused', 'Refused')
    ], compute='_compute_state', string='Status', copy=False, index=True, readonly=True, store=True, default='draft', tracking=True)

    def refuse_expense(self):
        if not self.user_has_groups('hr_expense.group_hr_expense_team_approver'):
            raise UserError(_("Only Managers and HR Officers can approve expenses"))
        elif not self.user_has_groups('hr_expense.group_hr_expense_manager'):
            current_managers = self.employee_id.expense_manager_id | self.employee_id.parent_id.user_id | self.employee_id.department_id.manager_id.user_id | self.user_id

            if self.employee_id.user_id == self.env.user:
                raise UserError(_("You cannot refuse your own expenses"))

            if not self.env.user in current_managers and not self.user_has_groups('hr_expense.group_hr_expense_user') and self.employee_id.expense_manager_id != self.env.user:
                raise UserError(_("You can only refuse your department expenses"))
        if self.state != 'reported':
            raise ValidationError(_("You can refuse expense in submit state"))
        self.write({'expense_line_ids': [(3, self.id, False)]})
        self.write({'is_refused': True})
        self.write({'state': 'refused'})
        # self.message_post_with_view('hr_expense.hr_expense_template_refuse_reason',
        #                                      values={'reason': reason, 'is_sheet': False, 'name': self.name})





