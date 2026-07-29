# Longest Line of Consecutive One in Matrix

> **LeetCode:** 562. Longest Line of Consecutive One in Matrix · **Difficulty:** 🟡 Medium · **Pattern:** DP on a grid (4 directions) · **Google frequency:** ⭐ high

---

## Problem

Given a binary matrix `mat` (every cell is `0` or `1`), find the length of the **longest line of consecutive 1s**. A line can run in any of **four** orientations: **horizontal** (→), **vertical** (↓), **diagonal** (↘, down-right), or **anti-diagonal** (↙, down-left). You return a single number — the longest such run anywhere in the grid.

**Example:** `mat = [[0,1,1,0],[0,1,1,0],[0,0,0,1]]` → `3`

```
0 1 1 0
0 1 1 0
0 0 0 1
```

*(The winner is the diagonal `(0,1) → (1,2) → (2,3)` — three 1s stepping down-right. The two little 2×2 blocks of 1s only give runs of length 2 horizontally and vertically; the diagonal sneaks out to that lone `1` in the bottom-right corner.)*

**Constraints that matter:** the grid is up to a few hundred on a side, so `m·n` cells. The naive "stand on each 1 and walk each direction" is `O(m·n·max(m,n))` — fine for small grids, but it re-walks the same segments over and over. The intended answer is a single `O(m·n)` sweep. Nothing here needs recursion or a visited set; it's pure tabulation.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** stand on every `1`, and from there walk right, walk down, walk down-right, walk down-left, counting 1s until you hit a `0` or the edge. Take the longest walk you ever measured. That's completely correct — and it's the brute force.
- **Where it hurts:** watch what happens on a long horizontal band of 1s. Standing on the first cell, you walk the whole band. Standing on the *second* cell, you walk almost the whole band **again**. Every cell re-measures the tail that the cell before it already measured. You're recomputing the same runs `O(max(m,n))` times.
- **The leap:** flip the question. Instead of *"how far can I walk from here?"*, ask *"how long is the run that **ends** right here?"* And that has a one-step answer: the horizontal run ending at `(i,j)` is just *the horizontal run ending at my left neighbor, plus one*. Same for the other three directions — each looks at exactly **one** already-computed neighbor. No walking. Each cell does `O(1)` work.
- **Pattern trigger:** **"longest run / streak ending at each position"** → **DP where `dp[cell]` extends `dp[previous cell]`**. The transferable move is the direction flip: a "reach" that costs a walk becomes a "run ending here" that costs one lookup. Because there are four independent orientations, we carry **four** separate DP values per cell — one per direction — and they never interfere.

---

## ① Brute Force

Stand on each `1`; from there, walk in all four directions until you fall off a 1 or off the grid; track the longest walk.

```python
def longest_line_brute(mat):
    if not mat or not mat[0]:
        return 0
    m, n = len(mat), len(mat[0])
    # right, down, down-right, down-left — the four line orientations
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    best = 0
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                continue
            for dx, dy in dirs:
                length = 0
                x, y = i, j
                # walk while we're on the grid AND still on a 1
                while 0 <= x < m and 0 <= y < n and mat[x][y] == 1:
                    length += 1
                    x += dx
                    y += dy
                best = max(best, length)
    return best
```

**Why it's the natural first attempt:** it's literally the definition of the problem acted out — pick a start, follow the line, measure it.

**Why it's not enough:** it re-measures shared tails. On a solid row of `k` ones, the horizontal walk from cell 0 is length `k`, from cell 1 is `k−1`, from cell 2 is `k−2`… you re-scan the same run again and again. Each of the `m·n` cells can walk up to `max(m, n)` steps, so it's `O(m·n·max(m,n))`. Correct, but wasteful — and the waste is exactly the kind an interviewer will poke at.

**Complexity:** Time `O(m·n·max(m,n))`, Space `O(1)`.

---

## ② Optimised Solution

