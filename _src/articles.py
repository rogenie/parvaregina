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
        ("LinkedIn", f"https://www.linkedin.com/sharing/share-offsite/?url={u}"),
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
article("/fitness/vo2-max-women/", "/fitness/", "Fitness",
 "VO2 Max for Women: Why It Matters and How to Raise It",
 "VO2 max for women: why it matters and how to raise it",
 "What VO2 max is, how it changes with age in women, what the mortality research shows, and what trials in women found raises it.",
 "2026-11-04",
 "VO2 max has become the longevity number of the moment, showing up on smartwatches. Here&rsquo;s what it actually measures, why researchers care about it, and what trials in midlife and older women found about raising it.",
 "VO2 max is the most oxygen your body can use during all-out exercise, a measure of cardiorespiratory fitness. In large studies, fitter adults, women included, die at lower rates than less fit adults of the same age and sex. <b>Trials in midlife and older women show regular aerobic exercise raises it, with more exercise bringing bigger gains; interval training raised it too.</b>",
 "human-trial",
 [("Best evidence", "Randomized trials in women: a 6-month trial of 464 postmenopausal women (2007) and a 2026 review of 19 trials in middle-aged and older women. The link to longevity comes from observational studies, such as one of 122,007 adults (2018)"),
  ("Women included?", "Yes. The main trials studied women only; women were about 41% of the large mortality study"),
  ("Protocol tested", "About 72 to 192 minutes a week of moderate exercise for 6 months; interval training in other trials"),
  ("Bottom line", "Higher fitness is linked to a longer life. Moving more raises it, and harder intervals are one more way to do it")],
 """<h2>What is VO2 max?</h2>
<p>VO2 max is the most oxygen your body can take in and use during hard exercise. It&rsquo;s usually written in milliliters of oxygen per kilogram of body weight per minute (mL/kg/min). It reflects how well your heart, lungs, blood and muscles work together.</p>
<p>The most accurate test is done on a treadmill or bike in a lab, wearing a mask that measures your breathing while the effort gets harder until you can&rsquo;t continue. Most other numbers you see, including the one on your watch, are estimates.</p>

<h2>Why VO2 max matters for women: the mortality research</h2>
<p>The study most often cited followed 122,007 adults who took a treadmill test at the Cleveland Clinic between 1991 and 2014. About 41% were women, and the average age was 53. Researchers grouped people by fitness compared with others of the same age and sex, then tracked deaths over a median of 8.4 years. It was published in <i>JAMA Network Open</i> in 2018.</p>
<ul>
<li>People in the lowest fitness group had about 5 times the risk of death of those in the top group (the top 2.3%), after adjusting for other factors.</li>
<li>For comparison, in the same analysis smoking was linked to about 1.4 times the risk, and diabetes about 1.4 times.</li>
<li>In women, the difference between the &ldquo;high&rdquo; and &ldquo;elite&rdquo; fitness groups wasn&rsquo;t statistically significant.</li>
</ul>
<p><b>This is an association, not proof that raising your VO2 max will lengthen your life.</b> Everyone in it was having a treadmill test at a hospital, and fitter people may differ in many other ways that the adjustments can&rsquo;t fully capture.</p>

<h2>How VO2 max changes with age in women</h2>
<p>A US registry of 7,783 lab treadmill tests (3,172 of them in women), collected in 2014 and 2015, set reference values by age. For women, the middle value (50th percentile) was:</p>
<table>
<tr><th>Age</th><th>Middle VO2 max for women (mL/kg/min)</th></tr>
<tr><td>30&ndash;39</td><td>30.2</td></tr>
<tr><td>40&ndash;49</td><td>26.7</td></tr>
<tr><td>50&ndash;59</td><td>23.4</td></tr>
<tr><td>60&ndash;69</td><td>20.0</td></tr>
</table>
<p>Across the adult years, women&rsquo;s values were about 10% lower each decade. These are snapshots of different women at different ages, not the same women followed over time. The menopause years bring other abrupt body changes too (see <a href="/news/menopause-physiological-cliff-study/">our report on a study of a million women</a>).</p>

<h2>How to raise VO2 max: what trials in women found</h2>
<h3>More moderate exercise, more gain</h3>
<p>The DREW trial, published in <i>JAMA</i> in 2007, randomly assigned 464 inactive postmenopausal women in the Dallas area (ages 45 to 75, average 57, all overweight or with obesity and raised blood pressure) to no exercise or one of three exercise amounts for 6 months. The exercise groups worked at a moderate pace, set at about half of each woman&rsquo;s own peak capacity.</p>
<ul>
<li>About 72 minutes a week: fitness up about 4% compared with the control group.</li>
<li>About 136 minutes a week: up about 6%.</li>
<li>About 192 minutes a week: up about 8%.</li>
</ul>
<p><b>Even the smallest amount, well under the official 150 minutes, raised fitness, and more brought more.</b></p>

<h3>Do intervals work better?</h3>
<p>High-intensity interval training (HIIT) alternates hard bursts with easier recovery. A 2026 review in <i>Frontiers in Physiology</i> pooled 19 randomized trials with 646 women aged about 44 to 81, focused on women around and after menopause. In the 8 trials (168 women) that measured VO2 max, HIIT raised it more than the comparison groups, which included no exercise and steady moderate exercise. Trials that measured a closely related number, VO2 peak, didn&rsquo;t show a clear effect. On its own, it did little for everyday physical function such as strength or getting up from a chair.</p>
<p>A small Spanish trial shows what this looks like in practice. It randomized 54 women aged 55 to 85 (average about 68) to hour-long sessions twice a week of either high-intensity interval circuits or steady moderate training, or to no training, for 18 weeks; 41 finished. Compared with the no-training group, estimated VO2 max was about 3.4 mL/kg/min higher with the interval circuits and 1.9 higher with moderate training. The difference between the two training groups wasn&rsquo;t statistically significant, and VO2 max was estimated with an equation, not measured.</p>
<p>In a 2023 review of 29 trials in mostly younger adults (807 people, average age about 34), HIIT came out slightly ahead of steady exercise for fitness, but the authors called the clinical importance of the difference limited.</p>

<h3>What about &ldquo;zone 2&rdquo;?</h3>
<p>&ldquo;Zone 2&rdquo; usually means a steady pace where you can still talk. There&rsquo;s no single agreed definition, and none of the trials described here tested it under that name. The closest evidence here is DREW&rsquo;s moderate pace, which did raise fitness.</p>

<h2>Studies at a glance</h2>
<table>
<tr><th>Study</th><th>Who</th><th>What was tested</th><th>Length</th><th>Main result</th></tr>
<tr><td>Mandsager et al., 2018</td><td>122,007 adults, ~41% women, avg. 53</td><td>Treadmill fitness vs. death (observational)</td><td>Median 8.4 years</td><td>Lowest fitness: ~5x risk vs. top group</td></tr>
<tr><td>DREW (Church et al., 2007)</td><td>464 postmenopausal women, avg. 57</td><td>~72, 136 or 192 min/week moderate exercise</td><td>6 months</td><td>Fitness up ~4%, 6%, 8% vs. control</td></tr>
<tr><td>Cai et al., 2026 (review)</td><td>646 women in 19 trials, ages ~44&ndash;81</td><td>HIIT vs. various controls</td><td>Varied</td><td>VO2 max improved; little effect on function</td></tr>
<tr><td>Ballesta-Garc&iacute;a et al., 2020</td><td>54 women, avg. ~68</td><td>Interval circuits vs. moderate training, 2x/week</td><td>18 weeks</td><td>Both improved; no significant difference</td></tr>
</table>

<h2>How to estimate your VO2 max</h2>
<p>A lab test is the most accurate, but most people rely on a watch. A 2025 review of 13 small studies (273 people, about a third of them women) found that in most of the studies reporting an error figure, watch estimates were within 10% of lab values, while one study found an average error of about 16%, with the watch reading low. Two studies found watches tended to overestimate in less-fit people and underestimate in very fit ones. The review was done by a single author, and none of the studies tested the newest watch models.</p>
<p><b>Use a watch number to watch your own trend, not as a diagnosis.</b> More on device accuracy lives in <a href="/health-trackers/">Health Trackers</a>.</p>

<h2>What this means for you</h2>
<ul class="ticks">
<li><b>Start with the official baseline.</b> US guidelines (HHS) call for 150 to 300 minutes a week of moderate activity, such as brisk walking, or 75 to 150 minutes of vigorous activity, such as running, or a mix, plus muscle-strengthening work on 2 or more days.</li>
<li><b>Any amount counts.</b> In DREW, about 72 minutes a week still moved the needle.</li>
<li><b>Intervals are one more option.</b> Interval sessions raised VO2 max in trials of midlife and older women, but steady exercise worked too.</li>
<li><b>Keep lifting.</b> Cardio doesn&rsquo;t replace <a href="/bones/strength-training-bone-density-menopause/">strength training for bone and muscle</a>.</li>
</ul>
<p>If you have a heart condition, another health condition or an injury, or haven&rsquo;t been active, check with your clinician before starting harder exercise. Find more routines in <a href="/fitness/">Fitness</a> and the basics in <a href="/foundations/">Sleep &amp; Foundations</a>.</p>""",
 [("Mandsager K, Harb S, Cremer P, Phelan D, Nissen SE, Jaber W. Association of Cardiorespiratory Fitness With Long-term Mortality Among Adults Undergoing Exercise Treadmill Testing. JAMA Network Open, 2018;1(6)", "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2707428"),
  ("Church TS, Earnest CP, Skinner JS, Blair SN. Effects of Different Doses of Physical Activity on Cardiorespiratory Fitness Among Sedentary, Overweight or Obese Postmenopausal Women With Elevated Blood Pressure: A Randomized Controlled Trial. JAMA, 2007;297(19):2081&ndash;2091", "https://jamanetwork.com/journals/jama/fullarticle/1108370"),
  ("Cai L, Guo J, Zhang R, et al. Effects of high intensity interval training (HIIT) on cardiopulmonary fitness and physical function in middle-aged and elderly women: a systematic review and meta-analysis. Frontiers in Physiology, 2026;17", "https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2026.1778052/full"),
  ("Ballesta-Garc&iacute;a I, Mart&iacute;nez-Gonz&aacute;lez-Moro I, Ramos-Campo DJ, Carrasco-Poyatos M. High-Intensity Interval Circuit Training Versus Moderate-Intensity Continuous Training on Cardiorespiratory Fitness in Middle-Aged and Older Women: A Randomized Controlled Trial. IJERPH, 2020;17(5):1805", "https://www.mdpi.com/1660-4601/17/5/1805"),
  ("Guo Z, Li M, Cai J, et al. Effect of High-Intensity Interval Training vs. Moderate-Intensity Continuous Training on Fat Loss and Cardiorespiratory Fitness in the Young and Middle-Aged. IJERPH, 2023;20(6):4741", "https://www.mdpi.com/1660-4601/20/6/4741"),
  ("Kaminsky LA, Arena R, Myers J. Reference Standards for Cardiorespiratory Fitness Measured With Cardiopulmonary Exercise Testing: Data From the FRIEND Registry. Mayo Clinic Proceedings, 2015;90(11):1515&ndash;1523", "https://www.mayoclinicproceedings.org/article/S0025-6196(15)00642-4/pdf"),
  ("&#381;eleznik Me&#382;an L. Accuracy of wearables for determining the maximal oxygen uptake and lactate threshold: a qualitative systematic review. Frontiers in Sports and Active Living, 2025;7:1707991", "https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2025.1707991/full"),
  ("U.S. Department of Health and Human Services. Physical Activity Guidelines for Americans, 2nd edition: Executive Summary", "https://odphp.health.gov/sites/default/files/2019-10/PAG_ExecutiveSummary.pdf"),
  ("CDC. What You Can Do to Meet Physical Activity Recommendations", "https://www.cdc.gov/physical-activity-basics/guidelines/index.html")]),
