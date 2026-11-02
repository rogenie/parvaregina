# All articles. build.py publishes an article only when its "published" date (Pacific time) has arrived.
# Scheduled runs append new article(...) entries to ARTICLES. See _src/PUBLISHING.md.
from urllib.parse import quote
from html import unescape
import datetime

def _d(iso): return datetime.date.fromisoformat(iso).strftime('%B %-d, %Y')

EV = {  # evidence label keys -> display text (CSS class = key)
    "human-trial": "Human trial",
    "human-obs": "Human observational",
    "animal": "Animal study",
    "cell": "Lab / cells",
    "review": "Review",
}

def share_box(path, h1):
    url = "https://parvaregina.com" + path
    u = quote(url, safe=""); t = quote(unescape(h1), safe="")
    links = [
        ("Facebook", f"https://www.facebook.com/sharer/sharer.php?u={u}"),
        ("Pinterest", f"https://pinterest.com/pin/create/button/?url={u}&amp;description={t}"),
        ("X", f"https://twitter.com/intent/tweet?url={u}&amp;text={t}"),
        ("Email", f"mailto:?subject={t}&amp;body={u}"),
    ]
    a = "".join(f'<a href="{h}"{"" if n == "Email" else " target=\"_blank\" rel=\"noopener\""}>{n}</a>' for n, h in links)
    copy = (f'<button type="button" data-url="{url}" onclick="var b=this;navigator.clipboard.writeText(b.dataset.url)'
            f'.then(function(){{b.textContent=\'Link copied\'}},function(){{prompt(\'Copy this link:\',b.dataset.url)}})">Copy link</button>')
    native = (f'<button type="button" class="share-native" hidden data-url="{url}" data-title="{unescape(h1)}" '
              f'onclick="navigator.share({{title:this.dataset.title,url:this.dataset.url}}).catch(function(){{}})">Share</button>'
              f'<script>if(navigator.share)document.currentScript.previousElementSibling.hidden=false</script>')
    return f'<div class="share" aria-label="Share this article"><b>Share:</b> {native}{a}{copy}</div>'

def article(path, hub, hub_name, title, h1, desc, published, intro, quick, evidence, glance, sections, sources, updates=""):
    """
    quick    : 1-3 sentence "Quick answer" (HTML) shown right after the intro.
    evidence : key from EV for the strongest evidence the article rests on.
    glance   : list of (label, value) rows for the "Evidence at a glance" box,
               e.g. [("Best evidence","..."), ("Women included?","..."), ("Bottom line","...")].
    sources  : list of (title, url); primary sources first.
    updates  : optional HTML note of later changes (see corrections in PUBLISHING.md).
    """
    src = "".join(f'<li><a href="{u}" rel="noopener">{t}</a></li>' for t, u in sources)
    rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in glance)
    upd = f'<div class="callout"><b>Updates.</b> {updates}</div>' if updates else ""
    body = f'''<section class="hero small"><div class="wrap narrow">
<p class="eyebrow"><a href="{hub}">{hub_name}</a></p>
<h1>{h1}</h1>
<p class="lede">{intro}</p>
<p class="byline">By the <a href="/about/">Parva Regina Research Desk</a> &middot; Checked against sources {_d(published)} &middot; <a href="/editorial-policy/">How we work</a></p>
</div></section>
<section><div class="wrap narrow prose">
<div class="callout quick"><b>Quick answer.</b> {quick}</div>
<div class="evbox"><span class="ev {evidence}">{EV[evidence]}</span> <b>&nbsp;Evidence at a glance</b><dl>{rows}</dl></div>
{sections}
<!--NEWSLETTER-->
{share_box(path, h1)}
{upd}
<h2>Sources</h2><ul class="sources">{src}</ul>
<p class="fine">Wellness education, not medical advice. This article summarizes published research and official sources; it isn&rsquo;t a recommendation for your situation. Talk to your clinician before starting a supplement, device or protocol, especially if you&rsquo;re pregnant, nursing, take medication or manage a health condition.</p>
</div></section>'''
    return {"path": path, "hub": hub, "hub_name": hub_name, "title": title, "h1": h1, "desc": desc, "body": body,
            "article": True, "published": published, "reviewed": published, "evidence": (evidence, EV[evidence])}

