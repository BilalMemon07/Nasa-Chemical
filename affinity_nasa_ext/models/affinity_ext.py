from odoo import fields, models, api

class ProductCategoryInherited(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', string = 'Companies', default=lambda self: self.env.company)

class PurchaseRerquestLineInherited(models.Model):
    _inherit = 'purchase.request.line'

    minimum_stock_level = fields.Char('Minimum Stock Level')
    forcasting_stock = fields.Char('Forcasting Stock')
    date_due = fields.Datetime('Date Due')

    

    @api.depends('product_id')
    def _compute_stock_level(self):
        for rec in self:
            order = self.env['stock.warehouse.orderpoint'].search([('product_id', '=', rec.product_id)])
            rec['minimum_stock_level'] = order.product_min_qty