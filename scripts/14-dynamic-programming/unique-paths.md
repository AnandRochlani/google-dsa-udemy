# 🎬 Recording Script — Unique Paths
**Pattern: Dynamic Programming (grid) · LeetCode 62 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the grid-filling from LCS/Edit Distance; the "add the ways in" counting from Climbing Stairs.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a 3×7 grid. A robot at the top-left, a flag at the bottom-right. Faint arrows: only right and down allowed. A counter: "paths = ?"]**

> A robot sits at the top-left of a grid. It can only step **right** or **down**, and it wants the bottom-right corner. How many different paths are there?
>
> Your instinct might be to actually *trace* every path. For a big grid that's millions — hopeless by hand, and exponential in code. But there's a one-line insight that turns it into a grid you fill in a blink — and a space trick so slick it looks like a magic trick: `dp[j] += dp[j-1]`. By the end you'll see exactly why that tiny line counts every path. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: a 3×2 grid. Three paths drawn: DDR, DRD, RDD. Answer: 3.]**

> One line: **count the distinct right/down paths from top-left to bottom-right of an m-by-n grid.**
>
> Tiny example — a 3-row, 2-column grid. The paths: Down-Down-Right, Down-Right-Down, Right-Down-Down. **Three.** Hold that. (And the classic `3 × 7` grid, we'll see, is 28.)

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — the decision at a cell)*

**[VISUAL: the destination cell glows. Two arrows into it — one from above, one from the left.]**

> Same trick as Climbing Stairs — stand on the destination and ask *how did I get here?* But now it's a cell `(i, j)`.
>
> Only two legal incoming moves: the robot stepped **down** from the cell above, `(i-1, j)`, or **right** from the cell to the left, `(i, j-1)`. Every path into this cell came through exactly one of those, and the two groups don't overlap. So the count is the sum:
>
> **[VISUAL: boxed — `paths(i,j) = paths(i-1,j) + paths(i,j-1)`.]**
>
> Base case: the entire **top row** and **left column** have exactly **1** path each — along an edge you can only go straight. So they're all 1s.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: recursion tree from the start cell branching right/down; the same interior cells recompute across many branches, lighting up repeatedly.]**

> **TEACHER:** Written as recursion from the start, it forks right and down at every cell, so it re-derives the same interior cells over and over — exponential, roughly 2^(m+n).
>
> **LEARNER:** This is `ways(n-1) + ways(n-2)` from Climbing Stairs, isn't it — just in **two** dimensions? Up plus left instead of one-back plus two-back?
>
> **TEACHER:** Exactly — it's Fibonacci's grid cousin; some call the filled table Pascal's triangle. Same overlapping-subproblems disease, so the same cure: fill a table, each cell once.
>
> Predict — you've done grids twice now: **when I fill this grid row by row, left to right, do I actually need the whole 2-D array?** Pause on that; it's where the elegance is.
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration — derive the grid, then foreshadow 1-D)*

**[VISUAL: a 3×7 grid. Top row and left column pre-filled with 1s. Interior cells fill as up+left, glowing.]**

> **TEACHER:** Build `dp[i][j]` = number of paths from the start to cell `(i, j)`. Top row and left column: all 1s. Every interior cell is up plus left.
>
> **[VISUAL: the 3×7 grid fills: second row becomes 1,2,3,4,5,6,7; third row 1,3,6,10,15,21,28.]**
>
> Watch it fill. Second row: `1, 2, 3, 4, 5, 6, 7`. Third row: `1, 3, 6, 10, 15, 21, 28`. Bottom-right is **28**.
>
> Now hold onto the predict from a second ago. When I compute a cell, "up" is the value *already sitting* in that column from the previous row, and "left" is the value I *just wrote* one cell ago. Both of those can live in a **single 1-D array** if I update it in place, row after row. Keep that image — it's the whole space trick.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "paths(i,j) = up + left. Edges are all 1."]**

> The line: **every cell is the ways from above plus the ways from the left; the edges are all 1.**
>
> And the deeper move, the transferable one: *"how many ways to reach the end"* almost always means **add up the ways into each predecessor.** Count problems sum; optimization problems take min or max. Same skeleton, different operator.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: editor. Type the 2-D version first.]**

> The clear 2-D version first — initialize everything to 1, so the edges are already done.

