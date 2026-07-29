# 🎬 Recording Script — 01 Matrix
**Pattern: Graphs (multi-source BFS) · LeetCode 542 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Rotting Oranges (LC 994) — the many-stones-in-a-pond, multi-source BFS. Today we use the *same* trick, run in reverse.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a matrix of 0s and 1s. Each 1 sprouts a little "?" — "how far to the nearest 0?"]**

> Here's the ask: given a grid of 0s and 1s, for **every** cell, find the distance to the nearest 0.
>
> Your gut says: for each `1`, do a search until you bump into a `0`. Reasonable. But there could be thousands of 1s, and each search wanders the grid — so you re-explore the same ground over and over, and it times out.
>
> The fix is one of the most elegant moves in all of graph problems: instead of every `1` hunting for a `0`, you make **all the 0s hunt outward together.** Flip the direction of the search. Let me show you why that's a game-changer.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: a 3×3 matrix and its answer side by side:]**

```
mat =        answer =
0 0 0        0 0 0
0 1 0        0 1 0
1 1 1        1 2 1
```

> One line: **replace each cell with its distance, in steps, to the nearest 0.** Steps are up/down/left/right.
>
> Every `0` is distance 0 — trivially. The `1` at `(1,1)` sits right next to several 0s → `1`. The `1` at `(2,0)` is one step from the `0` above it → `1`. But `(2,1)`, dead center of the bottom row, is *two* steps from any 0 → `2`. That center cell is the one to watch.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — feel the waste)*

**[VISUAL: from the `1` at (2,1), a search balloon expands ring by ring until it touches a 0. Then it RESTARTS from (2,0) and re-expands over the same cells.]**

> Let's do the naive thing: for each `1`, launch a search and stop at the first `0`.
>
> Start at `(2,1)`. Ring 1: neighbors `(1,1)`, `(2,0)`, `(2,2)` — all 1s, no 0 yet. Ring 2: now I reach 0s. Distance `2`. Okay.
>
> Now `(2,0)`. Launch *another* search. Ring 1 finds the `0` above. Distance `1`.
>
> **[VISUAL: a "searches launched" tally ticking up, and overlapping ring regions glowing to show repeated coverage.]**
>
> See the problem? Every `1` starts its own search, and neighboring 1s re-explore almost the exact same cells. Nothing is shared. With up-to `m·n` ones, each search touching up-to `m·n` cells, that's `(m·n)` squared. On a 100×100 grid that's a hundred million operations. Too slow.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(generation effect — first pause)*

**[VISUAL: freeze on two adjacent 1s re-searching the same neighborhood. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is the *repeated, overlapping* searches. Each `1` independently rediscovers the same territory. We're computing the same distances again and again from different starting points.
>
> **LEARNER:** So could I somehow do a *single* search that fills in every cell's distance at once, instead of one search per `1`?
>
> **TEACHER:** Yes — and the trick to make one search serve everyone is to change *who starts it.* Pause and predict: **we just learned multi-source BFS on Rotting Oranges. Who should the sources be here — and which direction should the search flow?** Three seconds.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — invert the search, multi-source from all zeros)*

**[VISUAL: grid morphs to nodes. Instead of 1s searching, ALL the 0s light up and send wavefronts outward simultaneously, rings coloring 1, 2, 3…]**

> **TEACHER:** Here's the inversion. Don't ask each `1`, "where's my nearest 0?" Instead ask the **0s** to broadcast outward: "I'm distance 0 — everyone I reach in one step is distance 1, two steps is distance 2…"
>
> That's **multi-source BFS**, exactly like Rotting Oranges — but the sources are all the **0s**, not the 1s. Seed the queue with *every* 0 at distance 0. Expand in rings. Because BFS advances in nondecreasing distance, the **first** time a wavefront reaches a cell, that's guaranteed to be its shortest distance to the *nearest* 0.
>
> **[VISUAL: two 0-sources' wavefronts approach the center cell (2,1); whichever reaches first stamps its distance; the cell locks at 2.]**
>
> **LEARNER:** But wait — a fresh cell might be reachable from *two* different 0s. Don't I risk stamping it with the wrong, larger distance from the farther one?
>
> **TEACHER:** That's the misconception to kill. No — because BFS processes cells in *increasing* distance order. The **closest** 0's wavefront always arrives first. We mark each cell the first time it's reached and *never overwrite it.* So it locks in the minimum, automatically. The farther 0 shows up later, sees the cell already stamped, and moves on.
>
> One traversal fills the entire grid. From `(m·n)`-squared down to linear.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable line)*

**[VISUAL: boxed line: "Distance to nearest X? → seed BFS with ALL the X's at once, expand outward."]**

> The key move: **"distance from every cell to the nearest cell of type X" → multi-source BFS seeded with all the X cells.** Invert the search — let the targets broadcast, not the seekers.

---

## 7. CODE IT — LIVE & CHUNKED — `5:25`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Setup: a `dist` grid where `-1` means "not visited yet," and seed the queue with every 0.

```python
from collections import deque

def update_matrix(mat):
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]   # -1 = unvisited
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0          # every 0 is a source at distance 0
                q.append((r, c))
```

> **[VISUAL: add chunk 2, highlight.]** Now the BFS. One ring at a time, stamping distances.

```python
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1   # first visit = shortest distance
                q.append((nr, nc))
    return dist
```

