# 🎬 Recording Script — Max Area of Island

**Pattern: Grid DFS / Flood Fill · LeetCode 695 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** recursion basics; the "explore everything reachable" instinct.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a grid of 0s and 1s. The 1s form two blobs — a small cluster top-left, a bigger one bottom-right. A satellite-map vibe, land vs ocean.]**

> Picture a satellite map — 1s are land, 0s are water. Blobs of connected land are islands, and Google asks: *"How big is the largest one?"*
>
> This is the gateway to an entire category — grids, connected components, flood fill — that shows up constantly. And there's one small decision inside it that trips people: how do you count every cell of an island **exactly once**, without spiraling into infinite loops? The answer is a trick so clean it needs no extra memory. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, the 4×5 grid; the two islands outlined — area 3 and area 4.]**

> One line: **an island is a group of 1s connected up/down/left/right — return the number of cells in the biggest island.**
>
> Tiny example — this grid has two islands. The top-left blob has 3 cells. The bottom-right blob has 4. So the answer is **4**. Connected means 4-directionally — diagonals don't count. Keep this grid in view.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — the core mechanism)*

**[VISUAL: scan the grid cell by cell. Hit the first 1; from it, arrows spread to its 4 neighbors, then their neighbors — a spreading stain.]**

> The realization: an island is a **connected component**. So scan the grid, and each time you hit a 1 you haven't seen, that's a *new* island — explore all of it, count the cells, track the biggest.
>
> How do you explore one island? From a land cell, step to its four neighbors that are also land, and repeat — recursively. That's **flood fill**. Each cell contributes 1, plus whatever its neighbors contribute: `1 + explore(up) + explore(down) + explore(left) + explore(right)`.

**[VISUAL: the stain spreads across the bottom-right blob, counting 1, 2, 3, 4.]**

> Land, plus land, plus land, plus land — the bottom-right island returns 4.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: two adjacent land cells whose recursions point back at EACH OTHER — a red infinite-loop cycle. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the danger. Cell A recurses into its neighbor B — which is land, so B recurses back into A — which is land, so A recurses into B... forever. And even without an infinite loop, we'd count the same cell many times.
>
> **LEARNER:** So I need a "visited" set — mark each cell the first time I touch it, and refuse to re-enter. Standard graph traversal.
>
> **TEACHER:** That works — but pause and think if there's something *cheaper* than a whole separate set. **We're already allowed to look at the grid. When I visit a land cell, is there a way to mark it visited using the grid itself?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it)*

**[VISUAL: as the flood fill enters each land cell, the 1 flips to 0 — the island "sinks" behind the traversal.]**

> **TEACHER:** Here's the elegant move: the moment you step onto a land cell, **sink it** — overwrite the 1 to a 0. Now it *is* water. It can never be re-entered, never re-counted, and there's no infinite loop — because the cell you came from is already sunk.
>
> **[VISUAL: analogy — walking across stepping stones, each stone drops into the water the instant you step off it, so you can't step back.]**
>
> Think of stepping stones that sink as you cross. You physically can't backtrack, so no cycle, no revisiting — and you need *no separate visited set*, because the grid remembers for you. The base case becomes beautifully simple: if you're off the grid or standing on water, return 0.
>
> **LEARNER:** But doesn't sinking cells destroy the input?
>
> **TEACHER:** It does — so if the caller needs the grid intact, you'd restore it or keep a visited set instead. But when mutation's allowed, sinking is the cleanest, lightest way, and interviewers love it.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Scan for land → DFS flood fill, sinking each cell to 0 → return 1 + the four neighbors."]**

> The key move: **scan the grid; on each unvisited land cell, flood-fill it with DFS, sinking cells as you go, and return `1 + the four recursive calls`.** Sinking *is* your visited marker. Returning the *area* — a number — rather than just marking is the twist that makes this "max area" instead of "count islands."

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. The dfs helper first.]**

> The recursive flood fill — base case, then sink, then recurse.

```python
def maxAreaOfIsland(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
            return 0                        # off-grid or water → contributes nothing
        grid[r][c] = 0                      # sink: mark visited
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)
```

> **[VISUAL: add the outer scan.]** Now the scan — launch a DFS on every still-standing land cell, keep the max.

```python
    best = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:             # unvisited land → a new island
                best = max(best, dfs(r, c))
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:15`
*(elaboration — why each line exists)*

