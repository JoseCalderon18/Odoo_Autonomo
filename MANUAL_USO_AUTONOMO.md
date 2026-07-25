# Manual de uso - Proyecto Autonomo Odoo 19

Este manual explica que se puede hacer ahora mismo con el proyecto, para que sirve cada parte y que puedes pedirme a Codex para seguir construyendo el sistema.

Estado actual:

- Odoo 19 Community con Docker.
- Base de datos: `Autonomo`.
- Modulo `autonomo_core` instalado.
- Modulo `autonomo_legal_connector` instalado.
- Rama actual: `feature/autonomo-legal-boe`.
- Odoo disponible en: http://localhost:8069

Importante: este sistema ayuda a organizar datos, documentos, fuentes y revisiones. No sustituye a un asesor fiscal, laboral, juridico ni administrativo.

---

## 1. Entorno Docker

### Para que sirve

Sirve para ejecutar Odoo 19 y PostgreSQL de forma local sin instalar Odoo directamente en Windows.

### Que puedes hacer tu

Desde PowerShell, en la carpeta del proyecto:

```powershell
docker compose ps
docker compose up -d
docker compose restart odoo
docker compose logs -f odoo
docker compose down
```

No uses `docker compose down -v` salvo que quieras borrar la base de datos y el filestore.

### Que me puedes pedir

- "Revisa si Odoo esta levantado".
- "Mira los logs de Odoo".
- "Reinicia Odoo".
- "Comprueba si el modulo esta instalado".
- "Ejecuta los tests".

---

## 2. Git y ramas

### Para que sirve

Sirve para guardar avances del proyecto y separar cambios por funcionalidad.

### Ramas creadas

- `main`: base inicial.
- `develop`: base de desarrollo.
- `feature/autonomo-core`: modulo base `autonomo_core`.
- `feature/autonomo-legal-boe`: conector BOE.

### Commits actuales importantes

- `a73b177 chore: initial docker odoo workspace`
- `63e0deb feat: add autonomo core module`
- `5427163 feat: add BOE legal connector`

### Que me puedes pedir

- "Crea una rama nueva para X".
- "Haz commit de lo que acabas de hacer".
- "Dime que cambios hay pendientes".
- "Compara esta rama con develop".
- "Prepara un resumen para merge".

---

## 3. Modulo `autonomo_core`

### Para que sirve

Es la base comun del sistema para gestionar una actividad de autonomo en Espana.

Incluye:

- Actividades economicas.
- Categorias fiscales.
- Perfil censal.
- Perfil RETA.
- Tramites.
- Requisitos de tramites.
- Presentaciones o borradores.
- Checklists.
- Documentos asociados.
- Campos extra en empresas, contactos, presupuestos y facturas.
- Informes PDF internos.

### Donde verlo en Odoo

Menu principal:

```text
Autonomo
```

Apartados:

- `Autonomo > Panel`
- `Autonomo > Maestros > Actividades`
- `Autonomo > Maestros > Categorias fiscales`
- `Autonomo > Perfiles > Censal`
- `Autonomo > Perfiles > RETA`
- `Autonomo > Tramites > Catalogo de tramites`
- `Autonomo > Tramites > Presentaciones`

---

## 4. Actividades economicas

### Para que sirve

Sirve para registrar las actividades que realiza el autonomo: montaje, carpinteria, reformas, electricidad, reparaciones, etc.

Cada actividad puede guardar:

- Codigo interno.
- Empresa.
- Tipo de actividad: empresarial o profesional.
- Epigrafe IAE.
- Codigo CNAE.
- Metodo IRPF.
- Regimen IVA.
- Cuentas contables por defecto.
- Impuestos por defecto.
- Porcentaje de IVA deducible por defecto.
- Direccion de actividad.
- Fuentes oficiales.

### Que puedes hacer tu

Entrar en:

```text
Autonomo > Maestros > Actividades
```

