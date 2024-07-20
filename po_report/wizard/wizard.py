from odoo import _, api, fields, models


class POReportWizard(models.TransientModel):
    _name = 'po.report'
    _description = 'Purchase Order Report'
    
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)
    product_ids = fields.Many2many('product.template', string='Product', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string = "Ware House", required=True)
    vendor = fields.Char(string = "Vendor", required=True)
    po_no = fields.Char(string = "po_no", required=True)
    grn = fields.Char(string = "grn", required=True)
    invoice_no = fields.Char(string = "invoice_no", required=True)
    pr_no = fields.Char(string = "pr_no", required=True)

    

    def print_report(self):

        product_ids = []
        if self.product_ids:
            for id in self.product_ids:
                product_ids.append(id.id)
        
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'product_ids': product_ids,
            'warehouse_id': self.warehouse_id.id,
            'vendor': self.vendor,
            'po_no': self.po_no,
            'grn': self.grn,
            'invoice_no': self.invoice_no,
            'pr_no' : self.pr_no
            }

        return self.env.ref('po_report.po_report_pdf').with_context(landscape=True).report_action(self, data=data)