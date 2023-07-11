from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipo de mobiliario'

    name = fields.Char(string='Tipo', required=True)