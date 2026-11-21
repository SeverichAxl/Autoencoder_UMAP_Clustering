### 1. 01-introduccion-a-machine-learning.pdf

* **Definición de Machine Learning:** Es la ciencia que utiliza algoritmos para identificar patrones en los datos con el objetivo de resolver un problema específico. Se diferencia de la programación tradicional en que esta última toma reglas estrictas y datos para generar respuestas, mientras que el Machine Learning utiliza datos y respuestas para construir modelos que aprendan dichos patrones de forma automática.
* **Fundamentos Matemáticos:** Todo el Machine Learning se apoya en modelos simplificados sustentados en matemáticas y estadística. Además, forma parte del campo de la Inteligencia Artificial junto a otras disciplinas como algoritmos evolutivos, lógica difusa, agentes y sistemas expertos.
* **Categorías Principales de Aprendizaje:** Los métodos se dividen según la naturaleza y disponibilidad de los datos en:
  * **Aprendizaje Supervisado:** Predice un objetivo o *target* concreto. Puede ser de **regresión** (si el objetivo es un valor numérico) o de **clasificación** (si el objetivo es una etiqueta).
  * **Aprendizaje No Supervisado:** Explora y descubre la estructura o patrones inherentes en los datos sin etiquetas previa mediante técnicas de *clustering* o reducción de dimensionalidad.
  * **Aprendizaje por Refuerzo.**
* **La "Receta" de un Algoritmo de ML:** Todo algoritmo se compone de tres elementos esenciales:
  1. *Proceso de decisión:* Cómo se realizan las predicciones usando parámetros.
  2. *Función de error/coste:* Cómo se evalúa la calidad de las predicciones.
  3. *Regla de actualización:* Cómo se optimizan los parámetros para reducir el error.
* **Ruta de Selección de Modelos:** La elección del algoritmo depende de factores como el volumen de datos (si se tienen más o menos de 50 muestras), la presencia de datos etiquetados y la escala del dataset. La metodología **CRISP-ML(Q)** se presenta como el marco de calidad para llevar modelos desde la experimentación hasta la producción.

---

### 2. 02-aprendizaje-supervisado.pdf

* **Fundamento del Aprendizaje Supervisado:** Utiliza conjuntos de datos etiquetados (entradas acopladas con sus respuestas correctas) para entrenar modelos que mapean atributos (*features*) hacia etiquetas de salida, optimizando la precisión y evitando el sobreajuste (*overfitting*).
* **Modelos y Algoritmos Representativos:**
  * **Regresión Logística:** Utilizada en tareas como scoring crediticio y detección de spam, regulada por parámetros de penalización (\\(L1/L2\\)) e inversión de regularización (\\(C\\)).
  * **Árboles de Decisión y Random Forest:** Dividen los datos evaluando criterios de impureza como Gini o Entropía, controlando la profundidad máxima (`max_depth`) y la cantidad de árboles (`n_estimators`).
  * **Support Vector Machines (SVM):** Algoritmo versátil para clasificación y regresión que busca maximizar el margen geométrico mediante vectores de soporte. Utiliza el **Kernel Trick** para proyectar los datos a espacios de mayor dimensión y resolver no-linealidades, siendo obligatorio el escalado de datos previo (`StandardScaler`).
  * **Otros modelos:** K-Nearest Neighbors (KNN), Regresión Lineal, Ridge/Lasso, y Gradient Boosting (XGBoost/LightGBM).
* **Boosting y Regularización:**
  * Algoritmos como **XGBoost** funcionan como un *ensemble* de aprendices débiles donde cada nuevo árbol corrige de forma secuencial los errores residuales del anterior.
  * La función de optimización combina la pérdida con un término de regularización: \\(Obj(\Theta) = L(\Theta) + \Omega(\Theta)\\), equilibrando el sesgo (*bias*) y la varianza (*variance*).
* **Mejores Prácticas de Ingeniería:** Se enfatiza el uso de *Early Stopping* para ahorrar recursos, el manejo nativo de datos nulos, la aceleración por GPU (`gpu_hist`/`cuda`), el control estricto de profundidad (entre 3 y 8) y el uso de estructuras de datos optimizadas como `DMatrix`.

