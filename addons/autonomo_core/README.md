Autonomo Core
=============

Modulo base para gestionar actividad de una persona autonoma en Espana sobre Odoo 19 Community.

Analisis del proyecto
---------------------

- Entorno confirmado: Odoo Server 19.0-20260630, PostgreSQL 15 y Docker Compose.
- Ruta de addons: /mnt/extra-addons, montada desde ./addons.
- Base revisada: Autonomo.
- Modulos estandar instalados: base, contacts, mail, account, l10n_es, sale_management, purchase, product, uom y web.
- Repositorio Git inicializado con ramas main, develop y feature/autonomo-core.

Fuentes oficiales consultadas
-----------------------------

Consulta realizada el 2026-07-25.

- BOE, Datos abiertos, API de legislacion consolidada: https://www.boe.es/datosabiertos/api/api.php
- BOE, Ley 20/2007, Estatuto del trabajo autonomo: https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409
- BOE, Ley 35/2006 del IRPF: https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764
- BOE, Ley 37/1992 del IVA: https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740
- BOE, Reglamento de facturacion, Real Decreto 1619/2012: https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696
- Agencia Tributaria, Modelo 036: https://sede.agenciatributaria.gob.es/Sede/procedimientoini/G322.shtml
- Agencia Tributaria, guia practica del modelo censal 036: https://sede.agenciatributaria.gob.es/Sede/Ayuda/guia-practica-declaracion-censal.html
- Importass, guia practica de trabajo autonomo: https://portal.seg-social.gob.es/wps/portal/importass/importass/Colectivos/trabajo%2Bautonomo/guia
- Importass, alta en trabajo autonomo: https://portal.seg-social.gob.es/wps/portal/importass/importass/Categorias/Altas%2C%2Bbajas%2By%2Bmodificaciones/Altas%2By%2Bafiliacion%2Bde%2Btrabajadores/Alta_trabajo_autonomo

Normas y documentos aplicables
------------------------------

El modulo registra fuentes oficiales como datos versionables. No codifica casillas oficiales ni plazos fijos. Todo PDF es interno e informativo.

Arbol de archivos
-----------------

::

    autonomo_core/
      __init__.py
      __manifest__.py
      README.md
      data/
      demo/
      models/
      report/
      security/
      tests/
      views/

Entidades principales
---------------------

- res.company se amplia con perfil de autonomo, actividad por defecto y control de backup.
- res.partner se amplia con clasificacion fiscal y datos de factura electronica.
- sale.order se amplia con actividad, lugar de trabajo, alcance, coste y margen.
- account.move se amplia con actividad, fecha de operacion, periodo fiscal, documento origen y bloqueo de libro.
- account.move.line se amplia con categoria fiscal y porcentajes deducibles.
- autonomo.activity registra actividades economicas.
- autonomo.tax.category registra categorias fiscales configurables.
- autonomo.procedure, autonomo.procedure.requirement, autonomo.submission, autonomo.submission.document y autonomo.submission.checklist.line gestionan tramites y checklists.
- autonomo.census.profile gestiona ficha censal interna.
- autonomo.social.security.profile gestiona ficha RETA interna.

Seguridad
---------

Grupos creados:

- group_autonomo_user
- group_autonomo_manager
- group_autonomo_accounting
- group_autonomo_ai_reviewer
- group_autonomo_admin

Campos sensibles de NSS, banco y autorizaciones quedan restringidos al grupo administrador.

Vistas e informes PDF
---------------------

Vistas:

- Actividades economicas
- Categorias fiscales
- Tramites
- Presentaciones y checklists
- Perfil censal
- Perfil RETA
- Extensiones en empresa, contacto, presupuesto y factura

Informes:

- Ficha de actividad economica
- Resumen de categorias fiscales
- Ficha censal interna
- Ficha RETA interna

Datos de ejemplo
----------------

Incluye 10 actividades, 10 categorias fiscales, 10 tramites y 10 presentaciones con estados distintos.

Pruebas
-------

Cubren creacion, restricciones de fechas y porcentajes, checklist obligatorio, bloqueo de listo y renderizado de informes.

Plan de instalacion
-------------------

::

    docker compose exec odoo odoo -d Autonomo -i autonomo_core --stop-after-init
    docker compose restart odoo

No usar este modulo como sustituto de asesoramiento fiscal, juridico ni administrativo.
