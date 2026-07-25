# PROMPT MAESTRO PARA CODEX
## Odoo 19 Community para autónomo en España + presupuestos + fiscalidad + BOE + IA

**Versión del documento:** 1.0  
**Objetivo:** crear una solución modular sobre Odoo 19 Community para gestionar la actividad de una persona autónoma en España.

---

# 1. ROL DE CODEX

Actúa como:

- Arquitecto senior de Odoo 19 Community.
- Analista funcional contable y fiscal.
- Desarrollador Python, XML, QWeb y JavaScript de Odoo.
- Ingeniero de integración con APIs.
- Especialista en seguridad, pruebas y despliegue Docker.
- Asistente técnico que trabaja únicamente con requisitos jurídicos respaldados por fuentes oficiales.

No sustituyas el criterio de un asesor fiscal ni afirmes que una declaración es correcta de forma definitiva.

Cuando exista una duda jurídica, fiscal o de Seguridad Social:

1. Consulta primero una fuente oficial.
2. Identifica organismo, documento, norma, artículo o apartado.
3. Guarda la fecha de consulta.
4. Distingue norma, instrucción administrativa y recomendación.
5. Si falta información, no inventes: marca el caso para revisión humana.

---

# 2. ENTORNO TÉCNICO

```text
Odoo 19 Community
PostgreSQL 15
Docker Compose
Python 3
XML
QWeb
JavaScript solo cuando sea necesario
Git
```

Módulos estándar que deben reutilizarse:

```text
base
contacts
mail
account
l10n_es
sale_management
purchase
product
uom
web
```

Modelos estándar que no deben duplicarse:

| Función | Modelo estándar |
|---|---|
| Empresa/autónomo | `res.company` |
| Titular y contactos | `res.partner` |
| Usuarios | `res.users` |
| Productos y servicios | `product.template`, `product.product` |
| Presupuestos | `sale.order` |
| Líneas de presupuesto | `sale.order.line` |
| Facturas y facturas recibidas | `account.move` |
| Líneas fiscales | `account.move.line` |
| Pagos | `account.payment` |
| Impuestos | `account.tax` |
| Diarios | `account.journal` |
| Cuentas | `account.account` |
| Adjuntos | `ir.attachment` |

Prohibido crear modelos alternativos como:

```text
mi.cliente
mi.proveedor
mi.factura
mi.presupuesto
mi.pago
mi.impuesto
```

---

# 3. MÓDULOS PERSONALIZADOS

Crear exactamente estos módulos:

```text
1. autonomo_core
2. autonomo_quotes
3. autonomo_tax
4. autonomo_legal_connector
5. autonomo_ai_review
```

Orden obligatorio:

```text
autonomo_core
→ autonomo_quotes
→ autonomo_tax
→ autonomo_legal_connector
→ autonomo_ai_review
```

Cada módulo debe incluir, cuando corresponda:

```text
__init__.py
__manifest__.py
models/
views/
security/
data/
demo/
report/
tests/
static/description/
README.md
wizard/
services/
controllers/
```

---

# 4. PROTOCOLO JURÍDICO OBLIGATORIO

Antes de implementar campos, reglas, cálculos, declaraciones o informes relacionados con obligaciones legales, consulta únicamente fuentes oficiales.

## 4.1 Fuentes prioritarias

```text
BOE
Agencia Tributaria
Tesorería General de la Seguridad Social / Importass
Seguridad Social
SEPE
Ministerios y administraciones públicas competentes
```

No utilizar blogs, foros o páginas comerciales como fuente jurídica principal.

## 4.2 API del BOE

Implementar compatibilidad con la API oficial de legislación consolidada para obtener:

```text
listado de normas
metadatos
análisis
índice
bloques o artículos
versiones de cada bloque
normas modificadoras
relaciones anteriores y posteriores
estado de vigencia
fecha de actualización
```

Endpoints funcionales que debe contemplar el servicio externo:

