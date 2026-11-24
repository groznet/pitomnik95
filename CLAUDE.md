# 🌐 Pitomnik95 — Website Project 2026

> **Purpose:** Single source of truth for the Pitomnik95 website. Written for the developer (Kerim @ GrozNet) and for AI assistants that generate pages, sections and code. Keep it updated as decisions change.
> **Last updated:** 23 Nov 2026

---

## 🧭 Project Summary

**Pitomnik95** — садовый центр и питомник декоративных и плодовых растений в Чеченской Республике. Более 1400 наименований растений, садовой техники STIHL и сопутствующих товаров. Работаем с мировыми лидерами в области садоводства. Бесплатный выезд дизайнера. Доставка по республике и самовывоз.

| Field | Value |
| --- | --- |
| Project name | Pitomnik95 — Садовый питомник и центр |
| Type | Corporate site / catalog / portfolio |
| Status | Redesign — Hugo static site (replacing current WordPress) |
| Main language | Russian. No i18n planned |
| Client / owner | Руслан (уточнить у клиента) |
| Developer | Kerim @ GrozNet (info@groznet.com, github.com/groznet, groznet.com) |
| Domain | pitomnik95.ru |
| Hosting | GitHub Pages (static) |
| Analytics | Yandex Metrika |

### Design principle

The site must feel like an **immersive botanical experience** — not a shop catalog. Premium, nature-inspired, editorial. Organic curved layouts, layered depth, botanical photography. Full design rules in §5 — mandatory for all pages.

---

## 👥 Business Information

- **Company:** Садовый питомник Pitomnik95
- **Niche:** Садовый питомник, декоративные и плодовые растения, газоны, хвойные, ландшафтный дизайн, садовая техника STIHL
- **Locations:**
  - Чеченская Республика, трасса Грозный–Аргун, 7 км
  - Чеченская Республика, ул. Патриса Лумумбы, 56
- **Working hours:** 9:00–17:00, без выходных
- **Target audience:** Владельцы частных домов и дач, ландшафтные дизайнеры, организации, заинтересованные в озеленении территорий
- **In business since:** 2012

### Business goals

- Предоставить широкий выбор растений, адаптированных к местному климату
- Предложить удобные способы покупки: доставка по республике и самовывоз
- Генерировать входящие заявки на ландшафтный дизайн и озеленение
- Развивать бренд питомника как лидера рынка в регионе

### Key selling points

- Более 1400 наименований растений и товаров
- Работа с проверенными поставщиками и мировыми лидерами садоводства
- Опыт с 2012 года
- Бесплатный выезд дизайнера
- Садовая техника STIHL в наличии
- Доставка по всей Чеченской Республике

### Contacts

| Channel | Value |
| --- | --- |
| Phone / WhatsApp | 8 (928) 393-33-33 |
| Email | pitomnik95@mail.ru |
| Telegram | t.me/ozelenenie\_95 |
| Instagram | instagram.com/pitomnik95 |
| Address 1 | Чеченская Республика, трасса Грозный–Аргун, 7 км |
| Address 2 | Чеченская Республика, ул. Патриса Лумумбы, 56 |

---

## 🔍 SEO

- **Primary keywords:** садовый питомник, декоративные растения, плодовые деревья, ландшафтный дизайн Грозный, озеленение участка, купить растения Чечня
- **Intent:** Transactional / Informational
- **Target regions:** Чеченская Республика, Грозный, соседние регионы
- **Notes:** Каждая страница — уникальный title, meta description, один H1, логическая иерархия заголовков

---

## 📑 Pages and URLs

