import hashlib
import json

from odoo import fields, models
from odoo.exceptions import UserError


class AutonomoAiReview(models.Model):
    _name = "autonomo.ai.review"
    _description = "Revisión asistida por IA"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "created_at desc, id desc"

    review_type = fields.Selection(
        [
            ("invoice", "Factura"),
            ("expense", "Gasto"),
            ("quote", "Presupuesto"),
            ("quarter", "Trimestre"),
            ("tax_return", "Borrador fiscal"),
            ("procedure", "Trámite"),
            ("general_question", "Pregunta general"),
        ],
        string="Tipo",
        required=True,
        default="general_question",
    )
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    source_model = fields.Char(string="Modelo origen")
    source_record_id = fields.Integer(string="ID origen")
    request_payload_hash = fields.Char(string="Hash petición", compute="_compute_payload_hash", store=True)
    anonymized_payload = fields.Json(string="Payload anonimizado")
    question = fields.Text(string="Pregunta", required=True)
    answer = fields.Text(string="Respuesta")
    structured_result = fields.Json(string="Resultado estructurado")
    risk_level = fields.Selection([("low", "Bajo"), ("medium", "Medio"), ("high", "Alto"), ("critical", "Crítico")], string="Riesgo", default="medium")
    requires_human_review = fields.Boolean(string="Requiere revisión humana", default=True)
    provider = fields.Char(string="Proveedor")
    model_name = fields.Char(string="Modelo IA")
    prompt_version = fields.Char(string="Versión prompt", default="pending")
    state = fields.Selection(
        [("draft", "Borrador"), ("answered", "Respondida"), ("accepted", "Aceptada"), ("rejected", "Rechazada"), ("human_review", "Revisión humana")],
        string="Estado",
        default="draft",
        tracking=True,
    )
    created_at = fields.Datetime(string="Creado el", default=fields.Datetime.now)
    accepted_by = fields.Many2one("res.users", string="Aceptado por")
    accepted_at = fields.Datetime(string="Fecha aceptación")
    rejected_by = fields.Many2one("res.users", string="Rechazado por")
    rejected_at = fields.Datetime(string="Fecha rechazo")
    rejection_reason = fields.Text(string="Motivo rechazo")
    citation_ids = fields.One2many("autonomo.ai.citation", "review_id", string="Fuentes")
    issue_ids = fields.One2many("autonomo.compliance.issue", "review_id", string="Incidencias")

    def _compute_payload_hash(self):
        for review in self:
            review.request_payload_hash = hashlib.sha256(json.dumps(review.anonymized_payload or {}, sort_keys=True).encode()).hexdigest()

    def action_accept(self):
        for review in self:
            if not review.citation_ids:
                raise UserError("No se puede aceptar una revisión IA sin fuentes verificables.")
            if review.risk_level in ("high", "critical") and review.requires_human_review:
                raise UserError("La revisión requiere validación humana antes de aceptarse.")
            review.write({"state": "accepted", "accepted_by": self.env.user.id, "accepted_at": fields.Datetime.now()})
        return True

    def action_reject(self):
        self.write({"state": "rejected", "rejected_by": self.env.user.id, "rejected_at": fields.Datetime.now()})
        return True

    def action_request_human_review(self):
        self.write({"state": "human_review", "requires_human_review": True})
        return True

    def action_create_issue(self):
        for review in self:
            self.env["autonomo.compliance.issue"].create({
                "name": f"Incidencia {review.review_type}",
                "company_id": review.company_id.id,
                "review_id": review.id,
                "issue_type": "source_not_verified" if not review.citation_ids else "other",
                "risk_level": review.risk_level,
                "source_model": review.source_model,
                "source_record_id": review.source_record_id,
                "description": review.answer or review.question,
            })
        return True


class AutonomoAiCitation(models.Model):
    _name = "autonomo.ai.citation"
    _description = "Cita de revisión IA"
    _order = "review_id, sequence, id"

    review_id = fields.Many2one("autonomo.ai.review", string="Revisión", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Secuencia", default=10)
    legal_source_id = fields.Many2one("autonomo.legal.source", string="Fuente oficial")
    legal_connector_citation_id = fields.Many2one("autonomo.legal.citation", string="Cita del conector")
    title = fields.Char(string="Título", required=True)
    authority = fields.Char(string="Organismo")
    official_url = fields.Char(string="URL oficial")
    reference = fields.Char(string="Referencia")
    verified_at = fields.Datetime(string="Verificado el")
    source_version = fields.Char(string="Versión fuente")
    is_expired = fields.Boolean(string="Fuente caducada")
    notes = fields.Text(string="Notas")


class AutonomoComplianceIssue(models.Model):
    _name = "autonomo.compliance.issue"
    _description = "Incidencia de cumplimiento"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, id desc"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    review_id = fields.Many2one("autonomo.ai.review", string="Revisión IA")
    source_model = fields.Char(string="Modelo origen")
    source_record_id = fields.Integer(string="ID origen")
    issue_type = fields.Selection(
        [
            ("missing_data", "Falta dato"),
            ("missing_document", "Falta documento"),
            ("tax_mismatch", "Descuadre fiscal"),
            ("duplicate", "Duplicado"),
            ("deadline", "Plazo"),
            ("deductibility", "Deducibilidad"),
            ("legal_change", "Cambio normativo"),
            ("document_integrity", "Integridad documental"),
            ("source_not_verified", "Fuente no verificada"),
            ("other", "Otra"),
        ],
        string="Tipo",
        required=True,
        default="other",
    )
    risk_level = fields.Selection([("low", "Bajo"), ("medium", "Medio"), ("high", "Alto"), ("critical", "Crítico")], string="Riesgo", default="medium")
    priority = fields.Integer(string="Prioridad", default=10)
    state = fields.Selection([("open", "Abierta"), ("review", "En revisión"), ("resolved", "Resuelta"), ("cancelled", "Cancelada")], string="Estado", default="open", tracking=True)
    description = fields.Text(string="Descripción")
    resolution_notes = fields.Text(string="Notas de resolución")
    assigned_user_id = fields.Many2one("res.users", string="Asignado a")

    def action_resolve(self):
        self.write({"state": "resolved"})
        return True
