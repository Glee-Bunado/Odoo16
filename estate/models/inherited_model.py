from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = "inherited.user"

    property_ids = fields.One2many("estate.property")