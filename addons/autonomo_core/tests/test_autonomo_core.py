from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("at_install", "-post_install")
class TestAutonomoCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company

    def test_activity_constraints(self):
        activity = self.env["autonomo.activity"].create(
            {
                "name": "Actividad test",
                "code": "TEST-ACT",
                "company_id": self.company.id,
                "vat_deductible_default_percent": 75,
            }
        )
        self.assertEqual(activity.vat_deductible_default_percent, 75)
        with self.assertRaises(ValidationError):
            activity.vat_deductible_default_percent = 101
        with self.assertRaises(ValidationError):
            self.env["autonomo.activity"].create(
                {
                    "name": "Fechas mal",
                    "code": "TEST-DATE",
                    "company_id": self.company.id,
                    "start_date": "2026-12-31",
                    "end_date": "2026-01-01",
                }
            )

    def test_tax_category_percentages(self):
        with self.assertRaises(ValidationError):
            self.env["autonomo.tax.category"].create(
                {
                    "name": "Categoria test",
                    "code": "TEST-CAT",
                    "company_id": self.company.id,
                    "default_irpf_deductible_percent": -1,
                }
            )

    def test_submission_checklist_blocks_ready(self):
        procedure = self.env["autonomo.procedure"].create(
            {
                "name": "Tramite test",
                "code": "TEST-PROC",
                "company_id": self.company.id,
                "authority": "aeat",
                "procedure_type": "registration",
            }
        )
        self.env["autonomo.procedure.requirement"].create(
            {
                "procedure_id": procedure.id,
                "name": "Dato obligatorio",
                "requirement_type": "field",
                "mandatory": True,
            }
        )
        submission = self.env["autonomo.submission"].create(
            {
                "name": "Presentacion test",
                "company_id": self.company.id,
                "procedure_id": procedure.id,
            }
        )
        submission.action_refresh_checklist()
        self.assertEqual(submission.checklist_state, "incomplete")
        with self.assertRaises(UserError):
            submission.action_mark_ready()
        line = submission.checklist_line_ids[0]
        line.write({"data_present": True, "verified": True})
        submission.action_mark_ready()
        self.assertEqual(submission.state, "ready")

    def test_reports_render(self):
        activity = self.env["autonomo.activity"].create(
            {"name": "Actividad PDF", "code": "TEST-PDF-A", "company_id": self.company.id}
        )
        category = self.env["autonomo.tax.category"].create(
            {"name": "Categoria PDF", "code": "TEST-PDF-C", "company_id": self.company.id}
        )
        census_company = self.env["res.company"].create({"name": "Empresa test censal"})
        reta_company = self.env["res.company"].create({"name": "Empresa test RETA"})
        census = self.env["autonomo.census.profile"].create({"company_id": census_company.id})
        reta = self.env["autonomo.social.security.profile"].create({"company_id": reta_company.id})

        reports = [
            ("autonomo_core.action_report_autonomo_activity", activity.id),
            ("autonomo_core.action_report_autonomo_tax_category", category.id),
            ("autonomo_core.action_report_autonomo_census_profile", census.id),
            ("autonomo_core.action_report_autonomo_reta_profile", reta.id),
        ]
        for xmlid, res_id in reports:
            report = self.env.ref(xmlid)
            pdf, extension = report.with_context(force_report_rendering=True)._render_qweb_pdf(report.report_name, [res_id])
            self.assertEqual(extension, "pdf")
            self.assertGreater(len(pdf), 100)
