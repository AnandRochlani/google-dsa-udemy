# Number of Islands

> **LeetCode:** 200. Number of Islands · **Difficulty:** 🟡 Medium · **Pattern:** Graph BFS/DFS (flood fill) · **Google frequency:** ⭐ high

---

## Problem

You're given a 2D grid of `'1'`s (land) and `'0'`s (water). An **island** is a group of `'1'`s connected **horizontally or vertically** (not diagonally). Count how many islands there are. The grid is surrounded by water on all sides.

**Example:**

```
grid =
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

→ `3` — the top-left 2×2 block is one island, the single `1` in the middle is another, and the bottom-right pair is the third.

**Constraints that matter:** grid up to `300 × 300` = 90,000 cells. We need to visit each cell a small constant number of times → target `O(rows × cols)`. The characters are `'1'`/`'0'` **strings**, not ints — easy to trip on in code.

---

## 🧠 Intuition — how you'd actually arrive at this

> The whole game is realizing a grid *is* a graph in disguise.

- **First instinct:** "I need to count connected blobs of land." How do you even define a blob? Two land cells are in the same blob if you can walk between them stepping only up/down/left/right on land.
- **The reframe — grid as graph:** treat **each cell as a node**. Draw an edge between two cells if they're adjacent (up/down/left/right) and *both* are land. Now "island" is exactly a **connected component** of that graph. Counting islands = counting connected components.
- **How do you count components?** Walk the grid. The moment you hit an unvisited land cell, you've found a *new* island — increment the counter, then **flood fill**: from that cell, visit every land cell reachable from it and mark them all seen, so you never start a second count inside the same island. DFS or BFS both flood-fill; pick either.
- **Where the naive version hurts:** if you flood without marking cells visited, you walk in circles forever — cell A visits neighbor B, B visits A again, infinite loop. The fix is a **visited set** (or overwriting the cell in place).
- **Pattern trigger:** **2D grid + "connected region / group / island"** → **flood fill (DFS/BFS) counting connected components.** Burn that in. "Number of X regions" almost always means this.

---

## ① Brute Force

The "natural but broken" first attempt: recurse into neighbors without tracking what you've visited.

```python
def numIslands_broken(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != '1':
            return
        # BUG: never marks (r, c) as visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count
```

**Why it's the natural first attempt:** the flood-fill shape is right — find a land cell, dive into its neighbors. This is how everyone first sketches it.

**Why it's not enough:** without marking cells visited, `dfs(r, c)` calls `dfs(r+1, c)`, which calls `dfs(r, c)` right back → **infinite recursion / stack overflow.** And even if you dodged the loop, you'd never stop re-counting the same island. It's not just slow — it's *wrong*.

**Complexity:** doesn't terminate. (If you imagine a version that revisits but somehow halts, it explodes exponentially.)

---

## ② Optimised Solution

Same flood fill, but **mark cells visited** so each cell is processed once. Here's the DFS version:

```python
def numIslands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != '1':
            return
        grid[r][c] = '#'          # mark visited (sink the land)
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)         # flood the whole island
    return count
```

And the **BFS** version (safer against deep recursion on big grids):

```python
from collections import deque

def numIslands_bfs(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                grid[r][c] = '#'
                q = deque([(r, c)])
                while q:
                    x, y = q.popleft()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                            grid[nx][ny] = '#'   # mark BEFORE enqueue (avoids dupes)
                            q.append((nx, ny))
    return count
```

**Walk the example:**

```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

1. Scan hits `(0,0)='1'` → `count=1`. Flood fill sinks `(0,0),(0,1),(1,0),(1,1)` to `'#'`. The 2×2 block is gone.
2. Scan continues, skips all `'#'` and `'0'`, reaches `(2,2)='1'` → `count=2`. It has no land neighbors; only `(2,2)` sinks.
3. Scan reaches `(3,3)='1'` → `count=3`. Flood sinks `(3,3),(3,4)`.
4. Nothing left. **Return 3.** ✅

**Why it's correct:** the outer double-loop guarantees we *start* a fill only at cells that haven't been swallowed by a previous island. Each fill marks its entire component, so a new `count++` happens exactly once per connected component — no double counting, no missed land.

**Complexity:** Time `O(rows × cols)` — every cell is enqueued/recursed at most once. Space `O(rows × cols)` worst case for the recursion stack / BFS queue (e.g. a grid that's all land).

---

## ③ Space Optimization

The solution above is **already space-optimized on the "visited" front**: instead of a separate `visited` set (which would cost an extra `O(rows × cols)`), we overwrite each land cell to `'#'` **in place**. That's the trick — the grid itself is the visited marker.

What we *can't* escape is the traversal frontier:
- **DFS** costs `O(rows × cols)` recursion stack in the worst case (a single snake-shaped island fills the call stack).
- **BFS** costs `O(min(rows, cols))`... no — worst case the queue also holds `O(rows × cols)` cells (imagine flooding an all-land grid; the frontier can be a whole diagonal band, up to `O(min(rows,cols))` at a time, but total cells touched is `rows×cols`). In practice the queue peak is `O(min(rows, cols))` for a full grid, which is better than DFS's stack.

> If the interviewer forbids mutating the input, restore each `'#'` back to `'1'` at the end, or use a separate `visited` set at `O(rows × cols)` extra space. Mention this tradeoff out loud — it shows you noticed you're modifying their data.

---

## Java (for Java interviewers)

```java
public int numIslands(char[][] grid) {
    if (grid == null || grid.length == 0) return 0;
    int rows = grid.length, cols = grid[0].length, count = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == '1') {
                count++;
                dfs(grid, r, c);
            }
        }
    }
    return count;
}

private void dfs(char[][] grid, int r, int c) {
    if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != '1')
        return;
    grid[r][c] = '#';
    dfs(grid, r + 1, c);
    dfs(grid, r - 1, c);
    dfs(grid, r, c + 1);
    dfs(grid, r, c - 1);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (no visited) | ∞ (loops forever) | — |
| Optimised DFS (in-place mark) | O(rows × cols) | O(rows × cols) stack |
| Optimised BFS (in-place mark) | O(rows × cols) | O(min(rows, cols)) queue |

---

## Say it out loud (interview narration)

> *"I'll treat the grid as a graph: each cell is a node, edges connect adjacent land cells, and an island is a connected component. I scan the grid; every time I hit an unvisited land cell I increment my island count and flood-fill from it — DFS or BFS — marking every reachable land cell as visited so I don't count it twice. I'll mark cells in place by overwriting `'1'` with `'#'` instead of keeping a separate visited set, which saves memory. That's O(rows × cols) time since each cell is touched once. If you'd rather I not mutate the grid, I'll use a visited set or restore it afterward."*

## Related / follow-ups
- **Max Area of Island** (LC 695) — same flood fill, track the size of each component
- **Number of Closed Islands** (LC 1254) — flood-fill boundary islands out first
- **Surrounded Regions** (LC 130) — flood from the borders
- **Number of Provinces** (LC 547) — same component-counting idea on an adjacency matrix (or Union-Find)
- **Flood Fill** (LC 733) — the single-region primitive this is built on