---

### 3. 03-aprendizaje-no-supervisado.pdf

* **Propósito Central:** Descubrir estructuras, patrones ocultos, agrupaciones naturales y anomalías en datos masivos sin etiquetas previas ni intervención humana.
* **Paradigmas de Clustering (Agrupamiento):**
  * **Basado en Centroides (K-Means):** Asigna puntos según distancias rígidas a centroides en geometrías planas o esféricas.
  * **Basado en Densidad (DBSCAN):** Agrupa por densidad de puntos en geometrías no planas, gestionando el ruido explícitamente mediante el radio mínimo epsilon (\\(\epsilon\\)) y el umbral de vecindario (\\(MinPts\\)), sin necesidad de optimizar una función de coste global.
  * **Probabilístico (GMM):** Modela agrupaciones suaves con geometrías elípticas.
  * **Jerárquico:** Métodos como Aglomerativo y BIRCH para datasets masivos.
* **Técnicas de Reducción de Dimensionalidad:** Superan "La Maldición de la Dimensionalidad" en conjuntos de datos con miles de variables:
  * **PCA (Análisis de Componentes Principales):** Técnica lineal rápida y altamente interpretable que preserva la estructura global y sirve como línea base primaria.
  * **t-SNE:** Técnica no lineal y estocástica optimizada para visualización exploratoria; preserva la estructura y vecindades locales (evitando el hacinamiento mediante la distribución t de Student), aunque distorsiona las distancias globales.
  * **UMAP:** Basado en topología algebraica, equilibra y preserva tanto la estructura local como la global de forma exponencialmente más rápida que t-SNE.
  * **Autoencoders:** Compresión mediante redes neuronales.
* **Pilares de IA Moderna y NLP:** Reglas de asociación (Apriori, FP-Growth) e integración de **Embeddings** (representación de texto no estructurado en vectores numéricos de 384 dimensiones), Búsqueda Vectorial, arquitectura RAG y AutoML (como H2O) para construir *pipelines* de extremo a extremo.

---

### 4. 04-deep-learning-parte-1.pdf

* **Fundamentos de Redes Neuronales:** Escalamiento conceptual desde una sola neurona artificial hasta redes multicapa profundas utilizando TensorFlow y Keras.
* **Anatomía de la Neurona y Arquitectura:** Compuestas por capas de entrada, capas ocultas y capas de salida. Cada neurona calcula una suma ponderada (\\(\sum w_i x_i + b\\)) y aplica una función de activación no lineal \\(f(x)\\).
* **Ciclo de Entrenamiento / Bucle Matemático:**
  1. *Inferencia (Forward Pass):* Se calculan las salidas progresivas \\(Z = WX + b\\) y \\(A = f(Z)\\).
  2. *Evaluación de Pérdida (Loss Function):* Se cuantifica el error con respecto al valor real usando MSE para regresión o Entropía Cruzada (*Cross-Entropy*) para clasificación.
  3. *Derivación (Backward Pass / Backprop):* Se propagan los gradientes hacia atrás para evaluar la contribución de cada peso al error.
  4. *Aprendizaje (Optimizer):* Se ajustan los pesos internos mediante algoritmos como SGD o Adam (\\(W = W - \alpha \cdot dW\\)).
* **Funciones de Activación Frecuentes:**
  * **Capas Ocultas:** ReLU (\\(y = \max(0, x)\\)) para convertir valores negativos a cero de forma computacionalmente eficiente, Leaky ReLU y Tanh.
  * **Capa de Salida:** Sigmoide para clasificación binaria; **Softmax** para convertir las puntuaciones crudas finales en una distribución de probabilidades que suma 1.0 (100%) en clasificación multiclase; y capa lineal para regresión.
* **Ecosistema de Redes:** Clasificación en Perceptrones, FeedForward (FFNN), Redes de Base Radial (RBFF), Recurrentes (RNN/LSTM/GRU), Autoencoders, GANs, Redes de Atención (Transformers) y Redes Transferenciales.
* **Prevención de Sobreajuste:** Uso de **Dropouts** y **Early Stopping** (detención temprana) para asegurar la generalización. Se trabaja con la API `keras.Sequential` apilando capas modularmente.

