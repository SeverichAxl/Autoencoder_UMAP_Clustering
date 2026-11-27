"""
Genera los entregables oficiales definitivos (Word .docx y PowerPoint .pptx)
para el Grupo 3 — SIS-351 Machine Learning, integrando los resultados empíricos
del experimento en Wine y el paper de referencia analizado:
  "Parametric UMAP Embeddings for Representation and Semisupervised Learning"
  (Tim Sainburg, Leland McInnes & Timothy Q. Gentner, Neural Computation, 2021).

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
    r_u = p_univ.add_run("[UNIVERSIDAD CATÓLICA BOLIVIANA 'SAN PABLO']")
    r_u.bold = True
    r_u.font.size = Pt(13)
    r_u.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    p_mat = doc.add_paragraph()
    p_mat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_m = p_mat.add_run("SIS-351 Machine Learning — Evaluación 3er Parcial (Gestión 2026)")
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
        "Análisis del paper 'Parametric UMAP Embeddings for Representation and Semisupervised Learning'\n"
        "(Sainburg et al., 2021) y evidencia experimental reproducible sobre el dataset Wine"
    )
    r_s.italic = True
    r_s.font.size = Pt(11)
    r_s.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    for _ in range(4):
        doc.add_paragraph()

    datos_portada = [
        ("Grupo:", "Grupo 3 (Representaciones No Supervisadas)"),
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
        "En el aprendizaje no supervisado, descubrir estructuras latentes, patrones intrínsecos y agrupamientos "
        "en conjuntos de datos sin etiquetas depende críticamente del espacio en el que se representan las observaciones. "
        "En esta investigación analizamos cómo las técnicas de reducción de dimensionalidad lineal (PCA) y no lineal (UMAP), "
        "en conjunto con arquitecturas de redes neuronales profundas (Autoencoders), transforman la geometría de los datos "
        "y condicionan directamente los resultados de algoritmos de agrupamiento como K-means.",
    )
    _agregar_vineta(doc, "Título del paper: ", "Parametric UMAP Embeddings for Representation and Semisupervised Learning.")
    _agregar_vineta(doc, "Autores: ", "Tim Sainburg (UC San Diego), Leland McInnes (Tutte Institute) y Timothy Q. Gentner (UC San Diego).")
    _agregar_vineta(doc, "Año y publicación: ", "2021, publicado en la revista Neural Computation (MIT Press), Vol. 33, Núm. 11, págs. 2881–2907.")
    _agregar_vineta(doc, "Enlaces oficiales: ", "DOI: https://doi.org/10.1162/neco_a_01434 · arXiv: https://arxiv.org/abs/2009.12981.")
    _agregar_vineta(doc, "Versión de software: ", "Parametric UMAP integrado oficialmente en el paquete Python umap-learn (v0.6.0).")
    _agregar_parrafo(
        doc,
        "Comprender los fundamentos del Autoencoder y Parametric UMAP propuestos en el paper (sin necesidad de "
        "entrenar la red neuronal desde cero) y comparar experimentalmente dos representaciones en 2D (PCA lineal vs. "
        "UMAP no lineal) bajo K-means con el mismo k sobre el dataset Wine, respondiendo a la pregunta guía: "
        "¿Cómo influye la representación en los patrones que vemos?",
        negrita_prefijo="Objetivo de la práctica: ",
    )

    # --------------------------------------------------------------------------
    # 2. PROBLEMA Y CONTRIBUCIÓN
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "2. Problema Abordado y Contribución Central")
    _agregar_subtitulo(doc, "2.1 El problema de la reducción de dimensionalidad no lineal")
    _agregar_parrafo(
        doc,
        "Los métodos tradicionales de reducción de dimensionalidad no paramétricos —como t-SNE y UMAP estándar— "
        "han demostrado una notable capacidad para proyectar datos complejos de alta dimensión hacia variedades 2D o 3D, "
        "preservando con alta fidelidad las relaciones topológicas de vecindad local. Sin embargo, adolecen de una "
        "limitación teórica y práctica fundamental: al ser no paramétricos, optimizan de forma directa las coordenadas "
        "de salida de los puntos de entrenamiento sin aprender una función matemática continua f(x).",
    )
    _agregar_parrafo(
        doc,
        "Esto genera dos grandes inconvenientes: (1) no pueden proyectar nuevos datos de prueba (out-of-sample) de forma "
        "eficiente, requiriendo recomputar costosas aproximaciones del grafo; y (2) carecen de una función inversa analítica "
        "que permita reconstruir los datos originales a partir de sus coordenadas en el espacio latente. Por otro lado, los "
        "Autoencoders neuronales clásicos aprenden funciones paramétricas continuas mediante un codificador y un decodificador, "
        "pero su función de pérdida habitual (error cuadrático medio de reconstrucción) no garantiza la preservación de la "
        "estructura topológica de vecindad, produciendo espacios latentes a menudo desarticulados.",
    )

    _agregar_subtitulo(doc, "2.2 Contribución de Parametric UMAP y regularización de Autoencoders")
    _agregar_parrafo(
        doc,
        "Sainburg, McInnes y Gentner (2021) resuelven esta dicotomía introduciendo Parametric UMAP. La contribución se articula en tres pilares:",
    )
    _agregar_vineta(
        doc,
        "Parametrización mediante Redes Profundas: ",
        "Reemplazan la optimización directa de coordenadas por el entrenamiento de un Codificador (Encoder) que predice "
        "el embedding minimizando la pérdida de entropía cruzada difusa de UMAP mediante descenso de gradiente estocástico "
        "(mini-batch SGD) y muestreo negativo (negative sampling).",
    )
    _agregar_vineta(
        doc,
        "Autoencoder Regularizado por UMAP (Autoencoder Regularization): ",
        "Extienden el codificador acoplándolo a un Decodificador (Decoder) que reconstruye la entrada original x a partir de z. "
        "La función de pérdida combinada L_total = L_UMAP + λ L_recon obliga al espacio latente del Autoencoder a respetar la "
        "variedad topológica local de UMAP mientras preserva la capacidad de reconstrucción e interpolación continua.",
    )
    _agregar_vineta(
        doc,
        "Inferencia online y aprendizaje semi-supervisado: ",
        "El modelo entrenado permite proyectar nuevos datos hacia el espacio latente órdenes de magnitud más rápido que UMAP "
        "no paramétrico, pudiendo combinarse además con una cabeza clasificadora para aprendizaje semi-supervisado.",
    )

    # --------------------------------------------------------------------------
    # 3. FUNDAMENTOS Y CONEXIÓN CON SIS-351
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "3. Fundamentos Teóricos y Conexión con SIS-351")
    _agregar_subtitulo(doc, "3.1 El Autoencoder ('El Reloj de Arena Digital') en el Paper")
    _agregar_parrafo(
        doc,
        "En la unidad de Deep Learning de SIS-351 (Tema 05) se estudió el Autoencoder como una arquitectura no supervisada "
        "compuesta por dos componentes acoplados: un Codificador f_θ que comprime la entrada x ∈ R^D hacia un cuello de "
        "botella latente z ∈ R^d (d ≪ D), y un Decodificador g_ϕ que reconstruye x̂ = g_ϕ(z) ∈ R^D minimizando un error de "
        "reconstrucción L_recon(x, x̂) (MSE).",
    )
    _agregar_parrafo(
        doc,
        "En el paper de Sainburg et al., el Autoencoder se enriquece introduciendo la pérdida topológica de UMAP en el espacio latente: "
        "L_UMAP evalúa las probabilidades difusas de aristas p_ij en el espacio de alta dimensión frente a q_ij en el espacio latente z. "
        "Al optimizar conjuntamente ambas pérdidas con Adam, el 'cuello de botella' neuronal actúa como un filtro topológico que desenreda "
        "variedades no lineales complejas, permitiendo reconstrucciones superiores a las de un PCA lineal o un Autoencoder estándar.",
    )

    _agregar_subtitulo(doc, "3.2 Conexión con Aprendizaje No Supervisado en SIS-351")
    _agregar_vineta(
        doc,
        "PCA (Tema 03): ",
        "Técnica lineal determinista que busca proyecciones ortogonales de máxima varianza global. Sirve como línea base rápida "
        "y altamente interpretable, pero no puede desenredar variedades no lineales complejas.",
    )
    _agregar_vineta(
        doc,
        "UMAP (Tema 03): ",
        "Método no lineal basado en topología algebraica y geometría riemanniana que preserva vecindades locales y minimiza "
        "la distorsión entre simplex difusos, regulado por n_neighbors (escala de vecindad) y min_dist (compacidad).",
    )
    _agregar_vineta(
        doc,
        "K-means y Silhouette Score (Tema 03): ",
        "K-means agrupa observaciones mediante distancias euclidianas a k centroides, asumiendo clusters convexos y esféricos. "
        "El Silhouette Score (en [-1, 1]) evalúa internamente la calidad del agrupamiento (cohesión intra-cluster frente a separación "
        "inter-cluster) de forma 100% no supervisada.",
    )

    # --------------------------------------------------------------------------
    # 4. EXPERIMENTOS DEL PAPER
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "4. Experimentos Reportados en el Paper")
    _agregar_recuadro(
        doc,
        "SECCIÓN DE RESULTADOS PUBLICADOS EN EL PAPER (SAINBURG ET AL., 2021 — NO DEL GRUPO)",
        "Los datos y comparaciones descritos en esta sección provienen exclusivamente de las evaluaciones "
        "publicadas en Neural Computation (2021) y sirven como marco de referencia externo.",
        color_fondo="EFF6FF",
        color_borde="1D4ED8",
    )
    _agregar_parrafo(
        doc,
        "Los autores evaluaron Parametric UMAP sobre una suite diversa de datasets reales y sintéticos: imágenes estructuradas "
        "(MNIST, Fashion-MNIST, CIFAR-10), datos biomédicos de alta complejidad (transcriptomas unicelulares de retina de ratón de Macosko et al.), "
        "espectrogramas bioacústicos de cantos de aves (Cassin's vireo) y variedades geométricas (Moons, 3D Buffalo).",
    )
    _agregar_parrafo(
        doc,
        "Compararon su propuesta frente a líneas base no paramétricas (UMAP estándar, t-SNE estándar, PHATE) y paramétricas "
        "(Parametric t-SNE, SCVIS, IVIS, TriMap, Autoencoders estándar, VAEs y PCA). Los resultados clave reportados demostraron que: "
        "(1) Parametric UMAP alcanza un Silhouette Score y preservación de vecindad local (Trustworthiness) idénticos a UMAP estándar, "
        "pero infiriendo sobre nuevos datos órdenes de magnitud más rápido; y (2) el Autoencoder regularizado con pérdida UMAP supera "
        "a los Autoencoders convencionales y a PCA en error cuadrático medio de reconstrucción (MSE), permitiendo interpolaciones suaves en el espacio latente.",
    )

    # --------------------------------------------------------------------------
    # 5. PRÁCTICA DEL GRUPO
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "5. Práctica Experimental del Grupo")
    _agregar_recuadro(
        doc,
        "RESULTADOS OBTENIDOS POR EL GRUPO (EVIDENCIA REPRODUCIBLE PROPIA)",
        "Experimento ejecutado por el grupo sobre Wine (scikit-learn) con StandardScaler, semilla fija "
        "random_state=42 y selección de k 100% no supervisada (sin usar etiquetas en el ajuste).",
        color_fondo="ECFDF5",
        color_borde="047857",
    )

    _agregar_subtitulo(doc, "5.1 Dataset, preprocesamiento y justificación de k")
    _agregar_parrafo(
        doc,
        "Trabajamos con el dataset Wine de scikit-learn (178 muestras, 13 variables fisicoquímicas continuas). "
        "Aplicamos StandardScaler para neutralizar las diferencias de escala (p. ej., 'proline' con valores ~1000 frente a "
        "'nonflavanoid_phenols' < 1.0). Para seleccionar k de manera rigurosa y no supervisada (sin consultar etiquetas), "
        "evaluamos k ∈ {2, 3, 4, 5, 6} en el espacio escalado: k = 3 presentó el codo más pronunciado en inercia (1277.93) "
        "y el valor máximo de Silhouette Score (0.2849).",
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
        "Los resultados empíricos ofrecen una respuesta directa a la pregunta guía: la representación actúa como una "
        "lente geométrica que altera sustancialmente la estructura visible. En PCA 2D (que retiene el 55.41% de la varianza "
        "global: PC1 36.2%, PC2 19.21%), la proyección lineal distribuye las observaciones en un espacio continuo donde "
        "las fronteras entre grupos son cercanas y algo difusas, alcanzando un Silhouette Score de 0.5611. En contraste, "
        "UMAP 2D (n_neighbors=15, min_dist=0.1) contrae las vecindades locales en islas aisladas y compactas, elevando "
        "el Silhouette Score a 0.7111 y reduciendo la inercia interna a 202.20.",
    )
    _agregar_parrafo(
        doc,
        "Sin embargo, la comparación externa post-hoc contra las etiquetas de los tres cultivares de Wine revela una paradoja "
        "didáctica fundamental: PCA 2D obtuvo mayor concordancia externa (ARI = 0.8951, NMI = 0.8821) que UMAP 2D (ARI = 0.8025, NMI = 0.7955). "
        "Esto demuestra que un Silhouette Score elevado en un espacio no lineal comprimido refleja la densidad artificial de la "
        "proyección topológica, pero no garantiza mayor fidelidad a las clases reales subyacentes. Tal como concluyen Sainburg et al., "
        "las proyecciones no lineales deben interpretarse con cautela antes de tomar decisiones de agrupamiento.",
        negrita_prefijo="Lección crítica (Compacidad vs. fidelidad externa): ",
    )
    _agregar_vineta(
        doc,
        "Sensibilidad a hiperparámetros: ",
        "Tanto UMAP como Parametric UMAP dependen fuertemente de n_neighbors, min_dist y la semilla aleatoria; valores distintos "
        "pueden separar visualmente grupos continuos o fusionar clusters distintos.",
    )
    _agregar_vineta(
        doc,
        "Incompatibilidad de supuestos con K-means: ",
        "K-means asume clusters de dispersión esférica e isotrópica; si una variedad topológica genera grupos curvados o elongados, "
        "K-means puede fracturar erróneamente un mismo cluster natural.",
    )

    # --------------------------------------------------------------------------
    # 7. REPRODUCIBILIDAD Y USO DE IA
    # --------------------------------------------------------------------------
    _agregar_titulo_seccion(doc, "7. Reproducibilidad y Declaración de Uso de IA")
    _agregar_parrafo(
        doc,
        "El código completo de la práctica es reproducible en local y Google Colab mediante src/experimento.py y "
        "notebooks/01_practica_grupo3_umap.ipynb. Entorno registrado: Windows 10, Python 3.14.0, scikit-learn 1.9.1, "
        "umap-learn 0.6.0, NumPy 2.5.5, Pandas 3.1.1, con semilla fija random_state = 42 en PCA, UMAP y K-means (n_init=20).",
    )
    _agregar_parrafo(
        doc,
        "Se utilizó el asistente de IA Antigravity como apoyo para estructurar el proyecto, implementar los scripts reproducibles "
        "y redactar este borrador inicial a partir del análisis del PDF del paper de Sainburg et al. (2021). Todo el código y "
        "las métricas numéricas fueron ejecutados y verificados en el entorno de desarrollo local.",
        negrita_prefijo="Declaración de uso de IA: ",
    )

    # --------------------------------------------------------------------------
    # REFERENCIAS
    # --------------------------------------------------------------------------
    doc.add_page_break()
    _agregar_titulo_seccion(doc, "Referencias Bibliográficas")
    refs = [
        "Sainburg, T., McInnes, L., & Gentner, T. Q. (2021). Parametric UMAP Embeddings for Representation and Semisupervised Learning. Neural Computation, 33(11), 2881–2907. https://doi.org/10.1162/neco_a_01434 (arXiv:2009.12981).",
        "McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv:1802.03426.",
        "Aeberhard, S., Coomans, D., & de Vel, O. (1994). Comparative analysis of statistical pattern recognition methods in high dimensional settings. Pattern Recognition, 27(8), 1065–1077. (Dataset Wine en scikit-learn).",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
        "Hinton, G. E., & Salakhutdinov, R. R. (2006). Reducing the dimensionality of data with neural networks. Science, 313(5786), 504–507. (Fundamento de Autoencoders).",
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
# UTILIDADES PARA POWERPOINT (.pptx) — GRUPO 3 (11 DIAPOSITIVAS COMPLETAS)
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
    p_s.text = "¿Cómo influye la representación en los patrones que vemos?\nPaper: Parametric UMAP (Sainburg, McInnes & Gentner, Neural Computation 2021)"
    p_s.font.size = PptPt(18)
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
        "Grupo: Grupo 3 (Representaciones No Supervisadas)\n"
        "Integrantes: [Completar Nombre 1] · [Completar Nombre 2] · [Completar Nombre 3]\n"
        "Docente: [Completar Nombre del Docente]   |   Gestión 2026"
    )
    bp.font.size = PptPt(16)
    bp.font.color.rgb = BLANCO

    # 2. PROBLEMA
    s2 = _nuevo_slide_limpio(prs, "1. El Problema: Limitaciones en Dimensionalidad", "Contexto")
    _agregar_tarjeta(
        s2, 0.7, 1.5, 5.8, 5.2,
        "Métodos No Paramétricos (t-SNE / UMAP)",
        "• Capturan topología no lineal y vecindades locales con alta fidelidad.\n\n"
        "• Límite crítico: No aprenden una función f(x); no pueden proyectar nuevos datos de forma eficiente.\n\n"
        "• Carecen de mapeo inverso para reconstruir muestras desde el espacio latente.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_tarjeta(
        s2, 6.8, 1.5, 5.8, 5.2,
        "Autoencoders Tradicionales (AE / VAE)",
        "• Aprenden funciones continuas mediante redes neuronales (Encoder + Decoder).\n\n"
        "• Límite crítico: La pérdida de reconstrucción (MSE) no preserva la topología de vecindad local.\n\n"
        "• Pregunta del paper: ¿Cómo unir UMAP y Autoencoders en una sola arquitectura paramétrica?",
        FONDO_SUAVE, AZUL_OSCURO,
    )

    # 3. CONTRIBUCIÓN: PARAMETRIC UMAP Y AUTOENCODERS
    s3 = _nuevo_slide_limpio(prs, "2. Contribución: Parametric UMAP & Autoencoder", "Paper 2021")
    _agregar_tarjeta(
        s3, 0.7, 1.5, 5.8, 5.2,
        "Codificador Paramétrico (Encoder)",
        "• Red neuronal profunda que predice coordenadas latentes z = f_θ(x).\n\n"
        "• Optimiza directamente la pérdida de entropía cruzada difusa de UMAP con mini-batch SGD y negative sampling.\n\n"
        "• Beneficio: Proyección de nuevos datos órdenes de magnitud más rápida que UMAP clásico.",
        VERDE_CLARO, VERDE_OSCURO,
    )
    _agregar_tarjeta(
        s3, 6.8, 1.5, 5.8, 5.2,
        "Autoencoder Regularizado por UMAP",
        "• Añade un Decodificador g_ϕ(z) que reconstruye la entrada original x̂.\n\n"
        "• Función de pérdida conjunta: L_total = L_UMAP + λ L_recon (MSE).\n\n"
        "• El espacio latente preserva topología mientras permite reconstrucción e interpolación suave.",
        FONDO_SUAVE, AZUL_OSCURO,
    )

    # 4. CÓMO FUNCIONA: COMPARACIÓN DE REPRESENTACIONES
    s4 = _nuevo_slide_limpio(prs, "3. Representaciones 2D: PCA vs. UMAP vs. AE", "Métodos")
    _agregar_tarjeta(
        s4, 0.7, 1.5, 5.7, 5.2,
        "PCA 2D (Lineal Global)",
        "• Ejes ortogonales de máxima varianza global.\n\n"
        "• Determinista, rápido y sin hiperparámetros complejos.\n\n"
        "• Mezcla variedades no lineales en proyecciones de baja dimensión.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_tarjeta(
        s4, 6.9, 1.5, 5.7, 5.2,
        "UMAP 2D (Topología No Lineal)",
        "• Simplex difusos y grafos de vecindad local (n_neighbors=15, min_dist=0.1).\n\n"
        "• Contrae puntos cercanos en agrupaciones densas.\n\n"
        "• En el paper, el Autoencoder aprende esta variedad mediante descenso de gradiente.",
        VERDE_CLARO, VERDE_OSCURO,
    )

    # 5. CONEXIÓN CON SIS-351
    s5 = _nuevo_slide_limpio(prs, "4. Conexión con SIS-351 Machine Learning", "Materia")
    _agregar_caja_texto(
        s5, 0.8, 1.6, 11.7, 5.2,
        [
            ("• Aprendizaje No Supervisado (Tema 03): ", "PCA como reductor lineal de varianza global vs. UMAP como reductor no lineal topológico."),
            ("• Deep Learning (Tema 05): ", "Autoencoder ('Reloj de Arena Digital') como modelo de compresión no lineal con capas ocultas y funciones de activación."),
            ("• Escalamiento previo: ", "Uso obligatorio de StandardScaler para evitar que variables de magnitud dispar sesguen las distancias euclidianas."),
            ("• Clustering y Evaluación Interna: ", "K-means particiona por centroides y el Silhouette Score evalúa la compacidad sin requerir etiquetas."),
        ],
        font_size=17,
    )

    # 6. RESULTADOS PUBLICADOS EN EL PAPER
    s6 = _nuevo_slide_limpio(prs, "5. Resultados Publicados en el Paper", "SAINBURG ET AL. (2021)")
    _agregar_tarjeta(
        s6, 0.8, 1.4, 11.7, 1.2,
        "RESULTADOS EXTERNOS DEL ARTÍCULO CIENTÍFICO (NEURAL COMPUTATION 2021)",
        "Evaluación sobre MNIST, Fashion-MNIST, CIFAR-10, células de retina de ratón y cantos de aves (Cassin's vireo).",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_caja_texto(
        s6, 0.8, 3.0, 11.7, 3.9,
        [
            ("• Preservación y Calidad: ", "Parametric UMAP igualó el Silhouette Score y Trustworthiness de UMAP no paramétrico."),
            ("• Velocidad de Inferencia: ", "Proyectó nuevos datos órdenes de magnitud más rápido que t-SNE y UMAP clásico."),
            ("• Reconstrucción del Autoencoder: ", "El AE regularizado con UMAP superó a PCA y a VAEs en error cuadrático medio (MSE), permitiendo interpolaciones latentes continuas."),
        ],
        font_size=17,
    )

    # 7. NUESTRA PRÁCTICA EN WINE
    s7 = _nuevo_slide_limpio(prs, "6. Nuestra Práctica: Protocolo en Wine", "Diseño Propio")
    _agregar_caja_texto(
        s7, 0.8, 1.5, 6.2, 5.4,
        [
            ("• Dataset: ", "Wine (scikit-learn), 178 muestras, 13 variables fisicoquímicas continuas."),
            ("• Preprocesamiento: ", "StandardScaler estricto (media=0, std=1)."),
            ("• Elección no supervisada de k=3: ", "Codo en inercia (1277.93) y máximo Silhouette Score (0.2849) en k=2..6 sobre el espacio escalado."),
            ("• Semilla fija: ", "random_state=42 en PCA, UMAP (n_neighbors=15, min_dist=0.1) y K-means (n_init=20)."),
        ],
        font_size=16,
    )
    ruta_k = RESULTADOS_DIR / "seleccion_k.png"
    if ruta_k.exists():
        s7.shapes.add_picture(str(ruta_k), PptInches(7.1), PptInches(2.0), width=PptInches(5.8))

    # 8. RESULTADOS PROPIOS: PCA vs UMAP
    s8 = _nuevo_slide_limpio(prs, "7. Resultados Propios: Clusters y Silhouette", "EVIDENCIA DEL GRUPO")
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
        "¿Por qué UMAP eleva el Silhouette a 0.7111?",
        "• UMAP contrae vecindades locales en islas artificialmente aisladas y densas en 2D.\n\n"
        "• PCA retiene el 55.41% de varianza en ejes lineales globales, dejando clusters continuos más cercanos (Silhouette = 0.5611).",
        VERDE_CLARO, VERDE_OSCURO,
    )
    _agregar_tarjeta(
        s9, 6.8, 1.5, 5.8, 5.2,
        "La Paradoja: Compacidad ≠ Fidelidad Externa",
        "• Comparación externa post-hoc: PCA obtuvo mayor concordancia con las clases reales (ARI = 0.8951) frente a UMAP (ARI = 0.8025).\n\n"
        "• Conclusión crítica: Un Silhouette alto en UMAP refleja la compacidad del embedding 2D, no mayor fidelidad semántica.",
        FONDO_SUAVE, AZUL_OSCURO,
    )

    # 10. LÍMITES Y CRÍTICA
    s10 = _nuevo_slide_limpio(prs, "9. Límites y Crítica Metodológica", "Visión Crítica")
    _agregar_caja_texto(
        s10, 0.8, 1.6, 11.7, 5.2,
        [
            ("• Sensibilidad hiperparamétrica: ", "Tanto UMAP como Parametric UMAP varían según n_neighbors, min_dist y la semilla aleatoria."),
            ("• Supuesto de convexidad en K-means: ", "K-means asume centroides esféricos; si UMAP crea formas elongadas o no convexas, K-means puede fracturarlas."),
            ("• Pérdida topológica al proyectar a 2D: ", "Comprimir 13 dimensiones a 2 siempre distorsiona distancias relativas globales."),
            ("• Costo de entrenamiento en Autoencoders: ", "Aprender el mapeo paramétrico exige optimizar miles de pesos con GPU y sintonizar hiperparámetros."),
        ],
        font_size=17,
    )

    # 11. CONCLUSIONES Y REFERENCIAS
    s11 = _nuevo_slide_limpio(prs, "10. Conclusiones y Referencias", "Cierre")
    _agregar_tarjeta(
        s11, 0.8, 1.4, 11.7, 1.9,
        "Respuesta a la Pregunta Guía: ¿Cómo influye la representación en los patrones que vemos?",
        "La representación actúa como un filtro geométrico: PCA amplifica la varianza global lineal manteniendo fidelidad de clases (ARI=0.8951), mientras que UMAP y los Autoencoders topológicos compactan vecindades locales (Silhouette=0.7111), transformando radicalmente los clusters detectados por K-means.",
        AZUL_CLARO, AZUL_PRIMARIO,
    )
    _agregar_caja_texto(
        s11, 0.8, 3.6, 11.7, 3.4,
        [
            ("• Paper analizado: ", "Sainburg, T., McInnes, L., & Gentner, T. Q. (2021). Parametric UMAP Embeddings for Representation and Semisupervised Learning. Neural Computation, 33(11), 2881–2907."),
            ("• Dataset evaluado: ", "Wine Dataset (Aeberhard et al., 1994 · scikit-learn)."),
            ("• Librerías: ", "scikit-learn 1.9.1 · umap-learn 0.6.0 · NumPy 2.5.5 · Pandas 3.1.1 · Matplotlib · Seaborn."),
            ("• Reproducibilidad: ", "Semilla 42 en src/experimento.py y notebooks/01_practica_grupo3_umap.ipynb."),
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

    print(f"Word generado exitosamente: {ruta_docx}")
    print(f"PowerPoint generado exitosamente: {ruta_pptx}")


if __name__ == "__main__":
    main()
