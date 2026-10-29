# Parva Regina topic scout runbook

A weekly scheduled run (Sunday afternoon, Pacific) follows this file. It finds the week's new longevity research that matters for women about 35-50, puts the best item on the calendar as a Wednesday news article, keeps the evergreen queue full, drafts that week's newsletter, and sends the owner a short digest.

The publisher (`_src/PUBLISHING.md`) writes and fact-checks each article on its date. The scout only plans and drafts the newsletter.

## Cadence it fills

- **Wed:** news, chosen by the scout. Keep the next 2 Wednesdays filled.
- **Mon/Fri:** evergreen articles, pre-planned, rotating across the site's sections so each gets new articles regularly: Fitness (`/fitness/`), Meal Plans (`/meal-plans/`), Health Trackers (`/health-trackers/`), Evidence Checks (`/evidence/`), and occasionally Foundations (`/foundations/`, for habits that don't fit the other sections, such as sleep). Don't schedule two items from the same section back to back when another section has none in the next 2 weeks. If fewer than 3 weeks of Mon/Fri items remain, add evergreen topics (see "Evergreen ideas"). Add at most 4 items per run.
- **Trending topics take priority** over evergreen Mon/Fri items (see "Trend check"). Publishing stays at 3 a week until the owner changes it.

## Trend check (Sunday and Wednesday runs)

Goal: when women 35-50 are suddenly searching or watching something about aging, Parva Regina publishes the evidence-based answer that week. The Sunday run does this check as well as the full scout; the Wednesday run does only this check.

**Where to look (last 7 days):**
- Google Trends: search `trends.google.com` for rising topics in health, skin, menopause and supplements; also WebSearch phrases like "trending wellness 2026", "viral skincare trend", "menopause TikTok trend", "longevity supplement news this week".
- News coverage: WebSearch restricted to major outlets (nytimes.com, washingtonpost.com, today.com, health.com, womenshealthmag.com, self.com, npr.org, cnn.com/health). Several outlets covering the same thing in the same week is the strongest signal.
- Video platforms, through search: WebSearch restricted to youtube.com and tiktok.com for the same phrases. You can't log in, so judge by how many recent results and articles about the trend you find.
- Your own audience: with the Metricool connector (brand id 2896902, "parvaregina"), check which recent TikTok and YouTube posts got the most views (use getAnalyticsAvailableMetrics for the posts connector to find the field IDs). A topic that over-performed on the account counts as trending for our readers.

**A trend qualifies only if all are true:**
1. Several independent sources show a rise in the last 7 days (not one viral post).
2. It touches women about 35-50: skin, menopause, muscle, bone, sleep, weight, heart, brain, or a product or routine they're being sold.
3. There is research to check it against: at least one peer-reviewed human study, a review, or an official agency statement you can open in this run. If the trend has no research behind it, it can still qualify; the angle is then "what the evidence does and doesn't show", and the brief must name the closest real studies.
4. It doesn't repeat a published article or calendar item. If it overlaps, the angle is what's new, and the article links the older one.

**Swapping it in:**
- Put the best qualifying trend in the next Mon or Fri slot that is at least 2 days away (on Sunday: Monday is too soon, so use Friday unless the trend is fading fast; on Wednesday: Friday is fine). Never touch a slot dated within 2 days, and never move a Wednesday news item.
- Move the evergreen item it replaces to the first empty Mon or Fri after the last calendar item. Don't delete it.
- Trend items use `"kind": "trend"` and the section that fits: `"hub": "evidence"` (checking a claim or product), `"fitness"` (a workout or exercise trend), `"meal-plans"` (a food or eating trend), `"health-trackers"` (a wearable, test or tracking trend) or `"foundations"` (any other habit), and a brief with: `"trend"` (what people are searching or watching, and where you saw it), `"sources"` (the URLs that showed the rise), plus the usual `"angle"` and the key studies to find.
- At most 2 trend swaps per week. If nothing qualifies, change nothing; that's a normal result.

**Report:** Wednesday runs send one push notification titled "Parva Regina: trending this week": what's trending (2-4 items, one line each), whether one was swapped in and for which date, and which evergreen item moved where. If nothing qualified, say so in one line. Sunday runs add a "Trending" line to their usual digest instead of sending a second notification.

Wednesday-only runs: run `python3 _src/build.py`, then commit `_src/calendar.json` and `status.json` with author `Rogenie Cordero <rogenie@gmail.com>` and message `Trend: <date swapped>`, push to `main`. Don't touch the newsletter on Wednesdays. If nothing changed, don't commit.

## Where to look (last 10 days)

One search per source, restricted to the domain:

