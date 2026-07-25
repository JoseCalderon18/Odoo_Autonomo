from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AutonomoTaxCategory(models.Model):
    _name = "autonomo.tax.category"
    _description = "Categoria fiscal autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "company_id, code"

    code = fields.Char(string="Codigo", required=True)
    name = fields.Char(string="Nombre", required=True, tracking=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company, index=True)
    category_kind = fields.Selection(
        [
            ("income", "Ingreso"),
            ("expense", "Gasto"),
            ("investment", "Bien de inversion"),
            ("withholding", "Retencion"),
            ("other", "Otro"),
        ],
        string="Tipo de categoria",
        required=True,
        default="expense",
    )
    official_label = fields.Char(string="Etiqueta oficial")
    model_reference = fields.Char(string="Modelo relacionado")
    valid_from = fields.Date(string="Vigente desde")
    valid_to = fields.Date(string="Vigente hasta")
    default_irpf_deductible_percent = fields.Float(string="IRPF deducible por defecto (%)", default=100.0)
    default_vat_deductible_percent = fields.Float(string="IVA deducible por defecto (%)", default=100.0)
    legal_reference = fields.Char(string="Referencia legal")
    official_source_url = fields.Char(string="URL fuente oficial")
    legal_source_ids = fields.Many2many("autonomo.legal.source", string="Fuentes oficiales")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")

    _code_company_uniq = models.Constraint(
        "UNIQUE(company_id, code)",
        "El codigo de categoria debe ser unico por empresa.",
    )

    @api.constrains("valid_from", "valid_to")
    def _check_dates(self):
        for record in self:
            if record.valid_from and record.valid_to and record.valid_from > record.valid_to:
                raise ValidationError("La fecha de inicio de vigencia no puede ser posterior a la fecha final.")

    @api.constrains("default_irpf_deductible_percent", "default_vat_deductible_percent")
    def _check_percentages(self):
        for record in self:
            values = [record.default_irpf_deductible_percent, record.default_vat_deductible_percent]
            if any(value < 0 or value > 100 for value in values):
                raise ValidationError("Los porcentajes deducibles deben estar entre 0 y 100.")
