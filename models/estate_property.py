# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import UserError
from datetime import timedelta
from odoo import api, fields, models


#Los modelos se definen en odoo como una clase de python 
#Donde es el _name no debe faltar o quedar vacios
#Al igual que _description
'''
_name ==> es el nombre del modelo. Es el nombre por el cual se podra instanciar desde cualquier parte 
_description ==> es el nombre que se mostrara en la vista cuando se muestre en la interfaz de odoo

luego definimos los campos que queremos que se agregue a nuestra base de datos 
ejemplo:
name = fields.Char(string='Title',required=True)
etc.

Nuestro modelo representa la tabla de nuestra base de datos
'''
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Propiedad Inmobiliaria"
    
    status = fields.Char(string="Estado", default="Nuevo" ,readonly=True)
    name = fields.Char(string='Title',required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Availabel From',copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price',required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False, compute="_compute_b_price")
    bedrooms = fields.Integer(string='Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    active = fields.Boolean(string='Active')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    buyer_id = fields.Many2one("res.partner", string="Buyer", compute="_parner_buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.Many2many("estate.property.offer")
    total_area  = fields.Float(compute="_compute_area")
    best_price = fields.Float(compute="_compute_price")
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'El precio debe ser un porcentage positivo')
    ]


    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids.mapped('price') else 0.0


    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("No se puede cancelar una propiedad vendida.")
            record.status = 'canceled'

    def action_sold(self):
        for record in self:
            if record.status == 'canceled':
                raise UserError("No se puede marcar como vendida una propiedad cancelada.")
            record.status = 'sold'

    @api.depends('offer_ids.status', 'offer_ids.price')
    def _compute_b_price(self):
        for record in self:
            accepted_offers = record.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            record.selling_price = max(accepted_offers.mapped('price')) if accepted_offers else 0.0

    @api.depends('offer_ids.partner_id', 'offer_ids.status')
    def _parner_buyer(self):
        for record in self:
            accepted_offers = record.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            record.buyer_id = accepted_offers[0].partner_id if accepted_offers else False