| Page (RU) | URL | Notes |
| --- | --- | --- |
| Главная | `/` | Hero, about, services, catalog preview, stats, projects, CTA |
| Каталог | `/catalog/` | Все товары, фильтры по категории |
| ├─ Лиственные деревья | `/catalog/listvennye-derevya/` | Category |
| ├─ Хвойные растения | `/catalog/khvoinye/` | Category |
| ├─ Лиственные кустарники | `/catalog/kustarniki/` | Category |
| ├─ Многолетние растения | `/catalog/mnogoletniki/` | Category |
| ├─ Вьющиеся растения | `/catalog/vyushchiesya/` | Category |
| └─ Тропические и экзотические | `/catalog/ekzoticheskie/` | Category |
| Товар | `/catalog/{category}/{slug}/` | Product detail page |
| Галерея | `/gallery/` | Фото и видео работ |
| Услуги | `/services/` | Все услуги |
| ├─ Ландшафтный дизайн | `/services/landscape-design/` | Detail |
| ├─ Благоустройство участка | `/services/landscaping/` | Detail |
| └─ Озеленение | `/services/greening/` | Detail |
| Проекты | `/projects/` | Портфолио, новые сверху |
| └─ Проект | `/projects/{year}/{month}/{slug}/` | Case: до и после |
| Партнёры | `/partners/` | Партнёры и поставщики |
| О питомнике | `/about/` | О компании, миссия, преимущества |
| Новости / Блог | `/blog/` | Статьи |
| └─ Статья | `/blog/{slug}/` | Blog post |
| FAQ | `/faq/` | Вопросы и ответы |
| Контакты | `/contact/` | Карта, телефоны, мессенджеры |
| Политика конфиденциальности | `/privacy/` | Legal |
| Пользовательское соглашение | `/terms/` | Legal |

---

## ⚙️ Technical Stack

| Layer | Technology |
| --- | --- |
| Generator | Hugo (static site generator) |
| Frontend | HTML5, TailwindCSS, Alpine.js (where needed) |
| Backend / CMS | None |
| Data / Catalog | Hugo content files + `data/` JSON |
| Media | Hosted externally at `files.groznet.com/pitomnik95/` — URLs defined in JSON |
| Hosting | GitHub Pages |
| Versioning | GitHub |
| Analytics | Yandex Metrika |
| Integrations | WhatsApp, Telegram, Instagram |

### Media storage convention

This project follows the **Hugo Remote Media Architecture** — media lives locally during development and is served from `files.groznet.com` in production. The local Hugo project is the single source of truth; only the base URL changes at deploy time.

**Local development:** every content item is a Hugo page bundle with images stored alongside `index.md`:

```text
content/catalog/conifers/tuja-smaragd/
├── index.md
├── tuja-smaragd.jpg          # featured image (first image in bundle root)
└── images/                   # gallery images
    ├── a9QwT7nR.webp
    └── J4xMvP2k.jpg
```

**Production:** before deployment, a `media.json` is generated per bundle by scanning the local `images/` directory. It stores only filenames — templates construct full URLs by combining `remote_base_url + filename`:

```json
{
  "remote_base_url": "https://files.groznet.com/pitomnik95/catalog/conifers/tuja-smaragd/images/",
  "featured_image": "https://files.groznet.com/pitomnik95/catalog/conifers/tuja-smaragd/tuja-smaragd.jpg",
  "images": [
    "a9QwT7nR.webp",
    "J4xMvP2k.jpg"
  ]
}
```

Templates reference `{{ .featured_image }}` and loop over `{{ .images }}` — never hardcode full remote URLs in HTML or markdown.

**Deployment steps:**
1. Scan content directory for page bundles with images
2. Generate `media.json` per bundle from local `images/` directory
3. Build Hugo site
4. Deploy to GitHub Pages (repo stays lightweight — no binary media committed)

Media files must exist on `files.groznet.com/pitomnik95/` before or alongside deployment. To migrate hosting: change only `remote_base_url` — filenames and directory structure never change.

> See full architecture spec: `Hugo Remote Media Architecture` (attached reference doc)

### Hugo taxonomy mapping

| Taxonomy | Terms |
| --- | --- |
| `categories` | listvennye-derevya, khvoinye, kustarniki, mnogoletniki, vyushchiesya, ekzoticheskie |
| `services` | landscape-design, landscaping, greening |
| `tags` | free-form product tags |

Dated content (projects, blog) uses Hugo's built-in date ordering — newest first by default.

### Not planned

Live chat, online payments, cart, CRM. Chatbot and product reviews possible later.

---

## 📁 Project Structure

