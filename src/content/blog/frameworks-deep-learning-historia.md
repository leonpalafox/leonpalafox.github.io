---
title: "Los frameworks de deep learning nacieron en laboratorios y murieron en empresas"
description: "Theano, Caffe2, PyTorch, TensorFlow y MXNet: la gráfica de quién mantuvo cada framework entre 2007 y 2020, rehecha y con la explicación de cada tramo."
pubDate: 2026-10-04
lang: es
tags: ["deep-learning", "codigo-abierto", "historia", "datos"]
cover: frameworks-deep-learning-historia
---

Entre 2007 y 2020 el deep learning pasó de ser un tema de laboratorio a ser infraestructura. La gráfica que abre esta entrada —la de los cinco frameworks y quién los mantenía año con año— se ha compartido mucho, y cuenta casi toda la historia: **Theano, Caffe2, PyTorch, TensorFlow y MXNet**, con una barra de color para cada institución que los sostuvo.

Contiene un patrón que se repite cinco veces. Casi todos empiezan en una universidad y casi todos terminan dentro de una empresa. El único que hace el camino inverso es el que empezó corporativo.

Aquí está la gráfica otra vez, pero con los logos a color y todo explicado: haz clic en cualquier barra o en cualquier nombre y se abre el detalle de ese tramo. Mueve el año para ver el reparto de un momento concreto.

<nav class="toc" aria-label="Contenido">
  <details>
    <summary>
      <span class="toc-kicker">Contenido</span>
      <span class="toc-count">5 secciones</span>
    </summary>
    <ol>
      <li><a href="#grafica"><span class="toc-n">01</span><span class="toc-t">La gráfica, otra vez</span><span class="toc-d">Interactiva, con los logos y con el detalle de cada tramo</span></a></li>
      <li><a href="#patron"><span class="toc-n">02</span><span class="toc-t">El patrón</span><span class="toc-d">De la universidad a la empresa, cinco veces</span></a></li>
      <li><a href="#filas"><span class="toc-n">03</span><span class="toc-t">Las cinco filas</span><span class="toc-d">Qué fue cada framework y qué le pasó</span></a></li>
      <li><a href="#excepcion"><span class="toc-n">04</span><span class="toc-t">La excepción que confirma la regla</span><span class="toc-d">PyTorch y el camino inverso</span></a></li>
      <li><a href="#leer"><span class="toc-n">05</span><span class="toc-t">Qué dice esta gráfica hoy</span><span class="toc-d">Y por qué importa si estás eligiendo infraestructura</span></a></li>
    </ol>
  </details>
</nav>

<style>
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

## 01 · La gráfica, otra vez

La versión original tiene un problema de lectura: los tramos son cajas de color sin etiqueta, así que hay que adivinar qué cambió en cada frontera y por qué. La reconstruí como una línea de tiempo con logos, botones y un panel de detalle. Cada tramo de color es un periodo de mantenimiento, y cada frontera entre dos colores es una transferencia que sí ocurrió en una fecha concreta.

<a id="grafica"></a>

Los cuadros punteados son años en los que el proyecto todavía no existía. Si mueves el control de año, la gráfica te dice quién tenía cada framework ese año y en qué estado estaba. Si haces clic en una fila, ves las etapas completas de ese framework con sus fechas.

<a id="patron"></a>

## 02 · El patrón

Puestos en orden cronológico, los cinco arranques forman una secuencia bastante limpia: **Theano en 2007, Caffe en 2013, TensorFlow y MXNet en 2015, PyTorch en 2016**. Cuatro de los cinco nacieron dentro de una universidad o de un grupo de investigación.

El segundo acto es el que casi nadie recuerda: **todos menos uno terminaron absorbidos, transferidos o abandonados por una empresa**. Theano lo dejó de mantener su propio equipo, Caffe2 se fusionó con PyTorch, MXNet pasó a una fundación con el respaldo de Amazon, y PyTorch acabó en una fundación después de nacer en Meta. Cuando la gráfica original dice "no más en desarrollo" para Theano en 2018, está describiendo el final de un ciclo completo: el proyecto universitario que se quedó sin relevo porque el relevo se fue a la industria.

