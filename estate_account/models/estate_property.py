from odoo import fields, models
from odoo.fields import Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def sold(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        account_move = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids':[
                Command.create({
                    "name": self.name,
                    "quantity": 1.0,
                    "price_unit":0.6 * self.selling_price,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1.0,
                    "price_unit": 100.0
                })
            ]
        })


        print("--------------------------------I am an inherited function")
        super(InheritedEstateProperty, self).sold()
