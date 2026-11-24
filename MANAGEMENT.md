# Pitomnik95 — инструкция по работе с сайтом

Сайт — статический (Hugo + Tailwind CSS + Alpine.js). Базы данных и админки нет: всё хранится в файлах проекта. Чтобы что-то изменить, правится файл, затем сайт пересобирается и публикуется.

---

## 1. Запуск и сборка

Нужно один раз установить: [Hugo extended](https://gohugo.io/installation/) и Node.js.

```bash
npm install          # один раз, ставит Tailwind
npm run dev          # локальный просмотр: http://localhost:1313 (с автообновлением)
npm run build        # боевая сборка в папку public/
```

> `npm run dev` один раз собирает CSS. Если вы **добавили новые классы Tailwind** в шаблоны, во время разработки запускайте в соседнем терминале `npm run css:watch`. Перед публикацией всегда выполняйте `npm run build` — он пересобирает CSS.

Файл `static/css/site.css` генерируется автоматически. Руками его не правят — стили правятся в `assets/css/main.css` и `tailwind.config.js`.

---

## 2. Структура проекта

```
content/      страницы и тексты (Markdown), в т.ч. товары каталога
data/         данные: FAQ, партнёры, отзывы, контакты, меню, ключи картинок
layouts/      шаблоны страниц и общие блоки (partials)
assets/       CSS (main.css) и JS (main.js)
static/       файлы «как есть»: favicon, логотип (static/images)
hugo.toml     настройки сайта
```

---

## 3. Типовые задачи

### 3.1 Контакты, график, адреса
Файл `data/settings.json`: телефон, WhatsApp, Telegram, Instagram, e-mail, график, адреса, год основания, число позиций. Меняется один раз — обновится во всём сайте (шапка, подвал, CTA, контакты).

### 3.2 Меню
Файл `data/nav.json`: пункты главного меню и список категорий каталога.

### 3.3 Товары каталога (импорт и ручное добавление)
Каждый товар — папка `content/catalog/<категория>/<slug>/` с `index.md`, `media.json` и папкой `images/` (адрес `/catalog/<категория>/<slug>/`). Категории: `listvennye-derevya`, `khvoinye`, `kustarniki`, `mnogoletniki`, `vyushchiesya`, `ekzoticheskie` (список — `data/nav.json`).

Основной каталог (573 товара) загружен скриптом `python3 scripts/import_rozovsad.py` (уже существующие товары пропускаются; журнал — `scripts/import_log.json`). Формат `index.md`:

```yaml
---
title: "Аир болотный Вариегата"
latin_name: "Acorus calamus Variegatus"
category: "mnogoletniki"
source_id: "product2766"        # ID товара на сайте-источнике
source_url: "https://rozovsad.ru/catalog/..."
price: 4590                     # минимальная цена
price_label: "от 4 590 ₽/шт"
price_variants:                 # размеры и цены (пусто — «Цена по запросу»)
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
Текст «О растении» в Markdown.
```

- Все поля, кроме `title` и `category`, необязательны: пустые просто не показываются.
- Фото задаются **не в front matter**, а в папке `images/` и `media.json` (раздел 4a). У части товаров (133) на сайте-источнике нет фото — показывается нейтральная картинка-заглушка.
- Карточки в категориях ведут на страницу товара автоматически; в категориях по 24 товара на страницу.
- Кнопка «Заказать в WhatsApp» берёт номер из `data/settings.json` и подставляет название и выбранный размер.
- «Также в категории» показывает другие товары той же категории.
- Описания взяты с сайта-источника: проверьте права на использование и тексты, привязанные к другим регионам (например, «в условиях Подмосковья»).

### 3.4 Описание категории каталога
`content/catalog/<категория>/_index.md`: заголовок, `description` (для поиска), `lead` (подзаголовок), `points` (3 пункта), текст ниже — основной абзац.

### 3.5 Новый проект (до/после)
Создайте папку `content/projects/<slug>/` и файл `index.md`:

```yaml
---
title: "Озеленение частного двора, Гудермес"
description: "Короткое описание для поиска"
date: 2026-08-15
location: "Гудермес, ЧР"
area: "450 м²"
slug: "gudermes-2026"              # латиницей, обязательно
services: [landscaping, greening]   # landscape-design | landscaping | greening
before_image: "ключ-фото-до"
after_image: "ключ-фото-после"
gallery: ["ключ1", "ключ2", "ключ3"]
featured: true
summary: "Одно предложение для карточки."
---
## Задача
...
## Решение
...
## Использованные растения
- ...
```

Адрес страницы формируется автоматически: `/projects/ГОД/МЕСЯЦ/slug/`. Новые проекты показываются первыми (по `date`). Строку `demo: true` удалите у реальных проектов — у демо она показывает пометку «демонстрационный проект».
Два демо-проекта (`gudermes-2026`, `argun-2026`) нужно заменить или удалить.

### 3.6 Новая статья в блог
Папка `content/blog/<slug>/`, файл `index.md`:

```yaml
---
title: "Заголовок статьи"
description: "Описание для поиска, 1–2 предложения"
date: 2026-11-20
category: "Советы"
hero: "ключ-картинки"
---
Текст в Markdown. ## — подзаголовок, - — список, **жирный**.
```

Адрес: `/blog/<slug>/` (латиницей, через дефис). Последние 3 статьи автоматически попадают на главную.

### 3.6a Услуги
`content/services/<slug>/index.md`: `lead`, шаги `steps`, список `includes`, фото `before_image` / `after_image`. Три услуги: `landscape-design`, `landscaping`, `greening`.

### 3.7 FAQ, партнёры, отзывы
- Вопросы и ответы: `data/faq.json` (первые 3 показываются на главной, все — на `/faq/`; для поиска автоматически добавляется разметка FAQ).
- Партнёры: `data/partners.json`. У реального партнёра уберите `"pending": true` и укажите название. Для логотипов потребуется доработать шаблон `layouts/index.html` и `layouts/_default/partners.html` (сейчас показано название текстом).
- Отзывы: `data/testimonials.json`. Публикуйте **только реальные отзывы** клиентов; уберите `"pending": true`.

### 3.8 Тексты страниц
`content/about`, `content/contact`, `content/partners`, `content/faq`, `content/gallery`, `content/privacy`, `content/terms`: в `index.md` правятся заголовок, `description` и `lead`. Основные блоки «О питомнике» и «Контакты» находятся в шаблонах `layouts/_default/about.html` и `contact.html`.

### 3.9 Правила для текстов (SEO)
- У каждой страницы свой `title` и `description`; на странице один H1 (создаётся из `title`).
- Не выдумывать цены, адреса, телефоны, названия растений и отзывы — только факты от клиента.

### 3.10 Галерея
Список фото задан в `layouts/_default/gallery.html` (переменная `$g`: категория `k`, ключ картинки `i`, подпись `a`). Добавьте строку по образцу существующих.

---

## 4. Картинки

Сейчас для разработки используются фото Unsplash. Адреса не хранятся в шаблонах — только **ключи** в `data/images.json`:

```json
"rose-path": "1585320806297-9794b3e4eeae"
```

В шаблонах и в тексте используйте ключ (`rose-path`), а не адрес.

### 4a. Фото товаров (медиа-процесс)
Каждый товар — папка-бандл:

```
content/catalog/khvoinye/tuya-smaragd/
├── index.md
├── images/               # фото галереи; первое фото — обложка (карточка)
└── media.json            # генерируется скриптом, лежит в Git
```

1. Положите фото в `images/` локально (первое по алфавиту — обложка).
2. Выполните `python3 scripts/generate-media.py` — создаст/обновит `media.json` у всех товаров: базовый адрес `https://files.groznet.com/pitomnik95/catalog/<категория>/<slug>/images/` + имена файлов. Другой хостинг: `--base https://новый-адрес`.
3. Загрузите те же файлы на `files.groznet.com/pitomnik95/` по тому же пути.
4. Шаблоны берут адреса фото **только из `media.json`**. В режиме разработки (`npm run dev`) фото берутся из локальных папок, в боевой сборке (`npm run build`) — с `files.groznet.com`. Принудительно: `media_mode = "local"` или `"remote"` в `[params]` в `hugo.toml`.
5. Папки `images/` и `.jpg/.webp/.png` внутри `content/catalog` занесены в `.gitignore` — в репозиторий не попадают; `media.json` попадает.

> Боевая сборка до загрузки файлов на сервер покажет битые картинки товаров — сначала загрузите фото.

Остальные картинки сайта (шапки страниц, услуги, блог, проекты) пока берутся по ключам из `data/images.json` (Unsplash) или через `media_base`.

### Переход на files.groznet.com (боевой режим)
1. Загрузите файлы на `https://files.groznet.com/pitomnik95/` в формате `.webp`, имя файла = ключ (например, `rose-path.webp`).
2. В `hugo.toml` в `[params]` укажите:
   ```toml
   media_base = "https://files.groznet.com/pitomnik95/"
   ```
3. Все адреса картинок станут `media_base + ключ + .webp`. Менять шаблоны не нужно. При переезде на другой хостинг меняется только `media_base`.

Новый ключ можно добавить сразу в `data/images.json` (значение — id Unsplash) или, в боевом режиме, просто использовать имя загруженного файла как ключ.

> Реальные фото клиента загружайте на сервер, а не в репозиторий — бинарные файлы в Git не хранятся. Исключение — логотип и favicon в `static/`.

---

## 5. Логотип
- `static/images/logo.png` — оригинал (тёмный текст).
- `static/images/logo-light.png` — вариант для тёмного фона (белый текст, зелёная иконка); именно он используется в шапке, мобильном меню и подвале. Подключается в `layouts/partials/logo.html`.
- Если логотип обновится: замените файлы и проверьте размеры в `logo.html`.

---

## 6. Формы и ФЗ-152
Все формы на сайте **отключены**: у каждого `input`, `textarea`, `select`, `button` стоит `disabled`, под формой — обязательное уведомление об отключении. Не включайте формы, пока не будут готовы согласие на обработку данных и обновлённая политика конфиденциальности (`content/privacy/index.md`). Сейчас заявки принимаются по телефону, WhatsApp и Telegram.

Документы «Политика конфиденциальности» и «Пользовательское соглашение» — рабочие редакции, перед запуском их должен проверить юрист.

---

## 7. Яндекс Метрика
В `hugo.toml`: `ym_id = "XXXXXXXX"` — подставьте номер счётчика. Код выводится только в боевой сборке (`npm run build`), в режиме разработки счётчик не подключается.

---

## 8. Публикация (GitHub Pages)

Схема: `git push` → GitHub Actions собирает сайт → GitHub Pages публикует. Пример `.github/workflows/deploy.yml` (в проект пока не добавлен):

```yaml
name: Deploy
on:
  push: { branches: [main] }
permissions: { contents: read, pages: write, id-token: write }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci
      - uses: peaceiris/actions-hugo@v3
        with: { hugo-version: 'latest', extended: true }
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with: { path: public }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages }
    steps:
      - uses: actions/deploy-pages@v4
```

Для домена `pitomnik95.ru` добавьте файл `static/CNAME` с содержимым `pitomnik95.ru` и настройте DNS по инструкции GitHub Pages. В репозитории включите Pages → Source: GitHub Actions. Папки `public/`, `resources/` и `node_modules/` в Git не добавляйте (внесите в `.gitignore`).

---

## 9. Как обновлять сайт по материалам клиента (Аслан)

1. Клиент присылает материалы в Telegram: фото, название, описание, локацию, площадь.
2. Загрузить фото на `files.groznet.com/pitomnik95/`.
3. Создать/изменить файлы: товар → папка в `content/catalog/…`, проект → `content/projects/…`, статья → `content/blog/…`.
4. Проверить локально (`npm run dev`), затем `git push`.
5. Сообщить клиенту: что добавлено, ссылку на страницу, статус.

---

## 10. Чек-лист перед запуском
- [ ] Проверить импортированный каталог (описания, цены), заменить демо-проекты, партнёров и отзывы реальными данными.
- [ ] Указать `media_base` и загрузить фото на сервер.
- [ ] Указать номер Яндекс Метрики.
- [ ] Юридическая проверка политики и соглашения.
- [ ] Проверить телефоны, адреса и график в `data/settings.json`.
- [ ] Добавить `static/CNAME`, `.gitignore`, workflow публикации.
- [ ] Проверить сайт на телефоне и в разных браузерах.
- [ ] Добавить `title`/`description` для новых страниц.
