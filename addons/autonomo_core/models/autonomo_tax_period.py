from odoo import fields, models


class AutonomoTaxPeriod(models.Model):
    _name = "autonomo.tax.period"
    _description = "Periodo fiscal base autonomo"
    _order = "fiscal_year desc, period_code"

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    activity_id = fields.Many2one("autonomo.activity")
    fiscal_year = fields.Integer(required=True)
    period_type = fields.Selection(
        [("monthly", "Mensual"), ("quarterly", "Trimestral"), ("annual", "Anual")],
        required=True,
        default="quarterly",
    )
    period_code = fields.Char(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    state = fields.Selection(
        [("draft", "Borrador"), ("review", "Revision"), ("closed", "Cerrado"), ("reopened", "Reabierto")],
        default="draft",
        required=True,
    )
    closed_at = fields.Datetime()
    closed_by = fields.Many2one("res.users")
    reopen_reason = fields.Text()
