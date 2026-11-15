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
| 1. Overall accuracy | ≥ 0.70 | 0.615 | 0.615 | 0.615 | MISSED |
| 2. Per-label F1 | `take` ≥ 0.75 and `argued` ≥ 0.65 | 0.762 / 0.000 | 0.762 / 0.000 | 0.762 / 0.000 | MISSED |
| 3. No label above 65% of labels.csv | ≤ 65% | 61.7% | 61.7% | 61.7% | MET |
| 4. Agreement with staff labels | ≥ 85% | 83% | 83% | 83% | MISSED |
| 5. Confident predictions (≥ 0.80) right 10+ points more often | gap ≥ 10 pts | no predictions ≥ 0.80 | no predictions ≥ 0.80 | no predictions ≥ 0.80 | MISSED |

Criteria 3 and 4 don't depend on the seed: 3 is a property of `labels.csv` and 4 is a single check of 30 posts, so the same value is repeated in each column.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | argued | take |
|---|---|---|
| **argued** | 0 | 10 |
| **take** | 0 | 16 |

**My biggest off-diagonal number, and what it means:**
 All 10 real `argued` posts were predicted `take`, and 0 real `take` posts went the other way. The model didn't learn the `argued`/`take` boundary well enough to predict `argued` even once. It never predicts `argued`, so it isn't drawing a wrong line between the labels; it has fallen back to the majority label.


---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.70 on all 3 seeds | MISSED | 0.615 on every seed, which is exactly the always-`take` rate (16/26). |
| 2 | Per-label F1 | `take` ≥ 0.75 and `argued` ≥ 0.65 on all 3 seeds | MISSED | `take` passed (0.762) but `argued` was 0.000 on every seed, and the criterion needs both. |
| 3 | Balance | No label above 65% | MET | `take` is 103 of 167 posts (61.7%). This kept the always-`take` score (0.615) below my 0.70 accuracy target, so criterion 1 caught the collapse. |
| 4 | Agreement | ≥ 85% with staff | MISSED | 25/30 = 83%, one post short of 26/30 (86.7%). |
| 5 | Confidence | ≥ 0.80 predictions right 10+ points more often | MISSED | Mean confidence was 0.61–0.63 when right and 0.56–0.59 when wrong, so no or almost no predictions reached 0.80 and the gap can't be shown. |

**Diagnoses**

**Criteria 1 and 2: the model never predicts `argued`.** My matrix shows all 10 real `argued` posts predicted `take`, on all three seeds. I think the main cause is too little training combined with class imbalance, and less likely my labelling. Evidence:
- **Training was very short.** 116 posts at batch size 16 for 3 epochs is about 24 update steps. Validation accuracy stayed at 0.6 (always-`take`) on every epoch of every seed.
- **Imbalance made `take` the safe answer.** Training had 72 `take` vs 44 `argued`.
- **The model did learn a weak signal.** Its most confident third was 87.5–100% correct and its least confident third only 12.5–25%, so its confidence does separate the labels. That signal just never got strong enough to push any post over 50% toward `argued`.
- **The task is learnable.** The zero-shot baseline reached `argued` F1 = 0.690 from my definitions alone, so the difference is in the text.
- **Labelling may still play a part.** My agreement check shows I under-call the evidence-based label (all 5 disagreements were staff `analysis`, me `hot_take`), and 147 of my 167 labels were pre-labelled and not closely reviewed. But inconsistent labels would more likely give wrong guesses on borderline posts, not a model that never predicts `argued` at all.

**Criterion 4: 83% agreement, one post short.** All five disagreements went the same way: staff said `analysis`, I said `hot_take`. Three were pile (a): I treated any opinion in a post as disqualifying, when the staff rule only requires a checkable fact that carries the argument. This is a consistency problem in how I judge evidence, and it's the same boundary my model failed on. My criterion's reason also assumed I'd be applying my own rule, but this check used the staff taxonomy.

**Criterion 5: no confident predictions.** The model's confidence stayed around 0.6, close to the 62% share of `take` in training. This follows from the same cause as criteria 1 and 2: with so little training, the model never became sure of anything.

---

## Agreement Report

**Agreement rate:** 25 / 30 = 83%

**Disagreements**

**1.**
> *The post:* "Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* I think my `hot_take` is defensible. Rule 1 says `analysis` needs a specific, checkable fact that carries the argument. The only number given is the 1:45 cutoff. The actual finding that carries the argument, that the slowdown was "almost identical," has no number, so a reader can't check it. Without a checkable result, the conclusion rests on the writer's say-so.
>
> *Which pile:* (c). The rule is ambiguous about whether an unquantified result counts as a checkable fact, and my reading is defensible.

**2.**
> *The post:* "Checked the entry lists. 41% of this year's field have never run the distance before, against 26% five years ago. That's why the finish-line photos look different, not because standards dropped."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The 41% vs. 26% figures are checkable and they are the reason given for the conclusion; without them the argument has nothing. I called it `hot_take` because the post ends with an opinion, but the staff definition says `analysis` "makes an argument," and an argument includes an opinion. I applied a stricter rule than the one written.
>
> *Which pile:* (a)

