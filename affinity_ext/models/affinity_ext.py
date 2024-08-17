from odoo import fields, models, api


class ResPartnerInherited(models.Model):
    _inherit = "res.partner"

    legal_status = fields.Selection([('individual', 'Individual'), ('partnership', 'Partnership'), ('aop', 'AOP'), ('company', 'Company')], required = True)
    company_reg = fields.Char("Company Registration", required = True)
    artical = fields.Char("Article of Association and Memorandom", required = True)
    strn_no = fields.Char("STRN", required = True)
    cnic_no = fields.Char("CNIC Number", required = True)
    vendor_status = fields.Selection([('active', 'Active'), ('non_active', 'Non Active')], string = "Vendor Status")
    