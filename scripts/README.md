# Recording Scripts — Retention-Optimized, Two-Voice

96 video recording scripts, one per problem, mirroring `problems/`. Each is a **spoken teaching script** engineered for retention, following [`_SCRIPT_TEMPLATE.md`](./_SCRIPT_TEMPLATE.md).

**Every script:**
- Runs the **14-beat structure** — cold-open hook → concrete tiny example → **hand dry-run** to build intuition → predict-first pause → the aha → **live chunked coding** → **why-focused code explanation** → code dry-run → complexity → space → active recall → memory peg → cliffhanger.
- Uses the **hybrid two-voice** format: a **TEACHER** through-line (~85%) plus a **LEARNER** (smart peer) who interjects 3–5 times at the highest-value moments (predict beats, sharp code objections, common misconceptions).
- Has a matched **[VISUAL: …]** cue on every beat for the video editor, chunked Python, and a Java appendix.

**Grounded in learning science:** curiosity gaps (Zeigarnik), the generation effect (predict-first), worked examples, dual coding, cognitive-load management, vicarious learning (the two-voice dialogue), and retrieval practice. See the template for the full principle-to-beat mapping.

**Total:** 96 scripts · ~**22 hours** of video at ~14 min average. Audience: college students + working IT professionals.

The gold-standard exemplar is [`02-two-pointers/3sum.md`](./02-two-pointers/3sum.md). The foundational first lesson is [`02-two-pointers/pair-with-target-sum.md`](./02-two-pointers/pair-with-target-sum.md).

---

## Index (mirrors `problems/`)

- **02 · Two Pointers** — pair-with-target-sum · valid-palindrome · remove-duplicates-sorted-array · 3sum · container-with-most-water · sort-colors
- **03 · Sliding Window** — maximum-average-subarray · minimum-size-subarray-sum · longest-substring-without-repeating · longest-repeating-character-replacement · permutation-in-string · minimum-window-substring
- **04 · Fast & Slow Pointers** — linked-list-cycle · linked-list-cycle-ii · middle-of-linked-list · happy-number
- **05 · Linked-List Reversal** — reverse-linked-list · reverse-linked-list-ii · reverse-nodes-in-k-group · reorder-list
- **06 · Stacks** — valid-parentheses · min-stack · next-greater-element · daily-temperatures · largest-rectangle-histogram
- **07 · Binary Search** — binary-search · search-rotated-sorted-array · first-bad-version · search-2d-matrix · koko-eating-bananas · median-of-two-sorted-arrays
- **08 · Trees BFS** — level-order-traversal · zigzag-level-order · right-side-view · minimum-depth · populating-next-right-pointers
- **09 · Trees DFS** — maximum-depth · path-sum · binary-tree-paths · diameter-of-binary-tree · validate-bst · lowest-common-ancestor
- **10 · Graphs** — number-of-islands · rotting-oranges · flood-fill · clone-graph · 01-matrix · word-ladder
- **11 · Topological Sort** — course-schedule · course-schedule-ii · alien-dictionary · minimum-height-trees
- **12 · Heaps & Top-K** — kth-largest-element · top-k-frequent-elements · k-closest-points · merge-k-sorted-lists · find-median-from-data-stream · task-scheduler
- **13 · Backtracking** — subsets · permutations · combination-sum · letter-combinations · word-search · generate-parentheses · n-queens
- **14 · Dynamic Programming** — climbing-stairs · house-robber · coin-change · longest-increasing-subsequence · partition-equal-subset-sum · longest-common-subsequence · edit-distance · unique-paths · word-break · best-time-to-buy-sell-stock
- **15 · Greedy & Intervals** — merge-intervals · insert-interval · non-overlapping-intervals · meeting-rooms-ii · jump-game
- **16 · Tries & Union-Find** — implement-trie · word-search-ii · number-of-provinces · redundant-connection · accounts-merge
- **17 · Design** — lru-cache · lfu-cache · design-hashmap · insert-delete-getrandom · logger-rate-limiter
- **18 · Google Rapid-Fire** — two-sum · group-anagrams · product-except-self · copy-list-random-pointer · max-area-of-island · trapping-rain-water

---

## From script → video (the production loop)

Each script feeds the pipeline in `BUILD.md`: script (here) → record/generate audio → build scenes from the `[VISUAL: …]` cues → render → QA. The `[VISUAL: …]` markers are the storyboard.
