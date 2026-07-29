# Edit Distance

> **LeetCode:** 72. Edit Distance · **Difficulty:** 🔴 Hard · **Pattern:** Dynamic Programming (2-D grid) · **Google frequency:** ⭐ high

---

## Problem

Given two strings `word1` and `word2`, return the **minimum number of operations** to convert `word1` into `word2`. Allowed operations, each costing 1: **insert** a character, **delete** a character, **replace** a character.

**Example:** `word1 = "horse"`, `word2 = "ros"` → `3`.
`horse → rorse` (replace h→r) `→ rose` (delete r) `→ ros` (delete e).

**Example:** `word1 = "intention"`, `word2 = "execution"` → `5`.

**Constraints that matter:** `0 ≤ word1.length, word2.length ≤ 500`. An `O(m·n)` grid (~250k cells) is the target. This is the canonical **Levenshtein distance**.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision at the ends.** Look at the last characters of the two prefixes `word1[:i]` and `word2[:j]`:
- If `word1[i-1] == word2[j-1]`: the tails already agree — no cost, just recurse on both shorter prefixes: `dp[i-1][j-1]`.
- If they differ, you must spend one operation, and there are exactly three ways to fix the tail:
  - **Replace** `word1[i-1]` with `word2[j-1]`: `1 + dp[i-1][j-1]`.
  - **Delete** `word1[i-1]`: `1 + dp[i-1][j]`.
  - **Insert** `word2[j-1]` into `word1`: `1 + dp[i][j-1]`.
  Take the cheapest of the three.

> **dp[i][j]** = `dp[i-1][j-1]` if last chars match, else `1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])`.

**(b) Overlapping subproblems.** State is `(i, j)` — a grid of `m·n` prefix pairs. The three-way branch revisits the same `(i, j)` exponentially. DP signal.

**(c) Memoize** on `(i, j)` → `O(m·n)` states.

**(d) Bottom-up grid.** The base cases are meaningful here: converting a length-`i` string to `""` costs `i` **deletes**, and `""` to length-`j` costs `j` **inserts**. So `dp[i][0] = i` and `dp[0][j] = j` — the first row and column are `0,1,2,3,…`. Fill the rest with the recurrence.

**(e) Space — collapse to two rows (key skill).** Each cell reads only the diagonal, up, and left neighbours — all in the current or previous row. So keep the previous row plus the cell to the left; `O(m·n)` → `O(n)` space.

**State & recurrence (memorize this):**
- **State:** `dp[i][j]` = min edits to turn `word1[:i]` into `word2[:j]`.
- **Recurrence:** match → `dp[i-1][j-1]`; else `1 + min(replace dp[i-1][j-1], delete dp[i-1][j], insert dp[i][j-1])`.
- **Base:** `dp[i][0] = i`, `dp[0][j] = j`.

---

## ① Brute Force

Recurse on the two prefix lengths, branching three ways on a mismatch, no caching.

```python
def edit_brute(word1, word2):
    def helper(i, j):
        if i == 0:
            return j          # insert the remaining j chars
        if j == 0:
            return i          # delete the remaining i chars
        if word1[i - 1] == word2[j - 1]:
            return helper(i - 1, j - 1)
        return 1 + min(
            helper(i - 1, j - 1),   # replace
            helper(i - 1, j),       # delete
            helper(i, j - 1),       # insert
        )
    return helper(len(word1), len(word2))
```

**Why it's the natural first attempt:** it enumerates the three edit choices at each mismatched tail — a direct translation of the operations.

**Why it's not enough:** three-way branching to depth `m+n` is exponential, recomputing the same `(i, j)` prefixes over and over.

**Complexity:** Time `O(3^(m+n))`, Space `O(m + n)` (stack).

---

## ② Optimised Solution — 2-D grid

```python
def edit_2d(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i          # delete all i chars
    for j in range(n + 1):
        dp[0][j] = j          # insert all j chars
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],   # replace
                                   dp[i - 1][j],       # delete
                                   dp[i][j - 1])       # insert
    return dp[m][n]
```

**A small filled grid** for `word1 = "horse"` (rows), `word2 = "ros"` (cols):

| | "" | r | o | s |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| h | 1 | 1 | 2 | 3 |
| o | 2 | 2 | 1 | 2 |
| r | 3 | 2 | 2 | 2 |
| s | 4 | 3 | 3 | 2 |
| e | 5 | 4 | 4 | **3** |

Answer `dp[5][3] = 3`. ✅ (First row/column are pure insert/delete costs; matches copy the diagonal, mismatches add 1 to the best neighbour.)

**Why it's correct:** the three operations plus "chars already match" are the only ways to reconcile the tails, each reducing to a strictly smaller, already-optimal subproblem. The min preserves optimality.

**Complexity:** Time `O(m·n)`, Space `O(m·n)`.

---

## ③ Space Optimization — two rows

**The key DP skill.** Each cell needs `dp[i-1][j-1]` (diagonal), `dp[i-1][j]` (up), `dp[i][j-1]` (left) — all in the previous or current row. Keep two rows:

```python
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))            # dp[0][j] = j
    for i in range(1, m + 1):
        curr = [i] + [0] * n             # curr[0] = dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]                # diagonal, no cost
            else:
                curr[j] = 1 + min(prev[j - 1],       # replace (diagonal)
                                  prev[j],           # delete (up)
                                  curr[j - 1])       # insert (left)
        prev = curr
    return prev[n]
```

`prev` holds row `i-1`; `curr[j-1]` is the just-computed left neighbour. `O(m·n)` → `O(n)` space.

**Complexity:** Time `O(m·n)`, Space `O(min(m, n))` (swap so `word2` is the shorter to size the rows).

> Can be pushed to one row plus a scalar for the diagonal, but the two-row form is the safe interview default — obviously correct, same asymptotic cost.

---

## Java (for Java interviewers)

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[] prev = new int[n + 1];
    for (int j = 0; j <= n; j++) prev[j] = j;
    for (int i = 1; i <= m; i++) {
        int[] curr = new int[n + 1];
        curr[0] = i;
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = 1 + Math.min(prev[j - 1], Math.min(prev[j], curr[j - 1]));
            }
        }
        prev = curr;
    }
    return prev[n];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recursion) | O(3^(m+n)) | O(m + n) |
| Memoized (top-down) | O(m·n) | O(m·n) |
| Tabulated 2-D grid | O(m·n) | O(m·n) |
| Space-optimised (two rows) | O(m·n) | O(min(m, n)) |

---

## Say it out loud (interview narration)

> *"I define dp[i][j] as the min edits to turn the first i chars of word1 into the first j of word2. If the tail characters match, I inherit the diagonal for free; otherwise I pay 1 and take the cheapest of replace (diagonal), delete (up), or insert (left). The base cases are the first row and column — converting to or from an empty string costs its length. That's an O(m·n) grid, and since each cell only touches the previous row and the left cell, I roll it down to O(n) space."*

## Related / follow-ups
- **Longest Common Subsequence** (same grid; delete+insert only, maximize instead of minimize)
- **Delete Operation for Two Strings** (only delete allowed → m + n − 2·LCS)
- **One Edit Distance** (single-pass check for distance exactly 1)
- **Minimum ASCII Delete Sum** (weighted deletes by character value)
