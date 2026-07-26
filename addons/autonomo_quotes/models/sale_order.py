import hashlib

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quote_template_id = fields.Many2one("autonomo.quote.template", string="Plantilla de presupuesto")
    quote_type = fields.Selection([("installation", "Instalacion"), ("repair", "Reparacion"), ("custom", "A medida")], string="Tipo de presupuesto", default="custom")
    work_address = fields.Char(string="Direccion de trabajo")
    travel_rate_id = fields.Many2one("autonomo.travel.rate", string="Tarifa de desplazamiento")
    distance_one_way_km = fields.Float(string="Distancia ida (km)")
    distance_total_km = fields.Float(string="Distancia total (km)", compute="_compute_quote_amounts", store=True)
    free_distance_km = fields.Float(string="Km gratuitos", compute="_compute_quote_amounts", store=True)
    billable_distance_km = fields.Float(string="Km facturables", compute="_compute_quote_amounts", store=True)
    labor_hours = fields.Float(string="Horas de trabajo")
    labor_hour_price = fields.Monetary(string="Precio hora", currency_field="currency_id")
    labor_amount = fields.Monetary(string="Importe mano de obra", compute="_compute_quote_amounts", store=True, currency_field="currency_id")
    client_material_amount = fields.Monetary(string="Materiales a mostrar al cliente", currency_field="currency_id")
    travel_amount = fields.Monetary(string="Importe desplazamiento", compute="_compute_quote_amounts", store=True, currency_field="currency_id")
    fuel_amount = fields.Monetary(string="Combustible", currency_field="currency_id")
    parking_amount = fields.Monetary(string="Aparcamiento", currency_field="currency_id")
    toll_amount = fields.Monetary(string="Peajes", currency_field="currency_id")
    diet_amount = fields.Monetary(string="Dietas", currency_field="currency_id")
    overnight_amount = fields.Monetary(string="Alojamiento", currency_field="currency_id")
    other_travel_amount = fields.Monetary(string="Otros desplazamientos", currency_field="currency_id")
    estimated_material_cost = fields.Monetary(string="Coste materiales", currency_field="currency_id")
    estimated_labor_cost = fields.Monetary(string="Coste mano de obra", currency_field="currency_id")
    estimated_tool_cost = fields.Monetary(string="Coste herramientas", currency_field="currency_id")
    estimated_subcontract_cost = fields.Monetary(string="Coste subcontratas", currency_field="currency_id")
    estimated_total_cost = fields.Monetary(string="Coste total estimado", compute="_compute_quote_amounts", store=True, currency_field="currency_id")
    estimated_profit = fields.Monetary(string="Beneficio estimado", compute="_compute_quote_amounts", store=True, currency_field="currency_id")
    quote_estimated_margin_percent = fields.Float(string="Margen presupuesto (%)", compute="_compute_quote_amounts", store=True)
    advance_amount = fields.Monetary(string="Importe anticipo", compute="_compute_quote_amounts", store=True, currency_field="currency_id")
    quote_version = fields.Integer(string="Version", default=1)
    measurement_ids = fields.One2many("autonomo.work.measurement", "sale_order_id", string="Mediciones")
    surcharge_ids = fields.One2many("autonomo.quote.surcharge", "sale_order_id", string="Recargos")
    quote_version_ids = fields.One2many("autonomo.quote.version", "sale_order_id", string="Versiones")
    special_conditions = fields.Text(string="Condiciones especiales")
    quote_internal_notes = fields.Text(string="Notas internas de presupuesto")
    manual_travel_override = fields.Boolean(string="Desplazamiento manual")
    manual_travel_reason = fields.Char(string="Motivo ajuste desplazamiento")

    @api.depends(
        "distance_one_way_km",
        "travel_rate_id",
        "travel_rate_id.round_trip",
        "travel_rate_id.free_radius_km",
        "travel_rate_id.price_per_km",
        "travel_rate_id.minimum_charge",
        "labor_hours",
        "labor_hour_price",
        "fuel_amount",
        "parking_amount",
        "toll_amount",
        "diet_amount",
        "overnight_amount",
        "other_travel_amount",
        "estimated_material_cost",
        "estimated_labor_cost",
        "estimated_tool_cost",
        "estimated_subcontract_cost",
        "amount_untaxed",
        "advance_percent",
    )
    def _compute_quote_amounts(self):
        for order in self:
            multiplier = 2.0 if order.travel_rate_id.round_trip else 1.0
            order.distance_total_km = order.distance_one_way_km * multiplier
            order.free_distance_km = min(order.distance_total_km, order.travel_rate_id.free_radius_km or 0.0)
            order.billable_distance_km = max(order.distance_total_km - order.free_distance_km, 0.0)
            travel = order.billable_distance_km * (order.travel_rate_id.price_per_km or 0.0)
            if travel and order.travel_rate_id.minimum_charge:
                travel = max(travel, order.travel_rate_id.minimum_charge)
            order.travel_amount = travel
            order.labor_amount = order.labor_hours * order.labor_hour_price
            travel_costs = order.travel_amount + order.diet_amount + order.overnight_amount + order.other_travel_amount
            if not order.travel_rate_id.include_fuel:
                travel_costs += order.fuel_amount
            if not order.travel_rate_id.include_parking:
                travel_costs += order.parking_amount
            if not order.travel_rate_id.include_tolls:
                travel_costs += order.toll_amount
            order.estimated_total_cost = (
                order.estimated_material_cost
                + order.estimated_labor_cost
                + order.estimated_tool_cost
                + order.estimated_subcontract_cost
                + travel_costs
            )
            order.estimated_profit = order.amount_untaxed - order.estimated_total_cost
            order.quote_estimated_margin_percent = order.amount_untaxed and order.estimated_profit / order.amount_untaxed * 100.0 or 0.0
            order.advance_amount = order.amount_total * (order.advance_percent or 0.0) / 100.0

    @api.constrains("labor_hours", "distance_one_way_km")
    def _check_positive_quote_values(self):
        for order in self:
            if order.labor_hours < 0 or order.distance_one_way_km < 0:
                raise ValidationError("Horas y kilometros no pueden ser negativos.")

    def action_apply_quote_template(self):
        for order in self:
            if not order.quote_template_id:
                continue
            lines = []
            for line in order.quote_template_id.line_ids:
                product = line.product_id or line.cost_item_id.product_id
                lines.append((0, 0, {
                    "product_id": product.id if product else False,
                    "name": line.name,
                    "product_uom_qty": line.quantity,
                    "price_unit": line.price_unit or line.cost_item_id.sale_price,
                }))
            if lines:
                order.write({"order_line": lines, "activity_id": order.quote_template_id.activity_id.id or order.activity_id.id})
        return True

    def action_create_quote_version(self):
        for order in self:
            number = (max(order.quote_version_ids.mapped("version_number") or [0]) + 1)
            payload = f"{order.name}|{order.amount_total}|{order.estimated_total_cost}|{fields.Datetime.now()}"
            self.env["autonomo.quote.version"].create({
                "sale_order_id": order.id,
                "version_number": number,
                "state_snapshot": order.state,
                "amount_untaxed": order.amount_untaxed,
                "amount_total": order.amount_total,
                "estimated_total_cost": order.estimated_total_cost,
                "estimated_profit": order.estimated_profit,
                "snapshot_hash": hashlib.sha256(payload.encode()).hexdigest(),
            })
            order.quote_version = number
        return True
