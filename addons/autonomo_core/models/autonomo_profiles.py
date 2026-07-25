from odoo import fields, models


class AutonomoCensusProfile(models.Model):
    _name = "autonomo.census.profile"
    _description = "Perfil censal autonomo"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, ondelete="cascade")
    tax_identification_number = fields.Char()
    census_status = fields.Selection([("draft", "Borrador"), ("active", "Alta"), ("modified", "Modificado"), ("inactive", "Baja")], default="draft")
    census_start_date = fields.Date()
    census_end_date = fields.Date()
    tax_residence_country_id = fields.Many2one("res.country")
    fiscal_address_partner_id = fields.Many2one("res.partner", check_company=True)
    notification_address_partner_id = fields.Many2one("res.partner", check_company=True)
    main_activity_id = fields.Many2one("autonomo.activity")
    activity_start_date = fields.Date()
    usual_operations_start_date = fields.Date()
    iae_codes_json = fields.Json()
    cnae_codes_json = fields.Json()
    vat_taxpayer = fields.Boolean()
    vat_regime = fields.Selection(
        [("general", "General"), ("cash_criterion", "Criterio de caja"), ("simplified", "Simplificado"), ("exempt", "Exento"), ("other", "Otro")]
    )
    irpf_estimation_method = fields.Selection(
        [("direct_simplified", "Estimacion directa simplificada"), ("direct_normal", "Estimacion directa normal"), ("objective", "Estimacion objetiva")]
    )
    withholding_work_obligation = fields.Boolean()
    withholding_professional_obligation = fields.Boolean()
    withholding_rent_obligation = fields.Boolean()
    intracommunity_operator = fields.Boolean()
    cash_criterion = fields.Boolean()
    special_vat_sector = fields.Boolean()
    business_premises = fields.Boolean()
    premises_reference = fields.Char()
    representative_partner_id = fields.Many2one("res.partner", check_company=True)
    electronic_notifications_enabled = fields.Boolean()
    last_036_submission_id = fields.Many2one("autonomo.submission")
    verified_at = fields.Datetime()
    notes = fields.Text()

    _company_uniq = models.Constraint(
        "UNIQUE(company_id)",
        "Solo puede existir un perfil censal por empresa en autonomo_core.",
    )


class AutonomoSocialSecurityProfile(models.Model):
    _name = "autonomo.social.security.profile"
    _description = "Perfil Seguridad Social RETA"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, ondelete="cascade")
    social_security_number_encrypted = fields.Char(groups="autonomo_core.group_autonomo_admin")
    reta_status = fields.Selection([("draft", "Borrador"), ("active", "Alta"), ("modified", "Modificado"), ("inactive", "Baja")], default="draft")
    reta_start_date = fields.Date()
    reta_end_date = fields.Date()
    iae_code = fields.Char()
    cnae_code = fields.Char()
    activity_start_date = fields.Date()
    activity_address_partner_id = fields.Many2one("res.partner", check_company=True)
    estimated_annual_net_returns = fields.Monetary(currency_field="currency_id")
    selected_contribution_base = fields.Monetary(currency_field="currency_id")
    contribution_bracket_code = fields.Char()
    mutual_insurance_name = fields.Char()
    mutual_insurance_code = fields.Char()
    coverage_options_json = fields.Json()
    benefit_or_reduction_code = fields.Char()
    bank_account_id = fields.Many2one("res.partner.bank", groups="autonomo_core.group_autonomo_admin")
    bank_account_holder_partner_id = fields.Many2one("res.partner", check_company=True)
    bank_holder_authorization_attachment_id = fields.Many2one("ir.attachment", groups="autonomo_core.group_autonomo_admin")
    linked_company = fields.Boolean()
    community_property_member = fields.Boolean()
    family_collaborator = fields.Boolean()
    trade_dependent_worker = fields.Boolean()
    last_reta_submission_id = fields.Many2one("autonomo.submission")
    verified_at = fields.Datetime()
    notes = fields.Text()
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", store=True, readonly=True)

    _company_uniq = models.Constraint(
        "UNIQUE(company_id)",
        "Solo puede existir un perfil RETA por empresa en autonomo_core.",
    )
