import hashlib

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


AUTHORITY_SELECTION = [
    ("aeat", "Agencia Tributaria"),
    ("tgss", "TGSS / Importass"),
    ("sepe", "SEPE"),
    ("regional", "Autonomica"),
    ("local", "Local"),
    ("other", "Otra"),
]


class AutonomoProcedure(models.Model):
    _name = "autonomo.procedure"
    _description = "Tramite oficial autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "authority, code"

    name = fields.Char(string="Nombre", required=True, tracking=True)
    code = fields.Char(string="Codigo", required=True, index=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    authority = fields.Selection(AUTHORITY_SELECTION, string="Organismo", required=True, default="aeat")
    procedure_type = fields.Selection(
        [
            ("registration", "Alta"),
            ("modification", "Modificacion"),
            ("deregistration", "Baja"),
            ("tax_return", "Autoliquidacion"),
            ("informative_return", "Declaracion informativa"),
            ("social_security", "Seguridad Social"),
            ("benefit", "Beneficio o ayuda"),
            ("document_submission", "Aportacion documental"),
            ("other", "Otro"),
        ],
        string="Tipo de tramite",
        required=True,
        default="other",
    )
    model_code = fields.Char(string="Modelo")
    description = fields.Text(string="Descripcion")
    trigger_event = fields.Char(string="Evento disparador")
    periodicity = fields.Selection(
        [("once", "Una vez"), ("monthly", "Mensual"), ("quarterly", "Trimestral"), ("annual", "Anual"), ("event", "Por evento")],
        string="Periodicidad",
        default="event",
    )
    valid_from = fields.Date(string="Vigente desde")
    valid_to = fields.Date(string="Vigente hasta")
    official_source_url = fields.Char(string="URL fuente oficial")
    legal_reference = fields.Char(string="Referencia legal")
    legal_source_ids = fields.Many2many("autonomo.legal.source", string="Fuentes oficiales")
    requires_human_submission = fields.Boolean(string="Requiere presentacion humana", default=True)
    supports_file_generation = fields.Boolean(string="Permite generar archivo", default=False)
    requirement_ids = fields.One2many("autonomo.procedure.requirement", "procedure_id", string="Requisitos")
    submission_ids = fields.One2many("autonomo.submission", "procedure_id", string="Presentaciones")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")

    _code_company_uniq = models.Constraint(
        "UNIQUE(company_id, code)",
        "El codigo de tramite debe ser unico por empresa.",
    )


class AutonomoProcedureRequirement(models.Model):
    _name = "autonomo.procedure.requirement"
    _description = "Requisito de tramite autonomo"
    _order = "procedure_id, sequence, id"

    procedure_id = fields.Many2one("autonomo.procedure", string="Tramite", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Secuencia", default=10)
    requirement_type = fields.Selection(
        [
            ("field", "Dato"),
            ("document", "Documento"),
            ("declaration", "Declaracion"),
            ("authorization", "Autorizacion"),
            ("signature", "Firma"),
            ("payment", "Pago"),
            ("attachment", "Adjunto"),
            ("other", "Otro"),
        ],
        string="Tipo de requisito",
        required=True,
        default="field",
    )
    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripcion")
    field_model = fields.Char(string="Modelo del dato")
    field_name = fields.Char(string="Campo del dato")
    document_type = fields.Char(string="Tipo de documento")
    required_condition = fields.Char(string="Condicion")
    mandatory = fields.Boolean(string="Obligatorio", default=True)
    valid_from = fields.Date(string="Vigente desde")
    valid_to = fields.Date(string="Vigente hasta")
    official_source_url = fields.Char(string="URL fuente oficial")
    legal_reference = fields.Char(string="Referencia legal")
    active = fields.Boolean(string="Activo", default=True)

    @api.constrains("valid_from", "valid_to")
    def _check_dates(self):
        for record in self:
            if record.valid_from and record.valid_to and record.valid_from > record.valid_to:
                raise ValidationError("La fecha inicial del requisito no puede ser posterior a la final.")


class AutonomoSubmission(models.Model):
    _name = "autonomo.submission"
    _description = "Presentacion o borrador autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "submitted_at desc, draft_date desc, id desc"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    procedure_id = fields.Many2one("autonomo.procedure", string="Tramite", required=True)
    tax_period_id = fields.Many2one("autonomo.tax.period", string="Periodo fiscal")
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("incomplete", "Incompleto"),
            ("review", "Revision"),
            ("ready", "Listo"),
            ("submitted", "Presentado"),
            ("accepted", "Aceptado"),
            ("rejected", "Rechazado"),
            ("corrected", "Corregido"),
            ("cancelled", "Cancelado"),
        ],
        string="Estado",
        default="draft",
        required=True,
        tracking=True,
    )
    draft_date = fields.Date(string="Fecha de borrador", default=fields.Date.context_today)
    review_date = fields.Date(string="Fecha de revision")
    ready_date = fields.Date(string="Fecha listo")
    submitted_at = fields.Datetime(string="Fecha de presentacion")
    submission_channel = fields.Selection(
        [("electronic", "Electronico"), ("paper", "Papel"), ("representative", "Representante"), ("other", "Otro")],
        string="Canal de presentacion",
    )
    filing_reference = fields.Char(string="Referencia de presentacion")
    secure_verification_code = fields.Char(string="CSV")
    result = fields.Selection(
        [("pending", "Pendiente"), ("positive", "A ingresar"), ("negative", "A devolver"), ("zero", "Sin actividad/resultado cero"), ("other", "Otro")],
        string="Resultado",
    )
    amount = fields.Monetary(string="Importe", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="company_id.currency_id", store=True, readonly=True)
    payment_method = fields.Selection(
        [("none", "Sin pago"), ("direct_debit", "Domiciliacion"), ("bank_transfer", "Transferencia"), ("card", "Tarjeta"), ("other", "Otro")],
        string="Metodo de pago",
    )
    direct_debit_iban_masked = fields.Char(string="IBAN domiciliacion enmascarado")
    generated_file_id = fields.Many2one("ir.attachment", string="Archivo generado")
    filing_receipt_id = fields.Many2one("ir.attachment", string="Justificante de presentacion")
    human_approved_by = fields.Many2one("res.users", string="Aprobado por")
    human_approved_at = fields.Datetime(string="Fecha de aprobacion")
    source_snapshot_hash = fields.Char(string="Hash snapshot fuente")
    document_ids = fields.One2many("autonomo.submission.document", "submission_id", string="Documentos")
    checklist_line_ids = fields.One2many("autonomo.submission.checklist.line", "submission_id", string="Checklist")
    checklist_state = fields.Selection(
        [("pending", "Pendiente"), ("incomplete", "Incompleto"), ("verified", "Verificado")],
        string="Estado del checklist",
        compute="_compute_checklist_state",
        store=True,
    )
    notes = fields.Text(string="Notas")

    @api.depends("checklist_line_ids.mandatory", "checklist_line_ids.verified", "checklist_line_ids.data_present", "checklist_line_ids.document_attached")
    def _compute_checklist_state(self):
        for submission in self:
            lines = submission.checklist_line_ids
            mandatory = lines.filtered("mandatory")
            if not lines:
                submission.checklist_state = "pending"
            elif any(not line.requirement_ok for line in mandatory):
                submission.checklist_state = "incomplete"
            else:
                submission.checklist_state = "verified"

    def action_refresh_checklist(self):
        for submission in self:
            existing_by_requirement = {line.requirement_id.id: line for line in submission.checklist_line_ids if line.requirement_id}
            commands = []
            for requirement in submission.procedure_id.requirement_ids.filtered("active"):
                if requirement.id in existing_by_requirement:
                    continue
                commands.append(
                    (
                        0,
                        0,
                        {
                            "requirement_id": requirement.id,
                            "name": requirement.name,
                            "mandatory": requirement.mandatory,
                            "required_condition": requirement.required_condition,
                            "official_source_url": requirement.official_source_url,
                        },
                    )
                )
            if commands:
                submission.write({"checklist_line_ids": commands})
        return True

    def action_mark_ready(self):
        for submission in self:
            submission.action_refresh_checklist()
            mandatory = submission.checklist_line_ids.filtered("mandatory")
            if any(not line.requirement_ok for line in mandatory):
                raise UserError("No se puede marcar como listo: hay requisitos obligatorios sin verificar.")
            submission.write({"state": "ready", "ready_date": fields.Date.context_today(self)})


