# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts posts and comments from **r/TheLastAirbender**, a public subreddit about *Avatar: The Last Airbender* and *The Legend of Korra*, into two labels: `argued` (an opinion backed by a specific, checkable detail from the show) and `take` (an opinion with no specific evidence). The question it answers is the one regulars ask without saying it: is this person making a case, or just stating a view?

The subreddit is built around one franchise, which the brief's guideline advises against because of spoilers. I chose it anyway because both shows ended years ago (2008 and 2014), so spoiler risk is minimal. I only kept posts about the original shows and the older comics, and excluded anything about the live-action series, the upcoming movie, or other new releases.

---

## Label Taxonomy

### `argued`

**Definition:** Makes a claim about the show and backs it with a specific, checkable detail: an episode, scene, quote, or in-show event.

**Example 1:**
> Jet is overhated. He's literally a depiction of what happened in real life and how extremist come to exist. His whole town was killed and he's one of the view survivors. He literally witnessed his family and friends being killed by the fire nation... And at the end with all the hate he had towards the fire nation it wasn't even the fire nation that killed him.

**Example 2:**
> Unpopular Opinion: Zuko and Ozai have a lot of parallels... Both are disfavored by their fathers. Both have a more talented and smarter sibling that their father favors over them... Both end up betraying their fathers. With Ozai, it was Azulon. With Zuko, it was both Ozai and Iroh.

### `take`

**Definition:** A confident opinion, ranking, or reaction with no specific evidence offered.

**Example 1:**
> I enjoyed legend of Korra just as much as I enjoyed TLA... I don't understand why there's so much hate it's just a different story in the same universe

**Example 2:**
> It's ok to not enjoy season 3 compared to the other seasons :|

### The hardest boundary

**Which two labels:** `argued` vs `take`. The hard posts are strong opinions that mention something from the show without really using it as evidence.

**The decision rule I used every time:**
If the post names a specific episode, scene, quote, or in-show event as a *reason* for its opinion, it's `argued`, even if it's short or heated. Just mentioning a character's name doesn't count, and neither does a vague reference to a whole season ("season 3 was better"). For list posts with several opinions, I label the post as a whole: if most items cite a specific episode, scene, quote, or event, it's `argued`; otherwise it's `take`.

---

## The Dataset

**Where the posts came from:** r/TheLastAirbender, collected on November 11, 2026 by copying pages from old.reddit.com: a search for "unpopular opinion" in the subreddit, plus the full comment threads of three posts — *"Unpopular Opinion: Maybe Maiko Was Never Intended to Survive"*, *"Unpopular Opinion: Sue Has the Best Design, Bending, Combat Choreography and Achievements Among the Gaang Kids"*, and *"Unpopular Opinion (apparently): Let Uncle Iroh had a messy past"*. I left out posts about the live-action series, the upcoming movie, Seven Havens and other new releases; comments with no opinion about the show ("Same", "Me too lmao", server invites); comments about characters' looks; and long real-world history tangents. Duplicate posts were removed.

**How I labelled them:** I labelled 20 posts cold first, using only my definitions (marked `cold` in the note column). The other 147 were pre-labelled by Claude (an AI assistant) using my definitions and decision rule, and marked `prelabeled`. I reviewed the pre-labels but did not read every row closely, and I changed none.

I collected 167 posts instead of 200. I followed the brief's stop rule because I was short on time, and kept a smaller set I could describe honestly instead of rushing more rows.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `take` | 103 | 61.7% |
| `argued` | 64 | 38.3% |
| **Total** | 167 | 100% |

**Three hard cases**

**1.**
> *The post:* "Oh that kuvira fight was pure art"
>
> *Could have been:* `argued` or `take`
>
> *I chose `take`, because:* It names a specific scene (Suyin's fight with Kuvira), but the scene is the thing being praised, not a reason for a separate opinion. My rule needs the event to be evidence for the claim.

**2.**
> *The post:* "Izumi means "fountain"."
>
> *Could have been:* `argued` or `take`
>
> *I chose `argued`, because:* It states no opinion on its own, but in its thread it is offered as evidence that Izumi is Mai's daughter (Zuko and Mai's fountain moment), and it is a specific, checkable detail.