```text
/datosabiertos/api/legislacion-consolidada
/datosabiertos/api/legislacion-consolidada/id/{boe_id}/metadatos
/datosabiertos/api/legislacion-consolidada/id/{boe_id}/analisis
/datosabiertos/api/legislacion-consolidada/id/{boe_id}/texto/indice
/datosabiertos/api/legislacion-consolidada/id/{boe_id}/texto/bloque/{block_id}
```

Reglas:

- Nunca borrar versiones anteriores.
- Guardar hashes SHA-256.
- Regenerar embeddings únicamente cuando cambie el contenido.
- Guardar fecha de publicación, entrada en vigor, actualización y fin de vigencia.
- Conservar enlace o referencia a la publicación oficial.
- Marcar el texto consolidado como material informativo y no como sustituto del diario oficial.
- Si existen contradicciones, detener la respuesta y requerir revisión humana.

## 4.3 Normas iniciales que deben indexarse

```text
BOE-A-2007-13409 — Estatuto del trabajo autónomo
BOE-A-2006-20764 — Ley del IRPF
BOE-A-2007-6820 — Reglamento del IRPF
BOE-A-1992-28740 — Ley del IVA
BOE-A-1992-28925 — Reglamento del IVA
BOE-A-2012-14696 — Reglamento de facturación
BOE-A-2019-10487 — Libros registro del IRPF
BOE-A-2003-23186 — Ley General Tributaria
BOE-A-2022-12482 — Cotización de autónomos por rendimientos
BOE-A-2023-24840 — Sistemas informáticos de facturación
BOE-A-2024-22138 — Especificaciones técnicas de sistemas de facturación
```

Añadir automáticamente normas posteriores que modifiquen, desarrollen o deroguen las anteriores.

## 4.4 Fuentes administrativas

El sistema debe consultar y versionar también:

```text
Guía del modelo 036
Instrucciones del modelo 303
Instrucciones del modelo 130
Instrucciones de modelos 111, 115, 180, 190 y 390
Formatos electrónicos de libros registro de IVA e IRPF
Calendario anual del contribuyente
Guía de alta y modificación de trabajo autónomo de Importass
Información oficial de cotización por rendimientos
Documentación de ayudas y pago único del SEPE
```

Las instrucciones y diseños pueden cambiar por ejercicio. No codificar casillas o plazos de forma permanente sin:

```text
fiscal_year
valid_from
valid_to
source_document
source_version
verified_at
```

---

# 5. MODELO DE DOCUMENTACIÓN Y TRÁMITES

Añadir dentro de `autonomo_tax` y `autonomo_core` las entidades necesarias para controlar los papeles, justificantes y datos que pueden requerir Hacienda, Seguridad Social u otro organismo.

## 5.1 Modelo `autonomo.procedure`

Representa un trámite oficial.

Campos:

```text
name
code
company_id
authority
procedure_type
model_code
description
trigger_event
periodicity
valid_from
valid_to
official_source_url
legal_reference
requires_human_submission
supports_file_generation
active
notes
```

`authority`:

```text
aeat
tgss
sepe
regional
local
other
```

`procedure_type`:

```text
registration
modification
deregistration
tax_return
informative_return
social_security
benefit
document_submission
other
```

Ejemplos:

```text
Alta censal modelo 036
Modificación modelo 036
Baja censal modelo 036
Alta RETA
Modificación RETA
Baja RETA
Modelo 303
Modelo 130
Modelo 111
Modelo 115
```

## 5.2 Modelo `autonomo.procedure.requirement`

Campos:

```text
procedure_id
sequence
requirement_type
name
description
field_model
field_name
document_type
required_condition
mandatory
valid_from
valid_to
official_source_url
legal_reference
active
```

`requirement_type`:

```text
field
document
declaration
authorization
signature
payment
attachment
other
```

Permitir requisitos condicionales.

Ejemplos:

```text
IAE obligatorio para alta RETA
CNAE obligatorio para alta RETA
Fecha de inicio
Domicilio de actividad
Estimación de rendimientos netos
Base de cotización
Mutua colaboradora
IBAN de domiciliación
Autorización del titular de la cuenta si no coincide
Certificado o Cl@ve para presentación
Documento justificativo de bonificación
```

