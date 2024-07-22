from odoo import _, api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = 'purchase.report'
    _description = 'Purchase Report'
    
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)
    product_ids = fields.Many2many('product.template', string='Product', required=True)
    vendor = fields.Char(string = "Vendor", required=True)
    po_no = fields.Char(string = "po_no", required=True)
    grn = fields.Char(string = "grn", required=True)
    invoice_no = fields.Char(string = "invoice_no", required=True)
    

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
            'invoice_no': self.invoice_no
            }

        return self.env.ref('purchase_report.purchase_report_pdf').with_context(landscape=True).report_action(self, data=data)