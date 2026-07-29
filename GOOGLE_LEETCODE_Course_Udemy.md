# Crack the Google Coding Interview — Master 15 LeetCode Patterns

> 110 lessons + 15 patterns + 4 mock interviews + cheat sheets | ~16 hours | From "I freeze on the whiteboard" to "I've seen this before"

---

## Why This Course?

You grind 300 LeetCode problems. You still bomb the Google phone screen.

Why? Because you learned **300 problems** instead of **15 patterns**.

Google doesn't ask you a problem you've memorized. They ask you a problem you've never seen — but that *maps* to a pattern you have. The candidate who passes isn't the one who did the most problems. It's the one who looks at a new problem and thinks: *"Sliding window. I've got this,"* and then narrates a clean solution while the interviewer scores their **General Cognitive Ability**.

This course teaches you to **recognize the pattern in the first 60 seconds**, then code it cleanly while thinking out loud — the exact skill Google's interviewers score on the rubric.

---

## How This Course Is Different

| | This Course | Most LeetCode Courses |
|---|---|---|
| **Organizing idea** | 15 reusable patterns | A random list of 300 problems |
| **Per problem** | Brute force → why it's slow → the pattern → optimal | "Here's the optimal solution" (memorize it) |
| **Recognition** | "What signal in the problem tells you which pattern?" | You're on your own |
| **Google focus** | Most-asked Google tags + signature problems, mapped to patterns | Generic |
| **Interview skill** | Think-out-loud narration + complexity on demand — scored as GCA | Just the code |
| **Behavioral** | Googleyness, GCA & Leadership mapped to your project stories | Ignored (and Google scores it in every round) |

---

## What You Need Before Starting

- One language you're comfortable in (examples in **Python + Java**; ideas are language-agnostic)
- Basic data structures: you know what an array, hash map, and linked list *are* (we re-teach the rest)
- A LeetCode account (free tier is enough for every problem in this course)

No CS degree required. No advanced math. If you can write a `for` loop and a function, you can start here.

---

## How Every Lesson Works

Each problem-solving lesson follows the same rhythm — so your brain stops burning energy on "what's happening" and spends it on the actual idea.

**Part 1: The Pattern (~3 min)** — The signal that screams "use me," the mental model, and one quick recognition check.

**Part 2: The Solve (~6 min)** — every problem is broken into **three explicit layers**:

1. **Brute Force** — the obvious solution everyone writes first, with its Big-O and *why it times out*.
2. **Optimised Solution** — the pattern that removes the repeated work, with the new (better) time complexity.
3. **Space Optimization** — cut extra memory where the problem allows (in-place, rolling variables, two pointers instead of a copy). When a solution is already optimal on space, we **say so** — naming the absence is as strong as finding the trick.

> Example of THE BRUTE FORCE: "Two nested loops. For every number, scan the rest of the array looking for its complement. Works on the 4-element example. Times out on the 10,000-element hidden test. O(n²). The interviewer's face does not change — which is worse than a frown."

---

## Course Outline — 110 Lessons in 20 Sections

### Section 0: Orientation (3 lessons)

> How Google's loop actually works, and how to talk while you code.

| # | Lesson | Duration |
|---|--------|----------|
| 00 | What You'll Master + How to Use This Course | ~5 min (theory only) |
| 01 | Inside the Google Loop — Phone Screen, Onsite, Hiring Committee, Team Match | ~9 min |
| 02 | Think-Out-Loud — The 6-Step Framework for Any Problem | ~10 min |

**The 6-Step Framework (used in every lesson after this):** Clarify → Examples → Brute force + complexity → Optimize (name the pattern) → Code → Test & edge cases.

---

### Section 1: Complexity & The Toolbox (5 lessons)

> Big-O without the math-class dread, and the data structures every pattern leans on.

| # | Lesson | Duration |
|---|--------|----------|
| 03 | Big-O in Plain English — Why O(n²) Times Out | ~9 min |
| 04 | The Hash Map — Your Most-Used Weapon | ~9 min |
| 05 | Arrays & Strings — Indices, In-Place, and Gotchas | ~9 min |
| 06 | Stacks & Queues — LIFO/FIFO and When to Reach for Each | ~9 min |
| 07 | Recursion & The Call Stack — Reading Your Own Mind | ~10 min |