class AutonomoSubmissionChecklistLine(models.Model):
    _name = "autonomo.submission.checklist.line"
    _description = "Linea checklist tramite autonomo"
    _order = "submission_id, sequence, id"

    submission_id = fields.Many2one("autonomo.submission", string="Presentacion", required=True, ondelete="cascade")
    requirement_id = fields.Many2one("autonomo.procedure.requirement", string="Requisito")
    sequence = fields.Integer(string="Secuencia", related="requirement_id.sequence", store=True, readonly=True)
    name = fields.Char(string="Nombre", required=True)
    mandatory = fields.Boolean(string="Obligatorio", default=True)
    required_condition = fields.Char(string="Condicion")
    data_present = fields.Boolean(string="Dato presente")
    document_attached = fields.Boolean(string="Documento adjunto")
    verified = fields.Boolean(string="Verificado")
    verified_by = fields.Many2one("res.users", string="Verificado por")
    verified_at = fields.Datetime(string="Fecha de verificacion")
    official_source_url = fields.Char(string="URL fuente oficial")
    state = fields.Selection(
        [("missing", "Falta"), ("pending", "Pendiente"), ("verified", "Verificado")],
        string="Estado",
        compute="_compute_state",
        store=True,
    )
    requirement_ok = fields.Boolean(string="Requisito correcto", compute="_compute_state", store=True)

    @api.depends("mandatory", "data_present", "document_attached", "verified")
    def _compute_state(self):
        for line in self:
            has_evidence = line.data_present or line.document_attached
            line.requirement_ok = (not line.mandatory) or (has_evidence and line.verified)
            if line.requirement_ok:
                line.state = "verified"
            elif has_evidence:
                line.state = "pending"
            else:
                line.state = "missing"

    def action_verify(self):
        self.write({"verified": True, "verified_by": self.env.user.id, "verified_at": fields.Datetime.now()})