Y crear o revisar actividades.

### Que me puedes pedir

- "Crea una actividad de instalacion electrica".
- "Anade campos que falten para actividades".
- "Revisa si el IAE y CNAE de una actividad tienen sentido, usando fuentes oficiales".
- "Genera el PDF de ficha de actividad".
- "Haz 10 ejemplos mas de actividades".

---

## 5. Categorias fiscales

### Para que sirve

Sirve para clasificar ingresos y gastos de forma fiscal: materiales, herramientas, combustible, seguro, gestoria, publicidad, etc.

Cada categoria puede guardar:

- Codigo.
- Tipo: ingreso, gasto, inversion, retencion u otro.
- Porcentaje deducible IRPF.
- Porcentaje deducible IVA.
- Modelo relacionado.
- Fuente oficial.
- Vigencia.
- Notas.

### Que puedes hacer tu

Entrar en:

```text
Autonomo > Maestros > Categorias fiscales
```

Y revisar las categorias demo.

### Que me puedes pedir

- "Crea categorias fiscales para herramientas y vehiculo".
- "Revisa combustible con fuentes oficiales".
- "Marca telefonia como parcialmente deducible".
- "Anade reglas para que ciertos gastos pidan revision humana".
- "Genera el PDF de resumen de categoria fiscal".

---

## 6. Perfil censal

### Para que sirve

Sirve para guardar una ficha interna con datos relacionados con el censo de empresarios, profesionales y retenedores.

No es el formulario oficial del modelo 036. Es una ficha interna para preparar y revisar datos.

Puede guardar:

- NIF.
- Estado censal.
- Fecha de alta o baja.
- Residencia fiscal.
- Direccion fiscal.
- Direccion de notificaciones.
- Actividad principal.
- Codigos IAE y CNAE.
- Regimen IVA.
- Metodo IRPF.
- Obligaciones de retener.
- Operaciones intracomunitarias.
- Representante.
- Notificaciones electronicas.
- Ultima presentacion 036.

### Donde verlo

```text
Autonomo > Perfiles > Censal
```

### Que me puedes pedir

- "Revisa si faltan datos para alta censal".
- "Crea checklist para modelo 036".
- "Genera PDF de ficha censal".
- "Anade configuracion versionada por ejercicio del modelo 036".
- "Busca la fuente oficial actual del modelo 036".

---

## 7. Perfil RETA

### Para que sirve

Sirve para guardar una ficha interna relacionada con el alta o situacion en el Regimen Especial de Trabajadores Autonomos.

No presenta automaticamente altas, bajas ni modificaciones RETA.

Puede guardar:

- Estado RETA.
- Fecha de alta y baja.
- IAE.
- CNAE.
- Direccion de actividad.
- Rendimientos netos estimados.
- Base de cotizacion seleccionada.
- Codigo de tramo.
- Mutua.
- Coberturas.
- Bonificaciones o reducciones.
- Cuenta bancaria, protegida para administradores.
- Situaciones especiales.

### Donde verlo

```text
Autonomo > Perfiles > RETA
```

### Que me puedes pedir

- "Crea checklist de alta RETA".
- "Revisa que datos faltan para alta RETA".
- "Anade fuentes oficiales de Importass".
- "Genera PDF de ficha RETA".
- "No envies NSS ni IBAN a IA".

---

## 8. Tramites

### Para que sirve

Sirve para definir tramites oficiales o administrativos que puede necesitar el autonomo.

Ejemplos cargados:

- Alta modelo 036.
- Modificacion modelo 036.
- Baja modelo 036.
- Alta RETA.
- Modificacion RETA.
- Baja RETA.
- Aportacion documental TGSS.
- Solicitud de bonificacion.
- Cambio de base.
- Comunicacion de nueva actividad.

Cada tramite puede guardar:

