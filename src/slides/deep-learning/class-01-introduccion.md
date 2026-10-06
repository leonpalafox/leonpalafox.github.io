---
title: Deep Learning · Clase 1 · Universidad Panamericana
footer: Deep Learning · Dr. León Palafox
pdf: /slides/deep-learning/class-01-introduccion.pdf
credits:
> Texto: UPDL2024_1_Intro.pptx, material aportado por el profesor. Las ilustraciones originales se rehicieron como animaciones en HTML.
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
hint: Da clic en una línea para escribir. Se guarda en este navegador.
original:
> Anuncios
>
>
>
> 2

## Objetivos de la sesión
layout: text
lead: Al terminar la clase deberían poder:
objectives:
- Explicar | cómo una red aprende representaciones.
- Distinguir | qué hace la función de pérdida y qué hace el optimizador.
- Implementar y validar | una red en PyTorch.
guide:
- Explicar cómo una red aprende representaciones.
- Distinguir qué hace la función de pérdida y qué hace el optimizador.
- Implementar y validar una red en PyTorch.
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
caption: Cada clase tiene una parte de teoría y una de práctica. En la práctica revisamos casos reales: dónde funcionan los algoritmos y dónde fallan.
guide:
- Teoría: la intuición, cómo funciona y dónde deja de funcionar.
- Práctica: implementarlo, evaluarlo e interpretar los resultados.
- Casos de uso: dónde falla y dónde sirve.
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
- Escojan un problema concreto.
- Entrenen un modelo para resolverlo.
- Midan qué tan bien funciona.
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
- Un problema concreto, un modelo y una forma honesta de medirlo.
remark: Las nueve ideas vienen de la ilustración del material original; son proyectos típicos de cursos de deep learning.
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
- ¿A qué clase pertenece cada observación?
- ¿Dónde se atora nuestro clasificador?
- ¿Y si cambiamos cómo representamos los datos?
guide:
- ¿A qué clase pertenece cada observación?
- ¿Dónde se atora nuestro clasificador?
- ¿Y si cambiamos cómo representamos los datos?
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
lead: Con las coordenadas originales, una línea recta no alcanza.
class_a: Clase A
class_b: Clase B
result: No hay recta que separe el centro del anillo.
guide:
- Con las coordenadas originales, una línea recta no alcanza.
original:
> Por que es necesario el Deep Learning
>
> 11

## El mismo dato, otras coordenadas
layout: split
lead: Si usamos el radio, los círculos concéntricos se separan solos.
formula_r: r = √(x² + y²)
formula_theta: θ = atan2(y, x)
result: Una recta vertical, <span class="m">r</span> = 0.48, separa las clases.
guide:
- Si usamos el radio, los círculos concéntricos se separan solos.
original:
> 12
>
> Muchos problemas de integración se vuelven más fáciles al momento de usar polares.

## Clasificación y características
layout: text
bullets:
- Las características (features) describen al dato: píxeles, palabras, medidas.
- Con la representación original, a veces las clases no se pueden separar.
- Si transformamos los datos, clasificar se vuelve más fácil.
vector_label: Una observación → un vector de características
vector_rows:
- Imagen | píxeles | x = [0.12, 0.80, 0.33, …]
- Texto | conteo de palabras | x = [0, 2, 1, 0, …]
- Sensor | medidas | x = [36.8, 72, 1.2, …]
initial_label: Representación inicial
transformed_label: Después de una transformación <span class="nt m">φ(x)</span>
threshold_note: basta con un umbral
guide:
- Las características (features) describen al dato: píxeles, palabras, medidas.
- Con la representación original, a veces las clases no se pueden separar.
- Si transformamos los datos, clasificar se vuelve más fácil.
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
caption: Encuentran cosas simples, como bordes, esquinas y contornos, en cualquier parte de la imagen.
guide:
- Las primeras capas detectan patrones locales.
original:
> Clasificación
>
> 14

## La combinación de patrones
layout: split
lead: Las capas siguientes juntan esos rasgos hasta reconocer la clase.
caption: Bordes → esquinas → partes (ojo, oreja) → <b>persona</b>. Cada capa trabaja con lo que encontró la anterior.
guide:
- Las capas siguientes juntan esos rasgos hasta reconocer la clase.
remark: Las probabilidades de salida son inventadas, solo para ilustrar.
original:
> Clasificación
>
> 15
>
> Al final es la combinación de esas capas de abstracción las que permiten al clasificador identificar la clase del dato.

