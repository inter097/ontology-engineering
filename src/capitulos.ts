// Numeración verificada contra el índice del PDF en /libro. La que circula suele
// estar corrida +1: LibreTexts cuenta "How to Use the Book" como capítulo 1 y
// además inserta un "Prelude" al principio de cada capítulo, así que también
// corre las SECCIONES. Citar siempre contra /libro/OEbook.txt, no contra la web.
// La 2ª edición coincide hasta el 9 y difiere a partir del 10.
export interface Capitulo {
  n: number;
  titulo: string;
  slug: string;
  /** por qué se lee cuando se lee, según la ruta de lectura del repo */
  nota?: string;
  /** true = página propia, no un capítulo del libro (el 0) */
  propio?: boolean;
}

export const CAPITULOS: Capitulo[] = [
  { n: 0, titulo: 'Los símbolos, antes de empezar', slug: '00-simbolos', propio: true, nota: 'página propia: por qué hay dos notaciones y cómo se lee cada símbolo' },
  { n: 1, titulo: 'Introduction', slug: '01-introduccion', nota: 'qué es una ontología y por qué no es una base de datos' },
  { n: 2, titulo: 'First-Order Logic and Automated Reasoning in a Nutshell', slug: '02-logica-primer-orden' },
  { n: 3, titulo: 'Description Logics', slug: '03-logicas-descriptivas', nota: 'explica por qué el razonador infiere lo que infiere' },
  { n: 4, titulo: 'The Web Ontology Language OWL 2', slug: '04-owl-2', nota: 'la herramienta' },
  { n: 5, titulo: 'Methods and Methodologies', slug: '05-metodologias', nota: 'dominio, alcance y preguntas de competencia' },
  { n: 6, titulo: 'Top-down Ontology Development', slug: '06-top-down' },
  { n: 7, titulo: 'Bottom-up Ontology Development', slug: '07-bottom-up' },
  { n: 8, titulo: 'Ontology-Based Data Access', slug: '08-obda' },
  { n: 9, titulo: 'Ontologies and Natural Languages', slug: '09-lenguaje-natural' },
  { n: 10, titulo: 'Advanced Modelling with Additional Language Features', slug: '10-modelado-avanzado' },
  { n: 11, titulo: 'Ontology modularisation', slug: '11-modularizacion' },
];

