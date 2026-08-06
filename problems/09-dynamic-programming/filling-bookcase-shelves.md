# Filling Bookcase Shelves

> **LeetCode:** 1105. Filling Bookcase Shelves · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming / linear DP over prefixes (partition DP) · **Google frequency:** ⭐ high

*If the previous problem asked "can you make a DP transition fast enough?", this one asks something Google cares about just as much: **can you tell when greedy is a lie?** The greedy solution here is obvious, beautiful, one loop long — and wrong. Spotting that is the entire interview.*

---

## Problem

You're given `books`, where `books[i] = [width_i, height_i]`, and a bookcase of fixed `shelfWidth`. You place the books onto shelves **in the given order** — you may not reorder them. You walk left to right putting books on the current shelf; at any point you may stop, start a new shelf underneath, and continue. The total widths on any one shelf must be `≤ shelfWidth`. A shelf's height is the **height of the tallest book on it**. Return the **minimum possible total height** of the whole bookcase.

**Example:** `books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]]`, `shelfWidth = 4` → **`6`**

*(Shelf 1: just `[1,1]` → height 1. Shelf 2: `[2,3],[2,3]` → width 4, height 3. Shelf 3: `[1,1],[1,1],[1,1],[1,2]` → width 4, height 2. Total 1 + 3 + 2 = **6**.)*

Notice shelf 1 holds **one** book even though two more would have fit. That's the whole problem in a nutshell.

**Constraints that matter:** `1 ≤ books.length ≤ 1000`, and `1 ≤ width_i ≤ shelfWidth ≤ 1000`. `n ≤ 1000` is a deliberate, generous ceiling — it says loudly *"O(n²) is fine, so stop trying to be clever and just be correct."* It also quietly rules out the exponential search over all partitions (`2^999`). The **order is fixed** — that single sentence is what turns this from a bin-packing nightmare (NP-hard) into a clean prefix DP.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct — and it's a trap:** "Greedy. Cram as many books onto each shelf as physically fit, then drop to the next shelf." It feels obviously right. It's the same instinct that *does* work in **Text Justification** (LC 68), where greedy line-packing is the accepted answer. Here it is **flat-out wrong**, and it's wrong on the sample input: greedy on the example above produces **8**, not 6.
- **Why greedy dies — the exact reason:** in Text Justification, the cost of a line is *nothing* — any packing that fits is legal, and the extra spaces just spread out. Here every shelf charges you the **height of its tallest book**. That cost is a `max`, not a smooth function of leftover width. A `max` means one tall book **poisons an entire shelf**, and the shelf's cost doesn't shrink at all when you add short books beside it. So sometimes the right move is to *leave space empty* — push a tall book down so it shares a shelf with another tall book, and let their heights overlap instead of paying for both separately.
- **Where the brute force hurts:** okay, greedy is out — so try everything. Every arrangement is just a choice of where to cut the sequence into consecutive groups: `n − 1` gaps, cut or don't cut, `2^(n-1)` partitions. At `n = 1000` that's not a number, it's a joke. But look at *what* is being recomputed: every one of those partitions ends with some final shelf, and once you fix the final shelf, the best way to arrange **everything before it** is a subproblem you've already solved a million times.
- **The leap:** the order is fixed, so a partial arrangement is fully described by **one number** — how many books you've placed. Define `dp[i]` = minimum total height using the first `i` books. To compute it, ask the only real question: **which books share the last shelf?** That last shelf is some suffix `j..i` whose widths fit. Everything before `j` is `dp[j-1]`, already optimal. So `dp[i] = min over valid j of (dp[j-1] + max height of books j..i)`.
- **Pattern trigger:** **"process a fixed-ordered sequence, cut it into consecutive chunks, pay a per-chunk cost"** → **linear DP over prefixes (partition DP)**. The tell is the phrase *"in the given order."* The move is always the same: `dp[i]` over prefixes, and the inner loop walks the **last chunk** backwards while it stays legal, accumulating the chunk's cost as it goes. Once you've seen it here you'll recognise it instantly in Word Break and Partition Array for Maximum Sum.

---

## ① Brute Force

Try every way to split the sequence into consecutive groups. At each step, decide how many of the next books go on the current shelf, and recurse — no memo, pure exponential search.

```python
def minHeightShelves_brute(books, shelfWidth):
    n = len(books)

    def best_from(i):                     # min height to place books[i:]
        if i == n:
            return 0
        width, height = 0, 0
        result = float('inf')
        for j in range(i, n):             # books[i..j] share this shelf
            width += books[j][0]
            if width > shelfWidth:        # can't stretch the shelf further
                break
            height = max(height, books[j][1])
            result = min(result, height + best_from(j + 1))
        return result

    return best_from(0)
```

