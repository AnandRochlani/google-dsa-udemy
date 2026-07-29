# Course Schedule

> **LeetCode:** 207. Course Schedule · **Difficulty:** 🟡 Medium · **Pattern:** Topological Sort · **Google frequency:** ⭐ high

---

## Problem

You have `numCourses` courses labeled `0` to `numCourses - 1`. Some courses have prerequisites given as pairs `[a, b]`, meaning **you must take course `b` before course `a`**. Return `True` if you can finish all courses, `False` otherwise.

**Example:** `numCourses = 2`, `prerequisites = [[1, 0]]` → `True` *(take 0, then 1).*
`numCourses = 2`, `prerequisites = [[1, 0], [0, 1]]` → `False` *(1 needs 0, 0 needs 1 — a deadlock).*

**Constraints that matter:** up to `2000` courses and `5000` prerequisite pairs. The real question hiding inside "can you finish?" is **"does this dependency graph contain a cycle?"** If there's a cycle, some course can never become takeable, and the answer is `False`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Tasks with prerequisites... I keep looking for a course whose prerequisites are all done, take it, and repeat." That literal simulation works, but scanning all courses every round is wasteful.
- **Reframe it as a graph:** each prerequisite `[a, b]` is a **directed edge `b → a`** ("b unlocks a"). "Can I finish?" becomes "**can I order the nodes so every edge points forward?**" — a **topological sort**. A topological order exists **if and only if the graph has no cycle**.
- **The leap (Kahn's BFS):** define the **in-degree** of a node as *the number of edges pointing into it* — here, the number of unfinished prerequisites a course still has. A course is takeable the moment its in-degree hits `0`. So: start with every 0-in-degree course, take it, and "remove" it by decrementing the in-degree of everything it unlocks. Anything that drops to 0 becomes newly takeable. If you manage to take **all** the courses this way, no cycle exists.
- **Why a cycle blocks it:** courses tangled in a cycle each wait on each other, so their in-degree never reaches 0 — they never enter the queue. Count how many you took; if it's fewer than `numCourses`, there was a cycle.
- **Pattern trigger:** **"ordering with prerequisites / dependencies" or "detect a cycle in a directed graph"** → **Topological Sort (Kahn's BFS on in-degrees, or DFS post-order).**

---

## ① Brute Force

Repeatedly scan every remaining course looking for one whose prerequisites are all satisfied; take it, mark it done, and rescan from scratch. If a full pass finds nobody takeable but courses remain, you're stuck.

```python
def can_finish_brute(numCourses, prerequisites):
    remaining = set(range(numCourses))
    # prereqs[c] = set of courses that must come before c
    prereqs = {c: set() for c in range(numCourses)}
    for a, b in prerequisites:
        prereqs[a].add(b)

    while remaining:
        takeable = [c for c in remaining if prereqs[c].isdisjoint(remaining)]
        if not takeable:              # nobody is takeable → cycle
            return False
        for c in takeable:
            remaining.discard(c)
    return True
```

**Why it's the natural first attempt:** it mirrors exactly how a student reasons — "what can I take right now?" — and re-checks after each batch.

**Why it's not enough:** each `while` pass rescans every remaining course and, for each, tests its prerequisites against the `remaining` set. In the worst case that's roughly `O(V²)` node work on top of the edge checks. It re-derives "who's takeable" from scratch every round instead of updating incrementally.

**Complexity:** Time `O(V² + V·E)` in the worst case, Space `O(V + E)`.

---

## ② Optimised Solution

Kahn's algorithm: track each node's in-degree, seed a queue with the 0-in-degree nodes, and decrement neighbors as you pop.

```python
from collections import deque

def can_finish(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]   # b -> list of courses b unlocks
    indegree = [0] * numCourses               # unfinished prereqs per course
    for a, b in prerequisites:                # [a, b]: take b before a  (b -> a)
        graph[b].append(a)
        indegree[a] += 1

    queue = deque(c for c in range(numCourses) if indegree[c] == 0)
    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:             # this course unlocks nxt
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return taken == numCourses                # all taken ⇒ no cycle
```

**Walk the example** `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`:

- Edges: `0→1, 0→2, 1→3, 2→3`. In-degrees: `[0, 1, 1, 2]`.
- Queue starts `[0]` (only course 0 has in-degree 0). Take 0 (`taken=1`) → decrement 1 and 2 → in-degrees `[_,0,0,2]` → queue `[1, 2]`.
- Take 1 (`taken=2`) → decrement 3 → `indegree[3]=1`. Take 2 (`taken=3`) → decrement 3 → `indegree[3]=0` → queue `[3]`.
- Take 3 (`taken=4`). Queue empty. `taken == 4 == numCourses` → **`True`**. ✅

For the deadlock `[[1,0],[0,1]]`: in-degrees `[1,1]`, queue starts empty, `taken` stays `0 ≠ 2` → **`False`**.

**Why it's correct:** a node is dequeued only when all its prerequisites have already been taken, so the dequeue order *is* a valid topological order. Nodes on a cycle can never reach in-degree 0, so they're never taken — `taken < numCourses` exactly captures "a cycle exists."

**Complexity:** Time `O(V + E)` — each node enqueued once, each edge relaxed once. Space `O(V + E)`.

---

## ③ Space Optimization

The `O(V + E)` space is **inherent, not wasteful**: you must store the adjacency list to know what each course unlocks (`O(E)`), the in-degree array (`O(V)`), and the queue (`O(V)`). There's no way to answer the question without knowing the graph, so `O(V + E)` is the floor.

The one honest trade-off is **DFS instead of BFS**: a three-color DFS (white/gray/black) detects a back-edge — a node revisited while still on the recursion stack — and reports the cycle without an explicit in-degree array. Same `O(V + E)` time and space (the recursion stack replaces the queue), so it's a stylistic choice, not a memory win. Kahn's is usually cleaner to narrate because "in-degree 0 = takeable" maps directly onto the story.

> Already at the space floor — you can't detect a cycle without materializing the dependency graph.

---

## Java (for Java interviewers)

```java
import java.util.*;

public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    int[] indegree = new int[numCourses];
    for (int[] p : prerequisites) {       // p = [a, b], edge b -> a
        graph.get(p[1]).add(p[0]);
        indegree[p[0]]++;
    }

    Deque<Integer> queue = new ArrayDeque<>();
    for (int c = 0; c < numCourses; c++)
        if (indegree[c] == 0) queue.offer(c);

    int taken = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        taken++;
        for (int nxt : graph.get(course))
            if (--indegree[nxt] == 0) queue.offer(nxt);
    }
    return taken == numCourses;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (rescan takeable) | O(V² + V·E) | O(V + E) |
| Kahn's BFS | O(V + E) | O(V + E) |
| DFS cycle detection | O(V + E) | O(V + E) |

---

## Say it out loud (interview narration)

> *"Each prerequisite `[a, b]` is a directed edge `b → a`, so 'can I finish?' is really 'is this graph acyclic?' I'll use Kahn's algorithm: compute each course's in-degree — its number of unfinished prerequisites — and seed a queue with the zero-in-degree courses. Pop one, count it as taken, and decrement the in-degree of everything it unlocks; anything that hits zero joins the queue. If I take all `numCourses`, there's no cycle and the answer is true; if fewer, a cycle trapped the rest. It's O(V + E) time and space, which is the floor since I have to store the graph."*

## Related / follow-ups
- **Course Schedule II** (return the actual order, not just yes/no)
- **Alien Dictionary** (build the graph from word ordering, then topo-sort)
- **Minimum Height Trees** (topological trimming of leaves)
- **Sequence Reconstruction** (is the topo order unique?)