```
pitomnik95/
│
├── content/
│   ├── catalog/
│   │   └── {category}/
│   │       └── {slug}.md        # Plant / product pages
│   ├── projects/
│   │   └── {year}/{month}/
│   │       └── {slug}.md
│   ├── blog/
│   │   └── {year}/{month}/
│   │       └── {slug}.md
│   └── services/
│       └── {slug}.md
│
├── data/
│   ├── catalog.json             # Product list with external media URLs
│   ├── projects.json
│   ├── partners.json
│   └── settings.json            # Site-wide settings (phone, email, address)
│
├── layouts/
│   ├── _default/
│   ├── catalog/
│   ├── projects/
│   └── partials/
│       ├── header.html
│       ├── footer.html
│       ├── cta.html
│       └── ...
│
├── assets/
│   ├── css/
│   │   └── main.css             # Tailwind input file + custom CSS
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── visuals/             # Local decorative SVGs, overlays, textures
│
├── static/
│   └── favicon.ico
│
├── hugo.toml                    # Site config, taxonomies, permalinks
└── README.md
```

---

## 🎨 Design System

**Mandatory for all pages.** No exceptions.

### Core principle

Highly creative, nature-inspired, immersive botanical aesthetic. No straight horizontal layouts. Fluid, organic composition with curved layered shapes evoking natural terrain and forest depth.

Every page has three visual layers:
- **Background:** landscape gradients, sky, texture, grain overlays
- **Midground:** text and CTAs integrated into the environment — never boxed
- **Foreground:** leaves, branches, botanical SVG shapes, decorative silhouettes

Sections blend into each other with wave dividers, organic curves, asymmetric shapes — never hard horizontal lines or abrupt background changes.

### Tailwind configuration

Extend the default Tailwind config with these tokens. Choose final hex values to best match a deep botanical, premium garden aesthetic:

```js
// tailwind.config.js
module.exports = {
  content: ['./layouts/**/*.html', './assets/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        // Choose values that evoke: deep forest, moss, olive, warm beige, amber
        primary: '<deep-forest-green>',      // Main brand, headings, buttons
        'primary-dark': '<darker-forest>',   // Hover states, deep sections
        secondary: '<moss-or-olive>',        // Supporting elements
        accent: '<warm-gold-or-amber>',      // Highlights, icons, hover
        surface: '<warm-beige-or-sand>',     // Card backgrounds, light sections
        'surface-dark': '<dark-canopy>',     // Dark immersive sections
        muted: '<soft-gray-green>',          // Captions, metadata
      },
      fontFamily: {
        heading: ['Montserrat', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        organic: '40% 60% 55% 45% / 45% 55% 60% 40%', // Blob shapes
        wave: '0 0 50% 50% / 0 0 20px 20px',
      },
    },
  },
  plugins: [],
}
```

### Color palette direction

Pick colors that evoke:
- **Greens:** deep forest, moss, olive — rich and natural, not corporate lime
- **Neutrals:** warm beige, sand, linen — earthy, never cold gray
- **Accents:** warm gold or amber for highlights and hover states
- **Dark surfaces:** deep shade under a canopy, not flat black UI panels

Apply subtle gradients evoking sunlight filtering through leaves. No flat solid blocks — always blend, layer, transition.

### Typography

- **Headings:** Montserrat, semi-bold to bold. Expressive, large. Must integrate into the visual environment — can overlap imagery, sit on gradient overlays, emerge from organic shapes.
- **Body:** Inter, light and airy, 16px base, line-height 1.6
- **Optional serif accent:** Cormorant Garamond or Playfair Display for hero pull-quotes or large section headers
- **Rule:** Typography is never boxed. It lives inside the landscape.

### Layout rules

- No rigid grids. Use `clip-path`, SVG masks, `border-radius` for curved section edges
- Asymmetry is intentional. Avoid strict 12-column alignment
- Layered depth via `z-index`, `position: absolute`, organic clip shapes
- Sections must visually flow into each other: wave SVG dividers, overlapping shapes, blended backgrounds
- Generous negative space — don't fill every pixel

### Components

