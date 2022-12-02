# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import warnings
from odoo.exceptions import UserError, ValidationError

from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False,
                                    default=lambda self: fields.Date.today() + datetime.timedelta(90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(compute="_selling_price", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area_sqm = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean()
    garden = fields.Boolean(default=False)
    garden_area_sqm = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        selection=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')]
    )
    active = fields.Boolean(string="Available", default=True)
    state = fields.Selection(string="Status",
                             selection=[('new', 'New'), ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             default="new"
                             )
    property_type_id = fields.Many2one("estate.property.type", string="Property Types")
    user_id = fields.Many2one('res.users', string="Salesman", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, compute="_accepted_buyer")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(default=0, compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Float(compute="_highest_price", string="Best Offer")
    property_id = fields.Many2one("estate.property.type")
    available = fields.Boolean(string="Available", default="True")

    _sql_constraints = [
        ('positive_price2', 'CHECK(expected_price >= 0)', "Prices must not be a negative number")
    ]

    @api.depends("garden_area_sqm", "living_area_sqm")
    def _compute_total(self):
        for rec in self:
            rec.total_area = False
            if rec.garden_area_sqm:
                rec.total_area = rec.living_area_sqm + rec.garden_area_sqm

    @api.depends("offer_ids")
    def _highest_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0

    @api.depends("offer_ids")
    def _selling_price(self):
        for rec in self:
            accepted_offers = rec.offer_ids.filtered(lambda x: x.status == 'accepted')
            if len(accepted_offers.ids) > 1:
                raise ValidationError("An offer has already been accepted! Only one offer can be accepted. Please "
                                      "refuse the existing offer to accept a new one.")
            elif len(accepted_offers.ids) == 1:
                accepted_offer = accepted_offers[0]
                rec.state = "offer accepted"
                rec.selling_price = accepted_offer.price
            else:
                rec.selling_price = 0.0

    @api.depends("offer_ids")
    def _accepted_buyer(self):
        for rec in self:
            accepted_offers = rec.offer_ids.filtered(lambda x: x.status == 'accepted')
            if len(accepted_offers.ids) >= 1:
                accepted_offer = accepted_offers[0]
                rec.buyer_id = accepted_offer.partner_id.id
            else:
                rec.buyer_id = ''

    @api.onchange("garden")
    def onchange_garden(self):
        if self.garden:
            self.garden_area_sqm = 10
            self.garden_orientation = "north"
        else:
            self.garden_area_sqm = 0
            self.garden_orientation = ''

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price < rec.expected_price * 0.9:
                raise ValidationError("Selling price must not be less than 90% of the Expected Price")

    def sold(self):
        for rec in self:
            if rec.state != 'cancelled' or rec.state == 'offer accepted':
                rec.state = 'sold'
            else:
                raise UserError("Cancelled properties cannot be sold!")

    def cancelled(self):
        for rec in self:
            if rec.state != 'cancelled':
                rec.state = 'cancelled'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_status_new(self):
        for rec in self:
            if rec.state != 'new' or rec.state != 'cancelled':
                raise UserError("Only new and cancelled properties can be deleted")