## 5.3 Modelo `autonomo.submission`

Representa una presentación, borrador o justificante.

Campos:

```text
name
company_id
procedure_id
tax_period_id
state
draft_date
review_date
ready_date
submitted_at
submission_channel
filing_reference
secure_verification_code
result
amount
payment_method
direct_debit_iban_masked
generated_file_id
filing_receipt_id
human_approved_by
human_approved_at
source_snapshot_hash
notes
```

Estados:

```text
draft
incomplete
review
ready
submitted
accepted
rejected
corrected
cancelled
```

## 5.4 Modelo `autonomo.submission.document`

Campos:

```text
submission_id
requirement_id
attachment_id
document_type
document_number
issue_date
valid_until
issuer
sha256
contains_personal_data
verified
verified_by
verified_at
verification_notes
```

## 5.5 Checklist

Crear una vista checklist que muestre:

```text
requisito
obligatorio
condición
dato presente
documento adjunto
verificado
fuente oficial
estado
```

No marcar automáticamente un trámite como listo si existe un requisito obligatorio sin verificar.

---

# 6. DATOS CENSALES Y MODELO 036

Extender `res.company` o crear un perfil censal dependiente de la compañía.

## 6.1 Modelo `autonomo.census.profile`

Campos:

```text
company_id
tax_identification_number
census_status
census_start_date
census_end_date
tax_residence_country_id
fiscal_address_partner_id
notification_address_partner_id
main_activity_id
activity_start_date
usual_operations_start_date
iae_codes_json
cnae_codes_json
vat_taxpayer
vat_regime
irpf_estimation_method
withholding_work_obligation
withholding_professional_obligation
withholding_rent_obligation
intracommunity_operator
cash_criterion
special_vat_sector
business_premises
premises_reference
representative_partner_id
electronic_notifications_enabled
last_036_submission_id
verified_at
notes
```

No representar las casillas del formulario como nombres técnicos permanentes cuando puedan cambiar. Guardar:

```text
form_year
form_version
field_external_code
```

en configuraciones versionadas.

## 6.2 Datos y documentos que deben poder controlarse

```text
identidad y NIF
domicilio fiscal
domicilio de notificaciones
datos de contacto
representante, si existe
causa de presentación: alta, modificación o baja
fecha efectiva
actividad económica
epígrafe IAE
lugares de actividad
régimen de IVA
método de IRPF
obligaciones de retener
operaciones intracomunitarias
cuenta bancaria cuando proceda
firma o identificación electrónica
documentación adicional requerida según el caso
```

## 6.3 PDF

Crear:

```text
Ficha censal del autónomo
Checklist modelo 036
Resumen de alta, modificación o baja
```

Estos PDF son informativos y no deben presentarse como formulario oficial salvo que se implemente exactamente el diseño de registro oficial vigente.

---

# 7. DATOS DE ALTA EN RETA

Crear modelo:

```text
autonomo.social.security.profile
```

Campos:

```text
company_id
social_security_number_encrypted
reta_status
reta_start_date
reta_end_date
iae_code
cnae_code
activity_start_date
activity_address_partner_id
estimated_annual_net_returns
selected_contribution_base
contribution_bracket_code
mutual_insurance_name
mutual_insurance_code
coverage_options_json
benefit_or_reduction_code
bank_account_id
bank_account_holder_partner_id
bank_holder_authorization_attachment_id
linked_company
community_property_member
family_collaborator
trade_dependent_worker
last_reta_submission_id
verified_at
notes
```

Reglas:

- Cifrar o proteger el NSS.
- No enviar NSS, IBAN ni documentos personales a una API gratuita de IA.
- Guardar importes y tramos con ejercicio de vigencia.
- Permitir varias actividades, pero mantener la situación RETA asociada a la persona.
- Controlar documentos que acrediten bonificaciones o situaciones especiales.
- Generar checklist antes del alta.

PDF:

