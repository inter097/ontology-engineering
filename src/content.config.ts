import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Una sola fuente de verdad: los .md viven en /capitulos, navegables en GitHub,
// y de ahí mismo se genera el sitio. Nada se duplica.
//
// Una página por capítulo: `capitulos/NN-nombre.md`. Los artefactos ejecutables
// van en la carpeta hermana `capitulos/NN-nombre/artefactos/`, que el patrón del
// loader deja fuera a propósito.
const capitulos = defineCollection({
  loader: glob({ pattern: '*.md', base: './capitulos' }),
  schema: z.object({
    titulo: z.string(),
    capitulo: z.number(),
    descripcion: z.string(),
    keet: z.string().describe('capítulo/secciones de Keet que cubre'),
  }),
});

export const collections = { capitulos };
