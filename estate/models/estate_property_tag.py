from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(string="Name")
    color = fields.Integer()