**3.**
> *The post:* A reply that quotes the original poster's list ("Led the 600 day siege of Ba Sing Se", "Was the crown prince of a nation actively waging war...") and then adds: "Iroh fans are literally unhinged..."
>
> *Could have been:* `argued` or `take`
>
> *I chose `take`, because:* The specific events in it are quoted from someone else. The commenter's own contribution is an opinion with no evidence of their own.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42. Trained on **mps (Apple Silicon GPU)** with torch 2.14.1. The device is also recorded in `results.json`.

**Anything I changed from the defaults, and why:** Nothing. I used the default settings.

**Split sizes:** train 116 · val 25 · test 26.

| Label | Train | Val | Test |
|---|---|---|---|
| `argued` | 44 | 10 | 10 |
| `take` | 72 | 15 | 16 |

Both labels have at least 8 examples in the test split, but 10 and 16 are still small, so one post changes a label's score a lot.

---

## How I Used AI

I used Claude throughout this project. Two specific moments:

**Moment 1**

- *What I asked for:* Help choosing a community. I wanted r/TheLastAirbender.
- *What came back:* It pointed out that the brief says to avoid communities built around one show, and suggested broader options like r/television.
- *What I changed:* I kept r/TheLastAirbender because the rule is about spoilers and both shows ended years ago. I limited my data to the original shows and older comics and explained the choice in this README.

**Moment 2**

- *What I asked for:* Help with my acceptance criteria.
- *What came back:* It gave me multiple-choice options for each number; I picked the numbers, and it wrote the reasons under each criterion based on my picks. When I asked it to check them, it pointed out that a 0.65 accuracy target was too easy because a model that always guesses `take` would score 0.65 if `take` hit my 65% balance limit.
- *What I changed:* I raised the accuracy target from 0.65 to 0.70, and I changed criterion 5 to say "top predicted probability" so it is clear what "confidence" means.

**Pre-labelling disclosure:** Claude pre-labelled 147 of my 167 posts using my definitions and decision rule. It also pulled the individual posts out of the Reddit pages I copied and dropped the ones outside my scope. The 20 rows marked `cold` I labelled myself with no AI help. Claude also wrote the first drafts of my label definitions and of this README from what I had done, which I reviewed.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.654 | 0.615 | -0.038 |
| Macro F1 | 0.649 | 0.381 | -0.268 |
| F1 — `argued` | 0.690 | 0.000 | -0.690 |
| F1 — `take` | 0.609 | 0.762 | +0.153 |

**What I predicted before I looked:**
I predict the trained model will beat the baseline on `take` (F1 above 0.609) but not on `argued` (F1 at or below 0.690), because my training data is about 62% `take` (103 of 167), so the model will lean toward `take` when unsure and misclassify real `argued` posts.

**How the prediction held up:**
The direction was right, but the result was more extreme: the model predicted `take` for all 26 posts, so its accuracy equals the always-take rate (0.615) and `argued` F1 is 0.

**What the gap actually means:**
Fine-tuning added nothing: the trained model scored below the zero-shot baseline on accuracy (0.615 vs. 0.654) and macro F1 (0.381 vs. 0.649). Its 0.615 is exactly what always guessing `take` scores, and its higher `take` F1 comes from labelling every post `take`, not from learning the label. The baseline is only one post above that floor, so neither model is doing much better than the label counts alone.



---

## Run Log — Before

**Device:** mps (Apple Silicon GPU), torch 2.14.1

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.615 | 0.615 | 0.615 | 0.000 |
| Macro F1 | 0.381 | 0.381 | 0.381 | 0.000 |
| F1 — `argued` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `take` | 0.762 | 0.762 | 0.762 | 0.000 |

**Spread:** The notebook reports this as "stable enough to trust," but the zero spread isn't a sign of a reliable model. On every seed the model predicted `take` for all 26 test posts, so it scores the always-`take` rate (16/26 = 0.615) no matter which split it gets. Validation accuracy stayed at 0.6 for all three epochs, so the model never moved off the majority label.

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | argued | take |
|---|---|---|
| **argued** | 0 | 10 |
| **take** | 0 | 16 |

**My biggest off-diagonal number, and what it means:**
All 10 real `argued` posts were predicted `take`, and 0 real `take` posts went the other way. The model didn't learn the `argued`/`take` boundary at all. It never predicts `argued`, so it isn't drawing a wrong line between the labels; it has fallen back to the majority label.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