```text
Ficha RETA
Checklist alta RETA
Resumen de cotización estimada
```

No presentar automáticamente el alta.

---

# 8. MÓDULO `autonomo_core`

## 8.1 Objetivo

Crear la base común del sistema:

```text
perfil del autónomo
actividades económicas
categorías fiscales
perfil censal
perfil de Seguridad Social
campos adicionales de empresa, contacto, presupuesto y factura
gestión documental básica
```

## 8.2 Dependencias

```python
"depends": [
    "base",
    "contacts",
    "mail",
    "account",
    "l10n_es",
    "sale_management",
    "purchase"
]
```

## 8.3 Modelo `autonomo.activity`

Campos:

```text
name
code
company_id
activity_kind
iae_code
cnae_code
start_date
end_date
irpf_estimation_method
vat_regime
default_income_account_id
default_expense_account_id
default_sale_tax_ids
default_purchase_tax_ids
default_withholding_tax_id
vat_deductible_default_percent
activity_address_partner_id
tax_office_code
social_security_activity_code
notes
active
```

Selecciones:

```text
activity_kind:
- business
- professional

irpf_estimation_method:
- direct_simplified
- direct_normal
- objective

vat_regime:
- general
- cash_criterion
- simplified
- exempt
- other
```

Restricciones:

```text
unique(company_id, code)
start_date <= end_date
0 <= vat_deductible_default_percent <= 100
```

## 8.4 Modelo `autonomo.tax.category`

Campos:

```text
code
name
company_id
category_kind
official_label
model_reference
valid_from
valid_to
default_irpf_deductible_percent
default_vat_deductible_percent
legal_reference
official_source_url
active
notes
```

## 8.5 Extender `res.company`

```text
is_self_employed
owner_partner_id
fiscal_start_date
default_activity_id
irpf_estimation_method
default_vat_regime
tax_authority
reta_start_date
external_backup_enabled
last_verified_backup_at
census_profile_id
social_security_profile_id
```

## 8.6 Extender `res.partner`

```text
tax_subject_kind
e_invoice_required
e_invoice_channel
e_invoice_endpoint
privacy_alias
tax_data_verified_at
```

## 8.7 Extender `sale.order`

```text
activity_id
work_site_partner_id
scope_description
estimated_cost
estimated_margin
estimated_margin_percent
requires_advance
advance_percent
tax_review_state
```

## 8.8 Extender `account.move`

```text
activity_id
operation_date
tax_document_kind
income_expense_book_state
tax_period_id
tax_review_state
source_attachment_id
document_sha256
electronic_invoice_uuid
electronic_invoice_status
effective_payment_date
book_locked
```

## 8.9 Extender `account.move.line`

```text
activity_id
tax_category_id
irpf_deductible_percent
vat_deductible_percent
irpf_deductible_amount
vat_deductible_amount
withholding_rate_snapshot
withholding_amount_snapshot
is_investment_asset
deductibility_review_required
deductibility_notes
```

## 8.10 PDF obligatorios

```text
Ficha de actividad económica
Resumen de categorías fiscales
Ficha censal
Checklist de alta/modificación/baja censal
Ficha RETA
Checklist de alta RETA
```

## 8.11 Diez ejemplos demo

Actividades:

1. Montaje de muebles.
2. Montaje de cocinas.
3. Carpintería de madera.
4. Carpintería metálica.
5. Instalaciones eléctricas.
6. Albañilería.
7. Reforma integral.
8. Mobiliario clínico.
9. Mesas de resina.
10. Reparación de mobiliario.

Categorías:

1. Ingresos por montaje.
2. Ingresos por carpintería.
3. Materiales.
4. Herramientas.
5. Combustible.
6. Seguro RC.
7. Gestoría.
8. Telefonía.
9. Formación.
10. Publicidad.

Crear también 10 trámites demo:

1. Alta modelo 036.
2. Modificación modelo 036.
3. Baja modelo 036.
4. Alta RETA.
5. Modificación RETA.
6. Baja RETA.
7. Aportación documental TGSS.
8. Solicitud de bonificación.
9. Cambio de base.
10. Comunicación de nueva actividad.