| Source | Domain |
|---|---|
| Journal news and papers | nature.com, jamanetwork.com, thelancet.com, bmj.com, cell.com, nejm.org, menopause journal (journals.lww.com) |
| Research press releases | eurekalert.org, nih.gov, nia.nih.gov |
| Regulators and guidelines | fda.gov, uspreventiveservicestaskforce.org, cdc.gov, ods.od.nih.gov |
| Trials | clinicaltrials.gov (new results on aging, menopause, supplements) |

Good search phrases: "menopause study", "perimenopause trial", "women aging study", "healthspan women", "postmenopausal randomized trial", "biological age", plus any topic trending on the Parva Regina TikTok (red light, creatine, magnesium, NAD, collagen, zone 2, VO2 max, senolytics, lymphatic).

## Keep an item only if all are true

1. It's a published, peer-reviewed study (or an official agency action) from the last 21 days, and the paper or its abstract can be opened in this run.
2. It involves people, or it's an animal/cell finding big enough that readers will see it in the news anyway (then the angle is "what it does and doesn't mean").
3. It matters to women about 35-50: menopause transition, muscle, bone, heart, brain, sleep, skin, metabolism, or a supplement/device they're being sold.
4. It doesn't repeat a published article or calendar item (check `_src/calendar.json` and `_src/articles.py`). If it overlaps, the new article is about what's new and links the older one.

Rank keepers by: human trials over observational over animal; women-specific over mixed; size; how many readers it touches.

## Calendar entry

Add to `_src/calendar.json` `items`, kept in date order:

```json
{"date": "YYYY-MM-DD", "hub": "news", "path": "/news/<slug>/", "title": "<under 60 characters, plain>", "status": "todo", "kind": "news",
 "brief": {"study": "<paper title, journal, date>", "source": "<URL the search returned>", "evidence": "human-trial | human-obs | animal | cell | review",
           "who": "<participants>", "finding": "<one line>", "angle": "<what the article explains, incl. limits and what it means for readers>",
           "links": ["<2-3 Parva Regina paths>"]}}
```

Evergreen items use `"hub"` set to `"fitness"`, `"meal-plans"`, `"health-trackers"`, `"evidence"` or `"foundations"` (with `"path": "/<hub>/<slug>/"`), `"kind": "evergreen"`, and a `brief.angle` naming the key sources to find.

## Evergreen ideas (use, then remove from this list)

Fitness: a 20-minute home strength routine for women 40+ · Walking, steps per day and health · Balance and fall prevention after 40 · Hormones and training around the menopause transition · Recovery and rest days.
Meal Plans: a 7-day protein-first meal plan (every number from USDA FoodData Central; built around protein, fiber, calcium and plants; no calorie-restriction or weight-loss targets) · High-protein breakfasts · Fiber for women 35+ · Calcium and vitamin D from food · A week of anti-inflammatory-style eating: what the research shows.
Health Trackers: Sleep trackers and wearables: how accurate are they? · What to track after 35, and what to skip · Tracking protein and macros without obsessing · Heart-rate zones explained · Lab tests to discuss with your doctor in your 40s · Continuous glucose monitors for people without diabetes: the evidence.

Hormone therapy and long-term health: what trials show (WHI and after) · Vitamin D for women over 40 · Omega-3 and the heart · Cold plunge and sauna evidence · Intermittent fasting for women · Biological age tests: worth it? · Retinoids and skin aging · Sunscreen and photoaging · Alcohol and aging · Walking steps per day and mortality · Grip strength as a health marker · Iron and ferritin in perimenopause.

## Newsletter draft

Write `_src/newsletter/<next Monday's date>.md`: "The Little Queen Brief". Subject line under 50 characters; a 1-line opener; the 3 most useful findings of the past week (published articles and other kept items), each a short paragraph with its evidence label and a link to the article or source; one "habit with strong evidence" line linking a Fitness, Meal Plans or Foundations article; sign-off "The Parva Regina Research Desk". Same "Never" rules as `PUBLISHING.md`. Commit it with the calendar.

## Commit and report

1. Run `python3 _src/build.py`, then commit `_src/calendar.json`, `_src/newsletter/`, `status.json` (and `_src/TOPICS.md` if you removed evergreen ideas) with author `Rogenie Cordero <rogenie@gmail.com>` and message `Topics: <dates added>`, push to `main`.
2. Send one push notification titled "Parva Regina: this week in longevity research": the 3-5 most notable findings you saw (kept or not), one line each; which became articles and when; and the newsletter subject line plus a note that the draft is in `_src/newsletter/`. If nothing qualified or a search or push failed, say so.

## Never

Follow the "Never" list in `_src/PUBLISHING.md`.
