# Unique Paths

> **LeetCode:** 62. Unique Paths · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming (grid) · **Google frequency:** ⭐ high

---

## Problem

A robot sits at the **top-left** of an `m × n` grid and wants to reach the **bottom-right**. It can only move **right** or **down**. How many distinct paths are there?

**Example:** `m = 3`, `n = 7` → `28`.

**Example:** `m = 3`, `n = 2` → `3`. The paths: Down-Down-Right, Down-Right-Down, Right-Down-Down.

**Constraints that matter:** `1 ≤ m, n ≤ 100`, and the answer fits in a 32-bit int. `O(m·n)` DP is easy and clean; the space follow-up (1-D rolling row) is the interesting part.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision at each cell.** Stand on the destination cell `(i, j)`. How did the robot arrive? Only two possibilities: it stepped **down** from `(i-1, j)`, or **right** from `(i, j-1)`. Those are the only legal incoming moves. Every path into `(i, j)` came through exactly one of them, and the two sets are disjoint. So:

> **paths(i, j) = paths(i-1, j) + paths(i, j-1)**

Base: the entire **top row** and **left column** have exactly **1** path each (you can only go straight along the edge). `paths(0, j) = paths(i, 0) = 1`.

**(b) Overlapping subproblems.** Recursing `paths(i,j)` re-derives `paths(i-1, j-1)` from both the "down then" and "right then" branches — the same cells recompute exponentially. DP signal (this is a 2-D Fibonacci/Pascal's triangle).

**(c) Memoize** on `(i, j)` → `m·n` states.

**(d) Bottom-up grid.** Fill `dp[i][j]` row by row, first row and column set to 1, interior `= dp[i-1][j] + dp[i][j-1]`.

**(e) Space — collapse to one row (key skill).** When you compute row `i` left to right, `dp[i][j]` needs `dp[i-1][j]` (the value currently in the row array *before* you overwrite it) and `dp[i][j-1]` (the value you *just wrote* to the left). Both live in a **single 1-D array** if you update it in place. `O(m·n)` → `O(n)` space.

**State & recurrence (memorize this):**
- **State:** `dp[i][j]` = number of distinct paths from `(0,0)` to `(i,j)`.
- **Recurrence:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
- **Base:** `dp[0][j] = dp[i][0] = 1`.

*(Closed form: it's `C(m+n-2, m-1)` — but the DP is what interviewers want to see.)*

---

## ① Brute Force

Recurse the two moves from the start, counting paths that reach the goal.

```python
def unique_paths_brute(m, n):
    def helper(i, j):
        if i == m - 1 and j == n - 1:
            return 1
        if i >= m or j >= n:
            return 0
        return helper(i + 1, j) + helper(i, j + 1)   # down + right
    return helper(0, 0)
```

**Why it's the natural first attempt:** it literally explores every right/down move sequence to the corner.

**Why it's not enough:** the number of paths is exponential and the recursion recomputes each cell's count many times — ~`O(2^(m+n))` calls.

**Complexity:** Time `O(2^(m+n))`, Space `O(m + n)` (stack).

---

## ② Optimised Solution — 2-D grid

```python
def unique_paths_2d(m, n):
    dp = [[1] * n for _ in range(m)]      # top row & left col already 1
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

**A small filled grid** for `m = 3`, `n = 7`:

| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 1 | 3 | 6 | 10 | 15 | 21 | **28** |

Each interior cell is up + left. Bottom-right `= 28`. ✅

**Why it's correct:** every path into a cell arrives from above or from the left, disjoint and exhaustive, so summing the two source counts counts each path exactly once.

**Complexity:** Time `O(m·n)`, Space `O(m·n)`.

---

## ③ Space Optimization — rolling 1-D row

**The key DP skill.** Keep one row of length `n`. Processing rows top to bottom, when you reach column `j`, `dp[j]` still holds the value from the row above (that's the "up" neighbour), and `dp[j-1]` was just updated (the "left" neighbour). Update in place:

```python
def unique_paths(m, n):
    dp = [1] * n                      # top row: all 1s
    for _ in range(1, m):             # each subsequent row
        for j in range(1, n):
            dp[j] += dp[j - 1]        # dp[j](up) + dp[j-1](left)
    return dp[-1]
```

Row evolution for `m=3, n=7`: `[1,1,1,1,1,1,1] → [1,2,3,4,5,6,7] → [1,3,6,10,15,21,28]`. Return `28`. ✅

**Complexity:** Time `O(m·n)`, Space `O(n)` (use `min(m, n)` by orienting the shorter dimension as the row).

> `dp[j] += dp[j-1]` quietly does the whole recurrence: the `dp[j]` on the right is the old (upper) value, `dp[j-1]` is the freshly written left value. Recognizing that an in-place `+=` encodes "up + left" is the elegant move.

---

## Java (for Java interviewers)

```java
public int uniquePaths(int m, int n) {
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] += dp[j - 1];       // up + left
        }
    }
    return dp[n - 1];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recursion) | O(2^(m+n)) | O(m + n) |
| Memoized (top-down) | O(m·n) | O(m·n) |
| Tabulated 2-D grid | O(m·n) | O(m·n) |
| Space-optimised (rolling row) | O(m·n) | O(min(m, n)) |

---

## Say it out loud (interview narration)

> *"Any cell is reached only from above or from the left, so paths(i,j) = paths(i-1,j) + paths(i,j-1), with the top row and left column all 1. That's an O(m·n) grid. But when I fill row by row left to right, the value already in my array is the cell above and the value just to my left is the left neighbour — so I collapse it to a single row and do dp[j] += dp[j-1], O(n) space. There's also a closed form, C(m+n-2, m-1), if they want it."*

## Related / follow-ups
- **Unique Paths II** (obstacles — set blocked cells to 0)
- **Minimum Path Sum** (same grid, min of up/left plus cell cost instead of a count)
- **Unique Paths III** (must cover every cell — backtracking, not DP)
- **Dungeon Game** (grid DP filled from bottom-right with a health constraint)
