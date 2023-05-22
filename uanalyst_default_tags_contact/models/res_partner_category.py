# -*- coding: utf-8 -*-
from datetime import date

from odoo import api, models, fields, _


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    default_tag = fields.Many2one('res.partner.category', string="Default Tag", store=True)
