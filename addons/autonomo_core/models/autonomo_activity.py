from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AutonomoActivity(models.Model):
    _name = "autonomo.activity"
    _description = "Actividad economica del autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "company_id, code"

    name = fields.Char(string="Nombre", required=True, tracking=True)
    code = fields.Char(string="Codigo", required=True, tracking=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company, index=True)
    activity_kind = fields.Selection(
        [("business", "Empresarial"), ("professional", "Profesional")],
        string="Tipo de actividad",
        required=True,
        default="business",
        tracking=True,
    )
    iae_code = fields.Char(string="Epigrafe IAE")
    cnae_code = fields.Char(string="Codigo CNAE")
    start_date = fields.Date(string="Fecha de inicio")
    end_date = fields.Date(string="Fecha de fin")
    irpf_estimation_method = fields.Selection(
        [
            ("direct_simplified", "Estimacion directa simplificada"),
            ("direct_normal", "Estimacion directa normal"),
            ("objective", "Estimacion objetiva"),
        ],
        string="Metodo de estimacion IRPF",
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
        string="Regimen de IVA",
        required=True,
        default="general",
    )
    default_income_account_id = fields.Many2one("account.account", string="Cuenta de ingresos por defecto", check_company=True)
    default_expense_account_id = fields.Many2one("account.account", string="Cuenta de gastos por defecto", check_company=True)
    default_sale_tax_ids = fields.Many2many("account.tax", "autonomo_activity_sale_tax_rel", string="Impuestos de venta por defecto", check_company=True)
    default_purchase_tax_ids = fields.Many2many("account.tax", "autonomo_activity_purchase_tax_rel", string="Impuestos de compra por defecto", check_company=True)
    default_withholding_tax_id = fields.Many2one("account.tax", string="Retencion por defecto", check_company=True)
    vat_deductible_default_percent = fields.Float(string="IVA deducible por defecto (%)", default=100.0)
    activity_address_partner_id = fields.Many2one("res.partner", string="Direccion de actividad", check_company=True)
    tax_office_code = fields.Char(string="Codigo de administracion tributaria")
    social_security_activity_code = fields.Char(string="Codigo actividad Seguridad Social")
    legal_source_ids = fields.Many2many("autonomo.legal.source", string="Fuentes oficiales")
    notes = fields.Text(string="Notas")
    active = fields.Boolean(string="Activo", default=True)

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
