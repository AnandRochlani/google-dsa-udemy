# Crack the Google Coding Interview — The 50-Problem List, Decoded

> 50 real Google-tagged problems + the patterns behind them + Googleyness/GCA prep | ~11 hours | From "I froze on a problem I'd never seen" to "I've seen the *shape* of this before"

---

## Why This Course?

Most "Google prep" is a random pile of 300 problems. This course is built around **one specific, curated list of 50 problems** that actually show up in Google loops — the harder, stranger, often Google-premium questions (Robot Room Cleaner, Guess the Word, Race Car, Text Justification, Meeting Rooms III…) that generic courses skip.

But we don't memorize 50 answers. Each problem is taught **intuition-first** and mapped to the reusable **pattern** underneath it, because Google scores **General Cognitive Ability (GCA)** — *how you think out loud on a problem you've never seen* — not whether you'd memorized this exact one.

Every problem lesson runs the same 3-layer solve:

```
🧠 INTUITION → ① BRUTE FORCE (why it times out)
            → ② OPTIMISED (the pattern applied)
            → ③ SPACE OPTIMIZATION (or "already optimal — here's why")
→ COMPLEXITY OUT LOUD → ACTIVE RECALL → 3 TAKEAWAYS
```

---

## How This Course Is Different

| | This Course | Most Google Courses |
|---|---|---|
| **Problem set** | 50 real Google-tagged questions (incl. premium/hard) | Generic "top 75" everyone has |
| **Per problem** | Brute force → why it's slow → the pattern → optimal | "Here's the optimal solution" (memorize it) |
| **Organizing idea** | The pattern *underneath* each problem | A flat list |
| **Interview skill** | Think-out-loud narration — scored as **GCA** | Just the code |
| **Behavioral** | Googleyness, GCA & Leadership mapped to your stories | Ignored |

---

## What You Need Before Starting

- One language you're comfortable in (examples in **Python + Java**; ideas are language-agnostic)
- Basic data structures (array, hash map, tree, graph). We re-teach the patterns.
- A LeetCode account (several of these are LeetCode Premium — noted where relevant).

---

## The 50 Problems — Grouped by Pattern (11 Sections)

Each row links to a full write-up in `problems/` and a recording script in `scripts/`. Difficulty: 🟢 Easy · 🟡 Medium · 🔴 Hard.

### Section 1 — Strings & Parsing (10)
> Greedy line-packing, subsequence matching, in-place text surgery. Google's favorite warm-up territory.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 01 | 68 | Text Justification | 🔴 |
| 02 | 418 | Sentence Screen Fitting | 🟡 |
| 03 | 833 | Find And Replace in String | 🟡 |
| 04 | 777 | Swap Adjacent in LR String | 🟡 |
| 05 | 1554 | Strings Differ by One Character | 🟡 |
| 06 | 792 | Number of Matching Subsequences | 🟡 |
| 07 | 2135 | Count Words Obtained After Adding a Letter | 🟡 |
| 08 | 539 | Minimum Time Difference | 🟡 |
| 09 | 1055 | Shortest Way to Form String | 🟡 |
| 10 | 2018 | Check if Word Can Be Placed In Crossword | 🟡 |

### Section 2 — Tries (1)
> Share prefixes; count words-through-a-node.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 11 | 2416 | Sum of Prefix Scores of Strings | 🔴 |

### Section 3 — Graphs & Grids (8)
> BFS with state, Dijkstra-on-a-grid, flood/spread, grid-as-graph, DFS + memo.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 12 | 1293 | Shortest Path in a Grid with Obstacles Elimination | 🔴 |
| 13 | 778 | Swim in Rising Water | 🔴 |
| 14 | 2101 | Detonate the Maximum Bombs | 🟡 |
| 15 | 419 | Battleships in a Board | 🟡 |
| 16 | 562 | Longest Line of Consecutive One in Matrix | 🟡 |
| 17 | 2128 | Remove All Ones With Row and Column Flips | 🟡 |
| 18 | 329 | Longest Increasing Path in a Matrix | 🔴 |
| 19 | 2242 | Maximum Score of a Node Sequence | 🔴 |

### Section 4 — Union-Find (3)
> Merge sets, count components, "process by increasing value."

| # | LC | Problem | Diff |
|---|----|---------|------|
| 20 | 1101 | The Earliest Moment When Everyone Become Friends | 🟡 |
| 21 | 839 | Similar String Groups | 🔴 |
| 22 | 2421 | Number of Good Paths | 🔴 |

### Section 5 — Topological Sort (1)
> Resolve dependencies; make what your supplies allow.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 23 | 2115 | Find All Possible Recipes from Given Supplies | 🟡 |

### Section 6 — Trees (2)
> Root-to-node paths + LCA; height-from-the-bottom grouping.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 24 | 2096 | Step-By-Step Directions From a Binary Tree Node to Another | 🟡 |
| 25 | 366 | Find Leaves of Binary Tree | 🟡 |

