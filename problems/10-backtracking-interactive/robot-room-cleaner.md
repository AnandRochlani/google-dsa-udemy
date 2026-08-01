# Robot Room Cleaner

> **LeetCode:** 489. Robot Room Cleaner · **Difficulty:** 🔴 Hard · **Pattern:** Backtracking / Interactive DFS (spiral backtracking) · **Google frequency:** ⭐ top-tier — a true Google classic

> **🚪 New section: Backtracking & Interactive.** This problem opens a genre Google loves and LeetCode barely prepares you for: **interactive problems**. You don't get the input. There is no grid parameter, no array to index. You get an *API* — a handful of calls that poke at a hidden world — and your job is to reconstruct enough of that world, in your own bookkeeping, to solve the problem. The transferable skill of this whole section: **when you're blind, build your own map.**

---

## Problem

You control a robot vacuum standing on an **unknown** cell of an **unknown** grid, facing **up**. Some cells are open, some are blocked, and you are never shown the grid. All you have is the robot's API:

- `move()` → tries to step one cell forward; returns `true` if it moved, `false` if a wall/obstacle blocked it (the robot stays put).
- `turnLeft()` / `turnRight()` → rotate 90° in place.
- `clean()` → clean the current cell.

**Clean every open cell reachable from the start.** You return nothing — success is judged by which cells got cleaned.

**Example:** the room below, robot starting at `S` facing up (`▓` is blocked):

```
A B C
S ▓ D
```

The robot must clean all five open cells `S, A, B, C, D` — including `D`, which it can only reach by going up to `A`, across the top through `B` and `C`, and down the far side. There's no "output"; cleaning all five is the answer.

**Constraints that matter:** the hidden room is at most `100 × 200`, so there's nothing to fear from size — the constraint that decides everything is **you never see the grid**. No coordinates are handed to you, so *you* must invent a coordinate system (relative to the start). And moves are **physical**: when your search wants to retreat, the robot can't teleport or pop a stack frame — it has to physically drive back. Those two facts *are* the problem.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "This is just Number of Islands / flood fill — DFS the grid, mark visited, clean everything." The instinct is *right* — this genuinely is DFS over the open cells. But two things you've always been given are missing: there's **no grid to index** (so where does `visited` live?) and **no free return** (in normal DFS, returning from recursion is free; here the robot is physically standing in the far cell).
- **Where it hurts:** without coordinates you can't remember where you've been, so any naive wandering revisits cells forever and can never prove it's done. And without a way to *undo* a move, a recursive DFS leaves the robot stranded — the recursion unwinds in your head while the robot sits at the dead end.
- **The leap:** two moves, one for each missing piece. **(1) Build your own coordinates:** call the start `(0, 0)`, facing up = "row − 1." Every successful `move()` updates your position in *your* map; `visited` is a set of *your* coordinates, and the hidden grid never needs to exist. **(2) Backtrack physically:** after a recursive call returns, execute a real-world undo — `turnRight, turnRight` (face backwards), `move()` (step back), `turnRight, turnRight` (face forwards again). Position *and* heading are exactly restored, so the parent call's bookkeeping stays truthful. The final polish: try the four directions in **clockwise order starting from the current heading** (the "spiral"), so advancing to the next candidate direction is always a single `turnRight()` — no direction arithmetic, no wasted turns.
- **Pattern trigger:** **"interactive / blind exploration — an API instead of an input"** → **DFS on your own coordinate system + a physical undo move**. Whenever the world is hidden behind `move()`-style calls, your reflex is: origin at the start, visited set in *relative* coordinates, and every recursive retreat mirrored by a real retreat.

---

## ① Brute Force

Wander: clean, try to move forward, and when blocked, turn some amount and try again — hoping random coverage eventually cleans everything.

```python
import random

def clean_room_random(robot):
    while True:                      # when do we stop? exactly.
        robot.clean()
        if not robot.move():
            for _ in range(random.randint(1, 3)):
                robot.turnRight()
```

**Why it's the natural first attempt:** it's what a memoryless robot *can* do, and it's roughly what the cheapest real vacuums did for years — bounce around and hope.

