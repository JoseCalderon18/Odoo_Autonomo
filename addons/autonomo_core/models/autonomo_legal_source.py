from odoo import fields, models


class AutonomoLegalSource(models.Model):
    _name = "autonomo.legal.source"
    _description = "Fuente oficial autonomo"
    _order = "authority, code"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    authority = fields.Selection(
        [
            ("boe", "BOE"),
            ("aeat", "Agencia Tributaria"),
            ("tgss", "TGSS / Importass"),
            ("seguridad_social", "Seguridad Social"),
            ("sepe", "SEPE"),
            ("other", "Otro organismo oficial"),
        ],
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
        required=True,
        default="law",
    )
    official_url = fields.Char(required=True)
    document_reference = fields.Char()
    publication_date = fields.Date()
    valid_from = fields.Date()
    valid_to = fields.Date()
    verified_at = fields.Datetime(default=fields.Datetime.now)
    legal_disclaimer = fields.Text(
        default="Fuente oficial consultada con fines informativos. Requiere revision humana antes de presentar tramites o declaraciones."
    )
    active = fields.Boolean(default=True)
    notes = fields.Text()