- Organismo: AEAT, TGSS, SEPE, regional, local u otro.
- Tipo: alta, modificacion, baja, declaracion, Seguridad Social, beneficio, documento.
- Modelo.
- Periodicidad.
- Fuente oficial.
- Referencia legal.
- Si requiere presentacion humana.
- Requisitos.

### Donde verlo

```text
Autonomo > Tramites > Catalogo de tramites
```

### Que me puedes pedir

- "Crea un tramite para modelo 303".
- "Anade requisitos oficiales al alta RETA".
- "Revisa fuentes de un tramite".
- "Marca un tramite como pendiente de verificacion legal".
- "Crea 10 tramites demo nuevos".

---

## 9. Requisitos y checklists

### Para que sirve

Sirve para controlar si un tramite tiene todos los datos y documentos necesarios.

Un requisito puede ser:

- Dato.
- Documento.
- Declaracion.
- Autorizacion.
- Firma.
- Pago.
- Adjunto.
- Otro.

El checklist controla:

- Requisito.
- Si es obligatorio.
- Condicion.
- Dato presente.
- Documento adjunto.
- Verificado.
- Fuente oficial.
- Estado.

Regla importante:

No se puede marcar una presentacion como lista si hay requisitos obligatorios sin verificar.

### Donde verlo

```text
Autonomo > Tramites > Presentaciones
```

Abrir una presentacion y usar:

- `Actualizar checklist`
- `Marcar listo`

### Que me puedes pedir

- "Prueba que no deja marcar listo si falta un requisito".
- "Crea requisitos condicionales".
- "Anade documentos obligatorios para una bonificacion".
- "Haz una vista mejor de checklist".
- "Genera un informe PDF de checklist".

---

## 10. Presentaciones y documentos

### Para que sirve

Sirve para registrar borradores, revisiones, presentaciones, justificantes y recibos.

Estados disponibles:

- Borrador.
- Incompleto.
- Revision.
- Listo.
- Presentado.
- Aceptado.
- Rechazado.
- Corregido.
- Cancelado.

Puede guardar:

- Procedimiento.
- Periodo fiscal.
- Fecha de borrador.
- Fecha de revision.
- Fecha de listo.
- Fecha de presentacion.
- Canal.
- Referencia.
- CSV.
- Resultado.
- Importe.
- Metodo de pago.
- IBAN enmascarado.
- Archivo generado.
- Justificante.
- Aprobacion humana.
- Hash de snapshot.
- Documentos.

### Que me puedes pedir

- "Crea una presentacion demo incompleta".
- "Adjunta un justificante".
- "Comprueba hashes de documentos".
- "Haz que una presentacion pida aprobacion humana".
- "Crea PDF resumen de presentacion".

---

## 11. Campos extra en presupuestos

### Para que sirve

En `autonomo_core` ya se ampliaron los presupuestos de Odoo con campos basicos para fiscalidad y costes.

Campos actuales:

- Actividad.
- Lugar de trabajo.
- Descripcion de alcance.
- Coste estimado.
- Margen estimado.
- Porcentaje de margen.
- Si requiere anticipo.
- Porcentaje de anticipo.
- Estado de revision fiscal.

### Donde verlo

```text
Ventas > Presupuestos
```

En el formulario aparece informacion adicional de autonomo.

### Que me puedes pedir

- "Crea el modulo autonomo_quotes".
- "Anade kilometraje, combustible, peajes y dietas".
- "Calcula margen automaticamente".
- "Genera versiones de presupuesto".
- "Crea PDF de presupuesto profesional".

---

## 12. Campos extra en facturas

### Para que sirve

Permite conectar facturas y lineas contables con actividad, periodo, documento y deducibilidad.

En facturas:

- Actividad.
- Fecha de operacion.
- Tipo de documento fiscal.
- Estado en libro de ingresos/gastos.
- Periodo fiscal.
- Estado de revision fiscal.
- Adjunto origen.
- Hash del documento.
- UUID factura electronica.
- Estado factura electronica.
- Fecha efectiva de pago.
- Bloqueo de libro.

