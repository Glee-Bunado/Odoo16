from odoo import fields, models
from custom.estate.models import estate_property


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def sold(self):
        print("--------------------------------I am an inherited function")
        super(InheritedEstateProperty, self).sold()
