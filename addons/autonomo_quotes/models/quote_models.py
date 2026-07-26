from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AutonomoTravelRate(models.Model):
    _name = "autonomo.travel.rate"
    _description = "Tarifa de desplazamiento"
    _order = "company_id, name"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    origin_city = fields.Char(string="Ciudad origen")
    origin_address = fields.Char(string="Direccion origen")
    free_radius_km = fields.Float(string="Radio gratuito (km)")
    price_per_km = fields.Monetary(string="Precio por km", currency_field="currency_id")
    minimum_charge = fields.Monetary(string="Cargo minimo", currency_field="currency_id")
    round_trip = fields.Boolean(string="Ida y vuelta", default=True)
    include_fuel = fields.Boolean(string="Incluye combustible")
    include_vehicle_costs = fields.Boolean(string="Incluye costes vehiculo")
    include_tolls = fields.Boolean(string="Incluye peajes")
    include_parking = fields.Boolean(string="Incluye aparcamiento")
    valid_from = fields.Date(string="Valido desde")
    valid_to = fields.Date(string="Valido hasta")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="company_id.currency_id", store=True, readonly=True)

    @api.constrains("free_radius_km", "price_per_km", "minimum_charge")
    def _check_non_negative(self):
        for rate in self:
            if rate.free_radius_km < 0 or rate.price_per_km < 0 or rate.minimum_charge < 0:
                raise ValidationError("Los importes y kilometros no pueden ser negativos.")


class AutonomoCostItem(models.Model):
    _name = "autonomo.cost.item"
    _description = "Concepto de coste"
    _order = "company_id, cost_type, name"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", required=True, default=lambda self: self.env.company)
    cost_type = fields.Selection(
        [
            ("material", "Material"),
            ("labor", "Mano de obra"),
            ("travel", "Desplazamiento"),
            ("fuel", "Combustible"),
            ("tool", "Herramienta"),
            ("rental", "Alquiler"),
            ("parking", "Aparcamiento"),
            ("toll", "Peaje"),
            ("diet", "Dieta"),
            ("overnight", "Alojamiento"),
            ("subcontract", "Subcontrata"),
            ("waste", "Residuos"),
            ("other", "Otro"),
        ],
        string="Tipo de coste",
        required=True,
        default="material",
    )
    product_id = fields.Many2one("product.product", string="Producto")
    internal_cost = fields.Monetary(string="Coste interno", currency_field="currency_id")
    sale_price = fields.Monetary(string="Precio de venta", currency_field="currency_id")
    uom_id = fields.Many2one("uom.uom", string="Unidad de medida")
    reusable = fields.Boolean(string="Reutilizable")
    charge_method = fields.Selection(
        [("unit", "Por unidad"), ("hour", "Por hora"), ("day", "Por dia"), ("fixed", "Fijo"), ("included", "Incluido")],
        string="Metodo de cobro",
        default="unit",
    )
    default_margin_percent = fields.Float(string="Margen por defecto (%)")
    tax_ids = fields.Many2many("account.tax", string="Impuestos")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="company_id.currency_id", store=True, readonly=True)


class AutonomoQuoteSurcharge(models.Model):
    _name = "autonomo.quote.surcharge"
    _description = "Recargo de presupuesto"
    _order = "sale_order_id, sequence"

    sale_order_id = fields.Many2one("sale.order", string="Presupuesto", ondelete="cascade")
    sequence = fields.Integer(string="Secuencia", default=10)
    name = fields.Char(string="Nombre", required=True)
    surcharge_type = fields.Selection([("fixed", "Importe fijo"), ("percent", "Porcentaje")], string="Tipo", default="fixed")
    percent = fields.Float(string="Porcentaje")
    amount = fields.Monetary(string="Importe", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="sale_order_id.currency_id", store=True, readonly=True)
    notes = fields.Text(string="Notas")


