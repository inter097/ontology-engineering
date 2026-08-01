import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

// Sitemap a mano en vez de @astrojs/sitemap: son 14 rutas conocidas y sale de
// la misma colección que ya alimenta el sitio. Una dependencia menos.
export const GET: APIRoute = async ({ site }) => {
  const entradas = await getCollection('capitulos');
  const rutas = [
    '/',
    '/capitulos/',
    ...entradas
      .sort((a, b) => a.data.capitulo - b.data.capitulo)
      .map((e) => `/capitulos/${e.id}/`),
  ];

  const urls = rutas
    .map((r) => `  <url><loc>${new URL(r, site)}</loc></url>`)
    .join('\n');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
      `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
  );
};
