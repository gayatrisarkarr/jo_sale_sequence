from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Joflo Check List fields
    is_bg_submitted = fields.Boolean(string='Is BG Submitted?')
    bg_submitted_date = fields.Date(string='BG Submitted Date')
    bg_expiry_date = fields.Date(string='BG Expiry Date')
    is_retention_money_released = fields.Boolean(string='Is Retention Money Released?')
    bg_received_from_customer = fields.Boolean(string='BG Received from Customer?')