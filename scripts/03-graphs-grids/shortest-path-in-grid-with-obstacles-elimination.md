# 🎬 Recording Script — Shortest Path in a Grid with Obstacles Elimination
**Pattern: BFS with extra state · LeetCode 1293 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** plain grid BFS (Shortest Path in Binary Matrix / Number of Islands) — but watch the one thing that breaks it here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean grid-BFS is typed out, visited marked by (row, col). A LeetCode "Wrong Answer — 54 / 55" banner slams in red.]**

> Google onsite. Interviewer draws a grid of 0s and 1s. *"Get from top-left to bottom-right in the fewest steps. Obstacles are 1s — but you're allowed to blow up to `k` of them out of the way. Go."*
>
> You think: shortest steps, grid, every move costs one — that's **BFS**. You write it. Clean. It passes fifty-four tests. Then test fifty-five: **Wrong Answer.**
>
> Not Time Limit Exceeded. *Wrong Answer.* Your BFS is fast — it's just giving the wrong number. And here's the thing: the bug is a single word in your code — the word *visited*. By the end of this video you'll know exactly why plain BFS lies here, and the one change to your state that makes it tell the truth. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a small 5×3 grid, start marked ⭐ top-left, goal 🏁 bottom-right:]**

```
0 0 0
1 1 0
0 0 0
0 1 1
0 0 0
```

> The whole problem in one line: **fewest steps from top-left to bottom-right, up/down/left/right, and you may eliminate up to `k` obstacles on the way.**
>
> Here's our tiny example — five rows, three columns. Zeros are open, ones are walls. Let's say `k = 1`. You get to punch through *one* wall, total.
>
> Keep your eye on this exact grid. The straight-line distance is six steps — four down, two right. Hold that number: **the best you could ever hope for is six.** Question is whether one elimination is enough to get it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — feel where it goes wrong)*

**[VISUAL: the grid. A BFS wavefront floods out from ⭐. Each cell gets stamped "visited" the first time the wave touches it.]**

> Let's do what your brain does first: plain BFS. Flood outward. Mark every cell *visited* the first time you reach it, so you never waste time coming back.
>
> **[VISUAL: wave reaches (2,0), the open cell below the wall, via two different routes arriving at the same time.]**
>
> Watch cell `(2,0)` — this one, left edge, third row. Two waves hit it on the same step. One came straight down and had to **blow through the wall** at `(1,0)` to get here — it's now out of budget, zero eliminations left. The other snaked around the open right column and still has its full elimination in the bank.
>
> **[VISUAL: two tokens land on (2,0): one labeled "budget 0", one labeled "budget 1". Plain BFS stamps the cell "visited" and keeps only the FIRST — the budget-0 one.]**
>
> But plain BFS doesn't care *how* you arrived. It sees `(2,0)`, stamps it visited, and throws away the second arrival. If the one it kept is the **broke** one — zero budget — we may have just deleted the only path that could still punch through a wall later. That's your Wrong Answer.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on (2,0) holding two tokens, "budget 0" and "budget 1". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So name the bug. Two paths reach the same cell, same number of steps — but one has eliminations left and one doesn't. Plain BFS treats them as the same. They're **not**.
>
> **LEARNER:** Wait — but in every BFS I've ever written, the first time you reach a cell *is* the best. That's the whole point of the visited set. Why isn't that true here?
>
> **TEACHER:** Because normally a cell is just a location, and the first arrival can do everything a later one could. Here the arrival carries a *resource* — leftover eliminations — and that resource changes what you can do **next**. The broke arrival and the rich arrival at the same cell are two different futures. So here's your think: **if position alone isn't enough to describe where you are… what would you add to it?** Pause. What's the missing piece of the state?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: cell (2,0) splits into a stack of copies, one per budget level: a "(2,0), budget 0" tile and a "(2,0), budget 1" tile, side by side.]**

