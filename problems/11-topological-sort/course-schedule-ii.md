# Course Schedule II

> **LeetCode:** 210. Course Schedule II · **Difficulty:** 🟡 Medium · **Pattern:** Topological Sort · **Google frequency:** ⭐ high

---

## Problem

Same setup as Course Schedule, but now **return a valid order** in which to take all `numCourses` courses (labeled `0` to `numCourses - 1`). Each prerequisite `[a, b]` means **take `b` before `a`**. If it's impossible (a cycle), return an **empty array**. Any valid order is accepted.

**Example:** `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]` → `[0, 1, 2, 3]` or `[0, 2, 1, 3]` *(0 first, 3 last, both valid).*
`numCourses = 2`, `prerequisites = [[1,0],[0,1]]` → `[]` *(cycle).*

**Constraints that matter:** up to `2000` courses, `5000` pairs. This is Course Schedule I plus one line: instead of just counting how many you took, **record the order** they came off the queue. That dequeue order *is* the topological order.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** it's identical to "can I finish?" — model prerequisites as a directed graph, edge `b → a` for each `[a, b]`. The only difference is the deliverable: an actual sequence.
- **The key observation:** in Kahn's algorithm, a course is dequeued **only after every one of its prerequisites has already been dequeued**. So the order in which courses leave the queue is, by construction, a legal topological order. You don't need any extra machinery — just append each course to a result list as you take it.
- **Cycle handling comes for free:** if a cycle exists, some courses never reach in-degree 0, so your result list ends up *shorter* than `numCourses`. When that happens, return `[]` as the problem demands.
- **Pattern trigger:** **"produce a valid ordering under dependency constraints"** → **Topological Sort.** Kahn's BFS gives you the order directly; DFS post-order (reversed) is the other standard way.

Recall the two definitions: **in-degree** = number of edges pointing *into* a node (unfinished prerequisites). A node with in-degree 0 has nothing blocking it.

---

## ① Brute Force

Repeatedly scan for any course whose prerequisites are all already placed, append it, and rescan. If a pass finds nobody but courses remain, there's a cycle → return `[]`.

```python
def find_order_brute(numCourses, prerequisites):
    prereqs = {c: set() for c in range(numCourses)}
    for a, b in prerequisites:
        prereqs[a].add(b)

    placed, order = set(), []
    while len(order) < numCourses:
        progress = False
        for c in range(numCourses):
            if c not in placed and prereqs[c] <= placed:  # all prereqs placed
                placed.add(c)
                order.append(c)
                progress = True
        if not progress:            # stuck → cycle
            return []
    return order
```

**Why it's the natural first attempt:** it literally builds the schedule step by step, always adding whatever is currently unblocked.

**Why it's not enough:** every `while` pass rescans all `numCourses` courses and re-tests each one's full prerequisite set against `placed`. That's up to `O(V²)` passes-times-nodes plus the subset checks — quadratic in the courses. It recomputes "who's ready" from scratch instead of updating incrementally.

**Complexity:** Time `O(V² + V·E)`, Space `O(V + E)`.

---

## ② Optimised Solution

Kahn's algorithm, appending each course to `order` as it's dequeued.

```python
from collections import deque

def find_order(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]   # b -> courses b unlocks
    indegree = [0] * numCourses
    for a, b in prerequisites:                # edge b -> a
        graph[b].append(a)
        indegree[a] += 1

    queue = deque(c for c in range(numCourses) if indegree[c] == 0)
    order = []
    while queue:
        course = queue.popleft()
        order.append(course)                  # dequeue order = topo order
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == numCourses else []
```

**Walk the example** `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`:

- Edges `0→1, 0→2, 1→3, 2→3`; in-degrees `[0,1,1,2]`. Queue `[0]`.
- Pop 0 → `order=[0]`; decrement 1,2 → in-degrees `[_,0,0,2]` → queue `[1,2]`.
- Pop 1 → `order=[0,1]`; decrement 3 → `indegree[3]=1`.
- Pop 2 → `order=[0,1,2]`; decrement 3 → `indegree[3]=0` → queue `[3]`.
- Pop 3 → `order=[0,1,2,3]`. `len(order)==4` → return **`[0,1,2,3]`** ✅.

(Had the queue popped 2 before 1, you'd get `[0,2,1,3]` — also valid. Both are correct topological orders.)

**Why it's correct:** a course enters the queue only when its last prerequisite was dequeued, so when we append it, every prerequisite already sits earlier in `order`. If a cycle exists, the trapped courses never reach in-degree 0, `len(order) < numCourses`, and we correctly return `[]`.

**Complexity:** Time `O(V + E)`, Space `O(V + E)`.

---

## ③ Space Optimization

Already at the space floor. You need the adjacency list (`O(E)`) to know what each course unlocks, the in-degree array (`O(V)`), the queue (`O(V)`), and the output list itself (`O(V)`, unavoidable — it *is* the answer). Nothing here is slack.

The alternative is **DFS post-order**: run DFS from each unvisited node, and after exploring all of a node's successors, push it onto a stack; the reversed stack is a topological order. Use a three-color marking to catch cycles (a gray node revisited on the current path = back edge = cycle → return `[]`). Same `O(V + E)` time and space, recursion stack in place of the queue. Kahn's is easier to explain and returns the order in the natural forward direction without a final reverse, so it's usually the better whiteboard choice.

> Space is already minimal — the output array itself dominates, and you can't produce an ordering without emitting it.

---

## Java (for Java interviewers)

```java
import java.util.*;

public int[] findOrder(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    int[] indegree = new int[numCourses];
    for (int[] p : prerequisites) {        // p = [a, b], edge b -> a
        graph.get(p[1]).add(p[0]);
        indegree[p[0]]++;
    }

    Deque<Integer> queue = new ArrayDeque<>();
    for (int c = 0; c < numCourses; c++)
        if (indegree[c] == 0) queue.offer(c);

    int[] order = new int[numCourses];
    int idx = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        order[idx++] = course;
        for (int nxt : graph.get(course))
            if (--indegree[nxt] == 0) queue.offer(nxt);
    }
    return idx == numCourses ? order : new int[0];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (rescan ready courses) | O(V² + V·E) | O(V + E) |
| Kahn's BFS | O(V + E) | O(V + E) |
| DFS post-order | O(V + E) | O(V + E) |

---

## Say it out loud (interview narration)

> *"This is Course Schedule I but I return the order instead of a boolean. I build the graph with edge `b → a` per prerequisite, compute in-degrees, and run Kahn's algorithm — seed the queue with zero-in-degree courses and pop them one at a time, appending each to my result. Because a course is only popped after all its prerequisites, the pop order is a valid topological order. If a cycle traps some courses, my result comes out shorter than numCourses, so I return an empty array. O(V + E) time and space."*

## Related / follow-ups
- **Course Schedule** (just the yes/no cycle-detection version)
- **Alien Dictionary** (derive edges from adjacent words, then this exact algorithm)
- **Sequence Reconstruction** (verify the topological order is *unique*)
- **Parallel Courses** (BFS layers = minimum semesters)
