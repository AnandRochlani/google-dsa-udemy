# 🎬 Recording Script — Number of Islands
**Pattern: Graphs (flood fill) · LeetCode 200 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none required — but this is the lesson that turns "a grid" into "a graph." Everything in this section builds on it.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an Google phone-screen interview mock. A grid of 1s and 0s appears. Interviewer prompt in a chat bubble: "How many islands?"]**

> Google loves this one. They drop a grid of 1s and 0s in front of you and say: *"the 1s are land, the 0s are water. How many separate islands are there?"*
>
> And your brain freezes, because this doesn't look like any array problem you drilled. There's no sorting, no two pointers, no sliding window. It's a *picture*.
>
> Here's the secret that unlocks this entire section of the course: **this grid is secretly a graph.** Once you see that, this problem — and five more after it — all collapse into the same little engine. Let me show you.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a 4×5 grid:]**

```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

> The whole problem in one line: **count the groups of connected land.** Land connects up, down, left, right — *not* diagonally.
>
> Look at this tiny grid. Squint at it like a map. That 2-by-2 block of 1s in the top-left — that's one island. The lonely 1 in the middle — that's a second. And those two 1s touching in the bottom-right — that's a third.
>
> The answer is **3.** Hold that number. We're going to make the code arrive at exactly 3.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — feel the mechanism)*

**[VISUAL: same grid. A finger-cursor lands on the top-left 1. It highlights, then "spreads" to touching 1s one at a time.]**

> Let's think like a human first. You spot land at the top-left corner. What do you do? You trace it. You walk to every 1 you can reach without stepping on water.
>
> From `(0,0)`, I step right to `(0,1)` — land. Down to `(1,0)` — land. Over to `(1,1)` — land. Now I look around from each of those… everything else touching is water. That whole blob is *one* island. Paint it. Done.
>
> **[VISUAL: the top-left 2×2 block turns a flat gray — "counted."]**
>
> Then I keep scanning the grid. Next unpainted land I find is that middle 1. I try to spread from it — nothing but water around it. That's island number two.
>
> That "find land, then spread to everything connected" move — that's the whole algorithm. It has a name: **flood fill.** Like the paint-bucket tool dumping color until it hits a wall.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(generation effect — first pause)*

**[VISUAL: two adjacent land cells A and B. An arrow from A→B, then B→A, then A→B… looping. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Now here's the trap, and it's a nasty one. When I "spread" from cell A to its neighbor B — B is *also* land, so B spreads back to A. And A spreads to B. Forever. My paint bucket never stops.
>
> **LEARNER:** Oh — so a plain recursion into all four neighbors just bounces back and forth between two cells and blows the stack.
>
> **TEACHER:** Exactly right. Infinite loop, instant crash. So pause here and predict: **what's the one thing I need to add so the spread visits each cell once and then stops?** You already know this instinct from every graph traversal. Take three seconds.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — the grid IS a graph)*

**[VISUAL: the grid morphs — each cell sprouts into a circle (a node), and short lines (edges) connect each land cell to its 4 land neighbors. Water cells fade out.]**

> **TEACHER:** Here's the reframe that runs this whole course section. **A 2D grid IS a graph.** Each cell is a node. Each cell has an edge to its four neighbors — up, down, left, right. That's it.
>
> And once it's a graph, "an island" is just a **connected component** — a clump of nodes you can walk between. "Count the islands" becomes "count the connected components." That's a classic graph question with a classic answer.
>
> **LEARNER:** So the fix for the infinite loop is the same as any graph traversal — a *visited* marker.
>
> **TEACHER:** Yes. Mark every cell the moment you touch it. Here's the elegant version for a grid: don't even keep a separate visited set — just **overwrite the land with water.** Sink it. Once a `1` becomes a `'#'`, it's not land anymore, so the spread can't come back to it. The grid marks *itself*.
>
> **[VISUAL: replay the top-left flood — but now each visited 1 flips to `#` as it's touched, and the back-arrow to A is blocked by a little wall.]**
>
> Spread from A, sink A to `#`. B sees A is no longer land — dead end. No bounce. Each cell touched once.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable line)*

**[VISUAL: a single boxed line: "Scan for land → new island, count++ → flood-fill and sink it."]**

> Burn this line in: **scan the grid; every unsunk land cell you hit is a new island — count it, then flood-fill from it and sink the whole thing.**
>
> The outer scan finds *new* islands. The flood fill makes sure you only count each island once. That division of labor is the entire trick.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the setup and the outer scan.