> Notice — no explicit "minute" loop this time. We don't need level snapshots, because each cell just takes its parent's distance plus one.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> The seeding loop is "multi-source" again — every 0 enters the queue up front. That's what makes the nearest-0 guarantee work.
>
> The `dist[nr][nc] == -1` check is doing double duty: it's the visited test *and* the "write-once" guarantee. A cell only gets stamped when it's still `-1`. Once stamped, it's never touched again — which is exactly why the *first* (nearest) wavefront wins and later ones are ignored.
>
> `dist[nr][nc] = dist[r][c] + 1` — a cell is one step farther than whoever reached it. Since the queue is in distance order, `dist[r][c]` is already final when we read it, so `+1` is correct.
>
> **LEARNER:** In Rotting Oranges we had that `for _ in range(len(q))` level-snapshot line. Why don't we need it here?
>
> **TEACHER:** Great memory. There we needed a single global *minute* counter, so we had to know where each ring ended. Here, each cell carries *its own* distance in the `dist` grid — `parent + 1`. The distance rides along with the cell, so we never need to know the ring boundaries. Two flavors of the same BFS: one counts global levels, one stamps per-cell distance.

---

## 9. DRY-RUN THE CODE — `7:55`
*(worked example — prove it)*

**[VISUAL: dist grid filling in, queue shown.]**

> Seed the queue with all five 0s. `dist` starts:

```
0 0 0
0 -1 0
-1 -1 -1
```

| dequeue | stamps | dist now (changed) |
|---|---|---|
| (0,1) | (1,1) = 1 | center-top → 1 |
| (1,0) | (2,0) = 1 | (2,0) → 1 |
| (1,2) | (2,2) = 1 | (2,2) → 1 |
| (1,1) [d=1] | (2,1) = 2 | center-bottom → 2 |
| (2,0),(2,2) [d=1] | (2,1) already set → skip | — |

> Final:
> ```
> 0 0 0
> 0 1 0
> 1 2 1
> ```
> The center `(2,1)` locked at **2** — reached by the `1`-distance cell above it, and later wavefronts saw it already stamped and left it alone. Exactly right. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:55`
*(transfer to interview)*

**[VISUAL: Brute: O((m·n)²). Ours: O(m·n).]**

> Out loud: *"BFS-per-1 is O of (m times n) squared — a search per cell, each touching the whole grid. Inverting to one multi-source BFS from all the 0s touches every cell exactly once — O(m times n) time. Space is the queue plus the `dist` grid, O(m times n) — and the `dist` grid is also the required output, so it isn't really *extra.*"*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:30`
*(depth + honesty — the DP alternative)*

**[VISUAL: two arrows sweeping the grid — top-left pass, then bottom-right pass — no queue.]**

> The `dist` grid is the output, so it's not extra. The genuine extra is the queue. Can we kill even that? Yes — there's a slick **two-pass dynamic programming** version with *no queue at all*.
>
> The idea: a cell's nearest 0 is reached either from above/left or from below/right. So sweep once from the top-left, taking the min of "my up neighbor + 1" and "my left neighbor + 1." Then sweep from the bottom-right with down and right neighbors. Two passes, and every cell sees all four directions.

```python
def update_matrix_dp(mat):
    rows, cols = len(mat), len(mat[0])
    INF = float('inf')
    dist = [[0 if v == 0 else INF for v in row] for row in mat]
    for r in range(rows):                 # pass 1: up + left
        for c in range(cols):
            if dist[r][c] != 0:
                if r > 0: dist[r][c] = min(dist[r][c], dist[r-1][c] + 1)
                if c > 0: dist[r][c] = min(dist[r][c], dist[r][c-1] + 1)
    for r in range(rows - 1, -1, -1):     # pass 2: down + right
        for c in range(cols - 1, -1, -1):
            if r < rows - 1: dist[r][c] = min(dist[r][c], dist[r+1][c] + 1)
            if c < cols - 1: dist[r][c] = min(dist[r][c], dist[r][c+1] + 1)
    return dist
```

> Same O(m·n) time, but **O(1) extra space** — no queue. Say it out loud in the room; showing you know both the BFS *and* the DP is a strong-hire detail.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → As Far from Land as Possible (LC 1162)". Blank editor.]**

> Your turn: **As Far from Land as Possible.** Multi-source BFS from all the *land* cells — but instead of stamping each water cell, you track the **maximum** distance reached. Same seeding trick, different aggregation.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Nearest X" over a whole grid → invert the search.** Don't search *from* the seekers; broadcast *from* the targets.
> 2. **Seed multi-source BFS with all the targets** at distance 0; first arrival = shortest distance.
> 3. **Write-once** (`== -1` guard) locks in the minimum and makes later wavefronts harmless.
>
> Memory peg: **don't send a thousand scouts looking for water — let the water flood toward them.** One pond, many sources, ripples outward.

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: two graph nodes with an arrow, one holding a nested `[val, neighbors]`. Title blurred: "Clone Graph (LC 133)".]**

> We've been treating grids as graphs. But sometimes the interviewer hands you an *actual* graph — a web of node objects with pointers to each other — and says "make me a perfect copy." Sounds easy, until the cycles send your copy into infinite recursion. The fix is one clever hash map. That's next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[][] updateMatrix(int[][] mat) {
    int rows = mat.length, cols = mat[0].length;
    int[][] dist = new int[rows][cols];
    Queue<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (mat[r][c] == 0) q.offer(new int[]{r, c});
            else dist[r][c] = -1;               // unvisited
        }
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    while (!q.isEmpty()) {
        int[] cell = q.poll();
        for (int[] d : dirs) {
            int nr = cell[0] + d[0], nc = cell[1] + d[1];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && dist[nr][nc] == -1) {
                dist[nr][nc] = dist[cell[0]][cell[1]] + 1;
                q.offer(new int[]{nr, nc});
            }
        }
    }
    return dist;
}
```
