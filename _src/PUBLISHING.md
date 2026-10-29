# Parva Regina publishing runbook

Scheduled runs (Mon/Wed/Fri) follow this file to publish articles on parvaregina.com. Publishing is fully automatic by the owner's choice: nothing waits for human review, so every run must pass every check below before anything goes live. When a check fails, the article does not publish.

The site: evidence-based longevity science for women roughly 35-50 (the perimenopause decade and just after). Voice: warm, precise, calm. The reader is smart, busy and tired of hype.

## Each run

1. Get today's date in America/Los_Angeles.
2. Open `_src/calendar.json` and list every item whose `date` is today **or earlier** and whose status is `todo` or `written`. These are due. Skip `published` and `held`.
   - Nothing due: stop. No commits, no message.
3. Work through due items oldest first, one at a time: research, write, fact-check, publish, log. A past date means a run was missed; catch it up and say so in the run record's `note`.
4. Add each article to the end of the `ARTICLES` list in `_src/articles.py` with the `article(...)` helper, `published` set to **today's** date (the run date), then follow "Publish". Update the calendar item's `date` to today if it was a catch-up.

Never publish an item dated in the future.

## Sources (official and primary only)

Allowed as sources: peer-reviewed papers (PubMed, PubMed Central, Europe PMC, the journal's own page), ClinicalTrials.gov, and government health agencies (NIH, NIH Office of Dietary Supplements, National Institute on Aging, FDA, CDC, HHS, USPSTF). A journal's or university's official press release may support a summary of a study, but the paper (or its abstract) must be linked first. News sites can point you to a study and may be cited only for comments by independent experts, labeled as such.

**Fetching:** scheduled runs can't approve web fetches, and fetching a URL that didn't come from a search is refused. Search first (restrict to the domain, e.g. `pmc.ncbi.nlm.nih.gov` or `europepmc.org`), then fetch the URL the search returned. NCBI pages sometimes return a "Checking your browser" page instead of the article; when that happens, search for the same paper on `europepmc.org` or the journal's site and use that. **A study you couldn't open in this run is a study you can't cite.**

## Writing standards

- **Audience:** women about 35-50 in the US. Explain terms once in plain words.
- **Length:** 800-1,400 words. Short paragraphs, short sentences. Bold the one line per section a skimmer must not miss.
- **Title:** under 60 characters, leading with the search phrase people type ("creatine for women over 40", "red light therapy for skin"). **Description:** under 155 characters.
- **Opening:** a 1-2 sentence intro, then the `quick` answer (1-3 sentences) that fully answers the search question. This is what wins featured snippets.
- **Evidence at a glance (`glance`):** always include best evidence (type, size, year), whether women were included, the dose or protocol tested, and a one-line bottom line.
- **Evidence label (`evidence`):** the strongest evidence the article's main claim rests on: `human-trial`, `human-obs`, `animal`, `cell` or `review`. If only animal or cell evidence exists, the article must say so in the first 100 words.
- **H2s:** put the search phrase or a close variant in at least two H2s. Phrase some H2s as questions people search.
- **Every study described** gets: who (number, sex, age), design, how long, what was measured, what was found. Say plainly when women weren't included or were a minority.
- **Tables** for doses and multiple studies. A "What this means for you" or "The honest bottom line" section near the end.
- **Links:** at least 3 internal links to Parva Regina articles or hubs. Link freely to planned calendar paths; the build turns links to unpublished articles into plain text.
- **Byline:** set by the helper ("Parva Regina Research Desk"). Never put a person's name on an article.

### Kinds of articles

- **News** (`hub` `/news/`, hub name "Latest Research", `kind` `news`, chosen by the topic scout): one new study or official action from the last 21 days. Lead with what was found, then who was studied, then limits, then "What this means for you". Use `NewsArticle`-style headlines: what happened, in plain words. Don't call a study "new" if it was published more than 30 days before the article date.
Sections are grouped in the menu as **Body** (Fitness, Meal Plans, Bones & Strength, Sleep & Foundations), **Beauty** (Skin, Hair, Procedures) and **Longevity** (Latest Research, Supplements, Health Trackers). Every article belongs to exactly one section; set `hub`, `hub_name` and the path prefix to match.

- **Supplements** (`/supplements/`, hub name "Supplements"): "Does X work?" evidence checks on a supplement. Separate human trials from animal and cell work. Give the honest bottom line by goal (skin, muscle, bone, sleep, brain). A supplement aimed mainly at skin or hair (e.g. collagen, biotin) goes in Skin or Hair instead.
- **Skin** (`/skin/`, hub name "Skin"): skin aging, skincare ingredients, sun protection, and devices or at-home tools such as red light and facial massage. Use dermatology society and FDA sources alongside trials. Separate what's proven from what's marketed.
- **Hair** (`/hair/`, hub name "Hair"): thinning, shedding and greying. Name the medical causes worth ruling out (iron, thyroid, B12, hormones) and treatments with FDA approval or trial evidence. Say plainly when a popular supplement or product lacks evidence.
- **Procedures** (`/procedures/`, hub name "Procedures"): in-office treatments (lasers, microneedling, injectables, fillers, peels). Cover what studies show, how long results last, downtime, risks and side effects from the source, and questions to ask a board-certified provider. No prices unless from an official source, no provider or brand recommendations, and never present a procedure as risk-free. End every procedures article with: "Talk to a board-certified dermatologist or plastic surgeon about whether this is right for you."
- **Bones & Strength** (`/bones/`, hub name "Bones & Strength"): bone density, muscle, balance and falls. Use official sources for calcium, vitamin D and screening guidance (NIH ODS, USPSTF, Bone Health & Osteoporosis Foundation).
- **Sleep & Foundations** (`/foundations/`, hub name "Sleep & Foundations"): sleep and any evidence-backed habit that doesn't fit another section. Use official guidelines for any number a reader would act on (activity minutes, protein RDA, screening ages).
- **Fitness** (`/fitness/`, hub name "Fitness"): strength, cardio, mobility and daily routines. Base volume and intensity on official guidelines (HHS Physical Activity Guidelines) and trials. Routines list exercises, sets and reps, give an easier option for each move, and tell readers to check with their clinician before starting if they have a health condition, injury or haven't been active.
- **Meal Plans** (`/meal-plans/`, hub name "Meal Plans"): 7-day plans, recipes and nutrition basics. Every calorie, protein, fiber or nutrient number comes from USDA FoodData Central or another official source opened in the run. Build plans around protein, fiber, plants and calcium. No calorie-restriction targets, weight-loss promises, "detox", cleanses or skipped meals. Give swaps for common allergies and vegetarian eaters.
- **Health Trackers** (`/health-trackers/`, hub name "Health Trackers"): what to measure (sleep, steps, heart rate, macros, workouts, lab results), how accurate devices and tests are according to validation studies, and what the numbers can and can't tell you. Name a device only when the study tested that device. Never interpret someone's personal results; point to their clinician.

## Never

- Say anything "reverses aging", "cures", "prevents" a disease, "detoxes", "boosts immunity", or adds years to your life. Don't use "anti-aging miracle", "secret", "hack", "breakthrough" (unless quoting a headline you're debunking), "guaranteed".
- Turn an animal or cell result into advice for people.
- Recommend a dose. You may state the dose a study tested ("the trial tested 0.14 g per kg a day") and official upper limits (e.g. from NIH ODS), always followed by "talk to your clinician".
- Recommend a brand or product, or include affiliate or sales links.
- Invent or imply personal experience ("I tried", "my routine", "our editors use"), testimonials, quotes, statistics or studies. Quote nothing longer than a few words from any source; paraphrase.
- Give diagnosis or treatment advice, or tell anyone to stop or change a medication or hormone therapy.
- Name a public figure's protocol as a reason to do something.
- Use "doctor-approved", "clinically proven" or "science-backed" as selling words.
- Use fear framing. Describe risk with numbers from the source, not adjectives.

