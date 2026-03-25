from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hsn_sac_code = fields.Char(string='HSN/SAC', size=8)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    hsn_sac_code = fields.Char(string='HSN/SAC', size=8)

    @api.onchange('product_id')
    def _onchange_product_hsn(self):
        if self.product_id:
            self.hsn_sac_code = self.product_id.hsn_sac_code or False