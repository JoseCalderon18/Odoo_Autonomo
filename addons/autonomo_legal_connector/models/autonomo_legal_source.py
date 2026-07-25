import hashlib

from odoo import api, fields, models


def _parse_boe_date(value):
    if not value:
        return False
    if len(value) >= 8:
        return f"{value[0:4]}-{value[4:6]}-{value[6:8]}"
    return False


class AutonomoLegalSource(models.Model):
    _inherit = "autonomo.legal.source"

    boe_identifier = fields.Char(index=True)
    boe_update_at = fields.Datetime(string="Fecha actualizacion BOE")
    boe_scope_code = fields.Char()
    boe_scope_name = fields.Char()
    boe_department_code = fields.Char()
    boe_department_name = fields.Char()
    boe_rank_code = fields.Char()
    boe_rank_name = fields.Char()
    boe_disposition_date = fields.Date()
    boe_official_number = fields.Char()
    boe_title = fields.Char()
    boe_journal = fields.Char()
    boe_journal_number = fields.Char()
    boe_effective_date = fields.Date()
    boe_derogation_status = fields.Selection([("N", "No derogada"), ("S", "Derogada"), ("unknown", "Desconocido")], default="unknown")
    boe_annulment_status = fields.Selection([("N", "No anulada"), ("S", "Anulada"), ("unknown", "Desconocido")], default="unknown")
    boe_expired_validity = fields.Selection([("N", "No agotada"), ("S", "Agotada"), ("unknown", "Desconocido")], default="unknown")
    boe_consolidation_state_code = fields.Char()
    boe_consolidation_state = fields.Char()
    boe_eli_url = fields.Char()
    boe_eli_metadata_hash = fields.Char()
    boe_eli_metadata_xml = fields.Text()
    boe_html_consolidated_url = fields.Char()
    boe_metadata_hash = fields.Char()
    boe_analysis_hash = fields.Char()
    boe_index_hash = fields.Char()
    boe_last_sync_at = fields.Datetime()
    boe_sync_state = fields.Selection([("pending", "Pendiente"), ("ok", "Correcto"), ("error", "Error")], default="pending")
    boe_last_error = fields.Text()
    matter_ids = fields.One2many("autonomo.legal.matter", "source_id")
    relation_ids = fields.One2many("autonomo.legal.relation", "source_id")
    block_ids = fields.One2many("autonomo.legal.block", "source_id")

    def action_sync_boe_metadata(self):
        for source in self:
            source._sync_boe_metadata()
        return True

    def action_sync_boe_analysis(self):
        for source in self:
            source._sync_boe_analysis()
        return True

    def action_sync_boe_metadata_eli(self):
        for source in self:
            source._sync_boe_metadata_eli()
        return True

    def action_sync_boe_index(self):
        for source in self:
            source._sync_boe_index()
        return True

    def action_sync_boe_full(self):
        for source in self:
            source._sync_boe_metadata()
            source._sync_boe_metadata_eli()
            source._sync_boe_analysis()
            source._sync_boe_index()
        return True

    def action_sync_boe_block_versions(self):
        for source in self:
            for block in source.block_ids:
                block._sync_versions()
        return True

    def _client(self):
        from ..services.legal_client import BOELegalClient

        return BOELegalClient()

    def _sync_log(self, sync_type):
        self.ensure_one()
        return self.env["autonomo.legal.sync.status"].create(
            {"name": f"{self.code} {sync_type}", "source_id": self.id, "boe_identifier": self.boe_identifier or self.code, "sync_type": sync_type}
        )

    def _sync_boe_metadata(self):
        self.ensure_one()
        sync = self._sync_log("metadata")
        try:
            root, payload_hash, _url = self._client().get_metadatos(self.boe_identifier or self.code)
            meta = root.find("./data/metadatos")
            ambito = meta.find("ambito") if meta is not None else None
            departamento = meta.find("departamento") if meta is not None else None
            rango = meta.find("rango") if meta is not None else None
            estado = meta.find("estado_consolidacion") if meta is not None else None
            values = {
                "boe_identifier": meta.findtext("identificador"),
                "boe_update_at": self._parse_boe_datetime(meta.findtext("fecha_actualizacion")),
                "boe_scope_code": ambito.get("codigo") if ambito is not None else False,
                "boe_scope_name": ambito.text if ambito is not None else False,
                "boe_department_code": departamento.get("codigo") if departamento is not None else False,
                "boe_department_name": departamento.text if departamento is not None else False,
                "boe_rank_code": rango.get("codigo") if rango is not None else False,
                "boe_rank_name": rango.text if rango is not None else False,
                "boe_disposition_date": _parse_boe_date(meta.findtext("fecha_disposicion")),
                "boe_official_number": meta.findtext("numero_oficial"),
                "boe_title": meta.findtext("titulo"),
                "name": meta.findtext("titulo") or self.name,
                "boe_journal": meta.findtext("diario"),
                "publication_date": _parse_boe_date(meta.findtext("fecha_publicacion")),
                "boe_journal_number": meta.findtext("diario_numero"),
                "boe_effective_date": _parse_boe_date(meta.findtext("fecha_vigencia")),
                "valid_from": _parse_boe_date(meta.findtext("fecha_vigencia")) or self.valid_from,
                "boe_derogation_status": meta.findtext("estatus_derogacion") or "unknown",
                "boe_annulment_status": meta.findtext("estatus_anulacion") or "unknown",
                "boe_expired_validity": meta.findtext("vigencia_agotada") or "unknown",
                "boe_consolidation_state_code": estado.get("codigo") if estado is not None else False,
                "boe_consolidation_state": estado.text if estado is not None else False,
                "boe_eli_url": meta.findtext("url_eli"),
                "boe_html_consolidated_url": meta.findtext("url_html_consolidada"),
                "official_url": meta.findtext("url_html_consolidada") or self.official_url,
                "boe_metadata_hash": payload_hash,
                "boe_last_sync_at": fields.Datetime.now(),
                "boe_sync_state": "ok",
                "verified_at": fields.Datetime.now(),
            }
            self.write(values)
            sync.write({"state": "done", "finished_at": fields.Datetime.now(), "content_hash": payload_hash, "records_updated": 1})
        except Exception as error:
            self.write({"boe_sync_state": "error", "boe_last_error": str(error)})
            sync.write({"state": "error", "finished_at": fields.Datetime.now(), "error_message": str(error)})
            raise

    def _sync_boe_analysis(self):
        self.ensure_one()
        sync = self._sync_log("analysis")
        try:
            root, payload_hash, _url = self._client().get_analisis(self.boe_identifier or self.code)
            self.matter_ids.unlink()
            self.relation_ids.unlink()
            created = 0
            for matter in root.findall("./data/analisis/materias/materia"):
                self.env["autonomo.legal.matter"].create(
                    {"source_id": self.id, "code": matter.get("codigo"), "name": matter.text or ""}
                )
                created += 1
            for relation_kind, path in [("previous", "./data/analisis/referencias/anteriores/anterior"), ("later", "./data/analisis/referencias/posteriores/posterior")]:
                for rel in root.findall(path):
                    relation = rel.find("relacion")
                    self.env["autonomo.legal.relation"].create(
                        {
                            "source_id": self.id,
                            "relation_kind": relation_kind,
                            "related_identifier": rel.findtext("id_norma"),
                            "relation_code": relation.get("codigo") if relation is not None else False,
                            "relation_label": relation.text if relation is not None else False,
                            "description": rel.findtext("texto"),
                        }
                    )
                    created += 1
            self.write({"boe_analysis_hash": payload_hash, "boe_last_sync_at": fields.Datetime.now(), "boe_sync_state": "ok"})
            sync.write({"state": "done", "finished_at": fields.Datetime.now(), "content_hash": payload_hash, "records_created": created})
        except Exception as error:
            self.write({"boe_sync_state": "error", "boe_last_error": str(error)})
            sync.write({"state": "error", "finished_at": fields.Datetime.now(), "error_message": str(error)})
            raise

    def _sync_boe_metadata_eli(self):
        self.ensure_one()
        sync = self._sync_log("metadata_eli")
        try:
            root, payload_hash, _url = self._client().get_metadata_eli(self.boe_identifier or self.code)
            import xml.etree.ElementTree as ET

            data = root.find("./data")
            self.write(
                {
                    "boe_eli_metadata_hash": payload_hash,
                    "boe_eli_metadata_xml": ET.tostring(data, encoding="unicode") if data is not None else "",
                    "boe_last_sync_at": fields.Datetime.now(),
                    "boe_sync_state": "ok",
                }
            )
            sync.write({"state": "done", "finished_at": fields.Datetime.now(), "content_hash": payload_hash, "records_updated": 1})
        except Exception as error:
            self.write({"boe_sync_state": "error", "boe_last_error": str(error)})
            sync.write({"state": "error", "finished_at": fields.Datetime.now(), "error_message": str(error)})
            raise

    def _sync_boe_index(self):
        self.ensure_one()
        sync = self._sync_log("index")
        try:
            root, payload_hash, _url = self._client().get_indice(self.boe_identifier or self.code)
            existing = {block.block_identifier: block for block in self.block_ids}
            created = updated = 0
            for item in root.findall("./data/bloque"):
                values = {
                    "source_id": self.id,
                    "block_identifier": item.findtext("id"),
                    "title": item.findtext("titulo") or "",
                    "last_update_date": _parse_boe_date(item.findtext("fecha_actualizacion")),
                    "official_url": item.findtext("url"),
                    "active": True,
                }
                block = existing.get(values["block_identifier"])
                if block:
                    block.write(values)
                    updated += 1
                else:
                    self.env["autonomo.legal.block"].create(values)
                    created += 1
            self.write({"boe_index_hash": payload_hash, "boe_last_sync_at": fields.Datetime.now(), "boe_sync_state": "ok"})
            sync.write({"state": "done", "finished_at": fields.Datetime.now(), "content_hash": payload_hash, "records_created": created, "records_updated": updated})
        except Exception as error:
            self.write({"boe_sync_state": "error", "boe_last_error": str(error)})
            sync.write({"state": "error", "finished_at": fields.Datetime.now(), "error_message": str(error)})
            raise

    def _parse_boe_datetime(self, value):
        if not value or len(value) < 15:
            return False
        return f"{value[0:4]}-{value[4:6]}-{value[6:8]} {value[9:11]}:{value[11:13]}:{value[13:15]}"