> **TEACHER:** Here's the move. Your position isn't `(row, col)`. It's `(row, col, eliminations_left)`. Fold the budget **into** the state.
>
> Think of it like a video game. Same room, but "in this room with a key" and "in this room without a key" are different save points. You wouldn't merge them — one can open the locked door, one can't.
>
> **[VISUAL: the grid redraws as k+1 stacked layers — a layer for "budget 1" and a layer for "budget 0". Stepping on a wall drops you DOWN one layer.]**
>
> So imagine the grid stacked in layers, one per budget level. Walking on an open cell keeps you on your layer. Stepping on a wall drops you to the layer below — one fewer elimination. Now run **BFS over this bigger, layered graph.** Two arrivals only collide if they match on all three: row, column, *and* budget.
>
> **LEARNER:** Okay — but doesn't that make the graph way bigger? Won't BFS blow up?
>
> **TEACHER:** It gets bigger by a factor of `k` — every cell becomes `k+1` copies. But that's still just `m × n × k` states, and BFS touches each once. For a 40-by-40 grid that's tiny. Bigger graph, same BFS, still linear in the number of states. And critically — now it's **correct**.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "State = (row, col, budget_left). A resource that changes your future belongs IN the node."]**

> Burn this one line in: **when a shortest-path problem carries a resource that changes what you can do next, put the resource inside the state.**
>
> Keys collected, moves remaining, fuel, parity — same reflex every time. BFS was never wrong. Your *node* was too small.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, dimensions — and a shortcut that's free points in the interview.

```python
from collections import deque

def shortestPath(grid, k):
    m, n = len(grid), len(grid[0])
    # If budget covers a whole straight line's worth of walls,
    # nothing can force a detour — the answer is just the distance.
    if k >= m + n - 2:
        return m + n - 2
```

> **[VISUAL: add chunk 2, highlight it.]** Now the state. We track the best budget we've ever arrived at each cell with — that's our smarter "visited."

```python
    best = {(0, 0): k}                 # cell -> richest budget seen here
    queue = deque([(0, 0, k, 0)])      # r, c, remaining, steps
```

> **[VISUAL: add chunk 3.]** Standard BFS loop. Pop, and the first time we pop the goal, we're done — BFS guarantees it's the shortest.

```python
    while queue:
        r, c, rem, steps = queue.popleft()
        if r == m - 1 and c == n - 1:
            return steps
```

> **[VISUAL: add chunk 4, highlight the `nrem` and `> best` lines.]** For each neighbor: stepping on a `1` costs one elimination. Only explore it if budget's not negative **and** this arrival is *richer* than any before.

