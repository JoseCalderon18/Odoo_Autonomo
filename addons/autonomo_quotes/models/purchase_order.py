from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    autonomo_sale_order_id = fields.Many2one("sale.order", string="Presupuesto relacionado")


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    autonomo_sale_order_id = fields.Many2one(
        "sale.order",
        string="Presupuesto relacionado",
        related="order_id.autonomo_sale_order_id",
        store=True,
        readonly=True,
    )
    autonomo_quote_material_line_id = fields.Many2one(
        "autonomo.quote.material.line",
        string="Material previsto relacionado",
    )

    def _sync_material_line_link(self):
        if self.env.context.get("skip_autonomo_material_sync"):
            return
        for line in self.filtered("autonomo_quote_material_line_id"):
            material = line.autonomo_quote_material_line_id
            values = {"purchase_line_id": line.id}
            if line.order_id.autonomo_sale_order_id and material.sale_order_id != line.order_id.autonomo_sale_order_id:
                values["sale_order_id"] = line.order_id.autonomo_sale_order_id.id
            material.with_context(skip_autonomo_material_sync=True).write(values)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_material_line_link()
        return records

    def write(self, vals):
        result = super().write(vals)
        if "autonomo_quote_material_line_id" in vals or "order_id" in vals:
            self._sync_material_line_link()
        return result
