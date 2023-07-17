from datetime import timedelta
from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Otras ofertas'

    price = fields.Float()
    status = fields.Selection(string="Status", selection=[('accepted', 'Aceptado'), ('refused', 'Rechazado')], readonly=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    create_date = fields.Date(default=fields.Date.today())
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'El precio debe ser un porcentage positivo')
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity) if offer.create_date else False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.create_date = offer.date_deadline - timedelta(days=offer.validity)
            else:
                offer.create_date = False

    def action_confirm(self):
        for record in self:
            if record.status != 'accepted':
                record.status = 'accepted'
    

    def action_cancel(self):
        for record in self:
            record.status = 'refused'