**Why it's the natural first attempt:** once you've accepted that greedy lies, "just try every split" is the honest fallback — and it's *correct*, which is worth saying out loud before you optimise it.

**Why it's not enough:** every one of the `n − 1` gaps between books is an independent cut-or-don't-cut choice, so the search explores up to `2^(n-1)` partitions. At `n = 1000` that's `2^999` — more than atoms in the universe. And it's pure waste: `best_from(5)` gets recomputed from dozens of different prefixes, each time returning the identical number. The subproblem depends only on **the index**, nothing else.

**Complexity:** Time `O(2^n)`, Space `O(n)` recursion depth.

---

## ② Optimised Solution

Same recurrence, but indexed by prefix and filled bottom-up. `dp[i]` = minimum total height using the first `i` books, `dp[0] = 0`. For each `i`, walk `j` **backwards** from `i`, accumulating the width and the running max height of the candidate last shelf, and stop the instant the width overflows.

```python
def minHeightShelves(books, shelfWidth):
    n = len(books)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0                                   # zero books → zero height

    for i in range(1, n + 1):
        width, height = 0, 0
        j = i
        while j >= 1:                           # books j..i on the LAST shelf
            width += books[j - 1][0]
            if width > shelfWidth:              # this shelf can't reach back further
                break
            height = max(height, books[j - 1][1])
            dp[i] = min(dp[i], dp[j - 1] + height)
            j -= 1

    return dp[n]
```

Two details carry the whole thing. **Walking `j` backwards** lets `width` and `height` accumulate in `O(1)` per step — going forwards you'd have to recompute the max from scratch. And the `break` is not just a speed-up: a shelf that already overflows can never fit by reaching back *further*, so stopping is safe **and** correct.

**Walk the example** — `books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]]`, `shelfWidth = 4`:

| `i` | last-shelf options `(books j..i → width, shelf height, dp[j-1] + h)` | `dp[i]` |
|---|---|---|
| 1 | `1..1` → w1, h1, `0+1=1` | **1** |
| 2 | `2..2` → w2, h3, `1+3=4` · `1..2` → w3, h3, `0+3=3` | **3** |
| 3 | `3..3` → w2, h3, `3+3=6` · `2..3` → w4, h3, `1+3=4` · `1..3` → w5 ✗ stop | **4** |
| 4 | `4..4` → w1, h1, `4+1=5` · `3..4` → w3, h3, `3+3=6` · `2..4` → w5 ✗ | **5** |
| 5 | `5..5` → w1, h1, `5+1=6` · `4..5` → w2, h1, `4+1=5` · `3..5` → w4, h3, `3+3=6` | **5** |
| 6 | `6..6` → `5+1=6` · `5..6` → w2, h1, `5+1=6` · `4..6` → w3, h1, `4+1=5` · `3..6` → w5 ✗ | **5** |
| 7 | `7..7` → w1, h2, `5+2=7` · `6..7` → w2, h2, `5+2=7` · `5..7` → w3, h2, `5+2=7` · `4..7` → w4, h2, **`4+2=6`** · `3..7` → w6 ✗ | **6** |

`dp = [0, 1, 3, 4, 5, 5, 5, 6]` → answer **6**. ✅

Trace the winner back: `dp[7] = dp[3] + 2` (last shelf = books 4–7), `dp[3] = dp[1] + 3` (shelf = books 2–3), `dp[1] = dp[0] + 1` (shelf = book 1 alone). Exactly the arrangement in the problem statement — and notice the DP *chose* to leave book 1 alone on a half-empty shelf, which greedy would never do.

**Why it's correct:** every legal arrangement of the first `i` books ends with exactly one last shelf, holding some consecutive block `j..i` that fits within `shelfWidth`. The loop enumerates **every** such `j`, so no arrangement is missed. For a fixed `j`, the cost splits cleanly into `(best arrangement of books 1..j-1)` + `(height of this last shelf)` — the two are independent, because the last shelf's height depends only on books `j..i` and the books before `j` don't care what happens below them. That's optimal substructure, and it's exactly what the fixed ordering buys us. Since `dp[j-1]` is already the minimum for its prefix, taking the min over all `j` gives the minimum for `i`.

**Complexity:** Time `O(n²)` worst case, Space `O(n)`. In practice the inner loop stops after however many books fit one shelf — so the real bound is `O(n · k)` where `k` is the max books per shelf. With `n ≤ 1000`, even the full `10^6` is instant.

---

## ③ Space Optimization

**Already optimal at `O(n)` — and naming *why* you can't do better is the point.**

The reflex from the last lesson was "the transition only reads the previous row, so roll it down to `O(1)`." Try that here and it fails. The transition for `dp[i]` reads `dp[j-1]` for **every** `j` where the shelf `j..i` still fits — and that reach isn't fixed. If the books are one unit wide and `shelfWidth` is 1000, a single shelf spans a thousand books, so `dp[i]` depends on `dp[i-1000]`. The dependency window is **data-dependent and unbounded** by any constant, so there is no rolling set of variables that covers it.

