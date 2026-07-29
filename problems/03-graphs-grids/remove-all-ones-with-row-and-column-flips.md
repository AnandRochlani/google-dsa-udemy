# Remove All Ones With Row and Column Flips

> **LeetCode:** 2128. Remove All Ones With Row and Column Flips · **Difficulty:** 🟡 Medium · **Pattern:** Invariant / XOR insight · **Google frequency:** ⭐ high

---

## Problem

You're given a binary matrix `grid` (every cell is `0` or `1`). In one operation you pick **an entire row** or **an entire column** and **flip** it — every `0` becomes `1` and every `1` becomes `0`. You may do this **any number of times**, in **any order**, on **any** rows and columns. Return `True` if you can make the whole grid all zeros, `False` otherwise.

**Example:** `grid = [[0,1,0],[1,0,1],[0,1,0]]` → `True` *(flip column 1, then it's all zeros)*

**Example:** `grid = [[1,1,0],[0,0,0],[0,0,0]]` → `False` *(no sequence of full-row/full-column flips clears it)*

**Constraints that matter:** `m, n` up to a few hundred, so `O(m*n)` is the target — but the real constraint is conceptual, not asymptotic. "Any number of operations, any order" is a **huge** search space if you try to simulate it. The unlock is realizing you never have to search at all.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Let me simulate. Try flipping rows and columns until the grid is zero — some kind of BFS/DFS over grid states, or a greedy: flip every row that starts with a 1, then fix up the columns." That greedy feels right for about ten seconds. Then you notice a fix to a column can re-break a row you already cleared, and you're chasing your tail. The state space is `2^(m+n)` combinations of flips — way too big to brute-force blindly.
- **Where it hurts:** the pain is that you're treating flips like a *search problem* when they have far more structure than that. Two facts kill the search. **(1) A flip is its own inverse** — flip the same row twice and you're back where you started. So for each row and each column, the only thing that matters is whether you flip it an **odd** or **even** number of times: one bit. **(2) Order doesn't matter** — flipping row 2 then column 3 lands the exact same cell values as column 3 then row 2, because each cell `grid[i][j]` just gets XOR-ed by `rowFlip[i] XOR colFlip[j]`. Flipping is XOR, and XOR doesn't care about order or repeats.
- **The leap:** so the final value of cell `(i, j)` is `grid[i][j] XOR r[i] XOR c[j]`, where `r[i], c[j]` are single bits (did we flip that row / that column, odd times). We want *every* cell to be `0`. Freeze your attention on **row 0**. Whatever column-flip pattern `c[0..n-1]` we choose, it's forced to turn row 0 into zeros: `c[j] = grid[0][j]` (flip exactly the columns where row 0 has a 1). That column pattern is now **fixed for the entire grid** — columns are shared by all rows. Now ask: under that same column pattern, what does another row `i` become? Each cell `grid[i][j] XOR grid[0][j]`, possibly then flipped by the whole row. For row `i` to be clearable, `grid[i][j] XOR grid[0][j]` must be the **same value for every j** — either all `0` (row `i` was **identical** to row 0 → already zero) or all `1` (row `i` was the exact **complement** of row 0 → flip the whole row once and it's zero). If a row is a *mix* — matching row 0 in some columns and opposing it in others — no single row flip can save it.
- **Pattern trigger:** **"flip / toggle any number of times, any order"** → think **XOR + parity**, and hunt for an **invariant**: a property the operations can't change, that decides the answer without simulating. Here the invariant is *every row must be equal to row 0 or its exact complement*. The transferable move: when operations are self-inverse and commute, stop simulating — characterize the reachable set with a single equation.

---

## ① Brute Force

Try every combination of row flips and column flips (or BFS over grid states) and check if any reaches all-zeros.

```python
def remove_ones_brute(grid):
    m, n = len(grid), len(grid[0])

    # try all 2^m row-flip choices and all 2^n column-flip choices
    from itertools import product
    for row_mask in product([0, 1], repeat=m):
        for col_mask in product([0, 1], repeat=n):
            ok = True
            for i in range(m):
                for j in range(n):
                    # final cell = original XOR rowflip XOR colflip
                    if grid[i][j] ^ row_mask[i] ^ col_mask[j] != 0:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return True
    return False
```

**Why it's the natural first attempt:** "any number of flips, any order" *sounds* like search, so you enumerate the flip choices and test each.

**Why it's not enough:** it's `O(2^(m+n) · m · n)`. With `m, n` in the hundreds that's astronomically infeasible — you'd never finish a single test case. It also completely misses that the column choice is **forced** the instant you decide to clear row 0, which is the whole insight.

**Complexity:** Time `O(2^(m+n) · m·n)`, Space `O(m + n)`.

---

## ② Optimised Solution

Don't simulate anything. Use the invariant: **the grid is clearable if and only if every row equals row 0 or is row 0's exact complement.** Compare each row against row 0 directly.

```python
def remove_ones(grid):
    m, n = len(grid), len(grid[0])
    first = grid[0]

    for i in range(1, m):
        row = grid[i]
        # is this row identical to row 0 for all columns...
        same = all(row[j] == first[j] for j in range(n))
        # ...or the exact bitwise complement of row 0 for all columns?
        flipped = all(row[j] != first[j] for j in range(n))
        # anything else — a mix — is unclearable
        if not (same or flipped):
            return False
    return True
```

