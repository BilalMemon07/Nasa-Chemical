from odoo import fields, models, api

class ProductCategoryInherited(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', string = 'Companies', default=lambda self: self.env.company)