- **Buttons / CTAs:** Rounded, embedded into the layout. Accent color or semi-transparent green overlay. Never a plain rectangle on white.
- **Cards:** Rounded corners, imagery dominant, minimal text, soft botanical shadows
- **Dividers:** Wave SVG, leaf silhouette, or organic blob — never `<hr>`
- **Icons:** Botanical SVG for decoration; Font Awesome only for functional UI (phone, email, arrow)
- **Inputs:** Clean, accessible, green focus ring

### Motion

- Gentle fade-ins and slow upward reveals on scroll (`IntersectionObserver`)
- Soft parallax: background moves slower than foreground
- Floating animation on decorative leaf/branch elements
- Hover: `scale(1.02–1.04)`, smooth color transitions
- **Always respect `prefers-reduced-motion`**

### Imagery

- Close-up botanical: macro leaf, textured bark, stone, linen, sunlit paths, branch shadows
- Background images always `object-fit: cover` with gradient overlay for legibility
- Layer with grain textures, organic SVG shapes, blurred edges
- All media fetched from `files.groznet.com/pitomnik95/` — never embed local binary images in the repo

### Accessibility

- Semantic HTML5 throughout
- WCAG AA contrast minimum on all text, including over gradients
- Keyboard navigation friendly
- `alt` text on every image
- All motion respects `prefers-reduced-motion`

---

## 📋 Homepage Sections

| # | Section | Notes |
| --- | --- | --- |
| 1 | Hero | Cinematic, full-height, parallax, botanical layers, main CTA |
| 2 | About teaser | Short company intro, since 2012, 1400+ items, free designer visit |
| 3 | Services grid | Ландшафтный дизайн, Посадка растений, Уход за садом, Сезонные работы, Монтаж полива |
| 4 | Catalog preview | 8 categories with imagery |
| 5 | Why choose us | 5 advantages with icons |
| 6 | Stats | Projects done, years of experience, satisfied clients — real numbers |
| 7 | Projects preview | 3–5 latest portfolio cases, before/after |
| 8 | Partners | Partner logos carousel |
| 9 | Testimonials | 3 real client reviews |
| 10 | FAQ preview | 3 common questions |
| 11 | Blog preview | 3 latest articles |
| 12 | CTA | Contact call-to-action |
| 13 | Footer | Links, contacts, socials, legal |

---

## 🗂️ Projects Section (Portfolio)

Each project is a Hugo content file with front matter:

```yaml
---
title: "Озеленение частного двора, Гудермес"
date: 2026-08-15
location: "Гудермес, ЧР"
area: "450 м²"
services: [landscaping, greening]
before_image: "https://files.groznet.com/pitomnik95/projects/gudермес-2026/before.webp"
after_image: "https://files.groznet.com/pitomnik95/projects/gudермес-2026/after.webp"
gallery:
  - "https://files.groznet.com/pitomnik95/projects/gudермес-2026/01.webp"
video: ""
featured: true
summary: "Полное благоустройство участка с посадкой декоративных кустарников и укладкой газона."
---
```

Single project page structure:
1. Title, location, year, area
2. Before/after slider as main visual
3. Short story: задача, решение, использованные растения
4. Photo gallery + optional video
5. Services involved (links to service pages)
6. CTA to contact
7. Related projects

---

## 📝 Content Rules for AI Generation

- Use only this document as the source of facts. Do not invent prices, phone numbers, addresses, plant names or testimonials.
- Write original, professional Russian copy. No placeholder or lorem ipsum text.
- One H1 per page, unique title and meta description per page, natural keyword use.
- All media URLs must reference `files.groznet.com/pitomnik95/` — label any new asset clearly as a future asset with its proposed path.
- Reuse shared Hugo partials (header, footer, cta) by reference — never regenerate their content.
- Use Alpine.js only where it adds value (menus, accordions, filters, sliders, before/after slider). Plain HTML otherwise.
- Do not add frameworks or libraries unless asked.
- Output for page generation: the complete file only, no explanations.

### Forms directive (152-ФЗ)

All forms must be **visible but fully non-functional**. Apply `disabled` to every `<input>`, `<textarea>`, `<select>`, and `<button>`. Add this notice directly below every form:

