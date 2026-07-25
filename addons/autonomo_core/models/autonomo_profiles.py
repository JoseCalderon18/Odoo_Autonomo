from odoo import fields, models


class AutonomoCensusProfile(models.Model):
    _name = "autonomo.census.profile"
    _description = "Perfil censal autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company, ondelete="cascade")
    tax_identification_number = fields.Char(string="NIF")
    census_status = fields.Selection([("draft", "Borrador"), ("active", "Alta"), ("modified", "Modificado"), ("inactive", "Baja")], string="Estado censal", default="draft")
    census_start_date = fields.Date(string="Fecha alta censal")
    census_end_date = fields.Date(string="Fecha baja censal")
    tax_residence_country_id = fields.Many2one("res.country", string="Pais de residencia fiscal")
    fiscal_address_partner_id = fields.Many2one("res.partner", string="Direccion fiscal", check_company=True)
    notification_address_partner_id = fields.Many2one("res.partner", string="Direccion de notificaciones", check_company=True)
    main_activity_id = fields.Many2one("autonomo.activity", string="Actividad principal")
    activity_start_date = fields.Date(string="Fecha inicio actividad")
    usual_operations_start_date = fields.Date(string="Inicio operaciones habituales")
    iae_codes_json = fields.Json(string="Codigos IAE")
    cnae_codes_json = fields.Json(string="Codigos CNAE")
    vat_taxpayer = fields.Boolean(string="Sujeto pasivo IVA")
    vat_regime = fields.Selection(
        [("general", "General"), ("cash_criterion", "Criterio de caja"), ("simplified", "Simplificado"), ("exempt", "Exento"), ("other", "Otro")],
        string="Regimen de IVA",
    )
    irpf_estimation_method = fields.Selection(
        [("direct_simplified", "Estimacion directa simplificada"), ("direct_normal", "Estimacion directa normal"), ("objective", "Estimacion objetiva")],
        string="Metodo de estimacion IRPF",
    )
    withholding_work_obligation = fields.Boolean(string="Obligacion de retener por trabajo")
    withholding_professional_obligation = fields.Boolean(string="Obligacion de retener profesionales")
    withholding_rent_obligation = fields.Boolean(string="Obligacion de retener alquileres")
    intracommunity_operator = fields.Boolean(string="Operador intracomunitario")
    cash_criterion = fields.Boolean(string="Criterio de caja")
    special_vat_sector = fields.Boolean(string="Sector diferenciado IVA")
    business_premises = fields.Boolean(string="Local afecto a la actividad")
    premises_reference = fields.Char(string="Referencia del local")
    representative_partner_id = fields.Many2one("res.partner", string="Representante", check_company=True)
    electronic_notifications_enabled = fields.Boolean(string="Notificaciones electronicas activadas")
    last_036_submission_id = fields.Many2one("autonomo.submission", string="Ultima presentacion 036")
    verified_at = fields.Datetime(string="Fecha de verificacion")
    notes = fields.Text(string="Notas")

    _company_uniq = models.Constraint(
        "UNIQUE(company_id)",
        "Solo puede existir un perfil censal por empresa en autonomo_core.",
    )


class AutonomoSocialSecurityProfile(models.Model):
    _name = "autonomo.social.security.profile"
    _description = "Perfil Seguridad Social RETA"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company, ondelete="cascade")
    social_security_number_encrypted = fields.Char(string="NSS protegido", groups="autonomo_core.group_autonomo_admin")
    reta_status = fields.Selection([("draft", "Borrador"), ("active", "Alta"), ("modified", "Modificado"), ("inactive", "Baja")], string="Estado RETA", default="draft")
    reta_start_date = fields.Date(string="Fecha alta RETA")
    reta_end_date = fields.Date(string="Fecha baja RETA")
    iae_code = fields.Char(string="Epigrafe IAE")
    cnae_code = fields.Char(string="Codigo CNAE")
    activity_start_date = fields.Date(string="Fecha inicio actividad")
    activity_address_partner_id = fields.Many2one("res.partner", string="Direccion de actividad", check_company=True)
    estimated_annual_net_returns = fields.Monetary(string="Rendimientos netos anuales estimados", currency_field="currency_id")
    selected_contribution_base = fields.Monetary(string="Base de cotizacion seleccionada", currency_field="currency_id")
    contribution_bracket_code = fields.Char(string="Codigo de tramo")
    mutual_insurance_name = fields.Char(string="Mutua colaboradora")
    mutual_insurance_code = fields.Char(string="Codigo mutua")
    coverage_options_json = fields.Json(string="Opciones de cobertura")
    benefit_or_reduction_code = fields.Char(string="Codigo beneficio o reduccion")
    bank_account_id = fields.Many2one("res.partner.bank", string="Cuenta bancaria", groups="autonomo_core.group_autonomo_admin")
    bank_account_holder_partner_id = fields.Many2one("res.partner", string="Titular de la cuenta", check_company=True)
    bank_holder_authorization_attachment_id = fields.Many2one("ir.attachment", string="Autorizacion titular cuenta", groups="autonomo_core.group_autonomo_admin")
    linked_company = fields.Boolean(string="Sociedad vinculada")
    community_property_member = fields.Boolean(string="Comunero")
    family_collaborator = fields.Boolean(string="Familiar colaborador")
    trade_dependent_worker = fields.Boolean(string="TRADE")
    last_reta_submission_id = fields.Many2one("autonomo.submission", string="Ultima presentacion RETA")
    verified_at = fields.Datetime(string="Fecha de verificacion")
    notes = fields.Text(string="Notas")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="company_id.currency_id", store=True, readonly=True)

    _company_uniq = models.Constraint(
        "UNIQUE(company_id)",
        "Solo puede existir un perfil RETA por empresa en autonomo_core.",
    )
