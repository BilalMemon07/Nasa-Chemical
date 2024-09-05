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
    date_due = fields.Datetime('Date Due', required = True)
  

    # @api.depends('product_id')
    # def _compute_stock_level(self):
        
    #     for rec in self:
    #         order = self.env['stock.warehouse.orderpoint'].search([('product_id', '=', rec.product_id.id)])    
    #         if order:    
    #             rec['minimum_stock_level'] = order.product_min_qty

class QualityPoints(models.Model):
    _inherit = 'quality.point'
    
    methods = fields.Char(string="Methods")
    quality_parameters = fields.Selection([('physical','Physical Property'),('chemical','Chemical Property')])

class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    purchase_tolerance = fields.Float('Purchase Tolerance(%)')
    


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
