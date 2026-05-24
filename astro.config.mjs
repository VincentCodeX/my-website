import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://my-website-20m.pages.dev',
  base: '/',
  trailingSlash: 'ignore',
  integrations: [mdx(), sitemap()],
});
