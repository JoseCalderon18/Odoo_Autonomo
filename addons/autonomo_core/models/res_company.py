from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    is_self_employed = fields.Boolean(string="Persona autonoma")
    owner_partner_id = fields.Many2one("res.partner", string="Titular", check_company=True)
    fiscal_start_date = fields.Date()
    default_activity_id = fields.Many2one("autonomo.activity", check_company=True)
    irpf_estimation_method = fields.Selection(
        [
            ("direct_simplified", "Estimacion directa simplificada"),
            ("direct_normal", "Estimacion directa normal"),
            ("objective", "Estimacion objetiva"),
        ],
        default="direct_simplified",
    )
    default_vat_regime = fields.Selection(
        [
            ("general", "General"),
            ("cash_criterion", "Criterio de caja"),
            ("simplified", "Simplificado"),
            ("exempt", "Exento"),
            ("other", "Otro"),
        ],
        default="general",
    )
    tax_authority = fields.Selection([("aeat", "Agencia Tributaria"), ("foral", "Hacienda foral"), ("other", "Otra")], default="aeat")
    reta_start_date = fields.Date()
    external_backup_enabled = fields.Boolean()
    last_verified_backup_at = fields.Datetime()
    census_profile_id = fields.Many2one("autonomo.census.profile")
    social_security_profile_id = fields.Many2one("autonomo.social.security.profile")
