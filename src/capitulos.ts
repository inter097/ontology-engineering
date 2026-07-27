// Numeración verificada contra el índice del autor. La que circula suele estar
// corrida +1 porque cuenta "How to Use the Book" como capítulo 1 — LibreTexts, por
// ejemplo, publica el capítulo 1 (Introduction) bajo la URL ".../02%3A_...".
// La 2ª edición coincide hasta el 9 y difiere a partir del 10.
export interface Capitulo {
  n: number;
  titulo: string;
  slug: string;
  /** por qué se lee cuando se lee, según la ruta de lectura del repo */
  nota?: string;
}

export const CAPITULOS: Capitulo[] = [
  { n: 1, titulo: 'Introduction', slug: '01-introduccion', nota: 'qué es una ontología y por qué no es una base de datos' },
  { n: 2, titulo: 'First-Order Logic and Automated Reasoning in a Nutshell', slug: '02-logica-primer-orden' },
  { n: 3, titulo: 'Description Logics', slug: '03-logicas-descriptivas', nota: 'explica por qué el razonador infiere lo que infiere' },
  { n: 4, titulo: 'The Web Ontology Language OWL 2', slug: '04-owl-2', nota: 'la herramienta' },
  { n: 5, titulo: 'Methods and Methodologies', slug: '05-metodologias', nota: 'dominio, alcance y preguntas de competencia' },
  { n: 6, titulo: 'Top-down Ontology Development', slug: '06-top-down' },
  { n: 7, titulo: 'Bottom-up Ontology Development', slug: '07-bottom-up' },
  { n: 8, titulo: 'Ontology-Based Data Access', slug: '08-obda' },
  { n: 9, titulo: 'Ontologies and Natural Languages', slug: '09-lenguaje-natural' },
  { n: 10, titulo: 'Advanced Modeling with Additional Language Features', slug: '10-modelado-avanzado' },
];

export const ORDEN_SECCIONES = ['resumen', 'ejercicios', 'caso-de-estudio'] as const;

export const NOMBRE_SECCION: Record<string, string> = {
  resumen: 'resumen',
  ejercicios: 'ejercicios',
  'caso-de-estudio': 'caso de estudio',
};
