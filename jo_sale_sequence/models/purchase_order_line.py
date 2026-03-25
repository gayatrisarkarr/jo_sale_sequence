from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_in_no = fields.Float(string='Qty in No', digits=(16, 2))

    def _get_effective_qty(self):
        """Use product_qty if set, else fall back to qty_in_no."""
        return self.product_qty if self.product_qty else (self.qty_in_no or 0.0)

    def _compute_amount(self):
        # Temporarily swap product_qty with effective qty, then restore
        for line in self:
            original_qty = line.product_qty
            effective_qty = line._get_effective_qty()
            if effective_qty != original_qty:
                line.product_qty = effective_qty
                super(PurchaseOrderLine, line)._compute_amount()
                line.product_qty = original_qty
            else:
                super(PurchaseOrderLine, line)._compute_amount()