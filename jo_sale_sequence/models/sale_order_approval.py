from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    drawing_approved_by_customer = fields.Boolean(string='Drawing Approved by Customer?')
    approved_for_dispatch = fields.Boolean(string='Approved for Dispatch?')

    def action_confirm(self):
        for record in self:
            if not record.drawing_approved_by_customer:
                raise ValidationError(
                    "Drawing Approved  is not approved by customer, couldn't confirm the Sales Order."
                )
        return super().action_confirm()