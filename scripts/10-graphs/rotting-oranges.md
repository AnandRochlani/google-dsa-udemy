# 🎬 Recording Script — Rotting Oranges
**Pattern: Graphs (multi-source BFS) · LeetCode 994 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** flood fill (Number of Islands, LC 733). Today we upgrade the flood into a *timed wavefront* — BFS — and start it from many sources at once.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a grid of orange emoji — some fresh 🍊, a couple rotten 🟤. A clock ticks. Each tick, rot bleeds to neighbors.]**

> Google phone screen: a grid of oranges. Some fresh, some rotten. *"Every minute, rot spreads to any fresh orange next to a rotten one. How many minutes until they're all rotten — or is it impossible?"*
>
> Your first instinct is to simulate the clock — loop minute by minute, scan the whole grid each time. It works… and it re-scans the entire grid every single minute like it has amnesia.
>
> There's a way to do it in **one** pass. And it hinges on one idea that reappears in half the graph problems Google asks — starting a search from *many places at the same time.* Let me build it with you.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: a 3×3 grid. 2 = rotten, 1 = fresh, 0 = empty:]**

```
2 1 1
1 1 0
0 1 1
```

> One line: **find the minimum minutes for rot to reach every fresh orange.** If any fresh orange can never be reached, return `-1`.
>
> `2` is rotten, `1` is fresh, `0` is an empty gap. Just one rotten orange here, top-left. Watch — rot has to crawl outward from it, one ring per minute, until it reaches the far corner. Hold a guess: how many minutes to soak this whole grid? I'll tell you it's **4.** Let's earn that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — feel the waste)*

**[VISUAL: the grid with a "minute" counter. Each minute, a full-grid sweep highlights EVERY cell, then rot spreads.]**

> Let's simulate literally, the way the problem reads. Minute 1: scan *all nine cells*, find the rotten ones, rot their fresh neighbors. `(0,0)` rots `(0,1)` and `(1,0)`.
>
> **[VISUAL: minute counter → 1; two cells flip to brown; a "cells scanned: 9" tally.]**
>
> Minute 2: scan *all nine cells again*, find rotten ones — now three of them — rot their neighbors. Minute 3: scan all nine *again*. Minute 4: again.
>
> **[VISUAL: the "cells scanned" tally climbs 9, 18, 27, 36…]**
>
> See the waste? Every minute I re-scan the whole grid to re-find rotten oranges I *already knew about last minute.* I keep rediscovering the frontier from scratch. On a big grid, that's minutes times cells — brutal.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(generation effect — first pause)*

**[VISUAL: freeze. Highlight the rotten oranges from last minute being re-found by a full sweep. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is crystal clear: I already *had* the set of rotten oranges at the end of last minute. Those — and only those — are the ones that spread this minute. I don't need to search the whole grid to find them again.
>
> **LEARNER:** So instead of re-scanning, I should keep a running list of exactly the cells that *just* rotted, and only spread from those next minute?
>
> **TEACHER:** That's the whole insight. That "list of just-rotted cells I'll process next" has a name in graph algorithms. Pause and predict: **what data structure holds a frontier you process in order, and what classic traversal is this?** Three seconds.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — grid as graph, spread = BFS, MANY sources)*

**[VISUAL: grid morphs to nodes with edges to 4 neighbors. From the rotten cell, a colored wavefront ripples outward ring by ring, each ring a new shade.]**

> **TEACHER:** Reframe it. **The grid is a graph** — each cell a node, edges to its four neighbors. Rot flows along edges. "Minimum minutes for rot to reach a fresh orange" is just **shortest distance in an unweighted graph.** And the tool for shortest distance in an unweighted graph is **BFS** — breadth-first search.
>
> BFS's superpower: it explores in *rings*. All cells at distance 1 first, then all at distance 2, then 3. Sound familiar? That ring *is* one minute of rot. BFS doesn't re-scan — it keeps the frontier in a **queue** and marches outward exactly once.
>
> **[VISUAL: a single rotten source, wavefront rings labeled "minute 1, 2, 3, 4" in expanding colors.]**
>
> **LEARNER:** Okay, but here's what bugs me — there can be *several* rotten oranges to begin with, all spreading at once. BFS starts from one source. Do I run a separate BFS from each rotten orange and combine them somehow?
>
> **TEACHER:** *That's* the key question, and the answer is the trick of this entire lesson. You do **not** run many BFSs. You run **one** BFS with **many starting points.** It's called **multi-source BFS.**
>
> Here's the mental model: imagine every rotten orange is connected to one invisible "super-source" at distance zero. Seed the queue with *all* of them up front, before you start. Then BFS expands normally. Because every source sits at level 0 together, the wavefront from all of them advances in lockstep — which is *exactly* "they all rot simultaneously." Each fresh orange gets reached by whichever rotten orange is nearest, at the correct minute, automatically.
>
> **[VISUAL: TWO rotten sources this time; two wavefronts expand and merge — a fresh cell between them lights up from whichever wave hits first.]**
>
> One traversal. No re-scanning. Every cell touched once.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable line)*

