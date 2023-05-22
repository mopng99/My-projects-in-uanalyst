# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HrWorkEntry(models.TransientModel):

    _inherit = 'hr.work.entry.regeneration.wizard'

    employee_id = fields.Many2many('hr.employee', required=True, string="Employee")
    date_from = fields.Date('From', required=True, default=lambda self: self.env.context.get('date_start'))
    date_to = fields.Date('To', required=True, default=lambda self: self.env.context.get('date_end'))

    @api.depends('employee_id')
    def _compute_earliest_available_date(self):
        for wizard in self:
            dates = wizard.employee_id.contract_ids.mapped('date_generated_from')
            wizard.earliest_available_date = min(dates) if dates else None

    @api.depends('employee_id')
    def _compute_latest_available_date(self):
        for wizard in self:
            dates = wizard.employee_id.contract_ids.mapped('date_generated_to')
            wizard.latest_available_date = max(dates) if dates else None

    @api.depends('date_from', 'date_to', 'employee_id')
    def _compute_validated_work_entry_ids(self):
        for wizard in self:
            validated_work_entry_ids = self.env['hr.work.entry']
            if wizard.search_criteria_completed:
                search_domain = [('employee_id', 'in', wizard.employee_id.ids),
                                 ('date_start', '>=', wizard.date_from),
                                 ('date_stop', '<=', wizard.date_to),
                                 ('state', '=', 'validated')]
                validated_work_entry_ids = self.env['hr.work.entry'].search(search_domain, order="date_start")
            wizard.validated_work_entry_ids = validated_work_entry_ids

    @api.depends('validated_work_entry_ids')
    def _compute_valid(self):
        for wizard in self:
            wizard.valid = wizard.search_criteria_completed and len(wizard.validated_work_entry_ids) == 0

    @api.depends('date_from', 'date_to', 'employee_id')
    def _compute_search_criteria_completed(self):
        for wizard in self:
            wizard.search_criteria_completed = wizard.date_from and wizard.date_to and wizard.employee_id and wizard.earliest_available_date and wizard.latest_available_date

    @api.onchange('date_from', 'date_to', 'employee_id')
    def _check_dates(self):
        for wizard in self:
            wizard.earliest_available_date_message = ''
            wizard.latest_available_date_message = ''
            if wizard.search_criteria_completed:
                if wizard.date_from > wizard.date_to:
                    date_from = wizard.date_from
                    wizard.date_from = wizard.date_to
                    wizard.date_to = date_from
                if wizard.earliest_available_date and wizard.date_from < wizard.earliest_available_date:
                    wizard.date_from = wizard.earliest_available_date
                    wizard.earliest_available_date_message = 'The earliest available date is {date}' \
                        .format(date=self._date_to_string(wizard.earliest_available_date))
                if wizard.latest_available_date and wizard.date_to > wizard.latest_available_date:
                    wizard.date_to = wizard.latest_available_date
                    wizard.latest_available_date_message = 'The latest available date is {date}' \
                        .format(date=self._date_to_string(wizard.latest_available_date))

    @api.model
    def _date_to_string(self, date):
        if not date:
            return ''
        user_date_format = self.env['res.lang']._lang_get(self.env.user.lang).date_format
        return date.strftime(user_date_format)

    def _work_entry_fields_to_nullify(self):
        return ['active']

    def regenerate_work_entries(self):
        self.ensure_one()
        if not self.env.context.get('work_entry_skip_validation'):
            if not self.valid:
                raise ValidationError(_("In order to regenerate the work entries, you need to provide the wizard with an employee_id, a date_from and a date_to. In addition to that, the time interval defined by date_from and date_to must not contain any validated work entries."))

            if self.date_from < self.earliest_available_date or self.date_to > self.latest_available_date:
                raise ValidationError(_("The from date must be >= '%(earliest_available_date)s' and the to date must be <= '%(latest_available_date)s', which correspond to the generated work entries time interval.", earliest_available_date=self._date_to_string(self.earliest_available_date), latest_available_date=self._date_to_string(self.latest_available_date)))

        date_from = max(self.date_from, self.earliest_available_date) if self.earliest_available_date else self.date_from
        date_to = min(self.date_to, self.latest_available_date) if self.latest_available_date else self.date_to
        work_entries = self.env['hr.work.entry'].search([
            ('employee_id', 'in', self.employee_id.ids),
            ('date_stop', '>=', date_from),
            ('date_start', '<=', date_to),
            ('state', '!=', 'validated')])

        write_vals = {field: False for field in self._work_entry_fields_to_nullify()}
        work_entries.write(write_vals)
        self.employee_id.generate_work_entries(date_from, date_to, True)

