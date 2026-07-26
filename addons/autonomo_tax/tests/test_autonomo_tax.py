from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("at_install", "-post_install")
class TestAutonomoTax(TransactionCase):
    def test_return_requires_verified_source(self):
        obligation = self.env["autonomo.tax.obligation"].create({
            "company_id": self.env.company.id,
            "tax_kind": "vat",
            "model_code": "303",
            "periodicity": "quarterly",
        })
        period = self.env["autonomo.tax.period"].create({
            "company_id": self.env.company.id,
            "fiscal_year": 2026,
            "period_type": "quarterly",
            "period_code": "2T",
            "date_start": "2026-04-01",
            "date_end": "2026-06-30",
        })
        tax_return = self.env["autonomo.tax.return"].create({"obligation_id": obligation.id, "period_id": period.id})
        with self.assertRaises(UserError):
            tax_return.action_mark_ready()
        tax_return.source_verified = True
        tax_return.action_mark_ready()
        self.assertEqual(tax_return.state, "ready")
        tax_return.action_create_snapshot()
        self.assertTrue(tax_return.book_snapshot_ids.snapshot_hash)

    def test_asset_percentages(self):
        with self.assertRaises(ValidationError):
            self.env["autonomo.investment.asset"].create({"name": "Activo test", "vat_deductible_percent": 120})