---

# 9. MÓDULO `autonomo_quotes`

## 9.1 Objetivo

Ampliar presupuestos estándar para:

```text
mano de obra
materiales
kilometraje
combustible
peajes
aparcamiento
dietas
alojamiento
herramientas
alquileres
ayudantes
subcontratas
residuos
recargos
mediciones
versiones
anticipos
costes
márgenes
```

## 9.2 Modelos

```text
autonomo.travel.rate
autonomo.cost.item
autonomo.quote.surcharge
autonomo.quote.template
autonomo.quote.template.line
autonomo.quote.version
autonomo.work.measurement
autonomo.quote.calculation.wizard
```

## 9.3 `autonomo.travel.rate`

```text
name
company_id
origin_city
origin_address
free_radius_km
price_per_km
minimum_charge
round_trip
include_fuel
include_vehicle_costs
include_tolls
include_parking
valid_from
valid_to
active
notes
```

## 9.4 `autonomo.cost.item`

```text
name
company_id
cost_type
product_id
internal_cost
sale_price
uom_id
reusable
charge_method
default_margin_percent
tax_ids
active
notes
```

Tipos:

```text
material
labor
travel
fuel
tool
rental
parking
toll
diet
overnight
subcontract
waste
other
```

## 9.5 Extender `sale.order`

```text
quote_template_id
quote_type
work_address
travel_rate_id
distance_one_way_km
distance_total_km
free_distance_km
billable_distance_km
travel_amount
fuel_amount
parking_amount
toll_amount
diet_amount
overnight_amount
other_travel_amount
estimated_material_cost
estimated_labor_cost
estimated_tool_cost
estimated_subcontract_cost
estimated_total_cost
estimated_profit
estimated_margin_percent
requires_advance
advance_percent
advance_amount
quote_version
measurement_ids
surcharge_ids
special_conditions
internal_notes
```

Reglas:

- Calcular ida y vuelta.
- Descontar radio gratuito.
- Aplicar mínimo.
- Evitar duplicar combustible si está incluido.
- Crear líneas estándar.
- Permitir anulación manual con motivo.
- Guardar versión y PDF antes de modificar un presupuesto enviado.

## 9.6 PDF

```text
Presupuesto profesional
Hoja interna de costes
Informe de mediciones
Historial de versiones
```

## 9.7 Diez casos demo

1. Madrid sin km facturables.
2. Madrid fuera del radio gratuito.
3. Comunidad de Madrid.
4. Fuera de Madrid.
5. Combustible incluido.
6. Combustible separado.
7. Peajes.
8. Aparcamiento.
9. Urgencia.
10. Herramienta alquilada.

Crear 10 plantillas:

1. Cocina.
2. Armario.
3. Puerta.
4. Mobiliario clínico.
5. Baño.
6. Electricidad.
7. Reparación.
8. Carpintería.
9. Mesa de resina.
10. Reforma integral.

---

# 10. MÓDULO `autonomo_tax`

## 10.1 Objetivo

Gestionar:

```text
obligaciones
trámites
documentación
calendario
periodos
libros
cierres
snapshots
borradores
justificantes
bienes de inversión
exportación
```

## 10.2 Modelos

```text
autonomo.procedure
autonomo.procedure.requirement
autonomo.submission
autonomo.submission.document
autonomo.tax.obligation
autonomo.tax.deadline
autonomo.tax.period
autonomo.tax.return
autonomo.tax.book.entry
autonomo.tax.book.snapshot
autonomo.tax.book.snapshot.line
autonomo.investment.asset
```

## 10.3 `autonomo.tax.obligation`

```text
company_id
activity_id
authority
tax_kind
model_code
periodicity
start_date
end_date
calculation_service
legal_reference
official_source_url
active
notes
```

## 10.4 `autonomo.tax.deadline`

```text
authority
model_code
fiscal_year
period_code
filing_start_date
filing_end_date
direct_debit_end_date
source_document_url
source_version
verified_at
notes
```

