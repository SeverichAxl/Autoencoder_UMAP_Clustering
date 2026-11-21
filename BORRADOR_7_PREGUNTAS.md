# Borrador de las 7 Preguntas Obligatorias sobre el Paper
**Materia:** SIS-351 Machine Learning  
**Grupo:** Grupo 3 — Autoencoder, UMAP y clustering (aprendizaje no supervisado)  
**Pregunta guía:** *¿Cómo influye la representación en los patrones que vemos?*

> [!IMPORTANT]
> Los campos marcados con `[COMPLETAR]` dependen directamente del paper específico asignado al Grupo 3. No se han inventado títulos, autores, años ni resultados publicados.

---

## Pregunta 1: Identidad del Paper
* **Título completo:** `[COMPLETAR]`
* **Autores:** `[COMPLETAR]`
* **Año y Publicación:** `[COMPLETAR]`
* **Enlaces oficiales:** `[COMPLETAR]`
* **Versión / Código de referencia:** `[COMPLETAR]`

---

## Pregunta 2: Problema que aborda el Paper
* **Contexto general del tema:** En aprendizaje no supervisado con datos de alta dimensionalidad ("La Maldición de la Dimensionalidad"), agrupar observaciones directamente en el espacio original mediante distancias euclidianas (como K-means) suele degradarse: las distancias pierden poder discriminativo y las variables ruidosas o correlacionadas ocultan la estructura real.
* **Problema específico planteado en el paper:** `[COMPLETAR: describir el dominio o problema concreto que motivó a los autores del paper]`

---

## Pregunta 3: Contribución principal
* **Contribución del paper:** `[COMPLETAR: describir el método/arquitectura/protocolo exacto propuesto por los autores (p. ej., tipo de Autoencoder, combinación con UMAP y algoritmo de clustering)]`
* **Aporte conceptual clave:** Combinar aprendizaje de representaciones (espacio latente no lineal mediante redes neuronales) con técnicas de reducción de dimensionalidad y agrupamiento para descubrir patrones intrínsecos sin etiquetas previas.

---

## Pregunta 4: Funcionamiento y Fundamentos Teóricos (Conexión con SIS-351)
1. **El Autoencoder ("El Reloj de Arena Digital", Tema 05 de SIS-351):**
   * Arquitectura neuronal no supervisada compuesta por un **Codificador (Encoder)** que comprime la entrada $x \in \mathbb{R}^D$ hacia un espacio latente restringido (*bottleneck*) $z \in \mathbb{R}^d$ ($d \ll D$), y un **Decodificador (Decoder)** que reconstruye $\hat{x}$ minimizando el error de reconstrucción (p. ej., MSE).
   * A diferencia de PCA (proyección lineal ortogonal), el autoencoder utiliza funciones de activación no lineales para capturar variedades (*manifolds*) complejas.
   * **Detalles específicos de la arquitectura en el paper:** `[COMPLETAR: capas, función de pérdida, regularización o variante (CAE, VAE, SAE) usada en el paper]`
2. **Reducción de dimensionalidad 2D: PCA vs. UMAP (Tema 03 de SIS-351):**
   * **PCA (Análisis de Componentes Principales):** Transformación lineal rápida e interpretable que maximiza la varianza explicada y preserva la estructura global.
   * **UMAP (Uniform Manifold Approximation and Projection):** Técnica no lineal basada en topología algebraica y grafos de vecindad (`n_neighbors`, `min_dist`) que equilibra la preservación de la estructura local y la global.
3. **Agrupamiento con K-means y evaluación con Silhouette:**
   * **K-means:** Algoritmo basado en centroides que particiona los datos en $k$ grupos minimizando la inercia (suma de distancias cuadráticas intra-cluster), asumiendo geometrías convexas/esféricas.
   * **Silhouette Score:** Métrica interna no supervisada en $[-1, 1]$ que mide cohesión (qué tan cerca está un punto de su propio cluster) frente a separación (qué tan lejos está del cluster vecino más cercano).

---

## Pregunta 5: Experimentos y Resultados Publicados en el Paper
> **[RESULTADOS PUBLICADOS EN EL PAPER — NO PROPIOS]**
* **Datasets evaluados en el paper:** `[COMPLETAR]`
* **Modelos o líneas base comparadas:** `[COMPLETAR]`
* **Métricas reportadas:** `[COMPLETAR]`
* **Resultados principales publicados por los autores:** `[COMPLETAR]`

---

## Pregunta 6: Crítica, Limitaciones y Riesgos
1. **Sensibilidad a hiperparámetros:** UMAP depende fuertemente de `n_neighbors` (balance local vs. global) y `min_dist` (compacidad de los grupos), así como de la semilla aleatoria (`random_state`). Un cambio de parámetros puede crear la ilusión visual de clusters más o menos separados.
2. **Riesgo de sobreinterpretar representaciones 2D:** Comprimir múltiples dimensiones a 2D inevitablemente introduce distorsiones geométricas. Un Silhouette Score alto en 2D tras UMAP refleja qué tan compactos quedaron los puntos *en esa proyección específica*, no necesariamente que los grupos sean esféricos en el espacio original.
3. **Supuestos de K-means:** K-means asume clusters de tamaño y densidad similares y forma esférica; si la proyección UMAP genera formas alargadas o no convexas, K-means puede dividir erróneamente un mismo grupo natural.
4. **Limitaciones específicas del paper:** `[COMPLETAR: costos computacionales, supuestos o riesgos señalados en el paper]`

---

## Pregunta 7: Aplicación Práctica por Nuestro Grupo
* **¿Qué hicimos?**
  * Trabajamos sobre el dataset **Wine** de `scikit-learn` (178 muestras de vinos, 13 variables fisicoquímicas continuas).
  * Escalamos todas las variables con `StandardScaler` para evitar que atributos de mayor magnitud dominen las distancias.
  * Evaluamos la elección de $k$ de manera **100% no supervisada** (analizando inercia/codo y Silhouette Score en el rango $k=2..6$ sobre el espacio escalado y las proyecciones, sin usar las etiquetas reales para ajustar nada).
  * Generamos representaciones en 2D mediante **PCA** y **UMAP** (semilla `random_state=42`, `n_neighbors=15`, `min_dist=0.1`), aplicamos **K-means** con el mismo $k=3$ (`n_init=20`, `random_state=42`) en ambos espacios, y calculamos el **Silhouette Score** en cada representación.
  * *(Opcional declarado como comparación externa)*: contrastamos los clusters descubiertos frente a las etiquetas originales de Wine (ARI / NMI) únicamente como referencia externa post-hoc.
* **¿Qué demuestran los resultados?**
  * Demuestran directamente cómo cambia la geometría de los datos según la representación (proyección lineal PCA vs. proyección no lineal UMAP) y cómo esto impacta la separabilidad medida por K-means y el Silhouette Score.
