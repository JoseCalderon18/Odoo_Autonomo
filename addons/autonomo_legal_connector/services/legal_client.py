import hashlib
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from .response_validator import require_status_ok


class LegalClientError(Exception):
    pass


class BOELegalClient:
    BASE_URL = "https://www.boe.es/datosabiertos/api/legislacion-consolidada"

    def __init__(self, timeout=20, max_retries=2, retry_delay=1.0):
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _get_xml(self, path):
        url = f"{self.BASE_URL}{path}"
        request = urllib.request.Request(
            url,
            headers={"Accept": "application/xml", "User-Agent": "Autonomo Odoo legal connector"},
        )
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    payload = response.read()
                break
            except urllib.error.HTTPError as error:
                last_error = error
                if error.code not in {429, 500, 502, 503, 504} or attempt >= self.max_retries:
                    raise LegalClientError(f"BOE HTTP {error.code}: {url}") from error
            except urllib.error.URLError as error:
                last_error = error
                if attempt >= self.max_retries:
                    raise LegalClientError(f"BOE connection error: {error.reason}") from error
            time.sleep(self.retry_delay * (attempt + 1))
        else:
            raise LegalClientError(f"BOE request failed: {last_error}") from last_error
        root = ET.fromstring(payload)
        require_status_ok(root)
        return root, hashlib.sha256(payload).hexdigest(), url

    def get_metadatos(self, boe_id):
        return self._get_xml(f"/id/{boe_id}/metadatos")

    def get_analisis(self, boe_id):
        return self._get_xml(f"/id/{boe_id}/analisis")

    def get_metadata_eli(self, boe_id):
        return self._get_xml(f"/id/{boe_id}/metadata-eli")

    def get_indice(self, boe_id):
        return self._get_xml(f"/id/{boe_id}/texto/indice")

    def get_bloque(self, boe_id, block_id):
        return self._get_xml(f"/id/{boe_id}/texto/bloque/{block_id}")
