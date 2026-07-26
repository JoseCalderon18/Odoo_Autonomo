import hashlib
import json

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


AUTHORITY_SELECTION = [
    ("aeat", "Agencia Tributaria"),
    ("tgss", "TGSS / Importass"),
    ("sepe", "SEPE"),
    ("regional", "Autonómica"),
    ("local", "Local"),
    ("other", "Otra"),
]


class AutonomoTaxObligation(models.Model):
    _name = "autonomo.tax.obligation"
    _description = "Obligación fiscal del autónomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "model_code, start_date"

    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    activity_id = fields.Many2one("autonomo.activity", string="Actividad")
    authority = fields.Selection(AUTHORITY_SELECTION, string="Organismo", required=True, default="aeat")
    tax_kind = fields.Selection(
        [
            ("vat", "IVA"),
            ("irpf", "IRPF"),
            ("withholding", "Retenciones"),
            ("informative", "Informativa"),
            ("social_security", "Seguridad Social"),
            ("other", "Otra"),
        ],
        string="Tipo",
        required=True,
        default="other",
    )
    model_code = fields.Char(string="Modelo", required=True)
    periodicity = fields.Selection(
        [("monthly", "Mensual"), ("quarterly", "Trimestral"), ("annual", "Anual"), ("event", "Por evento")],
        string="Periodicidad",
        required=True,
        default="quarterly",
    )
    start_date = fields.Date(string="Fecha de inicio")
    end_date = fields.Date(string="Fecha de fin")
    calculation_service = fields.Char(string="Servicio de cálculo")
    legal_reference = fields.Char(string="Referencia legal")
    official_source_url = fields.Char(string="Fuente oficial")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")

    _uniq = models.Constraint("UNIQUE(company_id, activity_id, model_code, start_date)", "La obligación ya existe para esa empresa, actividad y fecha.")

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")


class AutonomoTaxDeadline(models.Model):
    _name = "autonomo.tax.deadline"
    _description = "Plazo fiscal versionado"
    _order = "fiscal_year desc, model_code, period_code"

    authority = fields.Selection(AUTHORITY_SELECTION, string="Organismo", required=True, default="aeat")
    model_code = fields.Char(string="Modelo", required=True)
    fiscal_year = fields.Integer(string="Ejercicio", required=True)
    period_code = fields.Char(string="Periodo", required=True)
    filing_start_date = fields.Date(string="Inicio presentación")
    filing_end_date = fields.Date(string="Fin presentación")
    direct_debit_end_date = fields.Date(string="Fin domiciliación")
    source_document_url = fields.Char(string="Documento fuente")
    source_version = fields.Char(string="Versión de fuente")
    verified_at = fields.Datetime(string="Verificado el")
    notes = fields.Text(string="Notas")

    _uniq = models.Constraint("UNIQUE(authority, model_code, fiscal_year, period_code)", "El plazo ya existe para ese modelo, ejercicio y periodo.")


