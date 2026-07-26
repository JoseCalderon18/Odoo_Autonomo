from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    is_self_employed = fields.Boolean(string="Persona autonoma")
    owner_partner_id = fields.Many2one("res.partner", string="Titular", check_company=True)
    fiscal_start_date = fields.Date(string="Fecha de inicio fiscal")
    default_activity_id = fields.Many2one("autonomo.activity", string="Actividad por defecto", check_company=True)
    irpf_estimation_method = fields.Selection(
        [
            ("direct_simplified", "Estimacion directa simplificada"),
            ("direct_normal", "Estimacion directa normal"),
            ("objective", "Estimacion objetiva"),
        ],
        string="Metodo de estimacion IRPF",
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
        string="Regimen de IVA por defecto",
        default="general",
    )
    tax_authority = fields.Selection([("aeat", "Agencia Tributaria"), ("foral", "Hacienda foral"), ("other", "Otra")], string="Administracion tributaria", default="aeat")
    reta_start_date = fields.Date(string="Fecha de alta RETA")
    external_backup_enabled = fields.Boolean(string="Copia externa activada")
    last_verified_backup_at = fields.Datetime(string="Ultima copia verificada")
    census_profile_id = fields.Many2one("autonomo.census.profile", string="Perfil censal")
    social_security_profile_id = fields.Many2one("autonomo.social.security.profile", string="Perfil RETA")