**Why it's not enough:** with no memory there is no termination condition — the robot can't distinguish "I've cleaned everything reachable" from "I keep re-cleaning the same hallway." Coverage is probabilistic, runtime is unbounded, and on an adversarial room shape it can starve a region for an arbitrarily long time. An interviewer will also probe the tempting "smarter" fix — *"why not BFS, like Number of Islands?"* — and that fails for a sneakier reason: BFS processes the frontier in queue order, hopping from a cell on one side of the room to a cell on the other. A stack frame can teleport; **a robot cannot**. Every BFS "pop" would require physically driving a computed path across everything you've explored — turning each step into an `O(cells)` journey. DFS is the right shape *because its retreat is local*: undoing one step of recursion is exactly one physical step backwards.

**Complexity:** Time unbounded (no termination guarantee), Space `O(1)` — and that `O(1)` memory is precisely why it can't work.

---

## ② Optimised Solution

**Spiral backtracking DFS.** Invent coordinates relative to the start, DFS over them with a `visited` set, try directions in clockwise order starting from the current heading, and after every recursive call **physically back up** and restore the heading.

```python
def cleanRoom(robot):
    # clockwise order — up, right, down, left — so that turnRight()
    # advances to the next candidate direction with zero bookkeeping
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    visited = set()

    def go_back():
        # physical undo: 180° turn, one step back, 180° turn again
        robot.turnRight(); robot.turnRight()   # face the way we came
        robot.move()                           # guaranteed open — we just came from there
        robot.turnRight(); robot.turnRight()   # restore the original heading

    def dfs(row, col, d):                      # robot is AT (row, col), FACING d
        visited.add((row, col))
        robot.clean()
        for i in range(4):
            nd = (d + i) % 4                   # current heading after i right turns
            nr, nc = row + DIRS[nd][0], col + DIRS[nd][1]
            if (nr, nc) not in visited and robot.move():
                dfs(nr, nc, nd)
                go_back()                      # child left us where it started; undo one step
            robot.turnRight()                  # rotate to the next heading — even after a failed move
        # four right turns total → we exit facing d, exactly as we entered

    dfs(0, 0, 0)                               # the start is our origin; facing up = 0
```

**Walk one example** — the room above, `S` = our `(0, 0)`, up = row −1, so `A=(-1,0)`, `B=(-1,1)`, `C=(-1,2)`, `D=(0,2)`, blocked cell = `(0,1)`:

