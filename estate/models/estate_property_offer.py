from odoo import fields, models, api
import datetime
from odoo.exceptions import UserError
from datetime import date

from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Model"
    _order = "price desc"
    _sql_constraints = [
        ('positive_price', 'CHECK(price >= 0)', "Prices must not be a negative number")
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status",
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')],
                              default='pending')
    partner_id = fields.Many2one("res.partner",  required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_validity_date", inverse="_inverse_validity_date")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)



    @api.depends("validity")
    def _validity_date(self):
        for rec in self:
            created_date = fields.Date.today()
            # rec.date_deadline = False
            if rec.validity:
                rec.date_deadline = datetime.timedelta(rec.validity) + created_date

    def _inverse_validity_date(self):
        for rec in self:
            if rec.date_deadline:
                d1 = date(rec.date_deadline.year, rec.date_deadline.month, rec.date_deadline.day)
                d2 = date(fields.Date.today().year, fields.Date.today().month, fields.Date.today().day)
                rec.validity = (d1 - d2).days

    def accept_offer(self):
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "status": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def refuse_offer(self):
        return self.write(
            {
                "status": "refused",
            }
        )
    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer received"
        return super().create(vals)
    #