**3.**
> *The post:* "Ran the same loop in 4C and in 24C within a fortnight, same effort by heart rate. 90 seconds slower in the heat over six miles. People keep saying heat costs you 'a bit' and it's more than that."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The 90 seconds over six miles is a specific figure, and it is exactly what disproves "a bit." Rule 3 says a personal post is still `analysis` if a checkable fact carries the argument. I was put off by the opinion at the end, which rule 1 doesn't disqualify.
>
> *Which pile:* (a)

**4.**
> *The post:* "The 10K route was remeasured in 2021 and came out 60 metres long. Everyone comparing PBs from before and after that is comparing two different races, which is about 12 seconds at club pace."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. A date, a distance and a time cost (2021, 60 metres, about 12 seconds) lead directly to the conclusion. This is the clearest load-bearing fact of the five. I reacted to the sweeping "everyone comparing PBs" phrasing instead of checking whether the figures carried it.
>
> *Which pile:* (a)

**5.**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Both labels can be argued from the rules. The post does give a figure (three runners within 10 seconds over 5 miles), and the conclusion is built on it, which supports `analysis`. But three people on one day is an anecdote, and the staff rules never say whether evidence that small and uncontrolled can count as the fact that carries an argument. Rule 1 asks whether the fact is load-bearing, not whether it is strong enough to bear the load.
>
> *Which pile:* (b). The rules don't say how strong the evidence has to be.

**What the pattern in my disagreements tells me:**
All five disagreements went the same way: staff said `analysis`, I said `hot_take`. I agreed with staff on every `reaction` and every `hot_take` post. I was treating any opinion in a post as disqualifying, when the staff definition allows an opinion as long as a checkable figure carries it. Three of the five are pile (a), one is (b) and one is (c). This suggests my instinct is to under-call the evidence-based label, and that matters for my own `argued` labels too.

---

## The Improvement

**What I changed:** Training epochs from 3 to 10. Nothing else: same labels, same learning rate (2e-5), same batch size (16), same three seeds (42, 7, 2024). Device: mps (Apple Silicon GPU), torch 2.14.1.

**Which diagnosis pointed at it:** My diagnosis for criteria 1 and 2 was too little training. 3 epochs was about 24 update steps, validation accuracy stayed at 0.6 (always-`take`) on every epoch of every seed, and the confidence data showed the model had learned a weak signal that never got strong enough to predict `argued`. More epochs targets that directly. I chose this over relabelling because the model never predicted `argued` at all, which pointed at training more than at an inconsistent boundary.

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.808 | 0.885 | 0.808 | 0.077 |
| Macro F1 | 0.805 | 0.883 | 0.782 | 0.102 |
| F1 — `argued` | 0.783 | 0.870 | 0.706 | 0.164 |
| F1 — `take` | 0.828 | 0.897 | 0.857 | 0.069 |

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 | 0.808 | 0.885 | 0.808 | MET |
| 2. Per-label F1 | `take` ≥ 0.75 and `argued` ≥ 0.65 | 0.828 / 0.783 | 0.897 / 0.870 | 0.857 / 0.706 | MET |
| 3. No label above 65% of labels.csv | ≤ 65% | 61.7% | 61.7% | 61.7% | MET |
| 4. Agreement with staff labels | ≥ 85% | 83% | 83% | 83% | MISSED |
| 5. Confident predictions right 10+ points more often | gap ≥ 10 pts | 100% vs 62.5% | 100% vs 75% | 87.5% vs 75% | MET by proxy |

Criterion 5 note: my criterion splits at a top probability of 0.80, but the results file records accuracy by confidence thirds, not by that threshold. The most-confident third beat the least-confident third by 37.5, 25 and 12.5 points, and mean confidence when right rose from about 0.62 to 0.83. I'm reporting this as met by proxy, not as a direct measurement of the 0.80 split.

### Confusion matrix — After (seed 42)

| true \ predicted | argued | take |
|---|---|---|
| **argued** | 9 | 1 |
| **take** | 4 | 12 |

The direction flipped: the model now calls 4 real `take` posts `argued`, and only 1 real `argued` post `take`.

**Did it help, and how do I know:** Yes. Accuracy went from 0.615 on every seed to 0.808–0.885, and `argued` F1 went from 0.000 to 0.706–0.870. The model now beats the zero-shot baseline (0.654) on every seed, and validation accuracy rose above 0.6 during training instead of staying flat. Criteria 1, 2 and 5 moved from MISSED to MET (5 by proxy). Two caveats: `argued` F1 on seed 2024 (0.706) is only 5.6 points over its target with a 0.164 spread, so a different split could miss it; and on seed 2024 validation accuracy peaked around epoch 5 and then dipped while validation loss rose, which suggests mild overfitting by epoch 10. Criterion 4 is unchanged because retraining doesn't change my labels.

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
