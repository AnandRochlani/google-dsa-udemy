# BUILD — Crack the Google Coding Interview (Video Production)

Source of truth for **video production scope + status**. Content comes from `problems/` + `scripts/` + `sessions/`, the render engine from `video-pipeline/lib_dsa.py` (ported from the Amazon course), the rules from the `lld-video` / `webdev-video` skills. Syllabus master: [`GOOGLE_LEETCODE_Course_Udemy.md`](./GOOGLE_LEETCODE_Course_Udemy.md).

## Conventions

- **Lesson id:** `LNN` (e.g. `L08`). Pipeline dir: `video-pipeline/l<nn>/`. Deliverable: `video-pipeline/l<nn>/GOOG_L<nn>.mp4`.
- **Every lesson** obeys the retention rules (cold open on content, no static > 4 s, word-synced reveals, explainer-before-code, teacher-paced typing). See the `lld-video` skill.
- **Coding lessons** use the dark IDE beat (Python primary, Java secondary). Conceptual lessons use light diagram primitives (array cells, pointers, trees, grids).
- **Reusable visuals in `lib_dsa.py`:** `array_cells` (with two moving pointer arrows), `sliding_window` band, `linked_list` node chain, `binary_tree`, `grid` (for islands/BFS), `stack_column`, `heap_triangle`, `dp_table`.
- Target length: **8–15 min** per lesson.

## Engine status

| Piece | Status |
|---|---|
| `lib_dsa.py` (base: theme, motion, WordClock, `array_cells`, `pointer_arrow`, pen set) | ✅ **ported from Amazon course** |
| `lib_dsa` DSA toolkit (`window_band`, `linked_list`, `binary_tree`, `grid`, `stack_column`, `heap_triangle`, `dp_table`) | ✅ available (ported) |
| `gen_audio` + `scenes_all` + `qa_check` pattern | ⏳ reuse per-lesson (see `l08/scenes_l08.py` reference) |

## Status legend
`⬜ not started` · `📝 script written` · `🎙️ audio` · `🎬 scenes` · `🟩 rendered` · `✅ QA-passed`

> **Where we are:** all 96 problem write-ups (`problems/`) and recording scripts (`scripts/`) are written, and the render engine is ported. Videos are produced **in syllabus order**, one section at a time, starting with L08. Below, `📝` = script + problem write-up ready; `⬜` = video not yet rendered.

---

## Section 0 — Orientation *(conceptual; base engine only)*

| id | Title | Status | Notes |
|---|---|---|---|
| L00 | What You'll Master + How to Use This Course | 📝 script | `sessions/L00_Course_Overview.md` written. Theory-only, ~5 min. |
| L01 | Inside the Google Loop | ⬜ | Phone screen → onsite → hiring committee → team match. Timeline diagram. |
| L02 | Think-Out-Loud — The 6-Step Framework | 📝 script | `sessions/L02_Six_Step_Framework.md` written. The narration spine (and GCA signal) for every later lesson. |

## Section 1 — Complexity & The Toolbox

| id | Title | Status | Notes |
|---|---|---|---|
| L03 | Big-O in Plain English | ⬜ | Growth-curve animation; O(n²) vs O(n) race. |
| L04 | The Hash Map | ⬜ | Buckets animation; the "seen" set trick. |
| L05 | Arrays & Strings | ⬜ | In-place, index math, off-by-one. |
| L06 | Stacks & Queues | ⬜ | LIFO/FIFO columns. |
| L07 | Recursion & The Call Stack | ⬜ | Stack-frames visual. |

## Section 2 — Two Pointers  📝 **scripts ready — current build target**

Engine: `lib_dsa.py` (native 1080p). Reference scene: `video-pipeline/l08/scenes_l08.py`.

| id | Title | Status | Notes |
|---|---|---|---|
| L08 | The Two-Pointer Idea — Pair with Target Sum | 📝 **script + reference scene** | Reference lesson every other pattern lesson is cloned from. `scenes_l08.py`. |
| L09 | Valid Palindrome | 📝 script | Both-ends squeeze, char cells. |
| L10 | Remove Duplicates In-Place | 📝 script | Slow/fast write pointer. |
| L11 | 3Sum | 📝 script | Sort + fix-one + two-pointer. |
| L12 | Container With Most Water | 📝 script | Bar chart + water shading, move shorter wall. |
| L13 | Sort Colors (Dutch flag) | 📝 script | Three pointers, color regions. |