**[VISUAL: boxed line: "Seed the queue with ALL sources at level 0 → BFS level-by-level → each level = one minute."]**

> Burn this in: **multi-source BFS — put every source in the queue up front, then expand level by level. Each drained level is one minute.**
>
> The "seed all sources first" move is the entire pattern. Say those words — *multi-source BFS* — the moment a problem says "spreads from many places" or "nearest of several."

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> First, seed the queue with every rotten orange, and count the fresh ones so we can detect the stuck case.

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))     # every rotten orange is a source at minute 0
            elif grid[r][c] == 1:
                fresh += 1
```

> **[VISUAL: add chunk 2.]** Edge case first: no fresh oranges means zero minutes.

```python
    if fresh == 0:
        return 0
    minutes = 0
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
```

> **[VISUAL: add chunk 3, highlight the `for _ in range(len(q))` line.]** Now the level-by-level BFS. This inner loop draining exactly one level is what turns rings into minutes.

```python
    while q and fresh > 0:
        minutes += 1                     # one minute per BFS level
        for _ in range(len(q)):          # drain EXACTLY this level
            x, y = q.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                    grid[nx][ny] = 2     # rot it now = mark visited
                    fresh -= 1
                    q.append((nx, ny))
```

> **[VISUAL: add chunk 4.]** Finally, the answer — or `-1` if a fresh orange was stranded.

```python
    return minutes if fresh == 0 else -1
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> The seeding loop is the heart of "multi-source" — *all* rotten oranges go in before BFS starts, so they share level 0.
>
> `fresh` is a live counter. It saves us from ever re-scanning to ask "are we done?" When it hits zero, every orange is rotten.
>
> `grid[nx][ny] = 2` — rotting a cell doubles as marking it visited. It's now a `2`, so no other wave re-adds it. The grid is our visited set, free.
>
> **LEARNER:** Hold on — that `for _ in range(len(q))` line. Why snapshot the length? Why not just `while q`?
>
> **TEACHER:** Crucial detail. We call `len(q)` *once*, at the start of the minute — that's how many oranges rotted as of last minute. Inside the loop we `append` newly-rotted oranges, growing the queue — but the snapshot freezes the count so those newcomers wait for *next* minute. Drop the snapshot and a plain `while q` would blend all the rings into one, and your minute count collapses to garbage. That one line is what keeps minutes honest.
>
> And `minutes if fresh == 0 else -1` — if the queue empties but fresh oranges remain, they were walled off, unreachable. That's the `-1` case, caught in O(1) thanks to the counter.

---

## 9. DRY-RUN THE CODE — `8:45`
*(worked example — prove it)*

**[VISUAL: the 3×3 grid, queue contents and `fresh` shown, cells flipping brown per minute.]**

```
2 1 1
1 1 0
0 1 1
```