```html
<div class="text-sm text-muted mt-3 border border-muted/30 rounded-lg px-4 py-3">
  Форма временно отключена. Данные не собираются и не обрабатываются
  в соответствии с ФЗ-152 «О персональных данных».
</div>
```

---

## 🌿 Reference Sites (Design & Industry)

Подборка «зелёных» сайтов схожей тематики — для вдохновения, анализа структуры и ориентира по дизайну:

| Site | URL |
| --- | --- |
| ВЕ-ЛЕС — питомник растений | https://ve-les.ru/ |
| Камыши — питомник | https://kamyshi-pitomnik.ru/ |
| Русиновский сад | https://rusinovsad.ru/ |
| БиоСад (Казахстан) | https://biosad.kz/ |
| Тамара Розы | https://tamararozi.ru/ |
| Живой Алтай | https://zhivoialtai.ru/ |
| Питомник Ахмечет | https://pitomnik-akhmechet.ru/ |
| Первоцвет | https://www.pervocvet-shop.ru/ |
| Древо Спас | https://www.drevo-spas.ru/ |
| Лавандовая ферма | https://lavender-farm.ru/ |

> Используй эти сайты как референс при принятии решений по структуре страниц, каталогу, подаче услуг и дизайн-деталям. Не копировать — брать лучшее и делать лучше.

---

## 🔄 Content Update Workflow

### Client contact

| Field | Value |
| --- | --- |
| Client (owner) | Аслан |
| Contact channel | Telegram (основной) |
| Developer | Kerim @ GrozNet |

### How updates flow

Аслан присылает новые материалы в Telegram:
- Новые товары и растения (фото + название + описание)
- Новые проекты (фото до/после + локация + площадь)
- Обновления цен, сезонные акции
- Новости и статьи для блога

Kerim получает материал, загружает медиа на `files.groznet.com/pitomnik95/`, создаёт или обновляет соответствующие Hugo content-файлы, деплоит.

### Streamlined intake (цель)

Настроить максимально простой pipeline, чтобы клиент не думал о техническом процессе:

| Step | Tool / Method |
| --- | --- |
| Клиент присылает контент | Telegram-сообщение или альбом фото |
| Kerim принимает | Telegram (личка или выделенный чат проекта) |
| Медиа → сервер | Загрузка на `files.groznet.com/pitomnik95/` по структуре проекта |
| Контент → Hugo | Новый `.md` файл в нужной папке (`catalog/`, `projects/`, `blog/`) |
| Деплой | `git push` → GitHub Actions → GitHub Pages |
| Отчёт клиенту | Kerim сообщает Аслану: что добавлено, что опубликовано |

### Reporting to client

После каждого значимого обновления Kerim сообщает Аслану:
- Что именно добавлено / изменено
- Ссылку на обновлённую страницу
- Статус проекта (в разработке / опубликовано)

Аслан не вникает в технический процесс — получает только результат.

### Automation ideas (на перспективу)

- Telegram-бот для приёма контента от Аслана с автоматической загрузкой медиа
- GitHub Actions скрипт для auto-deploy при изменениях в `main`
- Шаблон сообщения для Аслана: что присылать и в каком формате (формат фото, описание, локация и т.д.)

---

## ✅ Open Decisions

| # | Question | Current thinking |
| --- | --- | --- |
| 1 | Client name (owner) | Уточнить у клиента |
| 2 | YouTube channel URL | Уточнить |
| 3 | VK page URL | Уточнить |
| 4 | Exact number of product SKUs | Сайт говорит 1400+, уточнить |
| 5 | Pricing section: keep or drop? | На живом сайте есть monthly/annual — решить нужно ли это |
| 6 | Gallery: separate page or part of projects? | Пока отдельная страница |
| 7 | Partners page content | Нужен список партнёров от клиента |
| 8 | Launch date | Не установлена |

---

## 🗓️ Timeline

- Project start: Nov 2026
- Spec drafted: 23 Nov 2026
- Launch: not set

---

## 👤 Developer

- **Developer:** Kerim @ GrozNet
- **Email:** info@groznet.com
- **GitHub:** github.com/groznet
- **Site:** groznet.com