# Clone Graph

> **LeetCode:** 133. Clone Graph · **Difficulty:** 🟡 Medium · **Pattern:** Graph BFS/DFS (hash map old→new) · **Google frequency:** medium

---

## Problem

You're given a reference to a node in a **connected undirected graph**. Return a **deep copy** (clone) of the entire graph. Each node holds an integer `val` and a list of its `neighbors`.

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

**Example:**

```
   1 --- 2
   |     |
   4 --- 3
```

Adjacency: `1:[2,4]`, `2:[1,3]`, `3:[2,4]`, `4:[1,3]`. You must return a brand-new graph with the same structure — new `Node` objects, none shared with the original.

**Constraints that matter:** up to 100 nodes, values unique `1..100`. The graph has **cycles** (it's undirected, so every edge is a 2-cycle: 1→2 and 2→1). That means a naive recursive copy without memoization **recurses forever**. The whole problem is really "traverse a graph with cycles safely, and don't duplicate nodes."

---

## 🧠 Intuition — how you'd actually arrive at this

> The core realization: cloning a graph = traversing it once while remembering which originals you've already cloned.

- **First instinct:** "Walk the graph and make a copy of each node." Fine — but the moment you follow node 1 → neighbor 2 → neighbor 1, you're back where you started. Undirected edges create cycles, so a plain DFS/BFS that doesn't track visited nodes loops forever.
- **The second realization — you need identity, not just visited:** it's not enough to know "I've seen node 2." When you're cloning node 1's neighbor list, you need *the specific clone object* for node 2 — the same clone every time 2 appears, so the copied graph's edges point to shared clone nodes, not fresh duplicates. So a plain `visited` set isn't enough; you need a **map from each original node → its clone**.
- **The leap — the hash map does double duty:** `old_to_new[original] = clone`. It's simultaneously (a) your visited set — "have I cloned this original yet?" — and (b) your lookup table — "give me the clone that corresponds to this original." One dict solves both the cycle problem and the sharing problem.
- **The traversal:** DFS or BFS over the original graph. For each original node, ensure its clone exists in the map, then wire the clone's neighbor list to the clones of the original's neighbors (creating them on first sight).
- **Pattern trigger:** **"deep copy / clone a linked structure with cycles"** → **traverse (DFS/BFS) with a `visited/original→copy` hash map.** Same trick powers "Copy List with Random Pointer."

---

## ① Brute Force

The "natural but broken" attempt: recursively copy each node and its neighbors, with **no memoization**.

```python
def cloneGraph_broken(node):
    if not node:
        return None
    clone = Node(node.val)
    # BUG: no map — re-clones every neighbor, and cycles never terminate
    clone.neighbors = [cloneGraph_broken(nei) for nei in node.neighbors]
    return clone
```

**Why it's the natural first attempt:** "to copy a node, copy its value and recursively copy its neighbors" is the textbook recursive-copy shape, and it's exactly right for a *tree*.

**Why it's not enough:** this graph isn't a tree — it has cycles. Cloning node 1 recurses into 2, which recurses into 1 (its neighbor), which recurses into 2… **infinite recursion → stack overflow.** Even pretending it terminated, it would create a *new* clone every time a node is reached by a different path, so the copy's structure would be wrong (duplicated nodes instead of shared ones).

**Complexity:** never terminates on a cyclic graph.

---

## ② Optimised Solution

Traverse with a `old_to_new` map that serves as both visited set and clone lookup. DFS version:

```python
def cloneGraph(node):
    if not node:
        return None
    old_to_new = {}                       # original node -> its clone

    def dfs(cur):
        if cur in old_to_new:
            return old_to_new[cur]        # already cloned → return the clone
        copy = Node(cur.val)
        old_to_new[cur] = copy            # record BEFORE recursing (breaks cycles)
        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(node)
```

BFS version:

```python
from collections import deque

def cloneGraph_bfs(node):
    if not node:
        return None
    old_to_new = {node: Node(node.val)}
    q = deque([node])
    while q:
        cur = q.popleft()
        for nei in cur.neighbors:
            if nei not in old_to_new:
                old_to_new[nei] = Node(nei.val)  # first sight → clone it
                q.append(nei)
            old_to_new[cur].neighbors.append(old_to_new[nei])
    return old_to_new[node]
```

**Walk the example** (`1-2-3-4` square) with DFS starting at node 1:

- `dfs(1)`: not in map → make clone `1'`, record `{1:1'}`. Iterate neighbors `[2,4]`.
  - `dfs(2)`: make `2'`, record `{1:1',2:2'}`. Neighbors `[1,3]`.
    - `dfs(1)`: **already in map** → return `1'`. So `2'.neighbors` gets `1'`. (Cycle broken here.)
    - `dfs(3)`: make `3'`, record it. Neighbors `[2,4]`.
      - `dfs(2)`: in map → return `2'`.
      - `dfs(4)`: make `4'`. Neighbors `[1,3]`.
        - `dfs(1)`→`1'`, `dfs(3)`→`3'`. `4'.neighbors = [1',3']`.
      - `3'.neighbors = [2',4']`.
    - `2'.neighbors = [1',3']`.
  - back in `dfs(1)`, `dfs(4)`: already in map → return `4'`.
  - `1'.neighbors = [2',4']`.
- Return `1'` — a fully cloned square with all-new nodes. ✅

**Why it's correct:** recording `old_to_new[cur]` **before** recursing into neighbors is what breaks cycles — when the recursion loops back to `cur`, it finds the clone already in the map and returns it instead of recursing again. Every original node is cloned exactly once, and every edge in the copy points at the correct shared clone.

**Complexity:** Time `O(V + E)` — each node cloned once, each edge traversed once. Space `O(V)` for the map plus `O(V)` for the recursion/queue.

---

## ③ Space Optimization

The `old_to_new` map is **fundamental, not incidental** — it's the only thing that lets us reuse clones and break cycles. You cannot drop it: without it you either duplicate nodes or loop forever. So `O(V)` space is a hard floor here.

The choosable part is the traversal frontier:
- **DFS** adds `O(V)` recursion stack (worst case a long chain of nodes).
- **BFS** adds `O(V)` queue in the worst case too.

Neither beats the other asymptotically; both are `O(V)` total on top of the mandatory `O(V)` map. BFS is safer if the graph could be deep enough to blow Python's recursion limit.

> Say it: *"The hash map from original to clone is doing the essential work — it's both my visited set and my clone lookup, so O(V) space is required, not optional. This is already optimal."*

---

## Java (for Java interviewers)

```java
// Definition for a Node.
// class Node { public int val; public List<Node> neighbors; ... }

public Node cloneGraph(Node node) {
    if (node == null) return null;
    Map<Node, Node> oldToNew = new HashMap<>();
    return dfs(node, oldToNew);
}

private Node dfs(Node cur, Map<Node, Node> oldToNew) {
    if (oldToNew.containsKey(cur)) return oldToNew.get(cur);
    Node copy = new Node(cur.val);
    oldToNew.put(cur, copy);                  // record before recursing
    for (Node nei : cur.neighbors) {
        copy.neighbors.add(dfs(nei, oldToNew));
    }
    return copy;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (no map) | ∞ (cycles loop forever) | — |
| Optimised DFS | O(V + E) | O(V) map + O(V) stack |
| Optimised BFS | O(V + E) | O(V) map + O(V) queue |

---

## Say it out loud (interview narration)

> *"The graph is undirected so it has cycles — a plain recursive copy would loop forever and would also duplicate nodes reached by multiple paths. The fix is a hash map from each original node to its clone. That map does double duty: it's my visited set, and it's how I look up the one canonical clone for a node so the copied edges point to shared nodes. I DFS from the start; for each node I create its clone and record it in the map *before* recursing into neighbors — that's what breaks the cycle. Each node is cloned once, each edge walked once, so O(V + E) time and O(V) space, which is required because the map is doing the essential work."*

## Related / follow-ups
- **Copy List with Random Pointer** (LC 138) — same original→copy hash-map trick on a linked list
- **Number of Islands** (LC 200) — traversal-with-visited on a grid graph
- **Course Schedule** (LC 207) — building/traversing an adjacency-list graph
- **Graph Valid Tree** (LC 261) — traversal with cycle detection
