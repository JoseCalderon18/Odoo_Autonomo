from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
PDF_PATH = OUT / "manual_uso_autonomo_odoo.pdf"


class CycleFlow(Flowable):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.width = 16.4 * cm
        self.height = 12.0 * cm

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    def draw(self):
        c = self.canv
        box_w = self.width
        box_h = 1.0 * cm
        y = self.height - box_h
        palette = [
            colors.HexColor("#2F6F73"),
            colors.HexColor("#875A7B"),
            colors.HexColor("#B7791F"),
            colors.HexColor("#3F7C47"),
            colors.HexColor("#4A5568"),
            colors.HexColor("#24527A"),
            colors.HexColor("#8A4B38"),
            colors.HexColor("#5B5E8E"),
        ]
        for index, (title, body) in enumerate(self.steps, start=1):
            fill = palette[(index - 1) % len(palette)]
            c.setFillColor(colors.HexColor("#F8FAFC"))
            c.setStrokeColor(colors.HexColor("#E2E8F0"))
            c.roundRect(0, y, box_w, box_h, 7, stroke=1, fill=1)
            c.setFillColor(fill)
            c.circle(0.45 * cm, y + 0.5 * cm, 0.22 * cm, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(0.45 * cm, y + 0.41 * cm, str(index))
            c.setFillColor(colors.HexColor("#111827"))
            c.setFont("Helvetica-Bold", 9)
            c.drawString(0.85 * cm, y + 0.58 * cm, title)
            c.setFillColor(colors.HexColor("#4B5563"))
            c.setFont("Helvetica", 7.8)
            c.drawString(0.85 * cm, y + 0.25 * cm, body[:135])
            if index < len(self.steps):
                c.setStrokeColor(colors.HexColor("#CBD5E1"))
                c.line(box_w / 2, y - 0.08 * cm, box_w / 2, y - 0.28 * cm)
            y -= 1.38 * cm


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(doc.leftMargin, 1.35 * cm, A4[0] - doc.rightMargin, 1.35 * cm)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(doc.leftMargin, 0.85 * cm, "Manual interno de uso - Odoo autonomo Espana")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.85 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=10) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontSize=6,
    )


def module_block(name, purpose, has, use_for, relation):
    styles = build_styles()
    rows = [
        [Paragraph("<b>Para que sirve</b>", styles["CellHead"]), Paragraph(purpose, styles["Cell"])],
        [Paragraph("<b>Que tiene</b>", styles["CellHead"]), Paragraph(has, styles["Cell"])],
        [Paragraph("<b>Cuando usarlo</b>", styles["CellHead"]), Paragraph(use_for, styles["Cell"])],
        [Paragraph("<b>Relacion BOE/fuentes</b>", styles["CellHead"]), Paragraph(relation, styles["Cell"])],
    ]
    table = Table(rows, colWidths=[4.0 * cm, 12.0 * cm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, -2), 0.35, colors.HexColor("#E2E8F0")),
            ]
        )
    )
    return KeepTogether([p(name, styles["H2"]), table, Spacer(1, 0.28 * cm)])


def build_styles():
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=29,
            textColor=colors.HexColor("#111827"),
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#4B5563"),
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "H1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=colors.HexColor("#2F6F73"),
            spaceBefore=10,
            spaceAfter=8,
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#111827"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontSize=9.4,
            leading=13.4,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=5,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=4,
        ),
        "Cell": ParagraphStyle(
            "Cell",
            parent=base["BodyText"],
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#1F2937"),
        ),
        "CellHead": ParagraphStyle(
            "CellHead",
            parent=base["BodyText"],
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#111827"),
        ),
    }


