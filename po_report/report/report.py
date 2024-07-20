from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.po_report.po_reports"
    _description = "Purchase Order Report"


    def _get_report_values(self, docids, data=None):
        
    #     product_ids = fields.Many2many('product.template', string='Product', required=True)
    # warehouse_id = fields.Many2one('stock.warehouse', string = "Ware House")
    # vendor = fields.Char(string = "Vendor")
    # po_no = fields.Char(string = "po_no")
    # grn = fields.Char(string = "grn")
    # invoice_no = fields.Char(string = "invoice_no")
    # pr_no = fields.Char(string = "pr_no")

        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        product_ids = data['product_ids']
        warehouse_id = data['warehouse_id']
        vendor = data['vendor']
        po_no = data['po_no']
        grn = data['grn']
        invoice_no = data['invoice_no']
        pr_no = data['pr_no']


        other_details.update({
                'from_date': date_from,
                'to_date': date_to,
                'product_ids': product_ids,
                'warehouse_id': warehouse_id,
                'vendor': vendor,
                'po_no': po_no,
                'grn': grn,
                'invoice_no': invoice_no,
                'pr_no' : pr_no
            })
        
        if product_ids != []:
            product_ids_str = ','.join(map(str,product_ids))

        cr = self._cr
        query = ("""
                SELECT 
                    po.date_order AS date,
                    po.partner_ref AS vendor,
                    pt.name ->> 'en_US' AS item,
                    po.origin as prno,
                    po.name AS pono,
                    sp.name AS grn,
                    am.name AS invoiceno,
                    pol.product_qty AS orderqty,
                    pol.qty_received AS recievedqty,
                    (pol.product_qty - pol.qty_invoiced) AS balanceqty,
                    mm.name ->> 'en_US' AS unit,
                    pol.price_unit AS price, 
                    pol.price_total AS amount,
                    sw.name as location
                FROM purchase_order_line pol 
                INNER JOIN purchase_order po ON po.id = pol.order_id
                inner JOIN product_product pp ON pp.id = pol.product_id
                inner JOIN product_template pt ON pt.id = pp.product_tmpl_id
                Left JOIN stock_picking sp ON sp.origin = po.name   
                Left JOIN account_move am ON am.invoice_origin = po.name
                inner join stock_picking_type spt on spt.id = po.picking_type_id
                inner join stock_warehouse sw on sw.id = spt.warehouse_id
                inner join uom_uom mm on mm.id = pol.product_uom
                WHERE 
                    po.date_order BETWEEN '%s' AND '%s'
                    AND pt.id in (%s)
                    AND spt.warehouse_id = %s
                    AND po.partner_ref = '%s'
                    AND po.name = '%s'
                    AND sp.name = '%s'
                    AND am.name = '%s'
                    AND po.origin = '%s'
                order by po.name
                
                """
        
        % (date_from, date_to,product_ids_str,warehouse_id, vendor, po_no, grn, invoice_no, pr_no) )
        #  % (date_from,date_to)
# ,category_ids,stock_location_id
        cr.execute(query)
        data = cr.dictfetchall()

        return {
            'doc_ids': docids,
            'data': data,
            'other': other_details,
        }

         
#         Item Wise
# Vendor Wise
# Warehouse Wise
# PO No
# GRN
# Requisation No
# Invoice No

     
        # cr.execute(query)
        # result = cr.dictfetchall()

        # # raise UserError(str(result))
        
        # return {
        #     'data': result,
        # }

        
