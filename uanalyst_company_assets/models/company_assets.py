# -*- coding: utf-8 -*-
from odoo import models, fields


class EmployeeCustody(models.Model):
    _name = 'company.assets'
    _description = 'Company Assets'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    uanalyst_reference = fields.Char(default="NEW", compute="_compute_ref")
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    product_id = fields.Many2one('product.template', string='Product', tracking=True, required=True)
    state = fields.Selection([
        ('requested', 'Requested'),
        ('received', 'Received'),
        ('returned', 'Returned')]
        , default="requested", string="status", tracking=True)
    receiving_date = fields.Date(readonly=True, tracking=True)
    returned_date = fields.Date(readonly=True, tracking=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', tracking=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'received'
            rec.receiving_date = fields.Date.today()

    def action_return(self):
        for rec in self:
            rec.state = 'returned'
            rec.returned_date = fields.Date.today()

    def _compute_ref(self):
        self.uanalyst_reference = self.product_id.name
