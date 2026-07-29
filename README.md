# Crack the Google Coding Interview — Course Workspace

A Udemy-style course built around **one curated list of 50 real Google-tagged LeetCode problems** — the harder, stranger, often Google-premium questions generic courses skip — each taught **intuition-first** and mapped to the reusable **pattern** underneath it.

This repo is the **production workspace** for the course: the syllabus, the per-problem solution write-ups, the recording scripts, the downloadable resources, and the video render engine. It mirrors the structure of the sibling `aamzon-dsa-udemy` and `LLD-Udemy` course repos.

> 📚 **Start here:** [`GOOGLE_LEETCODE_Course_Udemy.md`](./GOOGLE_LEETCODE_Course_Udemy.md) — the full 50-problem syllabus, grouped into 11 pattern sections.

---

## What's in this repo

| Path | What it holds |
|------|---------------|
| `GOOGLE_LEETCODE_Course_Udemy.md` | **The master syllabus.** 50 problems in 11 pattern sections, lesson template, writing rules. |
| `BUILD.md` | **Video production tracker.** Per-lesson status from script → audio → scenes → render → QA. |
| `problems/` | **Per-question solution files** — 50 problems, grouped by pattern, each with intuition → brute force → optimised → space optimization → Java → complexity → narration. See [`problems/README.md`](./problems/README.md). |
| `scripts/` | **Per-question recording scripts** — 50 retention-optimized, two-voice (TEACHER + LEARNER) teaching scripts. See [`scripts/README.md`](./scripts/README.md). |
| `resources/` | Downloadable cheat sheets (pattern selector, Big-O, 6-step framework, Googleyness/GCA, the Google-50 checklist). |
| `video-pipeline/` | The shared `lib_dsa.py` render engine + per-lesson Python video folders, built lesson-by-lesson. |

---

## Why a fixed list of 50 (not 300)?

Google rarely asks a problem you've memorized — and this list leans into the *specific* Google-flavored questions (Robot Room Cleaner, Guess the Word, Race Car, Meeting Rooms III, Text Justification…). But the point isn't to memorize 50 answers. Google scores **General Cognitive Ability (GCA)** — *how you reason out loud on a problem you've never seen*. So every problem is taught the same way:

```
🧠 INTUITION → ① BRUTE FORCE (why it times out)
            → ② OPTIMISED (the pattern applied)
            → ③ SPACE OPTIMIZATION (or "already optimal — here's why")
→ COMPLEXITY OUT LOUD → ACTIVE RECALL → 3 TAKEAWAYS
```

Learn the pattern once, and the next unseen problem becomes "oh — it's *that* shape."

---

## The 11 pattern sections

1. **Strings & Parsing** (10) · 2. **Tries** (1) · 3. **Graphs & Grids** (8) · 4. **Union-Find** (3) · 5. **Topological Sort** (1) · 6. **Trees** (2) · 7. **Heaps, Intervals & Scheduling** (7) · 8. **Design / Implement-a-Class** (7) · 9. **Dynamic Programming** (7) · 10. **Backtracking & Interactive** (2) · 11. **Geometry & Math** (2).

---

## Google-specific framing

- **Behavioral is scored on Google's four attributes** — GCA, Role-Related Knowledge (RRK), Leadership, and *Googleyness* — see [`resources/Googleyness_and_Leadership.md`](./resources/Googleyness_and_Leadership.md).
- **GCA runs through every lesson** — Google scores *how you approach* a novel problem, so we drill narrating the approach and asking clarifying questions.
- **The list is real** — several problems are LeetCode Premium (marked 🔒 in the checklist), the kind that actually surface in Google loops.

---

## How to build a lesson (the production loop)

Mirrors the `aamzon-dsa-udemy` / `LLD-Udemy` pipeline:

1. **Write-up** — the intuition-first solution in `problems/`.
2. **Script** — the retention-optimized recording script in `scripts/`.
3. **Video** — build `video-pipeline/lNN/`: `gen_audio` → `scenes_all` → render → `qa_check`, using `video-pipeline/lib_dsa.py`.
4. **Track** — update the lesson's row in `BUILD.md`.

---

## Status

🚧 **Content in progress.** Syllabus, cheat sheets, and the 11-section structure are in place; the `problems/` and `scripts/` libraries are being authored problem-by-problem (the 4 problems shared with the Amazon course — Text Justification, Longest Increasing Path, Meeting Rooms II, Logger Rate Limiter — are reused). See `BUILD.md` for the live board.

---

## Audience & scope

- **For:** engineers targeting Google L3 / L4 who want the *actual* Google list, not a generic top-75.
- **Examples in:** Python (primary) + Java (secondary).
- **Prereqs:** one language, basic data structures. Several problems assume LeetCode Premium.
