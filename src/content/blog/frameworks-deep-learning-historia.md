---
title: "Quién sostuvo los frameworks de deep learning: laboratorios, empresas y comunidades"
description: "Theano, Caffe / Caffe2, PyTorch, TensorFlow y MXNet: una cronología de sus orígenes, mantenimiento y gobernanza entre 2007 y 2020."
pubDate: 2026-10-04
lang: es
tags: ["deep-learning", "codigo-abierto", "historia", "datos"]
---

Entre 2007 y 2020 el deep learning pasó de ser un tema de laboratorio a ser infraestructura. Los frameworks que hicieron posible ese cambio tuvieron trayectorias distintas: **Theano, Caffe / Caffe2, PyTorch, TensorFlow y MXNet** mezclan investigación académica, ingeniería corporativa y comunidades de código abierto.

No todos nacieron en una universidad ni todos terminaron dentro de una empresa. TensorFlow y PyTorch tienen origen corporativo; MXNet pasó a la incubadora de Apache; Theano perdió el desarrollo principal de su equipo académico, pero tuvo continuaciones. La pregunta interesante es quién sostiene el trabajo cuando una herramienta se vuelve infraestructura.

La [gráfica interactiva al final de la entrada](#grafica) permite explorar cada periodo. Los logos identifican los proyectos y las etiquetas explican quién los mantenía o en qué estado estaban.

<nav class="toc" aria-label="Contenido">
  <details>
    <summary>
      <span class="toc-kicker">Contenido</span>
      <span class="toc-count">5 secciones</span>
    </summary>
    <ol>
      <li><a href="#cronologia"><span class="toc-n">01</span><span class="toc-t">La gráfica, otra vez</span><span class="toc-d">Interactiva, con los logos y con el detalle de cada tramo</span></a></li>
      <li><a href="#patron"><span class="toc-n">02</span><span class="toc-t">El patrón</span><span class="toc-d">Distintos orígenes, un problema de mantenimiento</span></a></li>
      <li><a href="#filas"><span class="toc-n">03</span><span class="toc-t">Las cinco filas</span><span class="toc-d">Qué fue cada framework y qué le pasó</span></a></li>
      <li><a href="#excepcion"><span class="toc-n">04</span><span class="toc-t">El papel de las fundaciones</span><span class="toc-d">PyTorch y MXNet: gobernanza y continuidad</span></a></li>
      <li><a href="#leer"><span class="toc-n">05</span><span class="toc-t">Qué dice esta gráfica hoy</span><span class="toc-d">Y por qué importa si estás eligiendo infraestructura</span></a></li>
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

## 01 · La gráfica, otra vez

Una barra de color puede ocultar diferencias importantes: el origen de un proyecto, su financiación y su gobernanza no son lo mismo. En esta cronología el color identifica al framework; la etiqueta de cada tramo indica su responsable principal o su estado. No implica que una sola institución escribiera todo el código.

Los cuadros punteados preceden al lanzamiento público. Las fechas se agrupan por año: una frontera no representa necesariamente una transferencia de propiedad. En particular, la fila **Caffe / Caffe2 reúne dos proyectos relacionados**, no dos nombres del mismo repositorio. El logo de esa fila es el de Caffe2.

[Explorar la gráfica y sus detalles ↓](#grafica)

<a id="patron"></a>

## 02 · El patrón

Los arranques públicos se reparten así: **Theano en 2007, Caffe en 2013, TensorFlow y MXNet en 2015, PyTorch en enero de 2017**. Caffe2 se presentó en abril de 2017. Distinguir el trabajo previo del lanzamiento público evita adelantar artificialmente una barra.

Lo que comparten no es un mismo destino institucional, sino un problema de mantenimiento. Un framework necesita kernels para hardware nuevo, empaquetado, documentación y soporte. Mi lectura es que esa carga ayuda a explicar el peso que adquirieron las empresas, aunque una cronología por sí sola no demuestra por qué ganó o perdió cada proyecto.

Tampoco conviene confundir patrocinio con propiedad. AWS respaldó MXNet, pero Apache proporcionaba su marco de gobernanza. Y una fundación puede ampliar la participación sin garantizar que un proyecto siga teniendo mantenedores.

<a id="filas"></a>

## 03 · Las cinco filas

### Theano — Université de Montréal y MILA (2007–2017; mantenimiento posterior)

Theano permitía definir expresiones matemáticas como grafos simbólicos, optimizarlas y generar código eficiente para CPU y GPU. Salió del entorno de investigación de Montréal. No hay motivo para dibujar una transferencia formal de la universidad a MILA en 2013 sin una fuente que documente ese cambio.

El anuncio del fin del desarrollo principal llegó el **28 de septiembre de 2017**; la versión **1.0 se publicó el 15 de noviembre de 2017**. El equipo anunció un periodo de mantenimiento limitado, y hubo versiones posteriores. Por eso la barra desde 2018 dice «mantenimiento limitado», no «el proyecto desapareció». La historia también continuó en proyectos derivados, como PyTensor. Véanse el [anuncio de MILA](https://groups.google.com/g/theano-announce/c/PiH4p7NqZ60), el [historial de versiones](https://github.com/Theano/Theano/blob/master/HISTORY.txt) y el [repositorio de Theano](https://github.com/Theano/Theano).

### Caffe / Caffe2 — Berkeley, Facebook y la integración con PyTorch

Caffe nació en Berkeley, con Yangqing Jia y la comunidad de BVLC. Sus archivos de configuración facilitaron compartir arquitecturas y modelos. Caffe2 fue un proyecto relacionado que Facebook presentó en 2017, orientado también al despliegue móvil y distribuido; no fue una simple compraventa de Caffe.

La integración con PyTorch se desarrolló en 2018. El **2 de mayo** se anunció públicamente la plataforma conjunta PyTorch 1.0. La fila continúa después de esa fecha como «integrado en PyTorch»: marcarla como inexistente en 2019 o 2020 confundiría integración con desaparición. Fuentes: [Caffe, BVLC](https://caffe.berkeleyvision.org/) y el [anuncio conjunto de Caffe2 y PyTorch](https://caffe2.ai/blog/2018/05/02/Caffe2_PyTorch_1_0.html).

### PyTorch — Facebook AI Research y la PyTorch Foundation

PyTorch se publicó en **enero de 2017**, después de su desarrollo inicial. El grafo dinámico facilitó experimentar y depurar desde Python: no era necesario declarar por adelantado un grafo estático completo. Eso no significa que PyTorch carezca de código compilado; sus operaciones se apoyan en bibliotecas y kernels nativos. Su [balance del primer año](https://pytorch.org/blog/a-year-in/) documenta aquel lanzamiento.

Durante 2007–2020 la institución de referencia es Facebook AI Research. Usar «Meta» en esas barras sería emplear retrospectivamente el nombre posterior de la empresa. La [PyTorch Foundation se anunció en septiembre de 2022](https://pytorch.org/blog/PyTorchfoundation/), fuera de la ventana de la gráfica, con participación de varias empresas, incluida Meta.

### TensorFlow — Google (desde 2015)

TensorFlow también nació dentro de una empresa. Google lo publicó como código abierto el **9 de noviembre de 2015**, después de la experiencia de DistBelief. Por tanto, PyTorch no es el único framework de origen corporativo de esta selección. El [anuncio de Google Research](https://research.google/blog/tensorflow-googles-latest-machine-learning-system-open-sourced-for-everyone/) explica ese origen.

Dentro de esta ventana la barra permanece bajo Google. La herramienta sí cambió: TensorFlow 2.0 adoptó la ejecución eager por defecto, de modo que la oposición entre «PyTorch dinámico» y «todos los demás estáticos» tampoco describe todo el periodo. Véase la [documentación de ejecución eager](https://www.tensorflow.org/guide/eager).

### MXNet — comunidad DMLC, Apache y apoyo de AWS

MXNet apareció en 2015 como una colaboración de investigadores y recibió el [respaldo de AWS en 2016](https://press.aboutamazon.com/2016/11/aws-announces-three-new-amazon-ai-services). Su entrada al Apache Incubator fue en enero de 2017. **No se graduó ese mismo año:** la graduación llegó en septiembre de 2022, como registra la [ficha de incubación de Apache](https://incubator.apache.org/projects/mxnet.html).

La barra de 2017–2020 indica, por tanto, «Apache Incubator». El proyecto fue retirado en 2023, fuera del periodo dibujado; su [sitio oficial lo identifica como retirado](https://mxnet.apache.org/). Una fundación y un patrocinador importante no bastan, por sí solos, para asegurar continuidad.

<a id="excepcion"></a>

## 04 · El papel de las fundaciones

PyTorch y MXNet muestran que el recorrido no es simplemente «universidad, luego empresa». PyTorch pasó de liderazgo corporativo a una fundación; MXNet ya estaba en incubación en Apache años antes. Sus resultados distintos impiden tratar la fundación como garantía de éxito o como señal de abandono.

Ceder la gobernanza tampoco significa que las empresas dejen de contribuir. Conviene separar tres preguntas: quién toma decisiones, quién paga a los mantenedores y quién puede continuar el proyecto si uno de sus patrocinadores se retira.

<a id="leer"></a>

## 05 · Qué dice esta gráfica hoy

La cronología sirve para formular preguntas sobre infraestructura, no para decidir qué framework usar solamente por su logo o por la empresa que lo respalda:

- **¿Quién mantiene el código y cómo se financia ese trabajo?** Una licencia abierta no asegura tiempo de ingeniería.
- **¿Cómo se toman las decisiones?** Patrocinio, mantenimiento y gobernanza pueden recaer en grupos distintos.
- **¿Qué ocurre si un equipo se retira?** Importan la comunidad, la documentación y la posibilidad de continuar el desarrollo.

Estas cinco historias no demuestran que todos los proyectos académicos terminen absorbidos ni que las fundaciones resuelvan el mantenimiento. Sí muestran por qué una evaluación de infraestructura necesita mirar más allá de las prestaciones técnicas.

---

### Sobre la gráfica y las fuentes

La cronología resume el periodo **2007–2020** a resolución anual. Los desenlaces posteriores se explican en el texto y en los paneles, sin dibujarlos dentro de ese intervalo. Las fuentes primarias están enlazadas en cada sección.

<div class="frameworks-sources-table" role="region" aria-label="Resumen histórico de los frameworks" tabindex="0">

| Framework | Lanzamiento público | Origen | Evolución institucional |
|-----------|---------------------|--------|------------------------|
| Theano | 2007 | Université de Montréal / MILA | Fin del desarrollo principal anunciado en 2017; mantenimiento y derivados posteriores |
| Caffe / Caffe2 | 2013 / 2017 | BVLC / Facebook | Caffe2 se integra con PyTorch en 2018 |
| PyTorch | Enero de 2017 | Facebook AI Research | PyTorch Foundation desde 2022 |
| TensorFlow | Noviembre de 2015 | Google | Liderazgo de Google durante la ventana mostrada |
| MXNet | 2015 | Comunidad DMLC | Incubación en 2017; graduación en 2022; retiro en 2023 |

</div>

Los logos proceden de los sitios y repositorios de los proyectos y se sirven como archivos locales, respetando sus proporciones y colores. Son marcas de sus respectivos titulares y se usan con fines ilustrativos.
