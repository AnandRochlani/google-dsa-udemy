# Maximum Number of Points with Cost

> **LeetCode:** 1937. Maximum Number of Points with Cost · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming / row DP + directional prefix-max sweeps · **Google frequency:** ⭐ high

*This problem opens the Dynamic Programming block of the course — and it's the perfect gatekeeper. It's not "can you write a DP?" (the row DP is easy); it's "can you make a DP transition **fast enough**?" That second question is where Google separates candidates, and it's the theme of this whole section.*

---

## Problem

You're given an `m × n` integer matrix `points`. You must pick **exactly one cell from every row**, and your score is the sum of the picked cells — minus a penalty: for every pair of adjacent rows, if you pick column `c1` in row `r` and column `c2` in row `r + 1`, you pay `|c1 - c2|`. Maximize the final score.

**Example:** `points = [[1,2,3],[1,5,1],[3,1,1]]` → `9` *(pick 2 (row 0, col 1) + 5 (row 1, col 1) + 3 (row 2, col 0); penalties |1−1| + |1−0| = 1; total 2+5+3−1 = 9)*

**Constraints that matter:** `m, n ≤ 10^5` but `m · n ≤ 10^5`. That product is the tell. The natural row DP compares every column of one row against every column of the previous row — `O(n²)` per row, `O(m · n²)` total. With `m·n = 10^5` and a wide matrix (say `m = 1`... no, say `m = 10, n = 10^4`), that's `10 · 10^8 = 10^9` operations — dead on arrival. The transition itself has to become `O(n)`, for `O(m · n)` total. Also note `points[r][c] ≤ 10^5`, so the best score can reach `10^5 · 10^5 = 10^10` — **overflows a 32-bit int; use `long` in Java**.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** classic row-by-row DP. Define `dp[r][c]` = best score achievable if the row-`r` pick is column `c`. Then `dp[r][c] = points[r][c] + max over all c' of (dp[r-1][c'] - |c - c'|)`, and the answer is the max of the last row. This is *correct* — say it out loud, it's real progress. But that inner `max` scans all `n` columns for each of the `n` cells: `O(n²)` per row.
- **Where it hurts:** for two neighboring cells `c` and `c+1`, those two `O(n)` scans look at almost exactly the same values — each candidate `dp[r-1][c']` just contributes one more or one less penalty unit. We're recomputing nearly identical maxima `n` times per row. That's the wasted work.
- **The leap:** kill the absolute value. `|c - c'|` is hiding two clean cases: if the previous pick is **at or to the left** (`c' ≤ c`), the penalty is `c - c'`, so the candidate is `(dp[r-1][c'] + c') - c`; if it's **at or to the right**, the candidate is `(dp[r-1][c'] - c') + c`. In each case the parenthesized part **doesn't depend on `c`** — so the best left-side candidate for every `c` is a running prefix max swept left-to-right, and the best right-side candidate is a running suffix max swept right-to-left. Even cleaner: think of it as the best value "walking" toward you, paying 1 per step — `left[c] = max(left[c-1] - 1, prev[c])`. Two `O(n)` sweeps replace `n` scans.
- **Pattern trigger:** **an absolute-value distance penalty inside a DP transition → split it into two directional prefix sweeps.** `|c - c'|` always splits into a `c' ≤ c` case and a `c' ≥ c` case, and each side collapses into a running max. This is the transferable move — the same trick reappears whenever a transition says "take the best previous state, minus how far away it is."

---

## ① Brute Force

The honest row DP: for each cell, scan every column of the previous row to find the best predecessor after the distance penalty.

```python
def maxPoints_brute(points):
    m, n = len(points), len(points[0])
    dp = points[0][:]                       # best totals ending in row 0
    for r in range(1, m):
        new_dp = [0] * n
        for c in range(n):                  # for every cell in this row...
            new_dp[c] = points[r][c] + max( # ...scan ALL previous columns
                dp[pc] - abs(c - pc) for pc in range(n)
            )
        dp = new_dp
    return max(dp)
```

**Why it's the natural first attempt:** it's the textbook DP translation of the problem — "best way to be *here* = my value + best way to have been *anywhere* in the previous row, minus the travel cost." Nothing about it is wrong.

**Why it's not enough:** the inner `max` makes the transition `O(n)` per cell, so each row costs `O(n²)` and the whole thing is `O(m · n²)`. With `m·n ≤ 10^5` a wide matrix like `10 × 10^4` blows this up to ~10^9 operations — Time Limit Exceeded. The waste is concrete: the scans for columns `c` and `c+1` cover the same candidates with penalties that differ by exactly 1. We keep re-deriving almost-identical maxima.

**Complexity:** Time `O(m · n²)`, Space `O(n)`.

---

## ② Optimised Solution

Same DP states — but the transition drops to `O(1)` per cell via two directional sweeps over the previous row. `left[c]` = the best a predecessor from the left (or directly above) can deliver *to* column `c` after paying its walk; `right[c]` = the same from the right. Each is a running max that "decays" by 1 per step it travels.

```python
def maxPoints(points):
    m, n = len(points), len(points[0])
    dp = [[0] * n for _ in range(m)]
    dp[0] = points[0][:]                       # row 0: no penalty yet

    for r in range(1, m):
        prev = dp[r - 1]

        # left[c] = best of (prev[j] - (c - j)) for all j <= c
        left = [0] * n
        left[0] = prev[0]
        for c in range(1, n):
            left[c] = max(left[c - 1] - 1, prev[c])   # carried value fades by 1 per step

        # right[c] = best of (prev[j] - (j - c)) for all j >= c
        right = [0] * n
        right[n - 1] = prev[n - 1]
        for c in range(n - 2, -1, -1):
            right[c] = max(right[c + 1] - 1, prev[c])

        for c in range(n):
            dp[r][c] = points[r][c] + max(left[c], right[c])

    return max(dp[m - 1])
```

**Walk one example** — `points = [[1,2,3],[1,5,1],[3,1,1]]`:

| Step | left sweep | right sweep | dp row |
|---|---|---|---|
| Row 0 | — | — | `[1, 2, 3]` |
| Row 1 (prev `[1,2,3]`) | `[1, max(0,2)=2, max(1,3)=3]` | `[max(1,1)=1, max(2,2)=2, 3]` | `1+1, 5+2, 1+3` → `[2, 7, 4]` |
| Row 2 (prev `[2,7,4]`) | `[2, max(1,7)=7, max(6,4)=6]` | `[max(6,2)=6, max(3,7)=7, 4]` | `3+6, 1+7, 1+6` → `[9, 8, 7]` |

Answer: `max([9, 8, 7]) = 9`. ✅ And you can *see* the trick working in row 2, column 0: the `7` sitting at column 1 walks one step left, decays to `6`, and delivers `3 + 6 = 9` — no scan needed.

**Why it's correct:** unrolling the recurrence, `left[c] = max(left[c-1] - 1, prev[c]) = max over j ≤ c of (prev[j] - (c - j))` — every candidate at distance `d` has been decremented exactly `d` times by the time the running max reaches `c` (induction on `c`). Symmetrically `right[c] = max over j ≥ c of (prev[j] - (j - c))`. Their max is exactly `max over all j of (prev[j] - |c - j|)` — the brute-force inner loop, with the `j = c` case covered by both sweeps. Same DP, identical values, just computed without re-scanning.

**Complexity:** Time `O(m · n)` — three linear passes per row. Space `O(m · n)` for the full table.

---

## ③ Space Optimization

The transition only ever reads the **previous row**, so the 2-D table is dead weight — keep one rolling 1-D row plus the two sweep arrays.

```python
def maxPoints(points):
    n = len(points[0])
    prev = points[0][:]                        # rolling: only the last row's totals
    for row in points[1:]:
        left = [0] * n
        left[0] = prev[0]
        for c in range(1, n):
            left[c] = max(left[c - 1] - 1, prev[c])
        right = [0] * n
        right[n - 1] = prev[n - 1]
        for c in range(n - 2, -1, -1):
            right[c] = max(right[c + 1] - 1, prev[c])
        prev = [row[c] + max(left[c], right[c]) for c in range(n)]
    return max(prev)
```

**Complexity:** Time `O(m · n)`, Space `O(n)`.

> Can we go below `O(n)`? No — and say why: each new row needs the best delivered value **at every one of the `n` columns**, and those `n` values are all distinct pieces of state. `O(n)` is the floor for this transition; the win was cutting `O(m·n)` down to `O(n)`, the classic rolling-row move you'll reuse all through this DP section.

---

## Java (for Java interviewers)

One trap Java makes explicit: totals reach `10^5 rows × 10^5 per cell = 10^10` — **`long`, not `int`**. (LeetCode's signature returns `long maxPoints(int[][] points)` for exactly this reason.)

```java
public long maxPoints(int[][] points) {
    int n = points[0].length;
    long[] prev = new long[n];                 // rolling: previous row's best totals
    for (int c = 0; c < n; c++) prev[c] = points[0][c];

    long[] left = new long[n];
    long[] right = new long[n];
    for (int r = 1; r < points.length; r++) {
        // left[c] = best of (prev[j] - (c - j)) for j <= c
        left[0] = prev[0];
        for (int c = 1; c < n; c++)
            left[c] = Math.max(left[c - 1] - 1, prev[c]);

        // right[c] = best of (prev[j] - (j - c)) for j >= c
        right[n - 1] = prev[n - 1];
        for (int c = n - 2; c >= 0; c--)
            right[c] = Math.max(right[c + 1] - 1, prev[c]);

        long[] cur = new long[n];
        for (int c = 0; c < n; c++)
            cur[c] = points[r][c] + Math.max(left[c], right[c]);
        prev = cur;
    }

    long best = 0;
    for (long v : prev) best = Math.max(best, v);
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (scan all prev columns) | O(m · n²) | O(n) |
| Optimised (two prefix sweeps, full table) | O(m · n) | O(m · n) |
| Space-optimised (rolling row) | O(m · n) | O(n) |

*(m rows, n columns, m · n ≤ 10^5.)*

---

## Say it out loud (interview narration)

> *"This is a row DP: `dp[r][c]` is the best total if my row-`r` pick is column `c`, and the transition is the best previous cell minus the column distance. Naively that transition scans all `n` previous columns per cell — `O(m·n²)`, which the `m·n ≤ 10^5` constraint is designed to kill. So I split the absolute value: a predecessor to my left contributes `dp[r-1][c'] + c'` minus my `c`, one to my right contributes `dp[r-1][c'] - c'` plus my `c` — and neither parenthesized term depends on me. That means one left-to-right running max and one right-to-left running max hand every cell its best predecessor in `O(1)`: I picture the previous row's values walking toward each column, fading by one per step. Total `O(m·n)` time; I only ever read the previous row, so space rolls down to `O(n)`. One more thing — values times rows can hit `10^10`, so in Java this must be a `long`."*

Before you code, ask the clarifying question that proves you read the spec: *"The penalty applies between every pair of **adjacent** rows only, right — nothing between row 0 and row 2 directly?"* Cheap to ask, and it locks the DP structure before you commit.

## Related / follow-ups

- **Minimum Falling Path Sum (LC 931)** — same row-to-row DP shape, but the reach is only 3 neighbors, so no sweep trick is needed. Do it as the warm-up.
- **Minimum Falling Path Sum II (LC 1289)** — transition over *all* columns again; there the trick is tracking the top-2 minima of the previous row. Same disease ("O(n²) transition"), different cure.
- **Paint House II (LC 265)** — the classic top-2-minima transition compression; pairs beautifully with this problem's sweep compression.
- **Sliding-window-max DP (e.g. LC 1696 Jump Game VI)** — when the penalty is a *range cap* instead of a linear decay, the same "speed up the transition" instinct reaches for a monotonic deque instead of prefix sweeps.
