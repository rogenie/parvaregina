SITE = {
  "name": "Parva Regina",
  "url": "https://parvaregina.com",
  "desc": "Evidence-based longevity science for women 35+: what the research actually shows about sleep, strength, skin, hormones and supplements.",
  "author": "Parva Regina Research Desk",
  "publisher": "9nth Dimension Inc.",
  "tiktok": "https://www.tiktok.com/@parvaregina",
  # Kit form id for the newsletter (a number from the Kit form's embed code). None = signup not live yet.
  "kit_form_id": None,
  # Kit embed script uid (from the form's JavaScript embed code). Used when kit_form_id is None.
  "kit_embed_uid": "0ec8af6ff3",
  "kit_domain": "https://rogenie.kit.com",
  "nav": [("/news/","Longevity News"),("/evidence/","Evidence Checks"),("/foundations/","Foundations"),("/about/","About")],
}

EVIDENCE_LADDER = '''<ul class="ticks">
<li><span class="ev human-trial">Human trial</span> &nbsp;People were randomly assigned to the treatment or a comparison. The strongest single kind of evidence.</li>
<li><span class="ev human-obs">Human observational</span> &nbsp;Researchers tracked people and looked for links. Shows association, not cause.</li>
<li><span class="ev animal">Animal study</span> &nbsp;Mice, worms or other animals. Often promising; most results never carry over to people.</li>
<li><span class="ev cell">Lab / cells</span> &nbsp;Cells in a dish. Useful for mechanism, a long way from advice.</li>
<li><span class="ev review">Review</span> &nbsp;A summary of many studies. As strong as the studies it pools.</li>
</ul>'''

RESET_URL = "/ageless-reset/"

RESET_COVER = ('<div class="reset-cover" aria-hidden="true"><span class="rc-kick">Free guide</span>'
               '<span class="rc-t1">The 30-Day</span><span class="rc-t2">Ageless</span><span class="rc-t1">Reset</span>'
               '<span class="rc-rule"></span><span class="rc-sub">Wrinkles &middot; Energy &middot; Hair</span>'
               '<span class="rc-brand">Parva Regina</span></div>')

def kit_form(campaign, button="Send me the free guide"):
    fid = SITE["kit_form_id"]
    if fid:
        return (f'<form class="nl-form" action="https://app.kit.com/forms/{fid}/subscriptions" method="post">'
                f'<label class="skip" for="nl-{campaign}">Email address</label>'
                f'<input id="nl-{campaign}" type="email" name="email_address" placeholder="Your email" required autocomplete="email">'
                f'<input type="hidden" name="fields[source]" value="{campaign}">'
                f'<button type="submit">{button}</button></form>')
    if SITE.get("kit_embed_uid"):
        uid, dom = SITE["kit_embed_uid"], SITE["kit_domain"]
        return (f'<div class="nl-kit"><script async data-uid="{uid}" src="{dom}/{uid}/index.js"></script>'
                f'<noscript><p><a class="btn" href="{dom}/{uid}">Get the free guide</a></p></noscript></div>')
    return f'<p><a class="btn" href="{SITE["tiktok"]}" target="_blank" rel="noopener">Coming soon &middot; follow on TikTok meanwhile</a></p>'

def nl_block(campaign, heading="Get the free 30-Day Ageless Reset",
             text="Wrinkles, the 3 p.m. energy crash, and grey or thinning hair often grow from the same roots. This free guide for women 38&ndash;55 shows how they connect, and gives you a simple 30-day plan that works on all three at once."):
    """Call-to-action band: download the free 30-Day Ageless Reset (delivered by email through Kit)."""
    return (f'<div class="nl-band reset-band"><div class="reset-grid">{RESET_COVER}<div>'
            f'<p class="eyebrow">Free download</p><h2>{heading}</h2><p>{text}</p>'
            f'{kit_form(campaign)}'
            f'<p class="reset-fine">Enter your email and we&rsquo;ll send the guide straight to your inbox, along with our weekly longevity email. Unsubscribe anytime.</p>'
            f'</div></div></div>')

def hub(path, name, title, desc, intro, covers):
    lis = "".join(f"<li>{c}</li>" for c in covers)
    body = f'''<section class="hero small"><div class="wrap">
<p class="eyebrow">Parva Regina</p><h1>{name}</h1><p class="lede">{intro}</p></div></section>
<section><div class="wrap">
<!--HUB_ARTICLES-->
</div></section>
<section class="alt"><div class="wrap narrow">
<h2>What you&rsquo;ll find here</h2><ul class="ticks">{lis}</ul>
<p class="muted">Every article links the studies behind it and labels how strong the evidence is. <a href="/editorial-policy/">How we work</a>.</p>
{nl_block("hub-" + path.strip("/"))}
</div></section>'''
    return {"path":path,"title":title,"desc":desc,"h1":name,"body":body}

