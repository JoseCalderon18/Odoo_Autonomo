from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    activity_id = fields.Many2one("autonomo.activity", check_company=True)
    work_site_partner_id = fields.Many2one("res.partner", check_company=True)
    scope_description = fields.Text()
    estimated_cost = fields.Monetary(currency_field="currency_id")
    estimated_margin = fields.Monetary(compute="_compute_estimated_margin", store=True, currency_field="currency_id")
    estimated_margin_percent = fields.Float(compute="_compute_estimated_margin", store=True)
    requires_advance = fields.Boolean()
    advance_percent = fields.Float()
    tax_review_state = fields.Selection(
        [("pending", "Pendiente"), ("ok", "Revisado"), ("warning", "Aviso"), ("blocked", "Bloqueado")],
        default="pending",
    )

    @api.depends("amount_untaxed", "estimated_cost")
    def _compute_estimated_margin(self):
        for order in self:
            order.estimated_margin = order.amount_untaxed - order.estimated_cost
            order.estimated_margin_percent = order.amount_untaxed and (order.estimated_margin / order.amount_untaxed) * 100 or 0.0

    @api.constrains("advance_percent")
    def _check_advance_percent(self):
        for order in self:
            if order.advance_percent < 0 or order.advance_percent > 100:
                raise ValidationError("El anticipo debe estar entre 0 y 100%.")
