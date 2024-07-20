from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.po_report.po_reports"
    _description = "Purchase Order Report"

    def _get_report_values(self, docids, data=None):
        query = ("""
                SELECT 
                    po.date_order AS Date,
                    pol.name AS Item,
                    po.origin as ReqNo,
                    po.name AS PONo,
                    sp.name AS GRN,
                    am.name AS InvoiceNo,
                    pol.product_qty AS Orderqty,
                    pol.qty_received AS Recievedqty,
                    (pol.product_qty - pol.qty_invoiced) AS Balanceqty,
                    mm.name ->> 'en_US'  AS Unit,
                    pol.price_unit AS Price, 
                    pol.price_total AS Amount,
                    sw.name as Location
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

        
