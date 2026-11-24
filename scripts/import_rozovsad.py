#!/usr/bin/env python3
"""Import products from https://rozovsad.ru/catalog into Hugo page bundles.

Each product becomes  content/catalog/{pitomnik-category}/{product-slug}/
    index.md     front matter + description
    media.json   remote base URL (files.groznet.com) + image filenames
    images/      downloaded gallery images (git-ignored)

Usage:
    python3 scripts/import_rozovsad.py                       # full import, pages 1-57
    python3 scripts/import_rozovsad.py --only <product-url>  # import a single product (test)
Requires: requests, beautifulsoup4, transliterate
"""
import argparse
import json
import pathlib
import re
import sys
import time
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from transliterate import translit

BASE = "https://rozovsad.ru"
REMOTE = "https://files.groznet.com/pitomnik95/catalog"
ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "catalog"
LOG_FILE = ROOT / "scripts" / "import_log.json"
TOTAL_PAGES = 57
PAGE_DELAY = 1.0    # seconds between product-page requests
IMAGE_DELAY = 0.5   # seconds between image downloads

# rozovsad.ru category slug -> Pitomnik95 category slug
CATEGORY_MAP = {
    "listevennie-rasteniya": "listvennye-derevya",
    "hvoinei-rasteniya": "khvoinye",
    "listevennie-kustarniki": "kustarniki",
    "mnogoletnie-rasteniya": "mnogoletniki",
    "vishiesya-rasteniya": "vyushchiesya",
    "tropicheskiy-rasteniya": "ekzoticheskie",
}

# property name on the source page -> front matter key
SPEC_FIELDS = {
    "Высота": "height",
    "Ширина": "width",
    "Зимостойкость": "frost_zone",
    "Освещенность": "light",  # the site spells it without «ё»; names are compared with ё→е
    "Осенняя окраска листа": "autumn_color",
    "Форма кроны": "crown_shape",
}

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (compatible; catalog-import/1.0)"


