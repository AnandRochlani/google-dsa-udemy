# Shortest Path in a Grid with Obstacles Elimination

> **LeetCode:** 1293. Shortest Path in a Grid with Obstacles Elimination · **Difficulty:** 🔴 Hard · **Pattern:** BFS with extra state · **Google frequency:** ⭐ high

---

## Problem

You're given an `m × n` grid where each cell is `0` (empty) or `1` (obstacle). You start at the top-left `(0, 0)` and want to reach the bottom-right `(m-1, n-1)` in the **fewest steps** — moving up, down, left, or right. The twist: you may **eliminate up to `k` obstacles** along the way. Walking onto a `1` is allowed, but it spends one of your `k` eliminations. Return the minimum number of steps, or `-1` if you can't reach the end even with all `k` eliminations.

**Example:** `grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]`, `k = 1` → `6`

This is a 5×3 grid. The straight-line minimum is `m + n - 2 = 6` steps. Without any elimination you'd need a **10-step** detour, because the obstacle walls force you to snake around. Spend your one elimination to punch through the `1` at `(3, 2)` and you get a clean 6-step path: `(0,0)→(0,1)→(0,2)→(1,2)→(2,2)→(3,2)✳→(4,2)`.

**Constraints that matter:** `m, n` up to 40 and `k` up to `m*n` (~1600). A grid has only `m*n` cells, so plain BFS would be `O(m*n)` — trivial. The catch is that plain BFS is **wrong** here, and the fix multiplies the state space by `k`. Your target is `O(m*n*k)` — comfortably fast for 40×40, but you have to get the *state* right or you'll either output a wrong answer or blow up exponentially.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Shortest path, unweighted grid, all moves cost 1 step — that's textbook **BFS**. Flood out from `(0,0)`, first time I touch `(m-1, n-1)` is the answer." Correct reflex. BFS on an unweighted graph gives shortest steps for free. So you write it, mark cells visited by `(row, col)`, and… you get wrong answers.
- **Where it hurts:** the bug is in *what "visited" means*. In vanilla BFS, once you've reached a cell you never revisit it — the first arrival is always at least as good. **That assumption breaks here.** Two BFS paths can arrive at the same cell after the same number of steps but with a *different number of eliminations left*. One arrived with 3 eliminations still in the bank; the other burned them all and has 0. Those are **not the same situation** — the one with more budget can go places the other can't. If you mark the cell "visited" on the first arrival and block the second, you might block the *only* path that actually reaches the goal.
- **The leap:** the "position" isn't just where you are on the grid — it's where you are **plus how much elimination budget you have left**. Promote the state from `(row, col)` to `(row, col, k_remaining)`. Now BFS is correct again: you're doing shortest-path over a bigger graph where each cell is split into `k+1` copies, one per budget level. Two arrivals only collide if they match on *all three* coordinates.
- **Pattern trigger:** **"BFS is the right shape, but the naive state gives wrong answers"** → **BFS with extra state**. The transferable move: when a resource (budget, keys collected, parity, remaining moves) changes what you can do *next*, fold that resource into the node. The signal is a plain shortest-path problem carrying a side-quantity that isn't captured by position alone.

---

## ① Brute Force

Explore **every** path with DFS, carrying the remaining budget, and keep the shortest that reaches the end.

```python
def shortestPath_brute(grid, k):
    m, n = len(grid), len(grid[0])
    best = [float('inf')]

    def dfs(r, c, rem, steps, visited):
        if rem < 0:                       # spent more eliminations than we had
            return
        if steps >= best[0]:              # this route is already no better — cut it
            return
        if r == m - 1 and c == n - 1:
            best[0] = min(best[0], steps)
            return
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                visited.add((nr, nc))
                dfs(nr, nc, rem - grid[nr][nc], steps + 1, visited)
                visited.remove((nr, nc))  # backtrack — this cell is free again

    dfs(0, 0, k, 0, {(0, 0)})
    return best[0] if best[0] != float('inf') else -1
```

**Why it's the natural first attempt:** it's honest and obviously correct — try all the ways, respect the budget, take the shortest. It captures the elimination logic without any cleverness, and it's a great sanity oracle for testing the fast version.

**Why it's not enough:** it enumerates essentially every simple path in the grid, which is **exponential** — on a 40×40 grid it never finishes. The `steps >= best[0]` prune helps in practice but doesn't change the worst case. This is the classic "correct but times out" Hard: right answer, wrong asymptotics.

