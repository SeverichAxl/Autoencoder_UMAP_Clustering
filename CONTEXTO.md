# Contexto del proyecto — SIS-351 Machine Learning (3ra parte)

## Objetivo
Actividad grupal en 4 acciones: investigar un paper, comprender sus fundamentos
(conectados con lo visto en SIS-351), aplicar una práctica específica con evidencia
verificable y defender oralmente. NO se exige replicar el paper, igualar sus métricas,
entrenar modelos de gran escala desde cero ni presentar un notebook sin entenderlo.
Es independiente del proyecto integrador de SIS-351.

## Idioma y estilo
Todo en español. Explicaciones con palabras propias, claras y defendibles.
El código debe ser simple y comentado para que todos en el grupo puedan explicarlo.

## Entregables (una sola entrega grupal)
1. Informe científico: 4–6 páginas de contenido + portada + referencias.
2. Presentación: 8–12 diapositivas visuales y referenciadas.
3. Evidencia práctica: notebook/script con la práctica y resultados.
4. README: datos, dependencias, semilla y ejecución.
5. Defensa oral: 15–20 min por grupo, incluyendo preguntas.
Fecha y modalidad: las comunica el docente.

## 7 preguntas obligatorias sobre el paper
1 Identidad (título, autores, año, publicación, enlace, versión) · 2 Problema ·
3 Contribución (método/arquitectura/protocolo) · 4 Funcionamiento y fundamentos ·
5 Experimentos (datos, comparaciones, métricas, resultados publicados) ·
6 Crítica (limitaciones, supuestos, costos, riesgos) ·
7 Aplicación (qué hizo nuestro grupo y qué demuestran los resultados).

## Buenas prácticas (se evalúan)
- Citar papers, datasets, librerías y documentación.
- Trazabilidad: documentar entorno, particiones, semillas, parámetros y versiones.
- Rigor: evitar data leakage; NO ajustar modelos con el test.
- Distinguir resultados publicados vs. obtenidos por nosotros.
- Declarar uso de IA: herramientas, apoyo recibido y verificación.
- Ante problemas técnicos, consultar al docente antes de modificar la práctica.

## Práctica específica — Grupo 3

### Grupo 3 — Autoencoder, UMAP y clustering (no supervisado)
- Dataset: Wine (`load_wine` de scikit-learn), escalar las variables con `StandardScaler`.
- Obtener PCA y UMAP en 2D; aplicar K-means con el mismo `k` en cada espacio (y documentar la justificación de `k` sin usar etiquetas reales para ajustar).
- Explicar el autoencoder del paper (sin necesidad de entrenarlo).
- Evidencia: gráficos de clusters en PCA y UMAP; Silhouette Score en cada representación;
  interpretación crítica de las visualizaciones.
- Pregunta guía: ¿Cómo influye la representación en los patrones que vemos?
- Conexión con la materia: aprendizaje no supervisado (PCA, UMAP, K-means, Autoencoders) y representaciones.

## Datos del paper (completar)
- Título: [COMPLETAR]
- Autores: [COMPLETAR]
- Año: [COMPLETAR]
- Publicación: [COMPLETAR]
- Enlace: [COMPLETAR]
- Versión: [COMPLETAR]

## Plan de trabajo sugerido
1. Fijar decisiones: semilla global, split (random_state), versiones de librerías.
2. Resumir el paper respondiendo las 7 preguntas (borrador mío, el agente solo revisa).
3. Implementar la práctica en un notebook limpio, con celdas ordenadas y comentadas.
4. Generar tablas y gráficos exportados a /resultados.
5. Redactar README reproducible (requirements.txt, cómo ejecutar, semilla).
6. Informe + diapositivas + guion de defensa.
7. Checklist final (ver abajo).
## Modo de trabajo con el agente
- Trabajo con un solo agente a la vez, paso a paso, siguiendo el plan de trabajo.
- Antes de escribir código, confirma conmigo las decisiones (semilla, split, métricas).
- No avances al siguiente paso sin que yo valide el actual.
- Redacción del informe y las diapositivas: yo escribo con mis palabras; tú solo revisas
  claridad, coherencia y errores.
- Si algo del enunciado es ambiguo, pregúntame en vez de asumir.
- Lleva un registro breve de qué hiciste en cada paso (para declarar el uso de IA).
## Checklist antes de entregar
- [ ] Paper citado y contribución explicada con palabras propias
- [ ] Método relacionado con conceptos concretos de SIS-351
- [ ] Hicimos exactamente la práctica asignada
- [ ] Tablas, gráficos y evidencias obligatorias incluidas
- [ ] README permite reproducir el experimento
- [ ] Separamos resultados del paper, resultados propios y límites
- [ ] Todos podemos explicar la práctica y responder preguntas
- [ ] Uso de IA declarado