Hay una explicación estructural y no tiene nada de misteriosa. Un framework de deep learning no se sostiene con artículos: se sostiene con kernels de GPU para hardware que cambia cada año, con empaquetado para media docena de sistemas operativos, con documentación y con soporte. Eso es trabajo de ingeniería a tiempo completo y no encaja en el presupuesto de un laboratorio, cuyo producto son publicaciones. La industria sí tiene incentivo para pagarlo, porque necesita desplegar modelos.

<a id="filas"></a>

## 03 · Las cinco filas

### Theano — Université de Montréal y MILA (2007–2017)

Theano es el abuelo de la lista y no es un framework en el sentido actual: es un compilador de expresiones matemáticas. Escribías tu modelo como un grafo simbólico, Theano lo optimizaba y generaba código en C y CUDA. Esa separación entre lo que escribes y lo que se ejecuta es hoy normal; en 2007 era novedosa.

Salió del grupo de Yoshua Bengio en Montréal y creció junto con MILA. La versión 1.0 llegó en septiembre de 2017 y, poco después, el anuncio del fin del desarrollo. Cuando la gráfica marca 2018 como el año en que Theano deja de desarrollarse, el sucesor real ya tenía dos años en el mercado: PyTorch, que resolvía el mismo problema con Python corriente y sin compilar nada.

### Caffe2 — UC Berkeley y Meta (2013–2018)

Caffe apareció en diciembre de 2013, escrito por Yangqing Jia durante su doctorado en Berkeley, en el laboratorio de Trevor Darrell. Su aportación práctica fue permitir que un modelo se definiera en un archivo de configuración en vez de en código: se compartía un prototxt y cualquiera podía reproducir la red. Para una generación de investigadores, eso fue la diferencia entre leer un resultado y poder verificarlo.

Caffe2 es la segunda vida del proyecto. Facebook lo anunció en abril de 2017 con lo que al original le faltaba —redes recurrentes, despliegue en móvil, entrenamiento distribuido— y un año después lo fusionó dentro de PyTorch. Berkeley ya había cerrado el soporte del Caffe original en 2018. La frontera entre la barra de Berkeley y la de Meta en la gráfica es, literalmente, el momento en que el framework cambió de dueño.

### PyTorch — Meta y la PyTorch Foundation (2016– )

PyTorch llegó en 2016 y ganó por una razón poco glamorosa: se comportaba como Python normal. El grafo se construye mientras el código corre, así que un `print` o un depurador sirven de algo. El resto de la lista pedía que describieras el grafo antes de ejecutarlo, y depurar eso era incómodo.

Con la fusión de Caffe2 en 2018 quedó como el único framework de Meta, y en 2019 ya dominaba el código nuevo de investigación. La transferencia a la PyTorch Foundation es de 2022 y queda fuera del marco de esta gráfica, pero es el desenlace que importa: el único framework que nació dentro de una empresa terminó siendo el único que salió de una.

### TensorFlow — Google (2015– )

TensorFlow es el caso en el que la empresa no compró el proyecto ni lo absorbió: **lo construyó y lo mantuvo entero**. Google venía corriendo DistBelief internamente —en producción desde 2011, sin código público— y en noviembre de 2015 liberó TensorFlow como código abierto. Con Keras como fachada amable y una ruta clara hacia producción, se volvió durante años la respuesta por defecto a "qué uso".

Es también la única fila de la gráfica que no cambia de dueño ni una vez. Toda la barra es del mismo color.

### MXNet — consorcio académico, Apache y AWS (2015– )

MXNet es el experimento que más me interesa de los cinco. Lo armó un grupo de varias universidades en lugar de un solo laboratorio, Amazon lo adoptó como framework preferido en AWS, entró al Apache Incubator en enero de 2017 y se graduó como proyecto de primer nivel ese mismo diciembre. Todo el camino institucional correcto: fundación neutral, respaldo corporativo, soporte en la nube más grande.

