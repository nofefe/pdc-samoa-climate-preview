// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Keep local previews and captured review artefacts free of Astro’s development overlay.
  devToolbar: { enabled: false },
});
