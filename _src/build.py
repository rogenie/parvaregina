#!/usr/bin/env python3
"""Builds the static Parva Regina site from _src/ into the repo root.
Run from the repo root:  python3 _src/build.py
Jekyll ignores folders starting with "_", so _src is not published."""
import os, json, html, datetime, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from pages import SITE, PAGES, nl_block
from articles import ARTICLES
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = os.environ.get("PR_TODAY") or datetime.datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()

def esc(s): return html.escape(s, quote=True)
def plain(s): return html.unescape(re.sub(r"<[^>]+>", "", s))

CROWN = ('<svg width="30" height="30" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 44 L17 22 L25 32 L32 16 L39 32 L47 22 L50 44 Z" fill="none" '
         'stroke="#C9A46A" stroke-width="3.4" stroke-linejoin="round"/><line x1="14" y1="50" x2="50" y2="50" stroke="#C9A46A" stroke-width="3.4" stroke-linecap="round"/>'
         '<circle cx="32" cy="13" r="2.8" fill="#C9A46A"/><circle cx="16.5" cy="19.5" r="2.3" fill="#C9A46A"/><circle cx="47.5" cy="19.5" r="2.3" fill="#C9A46A"/></svg>')

def layout(p):
    url = SITE["url"] + p["path"]
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE["url"]+"/"}]
    if p.get("hub"):
        crumbs.append({"@type":"ListItem","position":2,"name":p["hub_name"],"item":SITE["url"]+p["hub"]})
    if p["path"] != "/":
        crumbs.append({"@type":"ListItem","position":len(crumbs)+1,"name":plain(p["h1"]),"item":url})
    ld = [{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs}]
    org = {"@type":"Organization","name":SITE["name"],"url":SITE["url"]+"/","logo":SITE["url"]+"/assets/favicon.svg",
           "sameAs":[SITE["tiktok"]],"publishingPrinciples":SITE["url"]+"/editorial-policy/"}
    if p["path"] == "/":
        ld.append({"@context":"https://schema.org","@type":"WebSite","name":SITE["name"],"url":SITE["url"]+"/","description":SITE["desc"]})
        ld.append({"@context":"https://schema.org", **org})
    if p.get("article"):
        ld.append({"@context":"https://schema.org","@type":"NewsArticle" if p["hub"]=="/news/" else "Article","headline":plain(p["h1"]),"description":p["desc"],
                   "author":{"@type":"Organization","name":SITE["author"],"url":SITE["url"]+"/about/"},"publisher":org,
                   "image":SITE["url"]+p.get("og_image","/assets/og/default.png"),
                   "datePublished":p["published"],"dateModified":p.get("reviewed",p["published"]),"mainEntityOfPage":url})
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if p["path"].startswith(h) else ""}>{esc(n)}</a>' for h,n in SITE["nav"])
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else '<meta name="robots" content="max-image-preview:large">'
    og = p.get("og_image", "/assets/og/default.png")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<link rel="canonical" href="{url}">
{robots}
<meta property="og:type" content="{"article" if p.get("article") else "website"}">
<meta property="og:site_name" content="{SITE["name"]}">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE["url"]}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(plain(p["h1"]))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE["url"]}{og}">
<meta name="theme-color" content="#2A1B2D">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Inter:wght@400;600&display=swap">
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/rss+xml" title="Parva Regina" href="/feed.xml">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap bar">
<a class="brand" href="/">{CROWN}<span>Parva Regina</span></a>
<nav aria-label="Main">{nav}<a class="nl" href="/newsletter/">Newsletter</a></nav>
</div></header>
<main id="main">
{p["body"]}
</main>
<footer class="site"><div class="wrap">
<div class="fgrid">
<div><b>Parva Regina</b><p>Evidence-based longevity science for women 35+. Every claim linked to its source.</p><a href="/newsletter/">The Little Queen Brief (free)</a><a href="{SITE["tiktok"]}" target="_blank" rel="noopener">TikTok @parvaregina</a><a href="/feed.xml">RSS feed</a></div>
<div><b>Read</b>{"".join(f'<a href="{h}">{esc(n)}</a>' for h,n in SITE["nav"][:3])}</div>
<div><b>Trust</b><a href="/editorial-policy/">Editorial policy</a><a href="/corrections/">Corrections</a><a href="/about/">About</a><a href="/privacy/">Privacy</a></div>
</div>
<p class="legal">Wellness education, not medical advice. We&rsquo;re not doctors; talk to your clinician before starting a supplement or changing your care. Studies can be wrong and science changes; check the date and sources on each article. &middot; &copy; {datetime.date.today().year} Parva Regina, published by {SITE["publisher"]}</p>
</div></footer>
</body>
</html>
'''

def card_list(arts):
    out = '<div class="cards">'
    for a in arts:
        ev = f'<span class="ev {a["evidence"][0]}">{a["evidence"][1]}</span> ' if a.get("evidence") else ""
        out += f'<a class="card" href="{a["path"]}"><p class="eyebrow">{a["hub_name"]} &middot; {fmt_date(a["published"])}</p><h3>{a["h1"]}</h3><p>{a["desc"]}</p><p style="margin-top:10px">{ev}</p></a>'
    return out + '</div>'

def fmt_date(d):
    return datetime.date.fromisoformat(d).strftime("%b %-d, %Y")

def main():
    live = sorted([a for a in ARTICLES if a["published"] <= TODAY], key=lambda a: a["published"], reverse=True)
    live_paths = {a["path"] for a in live}
    cal = json.load(open(os.path.join(ROOT, "_src", "calendar.json"), encoding="utf-8"))
    all_paths = {a["path"] for a in ARTICLES} | {i["path"] for i in cal["items"]}
    def unlink_future(body):
        def f(m):
            return m.group(2) if (m.group(1) in all_paths and m.group(1) not in live_paths) else m.group(0)
        return re.sub(r'<a href="(/[^"#]+)">(.*?)</a>', f, body)
    corr_path = os.path.join(ROOT, "_src", "corrections.json")
    corrections = json.load(open(corr_path, encoding="utf-8")) if os.path.exists(corr_path) else []
    pages = []
    for p in PAGES:
        p = dict(p)
        if "<!--HUB_ARTICLES-->" in p["body"]:
            mine = [a for a in live if a["hub"] == p["path"]]
            p["body"] = p["body"].replace("<!--HUB_ARTICLES-->", card_list(mine) if mine else '<p class="muted">The first articles in this section are on their way.</p>')
        if "<!--LATEST-->" in p["body"]:
            p["body"] = p["body"].replace("<!--LATEST-->", ('<section><div class="wrap"><h2>Latest</h2>' + card_list(live[:6]) + '</div></section>') if live else "")
        if "<!--CORRECTIONS-->" in p["body"]:
            rows = "".join(f'<li><b>{fmt_date(c["date"])}</b>: <a href="{c["path"]}">{c["title"]}</a>. {c["note"]}</li>' for c in sorted(corrections, key=lambda c: c["date"], reverse=True))
            p["body"] = p["body"].replace("<!--CORRECTIONS-->", f"<ul>{rows}</ul>" if rows else "<p>No corrections yet.</p>")
        pages.append(p)
    from og import make_card
    og_dir = os.path.join(ROOT, "assets", "og")
    make_card(os.path.join(og_dir, "default.png"), "Longevity science for women 35+, without the hype")
    for p in pages:
        if p["path"] not in ("/", "/404") and not p.get("noindex"):
            img = "page-" + p["path"].strip("/").replace("/", "-") + ".png"
            if make_card(os.path.join(og_dir, img), p["h1"]) or os.path.exists(os.path.join(og_dir, img)):
                p["og_image"] = "/assets/og/" + img
    for a in live:
        a = dict(a); a["body"] = unlink_future(a["body"]).replace("<!--NEWSLETTER-->", nl_block(a["path"].strip("/").split("/")[-1]))
        img = a["path"].strip("/").split("/")[-1] + ".png"
        if make_card(os.path.join(og_dir, img), a["h1"], a["hub_name"]) or os.path.exists(os.path.join(og_dir, img)):
            a["og_image"] = "/assets/og/" + img
        pages.append(a)
    for a in ARTICLES:
        if a["path"] not in live_paths:
            f = os.path.join(ROOT, a["path"].strip("/"), "index.html")
            if os.path.exists(f): os.remove(f)
    urls = []
    for p in pages:
        out = os.path.join(ROOT, p["path"].strip("/"), "index.html") if p["path"] != "/404" else os.path.join(ROOT, "404.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(layout(p))
        if not p.get("noindex"): urls.append((SITE["url"]+p["path"], p.get("reviewed", TODAY)))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    items = "".join(
        f"<item><title>{esc(plain(a['h1']))}</title><link>{SITE['url']}{a['path']}</link><guid>{SITE['url']}{a['path']}</guid>"
        f"<pubDate>{datetime.datetime.fromisoformat(a['published']).strftime('%a, %d %b %Y 06:00:00 -0800')}</pubDate>"
        f"<description>{esc(plain(a['desc']))}</description></item>" for a in live[:30])
    open(os.path.join(ROOT, "feed.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
        f"<title>Parva Regina</title><link>{SITE['url']}/</link><description>{esc(SITE['desc'])}</description><language>en-us</language>"
        + items + "</channel></rss>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    written = {a["path"] for a in ARTICLES}
    rows = []
    for i in cal["items"]:
        st = "held" if i.get("status") == "held" else ("written" if i["path"] in written or i.get("status") in ("written", "published") else "todo")
        row = {"date": i["date"], "hub": i["hub"], "status": st}
        if i["path"] in live_paths:
            row.update(title=plain(i["title"]), url=SITE["url"] + i["path"])
        rows.append(row)
    runs_path = os.path.join(ROOT, "_src", "runs.json")
    runs = json.load(open(runs_path, encoding="utf-8")) if os.path.exists(runs_path) else []
    json.dump({"built": TODAY, "cadence": cal.get("cadence"), "items": rows, "runs": runs},
              open(os.path.join(ROOT, "status.json"), "w", encoding="utf-8"), indent=1)
    print("built", len(pages), "pages;", len(live), "live articles; today", TODAY)

if __name__ == "__main__": main()
