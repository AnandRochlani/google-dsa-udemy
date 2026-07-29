# ⏱️ Big-O Cheat Sheet — and How to Say It Out Loud

> Interviewers don't just want the right answer. They want to hear you reason about cost. This is the vocabulary.

---

## The growth ladder (best → worst)

| Big-O | Name | n = 10 | n = 1,000 | n = 1,000,000 | Feels like |
|---|---|---|---|---|---|
| O(1) | Constant | 1 | 1 | 1 | Instant |
| O(log n) | Logarithmic | 3 | 10 | 20 | Binary search |
| O(n) | Linear | 10 | 1,000 | 1,000,000 | One pass |
| O(n log n) | Linearithmic | 33 | 10,000 | 20,000,000 | Good sort |
| O(n²) | Quadratic | 100 | 1,000,000 | 10¹² 💀 | Two nested loops |
| O(2ⁿ) | Exponential | 1,024 | astronomically huge | — | Naive recursion |
| O(n!) | Factorial | 3.6M | — | — | All permutations |

**The line most interviews care about:** at n ≈ 10⁴–10⁵, **O(n²) times out** and you need O(n log n) or O(n). That's the whole reason patterns exist.

---

## Common data-structure operations

| Structure | Access | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) | Index is instant; shifting is not |
| Hash Map / Set | — | O(1)* | O(1)* | O(1)* | *amortized; worst case O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(1) insert/delete *if you have the node* |
| Stack / Queue | — | — | O(1) | O(1) | Push/pop/enqueue/dequeue |
| Binary Heap | O(1) peek | O(n) | O(log n) | O(log n) | Top element is free to read |
| Balanced BST / TreeMap | O(log n) | O(log n) | O(log n) | O(log n) | Sorted order for free |
| Trie | — | O(L) | O(L) | O(L) | L = length of the word |

---

## Pattern → typical complexity

| Pattern | Time | Space |
|---|---|---|
| Two Pointers | O(n) | O(1) |
| Sliding Window | O(n) | O(k) for the window/counts |
| Fast & Slow Pointers | O(n) | O(1) |
| Binary Search | O(log n) | O(1) |
| Tree BFS / DFS | O(n) | O(n) worst (skewed / queue width) |
| Graph BFS / DFS | O(V + E) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| Heap / Top-K | O(n log k) | O(k) |
| Backtracking | O(branches^depth) | O(depth) recursion |
| DP | O(states × work/state) | O(states), often reducible |
| Union-Find | ~O(α(n)) ≈ O(1) per op | O(n) |

---

## How to say it out loud (the script)

Don't just write it — narrate it:

> *"Time is O(n) — I touch each element at most twice, once with each pointer. Space is O(1) — I only keep two indices, no extra structure that grows with the input."*

> *"This is O(n log k): I run through all n elements, and each heap push/pop is log k because the heap never holds more than k items."*

> *"Worst case the recursion is O(2ⁿ), but with memoization I collapse it to O(n) — each subproblem is solved once and cached."*

**Always give both time *and* space.** Forgetting space is the #1 thing that costs "strong hire" → "hire."

---

## Amortized vs worst case (know the difference)

- **Hash map lookup is O(1) *amortized*** — on average. A pathological set of colliding keys degrades it to O(n). Say "amortized O(1)" and you sound like you know why.
- **Dynamic array append is O(1) amortized** — occasionally it resizes (O(n)), but averaged over many appends it's constant.

---

## The one-liner to remember

> **Constants and lower-order terms drop.** O(2n + 5) is O(n). O(n² + n) is O(n²). Big-O is about *how it grows*, not the exact count.
