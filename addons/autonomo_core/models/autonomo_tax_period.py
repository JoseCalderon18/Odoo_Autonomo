from odoo import fields, models


class AutonomoTaxPeriod(models.Model):
    _name = "autonomo.tax.period"
    _description = "Periodo fiscal base autonomo"
    _order = "fiscal_year desc, period_code"

    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    activity_id = fields.Many2one("autonomo.activity", string="Actividad")
    fiscal_year = fields.Integer(string="Ejercicio fiscal", required=True)
    period_type = fields.Selection(
        [("monthly", "Mensual"), ("quarterly", "Trimestral"), ("annual", "Anual")],
        string="Tipo de periodo",
        required=True,
        default="quarterly",
    )
    period_code = fields.Char(string="Codigo de periodo", required=True)
    date_start = fields.Date(string="Fecha de inicio", required=True)
    date_end = fields.Date(string="Fecha de fin", required=True)
    state = fields.Selection(
        [("draft", "Borrador"), ("review", "Revision"), ("closed", "Cerrado"), ("reopened", "Reabierto")],
        string="Estado",
        default="draft",
        required=True,
    )
    closed_at = fields.Datetime(string="Fecha de cierre")
    closed_by = fields.Many2one("res.users", string="Cerrado por")
    reopen_reason = fields.Text(string="Motivo de reapertura")
