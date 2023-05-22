# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.user.has_group('uanalyst_groups_nocreate.uanalyst_group_no_create_new_product'):
                raise ValidationError(_('You do not have the authority to create a new record'))
        return super(ProductTemplate, self).create(vals_list)