```python
def unique_paths_2d(m, n):
    dp = [[1] * n for _ in range(m)]      # top row & left col already 1
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

> That's O(m·n) time and space. Clean. But the space collapse is the reason this problem is worth teaching — coming right up.

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: the grid; spotlight one cell and its up/left neighbors.]**

> The *why*:
>
> Initializing the whole grid to 1 is a shortcut — it pre-fills the top row and left column base cases, so the loops can start at `(1, 1)` and never special-case an edge.
>
> Loops from index 1 — the edges are already correct, so we only compute the interior.
>
> `dp[i-1][j] + dp[i][j-1]` — up plus left, the recurrence, verbatim.
>
> **LEARNER:** Why is it a plain **sum**, not a min or a max like the string DPs? When do I know which to use?
>
> **TEACHER:** The cleanest rule in all of DP. If the question is **"how many"** — counting paths, counting ways — you **sum** the sub-answers, because the groups are disjoint and you want the total. If it's **"best / fewest / longest"** — an optimization — you take **min or max**. Same grid, same neighbors; the operator is dictated by the *verb* in the problem. "How many paths" → sum. Lock that in.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×7 grid fully filled.]**

> Fill `m = 3`, `n = 7`:

| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 1 | 3 | 6 | 10 | 15 | 21 | **28** |

> Each interior cell is up + left: the `6` is `3` (up) `+ 3` (left). Bottom-right **28**. And our 3×2 example would give the `3` we counted by hand. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:30`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(2^(m+n)). Grid: O(m·n) time, O(m·n) space.]**

> To the interviewer: *"Naive recursion is exponential — it recounts each cell many times. The grid fills each of the m-times-n cells once — O(m·n) time, O(m·n) space."*
>
> And drop the bonus: *"There's also a closed form — it's the binomial coefficient C(m+n−2, m−1), since every path is a fixed arrangement of downs and rights."* Nice to mention; the DP is what they want to *see*.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:00`
*(depth + honesty — the strong beat)*

**[VISUAL: the 2-D grid collapsing into a single row that updates in place, sweeping left to right, row after row.]**

> Here's the payoff — the slickest space collapse in this whole course. Keep **one** row of length `n`. Sweep top to bottom. When you reach column `j`, the value **currently** in `dp[j]` is last row's value — that's your "up." And `dp[j-1]`, which you just updated this pass, is your "left." So:

```python
def unique_paths(m, n):
    dp = [1] * n                      # top row: all 1s
    for _ in range(1, m):             # each subsequent row
        for j in range(1, n):
            dp[j] += dp[j - 1]        # dp[j] is "up" (old), dp[j-1] is "left" (new)
    return dp[-1]
```

> Row evolution for 3×7: `[1,1,1,1,1,1,1] → [1,2,3,4,5,6,7] → [1,3,6,10,15,21,28]`. Return 28.
>
> **LEARNER:** Hang on — `dp[j] += dp[j-1]` is *one line*. How does a single `+=` encode "up plus left"?
>
> **TEACHER:** This is the magic, so savor it. On the right side of the `+=`, `dp[j]` hasn't been touched *this* row yet — it's still holding the row-above value, the "up." And `dp[j-1]` was overwritten a moment ago *this* row — it's the "left." So `dp[j] = dp[j] + dp[j-1]` literally *is* `up + left`, in place, no second array. Recognizing that an in-place `+=` hides the whole 2-D recurrence — that's the elegant move interviewers remember.
>
> O(m·n) time, **O(n)** space — O(min(m,n)) if you orient the shorter side as the row.

---

## 12. YOUR TURN (active recall) — `9:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Unique Paths II (LC 63)". Some cells blacked out as obstacles.]**

> Before the next video: **Unique Paths II** — now some cells are **obstacles**. The change is tiny and satisfying: an obstacle cell has **zero** paths through it, so set its `dp` to 0 (and be careful seeding the first row/column once a wall appears). Everything else is identical. Try to bolt it onto the code you just wrote.

---

## 13. LOCK IT IN — `9:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **A cell is reached only from up or left** → `dp[i][j] = up + left`, edges all 1.
> 2. **"How many" → sum; "best" → min/max.** The verb picks the operator.
> 3. **Grid → one rolling row: `dp[j] += dp[j-1]`** is "up + left" in place. O(n) space.
>
> Memory peg — *"count the paths across a grid, right and down only"* → **fill up-plus-left; then `dp[j] += dp[j-1]`.**

---

## 14. CLIFFHANGER — `10:20`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Word Break". A string being sliced into dictionary words.]**

> Every DP so far had a tidy numeric or grid index. Next, the "table" is indexed by **positions inside a string**, and the decision is "can I chop off a valid word here and keep going?" It looks nothing like a staircase — but it's the same bottom-up table underneath. That's Word Break. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// O(min(m,n)) space — single rolling row
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
