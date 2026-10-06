---
title: Deep Learning · Clase 1 · Universidad Panamericana
footer: Deep Learning · Dr. León Palafox
pdf: /slides/deep-learning/class-01-introduccion.pdf
credits:
> Texto: UPDL2024_1_Intro.pptx, material aportado por el profesor. Las ilustraciones originales se reconstruyeron como elementos HTML animados.
> Logotipos: el logotipo oficial de la Universidad Panamericana y los logotipos de Mila, UC Berkeley, Facebook, Google, Apache y Python provienen del material original del profesor. NVIDIA, Microsoft Azure, Google Colab y Google DeepMind: colecciones libres SVG Logos (Gil Barbara, CC0) y Simple Icons (CC0). Universidad de Toronto: plantilla Beamer-template-uoft (GitHub). Cada marca pertenece a su titular.
> Marca institucional UP: <a href="https://www.up.edu.mx/marca-institucional/marca/" target="_blank" rel="noopener">https://www.up.edu.mx/marca-institucional/marca/</a>
---

<!--
Every word on the Deep Learning class 1 slides lives in this file. The design and the
animations live in class-01-introduccion.template.html; the site merges the two at build time.

How to edit
- "# Section" names the section shown in each slide's header.
- "## Title" starts a slide. Keep the 44 slides in this order: each one has its own animation.
- "key: text" is one line of text. HTML is allowed (<b>, <br>, <sup>, <span class="m"> for math).
- "key:" followed by "- item" lines is a list. "a | b | c" splits an item into the parts
  that slide shows side by side (e.g. a heading and its description). Keep the same number of
  items and parts; the layout is drawn for them.