## Section 3 — Sliding Window  📝

| id | Title | Status |
|---|---|---|
| L14 | Maximum Average Subarray (fixed window) | 📝 script |
| L15 | Minimum Size Subarray Sum (dynamic window) | 📝 script |
| L16 | Longest Substring Without Repeating | 📝 script |
| L17 | Longest Repeating Character Replacement | 📝 script |
| L18 | Permutation in String | 📝 script |
| L19 | Minimum Window Substring (hard) | 📝 script |

## Section 4 — Fast & Slow Pointers  📝

| id | Title | Status |
|---|---|---|
| L21 | Linked List Cycle | 📝 script |
| L22 | Linked List Cycle II (find start) | 📝 script |
| L23 | Middle of the Linked List | 📝 script |
| L24 | Happy Number | 📝 script |

## Section 5 — Linked-List In-Place Reversal  📝

| id | Title | Status |
|---|---|---|
| L25 | Reverse Linked List | 📝 script |
| L26 | Reverse Linked List II (sublist) | 📝 script |
| L27 | Reverse Nodes in k-Group (hard) | 📝 script |
| L28 | Reorder List (middle + reverse + merge) | 📝 script |

## Section 6 — Stacks  📝

| id | Title | Status |
|---|---|---|
| L29 | Valid Parentheses | 📝 script |
| L30 | Min Stack (O(1) getMin) | 📝 script |
| L31 | Next Greater Element (monotonic) | 📝 script |
| L32 | Daily Temperatures (monotonic) | 📝 script |
| L33 | Largest Rectangle in Histogram (hard) | 📝 script |

## Section 7 — Modified Binary Search  📝

| id | Title | Status |
|---|---|---|
| L34 | Binary Search (template) | 📝 script |
| L35 | Search in Rotated Sorted Array | 📝 script |
| L36 | First Bad Version (boundary) | 📝 script |
| L37 | Search a 2D Matrix | 📝 script |
| L38 | Koko Eating Bananas (search the answer) | 📝 script |
| L39 | Median of Two Sorted Arrays (hard, partition) | 📝 script |

## Section 8 — Trees: BFS  📝

| id | Title | Status |
|---|---|---|
| L40 | Level Order Traversal | 📝 script |
| L41 | Zigzag Level Order | 📝 script |
| L42 | Right Side View | 📝 script |
| L43 | Minimum Depth | 📝 script |
| L44 | Populating Next Right Pointers | 📝 script |

## Section 9 — Trees: DFS  📝

| id | Title | Status |
|---|---|---|
| L45 | Maximum Depth | 📝 script |
| L46 | Path Sum | 📝 script |
| L47 | Binary Tree Paths (all root-to-leaf) | 📝 script |
| L48 | Diameter of Binary Tree | 📝 script |
| L49 | Validate BST | 📝 script |
| L50 | Lowest Common Ancestor | 📝 script |

## Section 10 — Graphs (grids & nodes)  📝

| id | Title | Status |
|---|---|---|
| L51 | Number of Islands | 📝 script |
| L52 | Rotting Oranges (multi-source BFS) | 📝 script |
| L53 | Flood Fill | 📝 script |
| L54 | Clone Graph | 📝 script |
| L55 | 01 Matrix (multi-source BFS) | 📝 script |
| L56 | Word Ladder (hard, BFS word graph) | 📝 script |

## Section 11 — Topological Sort  📝

