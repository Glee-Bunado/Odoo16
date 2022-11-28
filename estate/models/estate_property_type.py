from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(string="Property Types", required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property types must be unique')
    ]