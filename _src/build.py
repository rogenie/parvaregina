#!/usr/bin/env python3
"""Builds the static Parva Regina site from _src/ into the repo root.
Run from the repo root:  python3 _src/build.py
Jekyll ignores folders starting with "_", so _src is not published."""
import os, json, html, datetime, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from pages import SITE, PAGES, nl_block, offer_for
from articles import ARTICLES
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = os.environ.get("PR_TODAY") or datetime.datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()

import hashlib
def _v(rel): return hashlib.md5(open(os.path.join(ROOT, rel),'rb').read()).hexdigest()[:8]

def esc(s): return html.escape(s, quote=True)
def plain(s): return html.unescape(re.sub(r"<[^>]+>", "", s))

CROWN = ('<svg width="30" height="30" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 44 L17 22 L25 32 L32 16 L39 32 L47 22 L50 44 Z" fill="none" '
         'stroke="#E2C08A" stroke-width="3.4" stroke-linejoin="round"/><line x1="14" y1="50" x2="50" y2="50" stroke="#E2C08A" stroke-width="3.4" stroke-linecap="round"/>'
         '<circle cx="32" cy="13" r="2.8" fill="#E2C08A"/><circle cx="16.5" cy="19.5" r="2.3" fill="#E2C08A"/><circle cx="47.5" cy="19.5" r="2.3" fill="#E2C08A"/></svg>')

def layout(p):
    url = SITE["url"] + p["path"]
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE["url"]+"/"}]
    if p.get("hub"):
        crumbs.append({"@type":"ListItem","position":2,"name":p["hub_name"],"item":SITE["url"]+p["hub"]})
    if p["path"] != "/":
        crumbs.append({"@type":"ListItem","position":len(crumbs)+1,"name":plain(p["h1"]),"item":url})
    ld = [{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs}]
    org = {"@type":"Organization","name":SITE["name"],"url":SITE["url"]+"/","logo":SITE["url"]+"/assets/brand/icon-512.png",
           "sameAs":[SITE["tiktok"]],"publishingPrinciples":SITE["url"]+"/editorial-policy/"}
    if p["path"] == "/":
        ld.append({"@context":"https://schema.org","@type":"WebSite","name":SITE["name"],"url":SITE["url"]+"/","description":SITE["desc"]})
        ld.append({"@context":"https://schema.org", **org})
    if p.get("article"):
        ld.append({"@context":"https://schema.org","@type":"NewsArticle" if p["hub"]=="/news/" else "Article","headline":plain(p["h1"]),"description":p["desc"],
                   "author":{"@type":"Organization","name":SITE["author"],"url":SITE["url"]+"/about/"},"publisher":org,
                   "image":SITE["url"]+p.get("og_image","/assets/og/default.png"),
                   "datePublished":p["published"],"dateModified":p.get("reviewed",p["published"]),"mainEntityOfPage":url})
    nav = ""
    for n, kids in SITE["nav"]:
        on = any(p["path"].startswith(k) for k, _ in kids)
        items = "".join(f'<a href="{k}"{" aria-current=\"page\"" if p["path"].startswith(k) else ""}>{kn}</a>' for k, kn in kids)
        nav += (f'<details class="dd{" on" if on else ""}"><summary>{esc(n)}</summary>'
                f'<div class="dd-menu">{items}</div></details>')
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else '<meta name="robots" content="max-image-preview:large">'
    if p.get("redirect"):
        url = SITE["url"] + p["redirect"]
        robots += f'<meta http-equiv="refresh" content="0; url={p["redirect"]}"><script>location.replace("{p["redirect"]}"+location.search+location.hash)</script>'
    og = p.get("og_image", "/assets/og/default.png")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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
