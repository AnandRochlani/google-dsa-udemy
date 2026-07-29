# Battleships in a Board

> **LeetCode:** 419. Battleships in a Board · **Difficulty:** 🟡 Medium · **Pattern:** Grid counting (O(1)-space trick) · **Google frequency:** ⭐ high

---

## Problem

You're given an `m × n` grid of cells that are either `'X'` (part of a battleship) or `'.'` (empty water). Every battleship is a straight line — either a `1 × k` horizontal run or a `k × 1` vertical run of `'X'` cells. Crucially, **no two battleships touch**: there's always at least one `'.'` separating them (they never sit side-by-side horizontally *or* vertically). Count how many battleships are on the board.

**Example:** `board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]` → `2` *(one single-cell ship top-left, one vertical 3-cell ship down the right column).*

**Constraints that matter:** the "no two ships adjacent" rule is not flavor text — it's the whole reason the fast trick works. The follow-up is the real question Google asks: **can you do it in one pass, O(1) extra memory, and without modifying the board?** That last clause quietly rules out the tempting flood-fill (which mutates cells or carries a `visited` set).

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "It's a grid, I'm counting connected blobs of `'X'` — that's Number of Islands. Flood-fill each component, add one per component." Totally correct, and worth saying out loud. But it needs a `visited` set (or it mutates the board), which trips the follow-up.
- **Where it hurts:** flood-fill is *overkill here*. Islands can be any blobby shape, so you genuinely have to explore. But battleships are **straight lines that never touch**. That's a huge extra guarantee we're not using. We're bringing a graph-traversal cannon to a counting problem.
- **The leap:** if I want to count each ship exactly once, I should count it at **one canonical cell** — a spot that's guaranteed to appear once per ship and never twice. For a straight, isolated ship, the natural choice is its **top-left end**: the cell with no ship-cell directly *above* it and no ship-cell directly *to its left*. Every ship — horizontal or vertical, length 1 or 100 — has exactly one such cell. So I just scan the grid and count those.
- **Pattern trigger:** **"count connected pieces, but the pieces have a rigid shape + a separation guarantee"** → don't flood-fill, **count each piece at its canonical corner using only local neighbors.** The transferable move: when structure lets you *identify one unique cell per object*, you replace traversal with a local O(1) test.

---

## ① Brute Force

Treat it exactly like Number of Islands: DFS/flood-fill every unvisited `'X'`, mark the whole component, and add one to the count per component.

```python
def count_battleships_bruteforce(board):
    if not board or not board[0]:
        return 0
    rows, cols = len(board), len(board[0])
    visited = [[False] * cols for _ in range(rows)]   # extra O(m*n) memory

    def dfs(r, c):
        # walk the whole connected 'X' blob, marking it seen
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or board[r][c] != 'X' or visited[r][c]):
            return
        visited[r][c] = True
        dfs(r + 1, c); dfs(r - 1, c)
        dfs(r, c + 1); dfs(r, c - 1)

    ships = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'X' and not visited[r][c]:
                ships += 1          # a brand-new component = one more ship
                dfs(r, c)
    return ships
```

**Why it's the natural first attempt:** it's the Number-of-Islands reflex, and it's genuinely correct. Every interviewer accepts it as a starting point.

**Why it's not enough:** it carries a `visited` grid — `O(m*n)` extra space — or, if you skip that, it *mutates* the board (flipping `'X'` to `'.'`). Both violate the follow-up: **O(1) space, no modification, single pass.** It also does real traversal work we don't need, because the ship shapes are already constrained.

**Complexity:** Time `O(m*n)`, Space `O(m*n)` (the `visited` grid plus recursion stack).

---

## ② Optimised Solution

Count a ship only at its **top-left end**. A cell is the top-left end of a ship when it's an `'X'` **and** the cell directly above it is *not* `'X'` **and** the cell directly to its left is *not* `'X'`. Scan once, increment on those cells only.

```python
def count_battleships(board):
    if not board or not board[0]:
        return 0
    rows, cols = len(board), len(board[0])
    ships = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != 'X':
                continue
            # is there a ship-cell directly above? (guard the top edge)
            if r > 0 and board[r - 1][c] == 'X':
                continue
            # is there a ship-cell directly to the left? (guard the left edge)
            if c > 0 and board[r][c - 1] == 'X':
                continue
            # no 'X' above, no 'X' left → this is the top-left end of a ship
            ships += 1
    return ships
```

**Walk the example** `board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]`:

