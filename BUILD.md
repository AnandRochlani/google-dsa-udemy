# BUILD — Crack the Google Coding Interview (Video Production)

Source of truth for **content + video production status**. Content comes from `problems/` + `scripts/`, the render engine from `video-pipeline/lib_dsa.py`. Syllabus master: [`GOOGLE_LEETCODE_Course_Udemy.md`](./GOOGLE_LEETCODE_Course_Udemy.md).

## 📊 Progress at a glance

| Layer | Done | Total |
|---|---|---|
| **Problem write-ups** (`problems/`) | **50** | 50 |
| **Recording scripts** (`scripts/`) | **50** | 50 |
| **Videos rendered** | 0 | 50 |

> ✅ **Authoring is complete.** All 50 problems have a write-up *and* a matching recording script, across all 11 sections. Verified: 50 files in `problems/`, 50 in `scripts/`, one-to-one by filename with zero orphans on either side; every write-up carries all required template sections; every script carries ≥14 `[VISUAL: …]` cues and the two-voice format.
>
> **Next phase is video production** — nothing has been rendered yet. See "What's left" at the bottom.

## Status legend
`✅ write-up + script done` · `📝 write-up done · script pending` · `⬜ not started` — then video stages: `🎙️ audio · 🎬 scenes · 🟩 rendered · ✅QA`

## Engine status
`lib_dsa.py` (theme, motion, primitives, pen set) — ✅ ported from Amazon course. Reference scene: `video-pipeline/l08/scenes_l08.py`.

---

## Section 1 — Strings & Parsing  ✅ **complete (10/10 write-up + script)**

| LC | Problem | Status |
|----|---------|--------|
| 68 | Text Justification *(reference lesson)* | ✅ |
| 418 | Sentence Screen Fitting | ✅ |
| 833 | Find And Replace in String | ✅ |
| 777 | Swap Adjacent in LR String | ✅ |
| 1554 | Strings Differ by One Character | ✅ |
| 792 | Number of Matching Subsequences | ✅ |
| 2135 | Count Words Obtained After Adding a Letter | ✅ |
| 539 | Minimum Time Difference | ✅ |
| 1055 | Shortest Way to Form String | ✅ |
| 2018 | Check if Word Can Be Placed In Crossword | ✅ |

## Section 2 — Tries  ✅ **complete (1/1)**

| LC | Problem | Status |
|----|---------|--------|
| 2416 | Sum of Prefix Scores of Strings | ✅ |

## Section 3 — Graphs & Grids  ✅ **complete (8/8)**

| LC | Problem | Status |
|----|---------|--------|
| 1293 | Shortest Path in a Grid with Obstacles Elimination | ✅ |
| 778 | Swim in Rising Water | ✅ |
| 2101 | Detonate the Maximum Bombs | ✅ |
| 419 | Battleships in a Board | ✅ |
| 562 | Longest Line of Consecutive One in Matrix | ✅ |
| 2128 | Remove All Ones With Row and Column Flips | ✅ |
| 329 | Longest Increasing Path in a Matrix | ✅ |
| 2242 | Maximum Score of a Node Sequence | ✅ |

## Section 4 — Union-Find  ✅ **complete (3/3)**

| LC | Problem | Status |
|----|---------|--------|
| 1101 | The Earliest Moment When Everyone Become Friends | ✅ |
| 839 | Similar String Groups | ✅ |
| 2421 | Number of Good Paths | ✅ |

## Section 5 — Topological Sort  ✅ **complete (1/1)**

| LC | Problem | Status |
|----|---------|--------|
| 2115 | Find All Possible Recipes from Given Supplies | ✅ |

## Section 6 — Trees  ✅ **complete (2/2)**

| LC | Problem | Status |
|----|---------|--------|
| 2096 | Step-By-Step Directions From a Binary Tree Node to Another | ✅ |
| 366 | Find Leaves of Binary Tree | ✅ |

## Section 7 — Heaps, Intervals & Scheduling  ✅ **complete (7/7)**

