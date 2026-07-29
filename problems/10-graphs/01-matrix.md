# 01 Matrix

> **LeetCode:** 542. 01 Matrix · **Difficulty:** 🟡 Medium · **Pattern:** Graph BFS/DFS (multi-source BFS from all zeros) · **Google frequency:** medium

---

## Problem

Given an `m × n` binary matrix, return a matrix of the same size where each cell holds the **distance to the nearest `0`**, measured in 4-directional steps.

**Example:**

```
mat =
0 0 0
0 1 0
1 1 1

→
0 0 0
0 1 0
1 2 1
```

Every `0` maps to `0`. The `1` at `(1,1)` is one step from several `0`s → `1`. The `1` at `(2,0)` is one step from `(1,0)=0` → `1`. The `1` at `(2,1)` is two steps from the nearest `0` → `2`.

**Constraints that matter:** up to `10⁴ × 10⁴`... realistically `m*n ≤ 10⁴`. We want `O(m × n)`. Running a separate BFS from every `1` would be `O((m·n)²)` — far too slow. The winning move is to flip the question around: BFS **outward from all the zeros at once.**

---

## 🧠 Intuition — how you'd actually arrive at this

> The trap is doing BFS from each `1`. The unlock is doing **one** BFS from *all* the `0`s simultaneously — multi-source BFS.

- **First instinct:** "For each `1`, BFS until I hit the nearest `0`, record the distance." Correct, but you'd launch a fresh BFS per `1` cell — up to `m·n` BFS runs, each `O(m·n)` → `O((m·n)²)`. Way too slow.
- **Where it hurts — repeated work:** every one of those independent searches re-explores overlapping territory. Adjacent `1`s recompute almost the same neighborhood. Nothing is shared.
- **The leap — invert the direction:** instead of asking each `1` "where's my nearest `0`?", ask the `0`s to **broadcast distance outward**. Seed a BFS queue with **every `0` at distance 0**. BFS expands in rings: at step 1 you reach all cells adjacent to some `0` (distance 1), at step 2 the next ring (distance 2), and so on. The first time BFS reaches a cell, that's guaranteed to be its shortest distance to *any* `0`. One traversal fills the whole matrix.
- **Why multi-source works:** treating all sources as distance-0 and expanding level by level means every cell is discovered by the *closest* source first — exactly "distance to the nearest `0`."
- **Pattern trigger:** **"distance from every cell to the nearest cell of type X"** → **multi-source BFS: seed the queue with all X cells.** Same shape as Rotting Oranges and Walls and Gates.

---

## ① Brute Force

Independent BFS from each `1` to its nearest `0`.

```python
from collections import deque

def updateMatrix_brute(mat):
    rows, cols = len(mat), len(mat[0])
    res = [[0] * cols for _ in range(rows)]

    def bfs_from(sr, sc):
        seen = {(sr, sc)}
        q = deque([(sr, sc, 0)])
        while q:
            r, c, d = q.popleft()
            if mat[r][c] == 0:
                return d                      # nearest zero found
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, d + 1))
        return -1

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 1:
                res[r][c] = bfs_from(r, c)
    return res
```

**Why it's the natural first attempt:** it's the literal reading — "for each `1`, find the distance to the nearest `0`." Straightforward to reason about.

**Why it's not enough:** up to `m·n` cells each run a BFS that can touch `O(m·n)` cells → **`O((m·n)²)`**. On a `100×100` matrix that's `~10⁸` and it only gets worse. It re-derives overlapping distances again and again.

**Complexity:** Time `O((m × n)²)`, Space `O(m × n)` per BFS.

---

## ② Optimised Solution

Multi-source BFS outward from every `0` at once.

