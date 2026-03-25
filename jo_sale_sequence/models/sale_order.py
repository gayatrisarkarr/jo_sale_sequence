from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class ProjectProject(models.Model):
    _inherit = 'project.project'

    wo_standard = fields.Boolean(string='WO - Standard')
    wo_spares_repair = fields.Boolean(string='WO - Spares & Repair')
    wo_forecasting = fields.Boolean(string='WO - Forecasting')
    wo_id = fields.Char(string='WO ID')

    def _generate_wo_id(self):
        yy = str(date.today().year)[2:]

        if self.wo_standard:
            prefix = f'JVC {yy}'
            last = self.search([
                ('wo_id', 'like', f'{prefix}%'),
                ('id', '!=', self.id if self.id else 0),
            ], order='wo_id desc', limit=1)
            if last and last.wo_id:
                try:
                    num = int(last.wo_id.replace(prefix, '').strip()) + 1
                except ValueError:
                    num = 1
            else:
                num = 1
            return f'{prefix}{str(num).zfill(3)}'

        elif self.wo_spares_repair:
            prefix = f'{yy}/S&R/'
            last = self.search([
                ('wo_id', 'like', f'{prefix}%'),
                ('id', '!=', self.id if self.id else 0),
            ], order='wo_id desc', limit=1)
            if last and last.wo_id:
                try:
                    num = int(last.wo_id.split('/')[-1]) + 1
                except ValueError:
                    num = 1
            else:
                num = 1
            return f'{prefix}{str(num).zfill(3)}'

        elif self.wo_forecasting:
            last = self.search([
                ('wo_id', 'like', 'F%'),
                ('id', '!=', self.id if self.id else 0),
            ], order='wo_id desc', limit=1)
            if last and last.wo_id:
                try:
                    num = int(last.wo_id[1:]) + 1
                except ValueError:
                    num = 1
            else:
                num = 1
            return f'F{str(num).zfill(4)}'

        return False

    @api.onchange('wo_standard', 'wo_spares_repair', 'wo_forecasting')
    def _onchange_wo_type(self):
        # Figure out which field just got turned ON
        # by checking which one triggered (last changed = True)
        # Reset all others and set wo_id accordingly
        if self.wo_standard:
            self.wo_spares_repair = False
            self.wo_forecasting = False
        elif self.wo_spares_repair:
            self.wo_standard = False
            self.wo_forecasting = False
        elif self.wo_forecasting:
            self.wo_standard = False
            self.wo_spares_repair = False

        # Always recalculate wo_id based on current state
        if self.wo_standard or self.wo_spares_repair or self.wo_forecasting:
            self.wo_id = '/'  # placeholder; real ID assigned on create
        else:
            self.wo_id = False

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Always generate fresh from DB on actual save
            wo_id = record._generate_wo_id()
            if wo_id:
                record.wo_id = wo_id
            else:
                record.wo_id = False
        return records