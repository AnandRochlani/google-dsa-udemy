# 🎬 Recording Script — Longest Line of Consecutive One in Matrix
**Pattern: DP on a grid (4 directions) · LeetCode 562 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a binary grid of 0s and 1s. A cursor stands on the first 1 of a long row and walks the whole row, counting. Then it hops to the next 1 and walks *almost the same row again*. A "cells re-scanned" counter spins upward, alarming red.]**

> The interviewer draws a grid of 0s and 1s and says: *"Find the longest straight line of 1s. It can go across, down, or diagonal either way. Go."*
>
> You do the obvious thing — stand on each 1, walk each direction, measure. It works. But watch that counter: on a long row of ones, you walk the whole run, then walk almost all of it *again* from the next cell. You're measuring the same tail over and over.
>
> By the end of this video you'll kill that repetition with one idea — a direction flip — that turns the whole thing into a single clean sweep. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below it, a 3×4 grid of tiles:]**

```
0 1 1 0
0 1 1 0
0 0 0 1
```

> The whole problem in one line: **find the longest line of consecutive 1s — and a line can run horizontal, vertical, or either diagonal.**
>
> Here's our tiny example — twelve cells. Two little blocks of 1s on the left, and one lonely 1 down in the bottom-right corner.
>
> The answer here is **three**. Don't hunt for it yet — just hold that number. And here's a tease: it's *not* one of the obvious 2×2 blocks. Keep your eye on that lonely corner 1.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the grid. A "walks" counter top-right at 0. Arrows fire from each 1 in four directions: right, down, down-right, down-left.]**

> Let's do what your brain does first. Stand on a 1, then walk all four line directions until you hit a 0 or the edge, counting as you go.
>
> Stand on the top-left 1 at `(0,1)`. Walk right: `1, 1` — length 2. Walk down: `1, 1` — length 2. Walk down-right: `(0,1) → (1,2) → (2,3)` — that's `1, 1, 1`, length **3**!
>
> **[VISUAL: the down-right diagonal lights up through all three 1s to the corner; counter shows 3.]**
>
> Now stand on `(0,2)`. Walk right — length 1. Walk down — `1,1`, length 2. But notice: standing on `(1,1)` in a second, I'll walk down again and re-measure a run I basically already touched.
>
> **[VISUAL: highlight overlapping vertical segments being re-walked; "walks" counter jumps past the number of cells.]**
>
> On a big grid, every cell re-walks the tails of its neighbors. That's `O(m·n·max(m,n))` — the wasted work that'll cost you.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight a long horizontal run; three different cells each re-walking its tail. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? On a row of ones, the walk from cell 0 measures the whole run. From cell 1, almost the whole run again. Cell 2, again. We keep re-measuring the same tail.
>
> **LEARNER:** But that's just what the problem asks — measure lines. How do you *not* re-walk them?
>
> **TEACHER:** Here's the flip. Right now I'm asking *"how far can I reach from here?"* — and that costs a walk. What if I ask the opposite: *"how long is the run that **ends** right here?"* Pause the video. If you knew that answer for the cell just to my left, how fast could you get mine?

*(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a single row `1 1 1`. Under each cell a badge. Left cell fills "1", middle "2", right "3" — each just its left neighbor's badge plus one.]**

> **TEACHER:** Watch. For the horizontal run *ending* at a cell, the answer is dead simple: **it's the run ending at my left neighbor, plus one.** Left neighbor says 2? I'm 3. No walking — one lookup.
>
> It's like a queue at a counter. You don't recount everyone ahead of you — you ask the person right in front, *"what number are you?"*, and add one. That's your number.
>
> **[VISUAL: the same idea shown four times — arrows pointing from left, from above, from up-left, from up-right into one target cell.]**
>
> And there are four line directions, so I keep **four** of these per cell. Horizontal leans on my **left**. Vertical leans on the cell **above**. The down-right diagonal leans on **up-left**. And the anti-diagonal — down-left — leans on **up-right**.
>
> **LEARNER:** Wait — the down-*left* diagonal leans on the cell up and to the *right*? That feels backwards.
>
> **TEACHER:** It trips everyone. The line travels down-left as it grows. So the cell *before* me on that line — the one already computed — sits up and to the right. I read *its* anti-diagonal badge and add one. Up-right, `j + 1`. Say it twice; it's the one bounds bug people ship.
>
> **[VISUAL: an anti-diagonal `(0,2) → (1,1)`; arrow from `(1,1)` back up-right to `(0,2)`, badge 1 → 2.]**

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "run ending here = matching neighbor's run + 1 — four directions, four neighbors: left, up, up-left, up-right."]**

> Burn this in: **the run ending at a cell is the matching neighbor's run plus one — and a 0 resets all four to zero.**
>
> Left, up, up-left, up-right. Four directions, four already-computed neighbors, one lookup each. That's the whole trick.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, dimensions and the DP table — four zeros per cell, one slot per direction.

```python
def longest_line(mat):
    if not mat or not mat[0]:
        return 0
    m, n = len(mat), len(mat[0])
    # dp[i][j] = [horiz, vert, diag ↘, anti ↙] run ending at (i, j)
    dp = [[[0, 0, 0, 0] for _ in range(n)] for _ in range(m)]
    best = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Sweep every cell top-to-bottom, left-to-right. A 0 breaks every line — skip it, leave its four zeros.

```python
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                continue
```

> **[VISUAL: add chunk 3 — the four recurrences, each on its own line.]** Now the heart. Each direction extends one neighbor by 1, guarding the grid edge.

```python
            dp[i][j][0] = (dp[i][j - 1][0] if j > 0 else 0) + 1          # left
            dp[i][j][1] = (dp[i - 1][j][1] if i > 0 else 0) + 1          # above
            dp[i][j][2] = (dp[i - 1][j - 1][2] if i > 0 and j > 0 else 0) + 1     # up-left
            dp[i][j][3] = (dp[i - 1][j + 1][3] if i > 0 and j < n - 1 else 0) + 1 # up-right