```python
from collections import deque

def updateMatrix(mat):
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]   # -1 = not yet visited
    q = deque()

    # seed: every 0 is distance 0 and a BFS source
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))

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

**Walk the example:**

```
mat =            dist init (0s seeded):
0 0 0            0 0 0
0 1 0            0 -1 0
1 1 1            -1 -1 -1
```

Queue starts with all five `0` positions: `(0,0),(0,1),(0,2),(1,0),(1,2)`.

- Drain `(0,0)`: neighbor `(1,0)` already 0. Nothing new.
- Drain `(0,1)`: neighbor `(1,1)=-1` → set `dist[1][1]=1`, enqueue.
- Drain `(0,2)`, `(1,0)`: `(1,0)`→`(2,0)=-1` → `dist[2][0]=1`, enqueue.
- Drain `(1,2)`: `(2,2)=-1` → `dist[2][2]=1`, enqueue.
- Drain `(1,1)` (dist 1): `(2,1)=-1` → `dist[2][1]=2`, enqueue.
- Drain `(2,0)`,`(2,2)` (dist 1): their neighbor `(2,1)` already set. `(2,1)` (dist 2): no unvisited neighbors.
- Final:
  ```
  0 0 0
  0 1 0
  1 2 1
  ```
  ✅

**Why it's correct:** because every `0` enters the queue at distance 0 and BFS expands in nondecreasing distance order, the **first** time any cell is dequeued-into (assigned a `dist`), it's via the shortest path from the closest source. We never overwrite — `dist == -1` guards each cell as write-once — so each cell gets its true minimum distance.

**Complexity:** Time `O(m × n)` — every cell enqueued exactly once. Space `O(m × n)` for the queue and the distance matrix (which is also the required output).

---

## ③ Space Optimization

The `dist` matrix **is the output**, so it isn't "extra" space — it's the answer. The genuine extra is the BFS queue, `O(m × n)` worst case, which level-order traversal fundamentally needs. So BFS is already tight.

If you truly want to avoid the queue, there's an alternative **two-pass dynamic programming** solution that computes each cell's distance from its up/left neighbors in one pass and down/right neighbors in another, using only the `dist` grid itself:

```python
def updateMatrix_dp(mat):
    rows, cols = len(mat), len(mat[0])
    INF = float('inf')
    dist = [[0 if v == 0 else INF for v in row] for row in mat]

    # pass 1: from top-left — consider up and left neighbors
    for r in range(rows):
        for c in range(cols):
            if dist[r][c] != 0:
                if r > 0:
                    dist[r][c] = min(dist[r][c], dist[r-1][c] + 1)
                if c > 0:
                    dist[r][c] = min(dist[r][c], dist[r][c-1] + 1)

    # pass 2: from bottom-right — consider down and right neighbors
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if dist[r][c] != 0:
                if r < rows - 1:
                    dist[r][c] = min(dist[r][c], dist[r+1][c] + 1)
                if c < cols - 1:
                    dist[r][c] = min(dist[r][c], dist[r][c+1] + 1)
    return dist
```

**Complexity:** Time `O(m × n)`, Space `O(1)` extra (writes into the `dist`/output grid, no queue). This is the strictly-lowest-space answer.

> Say it out loud: *"BFS is O(m·n) time but keeps a queue. The two-pass DP hits the same distances with no queue at all — up/left then down/right — so it's O(1) extra space beyond the output."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (BFS per 1) | O((m × n)²) | O(m × n) |
| Optimised (multi-source BFS) | O(m × n) | O(m × n) queue |
| Two-pass DP | O(m × n) | O(1) extra |

---

## Say it out loud (interview narration)

> *"Naively I'd BFS from each 1 to its nearest 0 — but that's a BFS per cell, O((m·n)²). The trick is to invert it: instead of each 1 searching for a 0, I let all the 0s broadcast outward at once. I seed a BFS queue with every 0 at distance 0 and expand in rings; the first time BFS reaches a cell is its shortest distance to the nearest 0. That's one traversal, O(m·n). The distance grid is also my output and my visited marker. If you want to drop the queue entirely, there's a two-pass DP — up/left then down/right — that's O(m·n) time and O(1) extra space."*

## Related / follow-ups
- **Rotting Oranges** (LC 994) — multi-source BFS measuring spread time
- **Walls and Gates** (LC 286) — multi-source BFS from all gates, nearly identical
- **As Far from Land as Possible** (LC 1162) — multi-source BFS, take the maximum distance
- **Shortest Path in Binary Matrix** (LC 1091) — single-source BFS, 8 directions