## IA, machine learning y deep learning
layout: split
lead: Deep learning es un tipo de machine learning.
formula: DL ⊂ RL ⊂ ML ⊂ IA
caption: De afuera hacia adentro: aprender de los datos, aprender también la representación, y hacerlo con muchas capas.
circles:
- Inteligencia artificial | Ej.: bases de conocimiento
- Machine learning | Ej.: regresión logística
- Aprendizaje de<br>representaciones | Ej.: autoencoders superficiales
- Deep learning | Ej.: MLP
guide:
- Deep learning es un tipo de machine learning.
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
units_text: Cada una hace un cálculo con sus parámetros:
units_formula: h = f(w<sup>T</sup>x + b)
learning: Formas de aprendizaje
learning_kinds:
- Supervisado | pares (x, y) etiquetados
- Autosupervisado | la etiqueta sale del mismo dato
- Por refuerzo | recompensas de un entorno
guide:
- Redes neuronales profundas: modelos con varias capas.
- Neuronas o unidades: cada una hace un cálculo con sus parámetros.
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
advantage_1: La red aprende las características; ya no hay que diseñarlas a mano.
advantage_2: Las GPU hacen muy rápido todo lo que se puede paralelizar.
needs_label: Lo que sigue haciendo falta
needs:
- Datos
- Cómputo
- Evaluación
caption: Aunque la red aprenda la representación, igual hay que conseguir datos, pagar el cómputo y validar el modelo.
guide:
- La red aprende las características; ya no hay que diseñarlas a mano.
- Las GPU hacen muy rápido todo lo que se puede paralelizar.
- Igual hacen falta datos, cómputo y validación.
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
lead: Programamos en Python.
lead_2: Corremos en nuestra máquina o en la nube.
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
- Programamos en Python y corremos en nuestra máquina o en la nube.
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
message: Que algo esté de moda no quiere decir que funcione.
footnote: Posiciones según Gartner, <i>Hype Cycle for Artificial Intelligence, 2025</i> (junio de 2025). Selección de tecnologías.
guide:
- Que algo esté de moda no quiere decir que funcione. Hay que validarlo.
remark: Las posiciones vienen de la gráfica de Gartner «Hype Cycle for Artificial Intelligence, 2025» (junio de 2025). Escogí seis tecnologías.
sources:
- https://www.gartner.com/en/newsroom/press-releases/2025-08-05-gartner-hype-cycle-identifies-top-ai-innovations-in-2025
original:
> 21

## GPU: el origen gráfico
layout: image
lead: Las GPU se hicieron para dibujar gráficos.
timeline:
- 1993 | {logo:nvidia} se funda.
- 1998 | 3dfx Voodoo2 populariza la aceleración 3D en PC.
- 1999 | GeForce 256: NVIDIA la presenta como «la primera GPU».
caption_left: En ese entonces nadie las usaba para multiplicar matrices.
gpu_label: Lo que hace la GPU: calcular cada píxel muy rápido
frame_label: fotograma
caption_right: Cada píxel se calcula por separado, así que miles de cálculos iguales corren en paralelo.
remark: En lugar de la caricatura del material original, aquí hay una cuadrícula de píxeles que se recalculan todos a la vez en cada cuadro.
sources:
- https://blogs.nvidia.com/blog/first-gpu-gaming-ai/
- https://en.wikipedia.org/wiki/GeForce_256
original:
> 22

## Cómputo paralelo y CUDA
layout: image
lead: NVIDIA abrió sus tarjetas de video para hacer cálculo científico.
timeline:
- 2006 | Sale la GeForce 8800 GTX, con 128 núcleos programables.
- 2007 | Sale CUDA y la GPU se puede programar para cualquier cálculo.
-  | Detrás de CUDA estaban Ian Buck (venía de Stanford) y John Nickolls.
formula: <span class="m">C = A × B</span> · cada celda <span class="m">C<sub>ij</sub> = Σ<sub>k</sub> A<sub>ik</sub>B<sub>kj</sub></span> es independiente
cpu_label: CPU · 4 núcleos
gpu_label: GPU · 128 núcleos
steps_label: pasos:
caption: La misma multiplicación: 16 pasos en CPU, 1 en GPU.
remark: La comparación CPU contra GPU está simplificada: 64 celdas independientes, 4 núcleos (16 pasos) contra 128 núcleos (1 paso).
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
lead: Lo hicieron tres personas con dos tarjetas de video.
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
lead: Con las leyes de escalamiento, lo que limita es cuántas GPU tienes.
paper: Kaplan et al., 2020
paper_text: Al crecer los parámetros, los datos y el cómputo, la pérdida de un modelo de lenguaje baja siguiendo una ley de potencia.
caption: Si más cómputo da mejores modelos de forma predecible, todos quieren más GPU.
remark: La gráfica solo muestra la forma de una ley de potencia en escala logarítmica; no son datos del artículo.
sources:
- https://arxiv.org/abs/2001.08361
original:
> 25

