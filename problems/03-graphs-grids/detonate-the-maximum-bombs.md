# Detonate the Maximum Bombs

> **LeetCode:** 2101. Detonate the Maximum Bombs · **Difficulty:** 🟡 Medium · **Pattern:** Directed graph + DFS/BFS · **Google frequency:** ⭐ high

---

## Problem

You're given a list of `bombs`, where each bomb is `[x, y, r]` — a center at `(x, y)` and a blast **radius** `r`. When a bomb detonates, it triggers **every other bomb whose center falls inside its blast radius**. Those bombs then detonate too, triggering *their* in-range bombs, and so on — a chain reaction. You get to hand-detonate **exactly one** bomb to start it all. Return the **maximum number of bombs** that can go off from a single starting choice.

The one detail that decides everything: bomb `i` triggers bomb `j` when `j`'s center is within `i`'s radius —

```
(xi − xj)² + (yi − yj)² ≤ ri²
```

Notice `ri` — bomb `i`'s radius. Whether `i` reaches `j` depends on `i`'s radius, and whether `j` reaches `i` depends on `j`'s radius. Those can differ. **The reach is one-directional.**

**Example:** `bombs = [[2,1,3],[6,1,4]]` → `2`

*Distance² between the two centers is `(2−6)² + (1−1)² = 16`. Bomb 0 has `r² = 9`: `16 > 9`, so bomb 0 does **not** reach bomb 1. Bomb 1 has `r² = 16`: `16 ≤ 16`, so bomb 1 **does** reach bomb 0. Start at bomb 1 → it detonates bomb 0 → total 2. Start at bomb 0 → only itself → total 1. The best is 2.*

**Example:** `bombs = [[1,1,5],[10,10,5]]` → `1`

*Distance² is `(1−10)² + (1−10)² = 162`, both radii are `r² = 25`. Neither reaches the other. Best you can do is one bomb.*

**Constraints that matter:** `n` is small — up to `100` bombs. That's the green light for an `O(n²)` graph build and an `O(n)` traversal from each of the `n` starts. The dangerous constraint is the numbers: `x`, `y`, `r` range up to `10⁵`, so `(xi − xj)²` can hit `~4·10¹⁰` and `ri²` up to `10¹⁰`. That **overflows 32-bit int** — you must use 64-bit (Java `long`) or Python's big ints, and you must compare **squared** distances, never take a square root.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Union-Find! Group all the bombs that touch, find the biggest group." It's the reflex the second you hear *chain reaction* — connected components, done. Hold that thought, because it's a **trap**, and spotting *why* is exactly the signal Google wants.
- **Where it hurts:** union-find models an **undirected** relationship — "`i` and `j` are in the same blob." But look again at the trigger rule: bomb `i` reaches `j` when `j` is inside `i`'s radius. A big bomb can swallow a tiny neighbor that could never reach back. Reachability runs **one way**. Merge them into a single component and you've quietly claimed the small bomb can start a chain that engulfs the big one — which is false. Union-find throws away the direction, and the direction is the whole problem.
- **The leap:** stop thinking "who's connected to whom" and start thinking "**who can I reach if I start here.**" That's a directed graph. Draw an arrow `i → j` exactly when `i`'s blast covers `j`'s center. Now the answer is mechanical: from each starting bomb, follow the arrows and count how many distinct bombs you can reach. Take the max over all starts.
- **Pattern trigger:** **"asymmetric reachability + chain reaction"** → **directed graph, then DFS/BFS from every node.** The tell is that the relationship between two items isn't symmetric — `A` affects `B` but not necessarily the reverse. The instant a relation has a *direction*, undirected tools (union-find, "connected components") are the wrong shape, and you reach for directed edges plus traversal.

---

## ① Brute Force

Simulate the chain reaction from every starting bomb without ever building a graph: keep a frontier of "just exploded" bombs and, on each round, rescan **all** bombs to see which new ones fall in range.

```python
def maximum_detonation_brute(bombs):
    n = len(bombs)

    def chain(start):
        exploded = [False] * n
        exploded[start] = True
        frontier = [start]
        while frontier:
            nxt = []
            for i in frontier:                     # bombs that just went off
                xi, yi, ri = bombs[i]
                for j in range(n):                 # rescan EVERYONE every round
                    if not exploded[j]:
                        dx, dy = xi - bombs[j][0], yi - bombs[j][1]
                        if dx * dx + dy * dy <= ri * ri:   # j in i's range?
                            exploded[j] = True
                            nxt.append(j)
            frontier = nxt
        return sum(exploded)

    return max(chain(s) for s in range(n))
```

