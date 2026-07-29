# Recording Scripts — Retention-Optimized, Two-Voice

50 video recording scripts, one per problem, mirroring `problems/`. Each is a **spoken teaching script** engineered for retention, following [`_SCRIPT_TEMPLATE.md`](./_SCRIPT_TEMPLATE.md).

**Every script:**
- Runs the **14-beat structure** — cold-open hook → concrete tiny example → **hand dry-run** → predict-first pause → the aha → **live chunked coding** → **why-focused code explanation** → code dry-run → complexity → space → active recall → memory peg → cliffhanger.
- Uses the **hybrid two-voice** format: a **TEACHER** through-line (~85%) plus a **LEARNER** (smart peer) who interjects 3–5 times at the highest-value moments.
- Has a matched **[VISUAL: …]** cue on every beat, chunked Python, and a Java appendix.
- Weaves in a reminder that Google scores **GCA** — narrating the approach and asking clarifying questions is half the rubric.

The gold-standard exemplar is [`03-graphs-grids/longest-increasing-path-in-matrix.md`](./03-graphs-grids/longest-increasing-path-in-matrix.md).

---

## Index (mirrors `problems/`)

- **1 · Strings & Parsing** — text-justification · sentence-screen-fitting · find-and-replace-in-string · swap-adjacent-in-lr-string · strings-differ-by-one-character · number-of-matching-subsequences · count-words-after-adding-a-letter · minimum-time-difference · shortest-way-to-form-string · check-if-word-can-be-placed-in-crossword
- **2 · Tries** — sum-of-prefix-scores-of-strings
- **3 · Graphs & Grids** — shortest-path-in-grid-with-obstacles-elimination · swim-in-rising-water · detonate-the-maximum-bombs · battleships-in-a-board · longest-line-of-consecutive-one-in-matrix · remove-all-ones-with-row-and-column-flips · longest-increasing-path-in-matrix · maximum-score-of-a-node-sequence
- **4 · Union-Find** — earliest-moment-when-everyone-become-friends · similar-string-groups · number-of-good-paths
- **5 · Topological Sort** — find-all-possible-recipes-from-given-supplies
- **6 · Trees** — step-by-step-directions-in-binary-tree · find-leaves-of-binary-tree
- **7 · Heaps, Intervals & Scheduling** — meeting-rooms-ii · meeting-rooms-iii · find-servers-that-handled-most-requests · my-calendar-i · amount-of-new-area-painted-each-day · number-of-weak-characters-in-the-game · range-module
- **8 · Design** — random-pick-with-weight · rle-iterator · snapshot-array · detect-squares · stock-price-fluctuation · logger-rate-limiter · minimum-cost-to-set-cooking-time
- **9 · Dynamic Programming** — maximum-number-of-points-with-cost · student-attendance-record-ii · filling-bookcase-shelves · race-car · longest-string-chain · sort-integers-by-the-power-value · maximum-and-sum-of-array
- **10 · Backtracking & Interactive** — robot-room-cleaner · guess-the-word
- **11 · Geometry & Math** — maximum-number-of-visible-points · maximum-split-of-positive-even-integers

**Total:** 50 scripts. Audience: college students + working IT professionals prepping for Google.

---

## From script → video (the production loop)

Each script feeds the pipeline in `BUILD.md`: script (here) → record/generate audio → build scenes from the `[VISUAL: …]` cues → render → QA. The `[VISUAL: …]` markers are the storyboard.