class AutonomoTaxReturn(models.Model):
    _name = "autonomo.tax.return"
    _description = "Borrador fiscal"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "fiscal_year desc, model_code, id desc"

    name = fields.Char(string="Nombre", compute="_compute_name", store=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    obligation_id = fields.Many2one("autonomo.tax.obligation", string="Obligación", required=True)
    period_id = fields.Many2one("autonomo.tax.period", string="Periodo", required=True)
    fiscal_year = fields.Integer(string="Ejercicio", related="period_id.fiscal_year", store=True, readonly=True)
    model_code = fields.Char(string="Modelo", related="obligation_id.model_code", store=True, readonly=True)
    form_year = fields.Integer(string="Año formulario")
    form_version = fields.Char(string="Versión formulario")
    state = fields.Selection(
        [("draft", "Borrador"), ("review", "Revisión"), ("ready", "Listo"), ("submitted", "Presentado"), ("accepted", "Aceptado"), ("cancelled", "Cancelado")],
        string="Estado",
        default="draft",
        tracking=True,
    )
    calculation_version = fields.Char(string="Versión cálculo")
    calculation_snapshot = fields.Json(string="Snapshot de cálculo")
    amount_to_pay = fields.Monetary(string="A ingresar", currency_field="currency_id")
    amount_to_refund = fields.Monetary(string="A devolver", currency_field="currency_id")
    amount_to_compensate = fields.Monetary(string="A compensar", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="company_id.currency_id", store=True, readonly=True)
    book_snapshot_ids = fields.Many2many("autonomo.tax.book.snapshot", string="Snapshots de libros")
    generated_file_id = fields.Many2one("ir.attachment", string="Archivo generado")
    submitted_at = fields.Datetime(string="Fecha de presentación")
    filing_receipt_id = fields.Many2one("ir.attachment", string="Justificante")
    filing_reference = fields.Char(string="Referencia de presentación")
    human_approved_by = fields.Many2one("res.users", string="Aprobado por")
    human_approved_at = fields.Datetime(string="Fecha aprobación")
    source_verified = fields.Boolean(string="Diseño oficial verificado")
    notes = fields.Text(string="Notas")

    @api.depends("model_code", "period_id.period_code", "fiscal_year")
    def _compute_name(self):
        for record in self:
            record.name = f"Modelo {record.model_code or ''} - {record.period_id.period_code or ''}/{record.fiscal_year or ''}".strip()

    def action_mark_ready(self):
        for record in self:
            if not record.source_verified:
                raise UserError("No se puede marcar como listo: el diseño o fuente oficial del ejercicio no está verificado.")
            record.state = "ready"

    def action_create_snapshot(self):
        for record in self:
            snapshot = self.env["autonomo.tax.book.snapshot"].create({
                "name": f"Snapshot {record.name}",
                "company_id": record.company_id.id,
                "tax_period_id": record.period_id.id,
                "snapshot_type": "tax_return",
                "calculation_version": record.calculation_version or "pending_legal_verification",
                "source_model": record._name,
                "source_record_id": record.id,
            })
            record.book_snapshot_ids = [(4, snapshot.id)]
        return True


class AutonomoTaxBookEntry(models.Model):
    _name = "autonomo.tax.book.entry"
    _description = "Apunte de libro fiscal"
    _order = "fiscal_year desc, fiscal_quarter, entry_sequence"

    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    activity_id = fields.Many2one("autonomo.activity", string="Actividad")
    book_type = fields.Selection(
        [
            ("issued_invoice", "Facturas expedidas"),
            ("received_invoice", "Facturas recibidas"),
            ("income", "Ventas e ingresos"),
            ("expense", "Compras y gastos"),
            ("investment_asset", "Bienes de inversión"),
            ("provision", "Provisiones y suplidos"),
            ("intraeu", "Operaciones intracomunitarias"),
        ],
        string="Libro",
        required=True,
    )
    source_move_id = fields.Many2one("account.move", string="Factura")
    source_line_id = fields.Many2one("account.move.line", string="Línea")
    entry_sequence = fields.Integer(string="Secuencia")
    invoice_number = fields.Char(string="Número factura")
    invoice_series = fields.Char(string="Serie")
    issue_date = fields.Date(string="Fecha expedición")
    operation_date = fields.Date(string="Fecha operación")
    partner_name = fields.Char(string="Tercero")
    partner_vat = fields.Char(string="NIF tercero")
    concept_code = fields.Char(string="Código concepto")
    concept_description = fields.Char(string="Concepto")
    tax_base = fields.Monetary(string="Base imponible", currency_field="currency_id")
    vat_rate = fields.Float(string="Tipo IVA")
    vat_amount = fields.Monetary(string="Cuota IVA", currency_field="currency_id")
    vat_deductible_amount = fields.Monetary(string="IVA deducible", currency_field="currency_id")
    irpf_deductible_amount = fields.Monetary(string="IRPF deducible", currency_field="currency_id")
    withholding_rate = fields.Float(string="Tipo retención")
    withholding_amount = fields.Monetary(string="Retención", currency_field="currency_id")
    total_amount = fields.Monetary(string="Total", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Moneda", required=True, default=lambda self: self.env.company.currency_id)
    exchange_rate = fields.Float(string="Tipo cambio", default=1.0)
    is_rectifying = fields.Boolean(string="Rectificativa")
    rectified_move_id = fields.Many2one("account.move", string="Factura rectificada")
    document_sha256 = fields.Char(string="Hash documento")
    fiscal_year = fields.Integer(string="Ejercicio")
    fiscal_quarter = fields.Integer(string="Trimestre")


class AutonomoTaxBookSnapshot(models.Model):
    _name = "autonomo.tax.book.snapshot"
    _description = "Snapshot fiscal inmutable"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "created_at desc, id desc"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    tax_period_id = fields.Many2one("autonomo.tax.period", string="Periodo")
    snapshot_type = fields.Selection([("book", "Libro"), ("tax_return", "Borrador fiscal"), ("closure", "Cierre")], string="Tipo", default="book")
    calculation_version = fields.Char(string="Versión cálculo")
    source_model = fields.Char(string="Modelo origen")
    source_record_id = fields.Integer(string="ID origen")
    snapshot_hash = fields.Char(string="Hash SHA-256", compute="_compute_hash", store=True)
    locked = fields.Boolean(string="Bloqueado", default=True)
    created_at = fields.Datetime(string="Creado el", default=fields.Datetime.now)
    line_ids = fields.One2many("autonomo.tax.book.snapshot.line", "snapshot_id", string="Líneas")
    notes = fields.Text(string="Notas")

    @api.depends("name", "tax_period_id", "calculation_version", "line_ids.payload_hash")
    def _compute_hash(self):
        for record in self:
            payload = {
                "name": record.name,
                "period": record.tax_period_id.id,
                "version": record.calculation_version,
                "lines": record.line_ids.mapped("payload_hash"),
            }
            record.snapshot_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def unlink(self):
        if any(record.locked for record in self):
            raise UserError("No se pueden eliminar snapshots bloqueados.")
        return super().unlink()


class AutonomoTaxBookSnapshotLine(models.Model):
    _name = "autonomo.tax.book.snapshot.line"
    _description = "Línea de snapshot fiscal"

    snapshot_id = fields.Many2one("autonomo.tax.book.snapshot", string="Snapshot", required=True, ondelete="cascade")
    book_entry_id = fields.Many2one("autonomo.tax.book.entry", string="Apunte")
    payload = fields.Json(string="Datos")
    payload_hash = fields.Char(string="Hash línea", compute="_compute_payload_hash", store=True)

    @api.depends("payload")
    def _compute_payload_hash(self):
        for record in self:
            record.payload_hash = hashlib.sha256(json.dumps(record.payload or {}, sort_keys=True).encode()).hexdigest()


class AutonomoInvestmentAsset(models.Model):
    _name = "autonomo.investment.asset"
    _description = "Bien de inversión"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "acquisition_date desc, name"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    activity_id = fields.Many2one("autonomo.activity", string="Actividad")
    acquisition_date = fields.Date(string="Fecha adquisición")
    vendor_id = fields.Many2one("res.partner", string="Proveedor")
    source_move_id = fields.Many2one("account.move", string="Factura")
    acquisition_amount = fields.Monetary(string="Importe adquisición", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="company_id.currency_id", store=True, readonly=True)
    vat_deductible_percent = fields.Float(string="% IVA deducible", default=100.0)
    irpf_deductible_percent = fields.Float(string="% IRPF deducible", default=100.0)
    amortization_method = fields.Selection([("linear", "Lineal"), ("manual", "Manual"), ("pending", "Pendiente de verificar")], string="Método amortización", default="pending")
    useful_life_years = fields.Float(string="Vida útil años")
    annual_amortization_amount = fields.Monetary(string="Amortización anual", currency_field="currency_id")
    legal_reference = fields.Char(string="Referencia legal")
    official_source_url = fields.Char(string="Fuente oficial")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")

    @api.constrains("vat_deductible_percent", "irpf_deductible_percent")
    def _check_percentages(self):
        for record in self:
            if not 0 <= record.vat_deductible_percent <= 100 or not 0 <= record.irpf_deductible_percent <= 100:
                raise ValidationError("Los porcentajes de deducción deben estar entre 0 y 100.")