**Why it's the natural first attempt:** it's the problem read literally — "detonate this one, see what catches, repeat." No graph theory, just physics.

**Why it's not enough:** it *works* (and for `n ≤ 100` it even passes), but it recomputes the same in-range test over and over. The distance between bomb `i` and bomb `j` never changes — yet this rescans it every time a different start touches `i`. That in-range check is the expensive, repeated work. We're recomputing edges we could compute **once**. The structural fix is to build the reachability graph a single time, then just traverse it.

**Complexity:** Time `O(n³)` — `n` starts × up to `n` explosion rounds × `n` rescans, Space `O(n)`.

---

## ② Optimised Solution

Compute every directed edge **once** up front: `i → j` when bomb `j`'s center lies inside bomb `i`'s radius. Then from each start, run a DFS/BFS over those edges and count how many bombs are reachable. Return the biggest count.

```python
from collections import deque

def maximum_detonation(bombs):
    n = len(bombs)

    # ── 1. build the DIRECTED graph once: edge i -> j if j is in i's range ──
    graph = [[] for _ in range(n)]
    for i in range(n):
        xi, yi, ri = bombs[i]
        for j in range(n):
            if i == j:
                continue
            xj, yj, _ = bombs[j]
            dx, dy = xi - xj, yi - yj
            # squared distance vs squared radius — integer math, no floats.
            # ri is I's radius: this is directional and does NOT imply j -> i.
            if dx * dx + dy * dy <= ri * ri:
                graph[i].append(j)

    # ── 2. from each start, count everything reachable by following arrows ──
    def reachable(start):
        seen = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:          # only bombs u can trigger
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        return len(seen)

    return max(reachable(s) for s in range(n))
```

**Walk the example** `bombs = [[2,1,3],[6,1,4]]`:

**Build the graph.** Two bombs, so we test both ordered pairs. The squared distance between the centers is fixed at `16`.