PAGES = [
 {"path":"/","title":"Parva Regina | Longevity Science for Women 35+, Without the Hype","h1":"Parva Regina",
  "desc":"What longevity research actually shows for women 35+: new studies, evidence checks on trending supplements and protocols, and the habits with the strongest science.",
  "body":f'''<section class="hero"><div class="wrap">
<p class="eyebrow">Longevity science for women 35+</p>
<h1>Age on your own terms, <em>with the evidence in hand.</em></h1>
<p class="lede">New longevity research, evidence checks on what&rsquo;s trending, and the habits with the strongest science for women in their late 30s, 40s and beyond. Every claim links to its study and says how strong the evidence is.</p>
<p><a class="btn" href="/ageless-reset/">Get the free 30-Day Ageless Reset</a> &nbsp; <a class="btn ghost" href="/evidence/">Read the evidence checks</a></p>
</div></section>
<!--LATEST-->
<section><div class="wrap">
<h2>Start here</h2>
<div class="cards">
<a class="card" href="/news/"><p class="eyebrow">Weekly</p><h3>Longevity News</h3><p>New studies on aging, explained: what was tested, in whom, and whether it applies to you.</p></a>
<a class="card" href="/evidence/"><p class="eyebrow">Does it work?</p><h3>Evidence Checks</h3><p>Red light, creatine, NMN, magnesium, zone 2: what human trials show for women, and what they don&rsquo;t.</p></a>
<a class="card" href="/foundations/"><p class="eyebrow">The basics</p><h3>Foundations</h3><p>Sleep, strength, protein, VO2 max and the perimenopause decade, explained once and well.</p></a>
</div></div></section>
<section class="alt"><div class="wrap narrow">
<h2>Why women 35+?</h2>
<p>Most longevity advice is built on studies of men, or of mice. Yet the mid-30s through the menopause transition is when many women start paying close attention to how they age, and when sleep, muscle, bone and skin begin to change. We read the research with that decade in mind, and we say so when a study didn&rsquo;t include women at all.</p>
<h2>How to read our evidence labels</h2>
{EVIDENCE_LADDER}
<p><a href="/editorial-policy/">Our editorial policy</a></p>
{nl_block("home")}
</div></section>'''},
 hub("/news/","Longevity News","Longevity News for Women 35+: New Aging Research, Explained | Parva Regina",
     "New longevity and aging research explained for women 35+: what each study tested, who was in it, how strong the evidence is, and what it means for you.",
     "New research on aging, explained the day it matters: what was tested, who was studied, how strong the result is, and what changes for you (often, nothing yet).",
     ["New human trials on sleep, exercise, nutrition and supplements","Menopause and perimenopause research with longevity implications","Aging biomarkers and &ldquo;biological age&rdquo; tests, and how far to trust them","Big lab or animal findings, labeled clearly as early"]),
 hub("/evidence/","Evidence Checks","Evidence Checks: Do Longevity Supplements and Protocols Work for Women? | Parva Regina",
     "Does it work? Evidence checks on trending longevity supplements and protocols for women 35+, from red light therapy to creatine, NMN and magnesium.",
     "The trend is everywhere. Here&rsquo;s what the human trials show, whether women were studied, the dose that was tested, and the honest bottom line.",
     ["Supplements: creatine, magnesium, NMN and NAD+, urolithin A, collagen, fisetin","Devices and protocols: red light therapy, cold and heat, fasting","Head-to-head comparisons, like magnesium glycinate vs. threonate","What the research says, what it doesn&rsquo;t, and what to ask your doctor"]),
 hub("/foundations/","Foundations","Longevity Foundations for Women 35+: Sleep, Strength, Bone and More | Parva Regina",
     "The habits with the strongest evidence for healthy aging in women 35+: sleep, strength training, protein, aerobic fitness, bone health and the menopause transition.",
     "The unglamorous habits with the strongest evidence behind them, explained once and well, with what changes for women from the mid-30s on.",
     ["Sleep and deep sleep across the 30s, 40s and 50s","Strength training, muscle and bone density","VO2 max, zone 2 and cardiorespiratory fitness","Protein and nutrition basics with real numbers from official sources","The perimenopause and menopause transition: what&rsquo;s established and what&rsquo;s hype"]),
 {"path":"/ageless-reset/","title":"The 30-Day Ageless Reset: Free Guide for Women 38-55 | Parva Regina","h1":"The 30-Day Ageless Reset",
  "desc":"Free guide for women 38-55: why wrinkles, the afternoon energy crash and grey or thinning hair often share the same roots, plus a 30-day plan for all three.",
  "body":f'''<section class="hero small"><div class="wrap narrow"><p class="eyebrow">Free guide for women 38&ndash;55</p><h1>The 30-Day Ageless Reset</h1>
<p class="lede">The lines that don&rsquo;t leave anymore. The 3 p.m. wall. The extra hair in the drain. They feel like three separate problems, so you&rsquo;ve been fighting them with three shelves of products. This guide shows why they&rsquo;re connected, and what to do about all three at once.</p></div></section>
<section><div class="wrap narrow prose">
{nl_block("reset-page", heading="Send me the free guide", text="A 13-page guide you can read in one sitting, with a 30-day checklist and a list to take to your doctor.")}
<h2>What&rsquo;s inside</h2>
<ul class="ticks">
<li><b>Why it feels like it happened overnight:</b> what changes in your skin&rsquo;s collagen around menopause, and why creams on the surface can&rsquo;t reach it</li>
<li><b>The afternoon crash, explained:</b> how sleep, blood sugar and stress feed your energy, your skin and your hair at the same time</li>
<li><b>Grey and thinning hair:</b> the checks worth asking your doctor about before you buy another supplement</li>
<li><b>Three fronts, 30 days:</b> a short list of habits for skin, energy and hair, with the evidence behind each</li>
<li><b>A week-by-week checklist</b> so you add one thing at a time and keep what you&rsquo;ve built</li>
<li><b>An appointment checklist</b> to take to your doctor, so you don&rsquo;t get told it&rsquo;s &ldquo;just aging&rdquo;</li>
</ul>
<h2>Who it&rsquo;s for</h2>
<p>Women in their late 30s, 40s and 50s who are noticing changes in their skin, energy or hair and are tired of guessing. No crash diet, no 14-product routine, and nothing to buy.</p>
<p class="fine">Wellness education, not medical advice. Talk to your clinician before starting new skincare actives, supplements, exercise or medications. Signing up also subscribes you to our weekly email; unsubscribe from any email with one click. See our <a href="/privacy/">privacy policy</a>.</p>
</div></section>'''},
 {"path":"/newsletter/","title":"The 30-Day Ageless Reset | Parva Regina","h1":"The 30-Day Ageless Reset","noindex":True,"redirect":"/ageless-reset/",
  "desc":"This page has moved to the free 30-Day Ageless Reset guide.",
  "body":'''<section class="hero small"><div class="wrap narrow"><h1>This page has moved</h1><p class="lede"><a href="/ageless-reset/">Get the free 30-Day Ageless Reset &rarr;</a></p></div></section>'''},
 {"path":"/about/","title":"About Parva Regina","h1":"About Parva Regina",
  "desc":"Who publishes Parva Regina, how articles are researched and written, and what the site is and isn't.",
  "body":f'''<section class="hero small"><div class="wrap narrow"><p class="eyebrow">About</p><h1>About Parva Regina</h1>
<p class="lede"><i>Parva regina</i> is Latin for &ldquo;little queen.&rdquo; It&rsquo;s a reminder that aging well is something you rule over, one well-informed decision at a time.</p></div></section>
<section><div class="wrap narrow prose">
<h2>What we do</h2>
<p>We follow longevity and aging research and explain it for women from their mid-30s on: what a study tested, who was in it, how strong the result is, and whether it changes anything you do. We also run evidence checks on the supplements, devices and protocols that trend online.</p>
<h2>How articles are made</h2>
<p>Articles are researched and written by the Parva Regina Research Desk using AI, under a published <a href="/editorial-policy/">editorial policy</a>. Every factual claim must trace to a source we link: a peer-reviewed study, a clinical trial registry, or a government health agency such as the NIH or FDA. We label every study by evidence type, and we don&rsquo;t publish an article whose key claim we can&rsquo;t source. Mistakes get fixed and logged on our <a href="/corrections/">corrections page</a>.</p>
<h2>What we&rsquo;re not</h2>
<p>We&rsquo;re not doctors, and nothing here is medical advice for your situation. Talk to your clinician before starting a supplement, changing a medication, or trying a new protocol, especially if you&rsquo;re pregnant, nursing, or managing a health condition.</p>
<h2>Who publishes it</h2>
<p>Parva Regina is published by 9nth Dimension Inc. We don&rsquo;t accept payment for coverage. If we ever add affiliate links, every page that has them will say so at the top.</p>
<p>Find us on <a href="{SITE["tiktok"]}" target="_blank" rel="noopener">TikTok @parvaregina</a>.</p>
</div></section>'''},
 {"path":"/editorial-policy/","title":"Editorial Policy | Parva Regina","h1":"Editorial policy",
  "desc":"How Parva Regina researches, writes, labels and corrects its longevity articles, including how AI is used.",
  "body":f'''<section class="hero small"><div class="wrap narrow"><p class="eyebrow">How we work</p><h1>Editorial policy</h1><p class="lede">The rules every Parva Regina article follows before it goes live.</p></div></section>
<section><div class="wrap narrow prose">
<h2>Sources</h2>
<p>We rely on primary sources: peer-reviewed papers (usually found through PubMed), trial registries such as ClinicalTrials.gov, and government health agencies such as the National Institutes of Health, the National Institute on Aging and the FDA. News coverage can point us to a study, but the study itself is the source. Preprints that haven&rsquo;t been peer reviewed are labeled as such.</p>
<h2>Evidence labels</h2>
<p>Every study we discuss gets a label:</p>
{EVIDENCE_LADDER}
<p>We also note the number of participants, whether women were included, and how long the study ran.</p>
<h2>What we never do</h2>
<ul>
<li>Say a product or habit &ldquo;reverses aging,&rdquo; &ldquo;cures&rdquo; anything, or adds years to your life.</li>
<li>Turn a mouse or cell result into advice for people.</li>
<li>Recommend doses beyond restating what a study tested or what an official source says.</li>
<li>Invent personal experiences, testimonials, quotes or statistics.</li>
<li>Accept payment for coverage.</li>
</ul>
<h2>How AI is used</h2>
<p>Articles are researched and drafted with AI. Before an article publishes, every number, date and study detail it states is checked against the linked source in the same session; claims that can&rsquo;t be confirmed are removed, and an article that can&rsquo;t stand without them is held back. Each article shows the date it was last checked.</p>
<h2>Corrections</h2>
<p>When we get something wrong, we fix it, note the change at the bottom of the article, and log it on the <a href="/corrections/">corrections page</a>.</p>
</div></section>'''},
 {"path":"/corrections/","title":"Corrections | Parva Regina","h1":"Corrections",
  "desc":"A log of corrections and material updates to Parva Regina articles.",
  "body":'''<section class="hero small"><div class="wrap narrow"><p class="eyebrow">Accountability</p><h1>Corrections</h1><p class="lede">When we fix an error of fact in an article, we log it here with the date.</p></div></section>
<section><div class="wrap narrow prose">
<!--CORRECTIONS-->
</div></section>'''},
 {"path":"/privacy/","title":"Privacy Policy | Parva Regina","h1":"Privacy policy",
  "desc":"How Parva Regina handles information when you visit the site or sign up for the free guide.",
  "body":'''<section class="hero small"><div class="wrap narrow"><h1>Privacy policy</h1><p class="lede">Last updated October 29, 2026.</p></div></section>
<section><div class="wrap narrow prose">
<h2>What we collect</h2>
<p>Parva Regina has no accounts or comments and doesn&rsquo;t set cookies. We don&rsquo;t sell or share personal information.</p>
<h2>Visit counts</h2>
<p>We count visits with GoatCounter, a privacy-friendly analytics service. It records which page was viewed, the referring site, and general browser, screen size and country information. It uses no cookies, doesn&rsquo;t track you across other sites, and doesn&rsquo;t store your IP address. We use these totals only to see which articles are read.</p>
<h2>Free guide and email list</h2>
<p>If you sign up for the free 30-Day Ageless Reset, your email address is collected and stored by Kit, the service that sends the guide and our weekly email, under its own privacy policy. You can unsubscribe from any email.</p>
<h2>Services that load with the site</h2>
<p>The site is hosted on GitHub Pages, loads fonts from Google Fonts, and loads the free-guide signup form from Kit. Like any web server, these services receive your IP address and basic browser information when you load a page, under their own privacy policies.</p>
<h2>Changes</h2>
<p>If we add advertising, affiliate links or other analytics, this page will be updated first and will say what is collected and why.</p>
</div></section>'''},
 {"path":"/404","title":"Page not found | Parva Regina","h1":"Page not found","noindex":True,
  "desc":"This page doesn't exist.",
  "body":'''<section class="hero small"><div class="wrap"><h1>Page not found</h1><p class="lede">That page doesn&rsquo;t exist, or it has moved.</p><a class="btn" href="/">Go to the home page</a></div></section>'''},
]
