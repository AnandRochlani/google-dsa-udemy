# Longest Common Subsequence

> **LeetCode:** 1143. Longest Common Subsequence · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming (2-D grid) · **Google frequency:** ⭐ high

---

## Problem

Given two strings `text1` and `text2`, return the length of their **longest common subsequence** — the longest sequence of characters appearing left-to-right (not necessarily contiguous) in both. Return `0` if there's none.

**Example:** `text1 = "abcde"`, `text2 = "ace"` → `3`. The LCS is `"ace"`.

**Example:** `text1 = "abc"`, `text2 = "def"` → `0`. No common characters.

**Constraints that matter:** `1 ≤ text1.length, text2.length ≤ 1000`. An `O(m·n)` grid (~10⁶ cells) is the target; the exponential "compare all subsequences" approach is hopeless.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision at the ends.** Compare the **last characters** of the two strings (equivalently, walk a pointer `i` in `text1` and `j` in `text2`):
- If `text1[i] == text2[j]`: this character can be the tail of the LCS. Take it and recurse on both prefixes: `1 + LCS(i-1, j-1)`.
- If they differ: at least one of them isn't in the LCS. Try dropping each and keep the better: `max( LCS(i-1, j), LCS(i, j-1) )`.

> **LCS(i, j)** = `1 + LCS(i-1, j-1)` if chars match, else `max(LCS(i-1, j), LCS(i, j-1))`.

Base: if either string is empty, `LCS = 0`.

**(b) Notice overlapping subproblems.** The state is a pair of prefix lengths `(i, j)`. Different match/drop paths revisit the same `(i, j)` constantly — a 2-D grid of only `m·n` distinct states hides behind an exponential recursion. DP signal.

**(c) Memoize on `(i, j)`.** Cache each cell → `O(m·n)` states, each O(1) work.

**(d) Bottom-up table.** Use a grid `dp[i][j]` = LCS of `text1[:i]` and `text2[:j]`, with a zero-filled first row/column (empty-prefix base case). Fill row by row using the recurrence.

**(e) Space — collapse 2-D to two rows, then to one (the key skill).** Each cell `dp[i][j]` reads only the **current row** and the **row directly above** (`dp[i-1][*]`). So you never need the whole grid — keep the previous row and the current row. With a little care (a single scalar holding the "diagonal" value), you can even use **one row**. `O(m·n)` → `O(min(m, n))` space.

**State & recurrence (memorize this):**
- **State:** `dp[i][j]` = length of LCS of the first `i` chars of `text1` and first `j` chars of `text2`.
- **Recurrence:** `dp[i][j] = dp[i-1][j-1] + 1` if `text1[i-1] == text2[j-1]`, else `max(dp[i-1][j], dp[i][j-1])`.
- **Base:** `dp[0][*] = dp[*][0] = 0`.

---

## ① Brute Force

Recurse on the two prefix lengths, matching or dropping ends, no caching.

```python
def lcs_brute(text1, text2):
    def helper(i, j):
        if i == 0 or j == 0:
            return 0
        if text1[i - 1] == text2[j - 1]:
            return 1 + helper(i - 1, j - 1)
        return max(helper(i - 1, j), helper(i, j - 1))
    return helper(len(text1), len(text2))
```

**Why it's the natural first attempt:** it's the "match the tails or drop one" decision written directly.

**Why it's not enough:** on a mismatch it forks into two calls, so the tree is ~`O(2^(m+n))`, recomputing the same `(i, j)` prefixes endlessly.

**Complexity:** Time `O(2^(m+n))`, Space `O(m + n)` (stack).

---

## ② Optimised Solution — 2-D grid

```python
def lcs_2d(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

**A small filled grid** for `text1 = "abcde"` (rows), `text2 = "ace"` (cols):

| | "" | a | c | e |
|---|---|---|---|---|
| "" | 0 | 0 | 0 | 0 |
| a | 0 | **1** | 1 | 1 |
| b | 0 | 1 | 1 | 1 |
| c | 0 | 1 | **2** | 2 |
| d | 0 | 1 | 2 | 2 |
| e | 0 | 1 | 2 | **3** |

Diagonal `+1` on matches (`a`, `c`, `e`); otherwise carry the max of up/left. Answer `dp[5][3] = 3`. ✅

**Why it's correct:** every cell exhausts the only three possibilities — match (take the diagonal + 1) or mismatch (best of dropping one char from either string) — building on already-final smaller prefixes.

**Complexity:** Time `O(m·n)`, Space `O(m·n)`.

---

## ③ Space Optimization — rolling 1-D row

**The key DP skill.** A cell needs only the row above and the cell to its left. Keep just the **previous row** and the **current row** → `O(n)` space. Iterate so the smaller string sizes the array:

```python
def lcs(text1, text2):
    if len(text2) > len(text1):            # make text2 the shorter one
        text1, text2 = text2, text1
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1          # diagonal
            else:
                curr[j] = max(prev[j], curr[j - 1])  # up vs left
        prev = curr
    return prev[n]
```

`prev[j-1]` is the diagonal (old row, previous column), `prev[j]` is directly above, `curr[j-1]` is directly left — exactly the three neighbours the recurrence needs.

**Complexity:** Time `O(m·n)`, Space `O(min(m, n))`.

> Can be squeezed to a **single** row plus one scalar for the diagonal, but two rows is the version worth writing under pressure — it's obviously correct and just as cheap asymptotically.

---

## Java (for Java interviewers)

```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[] prev = new int[n + 1];
    for (int i = 1; i <= m; i++) {
        int[] curr = new int[n + 1];
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                curr[j] = prev[j - 1] + 1;
            } else {
                curr[j] = Math.max(prev[j], curr[j - 1]);
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
| Brute force (recursion) | O(2^(m+n)) | O(m + n) |
| Memoized (top-down) | O(m·n) | O(m·n) |
| Tabulated 2-D grid | O(m·n) | O(m·n) |
| Space-optimised (rolling row) | O(m·n) | O(min(m, n)) |

---

## Say it out loud (interview narration)

> *"I compare the two strings' ends: if the characters match, the LCS is 1 plus the LCS of both prefixes — the diagonal; if they differ, it's the best of dropping one character from either side — up or left. That's a 2-D grid, dp[i][j] over prefix lengths, filled in O(m·n). Since each cell only reads the row above and the cell to its left, I keep just two rows — O(min(m,n)) space instead of the full grid."*

## Related / follow-ups
- **Edit Distance** (same grid, but three ops: insert/delete/replace)
- **Longest Common Substring** (contiguous — reset to 0 on mismatch, track the global max)
- **Shortest Common Supersequence** (m + n − LCS, then reconstruct)
- **Delete Operation for Two Strings** (m + n − 2·LCS)
