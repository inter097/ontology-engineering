// Destilado del cuaderno para la portada: de cada capítulo, la idea que cambia
// cómo se modela y el hallazgo que un razonador confirmó.
//
// Regla de mantenimiento: `comprobado` solo puede contener afirmaciones que el
// `verificar.py` del capítulo correspondiente reproduzca. Si una comprobación
// deja de pasar, esta línea cambia o se va.

export interface Esencia {
  n: number;
  slug: string;
  tema: string;
  /** la idea del capítulo, en una frase */
  esencial: string;
  /** lo que el razonador confirmó en el caso de estudio */
  comprobado: string;
}

export const RESUMEN: Esencia[] = [
  {
    n: 0,
    slug: '00-simbolos',
    tema: 'Los símbolos',
    esencial:
      'Hay <b>dos notaciones</b> para lo mismo —lógica de primer orden y lógica descriptiva— y el libro salta de una a otra sin avisar. <code>⊑</code> es «está contenido en», no «implica».',
    comprobado:
      'Página propia, no del libro: la tabla de símbolos que los demás capítulos enlazan en vez de repetir.',
  },
  {
    n: 1,
    slug: '01-introduccion',
    tema: 'Qué es una ontología',
    esencial:
      'Una ontología no es una base de datos: es una <b>teoría lógica</b> bajo <b>mundo abierto</b>. Lo que no está escrito no es falso, es desconocido.',
    comprobado:
      'La ontología de ejemplo del propio libro pasa el razonador en verde y se cae al afirmar un individuo que no come nada.',
  },
  {
    n: 2,
    slug: '02-logica-primer-orden',
    tema: 'Lógica y razonamiento',
    esencial:
      '<code>T ⊨ α</code> cuantifica sobre <b>todos</b> los modelos, no sobre el que tienes en la cabeza. Un razonador solo <b>deduce</b>: ni abduce ni induce.',
    comprobado:
      'La inferencia sobre el impala del capítulo 1 nunca fue una deducción: es una abducción, y hay una hipótesis más débil que explica lo mismo.',
  },
  {
    n: 3,
    slug: '03-logicas-descriptivas',
    tema: 'Description Logics',
    esencial:
      'Es el motor de OWL. <code>∀R.C</code> se cumple <b>por vacuidad</b> si no hay ningún <code>R</code>, y <code>≡</code> frente a <code>⊑</code> decide qué puede deducirse.',
    comprobado:
      'Degradar dos clases definidas a primitivas no «pierde precisión»: destruye la subsunción que el propio ejercicio del libro pide demostrar.',
  },
  {
    n: 4,
    slug: '04-owl-2',
    tema: 'OWL 2',
    esencial:
      'Es <code>SROIQ(D)</code> con un estándar detrás. Los <b>perfiles</b> no se eligen por potencia sino por qué operación debe ser barata.',
    comprobado:
      'La cadena de propiedades que resuelve el ejercicio vuelve ilegal una restricción de cardinalidad que antes era válida: el razonador rechaza la ontología entera.',
  },
  {
    n: 5,
    slug: '05-metodologias',
    tema: 'Métodos y metodologías',
    esencial:
      'Las <b>preguntas de competencia</b> son las pruebas unitarias: consulta más respuesta esperada. Consistente no significa bien modelado.',
    comprobado:
      'De las once preguntas de competencia que el libro propone, su ontología de ejemplo contesta cuatro; y una parece contestada solo porque está rota.',
  },
  {
    n: 6,
    slug: '06-top-down',
    tema: 'Desarrollo top-down',
    esencial:
      'Elegir ontología fundacional es elegir <b>qué existe</b>. Y «parte de» son varias relaciones distintas que el idioma confunde.',
    comprobado:
      'Meter la pertenencia a un grupo en la misma propiedad transitiva que la parte estructural deduce que la hoja es parte del bosque.',
  },
  {
    n: 7,
    slug: '07-bottom-up',
    tema: 'Desarrollo bottom-up',
    esencial:
      'Reutilizar lo que ya hay —bases de datos, modelos, tesauros— sabiendo que <b>casi nada significa lo mismo después</b> de convertirlo.',
    comprobado:
      'Un <code>NOT NULL</code> no sobrevive a la traducción: ni como <code>domain</code>, ni como <code>∃</code>. La fila que la base de datos rechazaría, OWL la acepta.',
  },
  {
    n: 8,
    slug: '08-obda',
    tema: 'Acceso a datos (OBDA)',
    esencial:
      'La ontología se pone <b>encima</b> de la base de datos y <b>reescribe la pregunta</b> en vez de mover los datos. Por eso la TBox va en OWL 2 QL.',
    comprobado:
      'La misma consulta sobre los mismos datos devuelve <code>{}</code> o <code>{Mkhize, Naidoo}</code> según se reescriba o no con la TBox.',
  },
  {
    n: 9,
    slug: '09-lenguaje-natural',
    tema: 'Ontologías y lenguas',
    esencial:
      'El <b>nombre no es el concepto</b>: los identificadores no razonan. Y una frase natural no determina un axioma.',
    comprobado:
      'Alinear <i>fleuve</i> y <i>rivière</i> con <i>river</i> como equivalentes —lo que dice el diccionario— vuelve la ontología inconsistente.',
  },
  {
    n: 10,
    slug: '10-modelado-avanzado',
    tema: 'Modelado avanzado',
    esencial:
      'OWL es <b>nítido y atemporal</b>. Vaguedad y tiempo solo entran deformándolo, y todo umbral es una decisión de modelado.',
    comprobado:
      'Alinear dos ontologías que ponen el umbral de «joven» en 30 y en 35 revienta en cuanto aparece alguien de 31 años.',
  },
  {
    n: 11,
    slug: '11-modularizacion',
    tema: 'Modularización',
    esencial:
      '<b>Correcto</b> (no inventa axiomas) y <b>completo</b> (conserva las consecuencias) son independientes, y solo se comprueba el primero.',
    comprobado:
      'Un módulo con los tres nombres pedidos y ningún axioma inventado deja de deducir que un león no puede ser un impala.',
  },
];

