# Longest Increasing Path in a Matrix

> **LeetCode:** 329. Longest Increasing Path in a Matrix · **Difficulty:** 🔴 Hard · **Pattern:** DFS + Memoization (DP on a grid) · **Google frequency:** ⭐ high

---

## Problem

Given an `m × n` grid of integers, find the length of the **longest strictly increasing path**. From any cell you may move **up, down, left, or right** (no diagonals, no wrapping). You may **not** revisit a cell, and each step must go to a **strictly larger** value.

Return the number of cells on that longest path.

**Example:**

```
9 9 4
6 6 8
2 1 1
```

`→ 4` *(the path `1 → 2 → 6 → 9`: start at the `1` in the bottom row, step up-and-left to `2`, then to `6`, then to `9`).*

**Constraints that matter:** `m` and `n` can each be up to ~200, so the grid has up to ~40,000 cells. A naive DFS that re-explores paths is **exponential** and blows up instantly. We need something that touches each cell a small, bounded number of times — an `O(m·n)` algorithm.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "The longest path could start anywhere, so let me DFS from every cell, walking to bigger neighbors, and track the deepest walk." That's the honest brute force — and it's correct. It's just wildly wasteful.
- **Where it hurts:** Different starting cells keep walking into the **same** shared tails. The best path out of cell `6` is the same *every single time* you arrive at that `6` — but plain DFS recomputes it from scratch on every visit. You're re-answering a question you already answered.
- **The leap:** Define one clean subproblem — `best(r, c)` = the length of the longest increasing path that **starts** at cell `(r, c)`. It only depends on `best(...)` of its strictly-larger neighbors. So compute it once and **cache it**. That's memoization: the second time anyone asks for `best(6's cell)`, we hand back the stored number in O(1).
- **Why the cache is safe (the key insight):** every edge goes from a smaller value to a **strictly larger** one. You can never step back down, so you can **never form a cycle**. The grid, viewed as "cell → larger neighbor," is a **DAG** (directed acyclic graph). No cycles means the recursion always bottoms out, and a memo entry, once written, is final — **you never need a visited-set**.
- **Pattern trigger:** **"longest path" + "on a grid" + "strictly monotonic moves"** → the moves impose a DAG, and *longest path on a DAG* = **DFS + memoization** (equivalently, DP over the cells in value order).

---

## ① Brute Force

DFS from every cell, walking to any strictly-larger neighbor, and take the deepest walk. No cache.

```python
def longest_path_brute(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])

    def dfs(r, c):
        best = 1  # the cell itself is a path of length 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

**Why it's the natural first attempt:** it's the literal reading of the problem — "try every path from every start, keep the longest."

**Why it's not enough:** the same sub-path gets recomputed over and over. On a grid that increases smoothly (imagine values snaking upward), the number of distinct partial paths explodes — the work is **exponential**. Fine on a 3×3 toy; hopeless on 200×200.

**Complexity:** Time `O(exponential)`, Space `O(m·n)` recursion depth.

---

## ② Optimised Solution

Same DFS — but the **first** time we compute `best(r, c)`, we store it. Every later visit reads the cache.