**Walk the example** `grid = [[0,1,0],[1,0,1],[0,1,0]]`, so `first = [0,1,0]`:

| Row i | Row values | vs `first=[0,1,0]` | same? | complement? | verdict |
|---|---|---|---|---|---|
| 1 | `[1,0,1]` | differs in **every** column | no | **yes** | OK (flip whole row after col-clear) |
| 2 | `[0,1,0]` | matches in **every** column | **yes** | no | OK (already zero after col-clear) |

Every row is same-or-complement → return `True`. And concretely: flipping column 1 alone turns the grid into all zeros — matching the promise.

Counter-example `grid = [[1,1,0],[0,0,0],[0,0,0]]`, `first = [1,1,0]`:

| Row i | Row values | vs `first=[1,1,0]` | same? | complement? | verdict |
|---|---|---|---|---|---|
| 1 | `[0,0,0]` | matches col 2 (`0==0`), differs cols 0,1 | no | no | **mix → False** |

Row 1 matches row 0 in the last column but opposes it in the first two — no single row flip fixes a mix. Return `False`.

**Why it's correct:** the final value of any cell is `grid[i][j] XOR r[i] XOR c[j]`. To clear **row 0**, the column flips are pinned: `c[j] = grid[0][j]`. Under that fixed column pattern every cell in row `i` becomes `grid[i][j] XOR grid[0][j]` (before its own row flip). A single row flip `r[i]` can only add the *same* constant bit to the whole row — so the row is zeroable exactly when `grid[i][j] XOR grid[0][j]` is **constant across all j**: constant `0` means row `i` == row 0 (`r[i]=0`), constant `1` means row `i` is the complement (`r[i]=1`). If that XOR is `0` in some columns and `1` in others, no single `r[i]` clears them all — unclearable. And since order and repeat-count never matter (flips are XOR, self-inverse, commutative), pinning columns to clear row 0 loses no generality. Hence: clearable ⟺ every row equals row 0 or its complement.

**Complexity:** Time `O(m·n)`, Space `O(1)` (we compare against row 0 in place — no extra structures).

---

## ③ Space Optimization

**Already optimal — and here's the honest reason.** We compare each row against `grid[0]` directly, holding only a couple of loop indices and two boolean flags. Nothing grows with the input beyond the grid we were handed. There's no auxiliary matrix, no memo, no copy — the complement of row 0 is checked on the fly as `row[j] != first[j]` rather than being materialized.

```python
# No extra space to cut: we read grid[0] as the reference and scan the
# other rows against it. Auxiliary memory is O(1) — two booleans per row.
```

**Complexity:** Time `O(m·n)`, Space `O(1)` auxiliary.

> Say it out loud: *"I don't build the flipped row or store any masks — I just test each row against row 0 for 'all-equal or all-different,' so it's O(1) extra space. The whole algorithm is one pass over the grid."* Naming that there's genuinely nothing to optimize — because you never allocated anything — is the strong-hire move.

---

## Java (for Java interviewers)

```java
public boolean removeOnes(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[] first = grid[0];

    for (int i = 1; i < m; i++) {
        boolean same = true, flipped = true;
        for (int j = 0; j < n; j++) {
            // identical to row 0 in every column?
            if (grid[i][j] != first[j]) same = false;
            // exact complement of row 0 in every column?
            if (grid[i][j] == first[j]) flipped = false;
        }
        // a mix is neither — unclearable
        if (!same && !flipped) return false;
    }
    return true;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (enumerate all flips) | O(2^(m+n) · m·n) | O(m + n) |
| Optimised (equal-or-complement invariant) | O(m·n) | O(1) |
| Space-optimised | — (already O(1)) | O(1) |

---

## Say it out loud (interview narration)

> *"My first thought is to simulate flips, but 'any number, any order' is a `2^(m+n)` search — too big, and it hints there's structure I'm missing. Two observations collapse it. A flip is its own inverse, so only the parity of each row's and column's flips matters — one bit each. And flips commute, because each cell just gets XOR-ed by its row-bit and column-bit — order is irrelevant. So the final cell is `grid[i][j] XOR r[i] XOR c[j]`. To zero out row 0, the column flips are forced: flip exactly the columns where row 0 is 1. That column pattern is shared by every row, so now each other row is clearable only if it's uniformly equal to row 0 — already zero — or uniformly the opposite — flip the whole row once. A row that mixes matching and opposing columns can't be saved by one row flip. So the answer is: is every row equal to row 0 or its exact complement? That's a single O(m·n) pass, O(1) space, no simulation."*

Before coding, ask the interviewer the clarifying question that shows you see the structure: *"Since flipping a row twice cancels out and order doesn't change the result, I only care whether each row/column is flipped an odd or even number of times — right?"* Voicing the XOR/parity framing early is exactly the GCA signal Google rewards.

## Related / follow-ups
- **Flip Columns For Maximum Number of Equal Rows (LC 1072)** — same "rows are equal or complementary" grouping idea, applied to counting instead of a yes/no.
- **Bulb Switcher / Bulb Switcher II** — toggle-parity reasoning; the answer depends only on how many times each thing is flipped, mod 2.
- **Minimum Number of K Consecutive Bit Flips (LC 995)** — flips as XOR with a running parity, another "don't simulate, track parity" problem.
- **Transform to Chessboard (LC 782)** — row/column swaps and flips on a binary grid decided by an invariant, not by search.
