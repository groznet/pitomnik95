# Pitomnik95 — Hugo site

- `npm install` once, then `npm run dev` (Tailwind build + `hugo server`) or `npm run build` (production, minified).
- Images: keys in `data/images.json` → Unsplash URLs for development. For production set `media_base = "https://files.groznet.com/pitomnik95/"` in `hugo.toml` (URLs become `media_base + key + .webp`).
- Placeholders to replace with real content: `data/partners.json`, `data/testimonials.json`, projects marked `demo: true`, blog sample article, Yandex Metrika ID (`params.ym_id`), legal texts (need legal review).
- Forms are disabled per 152-ФЗ directive (contact page).
