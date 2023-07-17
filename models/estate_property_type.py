from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipo de mobiliario'

    name = fields.Char(string='Tipo', required=True)
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'Ya existe un registro con el mismo nombre')
    ]