<meta name="theme-color" content="#6E2F4C">
<link rel="manifest" href="/site.webmanifest">
<link rel="icon" href="/assets/brand/favicon-32.png?v={_v("assets/brand/favicon-32.png")}" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/brand/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Parva Regina">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;600&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;600&display=swap"></noscript>
<link rel="stylesheet" href="/assets/style.css?v={_v("assets/style.css")}">
<link rel="alternate" type="application/rss+xml" title="Parva Regina" href="/feed.xml">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap bar">
<a class="brand" href="/" aria-label="Parva Regina home"><img src="/assets/brand/lockup-light.png" alt="Parva Regina" width="1000" height="117"></a>
<nav aria-label="Main">{nav}</nav>
<a class="nl" href="/ageless-reset/"><span class="nl-long">Ageless Reset </span>Download</a>
</div></header>
<main id="main">
{p["body"]}
</main>
<footer class="site"><div class="wrap">
<div class="fgrid">
<div><img class="flogo" src="/assets/brand/logo-light.png" alt="Parva Regina: longevity for women" width="900" height="289" loading="lazy"><p>Evidence-based longevity science for women 35+. Every claim linked to its source.</p><a href="/ageless-reset/">Free guide: The 30-Day Ageless Reset</a><a href="{SITE["tiktok"]}" target="_blank" rel="noopener">TikTok @parvaregina</a><a href="/feed.xml">RSS feed</a></div>
{"".join(f'<div><b>{esc(n)}</b>' + "".join(f'<a href="{k}">{kn}</a>' for k, kn in kids) + '</div>' for n, kids in SITE["nav"])}
<div><b>Trust</b><a href="/editorial-policy/">Editorial policy</a><a href="/corrections/">Corrections</a><a href="/about/">About</a><a href="/privacy/">Privacy</a></div>
</div>
<p class="legal">Wellness education, not medical advice. We&rsquo;re not doctors; talk to your clinician before starting a supplement or changing your care. Studies can be wrong and science changes; check the date and sources on each article. &middot; &copy; {datetime.date.today().year} Parva Regina, published by {SITE["publisher"]}</p>
</div></footer>
<script>(function(){{var dds=document.querySelectorAll("details.dd");document.addEventListener("click",function(e){{dds.forEach(function(d){{if(!d.contains(e.target))d.removeAttribute("open")}})}});if(window.matchMedia("(hover:hover)").matches){{dds.forEach(function(d){{d.addEventListener("mouseenter",function(){{d.setAttribute("open","")}});d.addEventListener("mouseleave",function(){{d.removeAttribute("open")}})}})}}}})();</script>
{"" if p.get("redirect") else '<div class="mcta" id="mcta" hidden><a class="mcta-link" href="/ageless-reset/#get"><span class="mcta-k">Free guide</span><span class="mcta-t">The 30-Day Ageless Reset</span></a><a class="mcta-btn" href="/ageless-reset/#get">Download</a><button class="mcta-x" type="button" aria-label="Close">&times;</button></div>'}
<script>(function(){{var h=document.querySelector("header.site"),m=document.getElementById("mcta"),last=scrollY,bands=[...document.querySelectorAll(".reset-band")],seen=false,closed=false;try{{closed=sessionStorage.getItem("mcta")==="x"}}catch(e){{}}
if(m&&!closed&&window.matchMedia("(max-width:700px)").matches){{if("IntersectionObserver" in window&&bands.length){{var io=new IntersectionObserver(function(es){{seen=es.some(function(x){{return x.isIntersecting}});upd()}});bands.forEach(function(b){{io.observe(b)}})}}
m.querySelector(".mcta-x").addEventListener("click",function(){{m.hidden=true;closed=true;try{{sessionStorage.setItem("mcta","x")}}catch(e){{}}}})}}
function upd(){{if(m&&!closed)m.hidden=!(scrollY>500&&!seen&&window.matchMedia("(max-width:700px)").matches)}}
addEventListener("scroll",function(){{var y=scrollY;if(window.matchMedia("(max-width:700px)").matches){{if(y>last+6&&y>140){{h.classList.add("hide");document.querySelectorAll("details.dd[open]").forEach(function(d){{d.removeAttribute("open")}})}}else if(y<last-6||y<140){{h.classList.remove("hide")}}}}last=y;upd()}},{{passive:true}});upd()}})();</script>
<script data-goatcounter="https://parvaregina.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
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
            p["body"] = p["body"].replace("<!--HUB_ARTICLES-->", card_list(mine) if mine else ('<p class="muted">The first articles in this section are on their way. In the meantime, here&rsquo;s what&rsquo;s new:</p>' + card_list(live[:3])))
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
        a = dict(a); a["body"] = unlink_future(a["body"]).replace("<!--NEWSLETTER-->", nl_block(a["path"].strip("/").split("/")[-1], offer=offer_for(a["path"])))
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