Y aun así perdió. Es la prueba de que la gobernanza correcta no basta cuando el ecosistema ya eligió. Si algo enseña MXNet, es que en infraestructura de software el respaldo de una empresa grande no sustituye a la comunidad de desarrolladores que escribe los tutoriales, responde en los foros y publica el código de sus modelos.

<a id="excepcion"></a>

## 04 · La excepción que confirma la regla

Hay una lectura fácil de esta gráfica: "la industria se comió al código abierto académico". Es verdad a medias. La lectura más precisa es que **el coste de mantener un framework se volvió incompatible con la estructura de un laboratorio, y compatible con la de una empresa que necesita desplegar modelos**.

PyTorch no niega el patrón: lo invierte. Nació corporativo y terminó en una fundación neutral, que es exactamente el camino que ninguna otra fila recorre. Hoy el patrón dominante ya no es "universidad que se queda sin relevo" sino "empresa que cede la gobernanza cuando el proyecto se vuelve infraestructura crítica". TensorFlow sigue dentro de Google; PyTorch ya no está dentro de Meta.

<a id="leer"></a>

## 05 · Qué dice esta gráfica hoy

Si estás eligiendo infraestructura hoy, la gráfica de 2007–2020 se lee como una advertencia sobre qué preguntar. No "cuál es más rápido en el benchmark", sino:

- **¿Quién paga el mantenimiento dentro de tres años?** Theano no murió por un problema técnico, murió cuando el equipo que lo entendía dejó de estar financiado para mantenerlo.
- **¿Qué pasa si la empresa se aburre?** TensorFlow sobrevivió a dos cambios de estrategia interna de Google; MXNet no sobrevivió a la indiferencia del mercado. Una fundación neutral es una respuesta, no una garantía.
- **¿El paquete sobrevive sin la empresa?** Si la respuesta es no, no estás eligiendo una herramienta, estás eligiendo un proveedor.

La conclusión práctica es incómoda: entre 2007 y 2020, "código abierto" describió la licencia, no la gobernanza. Cinco proyectos con licencias permisivas, y cuatro de ellos con una sola institución decidiendo cuándo se terminaba. La buena noticia es que la curva cambió: la fundación dejó de ser un cementerio y se volvió una salida.

---

### Sobre la gráfica y las fuentes

La versión de esta entrada se construyó desde cero a partir del registro público de cada proyecto, no copiando la imagen original. Donde la original simplificaba una transferencia, esta abre el tramo en la fecha documentada:

| Framework | Nace | Primera casa | Segunda casa | Estado |
|-----------|------|--------------|--------------|--------|
| Theano | 2007 | Université de Montréal | MILA (2013) | Fin de desarrollo anunciado en 2018 |
| Caffe / Caffe2 | 2013 | UC Berkeley (BVLC) | Meta (2017) | Fusionado con PyTorch en marzo de 2018 |
| PyTorch | 2016 | Meta (FAIR) | PyTorch Foundation (2022) | Activo |
| TensorFlow | 2015 | Google Brain | — | Activo |
| MXNet | 2015 | Consorcio académico | Apache / AWS (2017) | Proyecto Apache |

Fuentes principales: la página de [Theano](https://github.com/Theano/Theano) y su anuncio de fin de soporte; la [historia de Caffe y Caffe2](https://en.wikipedia.org/wiki/Caffe_(software)) con el anuncio de [Facebook al liberar Caffe2](https://techcrunch.com/2017/04/18/facebook-open-sources-caffe2-its-flexible-deep-learning-framework-of-choice/); el [anuncio de TensorFlow](https://research.google/blog/tensorflow-googles-latest-machine-learning-system-open-sourced-for-everyone/) en el blog de Google Research; y la [entrada de MXNet al Apache Incubator](https://techcrunch.com/2017/01/30/mxnet-accepted-to-the-apache-incubator/).

Los logos son marcas de sus respectivos dueños y se usan aquí con fines ilustrativos. Están incluidos en la página —vectoriales o convertidos a PNG en el build— para que el diagrama no dependa de ninguna petición a un servidor externo.
