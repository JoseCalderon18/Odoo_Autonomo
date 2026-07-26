from odoo import fields, models


class AutonomoLegalSyncStatus(models.Model):
    _name = "autonomo.legal.sync.status"
    _description = "Estado sincronizacion legal"
    _order = "started_at desc, id desc"

    name = fields.Char(string="Nombre", required=True)
    source_id = fields.Many2one("autonomo.legal.source", string="Fuente", ondelete="cascade")
    boe_identifier = fields.Char(string="Identificador BOE", index=True)
    sync_type = fields.Selection(
        [("metadata", "Metadatos"), ("metadata_eli", "Metadatos ELI"), ("analysis", "Analisis"), ("index", "Indice"), ("block", "Bloque"), ("full", "Completa")],
        string="Tipo de sincronizacion",
        required=True,
        default="full",
    )
    state = fields.Selection([("running", "En curso"), ("done", "Correcto"), ("error", "Error")], string="Estado", default="running", required=True)
    started_at = fields.Datetime(string="Inicio", default=fields.Datetime.now)
    finished_at = fields.Datetime(string="Fin")
    http_status = fields.Char(string="Estado HTTP")
    content_hash = fields.Char(string="Hash del contenido")
    records_created = fields.Integer(string="Registros creados")
    records_updated = fields.Integer(string="Registros actualizados")
    error_message = fields.Text(string="Mensaje de error")