Flip "how far can I reach" into "how long is the run **ending** here." For each cell, keep **four** running lengths — horizontal, vertical, diagonal (↘), anti-diagonal (↙) — and each one just extends the matching neighbor by 1.

```python
def longest_line(mat):
    if not mat or not mat[0]:
        return 0
    m, n = len(mat), len(mat[0])
    # dp[i][j] = [horiz, vert, diag ↘, anti ↙] run lengths ENDING at (i, j)
    dp = [[[0, 0, 0, 0] for _ in range(n)] for _ in range(m)]
    best = 0
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                continue            # a 0 breaks every line → all four stay 0
            # horizontal: extend the run ending at my LEFT neighbor
            dp[i][j][0] = (dp[i][j - 1][0] if j > 0 else 0) + 1
            # vertical: extend the run ending ABOVE me
            dp[i][j][1] = (dp[i - 1][j][1] if i > 0 else 0) + 1
            # diagonal ↘: extend the run ending UP-LEFT of me
            dp[i][j][2] = (dp[i - 1][j - 1][2] if i > 0 and j > 0 else 0) + 1
            # anti-diagonal ↙: extend the run ending UP-RIGHT of me  (note j+1!)
            dp[i][j][3] = (dp[i - 1][j + 1][3] if i > 0 and j < n - 1 else 0) + 1
            best = max(best, dp[i][j][0], dp[i][j][1], dp[i][j][2], dp[i][j][3])
    return best
```

**Walk the example** `mat = [[0,1,1,0],[0,1,1,0],[0,0,0,1]]`. We sweep left-to-right, top-to-bottom. Below, each populated cell shows `[H, V, ↘, ↙]`; `0` cells reset to `[0,0,0,0]`.

| Cell | `mat` | H (left+1) | V (up+1) | ↘ (up-left+1) | ↙ (up-right+1) | note |
|---|---|---|---|---|---|---|
| (0,1) | 1 | 1 | 1 | 1 | 1 | top-left corner of the block |
| (0,2) | 1 | 2 | 1 | 1 | 1 | H extends `(0,1)` |
| (1,1) | 1 | 1 | 2 | 1 | **2** | ↙ reads `(0,2)`'s ↙ = 1, +1 |
| (1,2) | 1 | 2 | 2 | **2** | 1 | ↘ reads `(0,1)`'s ↘ = 1, +1 |
| (2,3) | 1 | 1 | 1 | **3** | 1 | ↘ reads `(1,2)`'s ↘ = 2, **+1 → 3** |

The running `best` climbs 1 → 2 → **3** and lands on that `dp[2][3][2] = 3`. That's the diagonal `(0,1) → (1,2) → (2,3)`. ✅

**Why it's correct:** each direction's recurrence is exact. A run of 1s ending at `(i,j)` in a given orientation is, by definition, one longer than the run ending at the single predecessor cell in that orientation — *provided* `(i,j)` itself is a 1. If `mat[i][j]` is `0`, no line can pass through it, so all four values are `0` and any future cell that leans on this one restarts from scratch. Because we sweep top-to-bottom, left-to-right, every predecessor (`left`, `up`, `up-left`, `up-right`) is **already computed** before we need it — including the up-right cell for the anti-diagonal, which lives in the row above. We never miss a line because every line has a unique "last" cell, and that cell's four values capture the line's full length.

**Complexity:** Time `O(m·n)` — one `O(1)` visit per cell. Space `O(m·n)` for the DP table.

---

## ③ Space Optimization

**Yes — we can drop to `O(n)`.** Look at what each recurrence reads: horizontal reads the **current** row (left neighbor); vertical, diagonal, and anti-diagonal all read the **row directly above**. Nothing ever reaches back two rows. So we only need the **previous row** and the **current row** — two rows of `n` cells, each holding the four values. Roll them as we descend.