# Herramientas

## AlphaFold
layout: split
bullets:
- Predice cómo se pliega una proteína.
- AlphaFold quedó primero en CASP13 y AlphaFold 2 en CASP14.
- AlphaFold 2 se basa en mecanismos de atención.
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
- Predice cómo se pliega una proteína.
- AlphaFold quedó primero en CASP13 y AlphaFold 2 en CASP14.
- AlphaFold 2 se basa en mecanismos de atención.
remark: La secuencia y el plegamiento son de ejemplo. Los colores siguen la escala pLDDT que usa AlphaFold para la confianza de cada residuo.
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
- Un Transformer aprende cómo se usa el lenguaje.
- Genera texto palabra por palabra a partir del contexto.
- Que suene bien no quiere decir que sea cierto.
context_label: Contexto
context: Las redes neuronales profundas
candidates_label: Siguiente palabra · probabilidad (ilustrativa)
next_words:
- aprenden 52 | son 21 | procesan 14 | requieren 8
- representaciones 47 | patrones 33 | de 11 | a 5
- jerárquicas 41 | útiles 30 | complejas 17 | a 7
hallucination: y fueron inventadas en 2012.
warning: <b>Suena bien, pero es falso.</b> Las redes neuronales existen desde finales de los cincuenta; en 2012, con AlexNet, fue cuando despegaron.
guide:
- Un Transformer aprende cómo se usa el lenguaje.
- Genera texto palabra por palabra a partir del contexto.
- Que suene bien no quiere decir que sea cierto.
remark: Las probabilidades son inventadas. La última frase es falsa a propósito, para mostrar cómo se ve una alucinación.
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
- Librería de Python para construir y entrenar redes.
- Trae tensores, derivadas automáticas y soporte para GPU.
- También existen TensorFlow, JAX y Keras.
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
- Librería de Python para construir y entrenar redes.
- Trae tensores, derivadas automáticas y soporte para GPU.
- También existen TensorFlow, JAX y Keras.
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
- Quién hizo cada herramienta y cuándo.
remark: La versión original llegaba hasta 2020; aquí está actualizada.
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
- Theano | MILA, Universidad de Montreal (grupo de Yoshua Bengio) | De los primeros: grafos simbólicos y derivadas automáticas. | Concluido · 2017
- Caffe → Caffe2 | Yangqing Jia (UC Berkeley) → Facebook | Visión por computadora; Caffe2 para móviles y producción. | Integrado a PyTorch · 2018
- PyTorch | Soumith Chintala y equipo (Facebook AI Research) | El grafo se arma mientras corre el código. | Activo · PyTorch Foundation
- TensorFlow | Jeff Dean, Rajat Monga y Google Brain | Pensado para producción a gran escala. | Activo
- MXNet | Tianqi Chen y la comunidad DMLC → Apache | Rápido y fácil de distribuir en varias máquinas. | Retirado · 2023
- Hoy | Opciones principales | PyTorch, TensorFlow y JAX; Keras 3 funciona sobre los tres. | Este curso: PyTorch
guide:
- Quién hizo cada framework y qué aportó.
- Cuál sigue activo hoy.
original:
> 30

## Keras
layout: text
bullets:
- Una API sencilla para armar y entrenar modelos.
- Keras 3 corre sobre TensorFlow, JAX o PyTorch.
- En el curso vamos a usar PyTorch directamente.
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
- Una API sencilla para armar y entrenar modelos.
- Keras 3 corre sobre TensorFlow, JAX o PyTorch.
- En el curso vamos a usar PyTorch directamente.
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
manual_text: Alguien que conoce el problema diseña las características
layers:
- Capa 1 | bordes
- Capa 2 | formas
- Capa 3 | partes
learned_note: la red aprende estas representaciones de los datos
bullets:
- <b>Feature engineering:</b> nosotros diseñamos las características.
- <b>Representation learning:</b> el modelo las aprende de los datos.
- Una red profunda aprende varias transformaciones, una tras otra.
guide:
- Feature engineering: nosotros diseñamos las características.
- Representation learning: el modelo las aprende de los datos.
- Una red profunda aprende varias transformaciones, una tras otra.
original:
> Feature Engineering
>
> Al área de ML encargada de estudiar como representar los datos para que un algoritmo funcione se llama Representation Learning.
>
> 33

