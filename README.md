# SIS-351 Machine Learning — Práctica Grupo 3: Autoencoder, UMAP y Clustering

Comparación experimental reproducible de representaciones en 2D (**PCA** vs. **UMAP**) y agrupamiento no supervisado (**K-means** con el mismo $k=3$) sobre el dataset **Wine**, conectando el análisis con la arquitectura de **Autoencoders** en aprendizaje no supervisado.

---

## 1. Paper de Referencia
* **Título:** `[COMPLETAR]`
* **Autores:** `[COMPLETAR]`
* **Año / Publicación:** `[COMPLETAR]`
* **Enlace / Versión:** `[COMPLETAR]`

---

## 2. Dataset y Reglas de Reproducibilidad
* **Dataset:** `load_wine()` de `scikit-learn` (178 muestras, 13 variables fisicoquímicas continuas).
* **Preprocesamiento:** Escalamiento estandarizado con `StandardScaler` (media 0, desviación estándar 1).
* **Semilla Global:** `random_state = 42` (fijada en `PYTHONHASHSEED`, `random`, `numpy`, `PCA`, `UMAP` y `KMeans`).
* **Hiperparámetros documentados:**
  * `PCA`: `n_components=2`, `random_state=42` (varianza explicada: PC1 36.2%, PC2 19.21%, total 55.41%).
  * `UMAP`: `n_components=2`, `n_neighbors=15`, `min_dist=0.1`, `random_state=42`.
  * `KMeans`: `n_clusters=3`, `n_init=20`, `random_state=42`.
* **Rigor no supervisado:** Las etiquetas reales de Wine **no** se utilizan para escalar, proyectar ni elegir $k$. La elección de $k=3$ se justifica mediante el método del codo y el máximo Silhouette Score en el rango $k=2..6$ sobre el espacio escalado (`0.2849`). Los índices ARI y NMI se reportan únicamente como comparación externa post-hoc declarada.

---

## 3. Estructura del Proyecto

```text
proyecto_3er_parcial/
├── CONTEXTO.md                          # Guía y alcance del proyecto (Grupo 3)
├── BORRADOR_7_PREGUNTAS.md              # Respuestas a las 7 preguntas (campos del paper con [COMPLETAR])
├── README.md                            # Este archivo (instrucciones de reproducción)
├── requirements.txt                     # Dependencias con versiones fijas
├── notebooks/
│   └── 01_practica_grupo3_umap.ipynb    # Notebook ejecutable en Local y Google Colab
├── src/
│   ├── experimento.py                   # Script modular reproducible que exporta evidencias
│   └── generar_entregables.py           # Generador del informe (.docx) y diapositivas (.pptx)
├── entregables/
│   ├── Informe_Grupo3_Autoencoder_UMAP.docx
│   └── Presentacion_Grupo3_Autoencoder_UMAP.pptx
└── resultados/                          # Evidencias generadas automáticamente
    ├── seleccion_k.csv
    ├── seleccion_k.png
    ├── tabla_metricas_comparativas.csv
    ├── resumen_dataset.csv
    ├── entorno.txt
    ├── clusters_pca_umap.png
    └── comparacion_silhouette.png
```

---

## 4. Cómo Ejecutar y Reproducir

### Opción A: Ejecución en Local
1. Crear y activar un entorno virtual e instalar las dependencias:
   ```bash
   python -m venv .venv
   # En Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # En Linux/macOS:
   # source .venv/bin/activate

   pip install -r requirements.txt
   ```
2. Ejecutar el script del experimento para regenerar tablas y gráficos en `/resultados`:
   ```bash
   python src/experimento.py
   ```
3. O abrir el notebook `notebooks/01_practica_grupo3_umap.ipynb` seleccionando el kernel `.venv`.

### Opción B: Ejecución en Google Colab
1. Abrir `notebooks/01_practica_grupo3_umap.ipynb` en [Google Colab](https://colab.research.google.com/).
2. Ejecutar todas las celdas en orden; la primera celda instala `umap-learn==0.6.0` si no está presente.

---

## 5. Resultados Obtenidos (Wine, n = 178, k = 3)

| Representación 2D | k | Silhouette Score | Inercia 2D | ARI (Comp. Externa) | NMI (Comp. Externa) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **PCA 2D (Lineal)** | 3 | 0.5611 | 259.5094 | 0.8951 | 0.8821 |
| **UMAP 2D (No lineal)** | 3 | **0.7111** | 202.2043 | 0.8025 | 0.7955 |

*Ver detalle completo y gráficas en [`resultados/`](resultados/).*

---

## 6. Declaración de Uso de IA (Trazabilidad)
En cumplimiento con las buenas prácticas de SIS-351:
* **Herramienta utilizada:** Antigravity (asistente de IA para ingeniería de software).
* **Apoyo recibido:**
  1. Actualización de `CONTEXTO.md`, `BORRADOR_7_PREGUNTAS.md` y `README.md` para la práctica del Grupo 3 (dejando `[COMPLETAR]` en los datos del paper aún no definidos).
  2. Implementación de `src/experimento.py`, `notebooks/01_practica_grupo3_umap.ipynb` y `src/generar_entregables.py` (Word y PowerPoint).
* **Verificación humana:** Todo el código, el escalado, la selección de $k$, las proyecciones PCA/UMAP y las métricas exportadas en `resultados/` fueron ejecutados y verificados en el entorno `.venv` local (Python 3.14.0, `scikit-learn 1.9.1`, `umap-learn 0.6.0`).
