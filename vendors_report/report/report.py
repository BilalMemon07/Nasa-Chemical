from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.vendors_report.vendors_reports"
    _description = "Advance to Vendors Report"


    def _get_report_values(self, docids, data=None):
        
        
        other_details = {}
        date_from = data['date_from']
        date_to = data['date_to']
        vendor_ids = data['vendor_ids']
        

        other_details.update({
                'from_date': date_from,
                'to_date': date_to,
                'vendor_ids': vendor_ids,
                
            })
        
        if vendor_ids != []:
            vendor_ids_str = ','.join(map(str,vendor_ids))

        cr = self._cr
        query = ("""
                    SELECT 
                            
                        rs.name as vendor,
                        po.date_order AS podate,
                        po.name as pono,
                        pol.price_total AS poamount,
                        am.date as advdate,
                        
                        am.invoice_date_due as duedate,
                        apt.name ->> 'en_US' as duedays,
                        am.amount_total as advamount,
                        am.amount_residual_signed as pendamount
                    
                        FROM purchase_order_line pol 
                        INNER JOIN purchase_order po ON po.id = pol.order_id
                        inner join res_partner rs on rs.id = po.partner_id
                        Left JOIN stock_picking sp ON sp.origin = po.name   
                        Left JOIN account_move am ON am.invoice_origin = po.name
                        left join account_payment_term apt on apt.id = am.invoice_payment_term_id
                        inner join stock_picking_type spt on spt.id = po.picking_type_id
                        inner join stock_warehouse sw on sw.id = spt.warehouse_id
                        inner join uom_uom mm on mm.id = pol.product_uom

                    WHERE 
                        po.date_order BETWEEN '%s' AND '%s'
                        
                        AND rs.id in (%s)
                        

                    order by po.name
                    
                """
        
        % (date_from, date_to,vendor_ids_str) )

        cr.execute(query)
        data = cr.dictfetchall()

        totals = {
            'total_poamount': sum(item['poamount'] for item in data),
            'total_advamount': sum(item['advamount'] for item in data),
            'total_pendamount': sum(item['pendamount'] for item in data),
            
        }

        return {
            'doc_ids': docids,
            'data': data,
            'totals':totals,
            'other': other_details,
        }


        
