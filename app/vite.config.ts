import { defineConfig } from 'vite';

/* No framework, no CDN, no font fetch. Everything the page asks for at runtime is
   same-origin under /data, /fonts and /patents, plus the analyst Worker.
   See notes/APP-SPEC-2026-09-02.md section 1. */
export default defineConfig({
  base: '/',
  build: {
    target: 'es2022',
    assetsInlineLimit: 0,
    reportCompressedSize: true,
  },
  server: { port: 5173 },
  preview: { port: 4173 },
});
