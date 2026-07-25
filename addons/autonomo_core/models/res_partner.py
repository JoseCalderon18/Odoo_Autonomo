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
        default="individual",
    )
    e_invoice_required = fields.Boolean()
    e_invoice_channel = fields.Selection([("face", "FACe"), ("private_platform", "Plataforma privada"), ("email", "Email"), ("other", "Otro")])
    e_invoice_endpoint = fields.Char()
    privacy_alias = fields.Char()
    tax_data_verified_at = fields.Datetime()