---

### Section 2: Pattern 1 — Two Pointers (6 lessons)

> Two indices walking an array so you don't need a second loop. Turns O(n²) into O(n).

> **Recognition signal:** sorted array · pair/triplet that sums to a target · comparing from both ends · in-place dedupe.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 08 | The Two-Pointer Idea | Pair with Target Sum (sorted) | Easy | ~9 min |
| 09 | Squeeze from Both Ends | Valid Palindrome | Easy | ~9 min |
| 10 | Remove Duplicates In-Place | Remove Duplicates from Sorted Array | Easy | ~9 min |
| 11 | The Fix for 3Sum | 3Sum | Medium | ~12 min |
| 12 | Trapping Water | Container With Most Water | Medium | ~10 min |
| 13 | Dutch National Flag | Sort Colors | Medium | ~10 min |

---

### Section 3: Pattern 2 — Sliding Window (7 lessons)

> A window that grows and shrinks over a contiguous run. The go-to for "longest/shortest substring or subarray."

> **Recognition signal:** contiguous subarray/substring · "longest / shortest / max / min" with a constraint · running sum or character counts.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 14 | Fixed Window — Max Sum Subarray of Size K | Maximum Average Subarray I | Easy | ~9 min |
| 15 | Dynamic Window — Smallest Subarray ≥ Target | Minimum Size Subarray Sum | Medium | ~11 min |
| 16 | Window + Hash Map | Longest Substring Without Repeating Characters | Medium | ~12 min |
| 17 | Character Replacement | Longest Repeating Character Replacement | Medium | ~11 min |
| 18 | Permutation in a String | Permutation in String | Medium | ~10 min |
| 19 | The Hard One — Minimum Window Substring | Minimum Window Substring | Hard | ~14 min |
| 20 | Pattern Recap + Recognition Drill | Mixed | — | ~8 min |

---

### Section 4: Pattern 3 — Fast & Slow Pointers (4 lessons)

> Two pointers at different speeds. Detects cycles and finds middles without extra memory.

> **Recognition signal:** linked list cycle · find the middle · "happy number" style number cycles.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 21 | Tortoise & Hare | Linked List Cycle | Easy | ~9 min |
| 22 | Find the Cycle Start | Linked List Cycle II | Medium | ~11 min |
| 23 | Middle of the List | Middle of the Linked List | Easy | ~8 min |
| 24 | Happy Number | Happy Number | Easy | ~9 min |

---

### Section 5: Pattern 4 — Linked List In-Place Reversal (4 lessons)

> Rewire `next` pointers as you walk. Reversal with O(1) extra space — a Google favorite for testing pointer discipline.

> **Recognition signal:** reverse a list or sublist · reorder nodes · no extra memory allowed.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 25 | Reverse a Whole List | Reverse Linked List | Easy | ~10 min |
| 26 | Reverse a Sublist | Reverse Linked List II | Medium | ~12 min |
| 27 | Reverse in K-Groups | Reverse Nodes in k-Group | Hard | ~13 min |
| 28 | Reorder List | Reorder List | Medium | ~11 min |

---

### Section 6: Pattern 5 — Stacks (5 lessons)

> When the answer depends on "the most recent unmatched thing," a stack is the tool.

> **Recognition signal:** matching pairs/brackets · "next greater/smaller element" · parsing/evaluating expressions · monotonic sequences.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 29 | Matching Brackets | Valid Parentheses | Easy | ~9 min |
| 30 | Min Stack — O(1) Minimum | Min Stack | Medium | ~10 min |
| 31 | The Monotonic Stack | Next Greater Element | Medium | ~11 min |
| 32 | Daily Temperatures | Daily Temperatures | Medium | ~10 min |
| 33 | Largest Rectangle in Histogram | Largest Rectangle in Histogram | Hard | ~14 min |

---

### Section 7: Pattern 6 — Binary Search (Modified) (6 lessons)

> Not just "find a number in a sorted array." Any time the answer space is monotonic, you can binary-search it.