| Cell `(r,c)` | Value | `'X'` above? | `'X'` left? | Counted? | Running total |
|---|---|---|---|---|---|
| (0,0) | `X` | edge → no | edge → no | ✅ top-left end | 1 |
| (0,3) | `X` | edge → no | `.` → no | ✅ top-left end | 2 |
| (1,3) | `X` | (0,3) is `X` → yes | — | ❌ | 2 |
| (2,3) | `X` | (1,3) is `X` → yes | — | ❌ | 2 |

Every other cell is `'.'` and skipped. Final answer: **2.** ✅ The single-cell ship at (0,0) counts once; the vertical 3-cell ship counts only at its top cell (0,3), and its lower cells are suppressed because each has an `'X'` right above it.

**Why it's correct:** consider any battleship. It's a straight run of `'X'`. Its **first cell** — topmost if vertical, leftmost if horizontal — has *no* ship-cell above it and *no* ship-cell to its left (if it did, the ship would extend further up or left, contradicting "first cell"). So that cell passes both tests and gets counted. **Every other cell of the ship** has a ship-cell immediately above it (vertical ship) or immediately to its left (horizontal ship), so it fails a test and is skipped. That's *exactly one* counted cell per ship. And because the "no two ships touch" rule guarantees a different ship's `'X'` can never sit directly above or left of this ship's start, we never mistake two adjacent ships for one or vice versa. One canonical cell per ship, no double counting, no misses.

**Complexity:** Time `O(m*n)` — one visit per cell, checking two neighbors is `O(1)`. Space `O(1)` — just a counter, and we never touch the board.

---

## ③ Space Optimization

**Already optimal — and this is the honest reason why.** The optimised scan holds a single integer counter and reads at most two already-existing neighbor cells per position. Nothing grows with the input: no `visited` grid, no recursion stack, no queue. We also never write to the board, so the "don't modify the input" clause is satisfied for free.

```python
# No further space to cut. We keep one integer (`ships`) and read O(1)
# neighbors per cell. There is nothing that scales with m or n to shrink.
```

You genuinely cannot beat `O(1)` here — you must look at every cell at least once to know it's not the start of a ship you'd otherwise miss, so `O(m*n)` time is a hard floor, and the auxiliary memory is already down to a single counter.

**Complexity:** Time `O(m*n)`, Space `O(1)`.

> If space is already optimal: **say so and explain why.** "It's O(1) — one counter, two local neighbor reads, no visited set, and I never mutate the board — so it clears the follow-up on every count." Naming the absence of a trick is as strong as finding one.

---

## Java (for Java interviewers)

```java
public int countBattleships(char[][] board) {
    if (board == null || board.length == 0 || board[0].length == 0) return 0;
    int rows = board.length, cols = board[0].length;
    int ships = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (board[r][c] != 'X') continue;
            if (r > 0 && board[r - 1][c] == 'X') continue;  // 'X' above → not the top end
            if (c > 0 && board[r][c - 1] == 'X') continue;  // 'X' left  → not the left end
            ships++;                                          // top-left end of a ship
        }
    }
    return ships;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (flood-fill components) | O(m·n) | O(m·n) |
| Optimised (count top-left ends) | O(m·n) | O(1) |
| Space-optimised | O(m·n) | O(1) — already optimal |

---

## Say it out loud (interview narration)

> *"My first read is Number of Islands — flood-fill each connected group of `X` and count the groups. That's correct but it needs a visited set or it mutates the board, and I see a follow-up asking for one pass and O(1) space. So I'll use the extra structure the problem hands me: ships are straight lines and no two touch. That means I can count each ship at exactly one cell — its top-left end. A cell is that end when it's an `X` with no `X` directly above it and no `X` directly to its left. Every ship has exactly one such cell, so I scan the grid once, apply that two-neighbor test, and increment. O(m·n) time, O(1) space, and I never modify the board."*

Before coding, ask the one clarifying question that proves you read the spec: *"Am I guaranteed no two battleships are adjacent? Because that's what lets me count each one locally instead of doing a full traversal."* Asking that early is exactly the General Cognitive Ability signal Google's rubric rewards.

## Related / follow-ups
- **Number of Islands (LC 200)** — the flood-fill parent; the version *without* the shape/separation guarantee, so you actually need the traversal.
- **Max Area of Island (LC 695)** — same component traversal, but you measure size instead of just counting.
- **Number of Closed Islands / Count Sub Islands** — component counting with an extra predicate per component.
- **Set Matrix Zeroes (LC 73)** — another "do it in O(1) space by using the grid's own structure" trick.
