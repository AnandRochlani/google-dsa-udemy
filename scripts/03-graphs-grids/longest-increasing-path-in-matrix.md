# 🎬 Recording Script — Longest Increasing Path in a Matrix
**Pattern: DFS + Memoization · LeetCode 329 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** plain grid DFS (Number of Islands / Word Search) — but watch what changes here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean recursive grid-DFS is typed out. A LeetCode "Time Limit Exceeded — 30 / 139" banner slams in red.]**

> Google onsite. The interviewer draws a grid of numbers and says: *"Longest path where every step goes to a bigger number. Go."*
>
> You write a clean depth-first search. It walks to bigger neighbors. It's *correct* — it passes the small tests. You hit run on the big one and… Time Limit Exceeded.
>
> Here's the twist: your code isn't wrong. It's just doing the **same work thousands of times**. By the end of this video, you'll fix it with a single line — a cache — and you'll understand the one property of this problem that makes that cache bulletproof. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a 3×3 grid of tiles:]**

```
9 9 4
6 6 8
2 1 1
```

> The whole problem in one line: **find the longest path where each step moves up, down, left, or right — to a strictly bigger number.**
>
> Here's our tiny example — nine cells. No diagonals. No stepping onto an equal or smaller value. Keep your eye on this exact grid; we'll solve it by hand before we write a line of code.
>
> There's a path of length **four** hiding in here. Don't hunt for it yet — just hold that the answer is four.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the 3×3 grid. A "calls to dfs" counter, top-right, starting at 0. Arrows trace walks from several starting cells.]**

> Let's do what your brain does first: start a walk from *every* cell, and each time, keep stepping to any bigger neighbor. Whatever walk goes deepest wins.
>
> Start at the `1` in the bottom row. Step up to `2`, up to `6`, up to `9`. Length four. Counter ticks.
>
> **[VISUAL: arrows 1 → 2 → 6 → 9 light up; counter climbs.]**
>
> Now start from the `2`. Step to `6`, to `9`. But wait — we *just* computed the best walk out of `6`. We're doing it **again**.
>
> **[VISUAL: highlight the `6 → 9` segment glowing a second time; counter jumps.]**
>
> Now start from that *other* `6` on the middle row. It walks to `8`… and to `9` again. Every start keeps crashing into the same tails.
>
> **[VISUAL: counter morphs into "≈ 2^(m·n)" with a scary red glow.]**
>
> On a 200-by-200 grid, that repetition explodes — exponential. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the `6` cell being re-entered from three different starts. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? Look at this `6`. The best path *starting* from it — `6 → 9`, length two — is the same no matter who walks in. But we recompute it every single time someone arrives.
>
> **LEARNER:** Right, but paths overlap — isn't that just unavoidable? Different starts *do* share cells.
>
> **TEACHER:** They share cells, yes — but the *answer* for a shared cell never changes. So here's your think: **what if, the first time we solve a cell, we just wrote the answer down?** Pause the video. What would we store, and what would we look up?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: each cell gets a small badge in its corner — empty at first. As `dfs` finishes a cell, its badge fills with a number.]**

> **TEACHER:** Here's the move. Define one clean question for every cell: **`best(cell)` — how long is the longest increasing path that *starts* right here?**
>
> That number depends only on the cell's **bigger** neighbors. So compute it once, then stamp it on the cell like a sticky note. Next time anyone asks, we read the sticky note — instant.
>
> **[VISUAL: solve `9` → badge "1". Solve `8` → badge "2". Solve `6` → badge "2". Each fills once and stays.]**
>
> `9` has no bigger neighbor, so `best` is 1 — just itself. `6` steps to `9`, so it's `1 + 1 = 2`. Stamp it. Now when the `2` below asks `6` for its best, it doesn't walk anywhere — it *reads the 2 off the sticky note.*
>
> **LEARNER:** Hold on — with normal grid DFS, like Number of Islands, we always carried a *visited* set so we don't loop forever. You didn't use one. Won't this cache go stale, or loop?
>
> **TEACHER:** That is exactly the right worry, and here's the beautiful part. Every step goes to a **strictly bigger** number. You can *never* step back down. So you can never return to a cell you came from — **there's no cycle. Ever.**
>
> **[VISUAL: try to draw an arrow back from `9` down to `6` — it turns red and snaps, "smaller — illegal".]**
>
> No cycles means the grid is a **DAG** — a directed acyclic graph. And on a DAG, a cell's answer is final the moment you compute it. So the cache can never be wrong, and we don't need a visited set at all. The strict-increase rule does that job for free.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "strictly increasing ⇒ DAG ⇒ memo is safe (no visited set)."]**

> Burn this one line in: **strictly increasing means no cycles — it's a DAG — so memoization is safe, and you don't need a visited set.**
>
> That sentence is the whole lesson. Any grid problem where the moves are *strictly monotonic*, this is your reflex: DFS plus a cache.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in pieces. First, dimensions and the memo grid — zero means "not solved yet."