```python
# No O(1) variant exists. The lookback distance depends on the widths:
#   narrow books + wide shelf → dp[i] reads dp[i - 1000]
#   every book exactly shelfWidth wide → dp[i] reads only dp[i - 1]
# You cannot size a rolling buffer for the worst case without... an O(n) buffer.
```

You *could* cap the buffer at "the most books that can ever share one shelf" — but in the worst case that's all `n` of them, so you've written more code for the same `O(n)`. The honest answer in the room is: **`O(n)` is the floor here, because the DP window is unbounded.** Compare that to a fixed-window DP like Fibonacci or House Robber, where two variables suffice — the difference is exactly whether the lookback is bounded by a constant.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## Java (for Java interviewers)

```java
public int minHeightShelves(int[][] books, int shelfWidth) {
    int n = books.length;
    int[] dp = new int[n + 1];
    dp[0] = 0;                                   // zero books → zero height

    for (int i = 1; i <= n; i++) {
        dp[i] = Integer.MAX_VALUE;
        int width = 0, height = 0;
        // walk j backwards: books j..i share the LAST shelf
        for (int j = i; j >= 1; j--) {
            width += books[j - 1][0];
            if (width > shelfWidth) break;       // can't reach back any further
            height = Math.max(height, books[j - 1][1]);
            dp[i] = Math.min(dp[i], dp[j - 1] + height);
        }
    }
    return dp[n];
}
```

*(No overflow worry: `n ≤ 1000` and `height ≤ 1000`, so the total tops out around `10^6` — `int` is plenty. But do initialise `dp[i]` to `Integer.MAX_VALUE` **inside** the loop, and note `j = i` always fits since `width_i ≤ shelfWidth` is guaranteed — so `dp[i]` is never left at infinity.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Greedy (cram each shelf full) | O(n) | O(1) — **but WRONG** |
| Brute force (all `2^(n-1)` partitions) | O(2ⁿ) | O(n) |
| Optimised (prefix DP, backward inner loop) | O(n²) *(really O(n·k))* | O(n) |
| Space-optimised | — none exists | O(n), unbounded lookback |

*(n = number of books; k = max books that fit on one shelf.)*

---

## Say it out loud (interview narration)

> *"My first instinct is greedy — fill each shelf as full as it goes — but let me check that before I commit. A shelf costs the **max** height of its books, not something that shrinks when I add more, so one tall book poisons a whole shelf. Small counterexample: widths and heights `[[3,1],[1,5],[1,5]]` with shelf width 4. Greedy puts the tall book with the wide short one, then the second tall book alone — five plus five, ten. But if I leave the short book alone on shelf one, the two tall books share shelf two: one plus five, **six**. So greedy is out. Since the order is fixed, a partial state is just 'how many books have I placed', so I'll do a prefix DP: `dp[i]` is the minimum height for the first `i` books, and the only question is which books share the **last** shelf. I walk `j` backwards from `i`, accumulating the shelf's width and running max height, and stop when the width overflows — that gives me `dp[i] = min(dp[j-1] + max_height(j..i))`. Time is O(n²) worst case, which `n ≤ 1000` clearly allows; space is O(n), and I can't roll that down to O(1) because the lookback distance depends on the widths, not a constant."*

Before you write a line, ask the clarifying question that proves you read the spec: *"The books have to go on the shelves in the given order — I can't reorder them, right?"* If the answer were "you can reorder," this becomes a bin-packing variant and the whole DP collapses. Asking shows you know exactly which constraint you're standing on.

## Related / follow-ups

- **Text Justification (LC 68)** — the greedy cousin, and the perfect contrast. Same "pack a sequence into fixed-width lines" shape, but there any legal packing is fine, so greedy wins. Learn to ask *"does the per-chunk cost punish me for packing tight?"* — if yes, DP; if no, greedy.
- **Partition Array for Maximum Sum (LC 1043)** — the near-twin. Same `dp[i]` over prefixes, same backwards inner loop accumulating a running max; the only differences are "at most `k` per chunk" instead of a width budget, and maximise instead of minimise. Do this one right after.
- **Word Break (LC 139)** — the same prefix DP skeleton with a boolean payload: `dp[i]` is true if some suffix `j..i` is a word and `dp[j-1]` is true. Once you see it as partition DP, it stops being a "string problem."
- **Largest Sum of Averages (LC 813)** — partition DP where the number of chunks is also capped, so the state grows to `dp[i][k]`. The natural next rung.
- **Minimum Cost to Cut a Stick (LC 1547) / Burst Balloons (LC 312)** — what happens when the chunks *aren't* over a fixed prefix: interval DP, `O(n³)`. Worth seeing the ceiling of this family.
