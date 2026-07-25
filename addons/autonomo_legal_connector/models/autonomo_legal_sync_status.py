from odoo import fields, models


class AutonomoLegalSyncStatus(models.Model):
    _name = "autonomo.legal.sync.status"
    _description = "Estado sincronizacion legal"
    _order = "started_at desc, id desc"

    name = fields.Char(required=True)
    source_id = fields.Many2one("autonomo.legal.source", ondelete="cascade")
    boe_identifier = fields.Char(index=True)
    sync_type = fields.Selection(
        [("metadata", "Metadatos"), ("metadata_eli", "Metadatos ELI"), ("analysis", "Analisis"), ("index", "Indice"), ("block", "Bloque"), ("full", "Completa")],
        required=True,
        default="full",
    )
    state = fields.Selection([("running", "En curso"), ("done", "Correcto"), ("error", "Error")], default="running", required=True)
    started_at = fields.Datetime(default=fields.Datetime.now)
    finished_at = fields.Datetime()
    http_status = fields.Char()
    content_hash = fields.Char()
    records_created = fields.Integer()
    records_updated = fields.Integer()
    error_message = fields.Text()