**Complexity:** Time `O(4^(m*n))` in the worst case, Space `O(m*n)` for the recursion stack and visited set.

---

## ② Optimised Solution

BFS — but over the **enriched state** `(row, col, k_remaining)`. BFS explores in step order, so the **first** time we pop the goal cell, that step count is the shortest. Guard revisits with a `visited` set keyed on all three coordinates.

```python
from collections import deque

def shortestPath(grid, k):
    m, n = len(grid), len(grid[0])

    # Shortcut: if the budget covers a whole straight-line's worth of obstacles,
    # nothing can force a detour — the Manhattan distance is achievable.
    if k >= m + n - 2:
        return m + n - 2

    # State = (row, col, eliminations_left). Two arrivals differ if budgets differ.
    start = (0, 0, k)
    visited = {start}
    queue = deque([(0, 0, k, 0)])         # r, c, remaining, steps

    while queue:
        r, c, rem, steps = queue.popleft()
        if r == m - 1 and c == n - 1:     # first pop of the goal = shortest
            return steps
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                nrem = rem - grid[nr][nc]          # stepping on a 1 spends one
                state = (nr, nc, nrem)
                if nrem >= 0 and state not in visited:
                    visited.add(state)
                    queue.append((nr, nc, nrem, steps + 1))
    return -1
```

**Walk the example** `grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]`, `k = 1`. The winning frontier reaches the goal in 6 steps by spending the single elimination on `(3,2)`:

| Step | Cell | `grid` value | Budget left | Note |
|---|---|---|---|---|
| 0 | `(0,0)` | 0 | 1 | start |
| 1 | `(0,1)` | 0 | 1 | slide right, still full budget |
| 2 | `(0,2)` | 0 | 1 | right again |
| 3 | `(1,2)` | 0 | 1 | drop down the open column |
| 4 | `(2,2)` | 0 | 1 | down |
| 5 | `(3,2)` | 1 | **0** | ✳ eliminate — budget spent |
| 6 | `(4,2)` | 0 | 0 | **goal popped → return 6** |

Meanwhile a *different* frontier reaches `(2,2)` having already burned its elimination elsewhere — budget `0`. Because our `visited` key includes the budget, that arrival is stored as a **separate** state `(2,2,0)`, distinct from `(2,2,1)`. Plain 2-D visited would have collapsed them and possibly discarded the branch that still had budget to punch through `(3,2)`.

**Why it's correct:** two properties. **(1)** BFS over an unweighted graph visits nodes in nondecreasing step order, so the first pop of any state is via a shortest path to it — dequeuing the goal gives the true minimum. **(2)** By keying `visited` on `(r, c, rem)`, we only skip a state we've genuinely seen before, at equal-or-fewer steps. We never wrongly prune the higher-budget twin of a cell, so no reachable-with-eliminations route is lost. The `if k >= m + n - 2` shortcut is a pure speedup: the shortest possible route is the Manhattan distance `m + n - 2`, which passes through at most that many cells beyond the start; if you can eliminate that many obstacles, no wall can force a longer path.

**Complexity:** Time `O(m*n*k)` — the graph has `m*n*(k+1)` states and each is processed once with 4 neighbors. Space `O(m*n*k)` for the `visited` set and queue.

---

## ③ Space Optimization

The `visited` set above can hold up to `m*n*(k+1)` entries — one per `(cell, budget)`. We can shrink the **bookkeeping to `O(m*n)`** with one observation: **more budget is never worse.** If we've already reached a cell in the same number of steps (or fewer) with *at least as much* budget left, a new arrival with *less* budget can't unlock anything the earlier one couldn't. So instead of remembering every `(cell, budget)` pair, remember only the **best budget seen so far at each cell**, and admit a new arrival only if it strictly beats that.

```python
from collections import deque

def shortestPath(grid, k):
    m, n = len(grid), len(grid[0])
    if k >= m + n - 2:
        return m + n - 2

    # best[cell] = the most elimination budget we've ever arrived with.
    # A new arrival is worth exploring ONLY if it brings strictly more budget.
    best = {(0, 0): k}
    queue = deque([(0, 0, k, 0)])          # r, c, remaining, steps

    while queue:
        r, c, rem, steps = queue.popleft()
        if r == m - 1 and c == n - 1:
            return steps
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                nrem = rem - grid[nr][nc]
                if nrem >= 0 and nrem > best.get((nr, nc), -1):
                    best[(nr, nc)] = nrem   # this cell now has a richer arrival
                    queue.append((nr, nc, nrem, steps + 1))
    return -1
```