En lineas:

- Actividad.
- Categoria fiscal.
- Porcentaje deducible IRPF.
- Porcentaje deducible IVA.
- Importe deducible IRPF.
- Importe deducible IVA.
- Retencion snapshot.
- Bien de inversion.
- Revision de deducibilidad.
- Notas.

### Donde verlo

```text
Contabilidad > Facturas
```

### Que me puedes pedir

- "Calcula deducibilidad de una factura".
- "Bloquea facturas contabilizadas".
- "Crea reglas para gastos parcialmente deducibles".
- "Prepara libros de ingresos y gastos".
- "Haz el modulo autonomo_tax".

---

## 13. Informes PDF actuales

### Para que sirven

Son informes internos para revisar informacion.

No son formularios oficiales.

PDF disponibles:

- Ficha de actividad economica.
- Resumen de categoria fiscal.
- Ficha censal interna.
- Ficha RETA interna.

### Que me puedes pedir

- "Genera PDF de una actividad".
- "Mejora el diseno del PDF".
- "Anade pie legal y fuentes".
- "Crea PDF de checklist".
- "Crea PDF de consulta BOE".

---

## 14. Modulo `autonomo_legal_connector`

### Para que sirve

Sirve para conectar Odoo con la API oficial de legislacion consolidada del BOE.

Permite guardar:

- Metadatos BOE.
- Metadata ELI.
- Analisis.
- Materias.
- Relaciones normativas anteriores.
- Relaciones normativas posteriores.
- Indice de bloques.
- Bloques o articulos.
- Versiones de cada bloque.
- Hashes SHA-256.
- Estado de sincronizacion.
- Errores.

### Donde verlo

```text
Autonomo > Legal BOE
```

Apartados:

- `Fuentes BOE`
- `Bloques`
- `Consultas`
- `Sincronizaciones`
- `Configuracion`

---

## 15. Fuentes BOE

### Para que sirve

Sirve para ver cada norma y su estado de sincronizacion.

Normas iniciales cargadas:

- BOE-A-2007-13409 - Estatuto del trabajo autonomo.
- BOE-A-2006-20764 - Ley del IRPF.
- BOE-A-2007-6820 - Reglamento del IRPF.
- BOE-A-1992-28740 - Ley del IVA.
- BOE-A-1992-28925 - Reglamento del IVA.
- BOE-A-2012-14696 - Reglamento de facturacion.
- BOE-A-2019-10487 - Libros registro del IRPF.
- BOE-A-2003-23186 - Ley General Tributaria.
- BOE-A-2022-12482 - Cotizacion autonomos por rendimientos.
- BOE-A-2023-24840 - Sistemas informaticos de facturacion.
- BOE-A-2024-22138 - Especificaciones tecnicas de facturacion.

Tambien existe la fuente de la propia API BOE.

### Botones disponibles

En una fuente BOE:

- `Sincronizar metadatos`
- `Sincronizar ELI`
- `Sincronizar analisis`
- `Sincronizar indice`
- `Sincronizar versiones`
- `Sincronizar BOE`

### Que me puedes pedir

- "Sincroniza todas las normas BOE".
- "Sincroniza solo la Ley del IVA".
- "Busca articulos modificados".
- "Mira normas posteriores que derogan algo".
- "Comprueba si una fuente esta caducada".

---

## 16. Metadatos BOE

### Para que sirve

Guardan la identidad oficial de la norma.

Campos incluidos:

- Identificador BOE.
- Fecha de actualizacion BOE.
- Ambito.
- Departamento.
- Rango.
- Fecha de disposicion.
- Numero oficial.
- Titulo.
- Diario.
- Fecha de publicacion.
- Numero de diario.
- Fecha de vigencia.
- Estatus de derogacion.
- Estatus de anulacion.
- Vigencia agotada.
- Estado de consolidacion.
- URL ELI.
- URL HTML consolidada.
- Hash de metadatos.

