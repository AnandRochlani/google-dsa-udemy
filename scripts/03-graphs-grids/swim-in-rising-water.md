# 🎬 Recording Script — Swim in Rising Water
**Pattern: Dijkstra / min-heap (minimize the maximum) · LeetCode 778 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** plain Dijkstra with a running *sum* (Network Delay Time) — watch the one thing we swap.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an n×n grid of elevation numbers. Blue water rises from the bottom, ticking a clock: t=0, 1, 2… A swimmer icon waits at the top-left corner, unable to move.]**

> Google onsite. The interviewer draws a grid of heights and says: *"It's raining. At time `t`, water sits at level `t`. You can only swim through cells the water has covered. Least time to get from this corner to the opposite corner. Go."*
>
> Your gut says: simulate it. Raise the water one unit at a time, check if you can cross yet. And that *works* — until the grid is big and you've re-scanned it a thousand times.
>
> Here's the twist that flips this from Hard to easy: the time you need isn't about how far you swim. It's about **one number** on your route. Find that number, and the whole problem collapses into a search you already know. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a 2×2 grid of tiles:]**

```
0  2
1  3
```

> The whole problem in one line: **water rises to level `t`; a cell opens up when `t` reaches its elevation; find the least `t` that lets you swim from the top-left to the bottom-right.**
>
> Movement between two open cells is instant — the *only* thing you wait on is the water. Here's our tiny example: four cells. Start on the `0`, finish on the `3`.
>
> Keep your eye on this grid. The answer is **3** — but don't take my word for it. We'll see *why* by hand before we write a line of code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the 2×2 grid. A water-level slider on the left. A "full grid scans" counter, top-right, at 0. The slider steps t=0, then 1, then 2, then 3, re-flooding each time.]**

> Let's do what your brain does first: try every water level, low to high, and each time flood-fill from the start to see if the corner is reachable.
>
> **t = 0:** only the `0` cell is open. Stuck on the start. Scan #1.
>
> **[VISUAL: only top-left glows; counter → 1.]**
>
> **t = 1:** the `0` and the `1` open up. I can go down to the `1`… but the corner's a `3`, still dry. Stuck. Scan #2.
>
> **t = 2:** now `0`, `1`, `2` are open. Still can't touch the `3`. Scan #3.
>
> **t = 3:** finally the `3` opens. Path exists. Answer 3 — but look at the counter.
>
> **[VISUAL: counter → 4; then morphs to "O(n²) levels × O(n²) scan = O(n⁴)" in red.]**
>
> Four full grid scans for four tiny cells. On a 50×50 grid that's thousands of levels, each triggering a fresh flood-fill. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the winning path 0 → 1 → 3. The three cells pulse. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So here's the waste: I searched over *time*, re-scanning the grid at every level. But look at the path that finally won — `0`, then `1`, then `3`. Which of those numbers actually decided my answer?
>
> **LEARNER:** …the `3`. The other cells were already open way earlier. I was really just waiting for the highest cell on the path to get wet.
>
> **TEACHER:** Exactly. Pause the video and sit with that. The time a path costs you isn't its length, and it isn't the sum of its cells. It's **one** cell — the biggest one on the route. So what should we actually be searching for?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two candidate paths from start to corner drawn side by side; each path's highest cell lights up bright red with its value labeled "cost of this path".]**

> **TEACHER:** Reframe the whole thing. A path is only crossable once the water covers **every** cell on it — so the earliest you finish that path is the moment the water reaches its **highest** cell. The path's cost is its peak.
>
> Think of a hiking trail between two towns. The trail's difficulty isn't its length — it's the tallest pass you have to climb over. You want the route with the **lowest** high point.
>
> **[VISUAL: two mountain trails; the one with the lower summit gets a green check.]**
>
> So the question isn't "search over time." It's: over all paths from corner to corner, find the one whose **maximum cell is as small as possible.** Minimize the maximum. A *minimax path.*
>
> **LEARNER:** That smells like Dijkstra — shortest path with a priority queue. But Dijkstra adds up edge weights. Here I don't want a sum at all.
>
> **TEACHER:** And that's the entire trick. It *is* Dijkstra — you just change what "distance" means. Instead of the running **sum** of what you've stepped on, your key is the running **max**. Cost to stand on the next cell equals `max(the peak so far, this new cell)`. Everything else about Dijkstra — the min-heap, settling each node once — stays exactly the same.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "minimize the MAX on a path ⇒ Dijkstra, but key = max(so far, next) not sum."]**

