"""
Genera los entregables preliminares (Word .docx y PowerPoint .pptx) para
revisión, corrección y mejora del Grupo 3 — SIS-351 Machine Learning.

Entregables generados en /entregables:
  - Informe_Grupo3_Autoencoder_UMAP.docx
  - Presentacion_Grupo3_Autoencoder_UMAP.pptx
"""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Inches, Pt, RGBColor
from pptx import Presentation
from pptx.dml.color import RGBColor as PptRGB
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches as PptInches
from pptx.util import Pt as PptPt

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTADOS_DIR = BASE_DIR / "resultados"
ENTREGABLES_DIR = BASE_DIR / "entregables"


# ==============================================================================
# UTILIDADES PARA WORD (.docx)
# ==============================================================================


def _set_cell_shading(cell, fill_hex: str) -> None:
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def _set_cell_margins(cell, top=100, bottom=100, left=150, right=150) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def _agregar_recuadro(doc: Document, titulo: str, texto: str, color_fondo: str, color_borde: str) -> None:
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    _set_cell_shading(cell, color_fondo)
    _set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{color_borde}"/>'
        f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
        f"</w:tcBorders>"
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_tit = p.add_run(titulo + "\n")
    r_tit.bold = True
    r_tit.font.size = Pt(10.5)
    r_tit.font.color.rgb = RGBColor.from_string(color_borde)

    r_txt = p.add_run(texto)
    r_txt.font.size = Pt(10)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def _agregar_titulo_seccion(doc: Document, texto: str) -> None:
    p = doc.add_heading(texto, level=1)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)


def _agregar_subtitulo(doc: Document, texto: str) -> None:
    p = doc.add_heading(texto, level=2)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)


def _agregar_parrafo(doc: Document, texto: str, negrita_prefijo: str | None = None) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if negrita_prefijo:
        r0 = p.add_run(negrita_prefijo)
        r0.bold = True
        r0.font.size = Pt(10.5)
    r1 = p.add_run(texto)
    r1.font.size = Pt(10.5)


def _agregar_vineta(doc: Document, negrita: str, texto: str) -> None:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.12
    r0 = p.add_run(negrita)
    r0.bold = True
    r0.font.size = Pt(10.5)
    r1 = p.add_run(texto)
    r1.font.size = Pt(10.5)


