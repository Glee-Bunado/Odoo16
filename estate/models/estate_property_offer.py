from odoo import fields, models, api
import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Model"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status",
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one("res.partner",  required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_validity_date")
    created_date = fields.Date(default=lambda self: fields.Date.today())

    @api.depends("created_date", "validity")
    def _validity_date(self):
        for rec in self:
            rec.date_deadline = False
            if rec.created_date:
                rec.date_deadline = datetime.timedelta(rec.validity) - rec.created_date