> **Recognition signal:** sorted (or rotated-sorted) input · "find the minimum X that works" · O(log n) demanded.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 34 | The Template That Never Off-by-Ones | Binary Search | Easy | ~10 min |
| 35 | Search a Rotated Array | Search in Rotated Sorted Array | Medium | ~12 min |
| 36 | Find the Boundary | First Bad Version | Easy | ~9 min |
| 37 | Search a 2D Matrix | Search a 2D Matrix | Medium | ~10 min |
| 38 | Binary Search on the Answer | Koko Eating Bananas | Medium | ~12 min |
| 39 | Median of Two Sorted Arrays | Median of Two Sorted Arrays | Hard | ~15 min |

---

### Section 8: Pattern 7 — Trees: BFS (5 lessons)

> Level-by-level traversal with a queue. The moment a problem says "level," reach for BFS.

> **Recognition signal:** "level order" · shortest path in an unweighted tree/grid · "per level" aggregation.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 40 | Level-Order Traversal | Binary Tree Level Order Traversal | Medium | ~11 min |
| 41 | Zigzag Levels | Binary Tree Zigzag Level Order Traversal | Medium | ~11 min |
| 42 | Right Side View | Binary Tree Right Side View | Medium | ~9 min |
| 43 | Minimum Depth | Minimum Depth of Binary Tree | Easy | ~8 min |
| 44 | Connect Level-Order Siblings | Populating Next Right Pointers | Medium | ~11 min |

---

### Section 9: Pattern 8 — Trees: DFS (6 lessons)

> Recursion down each branch. The workhorse for path sums, depths, and "does a path exist" questions.

> **Recognition signal:** root-to-leaf paths · "sum along a path" · tree height/diameter · validate a tree property.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 45 | The DFS Template | Maximum Depth of Binary Tree | Easy | ~9 min |
| 46 | Path Sum Exists | Path Sum | Easy | ~9 min |
| 47 | All Root-to-Leaf Paths | Binary Tree Paths | Easy | ~10 min |
| 48 | Diameter of a Tree | Diameter of Binary Tree | Easy | ~11 min |
| 49 | Validate a BST | Validate Binary Search Tree | Medium | ~11 min |
| 50 | Lowest Common Ancestor | Lowest Common Ancestor of a Binary Tree | Medium | ~12 min |

---

### Section 10: Pattern 9 — Graphs (BFS/DFS on Grids & Nodes) (7 lessons)

> Islands, rooms, and rotting oranges. Google *loves* grid-as-graph problems and node-graph modeling.

> **Recognition signal:** 2D grid of cells · "connected regions" · shortest steps to fill/reach · nodes with edges.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 51 | Grid as a Graph | Number of Islands | Medium | ~12 min |
| 52 | Multi-Source BFS | Rotting Oranges | Medium | ~12 min |
| 53 | Flood Fill | Flood Fill | Easy | ~9 min |
| 54 | Clone a Graph | Clone Graph | Medium | ~12 min |
| 55 | Walls and Gates / 01 Matrix | 01 Matrix | Medium | ~11 min |
| 56 | Word Ladder — Shortest Transformation | Word Ladder | Hard | ~14 min |
| 57 | Pattern Recap + Grid Template | Mixed | — | ~8 min |

---

### Section 11: Pattern 10 — Topological Sort (4 lessons)

> Ordering things with dependencies. If the problem smells like a schedule or prerequisites, it's topo sort.

> **Recognition signal:** "order of tasks" · prerequisites · detect a cycle in a directed graph · build order.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 58 | Kahn's Algorithm (BFS Topo) | Course Schedule | Medium | ~12 min |
| 59 | Return the Order | Course Schedule II | Medium | ~11 min |
| 60 | Alien Dictionary | Alien Dictionary | Hard | ~14 min |
| 61 | Minimum Height Trees | Minimum Height Trees | Medium | ~12 min |

---

### Section 12: Pattern 11 — Heaps & Top-K (6 lessons)

> A heap keeps the best (or worst) element one pop away. The answer to nearly every "top K / K closest / Kth largest."

