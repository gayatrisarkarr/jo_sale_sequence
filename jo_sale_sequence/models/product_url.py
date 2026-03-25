from odoo import models, fields, api


class ProductProductUrl(models.Model):
    _inherit = "product.product"

    product_url = fields.Char(string='Product URL')

    # ADD AFTER ABOVE ↓
    product_url_link = fields.Html(
        compute='_compute_url_link',
        string='Product URL'
    )

    @api.depends('product_url')
    def _compute_url_link(self):
        for rec in self:
            if rec.product_url:
                rec.product_url_link = f'<a href="{rec.product_url}" target="_blank">Product Details</a>'
            else:
                rec.product_url_link = ''



# from odoo import models, fields , api
#
# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#
#     product_url = fields.Char(string='Product URL')
#     product_url_link = fields.Html(
#         compute= 'compute_url_link',
#         string='Product URL'
#     )
#
#     # @api.depends('product_url')
#     # def_compute_url_link(self):
#     #    for rec on self ;
#     #        if rec.product.url = f'<a href="