ARTICLES = [
article("/supplements/creatine-for-women-over-40/", "/supplements/", "Supplements",
 "Creatine for Women Over 40: What the Research Shows",
 "Creatine for women over 40: what the research actually shows",
 "Does creatine help women over 40 with muscle, bone or brain? What the human trials found, the doses they tested, and the honest bottom line.",
 "2026-10-28",
 "Creatine has gone from gym-bro powder to midlife-women&rsquo;s staple in about two years. The pitch: more muscle, stronger bones, sharper thinking. Here&rsquo;s what the trials in women actually found.",
 "In postmenopausal women, the best trials show creatine adds little or nothing to bone density and only modest extra strength beyond what resistance training already gives. <b>Training is the main event; creatine is, at most, a small add-on.</b> Brain and mood claims rest on small, short studies.",
 "human-trial",
 [("Best evidence", "A 2-year randomized, placebo-controlled trial in 237 postmenopausal women (2023)"),
  ("Women included?", "Yes. The main trials studied women only, mostly after menopause"),
  ("Dose tested", "0.14 g per kg of body weight daily in the 2-year trial, alongside resistance training"),
  ("Bottom line", "No bone-density benefit; small, inconsistent muscle and strength effects; brain findings are early")],
 """<h2>Why creatine for women over 40 is suddenly everywhere</h2>
<p>From the mid-30s on, keeping muscle and bone becomes a priority, and the menopause transition brings an abrupt shift in bone metabolism (see <a href="/news/menopause-physiological-cliff-study/">our news report on a study of a million women</a>). Creatine, a compound your muscles already use for short bursts of energy, has strong evidence for helping athletes train harder. The question is whether that carries over to women in midlife who want to keep their strength and their skeleton.</p>
<p><b>That&rsquo;s a fair question, and it has been tested.</b> Not in mice, but in randomized trials of women.</p>

<h2>What the biggest trial found: creatine and bone density</h2>
<p>The largest and longest study so far followed 237 postmenopausal women, average age 59, for two years. Every woman did the same program: resistance training three days a week and walking six days a week. Half took creatine monohydrate (0.14 g per kilogram of body weight a day); half took a placebo. Neither the women nor the researchers knew who got which.</p>
<p>The results, published in 2023:</p>
<ul>
<li><b>Bone density:</b> no difference. Bone mineral density at the hip (femoral neck), the study&rsquo;s main measure, changed about the same in both groups.</li>
<li><b>Bone shape:</b> the creatine group held on to one measure of hip bone geometry (section modulus) that dropped slightly in the placebo group. That&rsquo;s a hint about bone strength, not proof of fewer fractures.</li>
<li><b>Strength:</b> no difference. Both groups got much stronger on the bench press and squat, because both groups were training.</li>
<li><b>Lean mass:</b> a small edge for creatine only among women who stuck closely to the program; in the full group, it wasn&rsquo;t significant.</li>
<li><b>Walking speed:</b> the creatine group got slightly faster over an 80-meter walk.</li>
</ul>
<p>Notice what the trial design tells you: everyone trained, and everyone got stronger. <a href="/bones/strength-training-bone-density-menopause/">Strength training itself</a> is the better-studied tool for muscle and bone.</p>

<h2>Does creatine build muscle in women after menopause?</h2>
<p>A 2026 review pooled trials that combined supplements with exercise in women across reproductive stages. It included three creatine trials, all in postmenopausal women, with about 300 women analyzed. Its findings:</p>
<ul>
<li>Upper-body strength improved a little more when creatine was added, which the authors attribute largely to creatine.</li>
<li>Muscle mass results were mixed: one short trial found a gain, the two longer ones didn&rsquo;t.</li>
<li><b>Exercise alone was the most reliable intervention.</b> The authors rated the certainty of the evidence as low for muscle and strength and very low for bone.</li>
</ul>

<h2>What about brain fog and mood?</h2>
<p>This is the newest and thinnest part of the evidence. One randomized trial of 36 perimenopausal and menopausal women (average age 50) tested creatine hydrochloride, a different form from the usual monohydrate, for 8 weeks. The middle dose (1,500 mg a day) raised creatine levels in the front of the brain and changed reaction time compared with placebo. The effect on mood swings didn&rsquo;t reach statistical significance.</p>
<p>That&rsquo;s interesting, and it&rsquo;s also 36 women for two months. <b>It&rsquo;s a reason for bigger studies, not a reason to expect clearer thinking.</b></p>

<h2>How much creatine was tested, and in whom</h2>
<table>
<tr><th>Study</th><th>Women</th><th>Dose</th><th>Length</th><th>Main result</th></tr>
<tr><td>Chilibeck et al., 2023</td><td>237 postmenopausal, avg. 59</td><td>0.14 g/kg/day + training</td><td>2 years</td><td>No bone-density benefit</td></tr>
<tr><td>Chen et al., 2026 (review)</td><td>~300 in 3 creatine trials</td><td>Varied</td><td>24&ndash;96 weeks</td><td>Small upper-body strength edge; low certainty</td></tr>
<tr><td>CONCRET-MENOPA, 2025</td><td>36 peri- and postmenopausal, avg. 50</td><td>750&ndash;1,500 mg/day creatine HCl</td><td>8 weeks</td><td>Higher brain creatine; mood not significant</td></tr>
</table>
<p>To put the big trial&rsquo;s dose in context: 0.14 g per kilogram works out to roughly 9.5 g a day for a 150-lb (68 kg) woman. That&rsquo;s the amount a study tested, not a recommendation.</p>

<h2>The honest bottom line</h2>
<ul class="ticks">
<li><b>If your goal is bone:</b> creatine hasn&rsquo;t shown a bone-density benefit in women after menopause. Strength training and a conversation with your clinician about bone screening are the better-supported moves.</li>
<li><b>If your goal is strength:</b> the training does the heavy lifting. Creatine may add a little on top, especially for the upper body.</li>
<li><b>If your goal is your brain:</b> it&rsquo;s too early to say.</li>
</ul>
<p>Creatine is one of the most-studied supplements in sport, but most of that research is in young men. Talk to your clinician before starting it, especially if you have kidney disease, take medication that affects your kidneys, or are pregnant or nursing.</p>
<p>Next up in our evidence checks: <a href="/supplements/magnesium-glycinate-vs-threonate/">magnesium glycinate vs. L-threonate</a> and <a href="/supplements/urolithin-a-evidence/">urolithin A</a>. For the basics, see <a href="/foundations/">Foundations</a>.</p>""",
 [("Chilibeck PD et al. A 2-yr randomized controlled trial on creatine supplementation during exercise for postmenopausal bone health. Med Sci Sports Exerc, 2023", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10487398/"),
  ("Chen et al. Nutritional supplementation combined with exercise for musculoskeletal health in women: a systematic review and meta-analysis. Int J Med Sci, 2026", "https://pmc.ncbi.nlm.nih.gov/articles/PMC13181379/"),
  ("CONCRET-MENOPA: creatine hydrochloride and creatine ethyl ester in perimenopausal and menopausal women, randomized controlled trial. J Am Nutr Assoc, 2025", "https://pubmed.ncbi.nlm.nih.gov/40854087/")]),
article("/news/menopause-physiological-cliff-study/", "/news/", "Latest Research",
 "Menopause Brings Abrupt Body-Wide Changes, Huge Study Finds",
 "Menopause brings abrupt changes in bone, liver and blood fats, huge study finds",
 "A Nature Medicine study of 300 million lab tests from over a million women found a sudden shift at the final period, with hormones changing 12-15 years earlier.",
 "2026-10-28",
 "Menopause is usually described as a slow fade. A study of more than a million women suggests something different: a sharp step change across the body at the final period, with hormone shifts starting more than a decade before.",
 "Researchers analyzed over 300 million routine lab tests from more than a million women in the US and Israel. <b>Many markers, especially bone, liver and blood-fat tests, shifted abruptly around the final menstrual period</b>, while key hormones began changing 12 to 15 years earlier. It&rsquo;s observational, so it shows when things change, not what to do about it.",
 "human-obs",
 [("Study type", "Retrospective analysis of routine lab records (observational)"),
  ("Who", "More than 1 million women in the United States and Israel, 1999&ndash;2024"),
  ("Published", "Nature Medicine, online October 12, 2026"),
  ("Bottom line", "Strong evidence about timing; no evidence yet about which interventions change the curve")],
 """<h2>What the menopause study found</h2>
<p>The team, whose lead author is at the Weizmann Institute of Science in Israel, pooled more than 300 million laboratory tests collected during ordinary medical care. Because the final menstrual period is rarely recorded, past studies have struggled to pin down exactly when changes happen. Working with a dataset this large let them line up women by the timing of their last period and look for patterns.</p>
<ul>
<li><b>An abrupt shift at the final period.</b> In the US data, 52 of the 90 lab tests studied showed a statistically significant, sudden change around menopause.</li>
<li><b>Which systems:</b> the biggest shifts were in bone metabolism, liver tests and how the body handles blood fats. Kidney function and blood chemistry shifted too.</li>
<li><b>Not just aging:</b> men of the same ages didn&rsquo;t show these abrupt changes, so the authors tie them to menopause itself rather than getting older.</li>
</ul>

<h2>Hormones start changing more than a decade earlier</h2>
<p>For women in their late 30s and 40s, this is the part worth noticing. The hormone shifts that lead up to menopause began long before the last period:</p>
<table>
<tr><th>Hormone</th><th>What happened</th><th>When</th></tr>
<tr><td>Anti-M&uuml;llerian hormone (AMH)</td><td>Declined rapidly</td><td>About 15 years before the final period</td></tr>
<tr><td>Follicle-stimulating hormone (FSH)</td><td>Began rising more rapidly</td><td>About 14 years before</td></tr>
<tr><td>Estradiol</td><td>Declined rapidly</td><td>About 12 years before</td></tr>
</table>
<p><b>In other words, the menopause transition is a story that often starts in your late 30s, even if nothing feels different yet.</b></p>

<h2>What about hormone therapy?</h2>
<p>According to the journal&rsquo;s press release, hormone therapy was associated with smaller changes in many measures, particularly bone, liver and kidney markers. The authors themselves say this needs to be confirmed in future studies. Because women weren&rsquo;t randomly assigned to hormone therapy here, the difference could reflect who chooses it, not just what it does.</p>

<h2>What the study can&rsquo;t tell you</h2>
<ul>
<li><b>It&rsquo;s observational.</b> It shows when lab values change, not what causes the change or what prevents it.</li>
<li><b>Menopause status was self-reported</b>, and the data were collected for routine care, not research.</li>
<li><b>&ldquo;Cliff&rdquo; describes lab curves, not how women feel.</b> Experts not involved in the study cautioned that the framing could sound more alarming than the findings, which don&rsquo;t show a dramatic physical or mental decline.</li>
</ul>

<h2>What this means for you</h2>
<p>Nothing here calls for a new supplement or test. What it does support is paying attention before menopause, not after:</p>
<ul class="ticks">
<li>Ask your clinician how they&rsquo;d monitor bone health and cholesterol as you move through your 40s, and what your personal risk factors are.</li>
<li>Keep building muscle and bone with <a href="/bones/strength-training-bone-density-menopause/">strength training</a>, which has the strongest evidence of any habit for both.</li>
<li>If you&rsquo;re weighing hormone therapy, that&rsquo;s a conversation about your own risks and benefits with your doctor, not a decision to make from one observational study.</li>
</ul>
<p>Related: our evidence check on <a href="/supplements/creatine-for-women-over-40/">creatine for women over 40</a>.</p>""",
 [("Pridham G, Hayut Y, Lavi-Shoseyov N, et al. Population-scale reconstruction of menopause dynamics reveals a physiological cliff at the final menstrual period. Nature Medicine, 2026. doi:10.1038/s41591-026-04614-0", "https://www.nature.com/articles/s41591-026-04614-0"),
  ("Nature Portfolio press release on the study, October 13, 2026", "https://www.natureasia.com/en/info/press-releases/detail/9458"),
  ("ScienceAlert: coverage including comments from independent experts, October 13, 2026", "https://sciencealert.com/bones-liver-and-blood-fats-all-shift-abruptly-at-menopause-huge-study-finds")]),
article("/skin/red-light-therapy-skin-over-40/", "/skin/", "Skin",
 "Red Light Therapy for Skin Over 40: What the Evidence Shows",
 "Red light therapy for skin over 40: what the evidence shows",
 "Do LED masks smooth wrinkles after 40? What the studies behind red light therapy found, what FDA clearance means, and how to use a mask safely.",
 "2026-11-01",
 "LED masks are now sold for home use on promises of firmer skin and fewer lines. Before you buy one, here&rsquo;s what the studies behind red light therapy for skin actually show.",
 "Red and near-infrared light may modestly improve fine lines and firmness, but most of the studies behind today&rsquo;s at-home masks are small, short and paid for by the companies that sell them, with no comparison group. <b>FDA clearance means a mask is considered safe and similar to older devices, not that it was proven to work in people.</b>",
 "review",
 [("Best evidence", "Reviews of small clinical studies, plus company-funded studies of specific masks that had no control group"),
  ("Women included?", "Yes. Recent mask studies enrolled mostly or only women aged roughly 41 to 70"),
  ("What was tested", "Red light (about 630&ndash;660 nm), often combined with near-infrared (830 nm and above), for 10&ndash;21 minutes, two to five times a week, over 1&ndash;3 months"),
  ("Bottom line", "Low risk when used as directed, possibly a small benefit, and much less proven than the marketing suggests")],
 """<h2>What red light therapy for skin is supposed to do</h2>
<p>The technique is called photobiomodulation: shining low-power red or near-infrared light on the skin. The leading theory is that the light is absorbed by an enzyme in mitochondria (cytochrome c oxidase), nudging cells to make more energy, and that skin cells called fibroblasts respond by making more collagen.</p>
<p>A 2024 review in the <i>International Journal of Molecular Sciences</i> describes red light as roughly 620 to 700 nanometers and near-infrared as 700 nanometers and up, with longer wavelengths reaching deeper into the skin. The same review notes that <b>there are still no standard recommendations</b> for how much light, how often, or for how long.</p>

<h2>What the studies behind LED masks found</h2>
<p>The studies most often quoted in mask marketing look impressive on paper. Look closely at how they were designed.</p>
<p><b>A luxury-brand mask study (2023).</b> Twenty volunteers aged 45 to 70 used a red-light mask (630 nanometers) for 12 minutes twice a week for three months. Crow&rsquo;s-feet wrinkle depth was reported as 38% lower by the end. But there was no comparison group, participants kept using their own skincare and makeup, and the authors included staff of the cosmetics brand that sells the mask and the chief executive of the company that makes it. The authors themselves list the uncontrolled skincare as a limitation.</p>
<p><b>A multi-wavelength mask study (2026).</b> Thirty-three women aged 41 to 55 used a face mask and a neck mask combining red and near-infrared light (633, 830 and 1,072 nanometers) for 10 minutes, five days a week, for eight weeks; 31 finished. A dermatologist graded fine lines and wrinkles on the face about 6% better, and measured wrinkle depth was about 9% lower. Again, there was no control group, and the study was funded by the device maker, whose innovation manager was the lead author. The authors note that without a control group, expectations may explain part of the result.</p>
<p><b>Why that matters:</b> skin often looks better simply because people in a study are paying attention to it, moisturizing and protecting it from the sun. Without a group using a sham (fake) mask, there&rsquo;s no way to know how much of the change came from the light.</p>

<h2>Are there controlled trials of red light for wrinkles?</h2>
<p>Some exist, and researchers are running more rigorous ones. For example, a team in Brazil published the plan for a randomized, double-blind trial in 108 women aged 45 to 60, all past menopause, comparing two schedules of a red-light (660 nanometer) mask against a sham mask that made the same sound with the light off. That kind of design is what the field needs.</p>
<p>The 2024 review above reports that in the clinical studies it covered, red combined with near-infrared light improved wrinkles, smoothness and firmness. It also points out that treatment schedules varied widely and that protocols haven&rsquo;t been standardized. <b>The honest summary: a plausible, modest effect, from studies that are mostly small and short.</b></p>

<h2>What FDA clearance for an LED mask means</h2>
<p>Many masks advertise that they&rsquo;re &ldquo;FDA cleared.&rdquo; Clearance is not the same as approval. Most at-home LED masks are cleared through the 510(k) process, which asks whether a device is substantially equivalent to one already on the market.</p>
<p>One popular mask cleared in June 2026 for over-the-counter treatment of full-face wrinkles is a good example. Its FDA summary states that clinical performance testing was not needed: clearance rested on comparison with earlier devices and on lab testing for electrical, light and battery safety. Its clearance also covers only lighter to medium skin tones (Fitzpatrick types I to IV).</p>
<p>FDA&rsquo;s own draft guidance for these devices, issued in January 2023, recommends that companies run clinical studies for new devices, ideally with sham or other blinded controls.</p>

<h2>Is red light therapy safe? Eyes come first</h2>
<ul>
<li><b>Your eyes:</b> FDA&rsquo;s draft guidance says light therapy devices can pose a risk of eye damage and recommends that instructions call for safety eyewear when the output requires it. Use the eye protection that comes with the device and never look into the LEDs.</li>
<li><b>Long-term use:</b> the same guidance suggests labels say that the long-term effects of prolonged use are unknown.</li>
<li><b>Cancer:</b> a 2023 systematic review in <i>Aesthetic Surgery Journal</i> looked at 57 papers, including 7 clinical trials, and concluded that current evidence suggests the treatment is safe for skin rejuvenation from a cancer standpoint. Those trials weren&rsquo;t designed to study cancer, so the evidence is limited.</li>
<li><b>Who should check first:</b> FDA&rsquo;s suggested labeling includes warnings about use during pregnancy and over cancerous lesions. If you have a skin condition or a history of skin cancer, ask your clinician first.</li>
</ul>

<h2>Studies at a glance</h2>
<table>
<tr><th>Study</th><th>Who</th><th>Light and schedule</th><th>Control group?</th><th>Reported result</th></tr>
<tr><td>Luxury-brand mask, 2023</td><td>20 volunteers, aged 45&ndash;70</td><td>630 nm; 12 min, twice weekly, 3 months</td><td>No</td><td>Crow&rsquo;s-feet depth about 38% lower</td></tr>
<tr><td>Multi-wavelength mask, 2026</td><td>33 women, aged 41&ndash;55 (31 finished)</td><td>633, 830, 1,072 nm; 10 min, 5 days a week, 8 weeks</td><td>No</td><td>Graded lines about 6% better; wrinkle depth about 9% lower</td></tr>
<tr><td>Brazilian trial plan, 2023</td><td>108 postmenopausal women, aged 45&ndash;60</td><td>660 nm; 21 min sessions, 4 weeks</td><td>Yes (sham mask)</td><td>Protocol only; no results in that paper</td></tr>
</table>

<h2>The honest bottom line</h2>
<ul class="ticks">
<li><b>If you already own a mask:</b> it&rsquo;s low risk when used as directed with eye protection. Expect subtle changes at most, and judge it by photos in the same light over two to three months.</li>
<li><b>If you&rsquo;re deciding whether to buy one:</b> the evidence for a visible difference is weaker than the ads suggest, and &ldquo;FDA cleared&rdquo; doesn&rsquo;t mean proven.</li>
<li><b>If you have darker skin:</b> check the clearance; some masks are cleared only for skin types I to IV.</li>
<li>For in-office options with stronger evidence and more downtime, see our <a href="/procedures/">Procedures</a> section, and browse everything we&rsquo;ve checked in <a href="/skin/">Skin</a>.</li>
</ul>
<p>Related: <a href="/skin/collagen-supplements-skin-evidence/">collagen supplements for skin</a> and <a href="/skin/facial-lymphatic-drainage-evidence/">facial lymphatic drainage</a>.</p>""",
 [("Couturaud V, Le Fur M, Pelletier M, Granotier F. Reverse skin aging signs by red light photobiomodulation. Skin Research and Technology, 2023;29(7):e13391", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10311288/"),
  ("Bradbury E, Langton AK. Multi-Wavelength LED Photobiomodulation Improves Photoaged Skin of the Face, Neck, and D&eacute;collet&eacute;. Cosmetics, 2026;13(5):276", "https://www.mdpi.com/2079-9284/13/5/276"),
  ("Comparison of the effects of 2 frequencies of application of photobiomodulation on facial rejuvenation: controlled, randomized, and double-blind clinical trial (protocol). Medicine, 2023;102(5):e32514", "https://pmc.ncbi.nlm.nih.gov/articles/PMC9902007/"),
  ("U.S. FDA. 510(k) clearance K260715 and summary for an over-the-counter LED light therapy mask, June 3, 2026", "https://www.accessdata.fda.gov/cdrh_docs/pdf26/K260715.pdf"),
  ("U.S. FDA. Photobiomodulation (PBM) Devices: Premarket Notification [510(k)] Submissions. Draft guidance, January 2023", "https://www.fda.gov/media/164417/download"),
  ("Hern&aacute;ndez-Bule ML, Naharro-Rodr&iacute;guez J, Bacci S, Fern&aacute;ndez-Guarino M. Unlocking the Power of Light on the Skin: A Comprehensive Review on Photobiomodulation. International Journal of Molecular Sciences, 2024;25(8):4483", "https://www.mdpi.com/1422-0067/25/8/4483"),
  ("Glass GE. Photobiomodulation: A Systematic Review of the Oncologic Safety of Low-Level Light Therapy for Aesthetic Skin Rejuvenation. Aesthetic Surgery Journal, 2023;43(5):NP357&ndash;NP371", "https://academic.oup.com/asj/article/43/5/NP357/7018419")]),
]
