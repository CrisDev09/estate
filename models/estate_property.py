# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta
from odoo import fields, models


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
    
    name = fields.Char(string='Title',required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Availabel From',copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price',required=True)
    selling_price = fields.Float(string='Selling Price',readonly=True, copy=False)
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
    salesperson_id = fields.Many2one("res.partner", string="Salesperson")
    buyer_id = fields.Many2one("res.user", string="Buyer")