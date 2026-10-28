# Parva Regina topic scout runbook

A weekly scheduled run (Sunday afternoon, Pacific) follows this file. It finds the week's new longevity research that matters for women about 35-50, puts the best item on the calendar as a Wednesday news article, keeps the evergreen queue full, drafts that week's newsletter, and sends the owner a short digest.

The publisher (`_src/PUBLISHING.md`) writes and fact-checks each article on its date. The scout only plans and drafts the newsletter.

## Cadence it fills

- **Wed:** news, chosen by the scout. Keep the next 2 Wednesdays filled.
- **Mon/Fri:** evidence checks and foundations, pre-planned. If fewer than 3 weeks of Mon/Fri items remain, add evergreen topics (see "Evergreen ideas"). Add at most 4 items per run.

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

Evergreen items use `"hub": "evidence"` or `"foundations"`, `"kind": "evergreen"`, and a `brief.angle` naming the key sources to find.

## Evergreen ideas (use, then remove from this list)

Hormone therapy and long-term health: what trials show (WHI and after) · Vitamin D for women over 40 · Omega-3 and the heart · Cold plunge and sauna evidence · Intermittent fasting for women · Biological age tests: worth it? · Retinoids and skin aging · Sunscreen and photoaging · Alcohol and aging · Walking steps per day and mortality · Grip strength as a health marker · Iron and ferritin in perimenopause.

## Newsletter draft

Write `_src/newsletter/<next Monday's date>.md`: "The Little Queen Brief". Subject line under 50 characters; a 1-line opener; the 3 most useful findings of the past week (published articles and other kept items), each a short paragraph with its evidence label and a link to the article or source; one "habit with strong evidence" line linking a Foundations article; sign-off "The Parva Regina Research Desk". Same "Never" rules as `PUBLISHING.md`. Commit it with the calendar.

## Commit and report

1. Run `python3 _src/build.py`, then commit `_src/calendar.json`, `_src/newsletter/`, `status.json` (and `_src/TOPICS.md` if you removed evergreen ideas) with author `Rogenie Cordero <rogenie@gmail.com>` and message `Topics: <dates added>`, push to `main`.
2. Send one push notification titled "Parva Regina: this week in longevity research": the 3-5 most notable findings you saw (kept or not), one line each; which became articles and when; and the newsletter subject line plus a note that the draft is in `_src/newsletter/`. If nothing qualified or a search or push failed, say so.

## Never

Follow the "Never" list in `_src/PUBLISHING.md`.
