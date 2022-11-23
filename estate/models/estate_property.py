# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime

from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False,
                                    default=lambda self: fields.Date.today() + datetime.timedelta(90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area_sqm = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area_sqm = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer Received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default="new"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Types")
    user_id = fields.Many2one('res.users', string="Salesman", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Name")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(default=0, compute="_compute_total", string="Total Area (sqm)")

    @api.depends("garden_area_sqm", "living_area_sqm")
    def _compute_total(self):
        for rec in self:
            rec.total_area = False
            if rec.garden_area_sqm:
                rec.total_area = rec.living_area_sqm + rec.garden_area_sqm
