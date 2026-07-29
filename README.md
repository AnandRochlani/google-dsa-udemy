# Crack the Google Coding Interview — Course Workspace

A Udemy-style course that teaches you to pass the **Google coding interview** by mastering **15 reusable LeetCode patterns** instead of grinding 300 random problems.

This repo is the **production workspace** for the course: the syllabus, the lesson scripts, the downloadable resources, and (eventually) the rendered videos. It mirrors the structure of the sibling `aamzon-dsa-udemy` and `LLD-Udemy` course repos.

> 📚 **Start here:** [`GOOGLE_LEETCODE_Course_Udemy.md`](./GOOGLE_LEETCODE_Course_Udemy.md) — the full 117-lesson syllabus.

---

## What's in this repo

| Path | What it holds |
|------|---------------|
| `GOOGLE_LEETCODE_Course_Udemy.md` | **The master syllabus.** 20 sections, 117 lessons, 15 patterns, 4 mock interviews, lesson template, writing rules. |
| `BUILD.md` | **Video production tracker.** Per-lesson status from script → audio → scenes → render → QA. |
| `problems/` | **Per-question solution files** — grouped by pattern, each with intuition → brute force → optimised → space optimization. See [`problems/README.md`](./problems/README.md). |
| `scripts/` | **Per-question video recording scripts** — retention-optimized, two-voice (TEACHER + LEARNER) teaching scripts. See [`scripts/README.md`](./scripts/README.md). |
| `sessions/` | **Lesson scripts** — the full teaching script for each lesson (`LNN_Title.md`), following the lesson template. |
| `resources/` | Downloadable cheat sheets students get (pattern selector, Big-O, framework, Googleyness/GCA, top-50 list). |
| `video-pipeline/` | Per-lesson Python video-generation folders (`lNN/`) + the shared `lib_dsa.py` render engine, built lesson-by-lesson. |

---

## The teaching idea

Google rarely asks a problem you've memorized. They ask a *new* problem that maps to a pattern you know — and they score **how you think** (General Cognitive Ability), not just whether you land the answer. So the whole course is organized around **recognition + narration**:

1. **See the signal** — "sorted array + find a pair" → Two Pointers. "longest substring with a constraint" → Sliding Window.
2. **Recall the template** — each pattern has one reusable skeleton.
3. **Adapt and narrate** — code it while talking, the way the interviewer scores you on the rubric.

Every problem lesson runs the same beats:

```
HOOK → STORY/ANALOGY → THE PATTERN → QUICK CHECK
  → ① BRUTE FORCE (why it times out)
  → ② OPTIMISED SOLUTION (the pattern applied)
  → ③ SPACE OPTIMIZATION (in-place / rolling vars — or "already optimal, here's why")
  → COMPLEXITY OUT LOUD → ACTIVE RECALL → 3 TAKEAWAYS → CLIFFHANGER
```

Every problem is dissected in **three explicit layers — brute force → optimised → space optimization** — so students learn to *improve* a solution, not memorize the final one.

---

## The 15 patterns

Two Pointers · Sliding Window · Fast & Slow Pointers · In-Place Linked-List Reversal · Stacks (incl. Monotonic) · Modified Binary Search · Tree BFS · Tree DFS · Graph BFS/DFS (grids & nodes) · Topological Sort · Heaps & Top-K · Subsets & Backtracking · Dynamic Programming · Greedy & Intervals · Tries & Union-Find.

Plus three Google-specific blocks: **design problems** (LRU/LFU cache, O(1) structures), **most-asked rapid-fire** (Two Sum, Number of Islands, Trapping Rain Water, …), and **Google signature problems** (Text Justification, Decode String, Longest Increasing Path in a Matrix, Time-Based Key-Value Store, …).

---

## Google vs. Amazon — what's different here

This course shares the 15-pattern spine with the sibling Amazon course (the patterns transfer to any FAANG loop), but it's tuned for the Google loop:

- **Behavioral is scored on Google's four attributes** — General Cognitive Ability (GCA), Role-Related Knowledge (RRK), Leadership, and *Googleyness* — not Amazon's Leadership Principles. See [`resources/Googleyness_and_Leadership.md`](./resources/Googleyness_and_Leadership.md).
- **GCA framing throughout** — Google scores *how you approach* a novel problem. Every lesson reinforces narrating the approach, not just typing the answer.
- **A dedicated Google Signature Problems section** — the string-parsing, grid-memoization, and prefix-sum problems Google is famous for.
- **The loop itself** — phone screen → onsite (4–5 rounds) → hiring committee → team match, instead of Amazon's bar-raiser + Leadership Principles model.

---

## How to build a lesson (the production loop)

Mirrors the `aamzon-dsa-udemy` / `LLD-Udemy` pipeline:

1. **Script** — write `sessions/LNN_Title.md` from the syllabus row (use the lesson template).
2. **Recording script** — the retention-optimized version in `scripts/`.
3. **Video** — build `video-pipeline/lNN/`: `gen_audio` → `scenes_all` → render → `qa_check`, using the shared `video-pipeline/lib_dsa.py` engine.
4. **Track** — update the lesson's row in `BUILD.md`.

Target length per lesson: **8–15 min** (patterns short, hard problems and mocks longer).

---

## Status

🚧 **Content foundation laid.** Syllabus complete; all five cheat sheets written; the full per-pattern `problems/` and `scripts/` libraries in place; the `lib_dsa.py` render engine ported from the Amazon course. Videos are produced section-by-section, in syllabus order, starting with Section 0 → Section 2 (Two Pointers). See `BUILD.md` for the live board.

---

## Audience & scope

- **For:** engineers targeting Google L3 / L4 (the patterns transfer to any FAANG-tier loop).
- **Examples in:** Python (primary, for readability) + Java (secondary, for Java interviewers).
- **Prereqs:** one language, basic data structures. No CS degree, no heavy math.