```python
def longest_line_space(mat):
    if not mat or not mat[0]:
        return 0
    m, n = len(mat), len(mat[0])
    prev = [[0, 0, 0, 0] for _ in range(n)]   # row i-1
    best = 0
    for i in range(m):
        curr = [[0, 0, 0, 0] for _ in range(n)]   # row i, fresh (0s = line broken)
        for j in range(n):
            if mat[i][j] == 1:
                curr[j][0] = (curr[j - 1][0] if j > 0 else 0) + 1     # H ← left (this row)
                curr[j][1] = prev[j][1] + 1                           # V ← above
                curr[j][2] = (prev[j - 1][2] if j > 0 else 0) + 1     # ↘ ← up-left
                curr[j][3] = (prev[j + 1][3] if j < n - 1 else 0) + 1 # ↙ ← up-right
                best = max(best, max(curr[j]))
        prev = curr   # descend one row
    return best
```

**Complexity:** Time `O(m·n)`, Space `O(n)` — two rolling rows instead of the full `m·n` table.

> Say it out loud: *"Every recurrence only reaches into the current row or the one right above it — never two rows back — so I keep just a previous row and a current row and roll them down. That's O(n) space instead of O(m·n), same O(m·n) time."* Spotting that the dependency depth is exactly one row is the strong-hire move.

---

## Java (for Java interviewers)

```java
public int longestLine(int[][] mat) {
    if (mat.length == 0 || mat[0].length == 0) return 0;
    int m = mat.length, n = mat[0].length;
    // dp[i][j][d]: d = 0 horiz, 1 vert, 2 diag ↘, 3 anti ↙ — run ending at (i,j)
    int[][][] dp = new int[m][n][4];
    int best = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (mat[i][j] == 0) continue;                 // 0 breaks all four lines
            dp[i][j][0] = (j > 0 ? dp[i][j - 1][0] : 0) + 1;               // left
            dp[i][j][1] = (i > 0 ? dp[i - 1][j][1] : 0) + 1;               // above
            dp[i][j][2] = (i > 0 && j > 0 ? dp[i - 1][j - 1][2] : 0) + 1;  // up-left
            dp[i][j][3] = (i > 0 && j < n - 1 ? dp[i - 1][j + 1][3] : 0) + 1; // up-right
            best = Math.max(best, Math.max(Math.max(dp[i][j][0], dp[i][j][1]),
                                           Math.max(dp[i][j][2], dp[i][j][3])));
        }
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (walk 4 directions from each cell) | O(m·n·max(m,n)) | O(1) |
| Optimised (4-layer DP table) | O(m·n) | O(m·n) |
| Space-optimised (two rolling rows) | O(m·n) | O(n) |

---

## Say it out loud (interview narration)

> *"The brute force is to stand on every 1 and walk all four line directions — horizontal, vertical, and both diagonals — measuring each run. That's O(m·n·max(m,n)), and it re-measures the same tails over and over. So I'll flip it: instead of 'how far can I reach,' I compute 'how long is the run ending at this cell' for each of the four directions. Each one just extends a single already-computed neighbor by one — left for horizontal, above for vertical, up-left for the down-right diagonal, and up-right for the anti-diagonal. A 0 resets all four. One sweep, O(1) per cell, so O(m·n) time. And since every recurrence only touches the current row or the row above, I can roll two rows and get O(n) space."*

The one clarifying question worth asking up front: *"By 'line' we mean all four orientations — horizontal, vertical, and both diagonals — and consecutive means no gaps, right?"* Pinning that down before you code is exactly the kind of narration Google's rubric rewards.

## Related / follow-ups
- **Maximal Square (LC 221)** — same "run/size ending at each cell" DP, but the value is the largest all-1 square, taking a `min` of three neighbors.
- **Maximal Rectangle (LC 85)** — the harder cousin; per-column heights fed into a largest-rectangle-in-histogram sweep.
- **Count Square Submatrices with All Ones (LC 1277)** — identical DP recurrence to Maximal Square, but you sum instead of max.
- **Longest Increasing Path in a Matrix (LC 329)** — the DFS-plus-memo grid cousin, when the transition isn't a fixed direction but "any bigger neighbor."
