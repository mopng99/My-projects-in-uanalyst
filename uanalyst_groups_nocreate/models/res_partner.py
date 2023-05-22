# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    group_ids = fields.Many2many('res.groups', default=lambda self: self.env.ref('base.group_user'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.user.has_group('uanalyst_groups_nocreate.uanalyst_group_no_create_new_partner'):
                raise ValidationError(_('You do not have the authority to create a new record'))
        return super(ResPartner, self).create(vals_list)