## Fact check (required before publishing)

1. List every number, date, sample size, dose, percentage, study design claim, journal name and official guideline in the article.
2. Confirm each one against a source opened in this run. Confirm the year and the population (women? which ages?), not just the number.
3. Anything you can't confirm: remove it, or rewrite the sentence without it. Remove its source from the list if it was the only thing citing it.
4. If the article can't stand without an unconfirmed item, don't publish. Set the calendar item's status to `held`, add a `note`, add a run record with `"result": "held"`, run `python3 _src/build.py`, commit and push only `_src/calendar.json`, `_src/runs.json` and `status.json`, and report HELD with the reason. If the item is still worth doing, you may instead move it to the next empty Mon/Wed/Fri at least 5 days out and say so in its `note`.
5. Re-read the finished article against the "Never" list. Fix anything that breaks it.

## Publish

1. From the repo root run `python3 _src/build.py`. The new article must appear in the live count. The build also makes the share image (`assets/og/<slug>.png`); it needs Pillow (`pip install --break-system-packages pillow` if missing). Commit it with the article.
2. Set the calendar item's status to `published` and add `"url": "https://parvaregina.com<path>"`.
3. Commit with author `Rogenie Cordero <rogenie@gmail.com>` and message `Publish: <title>`, then push to `main`.
4. Verify: fetch the live page once (after a search has returned it, or skip if the fetch is refused) and set `live_verified` accordingly. GitHub Pages usually deploys within a few minutes.
5. Write a social caption for the Parva Regina social engine and save it as `_src/social/<date>-<slug>.md` in the same commit: a hook line naming the reader's question, 3 short takeaways with the evidence label, a soft line pointing to the article ("Full article: link in bio"), and the line "(Wellness education, not medical advice.)". Same "Never" rules, no first-person experience. Don't post it anywhere.
6. Append a run record (see "Run log"), run `python3 _src/build.py` again so `status.json` includes it, commit `Run log: <date>` and push.
7. Finish with a short summary: title, live URL, facts checked, anything removed, and the social caption.

## Corrections

If a run finds an error of fact in a live article (for example while fact-checking a related piece), fix it, add an `updates` note to that article ("<Month D, YYYY>: corrected ..."), append `{"date": ..., "path": ..., "title": ..., "note": ...}` to `_src/corrections.json`, rebuild, commit `Correction: <title>` and push. Mention it in the run summary.

## Run log

Every run that publishes or holds an item appends one record to `_src/runs.json`. Never edit or delete earlier records.

```json
{"date": "YYYY-MM-DD", "at": "<ISO time with Pacific offset>", "result": "published" | "held",
 "path": "<the item's path>", "facts_checked": <n>, "removed": <n>,
 "live_verified": true | false, "social_caption": true | false, "note": "<one line>"}
```
