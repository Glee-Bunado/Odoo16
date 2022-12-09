from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "name"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property types must be unique')
    ]

    name = fields.Char(string="Property Types", required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_total_offers", string="Offers")



    @api.depends("offer_ids")
    def _total_offers(self):

        for rec in self:
            accepted_offers = rec.offer_ids.mapped("status")
            rec.offer_count = int(len(accepted_offers))