### Section 7 — Heaps, Intervals & Scheduling (7)
> Two-heap assignment, room scheduling, interval books, paint-skipping.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 26 | 253 | Meeting Rooms II | 🟡 |
| 27 | 2402 | Meeting Rooms III | 🔴 |
| 28 | 1606 | Find Servers That Handled Most Number of Requests | 🔴 |
| 29 | 729 | My Calendar I | 🟡 |
| 30 | 2158 | Amount of New Area Painted Each Day | 🔴 |
| 31 | 1996 | The Number of Weak Characters in the Game | 🟡 |
| 32 | 715 | Range Module | 🔴 |

### Section 8 — Design (Implement-a-Class) (7)
> Prefix-sum + binary search, versioned arrays, lazy heaps, geometry counting.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 33 | 528 | Random Pick with Weight | 🟡 |
| 34 | 900 | RLE Iterator | 🟡 |
| 35 | 1146 | Snapshot Array | 🟡 |
| 36 | 2013 | Detect Squares | 🟡 |
| 37 | 2034 | Stock Price Fluctuation | 🟡 |
| 38 | 359 | Logger Rate Limiter | 🟢 |
| 39 | 2162 | Minimum Cost to Set Cooking Time | 🟡 |

### Section 9 — Dynamic Programming (7)
> Row DP with L/R passes, state machines, bitmask assignment, chains.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 40 | 1937 | Maximum Number of Points with Cost | 🟡 |
| 41 | 552 | Student Attendance Record II | 🔴 |
| 42 | 1105 | Filling Bookcase Shelves | 🟡 |
| 43 | 818 | Race Car | 🔴 |
| 44 | 1048 | Longest String Chain | 🟡 |
| 45 | 1387 | Sort Integers by The Power Value | 🟡 |
| 46 | 2172 | Maximum AND Sum of Array | 🔴 |

### Section 10 — Backtracking & Interactive (2)
> DFS + backtrack against a hidden world; minimax against a Master API.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 47 | 489 | Robot Room Cleaner | 🔴 |
| 48 | 843 | Guess the Word | 🔴 |

### Section 11 — Geometry & Math (2)
> Angle sliding windows; greedy even splits.

| # | LC | Problem | Diff |
|---|----|---------|------|
| 49 | 1610 | Maximum Number of Visible Points | 🔴 |
| 50 | 2178 | Maximum Split of Positive Even Integers | 🟡 |

---

## The Patterns Behind the 50

Strings/Greedy · Trie · Grid BFS/DFS (with state) · Dijkstra-on-grid · Union-Find · Topological Sort · Tree DFS/LCA · Heaps & Two-Heap scheduling · Interval structures (TreeMap/segment) · Prefix-sum + Binary Search · Row/State-machine/Bitmask DP · Backtracking · Interactive minimax · Angle geometry.

Learn the pattern once; each problem becomes "oh, it's *that* shape."

---

## Behavioral & GCA (bundled, not bolted-on)

Google scores four attributes — **General Cognitive Ability (GCA)**, **Role-Related Knowledge (RRK)**, **Leadership**, and **Googleyness**. GCA is scored *while you code*, which is why every lesson drills narrating your approach. See `resources/Googleyness_and_Leadership.md` for the story map and STAR template.

---

## What You Can Download

| Resource | What's In It |
|----------|-------------|
| **Pattern Selector Cheat Sheet** | Every pattern + the signal that triggers it → `resources/Cheat_Sheet_Pattern_Selector.md` |
| **Big-O Cheat Sheet** | Complexity of every common operation → `resources/Cheat_Sheet_Big_O.md` |
| **The 6-Step Framework Card** | The think-out-loud script for any problem → `resources/Cheat_Sheet_6_Step_Framework.md` |
| **Googleyness, GCA & Leadership Map** | Google's four attributes → which story to tell → `resources/Googleyness_and_Leadership.md` |
| **The Google 50 List** | This exact list, grouped, as a checklist → `resources/Google_50_Problem_List.md` |

---

## Lesson Template (Every Problem Lesson Follows This)

| Phase | What Happens |
|-------|-------------|
| **HOOK** | A "you've been there" moment. |
| **THE PATTERN** | The signal + the mental model + a recognition check. |
| **① BRUTE FORCE** | The obvious slow solution + its Big-O + *why* it times out. |
| **② OPTIMISED** | The pattern applied; the better complexity, contrasted. |
| **③ SPACE OPTIMIZATION** | Cut memory if possible; if optimal, say why. |
| **COMPLEXITY OUT LOUD** | Time & space, said the interviewer's way (your GCA moment). |
| **ACTIVE RECALL + TAKEAWAYS** | A near-twin to try + 3 things to remember + a memory peg. |

---

## Writing Style Rules (For Session Authors)

- **Tone:** Senior engineer who passed the Google loop, explaining to a friend. Not a professor.
- **Sentences:** Short. Punchy. One idea per line.
- **Code:** Python first for readability, Java second. Comment the *why*.
- **Complexity:** Every lesson ends with time AND space, stated out loud.
- **GCA framing:** Google scores *how you think*. Narrate the approach — clarifying questions score.
- **Recognition over memorization:** Every lesson answers "what in the problem told you to use this pattern?"

---

**Total: 50 problems across 11 pattern sections + behavioral/GCA prep | ~11 hours | Full intuition-first write-ups + two-voice recording scripts.**
