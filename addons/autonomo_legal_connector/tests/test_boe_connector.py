from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestBOEConnector(TransactionCase):
    def test_sync_boe_metadata_analysis_index_and_block(self):
        source = self.env["autonomo.legal.source"].create(
            {
                "name": "Estatuto autonomo test",
                "code": "BOE-A-2007-13409-TEST",
                "boe_identifier": "BOE-A-2007-13409",
                "authority": "boe",
                "source_type": "law",
                "official_url": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409",
            }
        )

        source.action_sync_boe_metadata()
        self.assertEqual(source.boe_identifier, "BOE-A-2007-13409")
        self.assertTrue(source.boe_title)
        self.assertTrue(source.boe_metadata_hash)
        self.assertTrue(source.boe_eli_url)

        source.action_sync_boe_analysis()
        self.assertTrue(source.matter_ids)
        self.assertTrue(source.relation_ids)
        self.assertTrue(source.boe_analysis_hash)

        source.action_sync_boe_metadata_eli()
        self.assertTrue(source.boe_eli_metadata_hash)

        source.action_sync_boe_index()
        block = source.block_ids.filtered(lambda item: item.block_identifier == "a1")[:1]
        self.assertTrue(block)
        self.assertTrue(source.boe_index_hash)

        block.action_sync_versions()
        self.assertTrue(block.version_ids)
        self.assertTrue(block.content_hash)
        self.assertTrue(block.version_ids[0].content_hash)

    def test_config_connection_and_query_hash(self):
        config = self.env["autonomo.legal.config"].create({"name": "BOE test"})
        config.action_test_connection()
        self.assertEqual(config.last_connection_state, "ok")

        query = self.env["autonomo.legal.query"].create(
            {
                "name": "Consulta hash",
                "question": "Revisar BOE-A-2007-13409",
                "anonymized_payload": "NIF 00000000T e IBAN ES0000000000000000000000 anonimizados antes de IA",
            }
        )
        self.assertTrue(query.payload_hash)