```python
def longest_path(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    memo = [[0] * cols for _ in range(rows)]
```

> **[VISUAL: add chunk 2, highlight it.]** Now the heart — `dfs` for one cell. First line: if it's cached, hand it back.

```python
    def dfs(r, c):
        if memo[r][c]:
            return memo[r][c]
        best = 1                      # the cell itself is a path of length 1
```

> **[VISUAL: add chunk 3.]** Look at all four neighbors; only walk into strictly-bigger ones.

```python
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
```

> **[VISUAL: add chunk 4, highlight the `memo[r][c] = best` line.]** Stamp the sticky note *before* returning — that's the whole optimization. Then take the max over every starting cell.

```python
        memo[r][c] = best
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `if memo[r][c]: return memo[r][c]` — this one line is the difference between exponential and linear. It's the sticky note. Without it, you're back to the brute force.
>
> `best = 1` — a single cell is already a path of length one. That's our floor.
>
> `matrix[nr][nc] > matrix[r][c]` — **strictly** greater. This is what makes the whole thing a DAG. Change that `>` to `>=` and equal cells could point at each other — you'd get a cycle, the recursion would spin forever, and the memo *would* be unsafe.
>
> **LEARNER:** So we never mark a cell "in progress" and never unmark it. In a normal DFS that's how you avoid infinite loops. Why is it fine to skip that here?
>
> **TEACHER:** Because the `>` guarantees we always move to a *bigger* value. You can't walk in a circle when every step goes strictly up — you'd have to eventually come back down, and the code forbids that. The visited set is unnecessary; the ordering *is* the guard.
>
> `memo[r][c] = best` — written once, read many times. Once it's set, it never changes, because a cell's bigger-neighbors never change.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×3 grid with badges; a trace table filling row by row.]**

```
9 9 4
6 6 8
2 1 1
```

> Let's run the actual code and watch the sticky notes fill in. We'll chase the winning path from the `1` at bottom-middle.

| Call | bigger neighbor | computes | memo stamped |
|---|---|---|---|
| dfs(9) top-left | none | 1 | 9 → **1** |
| dfs(6) mid-left | 9 (reads memo) | 1 + 1 = 2 | 6 → **2** |
| dfs(2) bot-left | 6 (reads memo) | 1 + 2 = 3 | 2 → **3** |
| dfs(1) bot-mid | 2 (reads memo) | 1 + 3 = 4 | 1 → **4** |

> Every arrow after the first *reads* a badge instead of re-walking. `dfs(9)` ran exactly once. The `max` over all cells picks up that **4**. Loop closed — and the path was `1 → 2 → 6 → 9`, exactly the four we promised at the start.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(2^(m·n)). Ours: O(m·n). A note: "each cell solved once × 4 neighbors".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is exponential because it recomputes shared tails. With memoization, each of the `m·n` cells is solved exactly once, and each solve checks at most four neighbors — so it's `O(m·n)` time. Space is `O(m·n)` for the memo, plus recursion depth."*
>
> That's the sentence that flips a Hard from "I hope" to "I've got this."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the memo grid; a "roll to one row?" thought bubble appears, then gets a red ✗.]**

> Quick but important — and here honesty scores points.
>
> Can we shrink the `O(m·n)` memo? **No — and I can say exactly why.** The memo *is* the algorithm; every cell's answer gets reused by its smaller neighbors. And I can't roll it down to a single row like some DP tables, because a cell depends on neighbors in **all four directions** — above, below, left, right — not just the previous row.
>
> Say that out loud in the interview: *"Space is `O(m·n)` and that's optimal here, because dependencies point every direction — there's no rolling-row trick."* Naming *why* it can't shrink is a stronger signal than silently accepting it.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Increasing Paths in a Grid (LC 2328)". A blank editor.]**

> Before the next video, try **Number of Increasing Paths in a Grid**. Same DAG, same DFS-plus-memo skeleton — but instead of the *longest* path, you *count* how many increasing paths exist.
>
> Don't peek at the solution. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Plain DFS recomputes shared tails → exponential.** The fix is one line: a cache.
> 2. **`best(cell)` = longest path starting there** — compute once, stamp it, reuse it.
> 3. **No visited set needed** — the strict-increase rule already forbids cycles.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "strictly increasing ⇒ DAG ⇒ memo is safe."]**
>
> When the moves on a grid only ever go *up*, your hand should already be reaching for DFS plus a memo — no visited set required.
>
> *(GCA reminder — for the interview itself: state brute force, name the repeated work out loud, then reach for the cache. Google's General Cognitive Ability signal isn't the trick — it's you narrating the path from naive to optimal. Say the DAG insight before you write the memo line.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Course Schedule" — a graph with a cycle drawn in red.]**

> We got away without a visited set because this grid *couldn't* have a cycle. But what happens when the graph **can** loop back on itself — when the whole question becomes *"is there a cycle at all?"* That's the next one: Course Schedule. Same DAG idea, flipped inside out — now detecting the cycle is the entire game. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
private static final int[][] DIRS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

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
