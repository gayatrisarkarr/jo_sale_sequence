from odoo import models, fields, api
from datetime import date


class ProjectProject(models.Model):
    _inherit = 'project.project'

    wo_type = fields.Selection([
        ('standard', 'WO - Standard'),
        ('spares_repair', 'WO - Spares & Repair'),
        ('forecasting', 'WO - Forecasting'),
    ], string='Work Order Type')

    wo_id = fields.Char(string='WO ID')

    def _generate_wo_id(self):
        yy = str(date.today().year)[2:]

        if self.wo_type == 'standard':
            prefix = f'JVC {yy}'
            last = self.search([
                ('wo_id', 'like', f'{prefix}%'),
                ('id', '!=', self.id if self.id else 0),
            ], order='wo_id desc', limit=1)
            try:
                num = int(last.wo_id.replace(prefix, '').strip()) + 1 if last and last.wo_id else 1
            except ValueError:
                num = 1
            return f'{prefix}{str(num).zfill(3)}'

        elif self.wo_type == 'spares_repair':
            prefix = f'{yy}/S&R/'
            last = self.search([
                ('wo_id', 'like', f'{prefix}%'),
                ('id', '!=', self.id if self.id else 0),
            ], order='wo_id desc', limit=1)
            try:
                num = int(last.wo_id.split('/')[-1]) + 1 if last and last.wo_id else 1
            except ValueError:
                num = 1
            return f'{prefix}{str(num).zfill(3)}'

        elif self.wo_type == 'forecasting':
            last = self.search([
                ('wo_id', 'like', 'F%'),
                ('id', '!=', self.id if self.id else 0),
            ], order='wo_id desc', limit=1)
            try:
                num = int(last.wo_id[1:]) + 1 if last and last.wo_id else 1
            except ValueError:
                num = 1
            return f'F{str(num).zfill(4)}'

        return False

    @api.onchange('wo_type')
    def _onchange_wo_type(self):
        self.wo_id = self._generate_wo_id() or False

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            wo_id = record._generate_wo_id()
            record.wo_id = wo_id if wo_id else False
        return records