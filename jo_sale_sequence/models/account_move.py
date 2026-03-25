from odoo import models, api
from datetime import date


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_fiscal_year_str(self):
        """Returns e.g. '25-26' based on current date."""
        today = date.today()
        if today.month >= 4:
            return f"{str(today.year)[2:]}-{str(today.year + 1)[2:]}"
        else:
            return f"{str(today.year - 1)[2:]}-{str(today.year)[2:]}"

    def _generate_jo_invoice_sequence(self):
        """Generate custom invoice number based on partner GST treatment."""
        self.ensure_one()
        fy = self._get_fiscal_year_str()
        is_sez = (
            self.partner_id
            and self.partner_id.gst_treatment == 'sez'
        )

        if is_sez:
            prefix = f'INV/{fy}/SEZ/'
        else:
            prefix = f'INV/{fy}/'

        # Find last invoice with this prefix (exclude current)
        existing = self.search([
            ('name', 'like', prefix),
            ('move_type', '=', 'out_invoice'),
            ('id', '!=', self.id if self.id else 0),
        ], order='name desc', limit=1)

        if existing:
            last_num = existing.name.split('/')[-1]
            try:
                next_num = int(last_num) + 1
            except ValueError:
                next_num = 1
        else:
            next_num = 1

        return f"{prefix}{str(next_num).zfill(4)}"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.move_type == 'out_invoice' and record.name in ('/', False, 'New'):
                record.name = record._generate_jo_invoice_sequence()
        return records