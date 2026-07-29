# BUILD — Crack the Google Coding Interview (Video Production)

Source of truth for **video production scope + status**. Content comes from `problems/` + `scripts/`, the render engine from `video-pipeline/lib_dsa.py`, the rules from the `lld-video` / `webdev-video` skills. Syllabus master: [`GOOGLE_LEETCODE_Course_Udemy.md`](./GOOGLE_LEETCODE_Course_Udemy.md).

## Conventions

- **Deliverable per problem:** `video-pipeline/<slug>/GOOG_<slug>.mp4`.
- **Every lesson** obeys the retention rules (cold open, no static > 4 s, word-synced reveals, explainer-before-code, teacher-paced typing). See the `lld-video` skill.
- **Reusable visuals in `lib_dsa.py`:** `array_cells`, `pointer_arrow`, `window_band`, `linked_list`, `binary_tree`, `grid`, `stack_column`, `heap_triangle`, `dp_table` + the pen set.
- Target length: **10–14 min** per problem.

## Engine status

| Piece | Status |
|---|---|
| `lib_dsa.py` (theme, motion, primitives, pen set) | ✅ ported from Amazon course |
| `gen_audio` + `scenes_all` + `qa_check` pattern | ⏳ reuse per-lesson |

## Status legend
`⬜ not started` · `📝 write-up + script ready` · `🎙️ audio` · `🎬 scenes` · `🟩 rendered` · `✅ QA-passed`

> **Where we are:** the 50 problem write-ups (`problems/`) and recording scripts (`scripts/`) are being authored section by section (4 reused from the Amazon course: Text Justification, Longest Increasing Path, Meeting Rooms II, Logger Rate Limiter). Video rendering is the next phase, in syllabus order. `📝` = write-up + script ready; `⬜` = video not yet rendered.

---

## Section 1 — Strings & Parsing

| LC | Problem | Status |
|----|---------|--------|
| 68 | Text Justification | 📝 (reference lesson) |
| 418 | Sentence Screen Fitting | 📝 |
| 833 | Find And Replace in String | 📝 |
| 777 | Swap Adjacent in LR String | 📝 |
| 1554 | Strings Differ by One Character | 📝 |
| 792 | Number of Matching Subsequences | 📝 |
| 2135 | Count Words Obtained After Adding a Letter | 📝 |
| 539 | Minimum Time Difference | 📝 |
| 1055 | Shortest Way to Form String | 📝 |
| 2018 | Check if Word Can Be Placed In Crossword | 📝 |

## Section 2 — Tries

| LC | Problem | Status |
|----|---------|--------|
| 2416 | Sum of Prefix Scores of Strings | 📝 |

## Section 3 — Graphs & Grids

| LC | Problem | Status |
|----|---------|--------|
| 1293 | Shortest Path in a Grid with Obstacles Elimination | 📝 |
| 778 | Swim in Rising Water | 📝 |
| 2101 | Detonate the Maximum Bombs | 📝 |
| 419 | Battleships in a Board | 📝 |
| 562 | Longest Line of Consecutive One in Matrix | 📝 |
| 2128 | Remove All Ones With Row and Column Flips | 📝 |
| 329 | Longest Increasing Path in a Matrix | 📝 |
| 2242 | Maximum Score of a Node Sequence | 📝 |

## Section 4 — Union-Find

| LC | Problem | Status |
|----|---------|--------|
| 1101 | The Earliest Moment When Everyone Become Friends | 📝 |
| 839 | Similar String Groups | 📝 |
| 2421 | Number of Good Paths | 📝 |

## Section 5 — Topological Sort

| LC | Problem | Status |
|----|---------|--------|
| 2115 | Find All Possible Recipes from Given Supplies | 📝 |

## Section 6 — Trees

| LC | Problem | Status |
|----|---------|--------|
| 2096 | Step-By-Step Directions From a Binary Tree Node to Another | 📝 |
| 366 | Find Leaves of Binary Tree | 📝 |

## Section 7 — Heaps, Intervals & Scheduling

| LC | Problem | Status |
|----|---------|--------|
| 253 | Meeting Rooms II | 📝 |
| 2402 | Meeting Rooms III | 📝 |
| 1606 | Find Servers That Handled Most Number of Requests | 📝 |
| 729 | My Calendar I | 📝 |
| 2158 | Amount of New Area Painted Each Day | 📝 |
| 1996 | The Number of Weak Characters in the Game | 📝 |
| 715 | Range Module | 📝 |

## Section 8 — Design (Implement-a-Class)

| LC | Problem | Status |
|----|---------|--------|
| 528 | Random Pick with Weight | 📝 |
| 900 | RLE Iterator | 📝 |
| 1146 | Snapshot Array | 📝 |
| 2013 | Detect Squares | 📝 |
| 2034 | Stock Price Fluctuation | 📝 |
| 359 | Logger Rate Limiter | 📝 |
| 2162 | Minimum Cost to Set Cooking Time | 📝 |

## Section 9 — Dynamic Programming

| LC | Problem | Status |
|----|---------|--------|
| 1937 | Maximum Number of Points with Cost | 📝 |
| 552 | Student Attendance Record II | 📝 |
| 1105 | Filling Bookcase Shelves | 📝 |
| 818 | Race Car | 📝 |
| 1048 | Longest String Chain | 📝 |
| 1387 | Sort Integers by The Power Value | 📝 |
| 2172 | Maximum AND Sum of Array | 📝 |

## Section 10 — Backtracking & Interactive

| LC | Problem | Status |
|----|---------|--------|
| 489 | Robot Room Cleaner | 📝 |
| 843 | Guess the Word | 📝 |

## Section 11 — Geometry & Math

| LC | Problem | Status |
|----|---------|--------|
| 1610 | Maximum Number of Visible Points | 📝 |
| 2178 | Maximum Split of Positive Even Integers | 📝 |

---

## Current build target

**▶ Section 1 — Strings & Parsing**, starting with **Text Justification (68)** as the reference lesson. Per lesson: finalize script → gen audio → scenes → render → QA loop.

## Build order

Ship **in syllabus order**, one section at a time. The engine (`lib_dsa.py`) is ready; render Section 1 first (it reuses `array_cells` + the pen set), then onward.