| Robot at | Tries heading | Result |
|---|---|---|
| `S (0,0)` facing up | up | `move()` ✓ → recurse into `A`, clean it |
| `A (-1,0)` | up | wall — `move()` ✗, `turnRight` |
| `A` | right | ✓ → clean `B (-1,1)` |
| `B` | right | ✓ → clean `C (-1,2)` |
| `C` | right | wall ✗ → turn; **down** ✓ → clean `D (0,2)` |
| `D` | down ✗ wall · left ✗ blocked `(0,1)` · up — `C` visited, skip · right ✗ wall | dead end — all four headings exhausted |
| `D → C` | — | **`go_back()`**: turnRight ×2 (now facing up), `move()` (back on `C`), turnRight ×2 (facing down again — exactly the heading `C`'s loop expects) |
| `C → B → A → S` | — | each frame finishes its remaining headings (everything is visited or wall) and unwinds the same way; `S` checks right/down/left, all blocked or walls |

Five cells, five `clean()` calls, every cell entered exactly once. ✅

**Why it's correct:** two invariants carry the whole proof. **(1) `dfs(row, col, d)` always begins with the robot physically at `(row, col)` facing `d`, and always ends the same way** — the loop makes exactly four `turnRight()` calls (net 360°), and every excursion into a child is followed by `go_back()`, which is an exact inverse (the backward cell is open because we just traversed it). So the physical robot and our virtual coordinates never drift apart. **(2) Standard DFS coverage:** every open cell reachable from the start is adjacent to some visited cell along a path, each cell is entered at most once (the `visited` check), and each is cleaned when entered — so all reachable cells get cleaned and the recursion terminates.

**Complexity:** Time `O(N)` where `N` = reachable open cells — each cell is entered once, does at most 4 move-attempts + 4 turns, and each DFS edge costs one extra `go_back` (3 constant API calls... 5 calls, still `O(1)`). Space `O(N)` for `visited` plus `O(N)` recursion depth in the worst (snake-shaped) room.

---

## ③ Space Optimization

**Already optimal — and the reason is the heart of the problem.** The `visited` set *is the map the robot was never given*. A blind robot with `o(N)` memory cannot, in general, distinguish cells it has cleaned from cells it hasn't — forget any cell and you either re-clean it forever or can't prove you're done (that's exactly the brute force's disease). The recursion stack is likewise forced: it's the physical breadcrumb trail back to unexplored territory. You could convert the recursion to an explicit stack, but it holds the same `O(N)` path in the worst case.

```python
# No space-optimised variant exists: visited IS the self-built map, and
# remembering where you've been is the entire difference between this
# solution and the never-terminating random walk.
```

**Complexity:** Time `O(N)`, Space `O(N)` — forced.

> Say it out loud: *"Space is O(N) and that's the floor — the robot is blind, so the visited set is the map I'm building myself. Drop any part of it and I lose termination, which is precisely what's wrong with the naive wanderer."*

---

## Java (for Java interviewers)

```java
class Solution {
    // clockwise: up, right, down, left — matches turnRight()
    private static final int[][] DIRS = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    private final Set<String> visited = new HashSet<>();
    private Robot robot;

    public void cleanRoom(Robot robot) {
        this.robot = robot;
        dfs(0, 0, 0);                          // start = origin, facing up = 0
    }

    private void dfs(int row, int col, int d) {
        visited.add(row + "," + col);
        robot.clean();
        for (int i = 0; i < 4; i++) {
            int nd = (d + i) % 4;
            int nr = row + DIRS[nd][0];
            int nc = col + DIRS[nd][1];
            if (!visited.contains(nr + "," + nc) && robot.move()) {
                dfs(nr, nc, nd);
                goBack();                       // restore position AND heading
            }
            robot.turnRight();                  // next heading, even after a failed move
        }
        // net four right turns: we exit facing d, as we entered
    }

    private void goBack() {
        robot.turnRight();
        robot.turnRight();
        robot.move();                           // step back — guaranteed open
        robot.turnRight();
        robot.turnRight();
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (memoryless wandering) | unbounded — no termination guarantee | O(1) |
| Optimised (spiral backtracking DFS) | O(N) cleans/moves | O(N) visited + O(N) recursion |
| Space-optimised | — (none exists) | O(N) — the visited set *is* the self-built map |

*(N = number of open cells reachable from the start.)*

---

## Say it out loud (interview narration)

> *"This is DFS on a graph I can't see, so I'll solve the two things the blindness takes away. First, coordinates: I declare the start to be (0, 0) facing up, and track my position myself — the visited set lives in my own relative coordinate system, so the hidden grid never matters. Second, backtracking: recursion normally retreats for free, but this robot is physical, so after every recursive call I execute a real undo — turn 180, move one step back, turn 180 again — which restores both position and heading. I try the four directions in clockwise order starting from my current heading, so stepping to the next direction is always a single turnRight, and each DFS call makes exactly four right turns, meaning it exits facing the way it entered — that invariant is what keeps my virtual map and the physical robot in sync. Time is O(N) over reachable cells — each cell is entered once with constant API calls; space is O(N) for the visited set and recursion, and that's forced: the visited set is the map I was never given."*

Before you code, ask the clarifying questions that prove you understand the interaction model: *"The robot starts on an open cell facing up, moves are 4-directional, and `move()` returns false and stays put when blocked — right?"* Nailing the API contract out loud, before touching the keyboard, is exactly what the interactive genre is testing.

## Related / follow-ups
- **Guess the Word (LC 843)** — the *other* famous Google interactive: no grid at all, just a `master.guess()` API and an information-elimination strategy. Next lesson.
- **Number of Islands (LC 200)** — the same DFS with the blindfold off; do that one first if this felt steep.
- **Unique Paths III (LC 980)** — walk over every open cell exactly once; backtracking where the *undo* is virtual instead of physical.
- **Word Search (LC 79)** — grid backtracking with explicit mark/unmark — the "undo move" idea in its classic form.
