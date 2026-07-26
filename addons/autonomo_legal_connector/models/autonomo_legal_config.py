from odoo import fields, models


class AutonomoLegalConfig(models.Model):
    _name = "autonomo.legal.config"
    _description = "Configuracion conector legal"
    _order = "name"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company)
    service_url = fields.Char(string="URL del servicio", default="https://www.boe.es/datosabiertos/api/legislacion-consolidada", required=True)
    auth_type = fields.Selection([("none", "Sin autenticacion"), ("token", "Token")], string="Tipo de autenticacion", default="none", required=True)
    api_token = fields.Char(string="Token API", groups="autonomo_core.group_autonomo_admin")
    timeout_seconds = fields.Integer(string="Timeout (segundos)", default=20)
    verify_ssl = fields.Boolean(string="Verificar SSL", default=True)
    anonymization_mode = fields.Selection([("strict", "Estricto"), ("basic", "Basico"), ("none", "Sin anonimizar")], string="Modo de anonimizacion", default="strict")
    active = fields.Boolean(string="Activo", default=True)
    last_connection_at = fields.Datetime(string="Ultima conexion")
    last_connection_state = fields.Selection([("unknown", "Sin probar"), ("ok", "Correcto"), ("error", "Error")], string="Estado de conexion", default="unknown")
    last_error = fields.Text(string="Ultimo error")

    def action_test_connection(self):
        self.ensure_one()
        from ..services.legal_client import BOELegalClient

        try:
            BOELegalClient(timeout=self.timeout_seconds).get_metadatos("BOE-A-2007-13409")
            self.write({"last_connection_at": fields.Datetime.now(), "last_connection_state": "ok", "last_error": False})
        except Exception as error:
            self.write({"last_connection_at": fields.Datetime.now(), "last_connection_state": "error", "last_error": str(error)})
        return True