def generar_informe_word(ruta_salida: Path) -> None:
    doc = Document()

    for section in doc.sections:
        section.top_margin = Cm(2.2)
        section.bottom_margin = Cm(2.2)
        section.left_margin = Cm(2.4)
        section.right_margin = Cm(2.4)

    estilo_normal = doc.styles["Normal"]
    estilo_normal.font.name = "Calibri"
    estilo_normal.font.size = Pt(10.5)

    # --------------------------------------------------------------------------
    # PORTADA
    # --------------------------------------------------------------------------
    for _ in range(3):
        doc.add_paragraph()

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_u = p_univ.add_run("[NOMBRE DE LA UNIVERSIDAD / FACULTAD / CARRERA]")
    r_u.bold = True
    r_u.font.size = Pt(13)
    r_u.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    p_mat = doc.add_paragraph()
    p_mat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_m = p_mat.add_run("SIS-351 Machine Learning — Evaluación 3er Parcial")
    r_m.font.size = Pt(12)
    r_m.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    for _ in range(2):
        doc.add_paragraph()

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_tit.add_run(
        "Autoencoder, UMAP y Clustering:\n"
        "Influencia de la Representación en el Aprendizaje No Supervisado"
    )
    r_t.bold = True
    r_t.font.size = Pt(20)
    r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run(
        "Análisis teórico y práctica experimental reproducible sobre el dataset Wine (PCA vs. UMAP + K-means)"
    )
    r_s.italic = True
    r_s.font.size = Pt(11.5)
    r_s.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    for _ in range(4):
        doc.add_paragraph()

    datos_portada = [
        ("Grupo:", "Grupo 3"),
        ("Integrantes:", "[Integrante 1 — Completar]\n[Integrante 2 — Completar]\n[Integrante 3 — Completar]"),
        ("Docente:", "[Nombre del Docente — Completar]"),
        ("Fecha:", "[Fecha de entrega — Completar]"),
    ]
    tbl_p = doc.add_table(rows=len(datos_portada), cols=2)
    tbl_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (k, v) in enumerate(datos_portada):
        c0, c1 = tbl_p.rows[idx].cells
        c0.width = Cm(4.0)
        c1.width = Cm(10.0)
        r0 = c0.paragraphs[0].add_run(k)
        r0.bold = True
        r0.font.size = Pt(11)
        r1 = c1.paragraphs[0].add_run(v)
        r1.font.size = Pt(11)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 1. INTRODUCCIÓN E IDENTIDAD
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "1. Introducción e Identidad del Paper")
    _agregar_parrafo(
        doc,
        "En el aprendizaje no supervisado, descubrir estructuras naturales y agrupamientos en datos sin "
        "etiquetas depende críticamente de cómo se representan las observaciones. En esta práctica "
        "estudiamos el uso conjunto de representaciones latentes (Autoencoders), reducción de dimensionalidad "
        "(PCA y UMAP) y clustering (K-means).",
    )
    _agregar_vineta(doc, "Título del paper: ", "[COMPLETAR]")
    _agregar_vineta(doc, "Autores: ", "[COMPLETAR]")
    _agregar_vineta(doc, "Año y publicación: ", "[COMPLETAR]")
    _agregar_vineta(doc, "Enlace y versión: ", "[COMPLETAR]")
    _agregar_parrafo(
        doc,
        "Analizar los fundamentos del autoencoder del paper (sin necesidad de entrenarlo) y comparar "
        "experimentalmente las representaciones 2D de PCA y UMAP bajo K-means con el mismo número de clusters k "
        "sobre el dataset Wine, respondiendo a la pregunta guía: ¿Cómo influye la representación en los patrones que vemos?",
        negrita_prefijo="Objetivo de la práctica: ",
    )

    # --------------------------------------------------------------------------
    # 2. PROBLEMA Y CONTRIBUCIÓN
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "2. Problema Abordado y Contribución Central")
    _agregar_subtitulo(doc, "2.1 El problema de la alta dimensionalidad y las representaciones")
    _agregar_parrafo(
        doc,
        "Cuando trabajamos con conjuntos de datos multivariados sin etiquetas, aplicar algoritmos de agrupamiento "
        "directamente en el espacio original suele verse afectado por la 'Maldición de la Dimensionalidad': las "
        "distancias euclidianas pierden poder discriminativo, las variables en distintas escalas dominan el cálculo "
        "y las relaciones no lineales permanecen ocultas.",
    )
    _agregar_parrafo(
        doc,
        "[COMPLETAR: describir el problema específico y dominio planteado por los autores del paper asignado al Grupo 3].",
        negrita_prefijo="Problema específico del paper: ",
    )

    _agregar_subtitulo(doc, "2.2 Contribución del paper y rol del Autoencoder")
    _agregar_parrafo(
        doc,
        "[COMPLETAR: describir la contribución, método o protocolo propuesto en el paper (arquitectura del autoencoder, "
        "uso de UMAP y estrategia de clustering)].",
    )

    # --------------------------------------------------------------------------
    # 3. FUNDAMENTOS Y CONEXIÓN CON SIS-351
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "3. Fundamentos Teóricos y Conexión con SIS-351")
    _agregar_subtitulo(doc, "3.1 El Autoencoder ('El Reloj de Arena Digital')")
    _agregar_parrafo(
        doc,
        "Tal como se estudió en la unidad de Deep Learning de SIS-351, un Autoencoder es una red neuronal no "
        "supervisada diseñada para aprender una representación comprimida de los datos de entrada sin utilizar "
        "etiquetas. Consta de un Codificador (Encoder) que proyecta la entrada hacia un espacio latente restringido "
        "(bottleneck) y un Decodificador (Decoder) que reconstruye la entrada original minimizando una función de "
        "pérdida de reconstrucción (habitualmente el Error Cuadrático Medio, MSE).",
    )
    _agregar_parrafo(
        doc,
        "[COMPLETAR: detallar la arquitectura exacta del autoencoder del paper (capas, función de activación, "
        "dimensión del bottleneck o variante utilizada) y por qué resulta útil antes o junto con UMAP].",
        negrita_prefijo="Autoencoder del paper: ",
    )

    _agregar_subtitulo(doc, "3.2 PCA, UMAP, K-means y Silhouette Score en SIS-351")
    _agregar_vineta(
        doc,
        "PCA (Análisis de Componentes Principales): ",
        "Técnica lineal rápida e interpretable que encuentra ejes ortogonales de máxima varianza global.",
    )
    _agregar_vineta(
        doc,
        "UMAP (Uniform Manifold Approximation and Projection): ",
        "Técnica no lineal basada en topología algebraica y grafos de vecindad (controlados por n_neighbors y min_dist) "
        "que equilibra la preservación de vecindades locales y estructura global.",
    )
    _agregar_vineta(
        doc,
        "K-means y Silhouette Score: ",
        "K-means agrupa por centroides asumiendo geometrías esféricas; el Silhouette Score (en [-1, 1]) mide "
        "cohesión intra-cluster frente a separación inter-cluster sin usar etiquetas reales.",
    )

    # --------------------------------------------------------------------------
    # 4. EXPERIMENTOS DEL PAPER
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "4. Experimentos Reportados en el Paper")
    _agregar_recuadro(
        doc,
        "SECCIÓN DE RESULTADOS PUBLICADOS EN EL PAPER (NO OBTENIDOS POR EL GRUPO)",
        "Los datos de esta sección pertenecen exclusivamente al paper de referencia del Grupo 3. "
        "Deben completarse únicamente con las cifras verificadas del artículo.",
        color_fondo="EFF6FF",
        color_borde="1D4ED8",
    )
    _agregar_vineta(doc, "Datasets evaluados en el paper: ", "[COMPLETAR]")
    _agregar_vineta(doc, "Comparadores / líneas base: ", "[COMPLETAR]")
    _agregar_vineta(doc, "Métricas y resultados publicados: ", "[COMPLETAR]")

    # --------------------------------------------------------------------------
    # 5. PRÁCTICA DEL GRUPO
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "5. Práctica Experimental del Grupo")
    _agregar_recuadro(
        doc,
        "RESULTADOS OBTENIDOS POR EL GRUPO (EVIDENCIA REPRODUCIBLE PROPIA)",
        "Experimento ejecutado por el grupo sobre Wine (scikit-learn) con StandardScaler, semilla global "
        "random_state=42 y sin utilizar etiquetas reales para ajustar modelos ni elegir k.",
        color_fondo="ECFDF5",
        color_borde="047857",
    )

    _agregar_subtitulo(doc, "5.1 Dataset, preprocesamiento y justificación de k")
    _agregar_parrafo(
        doc,
        "Utilizamos el dataset Wine de scikit-learn (178 muestras, 13 variables fisicoquímicas continuas). "
        "Aplicamos StandardScaler (media 0, desviación estándar 1) para evitar que variables de gran magnitud "
        "como 'proline' dominen las distancias euclidianas. Para elegir k de manera puramente no supervisada, "
        "evaluamos k = 2..6 sobre el espacio escalado: k = 3 presentó un codo claro en inercia (1277.93) y el "
        "máximo Silhouette Score (0.2849).",
    )
    ruta_k = RESULTADOS_DIR / "seleccion_k.png"
    if ruta_k.exists():
        p_k = doc.add_paragraph()
        p_k.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_k.add_run().add_picture(str(ruta_k), width=Inches(5.6))

    _agregar_subtitulo(doc, "5.2 Resultados comparativos: PCA 2D vs. UMAP 2D (K-means con k = 3)")
    filas_tabla = [
        ["Representación 2D", "k", "Silhouette Score", "Inercia 2D", "ARI (Comp. Externa)", "NMI (Comp. Externa)"],
        ["PCA 2D (Lineal)", "3", "0.5611", "259.5094", "0.8951", "0.8821"],
        ["UMAP 2D (No lineal)", "3", "0.7111", "202.2043", "0.8025", "0.7955"],
    ]
    tbl_res = doc.add_table(rows=len(filas_tabla), cols=6)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_res.style = "Table Grid"
    for r_idx, fila in enumerate(filas_tabla):
        for c_idx, val in enumerate(fila):
            cell = tbl_res.rows[r_idx].cells[c_idx]
            _set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if r_idx == 0:
                _set_cell_shading(cell, "1E3A8A")
                run.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif r_idx == 2 and c_idx == 2:
                run.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    ruta_clusters = RESULTADOS_DIR / "clusters_pca_umap.png"
    if ruta_clusters.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(ruta_clusters), width=Inches(6.1))

    ruta_sil = RESULTADOS_DIR / "comparacion_silhouette.png"
    if ruta_sil.exists():
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(str(ruta_sil), width=Inches(4.6))

    # --------------------------------------------------------------------------
    # 6. INTERPRETACIÓN Y CRÍTICA
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "6. Interpretación Crítica de las Visualizaciones")
    _agregar_parrafo(
        doc,
        "Los resultados muestran directamente cómo la representación transforma la geometría observable: "
        "en PCA 2D (que retiene el 55.41% de la varianza total: PC1 36.2%, PC2 19.21%), los tres grupos "
        "aparecen más dispersos y con fronteras cercanas, obteniendo un Silhouette Score de 0.5611. "
        "En contraste, UMAP 2D (n_neighbors=15, min_dist=0.1) agrupa las vecindades locales en islas "
        "visualmente mucho más compactas y separadas, elevando el Silhouette Score a 0.7111.",
    )
    _agregar_parrafo(
        doc,
        "Sin embargo, al realizar una comparación externa post-hoc frente a las etiquetas originales de Wine "
        "(sin haberlas usado para entrenar ni ajustar nada), PCA 2D alcanzó mayor concordancia externa "
        "(ARI = 0.8951, NMI = 0.8821) que UMAP 2D (ARI = 0.8025, NMI = 0.7955). Esto demuestra una lección "
        "fundamental para la pregunta guía: un Silhouette Score más alto en una proyección no lineal 2D "
        "refleja mayor compacidad en el mapa proyectado, pero no garantiza automáticamente mayor fidelidad a "
        "las clases reales cuando K-means particiona geometrías comprimidas por UMAP.",
        negrita_prefijo="Lectura crítica (Silhouette vs. fidelidad externa): ",
    )
    _agregar_vineta(
        doc,
        "Sensibilidad a hiperparámetros: ",
        "UMAP depende de n_neighbors, min_dist y la semilla aleatoria; cambiar estos valores modifica la forma "
        "y separación aparente de los clusters.",
    )
    _agregar_vineta(
        doc,
        "Supuesto de esfericidad de K-means: ",
        "K-means busca centroides esféricos en 2D, por lo que puede dividir o fusionar clusters elongados generados "
        "por proyecciones no lineales.",
    )

    # --------------------------------------------------------------------------
    # 7. REPRODUCIBILIDAD Y USO DE IA
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "7. Reproducibilidad y Declaración de Uso de IA")
    _agregar_parrafo(
        doc,
        "Entorno verificado: Windows 10, Python 3.14.0, scikit-learn 1.9.1, umap-learn 0.6.0, NumPy 2.5.5, "
        "Pandas 3.1.1. Semilla global random_state = 42 fijada en UMAP, PCA y K-means (n_init=20). Código "
        "disponible en src/experimento.py y notebooks/01_practica_grupo3_umap.ipynb.",
    )
    _agregar_parrafo(
        doc,
        "Se utilizó el asistente de IA Antigravity como apoyo para estructurar los archivos del proyecto, "
        "implementar el script reproducible en Python/Jupyter y generar este borrador inicial para revisión y "
        "mejora del grupo (dejando [COMPLETAR] en los datos del paper aún por definir). Todas las ejecuciones "
        "y métricas fueron verificadas localmente.",
        negrita_prefijo="Declaración de uso de IA: ",
    )

    # --------------------------------------------------------------------------
    # REFERENCIAS
    # --------------------------------------------------------------------------
    doc.add_page_break()
    _agregar_titulo_seccion(doc, "Referencias Bibliográficas")
    refs = [
        "[COMPLETAR: Cita completa del paper asignado al Grupo 3 (Autores, Año, Título, Publicación, Enlace)].",
        "Aeberhard, S., Coomans, D., & de Vel, O. (1994). Comparative analysis of statistical pattern recognition methods in high dimensional settings. Pattern Recognition, 27(8), 1065–1077. (Dataset Wine en scikit-learn).",
        "McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv:1802.03426. (Librería umap-learn 0.6.0).",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830. (Versión 1.9.1).",
        "Harris, C. R., et al. (2020). NumPy · McKinney, W. (2010). Pandas · Hunter, J. D. (2007). Matplotlib · Waskom, M. (2021). Seaborn.",
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.8)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(r)
        run.font.size = Pt(10)

    doc.save(ruta_salida)


