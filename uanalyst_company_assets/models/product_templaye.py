# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uanalyst_company_asset = fields.Boolean(string="Company Assets", default=True)