| id | Title | Status |
|---|---|---|
| L58 | Course Schedule (Kahn's BFS) | 📝 script |
| L59 | Course Schedule II (return the order) | 📝 script |
| L60 | Alien Dictionary (hard) | 📝 script |
| L61 | Minimum Height Trees (leaf trimming) | 📝 script |

## Section 12 — Heaps & Top-K  📝

| id | Title | Status |
|---|---|---|
| L62 | Kth Largest Element | 📝 script |
| L63 | Top K Frequent Elements | 📝 script |
| L64 | K Closest Points to Origin | 📝 script |
| L65 | Merge k Sorted Lists (hard) | 📝 script |
| L66 | Find Median from Data Stream (two heaps, hard) | 📝 script |
| L67 | Task Scheduler | 📝 script |

## Section 13 — Subsets & Backtracking  📝

| id | Title | Status |
|---|---|---|
| L68 | Subsets (the template) | 📝 script |
| L69 | Permutations | 📝 script |
| L70 | Combination Sum | 📝 script |
| L71 | Letter Combinations | 📝 script |
| L72 | Word Search | 📝 script |
| L73 | Generate Parentheses | 📝 script |
| L74 | N-Queens (hard) | 📝 script |

## Section 14 — Dynamic Programming  📝

| id | Title | Status |
|---|---|---|
| L75 | Climbing Stairs (DP on-ramp) | 📝 script |
| L76 | House Robber | 📝 script |
| L77 | Coin Change | 📝 script |
| L78 | Longest Increasing Subsequence | 📝 script |
| L79 | Partition Equal Subset Sum | 📝 script |
| L80 | Longest Common Subsequence | 📝 script |
| L81 | Edit Distance (hard) | 📝 script |
| L82 | Unique Paths | 📝 script |
| L83 | Word Break | 📝 script |
| L84 | Best Time to Buy & Sell Stock | 📝 script |

## Section 15 — Greedy & Intervals  📝

| id | Title | Status |
|---|---|---|
| L85 | Merge Intervals | 📝 script |
| L86 | Insert Interval | 📝 script |
| L87 | Non-overlapping Intervals | 📝 script |
| L88 | Meeting Rooms II | 📝 script |
| L89 | Jump Game | 📝 script |

## Section 16 — Tries & Union-Find  📝

| id | Title | Status |
|---|---|---|
| L90 | Implement Trie (Prefix Tree) | 📝 script |
| L91 | Word Search II (Trie + DFS) | 📝 script |
| L92 | Number of Provinces (Union-Find intro) | 📝 script |
| L93 | Redundant Connection (cycle detect) | 📝 script |
| L94 | Accounts Merge | 📝 script |

## Section 17 — Google Design Problems  📝

| id | Title | Status |
|---|---|---|
| L95 | LRU Cache | 📝 script |
| L96 | LFU Cache | 📝 script |
| L97 | Design HashMap | 📝 script |
| L98 | Insert Delete GetRandom O(1) | 📝 script |
| L99 | Logger Rate Limiter | 📝 script |

## Section 18 — Google Most-Asked Rapid-Fire  📝

| id | Title | Status |
|---|---|---|
| L100 | Two Sum | 📝 script |
| L101 | Product of Array Except Self | 📝 script |
| L102 | Copy List with Random Pointer | 📝 script |
| L103 | Max Area of Island | 📝 script |
| L104 | Group Anagrams | 📝 script |
| L105 | Trapping Rain Water | 📝 script |

## Section 19 — Google Signature Problems  📝

| id | Title | Status |
|---|---|---|
| L111 | Text Justification (hard) | 📝 script |
| L112 | Decode String | 📝 script |
| L113 | Longest Increasing Path in a Matrix (hard) | 📝 script |
| L114 | Subarray Sum Equals K | 📝 script |
| L115 | Time-Based Key-Value Store | 📝 script |
| L116 | Longest Palindromic Substring | 📝 script |

## Section 20 — Mock Interviews & Behavioral

| id | Title | Status |
|---|---|---|
| L106 | Mock Interview 1 — Sliding Window (narrated end-to-end) | ⬜ |
| L107 | Mock Interview 2 — Merge k Sorted Lists (heap + follow-up) | ⬜ |
| L108 | Google's Four Attributes — GCA, RRK, Leadership & Googleyness | ⬜ |
| L109 | STAR Stories — 6 reusable behavioral answers | ⬜ |
| L110 | Your 4-Week Plan + night-before + course send-off | ⬜ |

---

## Current build target

**▶ L08 — The Two-Pointer Idea (Pair with Target Sum).** The engine (`lib_dsa.py`) and the reference scene (`l08/scenes_l08.py`) are in place. Next actions per lesson: finalize script → gen audio → scenes → render → QA loop. L08 is the reference lesson every other pattern lesson is cloned from.

## Build order

Ship **in syllabus order**, one section at a time, mirroring the Amazon/LLD cadence: Section 0 (conceptual, base engine) → Section 2 (Two Pointers) → onward. Conceptual lessons (Section 0–1) can render on the base engine.
