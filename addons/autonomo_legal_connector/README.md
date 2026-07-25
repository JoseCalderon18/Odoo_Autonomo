Autonomo Legal Connector
========================

Modulo para sincronizar fuentes oficiales con la API de legislacion consolidada del BOE.

Fuentes oficiales revisadas
---------------------------

Consulta realizada el 2026-07-25.

- BOE Datos abiertos: https://www.boe.es/datosabiertos/api/api.php
- API legislacion consolidada PDF: https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf
- Metadatos ejemplo BOE-A-2007-13409: https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2007-13409/metadatos
- Analisis ejemplo BOE-A-2007-13409: https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2007-13409/analisis
- Indice ejemplo BOE-A-2007-13409: https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2007-13409/texto/indice

Endpoints contemplados
----------------------

- /datosabiertos/api/legislacion-consolidada/id/{id}/metadatos
- /datosabiertos/api/legislacion-consolidada/id/{id}/analisis
- /datosabiertos/api/legislacion-consolidada/id/{id}/metadata-eli
- /datosabiertos/api/legislacion-consolidada/id/{id}/texto
- /datosabiertos/api/legislacion-consolidada/id/{id}/texto/indice
- /datosabiertos/api/legislacion-consolidada/id/{id}/texto/bloque/{id_bloque}

Campos BOE cubiertos
--------------------

- identificador
- fecha_actualizacion
- ambito
- departamento
- rango
- fecha_disposicion
- numero_oficial
- titulo
- diario
- fecha_publicacion
- diario_numero
- fecha_vigencia
- estatus_derogacion
- estatus_anulacion
- vigencia_agotada
- estado_consolidacion
- url_eli
- metadata-eli XML y hash
- url_html_consolidada
- materias
- referencias anteriores y posteriores
- bloques del indice
- versiones de bloque
- hashes SHA-256 de metadatos, analisis, indice, bloque y version

Reglas
------

- No se borra el registro principal de fuente legal.
- No se borran versiones anteriores de bloque; se conservan por hash SHA-256.
- Cada version de bloque guarda hash SHA-256.
- Las relaciones que indican derogacion o anulacion quedan marcadas para revision humana.
- El contenido consolidado se trata como informativo y no sustituye el diario oficial.
- El modulo no presenta tramites ni declaraciones.

Modelos
-------

- autonomo.legal.config
- autonomo.legal.source, extendido desde autonomo_core
- autonomo.legal.matter
- autonomo.legal.relation
- autonomo.legal.block
- autonomo.legal.block.version
- autonomo.legal.query
- autonomo.legal.citation
- autonomo.legal.sync.status

Instalacion
-----------

::

    docker compose exec odoo odoo -d Autonomo -i autonomo_legal_connector --stop-after-init
    docker compose restart odoo

Uso
---

Entrar en Autonomo > Legal BOE > Fuentes BOE y usar los botones de sincronizacion.