class AutonomoLegalMatter(models.Model):
    _name = "autonomo.legal.matter"
    _description = "Materia BOE"
    _order = "code"

    source_id = fields.Many2one("autonomo.legal.source", required=True, ondelete="cascade")
    code = fields.Char(index=True)
    name = fields.Char(required=True)


class AutonomoLegalRelation(models.Model):
    _name = "autonomo.legal.relation"
    _description = "Relacion normativa BOE"
    _order = "relation_kind, related_identifier"

    source_id = fields.Many2one("autonomo.legal.source", required=True, ondelete="cascade")
    relation_kind = fields.Selection([("previous", "Anterior"), ("later", "Posterior")], required=True)
    related_identifier = fields.Char(index=True)
    relation_code = fields.Char()
    relation_label = fields.Char()
    description = fields.Text()
    requires_human_review = fields.Boolean(compute="_compute_requires_human_review", store=True)

    @api.depends("relation_label")
    def _compute_requires_human_review(self):
        critical = {"SE DEROGA", "DEROGA", "SE ANULA", "ANULA"}
        for relation in self:
            relation.requires_human_review = relation.relation_label in critical


class AutonomoLegalBlock(models.Model):
    _name = "autonomo.legal.block"
    _description = "Bloque consolidado BOE"
    _order = "source_id, block_identifier"

    source_id = fields.Many2one("autonomo.legal.source", required=True, ondelete="cascade")
    block_identifier = fields.Char(required=True, index=True)
    block_type = fields.Char()
    title = fields.Char()
    last_update_date = fields.Date()
    expiration_date = fields.Date()
    official_url = fields.Char()
    content_hash = fields.Char()
    version_ids = fields.One2many("autonomo.legal.block.version", "block_id")
    active = fields.Boolean(default=True)

    _block_source_uniq = models.Constraint(
        "UNIQUE(source_id, block_identifier)",
        "El identificador de bloque debe ser unico por fuente.",
    )

    def action_sync_versions(self):
        for block in self:
            block._sync_versions()
        return True

    def _sync_versions(self):
        self.ensure_one()
        sync = self.env["autonomo.legal.sync.status"].create(
            {
                "name": f"{self.source_id.code} bloque {self.block_identifier}",
                "source_id": self.source_id.id,
                "boe_identifier": self.source_id.boe_identifier or self.source_id.code,
                "sync_type": "block",
            }
        )
        try:
            root, payload_hash, url = self.source_id._client().get_bloque(self.source_id.boe_identifier or self.source_id.code, self.block_identifier)
            bloque = root.find("./data/bloque")
            self.write(
                {
                    "block_type": bloque.get("tipo"),
                    "title": bloque.get("titulo") or self.title,
                    "expiration_date": _parse_boe_date(bloque.get("fecha_caducidad")),
                    "official_url": url,
                    "content_hash": payload_hash,
                }
            )
            created = 0
            updated = 0
            existing = {
                (version.modifier_identifier, version.publication_date, version.effective_date, version.content_hash): version
                for version in self.version_ids
            }
            for version in bloque.findall("version"):
                html = "".join([self.env["autonomo.legal.block.version"]._element_to_string(child) for child in list(version)])
                content_hash = hashlib.sha256(html.encode()).hexdigest()
                key = (
                    version.get("id_norma"),
                    _parse_boe_date(version.get("fecha_publicacion")),
                    _parse_boe_date(version.get("fecha_vigencia")),
                    content_hash,
                )
                values = {
                    "block_id": self.id,
                    "source_id": self.source_id.id,
                    "modifier_identifier": key[0],
                    "publication_date": key[1],
                    "effective_date": key[2],
                    "content_html": html,
                    "content_hash": key[3],
                }
                if key in existing:
                    existing[key].write(values)
                    updated += 1
                else:
                    existing[key] = self.env["autonomo.legal.block.version"].create(values)
                    created += 1
            sync.write({"state": "done", "finished_at": fields.Datetime.now(), "content_hash": payload_hash, "records_created": created, "records_updated": updated})
        except Exception as error:
            sync.write({"state": "error", "finished_at": fields.Datetime.now(), "error_message": str(error)})
            raise


class AutonomoLegalBlockVersion(models.Model):
    _name = "autonomo.legal.block.version"
    _description = "Version de bloque BOE"
    _order = "block_id, effective_date desc, publication_date desc"

    block_id = fields.Many2one("autonomo.legal.block", required=True, ondelete="cascade")
    source_id = fields.Many2one("autonomo.legal.source", required=True, ondelete="cascade")
    modifier_identifier = fields.Char(required=True, index=True)
    publication_date = fields.Date(required=True)
    effective_date = fields.Date()
    content_html = fields.Html(sanitize=False)
    content_hash = fields.Char(required=True, index=True)
    embedding_hash = fields.Char()
    active = fields.Boolean(default=True)

    def _element_to_string(self, element):
        import xml.etree.ElementTree as ET

        return ET.tostring(element, encoding="unicode", method="html")
