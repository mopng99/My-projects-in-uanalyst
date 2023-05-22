# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('import_file'):
            self._check_import_consistency(vals_list)
        for vals in vals_list:
            if not vals.get('category_id'):
                partner_tag = self.env['res.partner.category'].browse(1).default_tag
                vals['category_id'] = partner_tag
                print("partner_tag", partner_tag)
            if vals.get('website'):
                vals['website'] = self._clean_website(vals['website'])
            if vals.get('parent_id'):
                vals['company_name'] = False
        partners = super(ResPartner, self).create(vals_list)

        if self.env.context.get('_partners_skip_fields_sync'):
            return partners

        for partner, vals in zip(partners, vals_list):
            partner._fields_sync(vals)
            # Lang: propagate from parent if no value was given
            if 'lang' not in vals and partner.parent_id:
                partner._onchange_parent_id_for_lang()
            partner._handle_first_contact_creation()
        return partners