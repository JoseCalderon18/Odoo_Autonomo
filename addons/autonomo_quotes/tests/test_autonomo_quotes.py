from odoo.tests.common import TransactionCase, tagged


@tagged("at_install", "-post_install")
class TestAutonomoQuotes(TransactionCase):
    def test_travel_and_margin(self):
        partner = self.env["res.partner"].create({"name": "Cliente test quotes"})
        product = self.env["product.product"].create({"name": "Servicio test", "type": "service", "list_price": 100})
        rate = self.env["autonomo.travel.rate"].create({
            "name": "Tarifa test",
            "company_id": self.env.company.id,
            "free_radius_km": 10,
            "price_per_km": 1,
            "minimum_charge": 15,
            "round_trip": True,
        })
        order = self.env["sale.order"].create({
            "partner_id": partner.id,
            "travel_rate_id": rate.id,
            "distance_one_way_km": 20,
            "labor_hours": 2,
            "labor_hour_price": 30,
            "client_material_amount": 45,
            "estimated_material_cost": 20,
            "order_line": [(0, 0, {"product_id": product.id, "product_uom_qty": 1, "price_unit": 100})],
        })
        self.assertEqual(order.distance_total_km, 40)
        self.assertEqual(order.billable_distance_km, 30)
        self.assertEqual(order.travel_amount, 30)
        self.assertEqual(order.labor_amount, 60)
        self.assertTrue(order.estimated_total_cost)
        order.action_create_quote_version()
        self.assertEqual(len(order.quote_version_ids), 1)
        self.env["autonomo.quote.material.line"].create({
            "sale_order_id": order.id,
            "name": "Tablero test",
            "quantity": 2,
            "planned_unit_price": 25,
            "include_in_customer_report": True,
        })
        order.action_sync_materials_to_quote()
        self.assertEqual(order.client_material_amount, 50)
        report = self.env.ref("autonomo_quotes.action_report_autonomo_quote_cost_sheet")
        pdf_content, content_type = report._render_qweb_pdf(report.report_name, [order.id])
        self.assertIn(content_type, ("pdf", "html"))
        self.assertTrue(pdf_content)
        standard_report = self.env.ref("sale.action_report_saleorder")
        standard_content, standard_type = standard_report._render_qweb_pdf(standard_report.report_name, [order.id])
        self.assertIn(standard_type, ("pdf", "html"))
        self.assertTrue(standard_content)
