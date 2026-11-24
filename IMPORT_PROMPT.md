# IMPORT_PROMPT.md
# Инструкции для Claude CLI: импорт каталога из rozovsad.ru

Context: Hugo site per CLAUDE.md. We are importing products from a partner's catalog at https://rozovsad.ru/catalog into content/catalog/. Each product becomes a Hugo page bundle.

─── CONFIRMED PAGE STRUCTURE ───

CATALOG LISTING PAGE (https://rozovsad.ru/catalog?page=N):
- Product card selector: a.card-product[href]
- href pattern: /catalog/{category-slug}/{productNNNN}
- 57 pages total, pagination via ?page=N
- ~12 products per page, ~680 products total

PRODUCT DETAIL PAGE (/catalog/{cat}/{productNNNN}):
- Title (Russian):  h1.page-content__title (text node only, excluding span)
- Latin name:       h1.page-content__title > span
- Specs:            .page-properties__list article.property
                    → .property__name + .property__value
  Possible fields: Высота, Ширина, Зимостойкость, Освещённость,
                   Осенняя окраска листа, Форма кроны
- Description:      .accordion__body.rich-text p (join all paragraphs)
- Gallery images:   #page-gallery .page-gallery-preview .swiper-slide a[href]
  Pattern: https://rozovsad.ru/storage/app/media/catalog/*.jpg
- Price variants:   .page-offers__list .page-offer
                    → .page-offer__title (size + container) + .page-offer__price

─── CATEGORY MAPPING ───
rozovsad.ru slug            → Pitomnik95 slug
listevennie-rasteniya       → listvennye-derevya
hvoinei-rasteniya           → khvoinye
listevennie-kustarniki      → kustarniki
mnogoletnie-rasteniya       → mnogoletniki
vishiesya-rasteniya         → vyushchiesya
tropicheskiy-rasteniya      → ekzoticheskie

─── OUTPUT STRUCTURE ───

Each product creates:

content/catalog/{pitomnik-category}/{product-slug}/
├── index.md         ← front matter + description
├── media.json       ← image references for production
└── images/          ← downloaded image files (gitignored)
    ├── image1.jpg
    └── image2.jpg

─── FILE FORMATS ───

index.md front matter:
---
title: "Аир болотный Вариегата"
latin_name: "Acorus calamus Variegatus"
category: "mnogoletniki"
source_id: "product2766"
source_url: "https://rozovsad.ru/catalog/mnogoletnie-rasteniya/product2766"
price: 4590
price_label: "от 4 590 ₽/шт"
price_variants:
  - size: "40-60 см (Контейнер С60)"
    price: 4590
height: "0.6-0.8 м"
width: "0.9-1.2 м"
frost_zone: "Зона 4"
light: "Солнце"
crown_shape: "Стелющаяся"
autumn_color: "Желтая"
draft: false
---
(description paragraphs here)

media.json format:
{
  "remote_base_url": "https://files.groznet.com/pitomnik95/catalog/{category}/{slug}/images/",
  "featured_image": "https://files.groznet.com/pitomnik95/catalog/{category}/{slug}/images/image1.jpg",
  "images": ["image1.jpg", "image2.jpg"]
}

─── TASK ───

1. Write scripts/import_rozovsad.py:

   a) Loop pages 1–57: GET https://rozovsad.ru/catalog?page=N
      Collect all a.card-product[href] links per page

   b) For each product URL:
      - GET the detail page
      - Parse all fields listed above
      - Generate slug: transliterate Russian title to Latin,
        lowercase, replace spaces with hyphens
        Example: "Аир болотный Вариегата" → "air-bolotnyy-variegata"
      - Skip if content/catalog/{category}/{slug}/index.md already exists

   c) Download all gallery images into:
      content/catalog/{category}/{slug}/images/
      - Keep original filename from URL
      - Skip files already downloaded
      - Add 0.5s delay between image downloads

   d) Write index.md with front matter + description

   e) Write media.json from the downloaded images list:
      - remote_base_url uses files.groznet.com path
      - featured_image = first image with full remote URL
      - images = list of local filenames only

   f) Add 1 second delay between product page requests

   g) Log progress: "✓ {slug}" or "✗ {url} — {error}"

   h) Save scripts/import_log.json:
      { "total": N, "success": N, "failed": [{"url": "...", "error": "..."}] }

2. Update .gitignore — add:
   content/catalog/**/images/

3. Install if missing: requests, beautifulsoup4, transliterate

4. DO NOT run the script yet.
   Show me only the first 60 lines of the script, then stop and wait.

5. After I confirm, run a TEST first:
   Import only 1 product: https://rozovsad.ru/catalog/mnogoletnie-rasteniya/product2766
   Show me the generated index.md and media.json.
   Wait for my approval before running the full import.

6. Full import: only after test passes.
   Before the full run, delete any existing demo/placeholder products
   from content/catalog/ that have no source_id in their front matter.

Do not ask questions. Create the script, report when ready.