## El perceptrón
layout: split
lead: Multiplica cada entrada por un peso, suma todo y agrega un sesgo.
formula: z = Σ<sub>i</sub> w<sub>i</sub>x<sub>i</sub> + b
example_label: Ejemplo
example_1: z = 0.5 × 0.8 + (−1.0) × 0.2 + 2.0 × (−0.4) + 0.1
example_2: z = 0.4 − 0.2 − 0.8 + 0.1 = <b class="g-t">−0.5</b>
guide:
- Multiplica cada entrada por un peso, suma todo y agrega un sesgo.
- z = Σᵢ wᵢxᵢ + b
original:
> Perceptron
>
> 34

## La función de activación
layout: split
sigmoid_label: Sigmoide <span class="nt m">σ(z)</span>
bullets:
- A esa suma se le aplica la función de activación.
- Si la función es no lineal, la red puede aprender relaciones no lineales.
- <span class="m">h = f(z)</span>
guide:
- A esa suma se le aplica la función de activación.
- Si la función es no lineal, la red puede aprender relaciones no lineales.
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
caption: La que escojan cambia cómo pasan la señal y los gradientes.
guide:
- La que escojan cambia cómo pasan la señal y los gradientes.
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
- La salida de una capa es la entrada de la siguiente.
- Cada capa cambia un poco más la representación.
formula_1: a<sup>(2)</sup> = f(W<sup>(1)</sup>x + b<sup>(1)</sup>)
formula_2: h<sub>W,b</sub>(x) = f(W<sup>(2)</sup>a<sup>(2)</sup> + b<sup>(2)</sup>)
guide:
- La salida de una capa es la entrada de la siguiente.
- Cada capa cambia un poco más la representación.
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
remark: Los valores de pérdida son inventados.
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
- Backpropagation calcula la derivada de la pérdida respecto a cada peso.
- δ es el error que le toca a cada neurona.
- Con esos gradientes, el optimizador actualiza los pesos.
formula_1: δ<sup>(2)</sup> = ((W<sup>(2)</sup>)<sup>T</sup> δ<sup>(3)</sup>) ⊙ f′(z<sup>(2)</sup>)
formula_2: ∂J / ∂W<sup>(l)</sup> = δ<sup>(l+1)</sup> (a<sup>(l)</sup>)<sup>T</sup>
formula_3: W ← W − η ∂J / ∂W
compare_note: comparar con<br>la etiqueta <span class="m">y</span>
guide:
- Backpropagation calcula la derivada de la pérdida respecto a cada peso.
- δ es el error que le toca a cada neurona.
- Con esos gradientes, el optimizador actualiza los pesos.
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
formula_label: Culpa de cada nivel (números de ejemplo)
formula_text: culpa = culpa del jefe × influencia propia
formula_example: Cajera A: 1.0 × 0.5 × 0.8 × 0.5 × 0.25 = 0.05
bullets:
- Un mal resultado viene de decisiones en varios niveles.
- La pregunta es cuánta culpa le toca a cada quien.
- En una red, esa culpa se calcula con derivadas.
guide:
- Un mal resultado viene de decisiones en varios niveles.
- La pregunta es cuánta culpa le toca a cada quien.
- En una red, esa culpa se calcula con derivadas.
remark: Los números son inventados. El material original tenía fotos y logos de una empresa; aquí solo queda el organigrama.
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
- Si multiplicas muchas derivadas pequeñas, el gradiente se va a casi cero.
- Las primeras capas casi no aprenden.
- ReLU, una buena inicialización y las conexiones residuales ayudan.
- Aun así, el problema no ha desaparecido del todo.
guide:
- Si multiplicas muchas derivadas pequeñas, el gradiente se va a casi cero.
- Las primeras capas casi no aprenden.
- ReLU, una buena inicialización y las conexiones residuales ayudan.
- Aun así, el problema no ha desaparecido del todo.
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
- Usan filtros que buscan patrones pequeños en la imagen.
- El mismo filtro recorre toda la imagen, así que hay pocos pesos.
- Durante años fueron la arquitectura estándar en visión.
legend_conv: convolución + ReLU
legend_pool: max pooling
legend_fc: totalmente conectada
guide:
- Usan filtros que buscan patrones pequeños en la imagen.
- El mismo filtro recorre toda la imagen, así que hay pocos pesos.
- Durante años fueron la arquitectura estándar en visión.
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
- Leen una secuencia paso a paso y van guardando un estado.
- Sirven para series de tiempo y cualquier dato que venga en orden.
- Para texto, hoy se usan más los Transformers.
uses:
- series de tiempo
- texto
- audio
- sensores
guide:
- Leen una secuencia paso a paso y van guardando un estado.
- Sirven para series de tiempo y cualquier dato que venga en orden.
- Para texto, hoy se usan más los Transformers.
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