| minute | drain (level) | rots | fresh after | queue |
|---|---|---|---|---|
| seed | — | — | 6 | [(0,0)] |
| 1 | (0,0) | (0,1),(1,0) | 4 | [(0,1),(1,0)] |
| 2 | (0,1),(1,0) | (0,2),(1,1) | 2 | [(0,2),(1,1)] |
| 3 | (0,2),(1,1) | (2,1) | 1 | [(2,1)] |
| 4 | (2,1) | (2,2) | 0 | [(2,2)] |

> `fresh` hits 0 at minute **4.** Loop stops, returns 4 — exactly the guess from the start. Watch how each minute drained *only* the oranges that rotted the minute before. No re-scanning. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute (rescan): O(minutes × rows × cols). Ours: O(rows × cols).]**

> Say it: *"The naive simulation rescans the whole grid each minute — O(minutes times rows times cols). BFS touches each cell at most once — it enters the queue once and leaves once — so it's O(rows times cols) time, linear in the grid. Space is the queue, also O(rows times cols) worst case."*
>
> That contrast — "I dropped a factor of minutes by remembering my frontier instead of re-finding it" — is the sentence that earns the nod.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:20`
*(depth + honesty)*

**[VISUAL: "grid = visited set" checkmark; "queue is fundamental to BFS" note.]**

> This is essentially already optimal. We rot cells in place, so there's no separate visited set — the grid *is* the marker. The only extra memory is the BFS queue, and level-order traversal fundamentally needs a frontier. You can't drop it.
>
> Say it plainly: *"The grid doubles as my visited set, so my only extra space is the frontier queue, which BFS inherently requires — that's O(rows times cols) and can't be beaten here."* Naming *why* something is optimal is as strong as finding a trick.

---

## 12. YOUR TURN (active recall) — `11:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Walls and Gates (LC 286)". Blank editor.]**

> Your turn: **Walls and Gates.** Fill each empty room with its distance to the nearest gate. It's the *same* move — seed the queue with **all** gates at once, multi-source BFS outward. If you can adapt today's code by changing what you seed, you own the pattern.

---

## 13. LOCK IT IN — `11:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Spread / minimum-time on a grid → BFS**, because BFS discovers cells in distance order — and distance is time.
> 2. **Many starting points → multi-source BFS:** seed the queue with *all* sources at level 0.
> 3. **Snapshot the level size** (`for _ in range(len(q))`) to keep each ring — each minute — separate.
>
> Memory peg: when a problem says *"spreads from several places at once"* or *"minimum minutes,"* picture **many stones dropped in a pond at the same instant** — the ripples meet in the middle. That's multi-source BFS.

---

## 14. CLIFFHANGER — `12:15`
*(open loop to next lesson)*

**[VISUAL: a matrix of 0s and 1s, each 1 glowing faintly with a number. Title blurred: "01 Matrix (LC 542)".]**

> We just measured how *time* spreads outward. Next problem flips it: for every cell, find the *distance* to the nearest zero. Sounds like you'd run a search from each cell… which would be painfully slow. But there's a beautiful inversion — the same many-stones-in-a-pond trick, run *backwards.* That's next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int orangesRotting(int[][] grid) {
    int rows = grid.length, cols = grid[0].length, fresh = 0;
    Queue<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 2) q.offer(new int[]{r, c});
            else if (grid[r][c] == 1) fresh++;
        }
    if (fresh == 0) return 0;

    int minutes = 0;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    while (!q.isEmpty() && fresh > 0) {
        minutes++;
        for (int i = q.size(); i > 0; i--) {
            int[] cell = q.poll();
            for (int[] d : dirs) {
                int nr = cell[0] + d[0], nc = cell[1] + d[1];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1) {
                    grid[nr][nc] = 2;
                    fresh--;
                    q.offer(new int[]{nr, nc});
                }
            }
        }
    }
    return fresh == 0 ? minutes : -1;
}
```