> Burn this one line in: **when a path's cost is its worst step, not its total, run Dijkstra with a running MAX instead of a running sum.**
>
> That's the whole lesson, and it transfers. Minimize the maximum? Min-heap on max. Maximize the minimum? Flip to a max-heap on min. Same skeleton, one substitution.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Chunk one — the heap starts at the corner we're leaving, and its key is that cell's own elevation. We also track which cells we've settled.

```python
import heapq

def swim_in_water(grid):
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]   # (max elevation on path so far, r, c)
    seen = {(0, 0)}
```

> **[VISUAL: add chunk 2, highlight it.]** The loop — always pop the cell reachable with the *smallest* peak. And the payoff line: if that cell is the corner, we're done.

```python
    while heap:
        t, r, c = heapq.heappop(heap)
        if r == n - 1 and c == n - 1:
            return t              # first pop of the corner IS the answer
```

> **[VISUAL: add chunk 3.]** Look at all four neighbors, skip anything off-grid or already settled.

```python
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
```

> **[VISUAL: add chunk 4, highlight the `max(t, ...)` push.]** And the heart of it — push the neighbor with the *worse* of the peak so far and the neighbor's own height.

```python
                seen.add((nr, nc))
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
```

> That `max` is the entire algorithm. Everything else is plumbing you've written before.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `heap = [(grid[0][0], 0, 0)]` — you're standing on the start, so the peak so far is just its own elevation. That's your floor.
>
> `heapq.heappop` — the min-heap hands back the cell reachable with the smallest peak *anywhere on the frontier*. That ordering is what makes Dijkstra Dijkstra.
>
> `if corner: return t` — we return **the instant we pop it**, not when we first *see* it. Big difference.
>
> **LEARNER:** Hold on — why return on the *pop*, not when we first push the corner onto the heap? We might reach it earlier.
>
> **TEACHER:** Because "first reached" isn't "best reached." The first time we *touch* the corner might be via an ugly high-peak path. The heap could still be holding a gentler route with a lower peak that just hasn't surfaced yet. Only when the corner is **popped** are we guaranteed nothing cheaper remains — every path with a smaller peak has already come out ahead of it. Pop, not push. That's the Dijkstra discipline.
>
> `max(t, grid[nr][nc])` — the cost to *stand on* the neighbor is the worse of two things: the peak I already had to climb, and this neighbor's own height. And notice — `max(t, anything) >= t`. The cost can never go *down* as I extend a path. That non-decreasing property is exactly the "no negative edges" rule Dijkstra needs to be correct. It's not an accident; it's why this is allowed to be Dijkstra at all.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the 2×2 grid; a trace table filling row by row; the heap shown as a sorted list on the side.]**

```
0  2
1  3
```

> Let's run the actual code. Target is the bottom-right `3` at position `(1,1)`.

| Pop `(t, r, c)` | Corner? | Push neighbors `(max(t, elev), r, c)` | Heap after |
|---|---|---|---|
| `(0, 0, 0)` | no | down→`max(0,1)=1`; right→`max(0,2)=2` | `(1,1,0), (2,0,1)` |
| `(1, 1, 0)` | no | right→`max(1,3)=3` | `(2,0,1), (3,1,1)` |
| `(2, 0, 1)` | no | down `(1,1)` already seen | `(3,1,1)` |
| `(3, 1, 1)` | **yes** | — | **return 3** |

