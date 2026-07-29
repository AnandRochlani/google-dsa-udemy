# Rotting Oranges

> **LeetCode:** 994. Rotting Oranges · **Difficulty:** 🟡 Medium · **Pattern:** Graph BFS/DFS (multi-source BFS) · **Google frequency:** ⭐ high

---

## Problem

You're given a grid where each cell is:
- `0` — empty,
- `1` — a **fresh** orange,
- `2` — a **rotten** orange.

Every minute, any fresh orange **4-directionally adjacent** to a rotten one becomes rotten. Return the **minimum number of minutes** until no fresh orange remains. If some fresh orange can never rot, return `-1`.

**Example:**

```
grid =
2 1 1
1 1 0
0 1 1
```

Minute 0: rot at `(0,0)`.
Minute 1: `(0,1)` and `(1,0)` rot.
Minute 2: `(0,2)` and `(1,1)` rot.
Minute 3: `(2,1)` rots.
Minute 4: `(2,2)` rots.

→ `4`.

**Constraints that matter:** grid up to `10 × 10` here, but the pattern scales to `O(rows × cols)`. The key subtlety: rot spreads from **all** rotten oranges **simultaneously** each minute — that "simultaneous, from many sources" phrasing is the entire hint.

---

## 🧠 Intuition — how you'd actually arrive at this

> Two signals stack here: "grid → graph" and "minimum minutes to spread → BFS." Together they scream **multi-source BFS**.

- **First instinct:** simulate minute by minute. Each minute, scan the whole grid, find every rotten orange, rot its fresh neighbors, repeat until nothing changes. That works — but you re-scan the entire grid every single minute. Wasteful.
- **The reframe — grid as graph:** each cell is a node; edges connect adjacent cells. Rot flows along edges. "Minimum minutes for rot to reach every fresh orange" is a **shortest-path in an unweighted graph** question → that's **BFS**, whose defining property is that it discovers nodes in order of distance from the source.
- **The twist — many sources at once:** there isn't one starting rotten orange; there can be several, and they all spread *at the same time*. In BFS terms, that's **multi-source BFS**: instead of seeding the queue with one node, you **seed it with every rotten orange at distance 0**. BFS naturally processes them level by level, and each "level" is exactly one minute.
- **How minutes fall out:** process the queue **one level at a time**. Each fully drained level = one minute elapsed. The last level that actually rots something gives the answer. (Equivalently, store the minute alongside each cell and take the max.)
- **The `-1` case:** after BFS finishes, if any cell is still `1`, it was unreachable — walled off by water or with no rotten neighbor ever. Return `-1`.
- **Pattern trigger:** **"minimum time / steps for something to spread from multiple starting points"** → **multi-source BFS**: push all sources into the queue up front, then level-order.

---

## ① Brute Force

Simulate the clock literally — rescan the whole grid every minute.

```python
def orangesRotting_brute(grid):
    rows, cols = len(grid), len(grid[0])
    minutes = 0

    def count_fresh():
        return sum(row.count(1) for row in grid)

    while count_fresh() > 0:
        to_rot = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            to_rot.append((nr, nc))
        if not to_rot:
            return -1          # nothing rotted this minute but fresh remain → stuck
        for r, c in to_rot:
            grid[r][c] = 2
        minutes += 1
    return minutes
```

**Why it's the natural first attempt:** it mirrors the problem's wording exactly — "each minute, rotten oranges infect neighbors." Very readable.

**Why it's not enough:** every minute it rescans the **entire grid** to relocate the rotten oranges it already knew about. With `M` minutes and a grid of `R×C`, that's `O(M × R × C)`. It's re-discovering the whole frontier from scratch each round instead of remembering it.

**Complexity:** Time `O(minutes × rows × cols)`, Space `O(rows × cols)`.

---

## ② Optimised Solution

Multi-source BFS. Seed the queue with **every** rotten orange, then expand level by level, counting fresh oranges so we can detect the stuck case.

```python
from collections import deque

def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0

    # seed: every rotten orange starts at minute 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0                      # nothing to rot

    minutes = 0
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while q and fresh > 0:
        minutes += 1                  # advance one minute per BFS level
        for _ in range(len(q)):       # drain exactly this level
            x, y = q.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                    grid[nx][ny] = 2  # rot it now (also marks visited)
                    fresh -= 1
                    q.append((nx, ny))

    return minutes if fresh == 0 else -1
```

**Walk the example:**

```
2 1 1
1 1 0
0 1 1
```

- **Seed:** queue = `[(0,0)]`, fresh = 6.
- **Minute 1:** drain `(0,0)`. Rot `(0,1)` and `(1,0)`. fresh = 4. queue = `[(0,1),(1,0)]`.
- **Minute 2:** drain both. `(0,1)`→rot `(0,2)`; `(1,0)`→rot `(1,1)`. fresh = 2. queue = `[(0,2),(1,1)]`.
- **Minute 3:** drain both. `(1,1)`→rot `(2,1)`. `(0,2)` has no fresh neighbor. fresh = 1. queue = `[(2,1)]`.
- **Minute 4:** drain `(2,1)`→rot `(2,2)`. fresh = 0. queue = `[(2,2)]`.
- Loop stops (fresh == 0). **Return 4.** ✅

**Why it's correct:** BFS processes cells in nondecreasing distance from the *nearest* rotten source. Because all sources sit in the queue at level 0, each cell rots at exactly the minute equal to its shortest distance to any initial rotten orange — which is precisely how the simultaneous spread works. The `fresh` counter gives an O(1) stuck-check: if it never reaches 0, some fresh orange was unreachable → `-1`.

**Complexity:** Time `O(rows × cols)` — each cell is enqueued at most once. Space `O(rows × cols)` for the queue.

---

## ③ Space Optimization

This is essentially **already optimal**. We mark cells rotten **in place** (`grid[nx][ny] = 2`) instead of keeping a separate visited set, so the only extra memory is the BFS queue — unavoidable for level-order traversal, and bounded by `O(rows × cols)`.

You *could* shave the queue by encoding coordinates as a single integer (`r * cols + c`) to reduce per-entry overhead, but that's a constant-factor tweak, not an asymptotic win.

> Say it plainly: *"The grid doubles as my visited marker, so the only extra space is the frontier queue, which BFS fundamentally needs. That's already O(rows × cols) and can't be beaten for this traversal."* Naming why it's optimal is as strong as finding a trick.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (rescan each minute) | O(minutes × rows × cols) | O(rows × cols) |
| Optimised (multi-source BFS) | O(rows × cols) | O(rows × cols) |

---

## Say it out loud (interview narration)

> *"Rot spreading from many oranges at once, asking for minimum minutes — that's a shortest-path-in-an-unweighted-graph question, so BFS, and because rot starts from every rotten orange simultaneously it's multi-source BFS. I seed the queue with all rotten oranges at minute 0, then expand level by level; each drained level is one minute. I rot cells in place so the grid itself is my visited set, and I keep a fresh counter — if it doesn't hit zero by the end, some orange was unreachable and I return -1. It's O(rows × cols) time and space."*

## Related / follow-ups
- **01 Matrix** (LC 542) — multi-source BFS from all the zeros
- **Walls and Gates** (LC 286) — multi-source BFS from all gates
- **Shortest Path in Binary Matrix** (LC 1091) — single-source BFS, 8 directions
- **As Far from Land as Possible** (LC 1162) — multi-source BFS, take the max distance
- **Number of Islands** (LC 200) — same grid-as-graph framing, flood fill instead of shortest path