**Complexity:** Time `O(m*n*k)` (unchanged — a cell can still be admitted up to `k` times as budget improves), Space `O(m*n)` for the `best` map. That's the win: the visited structure drops from a 3-D cube to a 2-D grid.

> Say it out loud: *"I don't need to remember every budget level per cell — only the richest one. A poorer arrival can never reach somewhere the richer one couldn't, so I prune it. That takes my visited memory from `O(m·n·k)` down to `O(m·n)`."* Naming *why* the poorer arrival is safe to drop is the strong-hire signal — it shows you understand the invariant, not just the code.

---

## Java (for Java interviewers)

```java
public int shortestPath(int[][] grid, int k) {
    int m = grid.length, n = grid[0].length;
    // Shortcut: enough budget to punch straight through any wall.
    if (k >= m + n - 2) return m + n - 2;

    // best[r][c] = most elimination budget we've ever arrived at this cell with.
    int[][] best = new int[m][n];
    for (int[] row : best) java.util.Arrays.fill(row, -1);
    best[0][0] = k;

    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    // queue holds {row, col, remaining, steps}
    Deque<int[]> queue = new ArrayDeque<>();
    queue.offer(new int[]{0, 0, k, 0});

    while (!queue.isEmpty()) {
        int[] cur = queue.poll();
        int r = cur[0], c = cur[1], rem = cur[2], steps = cur[3];
        if (r == m - 1 && c == n - 1) return steps;   // first pop = shortest
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
            int nrem = rem - grid[nr][nc];             // stepping on a 1 costs one
            if (nrem >= 0 && nrem > best[nr][nc]) {     // only if strictly richer
                best[nr][nc] = nrem;
                queue.offer(new int[]{nr, nc, nrem, steps + 1});
            }
        }
    }
    return -1;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (enumerate all paths, DFS) | O(4^(m·n)) | O(m·n) |
| Optimised (BFS on `(r, c, rem)`, 3-D visited) | O(m·n·k) | O(m·n·k) |
| Space-optimised (BFS, best-budget-per-cell) | O(m·n·k) | O(m·n) |

*(m, n = grid dimensions; k = elimination budget, capped by `m·n`.)*

---

## Say it out loud (interview narration)

> *"Shortest steps on an unweighted grid screams BFS — but I need to be careful about what 'visited' means. The catch is that reaching a cell with 3 eliminations left is different from reaching it with 0 left; the richer one can go places the poorer one can't. So plain 2-D visited is wrong. I promote the state to `(row, col, eliminations_remaining)` and run BFS over that — first time I pop the goal is the shortest path. That's `O(m·n·k)` time and space. One clean optimization: I don't need every budget level per cell, only the highest one I've arrived with, since more budget is never worse — that drops my visited memory to `O(m·n)`. And a quick shortcut up front: if `k` is at least `m + n − 2`, I can punch straight through any wall, so the answer is just the Manhattan distance."*

Before you code, ask the one clarifying question that proves you read the spec: *"Does stepping onto an obstacle consume an elimination even if I could have gone around, and do I return -1 only when the goal is unreachable with all k used?"* Narrating that state-design decision out loud — *why* position alone isn't enough — is exactly the General Cognitive Ability signal Google's rubric rewards.

## Related / follow-ups
- **Shortest Path in Binary Matrix (LC 1091)** — the same BFS-for-shortest-steps reflex, but plain 2-D state suffices; a good contrast for *when* you do and don't need extra state.
- **Shortest Path to Get All Keys (LC 864)** — BFS with extra state again, but the side-quantity is a **bitmask of keys collected** instead of a budget count.
- **Minimum Obstacle Removal to Reach Corner (LC 2290)** — same grid, but you minimize obstacles removed instead of steps → **0-1 BFS / Dijkstra**.
- **Trapping Rain Water II / Swim in Rising Water (LC 778)** — grid shortest-path where the edge cost isn't 1, pushing you from BFS to Dijkstra.
