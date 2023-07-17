from odoo import fields, models 

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Etiqueta de propiedad'

    name = fields.Char(string = "Etiqueta de propiedad", required = True)
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'Ya existe un registro con el mismo nombre')
    ]