---

### 5. 05-deep-learning-parte-2.pdf

* **Evolución Histórica y el Perceptrón Multicapa (FFNN):**
  * Cronología desde 1943, el Perceptrón simple de Rosenblatt (1957), el "Invierno de la IA" en 1969 (cuando Minsky y Papert demostraron matemáticamente la incapacidad del perceptrón simple para resolver funciones no lineales como XOR) y el renacimiento mediante retropropagación (*backpropagation*) entre 1974 y 1985.
  * **Rol Crucial de la No-Linealidad:** Sin funciones de activación, cualquier red neuronal profunda colapsaría matemáticamente en un simple modelo de regresión lineal.
* **Arquitecturas Profundas Especializadas:**
  * **CNN (Redes Convolucionales):** Emplean filtros localizados y operadores de *pooling* para capturar relaciones espaciales; alta escalabilidad en visión por computadora.
  * **RNN (Redes Recurrentes):** Diseñadas para datos secuenciales con memoria contextual (texto, audio, series temporales). Presentan la limitación del **cuello de botella secuencial** y la degradación por gradiente evanescente (*vanishing gradient*), lo que impide su paralelización masiva en hardware moderno.
  * **Transformers:** Surgidos en 2017 ("*Attention Is All You Need*"), sustituyen la recurrencia por procesamiento paralelo global mediante el mecanismo de **Autoatención (Self-Attention)**. Desafíos actuales: complejidad computacional cuadrática \\(O(n^2)\\) respecto a la longitud del texto, alta demanda de VRAM y necesidad masiva de datos.
  * **Autoencoders ("El Reloj de Arena Digital"):** Arquitectura no supervisada que comprime la entrada en un espacio latente restringido (*bottleneck*) para posteriormente reconstruirla. Variantes: Convolucionales (CAE), Variacionales (VAE), RNN Autoencoders y Dispersos (SAE).
  * **GNN (Redes Neuronales de Grafos):** Diseñadas para datos no euclidianos y estructuras relacionales aleatorias (moléculas, redes sociales) mediante paso de mensajes.

---

### 6. 06-mlops.pdf

* **Definición y Cambio de Paradigma:** MLOps es la industrialización y gestión del ciclo de vida continuo de los modelos a escala. Extiende DevOps (enfocado únicamente en código determinista) al integrar **Datos** (estocásticos) y **Modelos** (sujetos a degradación y decaimiento silencioso en producción). Representa la "inmunidad del sistema" ante la entropía del mundo real.
* **Reglas de Oro e Ingeniería:**
  1. *Versionar todo:* Código (Git), datos (DVC) y entornos (Docker) para garantizar la reproducibilidad absoluta.
  2. *Entrenamiento Continuo (CT):* Automatizar el despliegue de *pipelines* de aprendizaje.
  3. *Monitoreo Activo:* Detectar la caída de métricas en vivo y la deriva de datos (*Data Drift*).
  4. *Despliegues Seguros:* Aplicar estrategias de liberación Canary, Blue/Green o Shadow.
  5. *Eliminar Silos:* Integración entre el científico de datos, el ingeniero y las métricas de negocio.
* **MLflow como Plataforma Central:**
  * **MLflow Tracking:** Centraliza la bitácora de experimentos registrando parámetros, métricas, código y artefactos.
  * **MLflow Model Registry:** Registro versionado e inmutable de modelos para la gestión de estados (Staging/Producción) e inferencia desacoplada.
* **Madurez y Aplicaciones Técnicas:**
  * Progresión por niveles de madurez: Nivel 0 (Manual / Jupyter Notebooks), Nivel 1 (Pipeline Automatizado) y Nivel 2 (Automatización Total con desencadenadores de eventos).
  * Integración de herramientas AutoML (FLAML) para la comparación objetiva de modelos frente a métricas *baseline* antes del pase a producción.
  * Implementación de arquitecturas avanzadas de RAG (Pre-recuperación con *Query Rewriting/HyDE*, Recuperación híbrida Vectores+BM25 y Post-recuperación con *Cross-Encoder*).