> **Recognition signal:** "K largest/smallest/closest/frequent" · running median · merge sorted streams.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 62 | Heap in 10 Minutes | Kth Largest Element in an Array | Medium | ~11 min |
| 63 | Top K Frequent | Top K Frequent Elements | Medium | ~11 min |
| 64 | K Closest Points to Origin | K Closest Points to Origin | Medium | ~10 min |
| 65 | Merge K Sorted Lists | Merge k Sorted Lists | Hard | ~13 min |
| 66 | Two Heaps — Find Median from a Stream | Find Median from Data Stream | Hard | ~14 min |
| 67 | Task Scheduler | Task Scheduler | Medium | ~12 min |

---

### Section 13: Pattern 12 — Subsets & Backtracking (7 lessons)

> Build every combination by choosing, recursing, and un-choosing. The template behind subsets, permutations, and constraint puzzles.

> **Recognition signal:** "all combinations / permutations / subsets" · "generate every valid ___" · constraint satisfaction (N-Queens, Sudoku).

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 68 | The Backtracking Template | Subsets | Medium | ~12 min |
| 69 | Permutations | Permutations | Medium | ~11 min |
| 70 | Combination Sum | Combination Sum | Medium | ~12 min |
| 71 | Letter Combinations of a Phone Number | Letter Combinations of a Phone Number | Medium | ~11 min |
| 72 | Word Search (Grid Backtracking) | Word Search | Medium | ~13 min |
| 73 | Generate Parentheses | Generate Parentheses | Medium | ~11 min |
| 74 | N-Queens (Optional Boss Level) | N-Queens | Hard | ~14 min |

---

### Section 14: Pattern 13 — Dynamic Programming (10 lessons)

> The one people fear. We kill the fear with one idea: *store answers to subproblems so you never redo work.*

> **Recognition signal:** "number of ways" · "min/max cost/path" · overlapping subproblems · "can you make X from these?"

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 75 | DP Demystified — Memoize First | Fibonacci / Climbing Stairs | Easy | ~12 min |
| 76 | House Robber — Choose or Skip | House Robber | Medium | ~11 min |
| 77 | Coin Change — Unbounded Knapsack | Coin Change | Medium | ~13 min |
| 78 | Longest Increasing Subsequence | Longest Increasing Subsequence | Medium | ~13 min |
| 79 | 0/1 Knapsack & Partition | Partition Equal Subset Sum | Medium | ~13 min |
| 80 | Longest Common Subsequence | Longest Common Subsequence | Medium | ~12 min |
| 81 | Edit Distance | Edit Distance | Hard | ~14 min |
| 82 | Unique Paths (Grid DP) | Unique Paths | Medium | ~10 min |
| 83 | Word Break | Word Break | Medium | ~12 min |
| 84 | Best Time to Buy & Sell Stock (I–II) | Best Time to Buy and Sell Stock | Easy/Medium | ~12 min |

---

### Section 15: Pattern 14 — Greedy & Intervals (5 lessons)

> Sort, then take the locally-best choice. Half of all "interval" problems fall to one greedy insight.

> **Recognition signal:** intervals to merge/schedule · "maximum non-overlapping" · "minimum to remove" · jump/reach problems.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 85 | Merge Intervals | Merge Intervals | Medium | ~11 min |
| 86 | Insert Interval | Insert Interval | Medium | ~11 min |
| 87 | Non-Overlapping Intervals | Non-overlapping Intervals | Medium | ~11 min |
| 88 | Meeting Rooms II | Meeting Rooms II | Medium | ~12 min |
| 89 | Jump Game | Jump Game | Medium | ~10 min |

---

### Section 16: Pattern 15 — Tries & Union-Find (5 lessons)

> Two specialized structures that make certain Google problems trivial — and everyone else's brute force too slow.

> **Recognition signal (Trie):** prefix search · autocomplete · word dictionaries. **(Union-Find):** connected components · "are these two joined?" · number of groups.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 90 | Build a Trie | Implement Trie (Prefix Tree) | Medium | ~12 min |
| 91 | Word Search II (Trie + Backtracking) | Word Search II | Hard | ~14 min |
| 92 | Union-Find Fundamentals | Number of Provinces | Medium | ~12 min |
| 93 | Redundant Connection | Redundant Connection | Medium | ~11 min |
| 94 | Accounts Merge | Accounts Merge | Medium | ~13 min |