article("/supplements/urolithin-a-evidence/", "/supplements/", "Supplements",
 "Urolithin A: What the Human Trials Show",
 "Urolithin A: what the human trials actually show",
 "Does urolithin A help muscle and mitochondria? What the human trials found, who was studied, the doses tested and what is still animal-only.",
 "2026-11-06",
 "Urolithin A is sold as a way to renew your mitochondria, the energy factories inside your cells. The most striking results come from worms and mice. Here&rsquo;s what has actually been tested in people, and what it found.",
 "A handful of small, company-sponsored trials, mostly in women, found that urolithin A was well tolerated and shifted some blood and muscle markers linked to mitochondria. <b>On the outcomes you&rsquo;d feel, like walking distance and overall strength, the results are mixed and mostly not better than placebo.</b> The lifespan findings come from worms, not people.",
 "human-trial",
 [("Best evidence", "Two 4-month randomized, placebo-controlled trials (66 and 88 adults, both 2022) and a 2026 meta-analysis of 5 trials (236 people)"),
  ("Women included?", "Yes. Women were about 76% of the older-adult trial and 64% of the midlife trial; the athlete trials studied men only"),
  ("Dose tested", "500 mg or 1,000 mg a day for 4 weeks to 4 months"),
  ("Bottom line", "Well tolerated in short trials; marker changes are real but functional benefits are unproven")],
 """<h2>What is urolithin A?</h2>
<p>Urolithin A is a compound made by gut bacteria from dietary compounds called ellagitannins. Not everyone&rsquo;s gut bacteria make it in the same amounts, which is one reason companies sell it already made.</p>
<p>The interest comes from mitophagy: the cell&rsquo;s way of clearing out worn-out mitochondria. <b>In worms, urolithin A extended lifespan; in rodents, it improved exercise capacity and muscle function.</b> Those are animal results. They explain why people are studying it. They don&rsquo;t tell you what it does in a 45-year-old woman.</p>

<h2>Urolithin A human trials: the first safety study</h2>
<p>The first study in people, published in <i>Nature Metabolism</i> in 2019, tested single doses and then 4 weeks of 500 mg or 1,000 mg a day in healthy, sedentary older adults. Urolithin A reached the blood at every dose and had a favorable safety profile. After 4 weeks, it changed blood levels of acylcarnitines (fat-burning byproducts) and the activity of mitochondrial genes in muscle.</p>
<p>That&rsquo;s a molecular signal, not a measure of strength or energy. The study was sponsored by Amazentis, the company that makes a commercial urolithin A product.</p>

<h2>Does urolithin A improve muscle endurance in older adults?</h2>
<p>A trial in <i>JAMA Network Open</i> (2022) randomized 66 adults aged 65 to 90 in Seattle, average age about 72. <b>Fifty were women (about 76%)</b>, and all were White. Half took 1,000 mg of urolithin A daily for 4 months; half took a placebo. Neither participants nor researchers knew who got which.</p>
<ul>
<li><b>Walking (a main outcome):</b> no significant difference. The urolithin A group walked about 61 meters farther on a 6-minute walk test, but the placebo group improved too, by about 43 meters.</li>
<li><b>Muscle energy production (the other main outcome):</b> no effect on peak energy output in a hand muscle.</li>
<li><b>Muscle endurance:</b> at 2 months, the urolithin A group could do more repeated contractions with a hand muscle and a leg muscle than placebo. By 4 months the difference was no longer significant, because the placebo group had caught up.</li>
<li><b>Blood markers:</b> acylcarnitines and several ceramides (fats linked to metabolic health) fell from baseline in the urolithin A group.</li>
<li><b>Safety:</b> side effects were similar in both groups, with no serious adverse events.</li>
</ul>
<p>Several authors were affiliated with Amazentis, which supplied the capsules.</p>

<h2>What about women in midlife?</h2>
<p>The trial closest to this site&rsquo;s readers, published in <i>Cell Reports Medicine</i> in 2022, randomized 88 sedentary, overweight adults (BMI 25 to 34.9) aged about 40 to 65, average age in the low 50s. <b>Fifty-six were women (about 64%).</b> They took a placebo, 500 mg or 1,000 mg of urolithin A daily for 4 months.</p>
<ul>
<li><b>Main outcome, peak cycling power:</b> no significant difference from placebo.</li>
<li><b>Hamstring strength:</b> rose about 12% on 500 mg and about 10% on 1,000 mg, a significant difference from placebo, whose strength fell. Thigh (quadriceps) strength and grip strength didn&rsquo;t differ.</li>
<li><b>Aerobic fitness:</b> peak oxygen use rose about 10% on 1,000 mg, but the difference from placebo fell just short of significance.</li>
<li><b>Walking:</b> the 1,000 mg group walked about 33 meters farther in 6 minutes, but this wasn&rsquo;t significantly different from placebo.</li>
<li><b>Inflammation:</b> C-reactive protein, a blood marker of inflammation, fell on 1,000 mg.</li>
<li><b>Safety:</b> described as well tolerated; most muscle-related side effects were linked to the biopsy procedure.</li>
</ul>
<p>The lead and senior authors were affiliated with Amazentis, which supplied the product. Lean muscle mass didn&rsquo;t change compared with placebo.</p>

<h2>What does the meta-analysis of urolithin A trials say?</h2>
<p>A 2026 review in <i>Frontiers in Nutrition</i>, by authors who reported no conflicts of interest, pooled the randomized trials of urolithin A and muscle: 5 trials, 236 people. Three of the five studied young male athletes or runners, so the evidence in women rests on the two trials above.</p>
<ul>
<li>Only the 6-minute walk could be combined, from two trials: about 17 meters farther with urolithin A, a difference that wasn&rsquo;t statistically significant. The authors rated certainty as low.</li>
<li>Strength results were mixed: a few measures improved in single trials, while bench press and squat strength didn&rsquo;t differ from placebo.</li>
<li><b>The trials were small and short (4 weeks to 4 months), and long-term safety is unknown.</b> The authors called the findings hypothesis-generating and said larger, longer trials are needed.</li>
</ul>

<h2>Urolithin A doses tested, and in whom</h2>
<table>
<tr><th>Study</th><th>Who</th><th>Dose</th><th>Length</th><th>Main result</th></tr>
<tr><td>Andreux et al., 2019</td><td>Healthy sedentary older adults</td><td>Single doses; then 500 or 1,000 mg/day</td><td>4 weeks</td><td>Safe; mitochondrial markers changed</td></tr>
<tr><td>Liu et al., 2022</td><td>66 adults 65&ndash;90, 76% women</td><td>1,000 mg/day</td><td>4 months</td><td>Walking not better than placebo; early endurance gain</td></tr>
<tr><td>Singh et al., 2022</td><td>88 adults ~40&ndash;65, 64% women</td><td>500 or 1,000 mg/day</td><td>4 months</td><td>Hamstring strength up; main outcome not met</td></tr>
<tr><td>Dao et al., 2026 (review)</td><td>236 people in 5 trials</td><td>500&ndash;1,000 mg/day</td><td>4 weeks&ndash;4 months</td><td>Walking gain not significant; low certainty</td></tr>
</table>
<p>These are the amounts studies tested, not recommendations. Talk to your clinician before starting any supplement.</p>

<h2>Is urolithin A FDA-approved?</h2>
<p>No. In 2018, Amazentis notified the FDA that it considers urolithin A &ldquo;generally recognized as safe&rdquo; (GRAS) as an ingredient in foods such as protein shakes, nutrition bars and yogurts, at up to 500 or 1,000 mg per serving. On December 20, 2018, the FDA replied that it had no questions about that conclusion.</p>
<p><b>A GRAS &ldquo;no questions&rdquo; letter is about safety as a food ingredient. It isn&rsquo;t an approval, and it says nothing about whether urolithin A works.</b></p>

<h2>The honest bottom line</h2>
<ul class="ticks">
<li><b>If your goal is muscle or strength:</b> the trials show scattered gains on some measures and no difference on most. <a href="/bones/strength-training-bone-density-menopause/">Strength training</a> has far stronger evidence.</li>
<li><b>If your goal is energy or fitness:</b> aerobic gains didn&rsquo;t clearly beat placebo. Regular cardio has much stronger evidence for helping you <a href="/fitness/vo2-max-women/">raise VO2 max</a>.</li>
<li><b>If your goal is longevity:</b> the lifespan data are from worms. None of the human trials measured lifespan.</li>
</ul>
<p>All three trials described above involved researchers from the company that makes a commercial urolithin A product, and none lasted longer than 4 months. Talk to your clinician before starting it, especially if you&rsquo;re pregnant, nursing, take medication or manage a health condition.</p>
<p>More evidence checks: <a href="/supplements/creatine-for-women-over-40/">creatine for women over 40</a> and the full <a href="/supplements/">Supplements</a> hub. For the basics, see <a href="/foundations/">Sleep &amp; Foundations</a>.</p>""",
 [("Liu S, et al. Effect of Urolithin A Supplementation on Muscle Endurance and Mitochondrial Health in Older Adults: A Randomized Clinical Trial. JAMA Network Open, 2022;5(1):e2144279", "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2788244"),
  ("Singh A, et al. Urolithin A improves muscle strength, exercise performance, and biomarkers of mitochondrial health in a randomized trial in middle-aged adults. Cell Reports Medicine, 2022", "https://www.sciencedirect.com/science/article/pii/S2666379122001586"),
  ("Andreux PA, et al. The mitophagy activator urolithin A is safe and induces a molecular signature of improved mitochondrial and cellular health in humans. Nature Metabolism, 2019;1:595&ndash;603", "https://www.nature.com/articles/s42255-019-0073-4"),
  ("Dao T, Nguyen TT, Gariani K, Kim HJ, Ryu D. Effects of Urolithin A supplementation on muscle health outcomes in humans from randomized controlled trials. Frontiers in Nutrition, 2026;13", "https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2026.1834344/full"),
  ("U.S. Food and Drug Administration. GRAS Notice No. 791: Urolithin A", "https://www.hfpappexternal.fda.gov/scripts/fdcc/index.cfm?id=791&set=grasnotices"),
  ("U.S. Food and Drug Administration. Agency Response Letter, GRAS Notice No. GRN 000791", "https://www.fda.gov/media/120300/download")]),
]