| LC | Problem | Status |
|----|---------|--------|
| 253 | Meeting Rooms II | ✅ |
| 2402 | Meeting Rooms III | ✅ |
| 1606 | Find Servers That Handled Most Number of Requests | ✅ |
| 729 | My Calendar I | ✅ |
| 2158 | Amount of New Area Painted Each Day | ✅ |
| 1996 | The Number of Weak Characters in the Game | ✅ |
| 715 | Range Module | ✅ |

## Section 8 — Design (Implement-a-Class)  ✅ **complete (7/7)**

| LC | Problem | Status |
|----|---------|--------|
| 528 | Random Pick with Weight | ✅ |
| 900 | RLE Iterator | ✅ |
| 1146 | Snapshot Array | ✅ |
| 2013 | Detect Squares | ✅ |
| 2034 | Stock Price Fluctuation | ✅ |
| 359 | Logger Rate Limiter | ✅ |
| 2162 | Minimum Cost to Set Cooking Time | ✅ |

## Section 9 — Dynamic Programming  ✅ **complete (7/7)**

| LC | Problem | Status |
|----|---------|--------|
| 1937 | Maximum Number of Points with Cost | ✅ |
| 552 | Student Attendance Record II | ✅ |
| 1105 | Filling Bookcase Shelves | ✅ |
| 818 | Race Car | ✅ |
| 1048 | Longest String Chain | ✅ |
| 1387 | Sort Integers by The Power Value | ✅ |
| 2172 | Maximum AND Sum of Array | ✅ |

## Section 10 — Backtracking & Interactive  ✅ **complete (2/2)**

| LC | Problem | Status |
|----|---------|--------|
| 489 | Robot Room Cleaner | ✅ |
| 843 | Guess the Word | ✅ |

## Section 11 — Geometry & Math  ✅ **complete (2/2)**

| LC | Problem | Status |
|----|---------|--------|
| 1610 | Maximum Number of Visible Points | ✅ |
| 2178 | Maximum Split of Positive Even Integers | ✅ |

---

## ⏭️ What's left

Authoring is done. Everything remaining is **video production** — 0 of 50 rendered.

1. **Render the 50 lessons in syllabus order**, starting with Section 1 / Text Justification. Per lesson: build `video-pipeline/lNN/` → `gen_audio` → `scenes_all` (storyboarded from the script's `[VISUAL: …]` cues) → render → `qa_check`.
2. **Decide what happens to `sessions/`.** It holds three lessons that are not part of the 50: `L00_Course_Overview` and `L02_Six_Step_Framework` (Section 0 orientation — not in the syllabus), and `L08_Two_Pointers_Pair_Sum` (carryover from the Amazon course; Two Sum II is not on the Google list). Either promote the two orientation lessons into the syllabus as a Section 0, or drop all three. `video-pipeline/l08/scenes_l08.py` belongs to that carryover lesson and is currently the engine's only reference scene.
3. **Optional polish:** `scripts/07-heaps-intervals/meeting-rooms-ii.md` and `scripts/08-design/logger-rate-limiter.md` each carry only 2 LEARNER interjections against the template's 3–5. Both are reused Amazon-course lessons; a short pass would bring them in line.

### Authoring QA — how the 50 were verified

Content was authored in waves of parallel agents, the last wave completing Sections 7–11. Verification actually run against the finished files (not assumed):

- 50 write-ups ↔ 50 scripts, matched one-to-one by filename, zero orphans in either direction.
- Every write-up contains all required template sections (Problem, Intuition, ① Brute Force, ② Optimised, ③ Space, Java, Complexity Summary).
- Every script carries ≥14 `[VISUAL: …]` cues, 3–5 LEARNER interjections, and ≥2 pause-and-predict beats (two pre-existing exceptions noted above).
- For the final wave, every Python and Java block was **extracted from the shipped markdown and executed**, cross-checked against brute force on randomized inputs, and the chunked live-coding blocks were concatenated in narration order to confirm they assemble into a working solution.
- All index links in `problems/README.md` and `scripts/README.md` resolve.