export interface Transversal {
  titulo: string;
  texto: string;
  donde: { n: number; slug: string }[];
}

export const TRANSVERSALES: Transversal[] = [
  {
    titulo: 'El universal vacío',
    texto:
      'Una definición hecha solo con <code>∀</code> admite a todo el que no participa en la relación. La forma correcta es <code>∀ + ∃</code>: el <code>∀</code> clasifica, el <code>∃</code> impide la vacuidad.',
    donde: [
      { n: 1, slug: '01-introduccion' },
      { n: 3, slug: '03-logicas-descriptivas' },
      { n: 5, slug: '05-metodologias' },
      { n: 6, slug: '06-top-down' },
      { n: 9, slug: '09-lenguaje-natural' },
    ],
  },
  {
    titulo: 'Vacío no es «no»',
    texto:
      'Bajo mundo abierto, una respuesta vacía significa «no consta», no «no existe». Y se puede <b>probar</b> cuál de las dos es: si al afirmar lo contrario la ontología sigue consistente, era ignorancia.',
    donde: [
      { n: 1, slug: '01-introduccion' },
      { n: 2, slug: '02-logica-primer-orden' },
      { n: 5, slug: '05-metodologias' },
      { n: 8, slug: '08-obda' },
    ],
  },
  {
    titulo: 'El dominio no valida, infiere',
    texto:
      '<code>domain</code> y <code>range</code> no rechazan nada: clasifican en silencio. Sus errores aparecen lejos de donde se cometieron, como una clase insatisfacible que no tiene la culpa.',
    donde: [
      { n: 5, slug: '05-metodologias' },
      { n: 7, slug: '07-bottom-up' },
    ],
  },
  {
    titulo: 'La misma palabra, dos relaciones',
    texto:
      'Parte y miembro, <code>broader</code> y subclase, <i>fleuve</i> y <i>river</i>, dos umbrales de «joven». Igualar por el nombre produce deducciones falsas o inconsistencias, nunca un aviso claro.',
    donde: [
      { n: 6, slug: '06-top-down' },
      { n: 7, slug: '07-bottom-up' },
      { n: 9, slug: '09-lenguaje-natural' },
      { n: 10, slug: '10-modelado-avanzado' },
    ],
  },
];
