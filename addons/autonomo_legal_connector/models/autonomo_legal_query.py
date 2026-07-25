import hashlib

from odoo import api, fields, models


class AutonomoLegalQuery(models.Model):
    _name = "autonomo.legal.query"
    _description = "Consulta legal"
    _order = "create_date desc"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company)
    query_type = fields.Selection(
        [("search", "Busqueda"), ("document", "Documento"), ("section", "Seccion"), ("review", "Revision")],
        string="Tipo de consulta",
        default="document",
        required=True,
    )
    question = fields.Text(string="Pregunta", required=True)
    anonymized_payload = fields.Text(string="Payload anonimizado")
    payload_hash = fields.Char(string="Hash del payload", compute="_compute_payload_hash", store=True)
    answer = fields.Text(string="Respuesta")
    state = fields.Selection([("draft", "Borrador"), ("answered", "Respondida"), ("needs_review", "Revision humana")], string="Estado", default="draft")
    citation_ids = fields.One2many("autonomo.legal.citation", "query_id", string="Citas")

    @api.depends("question", "anonymized_payload")
    def _compute_payload_hash(self):
        for query in self:
            payload = f"{query.question or ''}|{query.anonymized_payload or ''}"
            query.payload_hash = hashlib.sha256(payload.encode()).hexdigest()


class AutonomoLegalCitation(models.Model):
    _name = "autonomo.legal.citation"
    _description = "Cita legal"
    _order = "query_id, sequence, id"

    query_id = fields.Many2one("autonomo.legal.query", string="Consulta", ondelete="cascade")
    source_id = fields.Many2one("autonomo.legal.source", string="Fuente", required=True)
    sequence = fields.Integer(string="Secuencia", default=10)
    citation_kind = fields.Selection([("metadata", "Metadatos"), ("analysis", "Analisis"), ("block", "Bloque"), ("version", "Version")], string="Tipo de cita", default="block")
    block_id = fields.Many2one("autonomo.legal.block", string="Bloque")
    block_version_id = fields.Many2one("autonomo.legal.block.version", string="Version de bloque")
    title = fields.Char(string="Titulo")
    official_url = fields.Char(string="URL oficial")
    verified_at = fields.Datetime(string="Fecha de verificacion")
