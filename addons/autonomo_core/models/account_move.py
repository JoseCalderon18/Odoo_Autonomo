from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    activity_id = fields.Many2one("autonomo.activity", string="Actividad", check_company=True)
    operation_date = fields.Date(string="Fecha de operacion")
    tax_document_kind = fields.Selection(
        [
            ("invoice", "Factura"),
            ("simplified_invoice", "Factura simplificada"),
            ("rectifying_invoice", "Factura rectificativa"),
            ("receipt", "Justificante"),
            ("other", "Otro"),
        ],
        string="Tipo de documento fiscal",
        default="invoice",
    )
    income_expense_book_state = fields.Selection([("draft", "Borrador"), ("review", "Revision"), ("locked", "Bloqueado")], string="Estado en libro fiscal", default="draft")
    tax_period_id = fields.Many2one("autonomo.tax.period", string="Periodo fiscal")
    tax_review_state = fields.Selection(
        [("pending", "Pendiente"), ("ok", "Revisado"), ("warning", "Aviso"), ("blocked", "Bloqueado")],
        string="Estado de revision fiscal",
        default="pending",
    )
    source_attachment_id = fields.Many2one("ir.attachment", string="Adjunto origen")
    document_sha256 = fields.Char(string="Hash SHA-256 del documento")
    electronic_invoice_uuid = fields.Char(string="UUID factura electronica")
    electronic_invoice_status = fields.Selection(
        [("not_applicable", "No aplica"), ("pending", "Pendiente"), ("sent", "Enviada"), ("accepted", "Aceptada"), ("rejected", "Rechazada")],
        string="Estado factura electronica",
        default="not_applicable",
    )
    effective_payment_date = fields.Date(string="Fecha efectiva de pago")
    book_locked = fields.Boolean(string="Libro bloqueado")

    def unlink(self):
        locked = self.filtered(lambda move: move.state == "posted" or move.book_locked)
        if locked:
            raise UserError("No se pueden eliminar facturas contabilizadas o bloqueadas. Use rectificativas cuando proceda.")
        return super().unlink()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    activity_id = fields.Many2one("autonomo.activity", string="Actividad", check_company=True)
    tax_category_id = fields.Many2one("autonomo.tax.category", string="Categoria fiscal", check_company=True)
    irpf_deductible_percent = fields.Float(string="IRPF deducible (%)", default=100.0)
    vat_deductible_percent = fields.Float(string="IVA deducible (%)", default=100.0)
    irpf_deductible_amount = fields.Monetary(string="Importe deducible IRPF", compute="_compute_deductible_amounts", store=True, currency_field="currency_id")
    vat_deductible_amount = fields.Monetary(string="Importe deducible IVA", compute="_compute_deductible_amounts", store=True, currency_field="currency_id")
    withholding_rate_snapshot = fields.Float(string="Retencion snapshot (%)")
    withholding_amount_snapshot = fields.Monetary(string="Importe retencion snapshot", currency_field="currency_id")
    is_investment_asset = fields.Boolean(string="Bien de inversion")
    deductibility_review_required = fields.Boolean(string="Requiere revision de deducibilidad")
    deductibility_notes = fields.Text(string="Notas de deducibilidad")

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
