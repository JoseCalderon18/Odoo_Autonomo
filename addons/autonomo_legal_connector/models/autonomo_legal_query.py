import hashlib

from odoo import api, fields, models


class AutonomoLegalQuery(models.Model):
    _name = "autonomo.legal.query"
    _description = "Consulta legal"
    _order = "create_date desc"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    query_type = fields.Selection(
        [("search", "Busqueda"), ("document", "Documento"), ("section", "Seccion"), ("review", "Revision")],
        default="document",
        required=True,
    )
    question = fields.Text(required=True)
    anonymized_payload = fields.Text()
    payload_hash = fields.Char(compute="_compute_payload_hash", store=True)
    answer = fields.Text()
    state = fields.Selection([("draft", "Borrador"), ("answered", "Respondida"), ("needs_review", "Revision humana")], default="draft")
    citation_ids = fields.One2many("autonomo.legal.citation", "query_id")

    @api.depends("question", "anonymized_payload")
    def _compute_payload_hash(self):
        for query in self:
            payload = f"{query.question or ''}|{query.anonymized_payload or ''}"
            query.payload_hash = hashlib.sha256(payload.encode()).hexdigest()


class AutonomoLegalCitation(models.Model):
    _name = "autonomo.legal.citation"
    _description = "Cita legal"
    _order = "query_id, sequence, id"

    query_id = fields.Many2one("autonomo.legal.query", ondelete="cascade")
    source_id = fields.Many2one("autonomo.legal.source", required=True)
    sequence = fields.Integer(default=10)
    citation_kind = fields.Selection([("metadata", "Metadatos"), ("analysis", "Analisis"), ("block", "Bloque"), ("version", "Version")], default="block")
    block_id = fields.Many2one("autonomo.legal.block")
    block_version_id = fields.Many2one("autonomo.legal.block.version")
    title = fields.Char()
    official_url = fields.Char()
    verified_at = fields.Datetime()