```

> **[VISUAL: add chunk 4, highlight `best`.]** Track the global max over all four, all cells, and return it.

```python
            best = max(best, dp[i][j][0], dp[i][j][1], dp[i][j][2], dp[i][j][3])
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `if mat[i][j] == 0: continue` — a 0 can't be on any line, so all four runs stay zero. That's the reset. Any later cell leaning on this one restarts from scratch, exactly right.
>
> The four recurrences — each reads **one** neighbor that's already done. Left and above are obvious. The `[2]` diagonal reads up-left. The `[3]` anti-diagonal reads up-**right**, `j + 1` — the direction everyone fat-fingers.
>
> **LEARNER:** Those bounds checks — why `j < n - 1` on the last one but `j > 0` on the diagonal above it?
>
> **TEACHER:** Because they reach opposite ways. Up-left reads column `j - 1`, so it dies at the left edge — guard `j > 0`. Up-right reads column `j + 1`, so it dies at the *right* edge — guard `j < n - 1`. Mirror directions, mirror guards. Get one wrong and you either index out of bounds or silently read a stale cell.
>
> And why does reading a neighbor never read a *stale* value? Because we sweep top-down, left-right. Left, above, up-left, up-right — all four sit earlier in that sweep. Every predecessor is finalized before we touch it.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×4 grid; a trace table filling row by row. Each populated cell shows `[H, V, ↘, ↙]`.]**

```
0 1 1 0
0 1 1 0
0 0 0 1
```

> Let's run the real code and watch the diagonal build to the corner.

| Cell | `[H, V, ↘, ↙]` | why |
|---|---|---|
| (0,1) | `[1, 1, 1, 1]` | block corner, nothing before it |
| (0,2) | `[2, 1, 1, 1]` | H extends `(0,1)` |
| (1,1) | `[1, 2, 1, 2]` | ↙ reads `(0,2)`'s ↙ = 1, +1 |
| (1,2) | `[2, 2, 2, 1]` | ↘ reads `(0,1)`'s ↘ = 1, +1 |
| (2,3) | `[1, 1, 3, 1]` | ↘ reads `(1,2)`'s ↘ = 2, **+1 → 3** |

> There it is. `best` climbs 1 → 2 → **3**, landing on that ↘ at the corner cell. The winning line was the diagonal `(0,1) → (1,2) → (2,3)` — the lonely corner 1 we flagged at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(m·n·max(m,n)). Ours: O(m·n). Note: "one O(1) visit per cell, 4 lookups."]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force walks four directions from every cell — O(m·n·max(m,n)), and it re-measures shared tails. My DP visits each of the m·n cells once, does four constant-time lookups, so it's O(m·n) time. Space is O(m·n) for the table."*
>
> That's the sentence that turns a shaky Medium into a clean one.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: the full DP table; a "roll to two rows?" thought bubble; a green ✓.]**

> Quick win, and it scores points. Look at what each recurrence reads: horizontal reads the **current** row; the other three read the row **directly above**. Nothing ever reaches back two rows.
>
> **[VISUAL: fade all rows except the current one and the one above it.]**
>
> So keep just a **previous row** and a **current row** — two rows of size n — and roll them down as you descend. Same O(m·n) time, but space drops from O(m·n) to **O(n)**.
>
> Say it out loud: *"Every dependency is one row deep at most, so I roll two rows and get O(n) space."* Naming *why* it shrinks — dependency depth exactly one — is the strong-hire signal.

---

## 12. YOUR TURN (active recall) — `10:05`
*(retrieval practice)*

**[VISUAL: "Your turn → Maximal Square (LC 221)". A blank editor.]**

> Before the next video, try **Maximal Square**. Same skeleton — a value computed at each cell from its already-done neighbors — but instead of four directions, `dp[i][j]` is the biggest all-1 square ending there, and it takes the **min** of three neighbors plus one.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Brute force re-walks shared tails → O(m·n·max(m,n)).** The flip: ask "run *ending* here," not "reach from here."
> 2. **Four directions, four neighbors** — left, above, up-left, up-right. The anti-diagonal reads up-**right** (`j + 1`) — that's the bug people ship.
> 3. **Dependencies are one row deep** → roll two rows for O(n) space.
>
> The memory peg:
>
> **[VISUAL: big box → "run ending here = neighbor's run + 1 · four directions · a 0 resets all four."]**
>
> When a grid problem asks for the longest *streak* in fixed directions, your hand should reach for "run ending here, plus one" — not a walk.
>
> *(GCA reminder — for the interview itself: state the brute force, name the repeated tail-walking out loud, *then* reach for the direction flip. Google scores how you narrate naive → optimal, not just the final code. And ask the one clarifying question early: "lines run all four orientations, and consecutive means no gaps, right?")*

---

## 14. CLIFFHANGER — `11:05`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Maximal Rectangle" — a grid with a tall rectangle of 1s outlined, a histogram forming beneath it.]**

> We got our answer because a *line* only cares about one neighbor per direction. But what if the interviewer asks for the biggest all-1 **rectangle**, not a line? Suddenly one lookup isn't enough — you need to know how *wide* a bar can stretch at every height. That's the next one: Maximal Rectangle, where per-column heights meet the largest-rectangle-in-a-histogram trick. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
