---
title: "Qué pasó con los frameworks de deep learning"
description: "De Theano a PyTorch: qué pasó con cinco frameworks de deep learning, quién los mantuvo y cómo llegaron a 2026."
pubDate: 2026-10-04
lang: es
tags: ["deep-learning", "codigo-abierto", "historia", "datos"]
---

Cuando elegimos un framework para entrenar un modelo, normalmente nos fijamos en qué tan fácil es usarlo, si funciona con nuestras GPU y cuántos ejemplos hay disponibles. Es comprensible: queremos que el modelo corra. El problema aparece unos años después, cuando necesitamos actualizarlo y descubrimos que el equipo que mantenía la herramienta ya está trabajando en otra cosa.

La historia de Theano, Caffe, Caffe2, PyTorch, TensorFlow y MXNet tiene bastante de eso. En menos de veinte años hubo proyectos que salieron de universidades, otros que nacieron dentro de empresas y algunos que acabaron en fundaciones. Unos siguen publicando versiones; de otros quedan el código, la documentación y las aplicaciones que todavía dependen de ellos.

Me interesa esa parte de la historia porque mantener un framework es un compromiso mucho más largo que publicar un modelo. La [gráfica de arriba](#grafica) reúne esas trayectorias desde 2007, con información revisada al **4 de octubre de 2026**.

<nav class="toc" aria-label="Contenido">
  <details>
    <summary>
      <span class="toc-kicker">Contenido</span>
      <span class="toc-count">5 secciones</span>
    </summary>
    <ol>
      <li><a href="#cronologia"><span class="toc-n">01</span><span class="toc-t">Cómo leer la gráfica</span><span class="toc-d">Fechas, responsables y proyectos derivados</span></a></li>
      <li><a href="#patron"><span class="toc-n">02</span><span class="toc-t">El trabajo de mantenerlo</span><span class="toc-d">Lo que viene después del lanzamiento</span></a></li>
      <li><a href="#filas"><span class="toc-n">03</span><span class="toc-t">Qué pasó con cada framework</span><span class="toc-d">Qué fue cada framework y qué le pasó</span></a></li>
      <li><a href="#excepcion"><span class="toc-n">04</span><span class="toc-t">Qué puede hacer una fundación</span><span class="toc-d">PyTorch y MXNet: gobernanza y continuidad</span></a></li>
      <li><a href="#leer"><span class="toc-n">05</span><span class="toc-t">Elegir una herramienta que dure</span><span class="toc-d">Y por qué importa si estás eligiendo infraestructura</span></a></li>
    </ol>
  </details>
</nav>

<style>
  .frameworks-sources-table { overflow-x: auto; }
  .frameworks-sources-table:focus-visible { outline: 2px solid #c2472f; }
  .toc {
    margin: 32px 0;
    border: 1px solid #e0dcd4; border-radius: 2px;
    background: #fbfaf7; padding: 0 22px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  .toc a { text-decoration: none; color: #0a0a0a; }
  .toc summary {
    display: flex; align-items: baseline; gap: 10px;
    padding: 14px 0; cursor: pointer; list-style: none; min-height: 44px;
  }
  .toc summary::-webkit-details-marker { display: none; }
  .toc summary:hover .toc-kicker { color: #c2472f; }
  .toc summary::after {
    content: "+"; font-size: 15px; line-height: 1; color: #6b6b6b;
    margin-left: 10px; transition: color 140ms ease-out;
  }
  .toc details[open] summary::after { content: "\2212"; }
  .toc details[open] summary { border-bottom: 1px solid #e0dcd4; }
  .toc-kicker {
    font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase;
    color: #0a0a0a; font-weight: 600; transition: color 140ms ease-out;
  }
  .toc-count { font-size: 11px; color: #6b6b6b; margin-left: auto; }
  .toc ol { list-style: none; margin: 4px 0 0; padding: 0 0 14px; }
  .toc li { margin: 0; border-bottom: 1px solid #ece8e0; }
  .toc li:last-child { border-bottom: 0; }
  .toc li a { display: grid; grid-template-columns: 32px 1fr; gap: 0 10px; padding: 10px 0; }
  .toc li a:hover { color: #c2472f; }
  .toc li a:hover .toc-t { text-decoration: underline; text-underline-offset: 3px; }
  .toc-n {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px; color: #6b6b6b; padding-top: 3px;
  }
  .toc-t { font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
  .toc-d { grid-column: 2; font-size: 12.5px; color: #6b6b6b; margin-top: 2px; }
  @media (max-width: 560px) { .toc { padding: 0 16px; } .toc-t { font-size: 14px; } }
</style>

<a id="cronologia"></a>

## 01 · Cómo leer la gráfica

Cada color corresponde a un framework y cada tramo lleva el nombre de su responsable principal o del estado en que quedó. Puedes seleccionar una barra para ver las fechas y el detalle de lo que ocurrió. Los cuadros punteados son los años anteriores a su publicación.

Hay dos filas que conviene leer con cuidado. Caffe y Caffe2 comparten una porque están relacionados, aunque fueron proyectos distintos. La de Theano incluye sus derivados, hasta llegar a PyTensor. En ambos casos, agruparlos permite seguir la historia del código y de las personas que lo mantuvieron.

[Volver a la gráfica ↑](#grafica)

<a id="patron"></a>

## 02 · El trabajo de mantenerlo

Theano comenzó en 2007; Caffe se publicó en 2013; TensorFlow y MXNet aparecieron en 2015. PyTorch llegó al público en enero de 2017 y Caffe2 en abril de ese año. En una década se habían acumulado varias formas de resolver un problema parecido: permitir que un investigador entrenara redes neuronales sin escribir por su cuenta todo el código para ejecutarlas.

Después del lanzamiento empieza un trabajo menos visible. Sale una GPU nueva y hay que hacerla funcionar. Cambia Python y algo deja de instalarse. Un usuario encuentra un error que solo ocurre con cierta combinación de bibliotecas. Hay que reproducirlo, corregirlo y explicar qué cambió. Todo eso requiere gente que conozca el proyecto y tenga tiempo para atenderlo.

Ahí me parece que se entiende mejor el peso que adquirieron las empresas. Tienen equipos que necesitan usar estas herramientas y razones para pagar por su mantenimiento. Para un laboratorio, sostener ese esfuerzo durante años puede competir con el trabajo de investigación que le permite conseguir el siguiente financiamiento. Eso ayuda a explicar algunas de estas trayectorias, aunque cada proyecto tuvo sus propias dificultades.

<a id="filas"></a>

## 03 · Qué pasó con cada framework

### Theano: la historia siguió en PyTensor

Theano salió del grupo de investigación de Montréal. Permitía escribir expresiones matemáticas como un grafo simbólico y convertirlas en código eficiente para CPU y GPU. Buena parte del trabajo consistía en describir el cálculo y dejar que Theano decidiera cómo ejecutarlo.

El **28 de septiembre de 2017**, MILA [anunció que dejaría el desarrollo principal](https://groups.google.com/g/theano-announce/c/PiH4p7NqZ60) después de la versión 1.0. Esa versión [se publicó el 15 de noviembre](https://github.com/Theano/Theano/blob/master/HISTORY.txt). Hubo mantenimiento y versiones posteriores, pero el equipo estaba cerrando esa etapa.

Para quienes dependían de Theano, el anuncio dejaba una tarea pendiente. Los desarrolladores de PyMC tomaron una copia del proyecto en 2020 y la [renombraron Aesara en 2021](https://www.pymc.io/about/history.html). Más adelante surgieron diferencias sobre la dirección técnica y la forma de tomar decisiones. El 28 de noviembre de 2022, PyMC [anunció un nuevo fork: PyTensor](https://www.pymc.io/blog/pytensor_announcement.html).

Esa rama sigue trabajando en 2026. En mayo se anunciaron [PyMC 6.0 y PyTensor 3.0](https://www.pymc.io/blog/pymc_v6_ecosystem_updates.html), y el 2 de octubre apareció [PyTensor 3.3.3](https://github.com/pymc-devs/pytensor/releases/tag/rel-3.3.3). El [repositorio original de Theano](https://github.com/Theano/Theano) también remite a esa continuación. Su herencia encontró un lugar en la computación simbólica y probabilística que utiliza PyMC; el proyecto original quedó atrás.

### Caffe y Caffe2: de Berkeley a la integración con PyTorch

[Caffe nació en Berkeley](https://caffe.berkeleyvision.org/), con Yangqing Jia y la comunidad de BVLC. Una de sus ventajas era muy práctica: la arquitectura del modelo se podía definir en archivos de configuración. Compartir esos archivos y los pesos facilitaba que otro investigador reprodujera una red.

Facebook presentó Caffe2 en abril de 2017, con una orientación que incluía el despliegue móvil y el entrenamiento distribuido. Al mismo tiempo, la [versión 1.0 del Caffe original](https://github.com/BVLC/caffe/releases/tag/1.0) anunciaba el paso a modo de mantenimiento. Esa sigue siendo la última versión publicada en su repositorio.

Caffe2 tuvo una vida independiente bastante corta. El **2 de mayo de 2018** se [anunció su integración con PyTorch](https://caffe2.ai/blog/2018/05/02/Caffe2_PyTorch_1_0.html) para reunir las herramientas de investigación y producción en PyTorch 1.0.

Años después llegó una ruptura que importa si todavía tienes código viejo: el **15 de mayo de 2024** se incorporó la [eliminación del código Python de Caffe2](https://github.com/pytorch/pytorch/pull/126035) del repositorio de PyTorch. La documentación histórica puede hablar de aquella integración, pero ya no puedes dar por hecho que un programa que importa `caffe2.python` funcionará con una instalación moderna. El cambio se refiere a esa API; parte de la herencia en C++ es otra historia.

### PyTorch: una fundación y bastante más que grafos dinámicos

PyTorch se publicó en [enero de 2017](https://pytorch.org/blog/a-year-in/), desde Facebook AI Research. Su forma de trabajar resultaba familiar para quien ya programaba en Python: el grafo se construía mientras corría el programa y se podía depurar durante la ejecución. Esa facilidad para probar y corregir modelos fue parte de su atractivo.

Facebook, que adoptó el nombre corporativo Meta en 2021, siguió siendo su principal casa hasta el anuncio de la [PyTorch Foundation, el 12 de septiembre de 2022](https://pytorch.org/blog/PyTorchfoundation/). La fundación quedó bajo Linux Foundation, con varias empresas participantes. Meta permaneció entre ellas.

La herramienta también cambió. En marzo de 2023, [PyTorch 2.0 incorporó `torch.compile`](https://docs.pytorch.org/blog/pytorch-2.0-release/), que permite compilar modelos conservando la experiencia de desarrollo eager. Aquella discusión entre grafos estáticos y dinámicos explica una parte de sus orígenes, pero se queda corta para describir el PyTorch actual.

En 2026 el desarrollo continúa: la [versión estable 2.14.0](https://github.com/pytorch/pytorch/releases/tag/v2.14.0) se publicó el 2 de septiembre.

### TensorFlow: sigue en desarrollo

Google [publicó TensorFlow el 9 de noviembre de 2015](https://research.google/blog/tensorflow-googles-latest-machine-learning-system-open-sourced-for-everyone/), después de su experiencia con DistBelief. Desde el principio tuvo detrás a una empresa que lo necesitaba para su propio trabajo.

Su barra cambia poco en la gráfica porque Google sigue participando junto con la comunidad. Eso puede esconder cuánto cambió la herramienta. TensorFlow 2.0 adoptó la [ejecución eager por defecto](https://www.tensorflow.org/guide/eager), con operaciones que se evalúan directamente, y [Keras 3 amplió sus backends](https://keras.io/keras_3/) a TensorFlow, JAX y PyTorch. Ahora puedes trabajar con Keras sin quedar ligado exclusivamente a TensorFlow.

Al revisar las versiones disponibles al 4 de octubre de 2026, [TensorFlow 2.21.0](https://github.com/tensorflow/tensorflow/releases/tag/v2.21.0), publicada el 6 de marzo, sigue siendo la estable. También está [2.22.0-rc0](https://github.com/tensorflow/tensorflow/releases/tag/v2.22.0-rc0), del 24 de septiembre, todavía como candidata. El proyecto sigue publicando cambios; hablar de él como si ya hubiera sido abandonado pierde de vista ese trabajo.

### MXNet: el respaldo de AWS y Apache no alcanzó

MXNet apareció en 2015 como una colaboración de investigadores. Recibió el [respaldo de AWS en 2016](https://press.aboutamazon.com/2016/11/aws-announces-three-new-amazon-ai-services) y [entró al Apache Incubator en enero de 2017](https://incubator.apache.org/projects/mxnet.html). Sobre el papel, tenía una combinación prometedora: apoyo empresarial y una fundación con experiencia en proyectos de código abierto.

Pasó varios años en incubación. Se graduó como proyecto de primer nivel de Apache en septiembre de 2022 y, apenas un año después, fue retirado. La [ficha de Apache Attic](https://attic.apache.org/projects/mxnet.html) registra el retiro en septiembre de 2023 y la conclusión del traslado al archivo en febrero de 2024.

En 2026 todavía se pueden consultar su código y documentación, pero el proyecto está retirado. Es el caso que más me hace desconfiar de usar el nombre del patrocinador como garantía de futuro. Tener a AWS detrás y formar parte de Apache no aseguró que MXNet pudiera sostenerse.

<a id="excepcion"></a>

## 04 · Qué puede hacer una fundación

Una fundación permite repartir decisiones y responsabilidades entre varios participantes. Para una empresa que depende de una biblioteca desarrollada por otra, esa estructura puede hacer más atractivo contribuir: tiene un espacio para participar en la dirección del proyecto.

Pero las personas que revisan cambios, responden preguntas y preparan versiones siguen necesitando tiempo para hacerlo. La estructura institucional ayuda a organizar ese trabajo; conseguir que alguien lo haga es un problema que permanece. PyTorch y MXNet terminaron en fundaciones y tuvieron resultados muy distintos.

También está el caso de PyMC. Sus desarrolladores necesitaban seguir usando el código que venía de Theano y asumieron el trabajo de continuarlo. La licencia abierta hizo posible el fork; mantenerlo exigió un equipo dispuesto a hacerse cargo.

<a id="leer"></a>

## 05 · Elegir una herramienta que dure

Cuando una empresa elige un framework, compromete más que las horas necesarias para instalarlo. Su equipo aprende a usarlo, escribe modelos, prepara procesos de entrenamiento y construye aplicaciones alrededor. Cambiarlo después puede significar revisar años de trabajo.

Por eso, además de probar qué tan rápido entrena un modelo, vale la pena mirar quién responde los reportes de errores, cómo se publican las versiones y cuántas personas conocen las partes difíciles del código. También conviene entender cuánto depende ese esfuerzo de una sola empresa o de un solo laboratorio.

A mí me deja una pregunta bastante concreta: si mañana se retira el equipo que sostiene la herramienta, ¿quién podría hacerse cargo? PyMC encontró una respuesta para el código de Theano. MXNet terminó en un archivo. Esa diferencia puede importar mucho cuando la aplicación que depende de ellos es la tuya.

---

### Sobre la gráfica y las fuentes

La gráfica cubre **2007–2026**, con información revisada al **4 de octubre de 2026**. Cada año muestra el estado alcanzado al cierre, salvo 2026, que llega hasta esa fecha de revisión. Los paneles incluyen las fechas de los cambios y el texto enlaza los anuncios y repositorios consultados.

<div class="frameworks-sources-table" role="region" aria-label="Resumen histórico de los frameworks" tabindex="0">

| Proyecto o linaje | Estado al 4 de octubre de 2026 | Evidencia principal |
|-------------------|-------------------------------|---------------------|
| Theano → Aesara → PyTensor | Theano original como legado; PyTensor activo | Fork de PyTensor en noviembre de 2022; PyTensor 3.3.3 en octubre de 2026 |
| Caffe | Legado; última release publicada: 1.0 | Release de abril de 2017 que anuncia modo de mantenimiento |
| Caffe2 | Integración histórica; código Python retirado | Eliminación incorporada a PyTorch en mayo de 2024 |
| PyTorch | Activo; PyTorch Foundation | Gobernanza desde 2022; release 2.14.0 en septiembre de 2026 |
| TensorFlow | Activo; Google y comunidad | 2.21.0 estable; 2.22.0-rc0 candidata, ambas de 2026 |
| MXNet | Retirado; Apache Attic | Retiro en septiembre de 2023; traslado completado en febrero de 2024 |

</div>

Los logos pertenecen a sus respectivos titulares. Se tomaron de los sitios y repositorios de los proyectos para ilustrar la gráfica.