> Watch the heap always surface the smallest peak first: `0`, then `1`, then `2`, then finally `3`. We pop the corner carrying a peak of `3`, and that's our answer — exactly the **3** we promised in the cold open. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute (scan every level): O(n⁴). Ours: O(n² log n). Note: "n² cells settled once × log n per heap op".]**

> **TEACHER:** Say it the way you'd say it in the room: *"There are n² cells, each settled exactly once. Every heap push or pop is log of n², which is O(log n). So it's O(n² log n) time, and O(n²) space for the heap and the seen set. Compare that to the brute force — scanning every water level and re-flooding — which is O(n⁴)."*
>
> And a bonus line that scores points: *"I could also binary-search the time and BFS for feasibility, since 'can I cross by time t' only ever flips from no to yes — it's monotonic. Same O(n² log n). Or Union-Find, adding cells in increasing height until the two corners join."* Naming the cousins shows range.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the seen-grid and the heap; a "roll to one row?" thought bubble appears, then gets a red ✗.]**

> Quick but important — honesty scores here.
>
> Can we shrink the `O(n²)`? **No — and I can say exactly why.** Best-first search needs two things: a record of which cells are settled, and a frontier of candidates in the heap. Both can grow to the whole grid. And there's no rolling-row trick like some DP tables, because the frontier isn't stuck on one row — a cell's best path can arrive from *any* direction, so I can't throw rows away as I go.
>
> Say it out loud in the interview: *"Space is O(n²) and that's optimal — I need settled-cell tracking plus a heap frontier, both bounded by the grid, and there's no rolling-window trick because the frontier spreads in every direction."* Naming *why* it can't shrink beats silently accepting it.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Path With Minimum Effort (LC 1631)". A blank editor.]**

> Before the next video, try **Path With Minimum Effort**. Same exact skeleton — Dijkstra with a min-heap keyed on a running max — but instead of the cell's elevation, the cost is the **absolute height difference** between adjacent cells, and you minimize the largest jump on the route.
>
> Don't peek. Wrestle with it for ten minutes. See if you can spot that it's *this* problem wearing a different coat. That recognition is the whole skill.

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **A path's cost is its highest cell, not its length or sum.** Reframe first, code second.
> 2. **Minimize-the-max ⇒ Dijkstra with a running max.** One substitution: `sum` becomes `max`.
> 3. **Return on the POP of the target, not the first sighting** — that's the Dijkstra guarantee.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "worst step, not total steps ⇒ min-heap on max."]**
>
> When a route's difficulty is its single worst step, your hand should already be reaching for Dijkstra — with `max` where the sum used to be.
>
> *(GCA reminder — for the interview itself: don't jump to the heap. First *narrate the reframe* out loud — "the cost of a path is its peak cell" — then reach for Dijkstra. Google's General Cognitive Ability signal isn't the code; it's you saying the minimax insight before you write it. Ask the clarifying question up front too: "movement is free, only the water gates me, right?")*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Cheapest Flights Within K Stops" — a graph with a "≤ K hops" badge and a red warning on a node.]**

> Here, plain Dijkstra worked because nothing constrained our path except the water. But what happens when the problem adds a *second* rule — "get there cheapest, but in **at most K stops**"? Suddenly settling each node once isn't safe anymore, and vanilla Dijkstra quietly gives the wrong answer. That's the next one: Cheapest Flights Within K Stops — where the constraint breaks the heap, and we fix it. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int swimInWater(int[][] grid) {
    int n = grid.length;
    // min-heap keyed by the max elevation on the path so far
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    boolean[][] seen = new boolean[n][n];
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    pq.offer(new int[]{grid[0][0], 0, 0});   // {runningMax, row, col}
    seen[0][0] = true;

    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int t = cur[0], r = cur[1], c = cur[2];
        if (r == n - 1 && c == n - 1) return t;   // first pop of corner = answer
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc]) {
                seen[nr][nc] = true;
                pq.offer(new int[]{Math.max(t, grid[nr][nc]), nr, nc});
            }
        }
    }
    return -1;   // unreachable for a valid grid
}
```