class AutonomoSubmissionDocument(models.Model):
    _name = "autonomo.submission.document"
    _description = "Documento de presentacion autonomo"
    _order = "submission_id, id"

    submission_id = fields.Many2one("autonomo.submission", string="Presentacion", required=True, ondelete="cascade")
    requirement_id = fields.Many2one("autonomo.procedure.requirement", string="Requisito")
    attachment_id = fields.Many2one("ir.attachment", string="Adjunto", required=True)
    document_type = fields.Char(string="Tipo de documento")
    document_number = fields.Char(string="Numero de documento")
    issue_date = fields.Date(string="Fecha de emision")
    valid_until = fields.Date(string="Valido hasta")
    issuer = fields.Char(string="Emisor")
    sha256 = fields.Char(string="Hash SHA-256", compute="_compute_sha256", store=True)
    contains_personal_data = fields.Boolean(string="Contiene datos personales", default=True)
    verified = fields.Boolean(string="Verificado")
    verified_by = fields.Many2one("res.users", string="Verificado por")
    verified_at = fields.Datetime(string="Fecha de verificacion")
    verification_notes = fields.Text(string="Notas de verificacion")

    @api.depends("attachment_id.datas")
    def _compute_sha256(self):
        for document in self:
            document.sha256 = hashlib.sha256((document.attachment_id.datas or "").encode()).hexdigest() if document.attachment_id else False