class AutonomoQuoteMaterialLine(models.Model):
    _name = "autonomo.quote.material.line"
    _description = "Material previsto de presupuesto"
    _order = "sale_order_id, sequence, id"

    sale_order_id = fields.Many2one("sale.order", string="Presupuesto", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Secuencia", default=10)
    product_id = fields.Many2one("product.product", string="Producto")
    name = fields.Char(string="Descripcion", required=True)
    material_kind = fields.Selection(
        [
            ("wood", "Madera"),
            ("hardware", "Tornilleria"),
            ("tube", "Tubo o perfil"),
            ("board", "Tablero"),
            ("paint", "Pintura o acabado"),
            ("service", "Servicio externo"),
            ("other", "Otro"),
        ],
        string="Tipo de material",
        default="other",
    )
    quantity = fields.Float(string="Cantidad", default=1.0)
    uom_id = fields.Many2one("uom.uom", string="Unidad de medida")
    length = fields.Float(string="Largo")
    width = fields.Float(string="Ancho")
    thickness = fields.Float(string="Grosor")
    dimension_note = fields.Char(string="Detalle de medidas")
    planned_unit_price = fields.Monetary(string="Precio previsto unitario", currency_field="currency_id")
    planned_amount = fields.Monetary(string="Importe previsto", compute="_compute_amounts", store=True, currency_field="currency_id")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Linea de presupuesto")
    purchase_line_id = fields.Many2one("purchase.order.line", string="Linea de compra relacionada")
    purchase_order_id = fields.Many2one("purchase.order", string="Compra", related="purchase_line_id.order_id", store=True, readonly=True)
    include_in_customer_report = fields.Boolean(string="Mostrar al cliente", default=True)
    state = fields.Selection(
        [
            ("planned", "Previsto"),
            ("quoted", "Incluido en presupuesto"),
            ("purchased", "Comprado"),
            ("cancelled", "Cancelado"),
        ],
        string="Estado",
        default="planned",
    )
    notes = fields.Text(string="Notas")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="sale_order_id.currency_id", store=True, readonly=True)

    @api.depends("quantity", "planned_unit_price")
    def _compute_amounts(self):
        for line in self:
            line.planned_amount = line.quantity * line.planned_unit_price

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.name = line.name or line.product_id.display_name
                line.uom_id = line.uom_id or line.product_id.uom_id
                line.planned_unit_price = line.planned_unit_price or line.product_id.lst_price

    @api.constrains("quantity", "planned_unit_price", "length", "width", "thickness")
    def _check_non_negative(self):
        for line in self:
            if line.quantity < 0 or line.planned_unit_price < 0 or line.length < 0 or line.width < 0 or line.thickness < 0:
                raise ValidationError("Las cantidades, precios y medidas no pueden ser negativos.")


class AutonomoQuoteTemplate(models.Model):
    _name = "autonomo.quote.template"
    _description = "Plantilla de presupuesto"
    _order = "company_id, name"

    name = fields.Char(string="Nombre", required=True)
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.company, required=True)
    quote_type = fields.Selection([("installation", "Instalacion"), ("repair", "Reparacion"), ("custom", "A medida")], string="Tipo", default="custom")
    activity_id = fields.Many2one("autonomo.activity", string="Actividad")
    line_ids = fields.One2many("autonomo.quote.template.line", "template_id", string="Lineas")
    active = fields.Boolean(string="Activo", default=True)
    notes = fields.Text(string="Notas")


class AutonomoQuoteTemplateLine(models.Model):
    _name = "autonomo.quote.template.line"
    _description = "Linea de plantilla de presupuesto"
    _order = "template_id, sequence"

    template_id = fields.Many2one("autonomo.quote.template", string="Plantilla", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Secuencia", default=10)
    cost_item_id = fields.Many2one("autonomo.cost.item", string="Concepto")
    product_id = fields.Many2one("product.product", string="Producto")
    name = fields.Char(string="Descripcion", required=True)
    quantity = fields.Float(string="Cantidad", default=1.0)
    price_unit = fields.Monetary(string="Precio unitario", currency_field="currency_id")
    internal_cost = fields.Monetary(string="Coste interno", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="template_id.company_id.currency_id", store=True, readonly=True)


class AutonomoQuoteVersion(models.Model):
    _name = "autonomo.quote.version"
    _description = "Version de presupuesto"
    _order = "sale_order_id, version_number desc"

    sale_order_id = fields.Many2one("sale.order", string="Presupuesto", required=True, ondelete="cascade")
    version_number = fields.Integer(string="Version", required=True)
    state_snapshot = fields.Char(string="Estado")
    amount_untaxed = fields.Monetary(string="Base imponible", currency_field="currency_id")
    amount_total = fields.Monetary(string="Total", currency_field="currency_id")
    estimated_total_cost = fields.Monetary(string="Coste total estimado", currency_field="currency_id")
    estimated_profit = fields.Monetary(string="Beneficio estimado", currency_field="currency_id")
    snapshot_date = fields.Datetime(string="Fecha snapshot", default=fields.Datetime.now)
    snapshot_hash = fields.Char(string="Hash snapshot")
    notes = fields.Text(string="Notas")
    currency_id = fields.Many2one("res.currency", string="Moneda", related="sale_order_id.currency_id", store=True, readonly=True)


class AutonomoWorkMeasurement(models.Model):
    _name = "autonomo.work.measurement"
    _description = "Medicion de trabajo"
    _order = "sale_order_id, sequence"

    sale_order_id = fields.Many2one("sale.order", string="Presupuesto", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Secuencia", default=10)
    name = fields.Char(string="Concepto", required=True)
    area = fields.Char(string="Zona")
    length = fields.Float(string="Largo")
    width = fields.Float(string="Ancho")
    height = fields.Float(string="Alto")
    quantity = fields.Float(string="Cantidad", default=1.0)
    uom_id = fields.Many2one("uom.uom", string="Unidad")
    notes = fields.Text(string="Notas")
