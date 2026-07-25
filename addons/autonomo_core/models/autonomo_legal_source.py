from odoo import fields, models


class AutonomoLegalSource(models.Model):
    _name = "autonomo.legal.source"
    _description = "Fuente oficial autonomo"
    _order = "authority, code"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Codigo", required=True, index=True)
    authority = fields.Selection(
        [
            ("boe", "BOE"),
            ("aeat", "Agencia Tributaria"),
            ("tgss", "TGSS / Importass"),
            ("seguridad_social", "Seguridad Social"),
            ("sepe", "SEPE"),
            ("other", "Otro organismo oficial"),
        ],
        string="Organismo",
        required=True,
        default="boe",
    )
    source_type = fields.Selection(
        [
            ("law", "Norma"),
            ("regulation", "Reglamento"),
            ("administrative_instruction", "Instruccion administrativa"),
            ("technical_specification", "Especificacion tecnica"),
            ("guide", "Guia oficial"),
            ("api", "API oficial"),
        ],
        string="Tipo de fuente",
        required=True,
        default="law",
    )
    official_url = fields.Char(string="URL oficial", required=True)
    document_reference = fields.Char(string="Referencia del documento")
    publication_date = fields.Date(string="Fecha de publicacion")
    valid_from = fields.Date(string="Vigente desde")
    valid_to = fields.Date(string="Vigente hasta")
    verified_at = fields.Datetime(string="Fecha de verificacion", default=fields.Datetime.now)
    legal_disclaimer = fields.Text(
        string="Aviso legal",
        default="Fuente oficial consultada con fines informativos. Requiere revision humana antes de presentar tramites o declaraciones."
    )
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")
