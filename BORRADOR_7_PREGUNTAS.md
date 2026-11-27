# Borrador de las 7 Preguntas Obligatorias sobre el Paper
**Materia:** SIS-351 Machine Learning  
**Grupo:** Grupo 3 — Autoencoder, UMAP y clustering (aprendizaje no supervisado)  
**Paper asignado:** *Parametric UMAP Embeddings for Representation and Semisupervised Learning* (Sainburg, McInnes & Gentner, *Neural Computation*, 2021)  
**Pregunta guía:** *¿Cómo influye la representación en los patrones que vemos?*

---

## Pregunta 1: Identidad del Paper
* **Título completo:** *Parametric UMAP Embeddings for Representation and Semisupervised Learning*
* **Autores:** Tim Sainburg (University of California San Diego), Leland McInnes (Tutte Institute for Mathematics and Computing) y Timothy Q. Gentner (University of California San Diego).
* **Año y Publicación:** 2021, publicado en la prestigiosa revista *Neural Computation* (MIT Press), Vol. 33, Núm. 11, págs. 2881–2907. Comunicado por Terrence Sejnowski.
* **Enlaces oficiales:**
  * Neural Computation: [https://doi.org/10.1162/neco_a_01434](https://doi.org/10.1162/neco_a_01434)
  * arXiv: [https://arxiv.org/abs/2009.12981](https://arxiv.org/abs/2009.12981)
* **Versión y código de referencia:** Parametric UMAP, módulo oficial integrado dentro del paquete `umap-learn` en Python (soporta backends de TensorFlow/Keras y PyTorch).

---

## Pregunta 2: Problema que aborda el Paper
En aprendizaje no supervisado y reducción de dimensionalidad no lineal, existen dos grandes familias con limitaciones contrapuestas:
1. **Métodos no paramétricos basados en grafos (t-SNE, UMAP estándar):**
   * Destacan por capturar variedades topológicas no lineales complejas y preservar vecindades locales mucho mejor que métodos lineales como PCA.
   * **Limitación crítica:** Son no paramétricos; optimizan directamente las coordenadas 2D/3D de los puntos en el conjunto de entrenamiento. No aprenden una función explícita $f(x)$. Por ende, cuando llegan nuevos datos no vistos (*out-of-sample data*), es extremadamente lento o inviable proyectarlos sin reconstruir o aproximar costosamente todo el grafo. Tampoco permiten invertir la proyección de forma analítica para reconstruir los datos originales desde el espacio latente.
2. **Métodos paramétricos tradicionales (Autoencoders neuronales, VAEs):**
   * Aprenden funciones paramétricas continuas mediante redes neuronales (Encoder $f_\theta$ y Decoder $g_\phi$) optimizando un error de reconstrucción (MSE).
   * **Limitación crítica:** La función de pérdida de reconstrucción no preserva explícitamente las relaciones de vecindad ni la estructura topológica global o local del espacio original, produciendo a menudo espacios latentes dispersos o superpuestos donde clusters naturales quedan mezclados.

**El reto que aborda el paper:** ¿Cómo unir el poder de modelado topológico y de vecindad de UMAP con la flexibilidad funcional de una red neuronal profunda, permitiendo proyecciones paramétricas instantáneas para nuevos datos y regularizando el espacio latente de un Autoencoder?

---

## Pregunta 3: Contribución principal
Los autores introducen **Parametric UMAP**, un marco híbrido que parametriza el proceso de incrustación (*embedding*) de UMAP sobre los pesos de una red neuronal profunda:
1. **Parametrización con Redes Neuronales:** En lugar de optimizar directamente las coordenadas de salida como variables libres, se entrena una red neuronal profunda (*Encoder*) para predecir las coordenadas del embedding minimizando la pérdida de entropía cruzada difusa de UMAP (*UMAP loss*) mediante descenso de gradiente estocástico por minilotes (*mini-batch SGD*) y muestreo negativo (*negative sampling*).
2. **Autoencoder Regularizado por UMAP (Autoencoder Regularization):** Extienden la arquitectura agregando una red decodificadora (*Decoder*) que reconstruye la entrada original $\hat{x}$ a partir del espacio latente $z$. La función de pérdida global combina la preservación topológica con la reconstrucción:
   $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{UMAP}}(z) + \lambda \mathcal{L}_{\text{reconstrucción}}(x, \hat{x})$$
   Esto permite que el Autoencoder capture variedades no lineales con un espacio latente estructurado topológicamente y posibilite la interpolación y reconstrucción analítica.
3. **Inferencia online ultra-rápida:** Permite transformar nuevos datos (*forward pass*) órdenes de magnitud más rápido que UMAP no paramétrico, integrándose directamente en pipelines de Deep Learning y aprendizaje semi-supervisado (*semi-supervised learning*).

---

## Pregunta 4: Funcionamiento y Fundamentos Teóricos (Conexión con SIS-351)
* **Arquitectura del Autoencoder del Paper ("El Reloj de Arena Digital", Tema 05):**
  * **Encoder $f_\theta(x)$:** Red neuronal profunda (perceptrones multicapa densos para datos tabulares/vectoriales, redes convolucionales para imágenes o LSTMs para audio) que proyecta $x \in \mathbb{R}^D$ hacia el cuello de botella latente $z \in \mathbb{R}^d$ ($d \ll D$).
  * **Pérdida UMAP en el Latente:** Mide la divergencia entre la distribución de probabilidades difusas de aristas en el espacio original $P$ y en el espacio latente $Q$:
    $$\mathcal{L}_{\text{UMAP}} = \sum_{i \ne j} \left[ p_{ij} \log \frac{p_{ij}}{q_{ij}} + (1 - p_{ij}) \log \frac{1 - p_{ij}}{1 - q_{ij}} \right]$$
    Gracias al muestreo negativo, se evalúa eficientemente por minilotes sin requerir normalizaciones globales (a diferencia de parametric t-SNE).
  * **Decoder $g_\phi(z)$ y Reconstrucción:** Reconstruye $\hat{x} = g_\phi(z)$ minimizando el error cuadrático medio ($\mathcal{L}_{\text{MSE}} = \|x - \hat{x}\|^2$).
* **Conexión con los contenidos de SIS-351:**
  * **Aprendizaje No Supervisado (Tema 03):** Se conecta con PCA (línea base lineal que maximiza varianza global) y UMAP/t-SNE (geometría riemanniana y grafos de vecindad).
  * **Deep Learning (Temas 04 y 05):** Ilustra el uso de Autoencoders como modelos de compresión no lineal, funciones de activación (ReLU/LeakyReLU) para capturar no-linealidades complejas, optimizadores estocásticos (Adam) y regularización multi-tarea.
  * **Representaciones y Clustering:** K-means asume distancias euclidianas y centroides convexos; si el espacio de entrada está mal condicionado, K-means falla. La representación previa (sea PCA, UMAP o el espacio latente de un Autoencoder) determina directamente la calidad y geometría de los clusters resultantes.

---

## Pregunta 5: Experimentos y Resultados Publicados en el Paper
> **[RESULTADOS PUBLICADOS EN EL PAPER POR SAINBURG ET AL. (2021) — NO DEL GRUPO]**
* **Conjuntos de datos evaluados en el paper:**
  * Datasets de imágenes: MNIST (dígitos), Fashion-MNIST (prendas), CIFAR-10 (objetos naturales).
  * Datos biológicos y científicos: Transcriptomas de células individuales de retina de ratón (*Macosko et al.*), segmentos de cantos de aves (*Cassin's vireo*, espectrogramas acústicos).
  * Datasets geométricos sintéticos: *Moons* y *3D Buffalo*.
* **Líneas base comparadas:**
  * Métodos no paramétricos: UMAP estándar, t-SNE estándar, PHATE.
  * Métodos paramétricos y redes: Parametric t-SNE, SCVIS, IVIS, TriMap, Autoencoder estándar (AE), Variational Autoencoder (VAE) y PCA lineal.
* **Métricas evaluadas:** Error de reconstrucción (MSE), Silhouette Score en clusters, métrica de preservación de vecindad local (*Trustworthiness*), correlación de distancias globales y tiempo de inferencia/reconstrucción.
* **Resultados reportados por los autores:**
  * Parametric UMAP alcanza métricas de Silhouette Score y *Trustworthiness* equivalentes o superiores a UMAP no paramétrico, pero ejecutando la proyección de nuevos datos **órdenes de magnitud más rápido**.
  * El Autoencoder regularizado por UMAP ($\mathcal{L}_{\text{UMAP}} + \mathcal{L}_{\text{recon}}$) superó ampliamente a los Autoencoders clásicos y a PCA en calidad de reconstrucción no lineal (menor MSE), preservando simultáneamente la separación de clases en el espacio latente.

---

## Pregunta 6: Crítica, Limitaciones y Riesgos
1. **Costo de entrenamiento inicial y sobreajuste del Encoder:**
   A diferencia de UMAP no paramétrico que se calcula en una sola rutina de optimización numérica, Parametric UMAP requiere entrenar una red neuronal profunda con miles de parámetros, lo que exige sintonizar hiperparámetros de entrenamiento (tasa de aprendizaje, tamaño de lote, épocas) y puede sobreajustarse si los datos son muy escasos.
2. **Dependencia de la métrica de distancia original:**
   Si la distancia en el espacio original no captura similitud semántica (como ocurre con la distancia euclidiana directa en píxeles crudos de imágenes complejas como CIFAR-10), UMAP construye un grafo engañoso, degradando el espacio latente del Autoencoder.
3. **Distorsión geométrica en 2D y supuestos de K-means:**
   Reducir datos de alta dimensión a 2D genera necesariamente pérdidas topológicas. Aunque UMAP maximiza el Silhouette Score separando grupos locales, puede fracturar variedades continuas o alterar distancias globales. Si luego se aplica K-means, este algoritmo asume clusters esféricos de igual dispersión, lo que puede causar asignaciones erróneas si la proyección genera islas alargadas.

---

## Pregunta 7: Aplicación Práctica por Nuestro Grupo
* **¿Qué hicimos?**
  * Evaluamos empíricamente la influencia de las representaciones en el dataset **Wine** de `scikit-learn` (178 muestras, 13 variables fisicoquímicas continuas).
  * Estandarizamos las variables con `StandardScaler` (media 0, varianza 1) de forma estricta.
  * Justificamos la elección de $k=3$ de manera **100% no supervisada** mediante el método del codo en inercia y el punto máximo del Silhouette Score en el espacio escalado (`0.2849`).
  * Proyectamos los datos a dos dimensiones mediante dos paradigmas estudiados en la materia y en el paper:
    1. **PCA 2D (Lineal):** Basado en descomposición en valores singulares y varianza global.
    2. **UMAP 2D (No lineal):** Basado en topología difusa y grafos de vecindad (`n_neighbors=15`, `min_dist=0.1`, `random_state=42`).
  * Aplicamos K-means con el mismo $k=3$ (`n_init=20`, `random_state=42`) en ambos espacios y calculamos el Silhouette Score resultante (y ARI/NMI como comparación externa post-hoc declarada).
* **¿Qué demuestran los resultados propios?**
  * Demuestran que la representación condiciona drásticamente lo que el algoritmo de clustering "ve":
    * En PCA 2D (que retiene el 55.41% de varianza explicada), los clusters presentan fronteras cercanas y mayor solapamiento, con un Silhouette Score moderado de **0.5611**.
    * En UMAP 2D, las vecindades no lineales se compactan en agrupaciones nítidas y aisladas, elevando el Silhouette Score a **0.7111**.
  * Demuestran la lección crítica de la materia: una alta compacidad visual en 2D (alto Silhouette en UMAP) refleja la deformación de la proyección topológica, mientras que la proyección lineal de PCA preservó mayor fidelidad con las etiquetas externas reales (ARI de **0.8951** en PCA vs. **0.8025** en UMAP).