---

### Section 17: Google Design Problems (5 lessons)

> The "implement this class" questions Google reuses across teams. Half data-structure design, half taste.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 95 | LRU Cache — The Classic Design Problem | LRU Cache | Medium | ~14 min |
| 96 | LFU Cache | LFU Cache | Hard | ~14 min |
| 97 | Design an In-Memory Key-Value Store | Design HashMap | Easy | ~10 min |
| 98 | Insert/Delete/GetRandom O(1) | Insert Delete GetRandom O(1) | Medium | ~12 min |
| 99 | Design a Rate Limiter (Discussion) | Logger Rate Limiter | Medium | ~11 min |

---

### Section 18: Google Most-Asked Rapid-Fire (6 lessons)

> The exact tags that show up most on Google's LeetCode company page, drilled fast.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 100 | Two Sum + Group Anagrams | Two Sum · Group Anagrams | Easy/Medium | ~12 min |
| 101 | Product of Array Except Self | Product of Array Except Self | Medium | ~10 min |
| 102 | Copy List with Random Pointer | Copy List with Random Pointer | Medium | ~12 min |
| 103 | Number of Islands + Max Area | Max Area of Island | Medium | ~10 min |
| 104 | Kth Largest / Top K Recap | Mixed | — | ~10 min |
| 105 | Trapping Rain Water | Trapping Rain Water | Hard | ~13 min |

---

### Section 19: Google Signature Problems (6 lessons)

> The problems everyone associates with a Google interview — string parsing, grid memoization, prefix sums, and the ones that show up nowhere else as often.

> **Recognition signal:** greedy line-packing · nested decoding with a stack · DFS + memo on a matrix · running prefix-sum + hash map.

| # | Lesson | Problem | Difficulty | Duration |
|---|--------|---------|------------|----------|
| 111 | Text Justification | Text Justification | Hard | ~14 min |
| 112 | Decode String | Decode String | Medium | ~12 min |
| 113 | Longest Increasing Path in a Matrix | Longest Increasing Path in a Matrix | Hard | ~13 min |
| 114 | Subarray Sum Equals K | Subarray Sum Equals K | Medium | ~11 min |
| 115 | Time-Based Key-Value Store | Time Based Key-Value Store | Medium | ~11 min |
| 116 | Longest Palindromic Substring | Longest Palindromic Substring | Medium | ~12 min |

---

### Section 20: Mock Interviews & Behavioral (5 lessons)

> Pattern knowledge gets you to the loop. These two things get you the offer.

| # | Lesson | Duration |
|---|--------|----------|
| 106 | Mock Interview 1 — Medium, Narrated End-to-End | ~15 min |
| 107 | Mock Interview 2 — Hard, With a Follow-Up Twist | ~15 min |
| 108 | Google's Four Attributes — GCA, RRK, Leadership & Googleyness | ~12 min |
| 109 | STAR Stories — Build 6 Reusable Behavioral Answers | ~12 min |
| 110 | Your 4-Week Plan + What to Do the Night Before | ~10 min (theory only) |

---

## 4 Mock Interviews (You Solve Them Live With Me)

| # | Level | Pattern(s) Tested | Twist | Time |
|---|-------|-------------------|-------|------|
| 1 | Medium | Sliding Window | "Now do it in one pass" | ~15 min |
| 2 | Medium | Trees BFS + DFS | "What if the tree is huge?" | ~15 min |
| 3 | Hard | Heap + Graph | Merge streams under a memory cap | ~15 min |
| 4 | Medium→Hard | DP | "Reconstruct the actual answer, not just the count" | ~15 min |

Each mock is narrated the way you should narrate: clarify, brute force, optimize, code, test — out loud. Google interviewers score this narration as **General Cognitive Ability (GCA)** — how you *approach* the problem, not just whether you land the answer.

---

## What You Can Download

