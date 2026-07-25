from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AutonomoActivity(models.Model):
    _name = "autonomo.activity"
    _description = "Actividad economica del autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "company_id, code"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    activity_kind = fields.Selection(
        [("business", "Empresarial"), ("professional", "Profesional")],
        required=True,
        default="business",
        tracking=True,
    )
    iae_code = fields.Char(string="Epigrafe IAE")
    cnae_code = fields.Char(string="Codigo CNAE")
    start_date = fields.Date()
    end_date = fields.Date()
    irpf_estimation_method = fields.Selection(
        [
            ("direct_simplified", "Estimacion directa simplificada"),
            ("direct_normal", "Estimacion directa normal"),
            ("objective", "Estimacion objetiva"),
        ],
        required=True,
        default="direct_simplified",
    )
    vat_regime = fields.Selection(
        [
            ("general", "General"),
            ("cash_criterion", "Criterio de caja"),
            ("simplified", "Simplificado"),
            ("exempt", "Exento"),
            ("other", "Otro"),
        ],
        required=True,
        default="general",
    )
    default_income_account_id = fields.Many2one("account.account", check_company=True)
    default_expense_account_id = fields.Many2one("account.account", check_company=True)
    default_sale_tax_ids = fields.Many2many("account.tax", "autonomo_activity_sale_tax_rel", check_company=True)
    default_purchase_tax_ids = fields.Many2many("account.tax", "autonomo_activity_purchase_tax_rel", check_company=True)
    default_withholding_tax_id = fields.Many2one("account.tax", check_company=True)
    vat_deductible_default_percent = fields.Float(default=100.0)
    activity_address_partner_id = fields.Many2one("res.partner", check_company=True)
    tax_office_code = fields.Char()
    social_security_activity_code = fields.Char()
    legal_source_ids = fields.Many2many("autonomo.legal.source", string="Fuentes oficiales")
    notes = fields.Text()
    active = fields.Boolean(default=True)

    _code_company_uniq = models.Constraint(
        "UNIQUE(company_id, code)",
        "El codigo de actividad debe ser unico por empresa.",
    )

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

    @api.constrains("vat_deductible_default_percent")
    def _check_vat_percent(self):
        for record in self:
            if record.vat_deductible_default_percent < 0 or record.vat_deductible_default_percent > 100:
                raise ValidationError("El porcentaje de IVA deducible debe estar entre 0 y 100.")
