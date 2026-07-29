# Max Area of Island

> **LeetCode:** 695. Max Area of Island · **Difficulty:** 🟡 Medium · **Pattern:** Grid DFS / Flood Fill · **Google frequency:** medium

---

## Problem

Given an `m × n` binary grid where `1` is land and `0` is water, an **island** is a group of `1`s connected **4-directionally** (up/down/left/right). Return the **area of the largest island** (number of `1` cells). If there's no land, return `0`.

**Example:**
```
grid = [[0,0,1,0,0],
        [0,1,1,0,0],
        [0,0,0,1,1],
        [0,0,0,1,1]]
```
→ `4`. Two islands: the top-left blob (cells (0,2),(1,1),(1,2)) has area 3; the bottom-right blob has area 4 → answer 4.

**Constraints that matter:** grid up to `50 × 50`. Small, so complexity isn't the worry — correctness is. The core skill is **connected-component flood fill**: visit every cell once, and when you land on unvisited land, explore its whole island while counting cells, without double-counting.

---

## 🧠 Intuition — how you'd actually arrive at this

- **The realization:** an island is a **connected component** of `1`s. "Largest island" = "largest connected component by cell count." So the plan is: scan the grid; each time you hit a `1` you haven't visited, that's a *new* island — explore all of it, count its cells, and track the max.
- **How to explore one island:** from a land cell, recurse into its four neighbors that are also land. That's **DFS flood fill**. Each recursive call returns the area contributed by that cell plus everything reachable from it: `1 + dfs(up) + dfs(down) + dfs(left) + dfs(right)`.
- **How to avoid infinite loops / double counting:** the moment you enter a land cell, **mark it visited** — the simplest way is to overwrite it to `0` (sink it). Then it can never be counted again, and you don't need a separate visited set.
- **Why the outer scan is still cheap:** every cell is entered at most once (it's sunk on first visit), so the total work is O(m·n) even though we launch a DFS per island — the DFSs partition the grid.
- **Pattern trigger:** *"connected regions in a grid"* → **DFS/BFS flood fill, sink visited cells**. Returning the area (a number) rather than just marking is the twist that makes this "max area" instead of "count islands."

---

## ① Brute Force

There isn't a meaningfully different "slow" algorithm — you must visit the cells. The naive-but-clunky version uses a **separate `visited` set** instead of sinking cells (extra memory, more bookkeeping):

```python
def maxAreaOfIsland_visited(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r < 0 or r >= m or c < 0 or c >= n
                or grid[r][c] == 0 or (r, c) in visited):
            return 0
        visited.add((r, c))
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)

    best = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1 and (r, c) not in visited:
                best = max(best, dfs(r, c))
    return best
```

**Why it's the natural first attempt:** a `visited` set is the textbook way to avoid revisiting nodes in any graph traversal.

**Why we improve it:** it's already O(m·n) time, but the extra `visited` set costs **O(m·n) space** on top of the recursion. If we're allowed to mutate the grid, we can drop it entirely by sinking cells.

**Complexity:** Time `O(m·n)`, Space `O(m·n)` (visited set + recursion stack).

---

## ② Optimised Solution

DFS flood fill that **sinks** each visited cell to `0`, so no separate visited structure is needed. Each `dfs` returns the area of the island rooted at that cell.

```python
def maxAreaOfIsland(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
            return 0
        grid[r][c] = 0                      # sink: mark visited
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)

    best = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:             # unvisited land → new island
                best = max(best, dfs(r, c))
    return best
```

**Walk the example** (bottom-right island): the outer scan reaches cell `(2,3)` which is `1`. `dfs(2,3)` sinks it (count so far 1), recurses to `(2,4)` land (2), `(3,3)` land (3), `(3,4)` land (4); all further neighbors are water or already sunk → returns **4**. The top-left island returns **3** by the same process. `best = max(3, 4) = 4`.

**Why it's correct:** sinking a cell on entry guarantees each land cell is counted exactly once, so a single DFS from any cell of an island visits and counts that entire island and nothing else. The outer loop starts a fresh DFS only on still-standing land, so every island is measured exactly once; `best` keeps the maximum.

**Complexity:** Time `O(m·n)` — every cell is touched a constant number of times. Space `O(m·n)` worst case for the **recursion stack** (a grid that's all land forms one snake-like path).

---

## ③ Space Optimization

Time is already optimal (you must inspect every cell). The space you can attack is the **recursion stack**, which is O(m·n) in the worst case — a stack-overflow risk on large all-land grids. Use an explicit-stack **iterative DFS** (or BFS with a queue) to keep the depth under your control:

```python
def maxAreaOfIsland_iterative(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    best = 0
    for sr in range(m):
        for sc in range(n):
            if grid[sr][sc] != 1:
                continue
            area = 0
            stack = [(sr, sc)]
            grid[sr][sc] = 0                # sink on push to avoid re-queueing
            while stack:
                r, c = stack.pop()
                area += 1
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 0    # sink when pushed
                        stack.append((nr, nc))
            best = max(best, area)
    return best
```

**Honest accounting:** this trades the call stack for an explicit stack, so worst-case auxiliary space is still **O(m·n)** — but it's heap memory you control, not the call stack, so it won't blow the recursion limit. Sinking cells means we use **no separate visited set** — that's the real space win over the brute force (O(m·n) → we mutate the grid in place). If mutating the input is disallowed, restore the grid afterward or keep the visited set and accept the extra space.

> Say it out loud: *"I sink visited cells to avoid a visited set. Recursion is cleanest but risks a deep stack on an all-land grid, so if that's a concern I'd switch to an explicit stack — same asymptotic space, but no recursion-limit blowup."*

---

## Java (for Java interviewers)

```java
public int maxAreaOfIsland(int[][] grid) {
    int m = grid.length, n = grid[0].length, best = 0;
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) {
            if (grid[r][c] == 1) best = Math.max(best, dfs(grid, r, c));
        }
    }
    return best;
}

private int dfs(int[][] grid, int r, int c) {
    if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] == 0)
        return 0;
    grid[r][c] = 0;                          // sink
    return 1 + dfs(grid, r + 1, c) + dfs(grid, r - 1, c)
             + dfs(grid, r, c + 1) + dfs(grid, r, c - 1);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| DFS with visited set | O(m·n) | O(m·n) (set + stack) |
| DFS sinking cells (recursive) | O(m·n) | O(m·n) recursion worst case |
| Iterative DFS / BFS, sinking | O(m·n) | O(m·n) explicit stack/queue |

---

## Say it out loud (interview narration)

> *"An island is a connected component, so I scan the grid and every time I hit unvisited land I flood-fill it with DFS, counting cells. Each DFS returns 1 plus the areas of its four neighbors. To avoid double-counting I sink each cell to 0 the moment I visit it — that doubles as my visited marker, so no extra set. I track the max area across islands. It's O(m·n) time since each cell is touched once. Recursion depth can be O(m·n) on an all-land grid, so if that's a risk I'd use an explicit stack instead."*

## Related / follow-ups
- **Number of Islands** (200) — count components instead of measuring area; same flood fill.
- **Island Perimeter** (463) — count boundary edges during the traversal.
- **Flood Fill** (733) — the bare paint-bucket version.
- **Number of Connected Components in an Undirected Graph** (323) — same idea, general graph / union-find.