def build_pdf():
    OUT.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.7 * cm,
        title="Manual de uso Odoo autonomo",
        author="Codex",
    )
    story = []

    story += [
        Spacer(1, 1.1 * cm),
        p("Manual de uso", styles["Title"]),
        p("Odoo para autonomo en Espana: modulos, BOE, presupuestos, compras, fiscalidad e IA", styles["Subtitle"]),
        p(
            "Este documento explica como usar el sistema creado en Odoo. Es una guia interna: ayuda a ordenar trabajo, datos, documentos y revisiones, pero no sustituye a un asesor fiscal ni a la consulta directa de fuentes oficiales.",
            styles["Body"],
        ),
        Spacer(1, 0.3 * cm),
    ]

    summary_raw = [
        ["Modulo", "Idea principal", "Donde se usa"],
        ["Autonomo Core", "Base comun: empresa, actividades, categorias, censo, RETA, tramites y dashboard.", "Menu Autonomo y fichas base."],
        ["Autonomo Quotes", "Presupuestos con horas, kilometros, materiales, costes, margen y versiones.", "Ventas - Presupuestos."],
        ["Autonomo Tax", "Periodos, obligaciones, libros, borradores, snapshots y documentacion fiscal.", "Autonomo - Fiscalidad."],
        ["Legal BOE", "Fuentes oficiales, consultas legales, versiones y trazabilidad BOE.", "Autonomo - Legal BOE."],
        ["AI Review", "Revisiones IA con citas, incidencias y aprobacion humana.", "Autonomo - Revisiones IA."],
    ]
    summary_rows = [
        [Paragraph(cell, styles["CellHead"] if row_index == 0 else styles["Cell"]) for cell in row]
        for row_index, row in enumerate(summary_raw)
    ]
    table = Table(summary_rows, colWidths=[3.2 * cm, 8.6 * cm, 4.2 * cm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F6F73")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.2),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 1), (-1, -1), 0.35, colors.HexColor("#E2E8F0")),
            ]
        )
    )
    story += [table, PageBreak()]

    story += [p("1. Para Que Sirve Cada Modulo", styles["H1"])]
    modules = [
        (
            "Autonomo Core",
            "Es la base del sistema. Guarda la informacion estable del autonomo: empresa, titular, actividades economicas, categorias fiscales, perfil censal, perfil RETA, tramites, requisitos, documentos y dashboard.",
            "Actividades, categorias fiscales, tramites oficiales, requisitos, presentaciones/documentos, extensiones de cliente, empresa, presupuesto y factura, informes PDF base.",
            "Se usa primero. Antes de presupuestar o declarar, aqui deben estar bien configurados los datos de empresa, actividad, direccion fiscal, categorias y obligaciones basicas.",
            "Guarda fuentes oficiales y referencias, pero no calcula por si solo una declaracion oficial. Los datos sensibles se tratan como informacion interna.",
        ),
        (
            "Autonomo Quotes",
            "Amplia Ventas para que un presupuesto tenga sentido para un autonomo: horas de trabajo, kilometraje, dietas, aparcamiento, peajes, alojamiento, materiales previstos, mediciones, recargos, versiones y coste interno.",
            "Tarifas de desplazamiento, conceptos de coste, plantillas, materiales previstos, mediciones, versiones, PDF profesional y hoja interna de costes.",
            "Se usa cuando un cliente pide precio. Creas presupuesto en Ventas, rellenas horas/km/materiales, vuelcas materiales a lineas y descargas el PDF para cliente.",
            "El presupuesto no es una factura oficial. El PDF muestra descripcion, importes, impuestos y totales para claridad comercial; los costes internos y beneficio no se muestran al cliente.",
        ),
        (
            "Autonomo Tax",
            "Ordena la parte fiscal: periodos, obligaciones, vencimientos, libros, borradores, snapshots, justificantes y estado de revision.",
            "Modelo 303, 130, 111, 115 y anuales como estructura configurable; libros de ventas/gastos, bienes de inversion, resumen trimestral y checklists.",
            "Se usa despues de registrar ventas, facturas y gastos. Sirve para revisar datos, preparar borradores y saber que falta antes de presentar nada.",
            "No fija casillas ni plazos en codigo como definitivos. Deben venir de fuente oficial versionada por ejercicio y marcarse como verificados.",
        ),
        (
            "Autonomo Legal Connector",
            "Es el modulo Legal BOE. Sirve para conectar con un servicio que consulta BOE y fuentes oficiales, guarda versiones, citas, errores y fecha de consulta.",
            "Configuracion del servicio, fuentes legales, consultas, citas, estados de sincronizacion, hashes, vigencia y trazabilidad.",
            "Se usa cuando quieres saber de donde sale una regla, revisar si una norma cambio o documentar una decision fiscal/legal.",
            "Relacion directa con la API oficial de legislacion consolidada del BOE. La legislacion consolidada se marca como informativa y no como sustituto del diario oficial.",
        ),
        (
            "Autonomo AI Review",
            "Registra revisiones asistidas por IA sobre presupuestos, facturas, trimestres, tramites o dudas generales, siempre con citas y aprobacion humana.",
            "Revisiones IA, citas, incidencias, riesgo, estado, aceptacion/rechazo y PDF de revision o incidencias.",
            "Se usa para detectar faltantes: documento pendiente, impuesto dudoso, duplicado, dato sin fuente o caso que debe mirar una persona.",
            "No debe enviar NIF, NSS, IBAN ni datos personales sin anonimizar a servicios externos. Rechaza respuestas sin fuentes o con fuentes caducadas.",
        ),
    ]
    for block in modules:
        story.append(module_block(*block))

    story += [PageBreak(), p("2. Donde Va Cada Dato", styles["H1"])]
    story += [
        p("Productos y articulos", styles["H2"]),
        bullets(
            [
                "<b>Productos</b>: es el catalogo de Odoo. Aqui van madera, tornillos, tubos, perfiles, servicios, mano de obra, alquileres o cualquier cosa reutilizable.",
                "<b>Unidad de medida</b>: usa unidades, horas, dias, metros, metros cuadrados o la unidad que corresponda. Madera por dimensiones puede ir como producto con notas de largo/ancho/grosor en el presupuesto.",
                "<b>No comprado todavia</b>: va en <b>Materiales previstos</b> dentro del presupuesto.",
                "<b>Comprado de verdad</b>: va en <b>Compras</b>, enlazando la linea de compra con el material previsto.",
            ],
            styles["Body"],
        ),
        p("Costes privados vs datos para cliente", styles["H2"]),
        bullets(
            [
                "Al cliente se le muestra lo necesario: trabajo, desplazamiento, materiales mostrables, impuestos y total.",
                "El coste interno, beneficio estimado, margen, notas internas y hoja interna de costes son para ti.",
                "Si un material no debe verse en el PDF del cliente, desmarca <b>Mostrar al cliente</b> en Materiales previstos.",
            ],
            styles["Body"],
        ),
        p("Compras relacionadas con presupuesto", styles["H2"]),
        bullets(
            [
                "En la compra puedes elegir <b>Presupuesto relacionado</b>.",
                "En cada linea de compra puedes elegir <b>Material previsto relacionado</b>.",
                "Asi se ve que el tablero, los tornillos o el tubo comprado pertenecen a un presupuesto concreto.",
            ],
            styles["Body"],
        ),
    ]

    story += [PageBreak(), p("3. Relacion Con BOE Y Fuentes Oficiales", styles["H1"])]
    story += [
        p(
            "El sistema esta pensado para trabajar con fuentes oficiales, no con blogs ni reglas inventadas. Cuando una regla sea legal, fiscal o de Seguridad Social, debe quedar guardada con fuente, version, fecha de consulta y estado de revision.",
            styles["Body"],
        ),
        p("Que consulta Legal BOE", styles["H2"]),
        bullets(
            [
                "Listado de normas consolidadas.",
                "Metadatos de una norma.",
                "Analisis, relaciones, modificaciones y vigencia.",
                "Indice del texto consolidado.",
                "Bloques o articulos concretos.",
                "Hash del contenido para saber si cambio.",
            ],
            styles["Body"],
        ),
        p("Aviso importante", styles["H2"]),
        p(
            "La API de legislacion consolidada del BOE es una API REST de consulta. El propio BOE indica que los textos consolidados son informativos y que, para efectos juridicos, debe consultarse la publicacion oficial. Por eso el sistema guarda fuentes y exige revision humana cuando hay dudas o contradicciones.",
            styles["Body"],
        ),
        p("Normas y fuentes iniciales contempladas", styles["H2"]),
        bullets(
            [
                "BOE-A-2007-13409 - Estatuto del trabajo autonomo.",
                "BOE-A-2006-20764 y BOE-A-2007-6820 - IRPF y su reglamento.",
                "BOE-A-1992-28740 y BOE-A-1992-28925 - IVA y su reglamento.",
                "BOE-A-2012-14696 - Reglamento de facturacion.",
                "BOE-A-2023-24840 y BOE-A-2024-22138 - sistemas informaticos de facturacion y especificaciones.",
                "Agencia Tributaria, Seguridad Social/TGSS, Importass, SEPE y organismos oficiales cuando corresponda.",
            ],
            styles["Body"],
        ),
    ]

    story += [PageBreak(), p("4. Ciclo De Vida Completo", styles["H1"])]
    story += [
        p(
            "Este es el recorrido recomendado para que los datos nazcan en el sitio correcto y despues se puedan reutilizar en presupuestos, compras, facturas, libros fiscales y revisiones.",
            styles["Body"],
        ),
        CycleFlow(
            [
                ("Configurar base", "Empresa, autonomo, actividad, categorias fiscales, datos censales y RETA."),
                ("Crear catalogo", "Productos, servicios, materiales, unidades de medida y costes recurrentes."),
                ("Crear presupuesto", "Ventas - Presupuestos: cliente, trabajo, horas, km, dietas y condiciones."),
                ("Planificar materiales", "Materiales previstos: madera, tornillos, tubos, medidas, precio y visibilidad cliente."),
                ("Volcar materiales", "Boton Volcar materiales: crea lineas reales en el presupuesto y actualiza totales/PDF."),
                ("Comprar si hace falta", "Compras: proveedor, presupuesto relacionado y linea de material prevista."),
                ("Aprobar y facturar", "Si el cliente acepta, el presupuesto pasa a pedido y luego a factura de cliente."),
                ("Registrar gastos", "Facturas recibidas y compras se clasifican por actividad y categoria fiscal."),
                ("Revisar trimestre", "Autonomo Tax genera libros, snapshots, checklists y borradores informativos."),
                ("Revisar fuentes e IA", "Legal BOE y AI Review verifican fuentes, incidencias y necesidad de revision humana."),
            ]
        ),
    ]

    story += [PageBreak(), p("5. Uso Practico Rapido", styles["H1"])]
    quick_rows = [
        ["Necesitas", "Hazlo en", "Resultado"],
        ["Presupuesto para cliente", "Ventas - Presupuestos", "PDF profesional con trabajo, materiales publicos, impuestos y total."],
        ["Horas y kilometraje", "Pestana Costes y kilometraje", "Importes calculados para presupuesto y control interno."],
        ["Madera con medidas", "Materiales previstos", "Producto + cantidad + largo/ancho/grosor + nota de medidas."],
        ["Tornillos por unidad", "Productos + Materiales previstos", "Cantidad por unidades y precio previsto."],
        ["Tubos por metro", "Productos con unidad metro", "Cantidad en metros y precio por metro."],
        ["Material ya comprado", "Compras", "Compra enlazada al presupuesto y al material previsto."],
        ["Beneficio neto", "Datos internos de presupuesto", "No se muestra al solicitante en PDF publico."],
        ["Libro fiscal", "Autonomo Tax", "Resumen informativo y exportable para revision."],
        ["Duda legal", "Legal BOE", "Consulta con fuente, version y fecha de consulta."],
        ["Revision automatizada", "AI Review", "Incidencia o revision con citas y aprobacion humana."],
    ]
    quick_table = Table(quick_rows, colWidths=[4.1 * cm, 5.1 * cm, 6.8 * cm], hAlign="LEFT")
    quick_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#875A7B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.1),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 1), (-1, -1), 0.35, colors.HexColor("#E5E7EB")),
            ]
        )
    )
    story.append(quick_table)
    story += [
        Spacer(1, 0.4 * cm),
        p("Fuentes oficiales citadas", styles["H2"]),
        bullets(
            [
                "BOE Datos Abiertos - API legislacion consolidada: https://www.boe.es/datosabiertos/api/api.php",
                "BOE API legislacion consolidada PDF: https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf",
                "BOE-A-2012-14696 - Reglamento de facturacion: https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696",
            ],
            styles["Small"],
        ),
        p(
            "Fecha de preparacion del manual: 26/07/2026. Revisar fuentes oficiales antes de presentar declaraciones, tramites o documentos con efecto juridico.",
            styles["Small"],
        ),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return PDF_PATH


if __name__ == "__main__":
    print(build_pdf())
