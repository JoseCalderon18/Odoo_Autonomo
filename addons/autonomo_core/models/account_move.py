from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    activity_id = fields.Many2one("autonomo.activity", check_company=True)
    operation_date = fields.Date()
    tax_document_kind = fields.Selection(
        [
            ("invoice", "Factura"),
            ("simplified_invoice", "Factura simplificada"),
            ("rectifying_invoice", "Factura rectificativa"),
            ("receipt", "Justificante"),
            ("other", "Otro"),
        ],
        default="invoice",
    )
    income_expense_book_state = fields.Selection([("draft", "Borrador"), ("review", "Revision"), ("locked", "Bloqueado")], default="draft")
    tax_period_id = fields.Many2one("autonomo.tax.period")
    tax_review_state = fields.Selection(
        [("pending", "Pendiente"), ("ok", "Revisado"), ("warning", "Aviso"), ("blocked", "Bloqueado")],
        default="pending",
    )
    source_attachment_id = fields.Many2one("ir.attachment")
    document_sha256 = fields.Char()
    electronic_invoice_uuid = fields.Char()
    electronic_invoice_status = fields.Selection(
        [("not_applicable", "No aplica"), ("pending", "Pendiente"), ("sent", "Enviada"), ("accepted", "Aceptada"), ("rejected", "Rechazada")],
        default="not_applicable",
    )
    effective_payment_date = fields.Date()
    book_locked = fields.Boolean()

    def unlink(self):
        locked = self.filtered(lambda move: move.state == "posted" or move.book_locked)
        if locked:
            raise UserError("No se pueden eliminar facturas contabilizadas o bloqueadas. Use rectificativas cuando proceda.")
        return super().unlink()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    activity_id = fields.Many2one("autonomo.activity", check_company=True)
    tax_category_id = fields.Many2one("autonomo.tax.category", check_company=True)
    irpf_deductible_percent = fields.Float(default=100.0)
    vat_deductible_percent = fields.Float(default=100.0)
    irpf_deductible_amount = fields.Monetary(compute="_compute_deductible_amounts", store=True, currency_field="currency_id")
    vat_deductible_amount = fields.Monetary(compute="_compute_deductible_amounts", store=True, currency_field="currency_id")
    withholding_rate_snapshot = fields.Float()
    withholding_amount_snapshot = fields.Monetary(currency_field="currency_id")
    is_investment_asset = fields.Boolean()
    deductibility_review_required = fields.Boolean()
    deductibility_notes = fields.Text()

    @api.depends("balance", "irpf_deductible_percent", "vat_deductible_percent")
    def _compute_deductible_amounts(self):
        for line in self:
            base = abs(line.balance)
            line.irpf_deductible_amount = base * line.irpf_deductible_percent / 100.0
            line.vat_deductible_amount = base * line.vat_deductible_percent / 100.0

    @api.constrains("irpf_deductible_percent", "vat_deductible_percent")
    def _check_deductible_percentages(self):
        for line in self:
            if any(value < 0 or value > 100 for value in [line.irpf_deductible_percent, line.vat_deductible_percent]):
                raise ValidationError("Los porcentajes deducibles deben estar entre 0 y 100.")