def get(url, timeout=30, attempts=3):
    """GET with retries (timeouts / 5xx); raises on the final failure."""
    for attempt in range(1, attempts + 1):
        try:
            r = session.get(url, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt == attempts:
                raise
            time.sleep(2 * attempt)


def fetch(url):
    """GET a page and return parsed HTML (raises on HTTP errors)."""
    return BeautifulSoup(get(url).text, "html.parser")


def slugify(title):
    """'Аир болотный Вариегата' -> 'air-bolotnyy-variegata'."""
    latin = translit(title, "ru", reversed=True).lower().replace("j", "y")
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", latin)).strip("-")


def to_int(text):
    """'4 590 ₽' -> 4590 (None when there are no digits)."""
    digits = re.sub(r"\D", "", text or "")
    return int(digits) if digits else None


def clean_spec(key, text):
    """'От -29,0 до -34,4 (Зона 4)' -> 'Зона 4' (format used in IMPORT_PROMPT.md); other fields unchanged."""
    if key == "frost_zone":
        m = re.search(r"Зона\s*\d+", text)
        return m.group(0) if m else text
    return text


def clean_size(text):
    """'40-60 см ( Контейнер С60 )' -> '40-60 см (Контейнер С60)'."""
    return re.sub(r"\s+([)])", r"\1", re.sub(r"([(])\s+", r"\1", " ".join(text.split())))


def yaml_str(value):
    """Double-quoted YAML scalar (JSON string syntax is valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


# ───────────────────────── listing pages ─────────────────────────
PRODUCT_HREF = re.compile(r"^/catalog/[^/]+/product\d+/?$")


def collect_product_urls(pages):
    """Return (urls, failures) from /catalog?page=N for every N in `pages` (order kept, no duplicates).

    NOTE: on the live site `.card-product` is a wrapper element, not the <a> itself (the
    `a.card-product[href]` selector from IMPORT_PROMPT.md matches nothing), so we take every link
    inside a `.card-product` whose path looks like /catalog/{cat}/productNNNN.
    """
    urls, failures = [], []
    for n in pages:
        page_url = f"{BASE}/catalog?page={n}"
        try:
            soup = fetch(page_url)
            links = [urljoin(BASE, a["href"]) for a in soup.select(".card-product a[href], a.card-product[href]")
                     if PRODUCT_HREF.match(urlparse(urljoin(BASE, a["href"])).path)]
            if not links:
                raise ValueError("no product links found on listing page")
        except Exception as exc:  # a failed listing page must not stop the whole import
            print(f"✗ {page_url} — {exc}")
            failures.append({"url": page_url, "error": str(exc)})
            continue
        new = [u for u in dict.fromkeys(links) if u not in urls]
        print(f"page {n}/{TOTAL_PAGES}: {len(new)} products")
        urls += new
        time.sleep(PAGE_DELAY)
    return urls, failures


# ───────────────────────── product page ─────────────────────────
def parse_product(url, soup):
    """Extract every field described in IMPORT_PROMPT.md from a product detail page."""
    parts = [p for p in urlparse(url).path.split("/") if p]  # ['catalog', '{cat}', 'productNNNN']
    if len(parts) < 3 or parts[1] not in CATEGORY_MAP:
        raise ValueError(f"unknown category in URL: {url}")
    h1 = soup.select_one("h1.page-content__title")
    if h1 is None:
        raise ValueError("title (h1.page-content__title) not found")
    span = h1.find("span")
    title = " ".join("".join(h1.find_all(string=True, recursive=False)).split())  # text nodes only
    if not title:
        raise ValueError("empty title")

    product = {
        "title": title,
        "latin_name": " ".join(span.get_text().split()).strip("() ") if span else "",
        "category": CATEGORY_MAP[parts[1]],
        "source_id": parts[2],
        "source_url": url,
    }

    for art in soup.select(".page-properties__list article.property"):
        name = art.select_one(".property__name")
        value = art.select_one(".property__value")
        key = SPEC_FIELDS.get(name.get_text(strip=True).replace("ё", "е")) if name else None
        if key and value:
            product[key] = clean_spec(key, " ".join(value.get_text().split()))

    variants = []
    for offer in soup.select(".page-offers__list .page-offer"):
        size = offer.select_one(".page-offer__title")
        price = to_int(offer.select_one(".page-offer__price").get_text()) if offer.select_one(".page-offer__price") else None
        if size and price:
            variants.append({"size": clean_size(size.get_text()), "price": price})
    product["price_variants"] = variants
    if variants:
        low = min(v["price"] for v in variants)
        product["price"] = low
        product["price_label"] = f"от {low:,}".replace(",", " ") + " ₽/шт"

    paragraphs = [" ".join(p.get_text().split()) for p in soup.select(".accordion__body.rich-text p")]
    product["description"] = "\n\n".join(p for p in paragraphs if p)

    seen = []
    for a in soup.select("#page-gallery .page-gallery-preview a.swiper-slide[href], #page-gallery .page-gallery-preview .swiper-slide a[href]"):
        src = urljoin(BASE, a["href"])
        # products without photos carry a placeholder link to the bare media folder: skip non-image links
        if not re.search(r"\.(jpe?g|png|webp|avif|gif)$", urlparse(src).path, re.I):
            continue
        if src not in seen:
            seen.append(src)
    product["gallery"] = seen
    return product


def download_images(urls, dest):
    """Download gallery images (original filenames); returns the filenames that exist locally."""
    dest.mkdir(parents=True, exist_ok=True)
    names = []
    for src in urls:
        name = pathlib.Path(unquote(urlparse(src).path)).name
        target = dest / name
        if not target.exists():
            target.write_bytes(get(src, timeout=60).content)
            time.sleep(IMAGE_DELAY)
        names.append(name)
    return names


def write_index(bundle, p):
    """index.md: front matter in the field order of IMPORT_PROMPT.md, then the description."""
    lines = ["---", f"title: {yaml_str(p['title'])}"]
    if p["latin_name"]:
        lines.append(f"latin_name: {yaml_str(p['latin_name'])}")
    lines += [
        f"category: {yaml_str(p['category'])}",
        f"source_id: {yaml_str(p['source_id'])}",
        f"source_url: {yaml_str(p['source_url'])}",
    ]
    if p["price_variants"]:
        lines += [f"price: {p['price']}", f"price_label: {yaml_str(p['price_label'])}", "price_variants:"]
        for v in p["price_variants"]:
            lines += [f"  - size: {yaml_str(v['size'])}", f"    price: {v['price']}"]
    for key in SPEC_FIELDS.values():
        if key in p:
            lines.append(f"{key}: {yaml_str(p[key])}")
    lines += ["draft: false", "---", "", p["description"], ""]
    (bundle / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_media_json(bundle, p, slug, filenames):
    """media.json: remote base URL + local filenames; featured_image = first image (full remote URL)."""
    base = f"{REMOTE}/{p['category']}/{slug}/images/"
    media = {
        "remote_base_url": base,
        "featured_image": base + filenames[0] if filenames else "",
        "images": filenames,
    }
    (bundle / "media.json").write_text(json.dumps(media, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def import_product(url):
    """Import one product. Returns the slug, or None when it already exists (skipped)."""
    p = parse_product(url, fetch(url))
    slug = slugify(p["title"])
    bundle = CONTENT / p["category"] / slug
    if (bundle / "index.md").exists():
        return None
    filenames = download_images(p["gallery"], bundle / "images")
    write_index(bundle, p)
    write_media_json(bundle, p, slug, filenames)
    return slug


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", metavar="URL", help="import just this product URL (used for the test run)")
    args = ap.parse_args()

    if args.only:
        urls, listing_failures = [args.only], []
    else:
        urls, listing_failures = collect_product_urls(range(1, TOTAL_PAGES + 1))
    log = {"total": len(urls), "success": 0, "failed": list(listing_failures)}
    try:
        for i, url in enumerate(urls, 1):
            try:
                slug = import_product(url)
                if slug is None:
                    print(f"- skipped (exists) {url}")
                else:
                    log["success"] += 1
                    print(f"✓ {slug}")
            except Exception as exc:
                log["failed"].append({"url": url, "error": str(exc)})
                print(f"✗ {url} — {exc}")
            if i < len(urls):
                time.sleep(PAGE_DELAY)
    finally:
        LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"done: {log['success']}/{log['total']} imported, {len(log['failed'])} failed → {LOG_FILE.name}")
    return 1 if log["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
