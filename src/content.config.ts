import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Una sola fuente de verdad: los .md viven en /capitulos, navegables en GitHub,
// y de ahí mismo se genera el sitio. Nada se duplica.
const capitulos = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './capitulos' }),
  schema: z.object({
    titulo: z.string(),
    capitulo: z.number(),
    // resumen = qué dice el libro · ejercicios = resueltos paso a paso
    // caso-de-estudio = el cierre del capítulo, algo verificable
    seccion: z.enum(['resumen', 'ejercicios', 'caso-de-estudio']),
    descripcion: z.string(),
    keet: z.string().describe('capítulo/secciones de Keet que cubre'),
  }),
});

export const collections = { capitulos };