```python
def longest_path(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    memo = [[0] * cols for _ in range(rows)]   # 0 = "not computed yet"

    def dfs(r, c):
        if memo[r][c]:                          # already solved this cell
            return memo[r][c]
        best = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[r][c] = best                       # cache before returning
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

**Walk the example** on:

```
9 9 4
6 6 8
2 1 1
```

Ask for `dfs` on the bottom-left `2` at `(2,0)`. Its only strictly-larger neighbor is the `6` at `(1,0)`. `dfs(6)` looks up — its larger neighbor is the `9` at `(0,0)`. `dfs(9)` has no larger neighbor → `best = 1`, cached. Back at `6`: `1 + 1 = 2`, cached. Back at `2`: `1 + 2 = 3`, cached. Now the `1` at `(2,1)` steps up to that `2` → `1 + 3 = 4`. That's the answer, **4**. Notice the `6`, `9`, and `2` cells were each solved **once**; when other cells reach them, the value is already sitting in `memo`.

**Why it's correct:** `best(r, c)` depends only on cells with **strictly larger** values, and strictly-larger is a partial order with no cycles — so the recursion is well-founded and always terminates. Because a cell's answer never changes once computed, the memo is exact. Taking the `max` over all starting cells gives the global longest path.

**Complexity:** Time `O(m·n)` — each cell's `best` is computed exactly once, and each computation looks at ≤ 4 neighbors, so total work is `O(4·m·n) = O(m·n)`. Space `O(m·n)` for the memo, plus up to `O(m·n)` recursion depth in the worst case.

---

## ③ Space Optimization

The memo is **not** removable here — it's the whole reason we're `O(m·n)` instead of exponential. Every cell's answer is reused by its smaller neighbors, so we genuinely need to remember all `m·n` of them. There's no rolling-row trick like a 1-D DP, because the dependencies point in **all four directions**, not just "the previous row."

> **Say so honestly:** *"Space is `O(m·n)` and that's optimal for this DP — the memo IS the algorithm. I can't roll it down to one row because a cell can depend on neighbors above, below, left, or right, not just the row before it. The only thing I could trim is recursion depth by going iterative (topological order), but the table itself stays `O(m·n)`."*

Naming *why* the space can't shrink is the strong-hire move — it shows you understand the dependency structure, not just the code.

---

## Java (for Java interviewers)

```java
public int longestIncreasingPath(int[][] matrix) {
    if (matrix.length == 0 || matrix[0].length == 0) return 0;
    int rows = matrix.length, cols = matrix[0].length;
    int[][] memo = new int[rows][cols];       // 0 = not computed
    int best = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            best = Math.max(best, dfs(matrix, memo, r, c));
    return best;
}

private static final int[][] DIRS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

private int dfs(int[][] matrix, int[][] memo, int r, int c) {
    if (memo[r][c] != 0) return memo[r][c];
    int rows = matrix.length, cols = matrix[0].length;
    int best = 1;
    for (int[] d : DIRS) {
        int nr = r + d[0], nc = c + d[1];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                && matrix[nr][nc] > matrix[r][c]) {
            best = Math.max(best, 1 + dfs(matrix, memo, nr, nc));
        }
    }
    memo[r][c] = best;
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (DFS, no memo) | O(exponential) | O(m·n) recursion |
| Optimised (DFS + memo) | O(m·n) | O(m·n) |
| Topological / peeling (BFS, Kahn's) | O(m·n) | O(m·n) |

---

## Say it out loud (interview narration)

> *"Brute force is DFS from every cell walking to bigger neighbors — correct but exponential, because it recomputes the same tails again and again. So I define `best(cell)` = longest increasing path starting there, and memoize it. The key observation is that every edge goes to a strictly larger value, so there are no cycles — the grid is a DAG — which means I don't even need a visited set, and each cell is computed exactly once. That's `O(m·n)` time. Space is `O(m·n)` for the memo, and that's optimal because the dependencies point in all four directions, so I can't collapse it to a single row."*

## Related / follow-ups
- **Number of Increasing Paths in a Grid** (LC 2328) — same DAG + memo, but *count* paths instead of finding the longest.
- **Topological-sort variant:** peel the grid layer by layer (Kahn's algorithm / BFS on out-degree) to get the same answer **iteratively** — no recursion stack, so no depth limit. Good to mention when the interviewer worries about very large grids.
- **Course Schedule / Longest Path in a DAG** — the general lesson: strictly-monotonic edges ⇒ DAG ⇒ longest path by DFS+memo or topological DP.
- **Word Search / Number of Islands** — grid DFS cousins (but those *do* need a visited set, because their moves aren't monotonic — a useful contrast).
