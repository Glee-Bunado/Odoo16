from odoo import fields, models, api
import datetime
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Model"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status",
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')],
                              default='pending')
    partner_id = fields.Many2one("res.partner",  required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_validity_date", inverse="_inverse_validity_date")

    _sql_constraints = [
        ('positive_price', 'CHECK(price >= 0)', "Prices must not be a negative number")
    ]

    @api.depends("validity")
    def _validity_date(self):
        for rec in self:
            created_date = fields.Date.today()
            # rec.date_deadline = False
            if rec.validity:
                rec.date_deadline = datetime.timedelta(rec.validity) + created_date

    def _inverse_validity_date(self):
        for rec in self:
            created_date = fields.Date.today()
            if rec.date_deadline:
                rec.validity = rec.date_deadline.day - created_date.day

    def accept_offer(self):
        for rec in self:
            if rec.status == 'pending' or rec.status == 'refused':
                rec.status = 'accepted'

    def refuse_offer(self):
        for rec in self:
            if rec.status == 'pending' or rec.status == 'accepted':
                rec.status = 'refused'







