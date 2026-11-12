// Asset manager for blog imagery.
//
// Drop a file in `src/assets/blog/` and it is picked up automatically — the id is
// the path under that folder without the extension (`mercado-de-inteligencia`,
// or `2026/foo` if you nest it). Register alt text / caption / credit here once
// and every post that uses the asset inherits them, so the same image reused
// across posts never loses its description.
//
// Posts opt in through frontmatter:
//
//   cover: mercado-de-inteligencia
//   coverAlt: "…"        # optional, overrides the entry below
//   coverCaption: "…"    # optional, overrides the entry below

const files = import.meta.glob<ImageMetadata>('../assets/blog/**/*.{png,jpg,jpeg,webp,avif,svg}', {
  eager: true,
  import: 'default',
});

const PREFIX = '../assets/blog/';

/** id -> imported image, keyed by path under src/assets/blog/ minus the extension. */
const sources: Record<string, ImageMetadata> = Object.fromEntries(
  Object.entries(files).map(([path, src]) => [path.slice(PREFIX.length).replace(/\.[^.]+$/, ''), src]),
);

export interface AssetEntry {
  /** Describes the image for screen readers. Empty string marks it purely decorative. */
  alt: string;
  /** Shown under the image. Keep it short — it renders in the mono micro-label style. */
  caption?: string;
  /** Photographer / illustrator / outlet, appended after the caption. */
  credit?: string;
}

