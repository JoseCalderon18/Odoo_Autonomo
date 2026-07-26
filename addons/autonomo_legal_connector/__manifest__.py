{
    "name": "Autonomo Legal Connector",
    "summary": "Sincronizacion BOE y fuentes oficiales para autonomos",
    "description": "Conector legal para consultar la API oficial de legislacion consolidada del BOE y versionar metadatos, analisis, bloques y versiones.",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "Jose",
    "license": "LGPL-3",
    "depends": ["autonomo_core"],
    "data": [
        "security/ir.model.access.csv",
        "data/autonomo_legal_connector_data.xml",
        "views/autonomo_legal_source_views.xml",
        "views/autonomo_legal_config_views.xml",
        "views/autonomo_legal_query_views.xml",
        "views/autonomo_legal_sync_views.xml",
        "views/autonomo_legal_connector_menus.xml",
    ],
    "demo": [
        "demo/autonomo_legal_connector_demo.xml",
    ],
    "application": False,
    "installable": True,
}
