from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tax_subject_kind = fields.Selection(
        [
            ("individual", "Persona fisica"),
            ("self_employed", "Autonomo"),
            ("company", "Sociedad"),
            ("public_body", "Administracion publica"),
            ("other", "Otro"),
        ],
        string="Tipo de sujeto fiscal",
        default="individual",
    )
    e_invoice_required = fields.Boolean(string="Factura electronica requerida")
    e_invoice_channel = fields.Selection([("face", "FACe"), ("private_platform", "Plataforma privada"), ("email", "Email"), ("other", "Otro")], string="Canal factura electronica")
    e_invoice_endpoint = fields.Char(string="Destino factura electronica")
    privacy_alias = fields.Char(string="Alias de privacidad")
    tax_data_verified_at = fields.Datetime(string="Datos fiscales verificados")