/** Metadata for the images in src/assets/blog/. Keys must match an id from that folder. */
const registry: Record<string, AssetEntry> = {
  'cuando-la-respuesta-llega-antes-que-la-explicacion': {
    alt: 'Un hombre de abrigo, de espaldas sobre un risco, sostiene un marco vacío frente a una gigantesca escultura de arcos y esferas translúcidas que flota sobre un valle desértico; un hilo rojo desciende desde la estructura hasta una máquina que dibuja sobre un rollo de papel.',
    caption: 'El Financiero · 13 de octubre de 2026',
  },
  'el-banco-de-jensen': {
    alt: 'Una mano gigante coloca un chip de Nvidia sobre un banco de columnas clásicas, rodeado de torres góticas llenas de servidores con luces verdes; una figura diminuta espera al pie de la escalinata.',
  },
  'mexico-industria-frente-a-pemex': {
    alt: 'Una balanza enfrenta una plataforma petrolera deteriorada con una fábrica automatizada de robots y servidores, frente a la silueta del mapa de México.',
  },
  'carrera-ia-sin-frenar': {
    alt: 'Portada de El Financiero: un conductor al volante a 180 km/h en una carretera costera, con señales que a la izquierda prometen “Innovación”, “Prosperidad” y “Soluciones a grandes retos” y a la derecha advierten “Pérdida de control”, “Usos maliciosos” y “Competencia global sin límites”, bajo el titular “La carrera de la IA que nadie sabe frenar”.',
    caption: 'El Financiero · 15 de septiembre de 2026',
  },
  'mercado-de-inteligencia': {
    alt: 'Portada de El Financiero: León Palafox frente a un pasillo de puestos que anuncian Kimi, GPT, Claude, Grok, Gemini y modelos abiertos, bajo el titular “Quién decide qué inteligencia compra su empresa”.',
    caption: 'El Financiero · 23 de julio de 2026',
  },
  riiaa: {
    alt: 'Conferencia RIIAA en el museo Universum, Ciudad de México',
  },
  'frameworks-deep-learning-historia': {
    alt: 'Línea de tiempo de 2007 a 2020 con cinco frameworks de deep learning —Theano, Caffe2, PyTorch, TensorFlow y MXNet— y una barra de color por cada institución que los mantuvo.',
    caption: 'Gráfica del artículo',
  },
  'the-cost-of-thinking-in-spanish': {
    alt: "Ilustración de una calle con un cartel gigante que dice ENGLISH, entre edificios y pantallas de datos, con personas caminando.",
    caption: "Medium · November 9, 2026",
  },
  'la-ia-esta-ampliando-el-espacio-de-soluciones': {
    alt: "Diagrama de flujo sobre la viabilidad de un recomendador de café, con pasos de necesidad, tiempo de entrega y relevancia.",
    caption: "GBM Tech · 5 de noviembre de 2026",
  },
  'corporations-without-new-hires': {
    alt: "Un brazo robótico sube una escalera hacia una puerta en un paisaje rojo, bajo la luna.",
    caption: "Medium · October 26, 2026",
  },
  'muse-and-the-internet-that-works-for-us': {
    alt: "Ilustración de una joven y un robot esponjoso en un prado, con una ciudad y nubes al fondo.",
    caption: "Medium · September 28, 2026",
  },
  'la-ultima-frontera-quizas-no-sea-humana': {
    alt: "Un libro abierto se convierte en un paisaje montañoso con figuras diminutas caminando por sus páginas.",
    caption: "Medium · 13 de septiembre de 2026",
  },
  'they-are-coming-to-deploy-us': {
    alt: "Un grupo de personas con traje entra a un edificio corporativo moderno.",
    caption: "Medium · July 6, 2026",
  },
  'silicon-valley-built-a-religion': {
    alt: "Un templo púrpura con arcos y una esfera luminosa, frente a una congregación de siluetas.",
    caption: "Medium · June 22, 2026",
  },
  'the-ai-world-just-changed-overnight': {
    alt: "Mapa mundial oscuro con líneas de red luminosas y una cúpula de cristal sobre una región.",
    caption: "Medium · June 13, 2026",
  },
  'the-cost-of-ai-written-code-is-not-the-same-everywhere': {
    alt: "Ilustración de un rostro humano y edificios atravesados por líneas de circuito.",
    caption: "Medium · June 8, 2026",
  },
  'the-three-forces-threatening-the-junior-data-scientist': {
    alt: "Ilustración de personas trabajando en cubículos y pantallas de código, en tonos naranja y azul.",
    caption: "Medium · June 6, 2026",
  },
  'the-spacex-ipo-is-not-just-a-space-story': {
    alt: "Un monolito negro de servidores se alza en un paisaje desértico con figuras diminutas.",
    caption: "Medium · May 25, 2026",
  },
  'de-listas-estaticas-a-recomendaciones-dinamicas-gbm': {
    alt: "Diagrama de una interfaz que pasa de recomendaciones genéricas a perfiles personalizados.",
    caption: "GBM Tech · 13 de abril de 2026",
  },
  'the-technology-that-keeps-almost-working': {
    alt: "Niños y adultos reunidos alrededor de máquinas recreativas en una tienda.",
    caption: "Medium · March 23, 2026",
  },
  'the-four-papers-every-ai-practitioner-should-have-a-fight-about': {
    alt: "Composición abstracta de cuadrículas y bloques de color sobre fondo oscuro.",
    caption: "Medium · March 18, 2026",
  },
  'the-algorithms-brutal-honesty': {
    alt: "Ilustración de una fábrica con máquinas, pantallas y personas trabajando.",
    caption: "Medium · February 2, 2026",
  },
  'netflixs-ai-pivot': {
    alt: "Ilustración en tres paneles sobre el consumo de contenido: una persona frente a una pantalla, un teléfono y una pared de imágenes.",
    caption: "Medium · January 26, 2026",
  },
  'the-ouroboros-in-the-server-room': {
    alt: "Ilustración de una serpiente mecánica en blanco y negro formando un arco.",
    caption: "Medium · January 5, 2026",
  },
};

export interface BlogAsset extends AssetEntry {
  id: string;
  src: ImageMetadata;
}

/** All registered ids, sorted — handy for error messages and for listing what exists. */
export function listAssets(): string[] {
  return Object.keys(sources).sort();
}

/**
 * Resolve an asset id to its image plus metadata. Throws at build time on a typo
 * or an unregistered file, so a broken cover never ships silently.
 */
export function getAsset(id: string, overrides: Partial<AssetEntry> = {}): BlogAsset {
  const src = sources[id];
  if (!src) {
    throw new Error(
      `Unknown blog asset "${id}". Add the file to src/assets/blog/ or fix the id. Available: ${listAssets().join(', ')}`,
    );
  }
  const entry = registry[id];
  if (!entry && overrides.alt === undefined) {
    throw new Error(
      `Blog asset "${id}" has no alt text. Add an entry to the registry in src/lib/assets.ts, or set coverAlt in the post frontmatter.`,
    );
  }
  return {
    id,
    src,
    alt: overrides.alt ?? entry.alt,
    caption: overrides.caption ?? entry?.caption,
    credit: overrides.credit ?? entry?.credit,
  };
}
