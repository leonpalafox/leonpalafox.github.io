---
layout: ../../layouts/Course.astro
title: "Deep Learning — León Palafox"
description: "From the single perceptron and the Universal Approximation Theorem to the state of the art."
heading: "Deep Learning"
---

**Universidad Panamericana** · *Master's in Data Science*  
**Instructor:** Dr. León Palafox

## Course Description

A comprehensive journey through the foundations and state-of-the-art of Deep Neural Networks, from the mathematical basics of the Perceptron through Transformers and training on multiple GPUs.

## Course at a glance

| # | Session | Resources |
| -- | ------- | ------ |
| 1 | [Introducción: representaciones, herramientas, perceptrón y backpropagation](/courses/deep-learning/class-01/) | [Deck](/slides/deep-learning/class-01-introduccion.html) · [PDF](/slides/deep-learning/class-01-introduccion.pdf) · [Colab](https://colab.research.google.com/drive/1eLdTmDQjlvF7qRlw2CBwDpHPO7j_mIrC?usp=sharing) |
| 2 | [Redes neuronales convolucionales: invarianza, convolución y pooling](/courses/deep-learning/class-02/) | [Deck](/slides/deep-learning/class-02-redes-convolucionales.html) · [PDF](/slides/deep-learning/class-02-redes-convolucionales.pdf) · [Colab](https://colab.research.google.com/drive/1HlMWpdtCkxoUpzOVyqYZ8HufpbYFEp_8?usp=sharing) |
| 3 | [Embeddings en CNN: de píxeles a vectores y aplicaciones](/courses/deep-learning/class-03/) | [Deck](/slides/deep-learning/class-03-embeddings-cnn.html) · [PDF](/slides/deep-learning/class-03-embeddings-cnn.pdf) · [Colab](https://colab.research.google.com/drive/1_LK6V7Rpdd2jtQMPKaLZiGtT8QGeMnxj) |
| 4 | [Regularización y transfer learning: generalización y CNN en la práctica](/courses/deep-learning/class-04/) | [Deck](/slides/deep-learning/class-04-regularizacion-transfer-learning.html) · [PDF](/slides/deep-learning/class-04-regularizacion-transfer-learning.pdf) · [Colab](https://colab.research.google.com/drive/13xNIhWsqNU3l9KoDVNDA6vkCZ75jfqwX?usp=sharing) |
| 5 | [Redes recurrentes: RNN, LSTM y GRU, de la recurrencia a las compuertas](/courses/deep-learning/class-05/) | [Deck](/slides/deep-learning/class-05-redes-recurrentes.html) · [PDF](/slides/deep-learning/class-05-redes-recurrentes.pdf) · [Colab](https://colab.research.google.com/drive/1SG6lPbf8fP4F_ClpeyO1zoPhHC523OoZ?usp=sharing) |
| 6 | [Transformers: atención, arquitectura y sus tres variantes](/courses/deep-learning/class-06/) | [Deck](/slides/deep-learning/class-06-transformers.html) · [PDF](/slides/deep-learning/class-06-transformers.pdf) |
| 7 | [Entrenamiento en paralelo: de los LLM a AlexNet en dos GPUs](/courses/deep-learning/class-07/) | [Deck](/slides/deep-learning/class-07-entrenamiento-paralelo.html) · [PDF](/slides/deep-learning/class-07-entrenamiento-paralelo.pdf) |

*Provisional syllabus. The session schedule will be posted once finalized.*

---

## Detailed syllabus

### Clase 1 — Introducción al aprendizaje profundo

*Por qué la representación de los datos lo cambia todo.* · [Slides & outline →](/courses/deep-learning/class-01/) · [PDF ↓](/slides/deep-learning/class-01-introduccion.pdf) · [Notebook en Colab ↗](https://colab.research.google.com/drive/1eLdTmDQjlvF7qRlw2CBwDpHPO7j_mIrC?usp=sharing)

1. **El curso** — objetivos, metodología, mapa del curso y evaluación (60% proyecto final en equipos de hasta 3; 40% tareas y participación).
2. **Representaciones y aplicaciones** — el problema de clasificación, cómo un cambio de coordenadas vuelve separable un problema, capas de representación, IA vs. ML vs. DL, y el papel de las GPUs, CUDA y la escala de datos. Casos: AlphaFold y modelos de lenguaje.
3. **Herramientas** — PyTorch, Keras y la historia de los frameworks de deep learning.
4. **Redes y entrenamiento** — el perceptrón, funciones de activación, redes de neuronas, el ciclo de entrenamiento, backpropagation y gradientes que se desvanecen; un primer vistazo a redes convolucionales y recurrentes.

### Clase 2 — Redes neuronales convolucionales

*Un mismo filtro recorre toda la imagen.* · [Slides & outline →](/courses/deep-learning/class-02/) · [PDF ↓](/slides/deep-learning/class-02-redes-convolucionales.pdf) · [Notebook en Colab ↗](https://colab.research.google.com/drive/1HlMWpdtCkxoUpzOVyqYZ8HufpbYFEp_8?usp=sharing)

1. **Invarianza y características locales** — por qué un dígito girado, desplazado o escalado es otra imagen píxel por píxel; aumentar los datos artificialmente frente a modelar las transformaciones; características locales y estacionaridad.
2. **Convolución y pooling** — el filtro que recorre la imagen, la convolución como ecuación, max y average pooling, y por qué compartir pesos equivale a entrenar con un conjunto de datos mucho más grande.
3. **Datos** — CIFAR-10, ImageNet y el reto ILSVRC, donde AlexNet (2012) mostró lo que podían hacer las CNN entrenadas en GPUs.

### Clase 3 — Embeddings en CNN

*De una imagen a un vector reutilizable.* · [Slides & outline →](/courses/deep-learning/class-03/) · [PDF ↓](/slides/deep-learning/class-03-embeddings-cnn.pdf) · [Notebook en Colab ↗](https://colab.research.google.com/drive/1_LK6V7Rpdd2jtQMPKaLZiGtT8QGeMnxj)

1. **Embeddings** — representaciones visuales, similitud más allá de los píxeles y un experimento con transformaciones de una misma imagen.
2. **De píxeles a vectores** — backbone y head de clasificación, jerarquía de características, feature maps y Global Average Pooling.
3. **Del clasificador al encoder** — quitar la última capa, reutilizar la representación y extraer un embedding de 2048 dimensiones con ResNet-50.
4. **Aplicaciones** — búsqueda visual por similitud, clustering sin etiquetas, transferencia de aprendizaje y detección de anomalías.
5. **Buenas prácticas** — elegir modelo y capa de extracción, congelar o ajustar el backbone, normalizar los vectores y escoger una métrica de similitud.

### Clase 4 — Regularización y transfer learning

*Cómo hacer que una CNN funcione en el mundo real.* · [Slides & outline →](/courses/deep-learning/class-04/) · [PDF ↓](/slides/deep-learning/class-04-regularizacion-transfer-learning.pdf) · [Colab ↗](https://colab.research.google.com/drive/13xNIhWsqNU3l9KoDVNDA6vkCZ75jfqwX?usp=sharing)

1. **Repaso y aplicaciones** — convolución, pooling y aprendizaje jerárquico; visión en medicina, búsqueda visual, segmentación y video.
2. **Generalización y regularización** — overfitting, Dropout, BatchNorm y data augmentation para entrenar con pocos datos y mejorar la generalización.
3. **Transfer learning** — modelos preentrenados, extracción de características frente a fine-tuning y adaptación de la cabeza de clasificación.
4. **Práctica y evaluación** — anatomía de una solución de visión, entrenamiento y comparación de modelos, accuracy, precision, recall y matriz de confusión.

### Clase 5 — Redes recurrentes: RNN, LSTM y GRU

*De la estructura espacial a la temporal.* · [Slides & outline →](/courses/deep-learning/class-05/) · [PDF ↓](/slides/deep-learning/class-05-redes-recurrentes.pdf) · [Notebook en Colab ↗](https://colab.research.google.com/drive/1SG6lPbf8fP4F_ClpeyO1zoPhHC523OoZ?usp=sharing) · *Diapositivas en inglés*

1. **Motivación** — lo que un MLP y una CNN no pueden hacer con secuencias: longitud variable, orden y memoria a distancias arbitrarias.
2. **La recurrencia** — una misma celda reutilizada en cada paso, el estado oculto como resumen comprimido, el desenrollado en el tiempo, compartir pesos a lo largo del tiempo (el truco de la CNN en otro eje) y las formas de entrada y salida: one-to-many, many-to-one y many-to-many.
3. **El problema** — backpropagation a través del tiempo: gradientes que explotan (se corrigen con gradient clipping) y gradientes que se desvanecen en silencio.
4. **LSTM** — el estado de celda como autopista de memoria; compuertas de olvido, entrada y salida, y por qué una actualización aditiva preserva la señal.
5. **GRU** — dos compuertas (reset y update) y un solo estado; comparación lado a lado de RNN, LSTM y GRU con ejemplos, y cuándo usar cada una.
6. **En la práctica** — redes bidireccionales y apiladas, padding, masking y empaquetado de secuencias en PyTorch.
7. **Panorama** — por qué los Transformers las reemplazaron, dónde siguen vivas (streaming, dispositivos embebidos, series de tiempo) y su regreso con Mamba, RWKV y xLSTM; cierra con un ejemplo resuelto paso a paso de una LSTM sobre “the movie was not good”.

### Clase 6 — Transformers: atención, arquitectura y sus tres variantes

*La recurrencia se va; la atención se queda.* · [Slides & outline →](/courses/deep-learning/class-06/) · [PDF ↓](/slides/deep-learning/class-06-transformers.pdf) · *Diapositivas en inglés*

1. **De la LSTM a la atención** — seq2seq, el cuello de botella de un solo vector, el problema de predecir con todo el contexto y por qué «Attention is all you need» elimina la recurrencia.
2. **Atención** — self-attention, queries, keys y values, producto punto escalado resuelto a mano y multi-head attention.
3. **Arquitectura** — tokenizer, embeddings, codificación posicional, bloques de encoder y decoder, y la proyección lineal + softmax que convierte un vector en un token.
4. **Flujo de tokens** — codificar la oración fuente, decodificar token a token, las formas de los tensores de extremo a extremo y teacher forcing.
5. **Tres variantes** — solo encoder (BERT), solo decoder (GPT) y encoder–decoder (T5, BART); quién puede ver a quién y cómo elegir.
6. **Panorama** — BERT en números, de 2017 a hoy y el precio de la escala: de 65M a ~10T parámetros.

### Clase 7 — Entrenamiento en paralelo

*De entrenar un LLM a medir dos GPUs.* · [Slides & outline →](/courses/deep-learning/class-07/) · [PDF ↓](/slides/deep-learning/class-07-entrenamiento-paralelo.pdf) · [mini_llm.py ↓](/code/deep-learning/mini_llm.py) · [mide.py ↓](/code/deep-learning/mide.py)

1. **¿Por qué GPUs?** — cómo se entrena un LLM, un mini LLM medido en CPU y GPU, cuánto tardaría un modelo grande y cuánta memoria pide.
2. **Pensar en paralelo** — dependencias paso a paso, speedup y eficiencia, la parte que no se divide, el costo de comunicar y los colectivos.
3. **Repartir el entrenamiento** — datos en paralelo y DDP en PyTorch; partir un modelo que no cabe (pipeline, tensorial, ZeRO y FSDP).
4. **AlexNet en dos GPUs** — por qué DDP con FP32 salió más lento que una GPU y tres formas de mover menos datos.
5. **Decidir** — resultados, una demo en Runpod y un ejercicio con un LLM.
6. **Cierre del curso** — todo es datos + modelo + optimización: un repaso de las siete clases y cómo la paralelización reparte las tres.

## Evaluación

La calificación del curso se compone de **60 % proyecto final** (en equipos de hasta 3 personas) y **40 % tareas y participación**. **Fecha de entrega del proyecto: jueves 3 de diciembre de 2026.**

### Rúbrica del proyecto final

El proyecto final consiste en el **despliegue completo, en un sitio web, de una solución basada en aprendizaje profundo**. El modelo debe haber sido **entrenado desde cero o ajustado (ajuste fino o *fine-tuning*)** por el equipo; no basta con usar un modelo ya entrenado tal como viene.

#### Reglas sobre el modelo

| Tipo de modelo | ¿Qué se permite? |
| -------------- | ---------------- |
| Basado en imágenes (clasificación, detección, segmentación, etc.) | Entrenamiento desde cero **o** fine-tuning de un modelo preentrenado. |
| Series de tiempo | Entrenamiento desde cero **o** fine-tuning de un modelo preentrenado. |
| LLM (modelos de lenguaje grandes) | **Solo entrenamiento desde cero.** No se permite hacer fine-tuning de un LLM ni limitarse a consumir uno por API. |
| Cualquier otra modalidad (audio, texto que no sea un LLM, datos tabulares) | **Solo entrenamiento desde cero.** El fine-tuning se acepta únicamente en modelos de imágenes y de series de tiempo. |

#### Qué se entrega

1. **Un archivo PDF** que describa:
   - **El dataset:** origen y licencia, tamaño, clases o variables, preprocesamiento, particiones de entrenamiento, validación y prueba, y limitaciones o sesgos conocidos.
   - **El modelo:** el tipo de red (por ejemplo CNN, LSTM, GRU, Transformer o LLM), si fue entrenado desde cero o ajustado (y a partir de qué modelo base), procedimiento de entrenamiento, métricas y resultados.
   - **La arquitectura:** una **explicación o un diagrama de arquitectura** del modelo de aprendizaje profundo (o ambos). Debe mostrar las capas o bloques principales y cómo fluyen los datos de la entrada a la salida.
2. **El enlace al sitio web** con el despliegue, escrito en el PDF y en el mensaje de entrega.

**El PDF no debe contener código**: ni fragmentos, ni capturas de pantalla de código, ni pseudocódigo. Las decisiones se explican con texto, tablas, figuras y el diagrama de arquitectura.

#### Requisitos mínimos

- El sitio es **público** y se puede abrir sin crear una cuenta ni instalar nada.
- El sitio **ejecuta el modelo entrenado por el equipo**: una persona externa introduce una entrada y obtiene una predicción.
- El sitio debe **seguir disponible hasta que se publiquen las calificaciones**.
- El PDF y el sitio describen el mismo modelo.

Un proyecto que no cumpla las reglas sobre el modelo obtiene **0 puntos en el criterio «Modelo y entrenamiento»**. Si el sitio no abre o no ejecuta el modelo, obtiene **0 puntos en «Despliegue»**.

#### Criterios y puntos (100 en total)

| Criterio | Puntos |
| -------- | :----: |
| Dataset | 20 |
| Modelo y entrenamiento | 30 |
| Despliegue | 30 |
| Documento | 20 |

Cada criterio se califica en tres niveles: **Sobresaliente** (90–100 % de los puntos del criterio), **Suficiente** (60–89 %) e **Insuficiente** (menos de 60 %).

**Dataset (20 puntos)**

- *Sobresaliente:* describe origen, licencia, tamaño, clases o variables, preprocesamiento y particiones; analiza sesgos, desbalance y limitaciones, y justifica por qué el dataset es adecuado para el problema.
- *Suficiente:* describe el origen, el tamaño y las particiones, pero el análisis de sesgos o limitaciones es superficial o falta.
- *Insuficiente:* descripción incompleta o confusa; no se puede saber cómo se dividieron los datos.

**Modelo y entrenamiento (30 puntos)**

- *Sobresaliente:* cumple las reglas sobre el modelo. Incluye una explicación o un diagrama de arquitectura claro y correcto, justifica la arquitectura, explica el procedimiento (hiperparámetros, regularización y modelo base si hubo fine-tuning), reporta métricas adecuadas en datos de prueba y las compara con una referencia, por ejemplo un modelo más simple.
- *Suficiente:* cumple las reglas y reporta métricas, pero la explicación o el diagrama de la arquitectura es vago, o la justificación o la comparación con una referencia es débil.
- *Insuficiente:* falta la explicación o el diagrama de la arquitectura; métricas ausentes o evaluadas solo con datos de entrenamiento; el procedimiento no se entiende.

**Despliegue (30 puntos)**

- *Sobresaliente:* sitio público y estable que ejecuta el modelo propio. La interfaz es clara, maneja entradas inválidas sin fallar y responde en un tiempo razonable.
- *Suficiente:* el sitio funciona, pero es poco claro, es lento o falla con ciertas entradas.
- *Insuficiente:* el sitio no abre, no ejecuta el modelo o requiere cuenta o instalación.

**Documento (20 puntos)**

- *Sobresaliente:* PDF claro y bien organizado, con figuras o tablas útiles, resultados y limitaciones discutidos con honestidad, el enlace al sitio visible y **sin ningún código**.
- *Suficiente:* contiene la información pedida, pero está desordenado o tiene poco análisis de resultados.
- *Insuficiente:* información faltante, difícil de seguir o incluye código.

## Schedule & Office Hours

Lecture times and office hours have not yet been posted.

**Contact:** [León Palafox](mailto:leon.palafox@gmail.com)