```python
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                nrem = rem - grid[nr][nc]          # a wall spends one
                if nrem >= 0 and nrem > best.get((nr, nc), -1):
                    best[(nr, nc)] = nrem
                    queue.append((nr, nc, nrem, steps + 1))
    return -1                                       # goal never reached
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `nrem = rem - grid[nr][nc]` — beautifully sneaky. `grid` is 0 or 1. Step on open ground, subtract 0, budget unchanged. Step on a wall, subtract 1, budget drops. The grid value *is* the cost.
>
> `nrem > best.get((nr, nc), -1)` — this is the whole fix, and it's doing two jobs. It's our visited check, **and** it encodes the insight: only bother if we're arriving *richer* than ever before.
>
> **LEARNER:** Hold on — shouldn't the key be `(r, c, rem)`, the full three-part state? Why are you storing just the best budget per cell instead?
>
> **TEACHER:** Great catch — and both are correct. Full `(r, c, rem)` visited works, it just costs `O(m·n·k)` memory. But think about it: if I already reached this cell with budget 3, is it *ever* worth coming back with budget 1? No. More budget can only open more doors — a poorer arrival can't reach anywhere the richer one couldn't. So I keep only the best budget per cell. That's strictly a superset of what the poorer arrival could do. It shrinks visited from a 3-D cube to a 2-D grid — `O(m·n)` — for free.
>
> `if k >= m + n - 2: return m + n - 2` — the shortcut. The shortest *possible* route is the Manhattan distance. If you can eliminate that many walls, no configuration can force you off the straight line. Skip the whole search.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the 5×3 grid; a trace table filling row by row; the winning path lighting up cell by cell.]**

```
0 0 0
1 1 0
0 0 0
0 1 1
0 0 0
```

> Let's run the actual code, `k = 1`, and chase the winning frontier. Watch the budget.

| Step | Cell | grid value | budget left | note |
|---|---|---|---|---|
| 0 | (0,0) | 0 | 1 | start |
| 1 | (0,1) | 0 | 1 | slide right |
| 2 | (0,2) | 0 | 1 | right again |
| 3 | (1,2) | 0 | 1 | drop down the open column |
| 4 | (2,2) | 0 | 1 | down |
| 5 | (3,2) | 1 | **0** | ✳ punch the wall — budget spent |
| 6 | (4,2) | 0 | 0 | **goal popped → return 6** |

> There it is — **six**, exactly the straight-line number we promised at the start. And notice: the broke arrival at `(2,0)`, budget 0, that plain BFS would've kept? Our `best` map recorded a *richer* arrival at those left-side cells, so the winning branch through the right column was never deleted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force DFS: O(4^(m·n)). Ours: O(m·n·k). A note: "m·n cells × (k+1) budgets, each touched once × 4 neighbors".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute-forcing every path is exponential. With BFS on the enriched state, the graph has `m·n·(k+1)` nodes — every cell times every budget level — and BFS touches each once, checking four neighbors. So it's `O(m·n·k)` time."*
>
> For 40 by 40 with `k` up to sixteen hundred, that's a few million operations. Instant. That's the sentence that turns a red Hard green.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: a 3-D cube of visited states fades to a flat 2-D grid; label "O(m·n·k) → O(m·n)".]**

> Here's where you score depth points. The obvious visited set is `(r, c, rem)` — three dimensions, `O(m·n·k)` memory. **But we already shrank it.** Because more budget is never worse, we store only the *best budget per cell* — a flat 2-D map, `O(m·n)`.
>
> Say it out loud in the interview: *"I don't need every budget level per cell, only the richest — a poorer arrival can't reach anywhere the richer one couldn't, so I prune it. That takes visited from `O(m·n·k)` down to `O(m·n)`."* Naming *why* the poorer arrival is safe to drop — that's the invariant, and stating invariants out loud is exactly what separates a strong hire from someone who memorized the code.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Shortest Path to Get All Keys (LC 864)". A blank editor.]**

> Before the next video, try **Shortest Path to Get All Keys**. Same skeleton — BFS with extra state — but here the resource in the node isn't a *count*, it's a **bitmask of which keys you've collected**. Position plus keys-so-far is the state.
>
> Don't peek. Wrestle with it for ten minutes. Feeling *what* to fold into the state — that's the muscle this whole lesson is building.

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Plain BFS is wrong when arrivals carry a resource** — two paths to a cell aren't equal if they've spent different eliminations.
> 2. **Fix it by enriching the state** — `(row, col, budget_left)`. BFS is fine; the node was too small.
> 3. **Prune smart** — keep only the *richest* budget per cell; more budget is never worse, so visited drops to `O(m·n)`.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "A resource that changes your future belongs IN the node."]**
>
> When a shortest-path problem hands you a budget, a key, or a fuel gauge, your hand should already be reaching to fold it into the state — not into a side variable.
>
> *(GCA reminder — for the interview itself: don't just code the fix. Say the wrong version first — "plain BFS, mark cells visited" — then catch yourself out loud: "wait, two arrivals differ by budget, so I need to add it to the state." Google's General Cognitive Ability signal isn't the final code — it's you narrating the bug and the repair. Ask up front whether stepping on an obstacle always spends an elimination. That clarifying question is free points.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Swim in Rising Water" — a grid where each cell shows a rising water level, and edges shimmer with different costs.]**

> We got away with BFS because every step cost exactly **one**. But what happens when the steps *don't* cost the same — when moving onto some cells costs more than others, and "fewest steps" becomes "cheapest path"? BFS quietly breaks, and a cousin takes over: **Dijkstra**. That's the next one — Swim in Rising Water. Same grid instincts, but the moment costs stop being equal, everything changes. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int shortestPath(int[][] grid, int k) {
    int m = grid.length, n = grid[0].length;
    if (k >= m + n - 2) return m + n - 2;      // straight line is achievable

    int[][] best = new int[m][n];               // richest budget seen per cell
    for (int[] row : best) java.util.Arrays.fill(row, -1);
    best[0][0] = k;

    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    Deque<int[]> queue = new ArrayDeque<>();
    queue.offer(new int[]{0, 0, k, 0});         // row, col, remaining, steps

    while (!queue.isEmpty()) {
        int[] cur = queue.poll();
        int r = cur[0], c = cur[1], rem = cur[2], steps = cur[3];
        if (r == m - 1 && c == n - 1) return steps;   // first pop = shortest
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
            int nrem = rem - grid[nr][nc];              // a wall spends one
            if (nrem >= 0 && nrem > best[nr][nc]) {      // only if strictly richer
                best[nr][nc] = nrem;
                queue.offer(new int[]{nr, nc, nrem, steps + 1});
            }
        }
    }
    return -1;
}
```