## 10.5 `autonomo.tax.period`

```text
company_id
activity_id
fiscal_year
period_type
period_code
date_start
date_end
state
closed_at
closed_by
reopen_reason
```

## 10.6 `autonomo.tax.return`

```text
company_id
obligation_id
period_id
model_code
form_year
form_version
state
calculation_version
calculation_snapshot
amount_to_pay
amount_to_refund
amount_to_compensate
book_snapshot_ids
generated_file_id
submitted_at
filing_receipt_id
filing_reference
human_approved_by
human_approved_at
notes
```

## 10.7 Datos funcionales por modelo

No implementar casillas sin verificar el diseño oficial del ejercicio.

### Modelo 303

Permitir snapshots de:

```text
bases por tipo de IVA
cuotas devengadas
IVA soportado
IVA deducible
regularizaciones
compensaciones anteriores
resultado
operaciones específicas
```

### Modelo 130

Permitir snapshots de:

```text
ingresos acumulados
gastos fiscalmente deducibles
amortizaciones
rendimiento neto
porcentaje de pago fraccionado
pagos anteriores
retenciones soportadas
resultado
```

Añadir regla configurable para comprobar excepciones relacionadas con ingresos sometidos a retención.

### Modelo 111

Permitir:

```text
número de perceptores
percepciones dinerarias
retenciones
percepciones en especie
ingresos a cuenta
tipo de rendimiento
```

### Modelo 115

Permitir:

```text
arrendador
inmueble
base de alquiler
retención
periodo
número de perceptores
```

### Modelos anuales

```text
180
190
390
347
349
```

Generar borradores únicamente cuando la obligación esté activa y el diseño del ejercicio esté verificado.

## 10.8 Libros

Crear vista SQL de solo lectura con:

```text
facturas expedidas
facturas recibidas
ventas e ingresos
compras y gastos
bienes de inversión
provisiones y suplidos
operaciones intracomunitarias
```

Campos:

```text
company_id
activity_id
book_type
source_move_id
source_line_id
entry_sequence
invoice_number
invoice_series
issue_date
operation_date
partner_name
partner_vat
concept_code
concept_description
tax_base
vat_rate
vat_amount
vat_deductible_amount
irpf_deductible_amount
withholding_rate
withholding_amount
total_amount
currency_id
exchange_rate
is_rectifying
rectified_move_id
document_sha256
fiscal_year
fiscal_quarter
```

## 10.9 Conservación e integridad

- No eliminar facturas contabilizadas.
- Usar rectificativas.
- Guardar hash de documentos.
- Bloquear libros cerrados.
- Mantener snapshots inmutables.
- Vincular cada snapshot a la versión de cálculo.
- Mantener justificantes y documentos durante el periodo legal configurable.
- No establecer permanentemente un plazo fijo en código: obtenerlo de fuente oficial versionada.

## 10.10 PDF y exportación

```text
Checklist de trámite
Resumen de presentación
Libro de ventas
Libro de gastos
Facturas expedidas
Facturas recibidas
Bienes de inversión
Resumen trimestral
Borrador fiscal
Declaración presentada
```

Permitir:

```text
PDF
CSV
JSON
XLSX cuando sea viable
```

## 10.11 Diez obligaciones demo

1. 303.
2. 130.
3. 111.
4. 115.
5. 390.
6. 180.
7. 190.
8. 347.
9. 349.
10. Cuota RETA informativa.

Crear 10 presentaciones demo con estados diferentes.

---

# 11. MÓDULO `autonomo_legal_connector`

## 11.1 Objetivo

Conectar Odoo con un servicio externo que sincroniza BOE y documentación administrativa.

## 11.2 Modelos

```text
autonomo.legal.config
autonomo.legal.source
autonomo.legal.query
autonomo.legal.citation
autonomo.legal.sync.status
```

## 11.3 Configuración

```text
name
company_id
service_url
auth_type
api_token
timeout_seconds
verify_ssl
anonymization_mode
active
last_connection_at
last_connection_state
last_error
```