| Resource | What's In It |
|----------|-------------|
| **Pattern Selector Cheat Sheet** | Every pattern + the exact signal that triggers it → `resources/Cheat_Sheet_Pattern_Selector.md` |
| **Big-O Cheat Sheet** | Complexity of every common operation + how to say it out loud → `resources/Cheat_Sheet_Big_O.md` |
| **The 6-Step Framework Card** | The think-out-loud script for any problem → `resources/Cheat_Sheet_6_Step_Framework.md` |
| **Googleyness, GCA & Leadership Map** | Google's four hiring attributes → which coding/project story to tell → `resources/Googleyness_and_Leadership.md` |
| **Google Top-50 Problem List** | The most-tagged problems, grouped by pattern → `resources/Google_Top_50_Problem_List.md` |

---

## Lesson Template (Every Problem Lesson Follows This)

| Phase | Time | What Happens |
|-------|------|-------------|
| **HOOK** | 0:00 | A "you've been there" moment — "You wrote two nested loops and the hidden test timed out." |
| **STORY / ANALOGY** | 0:30 | A real-world picture for the pattern — two pointers as bookends, sliding window as a train car. |
| **THE PATTERN** | 1:30 | The core idea + the recognition signal in plain English. |
| **QUICK CHECK** | 2:30 | One question: "Would this pattern fire here — yes or no?" |
| --- | --- | **PART 2 STARTS — the 3-layer solve** |
| **① THE BRUTE FORCE** | 3:00 | The obvious slow solution + its Big-O + *why* it times out. Mini-story. |
| **② THE OPTIMISED SOLUTION** | 5:00 | Same problem, the pattern applied. Better time complexity; you see the contrast instantly. |
| **③ SPACE OPTIMIZATION** | 7:00 | Cut extra memory if the problem allows (in-place / rolling vars / two pointers). If already optimal, say so and explain why. |
| **COMPLEXITY OUT LOUD** | 7:45 | State final time & space like you would to an interviewer. |
| **ACTIVE RECALL** | 8:00 | Your turn — a near-twin problem to try before the next lesson. |
| **3 TAKEAWAYS** | 8:30 | Three things to remember. |
| **CLIFFHANGER** | 9:00 | Why the next problem breaks this approach — and what fixes it. |

---

## Section Flow — Each Builds on the Last

```
Orientation (L00–L02) — the loop + how to talk while coding
    ↓
Toolbox (L03–L07) — Big-O, hash maps, arrays, stacks, recursion
    ↓
Linear patterns: Two Pointers → Sliding Window → Fast/Slow → List Reversal → Stacks
    ↓
Search: Binary Search (modified)
    ↓
Trees: BFS → DFS
    ↓
Graphs: grid/node BFS-DFS → Topological Sort
    ↓
Heaps & Top-K → Subsets/Backtracking
    ↓
Dynamic Programming (the big one)
    ↓
Greedy/Intervals → Tries & Union-Find
    ↓
Google design problems → most-asked rapid-fire → Google signature problems
    ↓
Mock interviews + Googleyness/GCA → your 4-week plan
```

No lesson uses a pattern that hasn't been taught yet. Every hard problem is the last brick on a wall of easier ones.

---

## Writing Style Rules (For Session Authors)

- **Tone:** Senior engineer who's passed the Google loop, explaining to a friend the night before. Not a professor.
- **Sentences:** Short. Punchy. One idea per line.
- **Words:** Plain English. "The loop scans the array again" not "the algorithm re-traverses the collection."
- **Jargon:** Define it the moment you use it. "Monotonic stack — a stack that only ever increases (or only decreases)."
- **The Pattern:** Under 3 minutes. If you can't state the recognition signal in one sentence, you don't understand it yet.
- **THE BRUTE FORCE:** Always a mini-story with a consequence. "It passes the example, times out on the hidden test, and the interviewer says nothing. Silence is the tell."
- **Code:** Python first for readability, Java second for the many Google candidates who interview in Java. Comment the *why*, not the *what*.
- **Complexity:** Every lesson ends with time AND space, stated the way you'd say it out loud.
- **Recognition over memorization:** Every lesson answers "what in the problem told you to use this?" — that's the transferable skill.
- **GCA framing:** Remind students that Google scores *how they think*, not just the final code. Narrate the approach.

---

**Total: 116 lessons (L00–L116) + 4 mock interviews + 5 downloadable resources | ~17 hours | Average ~11 min/lesson**
