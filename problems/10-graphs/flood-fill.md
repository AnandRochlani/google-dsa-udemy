# Flood Fill

> **LeetCode:** 733. Flood Fill · **Difficulty:** 🟢 Easy · **Pattern:** Graph BFS/DFS (flood fill) · **Google frequency:** medium

---

## Problem

You're given an image as a 2D grid of integer colors, a starting pixel `(sr, sc)`, and a new `color`. Starting from that pixel, recolor it and every pixel **4-directionally connected** to it that shares the **original** color. Return the modified image. (This is the paint-bucket tool.)

**Example:**

```
image =
1 1 1
1 1 0
1 0 1

sr = 1, sc = 1, color = 2
```

The pixel at `(1,1)` has color `1`. Every `1` connected to it (up/down/left/right chains) becomes `2`:

```
2 2 2
2 2 0
2 0 1
```

→ note the bottom-right `1` at `(2,2)` is *not* connected to the starting region (it's diagonally separated), so it stays `1`.

**Constraints that matter:** grid up to `50 × 50`. Tiny — the real trap is **not size but correctness**: the infamous edge case where `color == original color`. If you don't guard it, you flood a region that already matches the new color and spin forever.

---

## 🧠 Intuition — how you'd actually arrive at this

> This is the *primitive* that "Number of Islands" and friends are built on — a single flood fill of one connected region.

- **First instinct:** "Recolor the start pixel, then do the same to its neighbors that have the same original color, and their neighbors, and so on." That recursive spread *is* flood fill.
- **The reframe — grid as graph:** each pixel is a node; edges connect adjacent pixels **that share the starting color**. The set of pixels to recolor is exactly the **connected component** containing `(sr, sc)`. Recolor everything reachable in that component.
- **Where it can hurt:** if you don't mark visited pixels, you bounce between two same-colored neighbors forever. The elegant fix here: **recoloring the pixel IS marking it visited** — once it's the new color, it no longer matches the original, so you won't revisit it.
- **The one edge case that bites everyone:** if `color` already equals the original color, then recoloring changes nothing, so "is it the new color yet?" never becomes true → **infinite loop**. Guard it: if `newColor == oldColor`, return immediately.
- **Pattern trigger:** **"recolor / fill a connected region starting from one cell"** → **flood fill (DFS or BFS)** on the grid-as-graph. Same engine as island counting, minus the outer scan.

---

## ① Brute Force

The "natural but broken" version: recurse into neighbors that match, but forget the equal-color guard.

```python
def floodFill_broken(image, sr, sc, color):
    rows, cols = len(image), len(image[0])
    start = image[sr][sc]

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if image[r][c] != start:
            return
        image[r][c] = color          # BUG: if color == start, this changes nothing
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)                      # BUG: no guard for color == start
    return image
```

**Why it's the natural first attempt:** the flood-fill recursion is genuinely correct in shape — it's the classic paint-bucket.

**Why it's not enough:** when `color == start`, writing `image[r][c] = color` leaves the pixel matching `start`, so the neighbors keep re-qualifying and re-recursing → **infinite recursion / stack overflow**. On the example it happens to work, but a test like `color = 1` on a region already colored `1` crashes it.

**Complexity:** correct case is `O(rows × cols)`; the `color == start` case never terminates.

---

## ② Optimised Solution

Same flood fill, with the equal-color guard. DFS version:

```python
def floodFill(image, sr, sc, color):
    start = image[sr][sc]
    if start == color:              # the guard that prevents the infinite loop
        return image
    rows, cols = len(image), len(image[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if image[r][c] != start:
            return
        image[r][c] = color          # recolor = mark visited (no longer == start)
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

BFS version (no recursion depth worry):

```python
from collections import deque

def floodFill_bfs(image, sr, sc, color):
    start = image[sr][sc]
    if start == color:
        return image
    rows, cols = len(image), len(image[0])
    q = deque([(sr, sc)])
    image[sr][sc] = color
    while q:
        r, c = q.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == start:
                image[nr][nc] = color
                q.append((nr, nc))
    return image
```

**Walk the example** (`sr=1, sc=1, color=2`, start color `1`):

- `start = 1`, `color = 2` — guard passes (they differ).
- Fill `(1,1)`→2. Visit neighbors: `(0,1)=1`→2, `(2,1)=0` skip, `(1,0)=1`→2, `(1,2)=0` skip.
- From `(0,1)`: `(0,0)=1`→2, `(0,2)=1`→2.
- From `(1,0)`: `(0,0)` already 2, `(2,0)=1`→2.
- From `(2,0)`: `(2,1)=0` skip. Frontier drains.
- Result:
  ```
  2 2 2
  2 2 0
  2 0 1
  ```
  `(2,2)` never reached — not connected. ✅

**Why it's correct:** we recolor exactly the connected component of `start`-colored pixels reachable from `(sr, sc)`. Recoloring simultaneously marks visited (the pixel stops matching `start`), so each pixel is processed once and we can't loop. The guard handles the degenerate no-op case.

**Complexity:** Time `O(rows × cols)` — each pixel touched at most once. Space `O(rows × cols)` worst case for the stack/queue.

---

## ③ Space Optimization

**Already optimal.** We mutate the image **in place** and use the recolor itself as the visited marker — no separate `visited` structure. The only extra memory is the DFS recursion stack or BFS queue, which is unavoidable for traversal and bounded by `O(rows × cols)` (the whole image being one region).

> If the interviewer says "don't mutate the input," you'd need an `O(rows × cols)` visited set or a copy — but for this problem, in-place *is* the expected answer, and it's as tight as it gets.

---

## Java (for Java interviewers)

```java
public int[][] floodFill(int[][] image, int sr, int sc, int color) {
    int start = image[sr][sc];
    if (start == color) return image;      // guard against infinite loop
    dfs(image, sr, sc, start, color);
    return image;
}

private void dfs(int[][] image, int r, int c, int start, int color) {
    if (r < 0 || r >= image.length || c < 0 || c >= image[0].length || image[r][c] != start)
        return;
    image[r][c] = color;
    dfs(image, r + 1, c, start, color);
    dfs(image, r - 1, c, start, color);
    dfs(image, r, c + 1, start, color);
    dfs(image, r, c - 1, start, color);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (no guard) | O(rows × cols) or ∞ if color == start | O(rows × cols) |
| Optimised DFS | O(rows × cols) | O(rows × cols) stack |
| Optimised BFS | O(rows × cols) | O(rows × cols) queue |

---

## Say it out loud (interview narration)

> *"This is a single flood fill: the pixels I recolor are exactly the connected component of the start color reachable from the start pixel, treating the grid as a graph with edges between same-colored neighbors. I DFS (or BFS) from the start, recoloring as I go — and recoloring doubles as marking visited, since the pixel no longer matches the original color. The one gotcha is if the new color equals the original: then recoloring never changes anything and I'd loop forever, so I guard that up front and return early. It's O(rows × cols) time, in place, and the only extra space is the traversal frontier."*

## Related / follow-ups
- **Number of Islands** (LC 200) — flood fill run repeatedly to count components
- **Max Area of Island** (LC 695) — flood fill returning the region size
- **Surrounded Regions** (LC 130) — flood from the borders
- **Pacific Atlantic Water Flow** (LC 417) — flood fill from two edge sets
