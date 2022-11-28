from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "name"

    name = fields.Char(string="Property Types", required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_id")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property types must be unique')
    ]