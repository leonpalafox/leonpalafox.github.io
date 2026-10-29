---
layout: ../../layouts/Course.astro
title: "Deep Learning — León Palafox"
description: "From the single perceptron and the Universal Approximation Theorem to the state of the art."
heading: "Deep Learning"
---

**Universidad Panamericana** · *Master's in Data Science*  
**Instructor:** Dr. León Palafox

## Course Description

A comprehensive journey through the foundations and state-of-the-art of Deep Neural Networks, from the mathematical basics of the Perceptron through Transformers and generative models.

## Course at a glance

| # | Session | Resources |
| -- | ------- | ------ |
| 1 | [Introducción: representaciones, herramientas, perceptrón y backpropagation](/courses/deep-learning/class-01/) | [Deck](/slides/deep-learning/class-01-introduccion.html) · [PDF](/slides/deep-learning/class-01-introduccion.pdf) · [Colab](https://colab.research.google.com/drive/1eLdTmDQjlvF7qRlw2CBwDpHPO7j_mIrC?usp=sharing) |
| 2 | [Redes neuronales convolucionales: invarianza, convolución y pooling](/courses/deep-learning/class-02/) | [Deck](/slides/deep-learning/class-02-redes-convolucionales.html) · [PDF](/slides/deep-learning/class-02-redes-convolucionales.pdf) · [Colab](https://colab.research.google.com/drive/1HlMWpdtCkxoUpzOVyqYZ8HufpbYFEp_8?usp=sharing) |
| 3 | [Embeddings en CNN: de píxeles a vectores y aplicaciones](/courses/deep-learning/class-03/) | [Deck](/slides/deep-learning/class-03-embeddings-cnn.html) · [PDF](/slides/deep-learning/class-03-embeddings-cnn.pdf) · [Colab](https://colab.research.google.com/drive/1_LK6V7Rpdd2jtQMPKaLZiGtT8QGeMnxj) |
| 4 | [Regularización y transfer learning: generalización y CNN en la práctica](/courses/deep-learning/class-04/) | [Deck](/slides/deep-learning/class-04-regularizacion-transfer-learning.html) · [PDF](/slides/deep-learning/class-04-regularizacion-transfer-learning.pdf) |
| 5 | Recurrent networks: RNN, LSTM, GRU | *Próximamente* |
| 6 | Attention and the Transformer architecture | *Próximamente* |
| 7 | Pretrained language models: BERT, GPT | *Próximamente* |
| 8 | Generative models: VAEs and GANs | *Próximamente* |

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

*Cómo hacer que una CNN funcione en el mundo real.* · [Slides & outline →](/courses/deep-learning/class-04/) · [PDF ↓](/slides/deep-learning/class-04-regularizacion-transfer-learning.pdf)

1. **Repaso y aplicaciones** — convolución, pooling y aprendizaje jerárquico; visión en medicina, búsqueda visual, segmentación y video.
2. **Generalización y regularización** — overfitting, Dropout, BatchNorm y data augmentation para entrenar con pocos datos y mejorar la generalización.
3. **Transfer learning** — modelos preentrenados, extracción de características frente a fine-tuning y adaptación de la cabeza de clasificación.
4. **Práctica y evaluación** — anatomía de una solución de visión, entrenamiento y comparación de modelos, accuracy, precision, recall y matriz de confusión.

## Assessment

Assessment details and grading weights have not yet been posted.

## Schedule & Office Hours

Lecture times and office hours have not yet been posted.

**Contact:** [León Palafox](mailto:leon.palafox@gmail.com)