# ==============================================================================
# UTILIDADES PARA POWERPOINT (.pptx) — GRUPO 3 (11 DIAPOSITIVAS)
# ==============================================================================

AZUL_OSCURO = PptRGB(0x0F, 0x17, 0x2A)
AZUL_PRIMARIO = PptRGB(0x1E, 0x3A, 0x8A)
AZUL_CLARO = PptRGB(0xDB, 0xEA, 0xFE)
VERDE_OSCURO = PptRGB(0x06, 0x5F, 0x46)
VERDE_CLARO = PptRGB(0xD1, 0xFA, 0xE5)
GRIS_TEXTO = PptRGB(0x33, 0x41, 0x55)
BLANCO = PptRGB(0xFF, 0xFF, 0xFF)
FONDO_SUAVE = PptRGB(0xF8, 0xFA, 0xFC)


def _nuevo_slide_limpio(prs: Presentation, titulo: str, subtitulo_tag: str = ""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, PptInches(0), PptInches(0), PptInches(13.333), PptInches(1.1)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = AZUL_OSCURO
    header.line.fill.background()

    tb = slide.shapes.add_textbox(PptInches(0.6), PptInches(0.2), PptInches(9.8), PptInches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = titulo
    p.font.size = PptPt(24)
    p.font.bold = True
    p.font.color.rgb = BLANCO

    if subtitulo_tag:
        tag = slide.shapes.add_textbox(PptInches(10.2), PptInches(0.3), PptInches(2.7), PptInches(0.45))
        ptf = tag.text_frame
        pp = ptf.paragraphs[0]
        pp.alignment = PP_ALIGN.RIGHT
        pp.text = subtitulo_tag
        pp.font.size = PptPt(11)
        pp.font.bold = True
        pp.font.color.rgb = PptRGB(0x93, 0xC5, 0xFD)

    return slide


def _agregar_caja_texto(slide, left, top, width, height, items: list[tuple[str, str]], font_size=16):
    tb = slide.shapes.add_textbox(PptInches(left), PptInches(top), PptInches(width), PptInches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, (negrita, texto) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = PptPt(10)
        if negrita:
            r0 = p.add_run()
            r0.text = negrita
            r0.font.bold = True
            r0.font.size = PptPt(font_size)
            r0.font.color.rgb = AZUL_PRIMARIO
        r1 = p.add_run()
        r1.text = texto
        r1.font.size = PptPt(font_size)
        r1.font.color.rgb = GRIS_TEXTO
    return tb


def _agregar_tarjeta(slide, left, top, width, height, titulo: str, cuerpo: str, bg_color, title_color):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(left), PptInches(top), PptInches(width), PptInches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = title_color
    shape.line.width = PptPt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = PptInches(0.25)
    tf.margin_right = PptInches(0.25)
    tf.margin_top = PptInches(0.2)

    p0 = tf.paragraphs[0]
    p0.text = titulo
    p0.font.size = PptPt(16)
    p0.font.bold = True
    p0.font.color.rgb = title_color
    p0.space_after = PptPt(6)

    p1 = tf.add_paragraph()
    p1.text = cuerpo
    p1.font.size = PptPt(14)
    p1.font.color.rgb = GRIS_TEXTO


def generar_presentacion_pptx(ruta_salida: Path) -> None:
    prs = Presentation()
    prs.slide_width = PptInches(13.333)
    prs.slide_height = PptInches(7.5)

    # 1. PORTADA
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptInches(0), PptInches(0), PptInches(13.333), PptInches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = AZUL_OSCURO
    bg.line.fill.background()

    tb_p = s1.shapes.add_textbox(PptInches(1.0), PptInches(1.2), PptInches(11.3), PptInches(2.8))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p_m = tf_p.paragraphs[0]
    p_m.text = "SIS-351 MACHINE LEARNING · DEFENSA 3ER PARCIAL"
    p_m.font.size = PptPt(14)
    p_m.font.bold = True
    p_m.font.color.rgb = PptRGB(0x60, 0xA5, 0xFA)
    p_m.space_after = PptPt(14)

    p_t = tf_p.add_paragraph()
    p_t.text = "Autoencoder, UMAP y Clustering"
    p_t.font.size = PptPt(38)
    p_t.font.bold = True
    p_t.font.color.rgb = BLANCO
    p_t.space_after = PptPt(10)

    p_s = tf_p.add_paragraph()
    p_s.text = "¿Cómo influye la representación en los patrones que vemos?\nPaper: [COMPLETAR Título, Autores, Año]"
    p_s.font.size = PptPt(19)
    p_s.font.color.rgb = PptRGB(0xCB, 0xD5, 0xE1)

    box = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(1.0), PptInches(4.5), PptInches(11.3), PptInches(2.1)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = PptRGB(0x1E, 0x29, 0x3B)
    box.line.color.rgb = PptRGB(0x3B, 0x82, 0xF6)
    btf = box.text_frame
    btf.word_wrap = True
    btf.margin_left = PptInches(0.35)
    btf.margin_top = PptInches(0.25)
    bp = btf.paragraphs[0]
    bp.text = (
        "Grupo: Grupo 3\n"
        "Integrantes: [Completar Nombre 1] · [Completar Nombre 2] · [Completar Nombre 3]\n"
        "Docente: [Completar Nombre del Docente]   |   Fecha: [Completar Fecha]"
    )
    bp.font.size = PptPt(16)
    bp.font.color.rgb = BLANCO

    # 2. PROBLEMA
    s2 = _nuevo_slide_limpio(prs, "1. El Problema: Alta Dimensionalidad y Clustering", "Contexto")
    _agregar_tarjeta(
        s2, 0.7, 1.5, 5.8, 5.2,
        "Maldición de la Dimensionalidad",
        "• En espacios originales con muchas variables y distintas escalas, las distancias euclidianas pierden poder discriminativo.\n\n"
        "• Algoritmos como K-means sufren si no se escalan o comprimen las variables previamente.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_tarjeta(
        s2, 6.8, 1.5, 5.8, 5.2,
        "Problema específico del Paper",
        "• [COMPLETAR: dominio, datos y motivación planteada por los autores del paper del Grupo 3].\n\n"
        "• Pregunta guía: ¿Cómo influye la representación en los patrones que vemos?",
        FONDO_SUAVE, AZUL_OSCURO,
    )

    # 3. CONTRIBUCIÓN Y AUTOENCODER DEL PAPER
    s3 = _nuevo_slide_limpio(prs, "2. Contribución y Autoencoder del Paper", "Fundamentos")
    _agregar_tarjeta(
        s3, 0.7, 1.5, 5.8, 5.2,
        "El Autoencoder ('Reloj de Arena Digital')",
        "• Red neuronal no supervisada con Encoder + Bottleneck (espacio latente) + Decoder.\n\n"
        "• Comprime la entrada capturando relaciones no lineales minimizando el error de reconstrucción.\n\n"
        "• Arquitectura específica del paper: [COMPLETAR].",
        VERDE_CLARO, VERDE_OSCURO,
    )
    _agregar_tarjeta(
        s3, 6.8, 1.5, 5.8, 5.2,
        "Contribución del Paper",
        "• [COMPLETAR: método/protocolo exacto del paper combinando Autoencoder, UMAP y clustering].\n\n"
        "• Nota: En nuestra práctica explicamos el autoencoder sin necesidad de entrenarlo.",
        FONDO_SUAVE, AZUL_OSCURO,
    )

    # 4. PCA vs UMAP + K-MEANS
    s4 = _nuevo_slide_limpio(prs, "3. Representaciones 2D: PCA vs. UMAP", "Métodos")
    _agregar_tarjeta(
        s4, 0.7, 1.5, 5.7, 5.2,
        "PCA 2D (Proyección Lineal)",
        "• Busca combinaciones lineales ortogonales que maximizan la varianza global.\n\n"
        "• Rápido, determinista y altamente interpretable.\n\n"
        "• Puede mezclar estructuras no lineales al proyectar a 2D.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_tarjeta(
        s4, 6.9, 1.5, 5.7, 5.2,
        "UMAP 2D (Proyección No Lineal)",
        "• Basado en topología algebraica y grafos de vecindad.\n\n"
        "• Parámetros clave: n_neighbors=15 (balance local/global) y min_dist=0.1 (compacidad).\n\n"
        "• Separa fuertemente vecindades locales antes de aplicar K-means.",
        VERDE_CLARO, VERDE_OSCURO,
    )

    # 5. CONEXIÓN CON SIS-351
    s5 = _nuevo_slide_limpio(prs, "4. Conexión con SIS-351 Machine Learning", "Materia")
    _agregar_caja_texto(
        s5, 0.8, 1.6, 11.7, 5.2,
        [
            ("• Aprendizaje No Supervisado (Tema 03): ", "Uso de PCA, UMAP y K-means para descubrir patrones sin etiquetas previas."),
            ("• Escalamiento obligatorio: ", "StandardScaler evita que variables de mayor magnitud dominen las distancias."),
            ("• Deep Learning (Tema 05): ", "Autoencoders como compresión no lineal frente a métodos lineales como PCA."),
            ("• Evaluación interna sin etiquetas: ", "Uso de inercia (codo) y Silhouette Score para justificar k y medir compacidad."),
        ],
        font_size=18,
    )

    # 6. RESULTADOS PUBLICADOS EN EL PAPER
    s6 = _nuevo_slide_limpio(prs, "5. Resultados Publicados en el Paper", "NO PROPIOS")
    _agregar_tarjeta(
        s6, 0.8, 1.5, 11.7, 1.2,
        "SEPARACIÓN OBLIGATORIA: Resultados externos publicados en el paper",
        "Los datos de esta diapositiva corresponden al artículo del Grupo 3, no al experimento propio en Wine.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_caja_texto(
        s6, 0.8, 3.1, 11.7, 3.8,
        [
            ("• Datasets del paper: ", "[COMPLETAR]"),
            ("• Métodos comparados: ", "[COMPLETAR]"),
            ("• Métricas y hallazgos publicados: ", "[COMPLETAR]"),
        ],
        font_size=18,
    )

    # 7. NUESTRA PRÁCTICA EN WINE
    s7 = _nuevo_slide_limpio(prs, "6. Nuestra Práctica: Protocolo en Wine", "Diseño Propio")
    _agregar_caja_texto(
        s7, 0.8, 1.5, 6.2, 5.4,
        [
            ("• Dataset: ", "Wine (scikit-learn), 178 muestras, 13 variables continuas."),
            ("• Preprocesamiento: ", "StandardScaler (sin usar etiquetas)."),
            ("• Elección de k=3: ", "Codo en inercia (1277.93) y máximo Silhouette (0.2849) en k=2..6."),
            ("• Semilla y parámetros: ", "random_state=42, K-means (n_init=20), UMAP (n_neighbors=15, min_dist=0.1)."),
        ],
        font_size=16,
    )
    ruta_k = RESULTADOS_DIR / "seleccion_k.png"
    if ruta_k.exists():
        s7.shapes.add_picture(str(ruta_k), PptInches(7.1), PptInches(2.0), width=PptInches(5.8))

    # 8. RESULTADOS PROPIOS: PCA vs UMAP
    s8 = _nuevo_slide_limpio(prs, "7. Resultados Propios: Clusters y Silhouette", "RESULTADOS DEL GRUPO")
    tbl_shape = s8.shapes.add_table(3, 6, PptInches(0.6), PptInches(1.3), PptInches(12.1), PptInches(1.4))
    tbl = tbl_shape.table
    headers = ["Representación 2D", "k", "Silhouette Score", "Inercia 2D", "ARI (Comp. Externa)", "NMI (Comp. Externa)"]
    data = [
        ["PCA 2D (Lineal)", "3", "0.5611", "259.5094", "0.8951", "0.8821"],
        ["UMAP 2D (No lineal)", "3", "0.7111", "202.2043", "0.8025", "0.7955"],
    ]
    for c_i, h in enumerate(headers):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = AZUL_PRIMARIO
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = PptPt(12)
        p.font.color.rgb = BLANCO
    for r_i, row_data in enumerate(data, start=1):
        for c_i, val in enumerate(row_data):
            cell = tbl.cell(r_i, c_i)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER if c_i > 0 else PP_ALIGN.LEFT
            p.font.size = PptPt(12)
            if r_i == 2 and c_i == 2:
                p.font.bold = True

    ruta_clusters = RESULTADOS_DIR / "clusters_pca_umap.png"
    if ruta_clusters.exists():
        s8.shapes.add_picture(str(ruta_clusters), PptInches(1.3), PptInches(2.9), width=PptInches(10.7))

    # 9. INTERPRETACIÓN CRÍTICA
    s9 = _nuevo_slide_limpio(prs, "8. Interpretación Crítica de las Visualizaciones", "Análisis")
    _agregar_tarjeta(
        s9, 0.7, 1.5, 5.8, 5.2,
        "¿Por qué UMAP logra mayor Silhouette (0.7111)?",
        "• UMAP preserva vecindades locales formando islas compactas en 2D.\n\n"
        "• PCA solo retiene 55.41% de varianza (PC1 36.2%, PC2 19.21%) en ejes lineales, dejando grupos más cercanos (Silhouette = 0.5611).",
        VERDE_CLARO, VERDE_OSCURO,
    )
    _agregar_tarjeta(
        s9, 6.8, 1.5, 5.8, 5.2,
        "Cuidado: Compacidad ≠ Fidelidad Externa",
        "• Comparación externa declarada (post-hoc): PCA obtuvo ARI = 0.8951 frente a ARI = 0.8025 en UMAP.\n\n"
        "• Un Silhouette alto en 2D refleja la geometría de la proyección, no garantiza clusters reales perfectos.",
        FONDO_SUAVE, AZUL_OSCURO,
    )

    # 10. LÍMITES Y CRÍTICA
    s10 = _nuevo_slide_limpio(prs, "9. Límites y Crítica Metodológica", "Visión Crítica")
    _agregar_caja_texto(
        s10, 0.8, 1.6, 11.7, 5.2,
        [
            ("• Sensibilidad de UMAP: ", "Cambiar n_neighbors, min_dist o random_state altera la separación visual."),
            ("• Supuestos de K-means: ", "Asume clusters esféricos; sufre si UMAP produce formas alargadas o no convexas."),
            ("• Distorsión 2D: ", "Comprimir 13 dimensiones a 2 siempre sacrifica información geométrica."),
            ("• Límites del paper: ", "[COMPLETAR: costos o supuestos críticos reportados en el paper]."),
        ],
        font_size=17,
    )

    # 11. CONCLUSIONES Y REFERENCIAS
    s11 = _nuevo_slide_limpio(prs, "10. Conclusiones y Referencias", "Cierre")
    _agregar_tarjeta(
        s11, 0.8, 1.4, 11.7, 1.9,
        "Respuesta a la Pregunta Guía: ¿Cómo influye la representación en los patrones que vemos?",
        "La representación define qué relaciones (lineales globales en PCA vs. vecindades locales no lineales en UMAP/Autoencoders) se amplifican, cambiando tanto la geometría visual como el desempeño de K-means.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_caja_texto(
        s11, 0.8, 3.6, 11.7, 3.4,
        [
            ("• Paper: ", "[COMPLETAR cita completa del paper del Grupo 3]."),
            ("• Dataset: ", "Wine Dataset (Aeberhard et al., 1994 · scikit-learn)."),
            ("• Librerías: ", "scikit-learn 1.9.1 · umap-learn 0.6.0 · NumPy 2.5.5 · Pandas 3.1.1 · Matplotlib · Seaborn."),
            ("• Reproducibilidad: ", "random_state=42 en src/experimento.py y notebooks/01_practica_grupo3_umap.ipynb."),
        ],
        font_size=14,
    )

    prs.save(ruta_salida)


def main() -> None:
    ENTREGABLES_DIR.mkdir(parents=True, exist_ok=True)
    ruta_docx = ENTREGABLES_DIR / "Informe_Grupo3_Autoencoder_UMAP.docx"
    ruta_pptx = ENTREGABLES_DIR / "Presentacion_Grupo3_Autoencoder_UMAP.pptx"

    generar_informe_word(ruta_docx)
    generar_presentacion_pptx(ruta_pptx)

    print(f"Word generado: {ruta_docx}")
    print(f"PowerPoint generado: {ruta_pptx}")


if __name__ == "__main__":
    main()
