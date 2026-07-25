from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("at_install", "-post_install")
class TestAutonomoAiReview(TransactionCase):
    def test_review_requires_citation_to_accept(self):
        review = self.env["autonomo.ai.review"].create({"question": "¿Es aceptable?", "answer": "Sin fuente", "requires_human_review": False})
        with self.assertRaises(UserError):
            review.action_accept()
        review.write({
            "citation_ids": [(0, 0, {"title": "Fuente test", "official_url": "https://www.boe.es/", "verified_at": "2026-07-25 19:00:00"})],
            "risk_level": "low",
        })
        review.action_accept()
        self.assertEqual(review.state, "accepted")

    def test_create_issue(self):
        review = self.env["autonomo.ai.review"].create({"question": "Falta algo", "answer": "Crear incidencia"})
        review.action_create_issue()
        self.assertTrue(review.issue_ids)
