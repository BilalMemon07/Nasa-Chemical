from odoo import fields, models, api
from odoo.exceptions import UserError
from num2words import num2words

# class ProductCategoryInherited(models.Model):
#     _inherit = 'product.category'

#     company_id = fields.Many2one('res.company', string = 'Companies', default=lambda self: self.env.company)

class PurchaseRerquestLineInherited(models.Model):
    _inherit = 'purchase.request.line'

    minimum_stock_level = fields.Float('Minimum Stock Level')
    forecasting_stock = fields.Float('Forecasting Stock')
    on_hand_qty = fields.Flaot('On Hand Quantity')
    

class PurchaseRerquestInherited(models.Model):
    _inherit = 'purchase.request'

    department = fields.Char('Department', compute = "get_department")
    date_due = fields.Datetime('Date Due', required = True)
  

    @api.depends('requested_by')
    def get_department(self):
        
        for rec in self:
            rec['department'] = ""
            if rec.requested_by:
                rec['department'] = rec.requested_by.department_id.name
                
class QualityPoints(models.Model):
    _inherit = 'quality.point'
    
    methods = fields.Char(string="Methods")
    quality_parameters = fields.Selection([('physical','Physical Property'),('chemical','Chemical Property')])

class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    purchase_tolerance = fields.Float('Purchase Tolerance(%)', default=10.00)
    


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    amount_in_words = fields.Char(string='Amount in Words', compute='_compute_amount_in_words')
    
    @api.depends('amount_total')
    def _compute_amount_in_words(self):
        for payment in self:
            if payment.amount_total:
                payment.amount_in_words = num2words(payment.amount_total, lang='en').title()
            else:
                payment.amount_in_words = ''


class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    # Override the write method to check purchase tolerance before saving the record
    @api.model
    def write(self, vals):
        # Loop through each record in self (to handle multi-records)
        res =  super(StockPickingInherited, self).write(vals)
        high_perc_qty = 0
        low_perc_qty = 0
        for rec in self:
            for line in rec.move_ids_without_package:
                if line.quantity and line.product_uom_qty:
                    
                    high_perc_qty =  line.product_uom_qty + ((line.product_uom_qty * line.product_id.purchase_tolerance) / 100) 
                    low_perc_qty =  line.product_uom_qty - ((line.product_uom_qty * line.product_id.purchase_tolerance) / 100 )
                    
                    # raise UserError(str(high_perc_qty))
                    # or line.quantity < low_perc_qty:
                    
                if line.quantity > high_perc_qty or line.quantity < low_perc_qty:
                    raise UserError('You have violated the purchase tolerance limit')

        # Proceed with the default write behavior after the checks
        return res


# Purchase Tolerance Automated Action
# class StockPickingInherited(models.Model):
#     _inherit = 'stock.picking'

#     def getquantity(self):
#         for rec in self:
#             high_perc_qty = 0
#             low_perc_qty = 0
#             for line in rec.move_ids_without_package:
                
#                 if line.quantity and line.product_uom_qty:
#                     high_perc_qty = high_perc_qty + line.product_uom_qty + ((line.product_uom_qty * line.product_id.purchase_tolerance / 100) )
#                     low_perc_qty = low_perc_qty + line.product_uom_qty - ((line.product_uom_qty * line.product_id.purchase_tolerance / 100) )
#                 if line.quantity > high_perc_qty or line.quantity < low_perc_qty:
                    
#                     raise UserError('You have violated the purchase tolerance limit')
        
    