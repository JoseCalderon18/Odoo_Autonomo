from odoo import fields, models


class AutonomoLegalConfig(models.Model):
    _name = "autonomo.legal.config"
    _description = "Configuracion conector legal"
    _order = "name"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    service_url = fields.Char(default="https://www.boe.es/datosabiertos/api/legislacion-consolidada", required=True)
    auth_type = fields.Selection([("none", "Sin autenticacion"), ("token", "Token")], default="none", required=True)
    api_token = fields.Char(groups="autonomo_core.group_autonomo_admin")
    timeout_seconds = fields.Integer(default=20)
    verify_ssl = fields.Boolean(default=True)
    anonymization_mode = fields.Selection([("strict", "Estricto"), ("basic", "Basico"), ("none", "Sin anonimizar")], default="strict")
    active = fields.Boolean(default=True)
    last_connection_at = fields.Datetime()
    last_connection_state = fields.Selection([("unknown", "Sin probar"), ("ok", "Correcto"), ("error", "Error")], default="unknown")
    last_error = fields.Text()

    def action_test_connection(self):
        self.ensure_one()
        from ..services.legal_client import BOELegalClient

        try:
            BOELegalClient(timeout=self.timeout_seconds).get_metadatos("BOE-A-2007-13409")
            self.write({"last_connection_at": fields.Datetime.now(), "last_connection_state": "ok", "last_error": False})
        except Exception as error:
            self.write({"last_connection_at": fields.Datetime.now(), "last_connection_state": "error", "last_error": str(error)})
        return True
