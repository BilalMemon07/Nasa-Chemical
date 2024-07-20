from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.po_report.po_reports"
    _description = "Purchase Order Report"

    def _get_report_values(self, docids, data=None):
        query = ("""
                SELECT 
                    po.date_order AS date,
                    pol.name AS item,
                    po.origin as reqno,
                    po.name AS pono,
                    sp.name AS grn,
                    am.name AS invoiceno,
                    pol.product_qty AS orderqty,
                    pol.qty_received AS recievedqty,
                    (pol.product_qty - pol.qty_invoiced) AS balanceqty,
                    mm.name ->> 'en_US'  AS unit,
                    pol.price_unit AS price, 
                    pol.price_total AS amount,
                    sw.name as location
                FROM purchase_order_line pol 
                INNER JOIN purchase_order po ON po.id = pol.order_id
                Left JOIN stock_picking sp ON sp.origin = po.name   
                Left JOIN account_move am ON am.invoice_origin = po.name
                inner join stock_picking_type spt on spt.id = po.picking_type_id
                inner join stock_warehouse sw on sw.id = spt.warehouse_id
                inner join uom_uom mm on mm.id = pol.product_uom
                order by po.name
    """
                        ) 
     
        cr = self._cr
        cr.execute(query)
        result = cr.dictfetchall()

        # raise UserError(str(result))
        
        return {
            'data': result,
        }

        
