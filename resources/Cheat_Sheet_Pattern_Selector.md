# 🎯 Pattern Selector Cheat Sheet

> Print this. Before you write a line of code, read the problem and find the signal. The signal picks the pattern.

---

## The 30-Second Triage

| If the problem says / has… | Reach for… | Why |
|---|---|---|
| **Sorted array** + find a pair/triplet to a target | **Two Pointers** | Move ends inward; O(n) instead of O(n²) |
| **Contiguous** subarray/substring, "longest/shortest/max/min" with a constraint | **Sliding Window** | Grow/shrink a window; O(n) |
| **Linked list** + cycle / middle / "no extra space" | **Fast & Slow Pointers** | Two speeds meet inside a cycle |
| **Reverse** a list or sublist, in place | **In-Place Reversal** | Rewire `next` as you walk |
| **Matching pairs**, brackets, "next greater/smaller" | **Stack (Monotonic)** | Most-recent-unmatched lives on top |
| **Sorted / rotated-sorted**, or "min X that works" | **Binary Search** | Halve a monotonic answer space |
| Tree, **"level" / "level order" / per-level** | **Tree BFS** | Queue processes one level at a time |
| Tree, **root-to-leaf path / height / validate** | **Tree DFS** | Recurse each branch |
| **2D grid** of cells, "islands / regions / steps to fill" | **Graph BFS/DFS** | Each cell is a node; flood or spread |
| **"Order of tasks" / prerequisites / build order** | **Topological Sort** | Resolve a DAG's dependencies |
| **"K largest / smallest / closest / frequent"**, running median | **Heap / Top-K** | Best element is one pop away |
| **"All subsets / permutations / combinations"**, constraint puzzles | **Backtracking** | Choose → recurse → un-choose |
| **"Number of ways" / "min-max cost"**, overlapping subproblems | **Dynamic Programming** | Store subproblem answers, reuse |
| **Intervals** to merge/schedule; "max non-overlapping" | **Greedy + Sort** | Sort, then take locally-best |
| **Prefix / autocomplete / word dictionary** | **Trie** | Share common prefixes |
| **"Connected components" / "are these joined?"** | **Union-Find** | Merge sets, count roots |

---

## Recognition drills — say the pattern out loud

1. *"Find two numbers in a **sorted** array that add to 9."* → **Two Pointers**
2. *"Longest substring with at most 2 distinct chars."* → **Sliding Window**
3. *"Does this linked list have a cycle?"* → **Fast & Slow**
4. *"Number of islands in a grid."* → **Graph BFS/DFS**
5. *"Can you finish all courses given prerequisites?"* → **Topological Sort**
6. *"K closest points to the origin."* → **Heap / Top-K**
7. *"All subsets of [1,2,3]."* → **Backtracking**
8. *"Fewest coins to make amount 11."* → **DP (unbounded knapsack)**
9. *"Merge overlapping meeting intervals."* → **Greedy + Sort**
10. *"Autocomplete a search bar."* → **Trie**

---

## When two patterns both seem to fit

- **Sliding Window vs Two Pointers:** contiguous run with a running metric → window. Pair/triplet by value in sorted data → two pointers.
- **BFS vs DFS on a tree:** need *levels* or *shortest*? BFS. Need *paths* or *a property of subtrees*? DFS.
- **Heap vs Sort:** need only the *top K* (not the full order) or a *stream*? Heap — O(n log k) beats O(n log n).
- **DP vs Greedy:** does a locally-best choice always stay globally-best? Greedy. If you can't prove that, DP is the safe bet.
- **Backtracking vs DP:** need to *enumerate* every solution? Backtracking. Need to *count/optimize* over overlapping subproblems? DP.

---

## The meta-rule

> Brute force **first**, always. State its complexity out loud. *Then* ask: "what work am I repeating?" The pattern is almost always the answer to that question.