### Que me puedes pedir

- "Dime la fecha de vigencia de BOE-A-2007-13409".
- "Lista normas con estado de derogacion".
- "Comprueba hash de metadatos".
- "Actualiza metadatos de todas las normas".

---

## 17. Analisis BOE

### Para que sirve

Guarda materias y relaciones oficiales de cada norma.

Incluye:

- Materias.
- Normas anteriores.
- Normas posteriores.
- Tipo de relacion.
- Descripcion.
- Marca de revision humana si hay derogacion o anulacion.

### Que me puedes pedir

- "Que normas posteriores modifican el Estatuto del autonomo".
- "Busca relaciones criticas".
- "Dime que normas hay que revisar manualmente".
- "Anade automaticamente normas posteriores al catalogo".

---

## 18. Bloques BOE

### Para que sirve

Guarda el indice estructurado de una norma.

Un bloque puede ser:

- Preambulo.
- Titulo.
- Capitulo.
- Articulo.
- Disposicion.
- Anexo.

Cada bloque guarda:

- Identificador.
- Tipo.
- Titulo.
- Fecha de actualizacion.
- Fecha de caducidad si existe.
- URL oficial.
- Hash de contenido.
- Versiones.

### Estado actual de base

Se cargaron:

- 1.697 bloques.
- 3.362 versiones.
- 0 bloques sin versiones.

### Que me puedes pedir

- "Abre el articulo 1 del Estatuto del autonomo".
- "Sincroniza versiones de un bloque".
- "Busca bloques modificados desde una fecha".
- "Genera resumen de cambios por norma".

---

## 19. Versiones BOE

### Para que sirve

Sirve para conservar el historico de redacciones de cada bloque o articulo.

Cada version guarda:

- Norma modificadora.
- Fecha de publicacion.
- Fecha de vigencia.
- Contenido HTML.
- Hash SHA-256.
- Hash de embedding futuro.

Regla importante:

Las versiones no se borran. Si BOE devuelve una redaccion nueva, se crea otra version. Si devuelve una version ya conocida, se conserva y se actualiza metadata si procede.

### Que me puedes pedir

- "Compara versiones de un articulo".
- "Detecta cambios en una norma".
- "Prepara embeddings solo para versiones nuevas".
- "Lista articulos con varias versiones".

---

## 20. Consultas legales

### Para que sirve

Sirve para registrar preguntas, respuestas y citas legales.

Todavia no es una IA fiscal completa. Es una base para registrar consultas y fuentes.

Puede guardar:

- Pregunta.
- Payload anonimizado.
- Hash del payload.
- Respuesta.
- Estado.
- Citas.

### Que me puedes pedir

- "Crea una consulta legal sobre alta RETA".
- "Anade citas BOE a una consulta".
- "Rechaza una respuesta sin fuentes".
- "Anonimiza un texto antes de revisarlo".

---

## 21. Sincronizaciones BOE

### Para que sirve

Sirve para auditar cada llamada o proceso de sincronizacion.

Guarda:

- Fuente.
- Identificador BOE.
- Tipo de sincronizacion.
- Estado.
- Fecha de inicio.
- Fecha final.
- Hash.
- Registros creados.
- Registros actualizados.
- Error si existe.

### Que me puedes pedir

- "Mira errores de sincronizacion".
- "Reintenta los fallos".
- "Dime cuando fue la ultima sincronizacion".
- "Comprueba si todas las normas tienen hash".

---

## 22. Seguridad

### Para que sirve

Controla quien puede ver o modificar datos.

Grupos actuales:

- Usuario autonomo.
- Responsable autonomo.
- Contabilidad autonomo.
- Revisor IA.
- Administrador autonomo.

Campos sensibles:

- NSS.
- Cuenta bancaria.
- Token API.
- Adjuntos sensibles.

### Que me puedes pedir

