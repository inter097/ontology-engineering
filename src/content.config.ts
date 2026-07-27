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
    /** una frase con el hallazgo del capítulo, para la tarjeta del índice */
    hallazgo: z.string().optional(),
    /** dos o tres cifras del capítulo: lo que se contó o se comprobó */
    cifras: z
      .array(z.object({ valor: z.string(), etiqueta: z.string() }))
      .max(3)
      .optional(),
  }),
});

export const collections = { capitulos };