## 11.4 Servicios

```text
services/legal_client.py
services/anonymizer.py
services/response_validator.py
services/source_version_validator.py
```

Funciones:

```text
test_connection
search_legal_context
review_invoice
review_quote
review_tax_period
review_procedure
get_document
get_section
verify_source_version
```

## 11.5 Reglas

- Enviar datos mínimos.
- Anonimizar NIF, NSS, IBAN, nombres y direcciones.
- Manejar 401, 403, 404, 429 y 500.
- Usar reintentos limitados.
- Registrar tiempos y errores.
- Permitir modo simulación.
- Rechazar respuestas sin fuentes.
- Rechazar respuestas con fuentes caducadas.
- Marcar como crítica cualquier contradicción normativa.

## 11.6 PDF

```text
Informe de consulta jurídica
Informe de verificación de requisitos
Informe de cambio normativo
```

## 11.7 Diez consultas demo

1. Alta censal.
2. Alta RETA.
3. IVA de montaje.
4. Combustible deducible.
5. Factura simplificada.
6. Rectificativa.
7. Modelo 303.
8. Modelo 130.
9. Factura electrónica.
10. Conservación documental.

---

# 12. MÓDULO `autonomo_ai_review`

## 12.1 Objetivo

Registrar revisiones, citas e incidencias.

## 12.2 Modelos

```text
autonomo.ai.review
autonomo.ai.citation
autonomo.compliance.issue
```

## 12.3 `autonomo.ai.review`

```text
review_type
company_id
source_model
source_record_id
request_payload_hash
anonymized_payload
question
answer
structured_result
risk_level
requires_human_review
provider
model_name
prompt_version
state
created_at
accepted_by
accepted_at
rejected_by
rejected_at
rejection_reason
```

Tipos:

```text
invoice
expense
quote
quarter
tax_return
procedure
general_question
```

## 12.4 Incidencias

```text
missing_data
missing_document
tax_mismatch
duplicate
deadline
deductibility
legal_change
document_integrity
source_not_verified
other
```

## 12.5 Botones

Añadir:

```text
Revisar con IA
Ver fuentes
Ver requisitos
Crear incidencia
Aceptar
Rechazar
Solicitar revisión humana
```

## 12.6 PDF

```text
Informe de revisión IA
Informe de incidencias
Revisión de presupuesto
Revisión de factura
Revisión trimestral
Revisión de trámite
```

## 12.7 Diez ejemplos demo

1. Presupuesto con kilómetros.
2. Factura de montaje.
3. Combustible.
4. Herramienta.
5. Duplicado.
6. IVA dudoso.
7. Falta fecha de operación.
8. Falta justificante.
9. Presentación incompleta.
10. Cambio normativo.

---

# 13. PDF: REQUISITO GENERAL

Cada módulo debe exportar a PDF sus registros principales.

Todos los PDF deben incluir:

```text
empresa
NIF
dirección
referencia
fecha
usuario
estado
moneda
totales
fuentes oficiales cuando proceda
fecha de consulta legal
hash cuando proceda
pie de página
aviso de revisión humana
```

No llamar “formulario oficial” a un PDF interno.

Usar:

```text
ir.actions.report
QWeb
paperformat apropiado
```

Añadir pruebas que confirmen que cada informe se renderiza.

---

# 14. DIEZ EJEMPLOS POR MÓDULO

Cada módulo debe incluir **como mínimo 10 ejemplos completos**.

Los datos demo deben:

- Estar enlazados entre sí.
- Utilizar clientes, productos, impuestos y actividades.
- Cubrir casos normales y casos límite.
- Incluir ejemplos correctos e incorrectos.
- Permitir probar PDF.
- Permitir probar permisos.
- No contener datos personales reales.

---

# 15. SEGURIDAD

Crear grupos:

```text
group_autonomo_user
group_autonomo_manager
group_autonomo_accounting
group_autonomo_ai_reviewer
group_autonomo_admin
```

Reglas:

- Usuario operativo no puede modificar configuración fiscal.
- Solo contabilidad puede cerrar periodos.
- Solo administrador puede cambiar fuentes y tokens.
- Solo revisor puede aceptar conclusiones de IA.
- Ningún usuario puede eliminar snapshots bloqueados.
- Ocultar campos sensibles.
- No exponer PostgreSQL a Internet.
- No guardar secretos en Git.

---

# 16. DASHBOARD COMMUNITY

Crear un panel sin Enterprise:

```text
presupuestos pendientes
presupuestos aceptados
facturas pendientes
facturas de proveedor
ingresos trimestrales
gastos trimestrales
IVA repercutido
IVA soportado
obligaciones próximas
trámites incompletos
documentos pendientes
incidencias
revisiones IA
última copia
```

---

# 17. BACKUPS

Crear scripts:

```text
scripts/backup.ps1
scripts/backup.sh
scripts/restore.ps1
scripts/restore.sh
```

Deben:

```text
hacer pg_dump
copiar filestore
copiar configuración
guardar commit Git
guardar versión Docker
generar SHA-256
detectar disco externo por etiqueta
registrar resultado
mantener retención configurable
probar restauración
```

El volumen Docker no es una copia de seguridad.

---

# 18. GIT

Ramas:

```text
main
develop
feature/autonomo-core
feature/autonomo-quotes
feature/autonomo-tax
feature/autonomo-legal
feature/autonomo-ai
```

No trabajar directamente en `main`.

Versiones:

```text
19.0.1.0.0
19.0.1.1.0
19.0.2.0.0
```

---

# 19. PRUEBAS OBLIGATORIAS

Crear pruebas para:

```text
creación
restricciones
porcentajes
cálculos
kilometraje
márgenes
multiempresa
permisos
bloqueos
snapshots
checklists
documentos requeridos
versiones jurídicas
anonimización
respuestas sin citas
PDF
integración entre módulos
```

Casos integrales:

1. Alta censal incompleta.
2. Alta RETA completa.
3. Presupuesto sin km facturables.
4. Presupuesto con km.
5. Combustible separado.
6. Factura desde presupuesto.
7. Gasto parcialmente deducible.
8. Cierre trimestral.
9. Presentación con documento faltante.
10. Revisión IA con citas verificadas.

---

# 20. ORDEN DE TRABAJO PARA CODEX

Antes de crear código:

1. Inspeccionar el repositorio.
2. Leer `compose.yaml`.
3. Leer `odoo.conf`.
4. Confirmar versión de Odoo.
5. Confirmar ruta de addons.
6. Confirmar módulos estándar instalados.
7. Consultar fuentes oficiales aplicables.
8. Enumerar requisitos jurídicos.
9. Proponer modelos y relaciones.
10. Mostrar archivos que se crearán.
11. Crear rama.
12. Implementar un módulo cada vez.
13. Instalar el módulo.
14. Ejecutar pruebas.
15. Generar los 10 datos demo.
16. Generar PDF.
17. Corregir errores.
18. Documentar fuentes.
19. Crear commit.
20. Solicitar confirmación para continuar.

No crear los cinco módulos de golpe.

---

# 21. PRIMERA ORDEN PARA CODEX

Empieza únicamente por:

```text
autonomo_core
```

Primero entrega:

```text
análisis del proyecto
fuentes oficiales consultadas
normas y documentos aplicables
árbol de archivos
diagrama de entidades
campos
relaciones
seguridad
vistas
informes PDF
10 ejemplos demo
pruebas
plan de instalación
```

Después genera archivos completos.

No continuar con `autonomo_quotes` hasta que:

```text
autonomo_core se instale
no haya errores de carga
los permisos funcionen
las vistas funcionen
los PDF se generen
los checklists funcionen
los 10 ejemplos demo existan
las pruebas pasen
```

Si Codex no tiene acceso a Internet:

- No inventar normativa.
- Crear interfaces y datos configurables.
- Usar únicamente las fuentes oficiales incluidas en este documento.
- Marcar todo requisito no verificado como `pending_legal_verification`.
