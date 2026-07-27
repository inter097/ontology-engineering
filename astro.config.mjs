// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://ontologias.eliuth.dev',
  markdown: {
    shikiConfig: { theme: 'github-dark-dimmed', wrap: true },
  },
});
