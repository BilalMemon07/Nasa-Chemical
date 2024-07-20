from odoo import _, api, fields, models


class POReportWizard(models.TransientModel):
    _name = 'po.report'
    _description = 'Purchase Order Report'
    
  
    def print_report(self):
        return self.env.ref('po_report.po_report_pdf').with_context(landscape=True).report_action(self)