from odoo import models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for record in self:
            # get linked sale order
            sale_order = record.sale_id
            if sale_order and not sale_order.approved_for_dispatch:
                raise ValidationError(
                    "This product is not ready for dispatch. Please aprrove for dispatch on Sales Order page."
                )
        return super().button_validate()