| Edge tested | dist² | radius² (source's r²) | dist² ≤ r²? | Edge added? |
|---|---|---|---|---|
| `0 → 1` (bomb 0 reach bomb 1?) | 16 | `3² = 9` | `16 ≤ 9` ✗ | no |
| `1 → 0` (bomb 1 reach bomb 0?) | 16 | `4² = 16` | `16 ≤ 16` ✓ | **yes** |

So `graph = [[], [0]]` — a single arrow from 1 to 0, and *nothing* pointing back. This asymmetry is the entire lesson: same distance, different verdict, because each bomb judges with **its own** radius.

**Traverse from each start.**

| Start | BFS walk | Reachable count |
|---|---|---|
| 0 | `seen = {0}`; `graph[0]` is empty | **1** |
| 1 | `seen = {1}` → visit `graph[1] = [0]` → `seen = {1, 0}` | **2** |

`max(1, 2) = 2`. ✅ And note union-find would have merged `{0, 1}` into one component of size 2 and answered 2 here **by luck** — the asymmetry only bites when a small bomb reaches into a big one it can't be reached back from. That's the hidden test case union-find fails.

**Why it's correct:** the graph encodes reachability *exactly* — an arrow `i → j` exists iff detonating `i` directly sets off `j`. A chain reaction from `start` sets off precisely the set of bombs reachable from `start` by following arrows transitively, which is exactly what BFS/DFS enumerates (each bomb entered into `seen` once, and every out-edge of every exploded bomb is followed). Checking all `n` starts and taking the max guarantees we find the single best button to press. Using `dx*dx + dy*dy <= ri*ri` keeps everything in exact integers, so no floating-point rounding can flip a borderline `≤`.

**Complexity:** Time `O(n²)` to build the graph + `O(n · (n + E))` for `n` traversals over up to `E = O(n²)` edges = **`O(n³)`** worst case, Space `O(n²)` for the graph.

---

## ③ Space Optimization

The `O(n²)` here is honest, but you *can* trade the stored adjacency list for recomputing edges on the fly — skip the graph entirely and test the distance inside the traversal. That drops the graph's `O(n²)` memory down to `O(n)` for the visited set and stack, at the cost of recomputing each in-range check every time you traverse.

```python
def maximum_detonation_less_space(bombs):
    n = len(bombs)

    def in_range(i, j):                    # does bomb i reach bomb j?
        xi, yi, ri = bombs[i]
        xj, yj, _ = bombs[j]
        dx, dy = xi - xj, yi - yj
        return dx * dx + dy * dy <= ri * ri

    def reachable(start):
        seen = [False] * n
        seen[start] = True
        stack = [start]
        count = 1
        while stack:
            u = stack.pop()
            for v in range(n):             # recompute edges instead of storing
                if not seen[v] and in_range(u, v):
                    seen[v] = True
                    count += 1
                    stack.append(v)
        return count

    return max(reachable(s) for s in range(n))
```

**Complexity:** Time `O(n³)` (same order — the distance checks just moved into the traversal), Space `O(n)`.

> Honest read: with `n ≤ 100`, the `O(n²)` graph is at most 10,000 edges — a rounding error of memory. **Prefer the graph version in the interview.** It separates "build the model" from "use the model," which reads far cleaner and is easier to reason about out loud. Mention this space trade-off exists — "I could inline the checks to drop the adjacency list to O(n) if memory were tight" — but don't reach for it unless asked. Naming the trade you *chose not to make* is itself a signal of judgment.

---

## Java (for Java interviewers)

```java
public int maximumDetonation(int[][] bombs) {
    int n = bombs.length;
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());

    // 1. build the DIRECTED graph: edge i -> j if j's center is in i's radius
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            long dx = (long) bombs[i][0] - bombs[j][0];   // long: values up to 1e5,
            long dy = (long) bombs[i][1] - bombs[j][1];   // squared ~4e10 overflows int
            long r  = bombs[i][2];                        // I's OWN radius — directional
            if (dx * dx + dy * dy <= r * r) {
                graph.get(i).add(j);
            }
        }
    }

    // 2. from each start, BFS/DFS-count reachable bombs; keep the max
    int best = 0;
    for (int start = 0; start < n; start++) {
        boolean[] seen = new boolean[n];
        Deque<Integer> queue = new ArrayDeque<>();
        seen[start] = true;
        queue.add(start);
        int count = 1;
        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (int v : graph.get(u)) {
                if (!seen[v]) {
                    seen[v] = true;
                    count++;
                    queue.add(v);
                }
            }
        }
        best = Math.max(best, count);
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (re-simulate every start) | O(n³) | O(n) |
| Optimised (build graph once, traverse) | O(n³) | O(n²) |
| Space-optimised (inline distance checks) | O(n³) | O(n) |

*(All three are `O(n³)` worst case — the graph build itself is `O(n²)`, but `n` traversals over `O(n²)` edges dominate. With `n ≤ 100` this is trivially fast; the point of the optimised version is a clean, directional model, not an asymptotic win.)*

---

## Say it out loud (interview narration)

> *"First clarifying question: is the trigger relationship symmetric? Because bomb i reaches bomb j when j's center is inside i's radius — and since the radii differ, i reaching j does NOT mean j reaches i. That kills my first instinct, union-find, which only models undirected 'same group' relationships. So I'll build a **directed** graph instead: an arrow from i to j whenever i's blast covers j. I compute all edges once — that's O(n²) — using **squared** distance versus **squared** radius so I stay in exact integers and never touch a square root; and I'll use 64-bit ints because coordinates up to 10⁵ square past the 32-bit limit. Then from each of the n starting bombs I run a BFS or DFS and count everything reachable, and I return the max. n is only 100, so the O(n³) total is comfortably fast."*

The clarifying question about symmetry is the whole interview. Ask it before you write anything — voicing "wait, does i→j imply j→i?" and concluding "no, so union-find is wrong here" is precisely the General Cognitive Ability signal Google scores. Arriving at the directed graph *out loud*, by rejecting the undirected one, beats silently writing the right answer.

## Related / follow-ups
- **Number of Provinces (LC 547)** — the genuinely *undirected* version where union-find **is** right. Great contrast: same "count the reachable group" flavor, but a symmetric relation.
- **Course Schedule / Course Schedule II (LC 207 / 210)** — directed graph again, but now the question is cycle detection / topological order.
- **Find the Town Judge (LC 997)** — directed edges where in-degree vs out-degree is the whole trick; another "the direction matters" problem.
- **Number of Islands (LC 200)** — the undirected grid-DFS baseline this pattern builds on.
