from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold(self):
        print("--------------------------------I am an inherited function")
        return super().sold()