- {logo:nvidia} and {logo:uoft} insert those logos.
- Speaker notes (the deck's Notes button): guide, remark, sources, original.

After editing, preview with `npm run dev` at /slides/deep-learning/class-01-introduccion.html,
then run `npm run slides:pdf` to refresh the downloadable PDF before you push.
-->

# El curso

## Deep Learning
layout: cover
kicker: Sesión 01
heading: Deep<br>Learning
subtitle: Introducción
author: Dr. León Felipe Palafox Novack
email: lfpalafox@up.edu.mx
topics:
- Representaciones
- Redes neuronales
- Backpropagation
- Redes convolucionales
- Redes recurrentes
- Transformers
guide:
- Introducción
- Dr. León Felipe Palafox Novack
- lfpalafox@up.edu.mx
original:
> Deep Learning
>
> Dr. Leon Felipe Palafox Novack
> lfpalafox@up.edu.mx

## Anuncios
layout: quiet
label: Avisos de la sesión
hint: Haz clic en una línea para escribir · se guarda en este navegador
original:
> Anuncios
>
>
>
> 2

## Objetivos de la sesión
layout: text
lead: Al terminar la sesión, podrás:
objectives:
- Explicar | cómo una red aprende representaciones.
- Distinguir | las funciones de la pérdida y del optimizador.
- Implementar y validar | una red con PyTorch.
guide:
- Explicar cómo una red aprende representaciones.
- Distinguir las funciones de la pérdida y del optimizador.
- Implementar y validar una red con PyTorch.
original:
> Objetivo
>
> Los estudiantes serán capaces de implementar y validar diferentes técnicas de Aprendizaje Profundo, podrán utilizar la librería de Python llamada Pytorch, y podrán aplicar aprendizaje profundo a diferentes problemas.
>
>
> 3

## Metodología de aprendizaje
layout: text
columns:
- Teoría | Intuición; Mecanismo; Límites
- Práctica | Implementar; Evaluar; Interpretar
- Casos de uso | Fallas; Oportunidades
caption: La clase combina una sección teórica y una práctica; en la práctica analizamos casos de uso de los algoritmos, sus fallas y sus oportunidades.
guide:
- Teoría: intuición, mecanismo y límites.
- Práctica: implementar, evaluar e interpretar.
- Casos de uso: fallas y oportunidades.
original:
> Metodología de Aprendizaje
>
> La clase comprenderá de una sección teórica y una sección práctica.
> En la sección práctica analizaremos casos de uso de los algoritmos, asi como fallas y oportunidades.
>
> 4

## Mapa del curso
layout: agenda
modules:
- Introducción al aprendizaje profundo
- Redes convolucionales (CNN)
- Redes recurrentes (RNN)
- Transfer learning
- LSTM y Transformers
today: Hoy
guide:
- Introducción al aprendizaje profundo
- Redes convolucionales (CNN)
- Redes recurrentes (RNN)
- Transfer learning
- LSTM y Transformers
original:
> Temario
>
> Introduction to Deep Learning
> Convolutional Neural Networks (CNNs)
> Recurrent Neural Networks (RNNs)
> Transfer Learning
> Advanced Topics in Deep Learning (LSTM, Transformers)
>
> 5

## Evaluación
layout: assessment
project_weight: 60
project_label: Proyecto final
project_details:
- Equipos de hasta 3 personas
- Reporte de 3–5 páginas: datos, diseño y variables
coursework_weight: 40
coursework_label: Tareas y participación
coursework_details:
- Tareas
- Participación en clase
guide:
- 60% · Proyecto final
- 40% · Tareas y participación
- Equipos de hasta 3 personas
- Reporte de 3–5 páginas: datos, diseño y variables
original:
> Evaluación
>
> La evaluación consistirá en:
>
> - El proyecto final será el 60% de la evaluación final.
> - Pueden hacer equipos de hasta tres personas.
>   - Necesitan hacer un reporte de 3-5 paginas sobre el set de datos, el diseño y las variables usadas.
>
> - El restante 40% será distribuido de la siguiente forma:
> - Tareas.
>   - Participación en clase
>
>
> 6

## Proyecto final
layout: split
steps:
- Un problema concreto.
- Un modelo.
- Una evaluación.
ideas_label: Ideas de proyecto
ideas:
- Deportes | Despeje óptimo del portero | ¿A dónde patear para que su equipo gane el balón?
- Visión | Detección de autos | Localizar vehículos en video de calle
- Visión | Reconocimiento facial | Verificar identidad a partir de una foto
- Visión | Generación de arte | Transferir el estilo de una pintura a una foto
- Audio | Generación de música | Componer secuencias nuevas
- Texto | Generación de texto | Escribir con el estilo de un autor
- Texto | Emojificador | Elegir el emoji adecuado para una frase
- Texto | Traducción automática | Pasar un texto de un idioma a otro
- Audio | Palabra de activación | Encender un sistema al oír una palabra
guide:
- Un problema concreto. Un modelo. Una evaluación.
remark: Las nueve ideas reproducen los ejemplos de la ilustración original (proyectos clásicos de cursos de deep learning).
original:
> Proyecto Final
>
> 7

## Contenido de esta sesión
layout: agenda
topics:
- Aplicaciones del aprendizaje profundo | AlphaFold y modelos de lenguaje
- PyTorch y otros frameworks | Tensores, diferenciación automática y GPU
- Fundamentos de redes neuronales | Perceptrón, activaciones y capas
- Backpropagation y optimización | Regla de la cadena y gradiente descendente
- CNN y RNN | Visión y secuencias
guide:
- Aplicaciones del aprendizaje profundo
- PyTorch y otros frameworks
- Fundamentos de redes neuronales
- Backpropagation y optimización
- CNN y RNN
original:
> Temario
>
> Visión general del aprendizaje profundo y sus aplicaciones
> Introducción a los marcos de trabajo del aprendizaje profundo, como TensorFlow y PyTorch
> Fundamentos de las redes neuronales
> Retropropagación y algoritmos de optimización
> Arquitecturas avanzadas de redes neuronales, como CNNs y RNNs
>
>
> 8

# Representaciones y aplicaciones

## Aprendizaje profundo
layout: divider
number: 01
question: ¿Cómo aprende una red la representación que necesita?
guide:
- ¿Cómo aprende una red la representación que necesita?
original:
> Deep Learning
>
>
>
> 9
>
> 2

## El problema de clasificación
layout: question
questions:
- ¿Qué clase corresponde a cada observación?
- ¿Qué limita a nuestro clasificador?
- ¿Podemos cambiar la representación?
guide:
- ¿Qué clase corresponde a cada observación?
- ¿Qué limita a nuestro clasificador?
- ¿Podemos cambiar la representación?
original:
> Problema de Clasificacion
>
> En que consiste el problema de la clasificacion?
>
> Cuales son sus limitantes?
>
> Como lo podemos atacar?
>
> 10

## La representación cambia el problema
layout: split
lead: Una frontera lineal puede fallar en las coordenadas originales.
class_a: Clase A
class_b: Clase B
result: Ninguna recta separa el centro del anillo.
guide:
- Una frontera lineal puede fallar en las coordenadas originales.
original:
> Por que es necesario el Deep Learning
>
> 11

## El mismo dato, otras coordenadas
layout: split
lead: El radio puede separar clases que forman círculos concéntricos.
formula_r: r = √(x² + y²)
formula_theta: θ = atan2(y, x)
result: Una recta vertical, <span class="m">r</span> = 0.48, separa las clases.
guide:
- El radio puede separar clases que forman círculos concéntricos.
original:
> 12
>
> Muchos problemas de integración se vuelven más fáciles al momento de usar polares.

## Clasificación y características
layout: text
bullets:
- Las características describen el dato: píxeles, palabras o medidas.
- Algunas clases son difíciles de separar con la representación inicial.
- Transformar los datos puede simplificar la clasificación.
vector_label: Una observación → un vector de características
vector_rows:
- Imagen | píxeles | x = [0.12, 0.80, 0.33, …]
- Texto | conteo de palabras | x = [0, 2, 1, 0, …]
- Sensor | medidas | x = [36.8, 72, 1.2, …]
initial_label: Representación inicial
transformed_label: Después de una transformación <span class="nt m">φ(x)</span>
threshold_note: un umbral basta
guide:
- Las características describen el dato: píxeles, palabras o medidas.
- Algunas clases son difíciles de separar con la representación inicial.
- Transformar los datos puede simplificar la clasificación.
original:
> Clasificación
>
> En muchos problemas de clasificación es difícil (imposible) crear una separación usando los features que tenemos a nuestra disposición.
> Feature son los elementos descriptivos del dataset (pixeles, palabras, etc)
> Se recurre a técnicas de transformación para poder obtener mejores clasificadores.
>
>
> 13

## Capas de representación
layout: split
axis_top: más abstracto
axis_bottom: más local
parts:
- ojo
- rueda
- oreja
classes:
- AUTO
- PERSONA
- ANIMAL
layers:
- Entrada | Píxeles
- Capa 1 | Bordes
- Capa 2 | Esquinas y contornos
- Capa 3 | Partes de objetos
- Salida | Clase
lead: Las primeras capas detectan patrones locales.
caption: Bordes, esquinas y contornos: rasgos simples que aparecen en cualquier parte de la imagen.
guide:
- Las primeras capas detectan patrones locales.
original:
> Clasificación
>
> 14

## La combinación de patrones
layout: split
lead: Las capas combinan rasgos para identificar la clase.
caption: Bordes → esquinas → partes (ojo, oreja) → <b>persona</b>. Cada capa combina lo que detectó la anterior.
guide:
- Las capas combinan rasgos para identificar la clase.
remark: Las probabilidades de salida son ilustrativas.
original:
> Clasificación
>
> 15
>
> Al final es la combinación de esas capas de abstracción las que permiten al clasificador identificar la clase del dato.

## IA, machine learning y deep learning
layout: split
lead: Deep learning es una familia de métodos de machine learning.
formula: DL ⊂ RL ⊂ ML ⊂ IA
caption: Cada círculo agrega una idea: aprender de datos, aprender la representación y hacerlo con muchas capas.
circles:
- Inteligencia artificial | Ej.: bases de conocimiento
- Machine learning | Ej.: regresión logística
- Aprendizaje de<br>representaciones | Ej.: autoencoders superficiales
- Deep learning | Ej.: MLP
guide:
- Deep learning es una familia de métodos de machine learning.
original:
> 16

## Vocabulario de la clase
layout: text
networks: Redes neuronales profundas
networks_text: Modelos con varias capas.
networks_aka:
- deep learning
- redes profundas
- redes neuronales
units: Neuronas o unidades
units_text: Transformaciones con parámetros:
units_formula: h = f(w<sup>T</sup>x + b)
learning: Formas de aprendizaje
learning_kinds:
- Supervisado | pares (x, y) etiquetados
- Autosupervisado | la señal sale del propio dato
- Por refuerzo | recompensas de un entorno
guide:
- Redes neuronales profundas: modelos con varias capas.
- Neuronas o unidades: transformaciones con parámetros.
- Aprendizaje supervisado, autosupervisado y por refuerzo.
original:
> Reglas del Juego
>
> Redes Profundas, Deep Learning, Redes Neuronales.
> Aprendizaje Supervisado.
> Se esta usando en aprendizaje autosupervisado y reforzado.
> Unidades, Neuronas, etc
>
>
> 17

## Prerrequisitos
layout: question
prerequisites:
- Regresión logística | ŷ = σ(w<sup>T</sup>x + b)
- Gradiente descendente | w ← w − η ∇<i>L</i>(w)
- ¿Qué función minimiza el optimizador? | L(w) = <span class="blink">?</span>
guide:
- Regresión logística
- Gradiente descendente
- ¿Qué función minimiza el optimizador?
original:
> Asumptions
>
> Ya están familiarizados con Regresión Logística
> Gradiente Descendiente.
>
> 18

## Ventajas y límites
layout: text
advantages_label: Ventajas
advantage_1: Aprender representaciones reduce el diseño manual de características.
advantage_2: Las GPU aceleran operaciones que pueden ejecutarse en paralelo.
needs_label: Lo que sigue siendo necesario
needs:
- Datos
- Cómputo
- Evaluación
caption: Datos, cómputo y evaluación siguen siendo necesarios: aprender la representación no elimina el trabajo de validar.
guide:
- Aprender representaciones reduce el diseño manual de características.
- Las GPU aceleran operaciones que pueden ejecutarse en paralelo.
- Datos, cómputo y evaluación siguen siendo necesarios.
original:
> Ventajas
>
> Veremos que DL ofrece muchas ventajas con respecto a otros algoritmos de Machine Learning.
> Facilidad de implementación.
> Uso de GPU para aceleración de entrenamiento.
> Un “hype” de ensueño.
>
> 19

## Herramientas para implementarlo
layout: gallery
lead: Python para programar.
lead_2: Infraestructura local o en la nube.
rows:
- Lenguaje
- Frameworks
- Infraestructura
- Hardware
frameworks:
- PyTorch
- TensorFlow
- JAX
- Keras
local: Local
local_text: laptop o estación de trabajo
cloud: Nube
hardware:
- CPU
- GPU · CUDA
guide:
- Python para programar. Infraestructura local o en la nube.
remark: El logotipo de Python proviene del material original; los íconos de Microsoft Azure y Google Colab provienen de las colecciones libres SVG Logos y Simple Icons.
original:
> Hay muchas formas de usarlos
>
> 20

## Expectativas y madurez
layout: image
phases:
- Desencadenante de la innovación
- Pico de expectativas infladas
- Valle de la desilusión
- Pendiente de la iluminación
- Meseta de la productividad
technologies:
- IA cuántica
- Agentes de IA
- Datos listos para IA
- Servicios de IA en la nube
- Destilación de modelos
y_axis: Expectativas
x_axis: Tiempo →
highlight: IA generativa
highlight_note: entrando al valle de la desilusión
message: El entusiasmo no sustituye la validación.
footnote: Posiciones según Gartner, <i>Hype Cycle for Artificial Intelligence, 2025</i> (junio de 2025). Selección de tecnologías.
guide:
- El entusiasmo no sustituye la validación.
remark: Posiciones tomadas de la gráfica de Gartner «Hype Cycle for Artificial Intelligence, 2025» (junio de 2025); selección de seis tecnologías.
sources:
- https://www.gartner.com/en/newsroom/press-releases/2025-08-05-gartner-hype-cycle-identifies-top-ai-innovations-in-2025
original:
> 21

## GPU: el origen gráfico
layout: image
lead: Las GPU nacieron para dibujar, no para pensar.
timeline:
- 1993 | {logo:nvidia} se funda.
- 1998 | 3dfx Voodoo2 populariza la aceleración 3D en PC.
- 1999 | GeForce 256: NVIDIA la presenta como «la primera GPU».
caption_left: Nadie pensaba todavía en multiplicar matrices.
gpu_label: Trabajo de la GPU: calcular cada píxel, rápido
frame_label: fotograma
caption_right: Cada píxel se calcula por separado: miles de cálculos idénticos, en paralelo.
remark: La ilustración original (una caricatura) se reemplazó por una cuadrícula de «píxeles» HTML: en cada fotograma todos se recalculan a la vez.
sources:
- https://blogs.nvidia.com/blog/first-gpu-gaming-ai/
- https://en.wikipedia.org/wiki/GeForce_256
original:
> 22

## Cómputo paralelo y CUDA
layout: image
lead: NVIDIA convirtió un chip para videojuegos en un instrumento científico.
timeline:
- 2006 | GeForce 8800 GTX: 128 núcleos programables.
- 2007 | CUDA: programar la GPU para cálculo general.
-  | Ian Buck (de Stanford a NVIDIA) y John Nickolls impulsaron CUDA.
formula: <span class="m">C = A × B</span> · cada celda <span class="m">C<sub>ij</sub> = Σ<sub>k</sub> A<sub>ik</sub>B<sub>kj</sub></span> es independiente
cpu_label: CPU · 4 núcleos
gpu_label: GPU · 128 núcleos
steps_label: pasos:
caption: Misma operación: 16 pasos contra 1.
remark: La carrera CPU contra GPU es ilustrativa: 64 celdas independientes, 4 núcleos (16 pasos) contra 128 núcleos (1 paso).
sources:
- https://en.wikipedia.org/wiki/CUDA
- https://en.wikipedia.org/wiki/GeForce_8_series
- https://developer.download.nvidia.com/compute/cuda/1.0/NVIDIA_CUDA_Programming_Guide_1.0.pdf
original:
> 23

## Datos, cómputo y redes profundas
layout: image
chart_label: Error top-5 del ganador de ILSVRC (ImageNet)
winner: AlexNet
delta: −10.5 puntos
lead: Tres personas. Dos tarjetas gráficas. Un artículo.
facts:
- Equipo | Alex Krizhevsky, Ilya Sutskever y Geoffrey Hinton{logo:uoft}
- Cómputo | 2 GPU NVIDIA GTX 580 (3 GB) · 5–6 días de entrenamiento
- Artículo | «ImageNet Classification with Deep Convolutional Neural Networks», NeurIPS 2012
sources:
- https://en.wikipedia.org/wiki/AlexNet
- https://arxiv.org/abs/1409.0575
original:
> 24

## La escala del entrenamiento
layout: image
y_axis: Pérdida (escala log)
x_axis: Cómputo de entrenamiento (escala log) →
illustrative: ilustrativo
gpus:
- V100 · 2017
- A100 · 2020
- H100 · 2022
lead: Con las leyes de escalamiento, el cuello de botella pasó a ser el silicio.
paper: Kaplan et al., 2020
paper_text: La pérdida de un modelo de lenguaje baja como una ley de potencia al crecer parámetros, datos y cómputo.
caption: Más cómputo, mejores modelos de forma predecible: la carrera se volvió de GPU.
remark: La gráfica es ilustrativa: muestra la forma de una ley de potencia en escala logarítmica, no datos del artículo.
sources:
- https://arxiv.org/abs/2001.08361
original:
> 25

# Herramientas

## AlphaFold
layout: split
bullets:
- Predicción de estructuras de proteínas.
- AlphaFold destacó en CASP13. AlphaFold 2 destacó en CASP14.
- AlphaFold 2 usa un sistema de redes basado en atención.
lab: Google DeepMind
milestones:
- CASP13 · 2018 | AlphaFold
- CASP14 · 2020 | AlphaFold 2
- 2024 | Nobel de Química: Hassabis y Jumper
sequence_label: Secuencia de aminoácidos (1D)
structure_label: Estructura predicha · tres hélices
confidence_label: Confianza por residuo
confidence_levels:
- Muy alta (> 90)
- Alta (70–90)
- Baja (50–70)
- Muy baja (< 50)
guide:
- Predicción de estructuras de proteínas.
- AlphaFold destacó en CASP13. AlphaFold 2 destacó en CASP14.
- AlphaFold 2 usa un sistema de redes basado en atención.
remark: La secuencia y el plegamiento son ilustrativos; los colores siguen la escala pLDDT que usa AlphaFold para la confianza por residuo.
sources:
- https://deepmind.google/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/
- https://www.nobelprize.org/prizes/chemistry/2024/summary/
- https://alphafold.ebi.ac.uk/faq
original:
> Aplicaciones
>
> AlphaFold usa IA para predecir la estructura de proteínas.
> AlphaFold ganó la competencia CASP13.
> AlphaFold usa una arquitectura de red neuronal llamada transformador para mejorar la precisión.
>
>
> 26

## Modelos de lenguaje
layout: split
bullets:
- Los modelos Transformer aprenden patrones del lenguaje.
- Generan texto a partir del contexto disponible.
- Una respuesta plausible puede contener errores.
context_label: Contexto
context: Las redes neuronales profundas
candidates_label: Siguiente palabra · probabilidad (ilustrativa)
next_words:
- aprenden 52 | son 21 | procesan 14 | requieren 8
- representaciones 47 | patrones 33 | de 11 | a 5
- jerárquicas 41 | útiles 30 | complejas 17 | a 7
hallucination: y fueron inventadas en 2012.
warning: <b>Plausible, pero falso.</b> Las redes neuronales existen desde mediados del siglo XX; 2012 marcó su auge con AlexNet.
guide:
- Los modelos Transformer aprenden patrones del lenguaje.
- Generan texto a partir del contexto disponible.
- Una respuesta plausible puede contener errores.
remark: Las probabilidades son ilustrativas. La última frase es deliberadamente falsa para mostrar una alucinación plausible.
original:
> Aplicaciones
>
> ChatGPT es un modelo de lenguaje que utiliza aprendizaje profundo para generar respuestas en lenguaje natural.
> ChatGPT puede generar respuestas en diferentes idiomas y campos temáticos gracias a su gran cantidad de datos de entrenamiento y su arquitectura de red neuronal profunda.
> ChatGPT utiliza una arquitectura de red neuronal conocida como Transformer, que le permite procesar información de lenguaje natural a través de múltiples capas de atención y generar respuestas coherentes y precisas.
>
>
> 27

## PyTorch
layout: text
bullets:
- Framework de Python para construir y entrenar redes.
- Tensores, diferenciación automática y aceleración con GPU.
- Otras opciones: TensorFlow, JAX y Keras.
alternatives:
- TensorFlow
- JAX
- Keras
code:
```python
import torch
from torch import nn

# usa la GPU si está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
model = nn.Sequential(nn.Linear(3, 16), nn.ReLU(),
                      nn.Linear(16, 1)).to(device)
opt = torch.optim.SGD(model.parameters(), lr=0.1)

x = torch.randn(64, 3, device=device)   # tensores
y = torch.randn(64, 1, device=device)
loss = nn.functional.mse_loss(model(x), y)
loss.backward()    # diferenciación automática
opt.step()         # actualiza los pesos
```
guide:
- Framework de Python para construir y entrenar redes.
- Tensores, diferenciación automática y aceleración con GPU.
- Otras opciones: TensorFlow, JAX y Keras.
original:
> Pytorch
>
> ¿Qué es?
> Pytorch es un “modulo” (en realidad es un framework) de Python que facilita la implementación de redes neuronales y otros algoritmos de ML
> Alternativas
> Theano, Tensorflow, Caffe, MxNet (Apache), CNTK (Microsoft)
>
> 28

## Historia de los frameworks
layout: image
theano: Universidad de Montreal
pytorch: Facebook / Meta → PyTorch Foundation (2022)
tensorflow: Google Brain
keras: François Chollet · Keras 3 (2023): varios backends
mxnet: DMLC →
theano_end: fin del desarrollo · 2017
caffe2: Caffe2 se integra a PyTorch · 2018
mxnet_end: retirado · 2023
today: hoy
legend_active: en desarrollo activo
legend_ended: concluido, integrado o retirado
guide:
- Herramientas y equipos que impulsaron el ecosistema.
remark: Línea de tiempo extendida hasta hoy; la versión original terminaba en 2020.
sources:
- https://en.wikipedia.org/wiki/Theano_(software)
- https://en.wikipedia.org/wiki/Caffe_(software)
- https://en.wikipedia.org/wiki/PyTorch
- https://en.wikipedia.org/wiki/TensorFlow
- https://en.wikipedia.org/wiki/Keras
- https://en.wikipedia.org/wiki/Apache_MXNet
- https://en.wikipedia.org/wiki/JAX_(software)
original:
> 29

## El ecosistema de deep learning
layout: image
cards:
- Theano | MILA, Universidad de Montreal (grupo de Yoshua Bengio) | Pionero: grafos simbólicos y diferenciación automática. | Concluido · 2017
- Caffe → Caffe2 | Yangqing Jia (UC Berkeley) → Facebook | Visión por computadora; Caffe2 para móviles y producción. | Integrado a PyTorch · 2018
- PyTorch | Soumith Chintala y equipo (Facebook AI Research) | Grafo de cómputo dinámico y flexible. | Activo · PyTorch Foundation
- TensorFlow | Jeff Dean, Rajat Monga y Google Brain | Escalable y orientado a producción. | Activo
- MXNet | Tianqi Chen y la comunidad DMLC → Apache | Eficiente y escalable. | Retirado · 2023
- Hoy | Opciones principales | PyTorch, TensorFlow y JAX; Keras 3 funciona sobre los tres. | Este curso: PyTorch
guide:
- Quién creó cada framework y qué aportó.
- Cuál sigue activo hoy.
original:
> 30

## Keras
layout: text
bullets:
- API de alto nivel para definir y entrenar modelos.
- Keras 3 admite backends TensorFlow, JAX y PyTorch.
- En este curso trabajaremos directamente con PyTorch.
api_label: Keras 3 · API de alto nivel
this_course: este curso
code:
```python
import os
os.environ["KERAS_BACKEND"] = "torch"
import keras

model = keras.Sequential([
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(1),
])
model.compile(optimizer="sgd", loss="mse")
```
guide:
- API de alto nivel para definir y entrenar modelos.
- Keras 3 admite backends TensorFlow, JAX y PyTorch.
- En este curso trabajaremos directamente con PyTorch.
sources:
- https://keras.io/keras_3/
- https://keras.io/getting_started/
original:
> Keras
>
> Keras se usa bien cuando usamos algo que no es Pytorch
> Es más generalizable
> Se puede usar ya sea en Python o en R
> La mayoría de los recursos los van a encontrar en Keras
>
> 31

# Redes y entrenamiento

## Redes neuronales
layout: divider
number: 02
question: ¿Cómo ajustamos los parámetros de una red?
guide:
- ¿Cómo ajustamos los parámetros de una red?
original:
> Redes Neuronales
>
>
>
> 32

## Ingeniería de características
layout: text
manual_label: Feature engineering
learned_label: Representation learning
data: Datos
model: Modelo
manual_tag: a mano
manual_text: Una persona experta diseña las características
layers:
- Capa 1 | bordes
- Capa 2 | formas
- Capa 3 | partes
learned_note: representaciones aprendidas a partir de los datos
bullets:
- <b>Feature engineering:</b> diseñar características con conocimiento del problema.
- <b>Representation learning:</b> aprender la representación a partir de datos.
- Las redes profundas pueden aprender varias transformaciones sucesivas.
guide:
- Feature engineering: diseñar características con conocimiento del problema.
- Representation learning: aprender la representación a partir de datos.
- Las redes profundas pueden aprender varias transformaciones sucesivas.
original:
> Feature Engineering
>
> Al área de ML encargada de estudiar como representar los datos para que un algoritmo funcione se llama Representation Learning.
>
> 33

## El perceptrón
layout: split
lead: Combina entradas con pesos y un término de sesgo.
formula: z = Σ<sub>i</sub> w<sub>i</sub>x<sub>i</sub> + b
example_label: Ejemplo
example_1: z = 0.5 × 0.8 + (−1.0) × 0.2 + 2.0 × (−0.4) + 0.1
example_2: z = 0.4 − 0.2 − 0.8 + 0.1 = <b class="g-t">−0.5</b>
guide:
- Combina entradas con pesos y un término de sesgo.
- z = Σᵢ wᵢxᵢ + b
original:
> Perceptron
>
> 34

## La función de activación
layout: split
sigmoid_label: Sigmoide <span class="nt m">σ(z)</span>
bullets:
- La activación transforma la combinación de entradas.
- Una función no lineal permite aprender relaciones no lineales.
- <span class="m">h = f(z)</span>
guide:
- La activación transforma la combinación de entradas.
- Una función no lineal permite aprender relaciones no lineales.
- h = f(z)
original:
> 35
>
> f es llamada la función de activación y la utilizamos para discretizar las entradas del perceptron.
>
> Una de las funciones de activación más usadas es:

## Funciones de activación
layout: image
functions:
- Sigmoide | σ(x) = <span class="frac"><span>1</span><span>1 + e<sup>−x</sup></span></span> | Salida en (0, 1)
- tanh | <span class="u">tanh</span>(x) | Salida en (−1, 1)
- ReLU | <span class="u">max</span>(0, x) | Salida en [0, ∞)
- Leaky ReLU | <span class="u">max</span>(0.1x, x) | Pendiente 0.1 si x < 0
- Maxout | <span class="u">max</span>(w<sub>1</sub><sup>T</sup>x + b<sub>1</sub>, w<sub>2</sub><sup>T</sup>x + b<sub>2</sub>) | Aprende la forma (ejemplo)
- ELU | <span class="pw2">{</span><span class="cases"><span>x, &nbsp;x ≥ 0</span><span>α(e<sup>x</sup> − 1), &nbsp;x &lt; 0</span></span> | Suave si x < 0 · α = 1
caption: La elección afecta la señal y los gradientes.
guide:
- La elección afecta la señal y los gradientes.
original:
> Funciones de activación
>
> 36

## Una red de neuronas
layout: split
layers:
- Capa L<sub>1</sub> · entrada
- Capa L<sub>2</sub> · oculta
- Capa L<sub>3</sub> · salida
bullets:
- Las salidas de una capa alimentan a la siguiente.
- Cada capa transforma la representación.
formula_1: a<sup>(2)</sup> = f(W<sup>(1)</sup>x + b<sup>(1)</sup>)
formula_2: h<sub>W,b</sub>(x) = f(W<sup>(2)</sup>a<sup>(2)</sup> + b<sup>(2)</sup>)
guide:
- Las salidas de una capa alimentan a la siguiente.
- Cada capa transforma la representación.
original:
> Una Red Neuronal va a ser un conjunto de perceptrones interconectados uno con el otro.
>
> 37

## Backpropagation
layout: divider
number: 03
question: ¿Cómo contribuye cada parámetro al error?
guide:
- ¿Cómo contribuye cada parámetro al error?
original:
> ¿Qué es backpropagation?
>
> 38

## El ciclo de entrenamiento
layout: agenda
steps:
- Calcular una predicción | pred = model(x)
- Medir la pérdida | loss = loss_fn(pred, y)
- Calcular gradientes con la regla de la cadena | loss.backward()
- Actualizar parámetros con el optimizador | opt.step(); opt.zero_grad()
loss_label: Pérdida por iteración (ilustrativa)
iteration_label: iteración
guide:
- 1. Calcular una predicción.
- 2. Medir la pérdida.
- 3. Calcular gradientes con la regla de la cadena.
- 4. Actualizar parámetros con el optimizador.
remark: Los valores de pérdida por iteración son ilustrativos.
original:
> 39
>
> Para entrenar redes neuronales usamos Error Backpropagation.
> Encontramos el error
> Vamos hacia atras viendo cuanta culpa tiene cada unidad
> Calculamos la derivada de ese error, y despues utilizamos Gradiente Descendente.

## El gradiente en cada capa
layout: split
bullets:
- Backpropagation calcula derivadas de la pérdida.
- δ representa una señal de error local.
- El optimizador usa esos gradientes para actualizar los pesos.
formula_1: δ<sup>(2)</sup> = ((W<sup>(2)</sup>)<sup>T</sup> δ<sup>(3)</sup>) ⊙ f′(z<sup>(2)</sup>)
formula_2: ∂J / ∂W<sup>(l)</sup> = δ<sup>(l+1)</sup> (a<sup>(l)</sup>)<sup>T</sup>
formula_3: W ← W − η ∂J / ∂W
compare_note: comparar con<br>la etiqueta <span class="m">y</span>
guide:
- Backpropagation calcula derivadas de la pérdida.
- δ representa una señal de error local.
- El optimizador usa esos gradientes para actualizar los pesos.
sources:
- http://ufldl.stanford.edu/tutorial/supervised/MultiLayerNeuralNetworks/
original:
> 40
>
> Evaluamos los errores en los nodos centrales (δ)
>
>
>
> Labels
>
>
>
> δ

## Una analogía organizacional
layout: gallery
roles:
- Dirección general
- Dir. de Riesgos
- Dir. de Operaciones
- Dir. de Sucursales
- Director Zona Centro
- Gerente Sucursal Centro
- Cajera A
formula_label: Contribución de cada nivel (ilustrativa)
formula_text: contribución = contribución del jefe × influencia local
formula_example: Cajera A: 1.0 × 0.5 × 0.8 × 0.5 × 0.25 = 0.05
bullets:
- El resultado depende de decisiones en distintos niveles.
- La analogía ayuda a pensar en contribuciones locales.
- En una red, la contribución se calcula con derivadas.
guide:
- El resultado depende de decisiones en distintos niveles.
- La analogía ayuda a pensar en contribuciones locales.
- En una red, la contribución se calcula con derivadas.
remark: Los porcentajes de responsabilidad son ilustrativos. La versión original usaba fotografías y logotipos de un grupo empresarial; aquí se conserva solo el organigrama.
original:
> 41
>
> Director de Riesgos
>
> Director de Operaciones
>
> Director de Sucursales
>
> Gerente Sucursal Centro
>
> Director Zona Centro
>
> Cajera A

## Gradientes que se desvanecen
layout: text
chart_label: Magnitud del gradiente por capa · sigmoide: <span class="nt m">f′(z) ≤ 0.25</span>, pesos ≈ 1
layer_label: capa
direction_note: la señal de error viaja de la salida hacia la entrada
slow_note: aprenden muy lentamente
remedies:
- ReLU y variantes
- Inicialización cuidadosa
- Conexiones residuales
bullets:
- La multiplicación de derivadas pequeñas puede reducir el gradiente.
- Las primeras capas pueden aprender muy lentamente.
- Activaciones, inicialización y conexiones residuales ayudan a mitigarlo.
- El problema puede persistir: no desapareció por completo.
guide:
- La multiplicación de derivadas pequeñas puede reducir el gradiente.
- Las primeras capas pueden aprender muy lentamente.
- Activaciones, inicialización y conexiones residuales ayudan a mitigarlo.
- El problema puede persistir: no desapareció por completo.
sources:
- https://arxiv.org/abs/1801.03744
- https://arxiv.org/abs/1511.07289
original:
> 42
>
> Un gran problema es que si los δ son chicos, se van a ir hacienda mas chicos.
> Si tenemos muchas capas, vamos a terminar con errores muy chicos..
> Gradiente Descendente depende de esos errores.
> La explosion de DL se dio cuando ese problema dejo de existir..

## Redes convolucionales
layout: split
image_label: imagen 6×6
filter_label: filtro 3×3
map_label: mapa de activación 4×4
shared_note: el mismo filtro<br>(9 pesos) recorre<br>toda la imagen
vgg_label: VGG-16: 13 capas convolucionales + 3 totalmente conectadas
bullets:
- Filtros que detectan patrones locales en imágenes.
- Comparten pesos y aprovechan la estructura espacial.
- Una arquitectura importante para visión.
legend_conv: convolución + ReLU
legend_pool: max pooling
legend_fc: totalmente conectada
guide:
- Filtros que detectan patrones locales en imágenes.
- Comparten pesos y aprovechan la estructura espacial.
- Una arquitectura importante para visión.
remark: El ejemplo numérico es el clásico detector de bordes verticales: una imagen 6×6 (10 = claro, 0 = oscuro) convolucionada con un filtro 3×3.
sources:
- https://arxiv.org/abs/1409.1556
original:
> Redes Convolucionales
>
> 43
>
> Se diseñan exprofeso para el procesamiento de imágenes.
>
> Son una de las arquitectura mas usadas y el estado del arte.
>
> Tienen muchas ventajas que iremos viendo.

## Redes recurrentes
layout: split
inputs:
- Me
- gusta
- el
- curso
outputs:
- gusta
- el
- curso
- .
formula: h<sub>t</sub> = tanh(W<sub>x</sub>x<sub>t</sub> + W<sub>h</sub>h<sub>t−1</sub> + b)
bullets:
- Procesan secuencias mediante un estado que se actualiza.
- Aplicaciones en series de tiempo y otros datos secuenciales.
- Los Transformers ocupan un papel central en el lenguaje actual.
uses:
- series de tiempo
- texto
- audio
- sensores
guide:
- Procesan secuencias mediante un estado que se actualiza.
- Aplicaciones en series de tiempo y otros datos secuenciales.
- Los Transformers ocupan un papel central en el lenguaje actual.
original:
> Redes Recurrentes
>
> 44
>
> Son diseñadas para secuencias
>
> Son muy útiles para series de tiempo
>
> Hoy en día son muy usadas para texto.
