# Redundant Connection

> **LeetCode:** 684. Redundant Connection · **Difficulty:** 🟡 Medium · **Pattern:** Tries & Union-Find · **Google frequency:** medium

---

## Problem

A tree of `n` nodes (labeled `1..n`) had exactly **one extra edge** added, creating a graph with `n` nodes and `n` edges — so it now contains exactly one cycle. Given the edges in order, return the **one edge that can be removed** so the result is a tree. If several answers exist, return the edge that appears **last** in the input.

**Example:** `edges = [[1,2], [1,3], [2,3]]` → `[2,3]` *(1–2 and 1–3 already connect nodes 1, 2, 3 into a tree; adding 2–3 closes a cycle, so 2–3 is the redundant edge).*

**Constraints that matter:** `n` up to ~1000, exactly `n` edges and one cycle. Because we return the **last** edge that completes a cycle, processing edges **in input order** and stopping at the first one whose endpoints are *already connected* gives exactly the required answer — a perfect fit for **Union-Find**.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each edge, temporarily remove it and check whether the rest is still connected / acyclic with DFS." That's O(n) per edge × n edges = O(n²), and fiddly to implement.
- **The leap:** add edges one at a time and maintain the connectivity of what you've built so far. For each edge `(u, v)`: if `u` and `v` are **already in the same connected set**, then adding this edge creates a cycle — and since it's the *first* such edge in input order that closes a cycle, and there's only one cycle, it's exactly the redundant edge to return. Otherwise, `union(u, v)` to record the new connection.
- **Why "already connected ⇒ this edge is redundant":** if `u` and `v` already have a path between them (they're in the same set), a direct edge `u–v` is a second path — a cycle. In a graph that's a tree plus one edge, the single extra edge is precisely the one whose endpoints were already joined by the earlier edges.
- **Pattern trigger:** **"detect the cycle-closing edge / add edges and find when connectivity breaks"** → **Union-Find**: `find(u) == find(v)` before union means this edge is redundant.

---

## ① Brute Force

For each edge, build the graph from all *other* edges and check if `u` and `v` are already connected via DFS; the last such edge is the answer. (Simpler equivalent: for each candidate from the end, remove it and test if the rest is a valid tree.)

```python
def findRedundant_brute(edges):
    n = len(edges)
    from collections import defaultdict

    def connected(u, v, skip):
        graph = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            if i == skip:
                continue
            graph[a].append(b)
            graph[b].append(a)
        seen, stack = set(), [u]
        while stack:
            x = stack.pop()
            if x == v:
                return True
            if x in seen:
                continue
            seen.add(x)
            stack.extend(graph[x])
        return False

    for i in range(n - 1, -1, -1):     # prefer the last edge
        u, v = edges[i]
        if connected(u, v, i):         # still connected without edge i → i is redundant
            return edges[i]
    return []
```

**Why it's the natural first attempt:** "is this edge removable while keeping everything connected?" is the literal question, answered with a graph traversal.

**Why it's not enough:** it rebuilds the graph and runs a DFS for each candidate edge — O(n²). It also re-derives connectivity from scratch every time instead of accumulating it.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution (Union-Find)

Process edges in order; the first edge whose endpoints are already unioned is the answer.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                # already connected → cycle
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def findRedundantConnection(edges):
    uf = UnionFind(len(edges) + 1)      # nodes are 1..n; index 0 unused
    for u, v in edges:
        if not uf.union(u, v):          # union returns False → they were connected
            return [u, v]
    return []
```

**Walk the example** `[[1,2], [1,3], [2,3]]` (start: every node its own set):

| edge | find(u) vs find(v) | union? | sets after |
|---|---|---|---|
| (1,2) | 1 ≠ 2 | merge | {1,2}, {3} |
| (1,3) | find(1)=1 ≠ 3 | merge | {1,2,3} |
| (2,3) | find(2)=1, find(3)=1 → **equal** | **fails** → return **[2,3]** ✅ |

**Why it's correct:** we add edges in input order, so connectivity reflects exactly the prefix of edges seen. The moment `union(u, v)` finds `u` and `v` already share a root, edge `(u, v)` is the one that closes a cycle. In a "tree + one edge" graph there's a single cycle, and the first edge (in input order) that closes it is the last edge of the cycle to be added — which is exactly the "return the last one" answer the problem wants.

**Complexity:** Time `O(n · α(n))` ≈ `O(n)`, Space `O(n)` for `parent`/`rank`.

---

## ③ Space Optimization

The `parent` (and `rank`) arrays are inherent — `O(n)` to track membership of `n` nodes, and you can't go lower since you must remember which set each node is in.

> You could drop `rank` and rely on path compression alone (`O(log n)` amortized instead of `O(α(n))`) to use a single array, but `rank` is only `O(n)` and buys the near-constant guarantee, so it's not worth trimming. Already optimal at `O(n)` space, `O(n)` time — a single linear pass with no graph rebuild.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## Java (for Java interviewers)

```java
class UnionFind {
    int[] parent, rank;
    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];   // path compression
            x = parent[x];
        }
        return x;
    }
    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;          // already connected → cycle
        if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
        return true;
    }
}

public int[] findRedundantConnection(int[][] edges) {
    UnionFind uf = new UnionFind(edges.length + 1);   // nodes 1..n
    for (int[] e : edges) {
        if (!uf.union(e[0], e[1])) return e;          // closes a cycle
    }
    return new int[0];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute (remove-and-DFS per edge) | O(n²) | O(n) |
| Union-Find | O(n · α(n)) ≈ O(n) | O(n) |

---

## Say it out loud (interview narration)

> *"The graph is a tree plus one extra edge, so it has exactly one cycle, and I want the last edge that closes it. I process edges in order with Union-Find, unioning each edge's endpoints. The first edge whose two endpoints are already in the same set is the redundant one — because they're already connected by earlier edges, this edge forms a second path, i.e. the cycle. find uses path compression and union uses union by rank, so it's a single O(n) pass — no repeated graph rebuilds like the brute-force remove-and-check."*

## Related / follow-ups
- **Number of Provinces** (LC 547 — same Union-Find, counting components)
- **Redundant Connection II** (LC 685 — directed version, also handle a node with two parents)
- **Graph Valid Tree** (LC 261 — n−1 edges, no cycle, one component)
- **Accounts Merge** (LC 721 — union-find on emails)