```python
def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Now the flood fill itself — a little DFS that sinks land and dives into neighbors.

```python
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != '1':          # water, wall, or off-grid → stop
            return
        grid[r][c] = '#'               # sink it = mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
```

> **[VISUAL: add chunk 3, highlight the double loop.]** And the driver: scan every cell; each fresh land cell is a new island.

```python
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)              # flood the entire island
    return count
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk the *why*.
>
> The two base cases in `dfs` — off-grid, or not `'1'` — are your guardrails. Off-grid stops you walking off the map. "Not `'1'`" stops you on water *and* on already-sunk cells, because we turned those into `'#'`.
>
> `grid[r][c] = '#'` — this single line is doing two jobs: it records the answer *and* prevents the bounce-back. That's the visited marker, living inside the grid.
>
> The four recursive calls — that's "spread to all four neighbors." Up, down, left, right. No diagonals, because the problem said connectivity is 4-directional.
>
> And in the driver, `count += 1` fires *only* when we hit a `'1'` the scan hasn't sunk yet. That's the guarantee: one increment per island, because the flood immediately erases the rest of that island before the scan reaches it.
>
> **LEARNER:** Wait — the input is `'1'` and `'0'` as *strings*, not integers, right? So the comparison has to be `== '1'` with quotes?
>
> **TEACHER:** Sharp catch, and it's the number-one silent bug on this problem. LeetCode hands you `char` values — `'1'`, `'0'`, in quotes. Compare against the integer `1` and every check is false and you return zero islands. Quotes matter here.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the grid, with a step counter for `count` and cells flipping to `#` live.]**

> Let's run it on our grid and watch `count` climb.

```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

| scan hits | value | action |
|---|---|---|
| (0,0) | '1' | **count = 1**, flood sinks (0,0)(0,1)(1,0)(1,1) → all `#` |
| (0,1)…(2,1) | `#` or `0` | skip |
| (2,2) | '1' | **count = 2**, no land neighbors → only (2,2) sinks |
| (3,3) | '1' | **count = 3**, flood sinks (3,3)(3,4) |
| rest | `#`/`0` | skip |

> Final `count` = **3.** Exactly the three islands we counted by eye at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Time: O(rows × cols). Space: O(rows × cols) worst-case stack.]**

> Say it the way you'd say it to the interviewer: *"Every cell is visited at most once — the scan looks at it, and the flood fill touches it once and sinks it. So it's O(rows times cols) time, linear in the grid."*
>
> *"Space is the recursion stack. Worst case — a grid that's all land, one giant snaking island — the DFS stack can hold every cell, so O(rows times cols)."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: side by side — "separate visited set: +O(rows×cols)" crossed out; "sink in place: +O(1)".]**

> On the visited front, we're already lean. We could have kept a separate `visited` set — but that's a whole extra grid of memory. Sinking cells to `'#'` in place means the visited marker costs *nothing* extra.
>
> The one honest tradeoff: we're **mutating the interviewer's input.** Say that out loud. *"I'm sinking land in place to save the visited set — if you'd rather I not modify your grid, I'll restore the `'#'`s to `'1'` at the end, or use a visited set at O(rows times cols) extra space."* Naming that you noticed is a strong-hire signal.
>
> One more: if the grid could be enormous and deeply connected, DFS recursion might overflow — swap to a BFS queue. Same time, and the queue frontier is often smaller than the full DFS stack.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Max Area of Island (LC 695)". A blank editor.]**

> Before the next video, try **Max Area of Island.** Same flood fill, one twist: instead of just counting islands, have each fill *return the size* of the region, and track the biggest.
>
> Don't peek. If you can bolt "return a count" onto today's DFS, you've truly got the pattern.

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **A grid is a graph** — each cell a node, edges to 4 neighbors. This reframe powers the whole section.
> 2. **Island = connected component.** Count components by flood-filling each one once.
> 3. **Sink as you visit** — overwriting the cell is a free visited marker and kills the infinite bounce.
>
> The memory peg: when you see a grid and the words *"connected region," "group," or "island,"* your hand should already be reaching for the **paint bucket** — flood fill and sink it.

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a grid with a single glowing cell and a "paint bucket" icon — title blurred: "Flood Fill (LC 733)".]**

> Today we ran the flood fill *many* times — once per island. But what if you only need to fill *one* region, from one starting pixel — the actual paint-bucket tool? That's the pure primitive underneath everything we just did, and it hides one edge case that loops forever if you miss it. That's next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