**[VISUAL: the dfs function; spotlight the base case and the sink line.]**

> Why it's correct and why it's fast.
>
> The base case bundles *four* checks into one: off the top, off the bottom, off the sides, or on water — any of those, return 0. That's what lets us recurse into neighbors blindly without pre-checking bounds; the child call handles its own validity.
>
> `grid[r][c] = 0` — the sink — runs the instant we commit to a cell, *before* recursing. So by the time neighbors try to come back, this cell is already water. That single line replaces the whole visited set and kills every cycle.
>
> **LEARNER:** The outer loop launches a DFS per island — isn't that a lot of repeated work over the whole grid?
>
> **TEACHER:** It feels like it, but no. Every cell gets *sunk* on its first visit, so it's entered at most once across all the DFS calls — the islands partition the grid. Total work is O(m·n), even though we start many separate floods. The outer loop only ever *starts* a DFS on land that's still standing.

---

## 9. DRY-RUN THE CODE — `7:15`
*(worked example — prove it)*

**[VISUAL: the grid, bottom-right island; cells flip to 0 as counted; a running area counter.]**

> Trace the bottom-right island. The outer scan reaches cell (2,3), a 1.
>
> `dfs(2,3)`: sink it (area 1). Recurse to (2,4) — land, sink (2). Recurse to (3,3) — land, sink (3). Recurse to (3,4) — land, sink (4). Every remaining neighbor is water or already sunk → all return 0. So `dfs(2,3)` returns **4**.
>
> The top-left island returns **3** the same way. `best = max(3, 4) = 4`. And notice — because each island was sunk as we counted it, the outer scan never re-triggers on a cell we've already claimed. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:10`
*(transfer to interview)*

**[VISUAL: rows — Visited set: O(m·n) time, O(m·n) space. Sinking: O(m·n) time, O(m·n) recursion worst case.]**

> Out loud: *"Time is O(m·n) — every cell is touched a constant number of times. Sinking cells means no separate visited set. Space is the recursion stack, O(m·n) in the worst case — a grid that's all land forms one long snaking path of recursive calls."*
>
> That honesty about the recursion depth is exactly what a good interviewer wants to hear next.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:50`
*(depth + honesty)*

**[VISUAL: an all-land grid; the recursion stack tower growing dangerously tall. Then an explicit stack version, heap-based.]**

> Time is already optimal — you must inspect every cell. The space to attack is the **recursion stack**: on a giant all-land grid, recursion can go O(m·n) deep and blow the stack limit. Swap it for an **explicit stack** — iterative DFS.

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

> Honest accounting: worst-case space is *still* O(m·n) — but now it's heap memory you control, not the call stack, so no recursion-limit crash. And sinking cells means **no visited set** either way — that's the real space win over the brute-force approach.
>
> Say it out loud: *"I sink cells instead of keeping a visited set. Recursion is cleanest but risks a deep stack on an all-land grid, so if that's a concern I'd switch to an explicit stack — same asymptotic space, no recursion blowup."*

---

## 12. YOUR TURN (active recall) — `10:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Islands (LC 200)".]**

> Before the next video, try **Number of Islands** — same flood fill, but instead of measuring the biggest, you *count* how many islands there are. It's this exact code with one change: increment a counter each time the outer scan launches a new DFS, instead of tracking max area. If you own this, that one's a two-minute win.
>
> Ten minutes, no peeking.

---

## 13. LOCK IT IN — `10:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **An island is a connected component** — scan for land, flood-fill each region.
> 2. **Sink visited cells to 0** — it's your visited marker and kills all cycles, no extra set.
> 3. **Return `1 + four recursive calls`** to accumulate area; recursion depth can be O(m·n).
>
> The memory peg — *"stepping stones that sink behind you: touch a cell, drop it to water, count it, spread to the four neighbors."*

---

## 14. CLIFFHANGER — `11:05`
*(open loop to next lesson)*

**[VISUAL: a blurred histogram of bars with water pooling between them — Trapping Rain Water.]**

> Flood fill spreads *outward* to explore. The next problem pushes *inward* from both ends: bars of a histogram, and you compute how much rain pools in the valleys. Different shape, but the same discipline of processing each cell exactly once — this time with two pointers marching toward each other. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