- "Crea un usuario operativo sin permisos fiscales".
- "Comprueba permisos del grupo usuario".
- "Oculta mas campos sensibles".
- "Haz que solo admin pueda sincronizar fuentes".

---

## 23. Pruebas

### Para que sirven

Sirven para comprobar que los modulos cargan y que las reglas importantes funcionan.

Pruebas actuales:

`autonomo_core`:

- Restricciones de actividad.
- Porcentajes de categorias.
- Checklist obligatorio.
- Bloqueo de marcar listo.
- Renderizado de PDF.

`autonomo_legal_connector`:

- Conexion real BOE.
- Sincronizacion de metadatos.
- Sincronizacion de analisis.
- Sincronizacion de metadata ELI.
- Sincronizacion de indice.
- Sincronizacion de versiones de bloque.
- Hash de consulta.

### Que me puedes pedir

- "Ejecuta tests de autonomo_core".
- "Ejecuta tests de autonomo_legal_connector".
- "Crea tests para permisos".
- "Crea tests para sincronizacion masiva".
- "Corrige errores de tests".

---

## 24. Que falta por hacer

### `autonomo_quotes`

Para presupuestos avanzados:

- Mano de obra.
- Materiales.
- Kilometraje.
- Combustible.
- Peajes.
- Aparcamiento.
- Dietas.
- Herramientas.
- Subcontratas.
- Mediciones.
- Versiones.
- Anticipos.
- Margenes.

### `autonomo_tax`

Para fiscalidad:

- Obligaciones.
- Calendario.
- Periodos.
- Modelos 303, 130, 111, 115, 180, 190, 390, 347, 349.
- Libros registro.
- Snapshots.
- Cierres.
- Exportaciones.
- Justificantes.

### `autonomo_ai_review`

Para revisiones con IA:

- Revisiones.
- Citas.
- Incidencias.
- Aceptar/rechazar.
- Solicitar revision humana.
- Bloquear respuestas sin fuentes.

### Backups

Faltan scripts:

- `backup.ps1`
- `backup.sh`
- `restore.ps1`
- `restore.sh`

---

## 25. Ejemplos de cosas que puedes pedirme

### Sobre Odoo

- "Entra a revisar si el modulo esta instalado".
- "Mira los errores de Odoo".
- "Reinicia Odoo".
- "Haz una actualizacion del modulo".

### Sobre BOE

- "Sincroniza la Ley del IVA".
- "Busca normas posteriores que modifican el Estatuto del autonomo".
- "Compara versiones del articulo 1".
- "Genera informe de cambios normativos".

### Sobre fiscalidad

- "No inventes, busca fuente oficial".
- "Crea obligaciones demo para modelo 303".
- "Prepara estructura del modelo 130 sin codificar casillas fijas".
- "Marca esto como pendiente de revision humana".

### Sobre presupuestos

- "Crea autonomo_quotes".
- "Haz calculadora de kilometraje".
- "Anade versiones de presupuesto".
- "Genera PDF de presupuesto profesional".

### Sobre seguridad

- "Revisa permisos".
- "Oculta datos sensibles".
- "Comprueba que usuario operativo no modifica configuracion fiscal".

### Sobre Git

- "Crea una rama para autonomo_tax".
- "Haz commit".
- "Dime que cambios tiene esta rama".
- "Prepara merge a develop".

---

## 26. Forma recomendada de trabajar conmigo

Para avanzar con orden, pideme una cosa asi:

```text
Crea el modulo autonomo_quotes en una rama nueva, instala, prueba, carga demo y haz commit.
```

O:

```text
Revisa con fuentes oficiales el modelo 303 y prepara solo el diseno tecnico sin implementar casillas fijas.
```

O:

```text
Sincroniza BOE y dime que normas posteriores afectan al Estatuto del autonomo.
```

La regla buena: primero fuente oficial, luego modelo configurable, luego tests, luego instalacion, luego commit.
