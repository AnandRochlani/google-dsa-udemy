# Swim in Rising Water

> **LeetCode:** 778. Swim in Rising Water · **Difficulty:** 🔴 Hard · **Pattern:** Dijkstra / min-heap (minimize the maximum) · **Google frequency:** ⭐ high

---

## Problem

You're given an `n × n` grid where `grid[r][c]` is the **elevation** of that cell. Rain falls, and at time `t` the water level everywhere is `t`. You can stand on a cell only once the water has risen to at least its elevation — i.e. cell `(r, c)` is *swimmable* at time `t` when `elevation <= t`. From a swimmable cell you may swim to a 4-directionally adjacent cell (up/down/left/right) in zero time, **as long as both cells are under water** (both elevations `<= t`). You start at the top-left `(0, 0)` and want to reach the bottom-right `(n-1, n-1)`. Return the **least time `t`** at which you can make it across.

**Example:** `grid = [[0,2],[1,3]]` → `3` *(you must pass through the `3` cell to reach the corner, so you can't arrive before the water hits 3)*

**Constraints that matter:** `n` is up to 50, so the grid has up to `2500` cells. Elevations are a permutation of `0 … n²−1` (every value distinct). Small `n` — but the trap is in *how* you search. A naive "try every time step and re-scan the whole grid" is `O(n⁴)`; the intended answer runs in `O(n² log n)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "The answer is some time `t`. Let me just try `t = 0, 1, 2, …` and, for each, flood-fill from the corner to see if I can reach the far corner using only cells `<= t`. The first `t` that connects is my answer." That works — and it's the seed of a correct solution. But you're re-running a whole BFS for every candidate time.
- **Where it hurts:** two separate wastes. First, you scan `t` linearly across up to `n²` values, re-doing a full grid search each time — that's `O(n²)` searches × `O(n²)` each = `O(n⁴)`. Second, and deeper: you're treating this as "search over time," when really the *time you need is a property of the path itself*.
- **The leap:** flip the framing. Walk any path from start to finish. When can you complete it? Only once the water covers **every** cell on that path — so the time this path costs you is the **single highest elevation** it steps on. Not the sum. Not the length. The **max**. So the whole question becomes: over all paths from corner to corner, find the one whose **maximum cell is as small as possible**. That's a classic **minimax path** problem.
- **Pattern trigger:** *"minimize the maximum edge/cell along a path"* → **Dijkstra with a min-heap, but the key is the running MAX instead of the running SUM.** Any time the cost of a route is its worst step rather than its total, swap "sum" for "max" in Dijkstra and it just works. That one substitution is the transferable lesson.

---

## ① Brute Force

Guess the time. For each candidate `t` from `0` upward, run a plain DFS/BFS from `(0,0)` over cells with elevation `<= t`; return the first `t` that reaches the corner.

```python
def swim_in_water_brute(grid):
    n = len(grid)

    def can_reach(t):
        # is the corner reachable using only cells with elevation <= t?
        if grid[0][0] > t:
            return False
        stack, seen = [(0, 0)], {(0, 0)}
        while stack:
            r, c = stack.pop()
            if (r, c) == (n - 1, n - 1):
                return True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (0 <= nr < n and 0 <= nc < n
                        and (nr, nc) not in seen
                        and grid[nr][nc] <= t):
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return False

    for t in range(n * n):            # try every possible water level
        if can_reach(t):
            return t
```

**Why it's the natural first attempt:** it mirrors the physical picture — the water rises one unit at a time, and you keep checking "can I get across yet?" until you can.

**Why it's not enough:** you re-run an entire grid search for every one of the `n²` time levels, so it's `O(n⁴)`. The obvious patch is to **binary search** on `t` (feasibility is monotonic — if you can cross at time `t`, you can cross at any larger `t`), which cuts it to `O(n² log n)`. That's already good. But we can get the same bound with a single, cleaner pass that never guesses `t` at all — by searching the *paths* directly.

**Complexity:** Time `O(n⁴)` (linear scan) → `O(n² log n)` (binary-search variant), Space `O(n²)`.

---

## ② Optimised Solution

Treat cells as graph nodes. Run **Dijkstra / best-first search** from `(0,0)`, but the "distance" to a cell is the **maximum elevation on the best path reaching it so far**. A min-heap always hands you the cell with the smallest running-max. The moment you pop the target, its running-max **is** the answer.

```python
import heapq

def swim_in_water(grid):
    n = len(grid)
    # heap entries: (max elevation on the path so far, r, c)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}

    while heap:
        t, r, c = heapq.heappop(heap)     # smallest running-max first
        if r == n - 1 and c == n - 1:
            return t                       # first time we pop the corner = answer
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                # cost to stand on the neighbor = worse of (path so far, this cell)
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
```

**Walk the example** `grid = [[0,2],[1,3]]` (target is `(1,1)`):

| Step | Pop `(t, r, c)` | At corner? | Neighbors pushed `(max(t, elev), r, c)` | Heap after |
|---|---|---|---|---|
| 1 | `(0, 0, 0)` | no | down `(1,0)`→`max(0,1)=1`; right `(0,1)`→`max(0,2)=2` | `(1,1,0), (2,0,1)` |
| 2 | `(1, 1, 0)` | no | right `(1,1)`→`max(1,3)=3` | `(2,0,1), (3,1,1)` |
| 3 | `(2, 0, 1)` | no | down `(1,1)` already seen | `(3,1,1)` |
| 4 | `(3, 1, 1)` | **yes** | — | return **3** |

We reach the corner with running-max `3`. Both paths to the corner must cross either the `3` or… well, the `3` *is* the corner, so `3` is unavoidable. Answer `3`. ✅

**Why it's correct:** it's Dijkstra, and Dijkstra's guarantee carries over as long as the path cost never *decreases* when you extend a path. Here the cost is a running **max**, and `max(t, elevation) >= t` always — adding a cell can only keep the cost the same or push it up, never down. That monotonicity is exactly the non-negative-edge condition Dijkstra needs. So when a cell is first popped, no cheaper (lower-max) path to it can still exist, and its running-max is final. Pop the corner → that's the globally minimal possible maximum → the least survivable time.

**Complexity:** Time `O(n² log n)` — each of the `n²` cells is settled once, and every heap push/pop is `O(log n²) = O(log n)`. Space `O(n²)` for the heap and the `seen` set.

---

## ③ Space Optimization

**Already at the floor, and here's the honest reason.** Best-first search over a grid must be able to (a) remember which cells are settled and (b) hold the frontier of candidates. Both are bounded by the number of cells, `O(n²)`. There's no rolling-window trick like a 1-D DP, because the frontier can genuinely spread across the whole grid at once — a cell's best path can arrive from any direction, so you can't discard rows as you go.

```python
# Tiny constant-factor win only: replace the `seen` set with a boolean grid,
# and (optionally) skip stale heap entries instead of a membership test.
# The asymptotic bound does not move: still O(n^2) space, O(n^2 log n) time.
seen = [[False] * n for _ in range(n)]
```

> Say it out loud: *"Space is O(n²) and that's optimal — I need to track settled cells and a heap frontier, both bounded by the grid size. There's no rolling-row trick because the frontier isn't confined to one row; a cell's best path can come from any direction."* Naming *why* it can't shrink is the strong-hire move.

**Complexity:** Time `O(n² log n)`, Space `O(n²)`.

---

## Java (for Java interviewers)

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
                // cost of reaching neighbor = worse of (path so far, this cell)
                pq.offer(new int[]{Math.max(t, grid[nr][nc]), nr, nc});
            }
        }
    }
    return -1;   // unreachable for a valid grid
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (linear scan of `t` + BFS) | O(n⁴) | O(n²) |
| Binary search on `t` + BFS feasibility | O(n² log n) | O(n²) |
| Union-Find (add cells by increasing elevation) | O(n² α(n²)) | O(n²) |
| **Optimised — Dijkstra / min-heap on running-max** | **O(n² log n)** | **O(n²)** |

*(n = grid side length; the grid holds n² cells.)*

---

## Say it out loud (interview narration)

> *"First let me reframe the cost. The time a path costs isn't its length or the sum of elevations — it's the single highest cell it has to cross, because I can't move until the water covers that peak. So I want the path from corner to corner that minimizes its maximum cell — a minimax path. That's Dijkstra with one twist: instead of a running sum, my key is the running max, `max(pathSoFar, thisCell)`. A min-heap always pops the cell reachable with the smallest peak; the instant I pop the destination, that peak is the least time I need. It's O(n² log n) time, O(n²) space. As a sanity check I'd mention two cousins: binary-search the time and BFS for feasibility since 'can I cross by time t' is monotonic, or Union-Find, adding cells in increasing elevation order until start and end join — same bound, different flavor."*

Before coding, ask the one clarifying question that proves you read the spec: *"Movement itself is free — the only thing gating me is the water level, i.e. the max elevation on my route, right?"* Confirming the cost model out loud is exactly the General Cognitive Ability signal Google's rubric rewards.

## Related / follow-ups
- **Path With Minimum Effort (LC 1631)** — minimize the *maximum absolute difference* between adjacent cells on a path. Same Dijkstra-on-max skeleton.
- **Path With Maximum Minimum Value (LC 1102)** — mirror image: *maximize the minimum* cell on a path (max-heap instead of min-heap).
- **Kth Smallest Element in a Sorted Matrix (LC 378)** — another "binary search the answer" grid problem.
- **Network Delay Time (LC 743)** — plain Dijkstra with a running sum, to contrast the sum-vs-max substitution.
