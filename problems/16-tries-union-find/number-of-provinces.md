# Number of Provinces

> **LeetCode:** 547. Number of Provinces · **Difficulty:** 🟡 Medium · **Pattern:** Tries & Union-Find · **Google frequency:** medium

---

## Problem

There are `n` cities. You're given an `n × n` matrix `isConnected` where `isConnected[i][j] = 1` means city `i` and city `j` are directly connected. A **province** is a group of cities that are directly or indirectly connected. Return the number of provinces (connected components).

**Example:**
```
isConnected = [[1,1,0],
               [1,1,0],
               [0,0,1]]
→ 2
```
*(Cities 0 and 1 are connected → one province; city 2 is alone → a second province.)*

**Constraints that matter:** `n` up to 200, so the matrix is up to 200×200. This is the textbook **connected-components count** — solvable with DFS/BFS flood fill, but it's the canonical **Union-Find** teaching problem: merge connected cities, then count distinct roots.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Flood fill — pick an unvisited city, DFS/BFS to mark everything reachable as one province, repeat. The number of times you start a new fill is the answer." Perfectly valid and O(n²) here.
- **The Union-Find lens (the pattern to internalize):** think of each city as its own set. Every edge `isConnected[i][j] == 1` says "merge set of `i` with set of `j`." After processing all edges, the number of **distinct set roots** is the number of provinces.
- **How Union-Find stays fast:** each set is a tree; `find(x)` climbs to the root that names the set. **Path compression** flattens the tree during `find` (point every node straight at the root), and **union by rank** attaches the shorter tree under the taller one. Together they make each operation effectively **O(α(n))** — inverse Ackermann, basically constant.
- **Why choose Union-Find over DFS here?** For a static matrix, DFS is equally good. Union-Find shines when connections **stream in over time** and you must answer "connected?" incrementally without re-running DFS — this problem is the gentle introduction to that tool.
- **Pattern trigger:** **"count connected components / are these two in the same group / merge groups"** → **Union-Find** (or DFS flood fill for a one-shot count).

---

## ① Brute Force

Flood fill: DFS from each unvisited city, counting how many fills it takes.

```python
def findCircleNum_dfs(isConnected):
    n = len(isConnected)
    visited = [False] * n

    def dfs(i):
        for j in range(n):
            if isConnected[i][j] == 1 and not visited[j]:
                visited[j] = True
                dfs(j)

    provinces = 0
    for i in range(n):
        if not visited[i]:
            provinces += 1
            visited[i] = True
            dfs(i)
    return provinces
```

**Why it's the natural first attempt:** counting connected components by flood fill is the most direct reading — "how many separate blobs are there."

**Why it's "not enough":** nothing's wrong for a static matrix — it's O(n²), optimal here. The reason to reach past it is the *pattern lesson*: when edges arrive incrementally (dynamic connectivity), re-running DFS each query is wasteful, and Union-Find answers merges/queries in near-constant time. So we present Union-Find as the technique to master, not because DFS times out.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution (Union-Find)

Merge every connected pair, then count distinct roots. Here's the clean, reusable class you'll copy into any Union-Find problem:

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))    # each node starts as its own root
        self.rank = [0] * n             # tree height (upper bound) per root
        self.count = n                  # number of disjoint sets

    def find(self, x):
        # path compression: point x (and its ancestors) straight at the root
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                # already in the same set
        # union by rank: hang the shorter tree under the taller
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1                 # two sets became one
        return True


def findCircleNum(isConnected):
    n = len(isConnected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):       # upper triangle: matrix is symmetric
            if isConnected[i][j] == 1:
                uf.union(i, j)
    return uf.count
```

**Walk the example** `[[1,1,0],[1,1,0],[0,0,1]]`, start with `count = 3` (sets `{0}, {1}, {2}`):

| pair | isConnected? | union result | count |
|---|---|---|---|
| (0,1) | 1 | merge {0},{1} → {0,1} | 3 → 2 |
| (0,2) | 0 | skip | 2 |
| (1,2) | 0 | skip | 2 |

Final `count = 2`. ✅ Roots: `{0,1}` share a root, `{2}` alone.

**Why it's correct:** `union` merges two sets iff there's an edge, and it decrements `count` exactly when two *previously separate* sets combine (the `ra == rb` guard prevents double-counting). So `count` always equals the number of connected components. Path compression + union by rank keep every `find`/`union` near O(1) amortized.

**Complexity:** Time `O(n² · α(n))` ≈ `O(n²)` (we scan the matrix), Space `O(n)` for `parent`/`rank`.

---

## ③ Space Optimization

The two arrays `parent` and `rank` are inherent to Union-Find — together `O(n)`, which is already minimal for tracking `n` elements' membership. You can't go below `O(n)` because you must remember each node's set.

> Minor lever: you can drop the `rank` array and use **union by size** (one array instead of two) or even skip the balancing heuristic entirely — path compression alone still gives `O(log n)` amortized. But keeping both heuristics is the textbook near-constant version and the `rank` array is only `O(n)`, so there's nothing worth trimming. Already optimal at `O(n)`.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## Java (for Java interviewers)

```java
class UnionFind {
    int[] parent, rank;
    int count;
    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        count = n;
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
        if (ra == rb) return false;
        if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
        count--;
        return true;
    }
}

public int findCircleNum(int[][] isConnected) {
    int n = isConnected.length;
    UnionFind uf = new UnionFind(n);
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (isConnected[i][j] == 1) uf.union(i, j);
    return uf.count;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| DFS flood fill | O(n²) | O(n) |
| Union-Find | O(n² · α(n)) ≈ O(n²) | O(n) |

---

## Say it out loud (interview narration)

> *"This is counting connected components. DFS flood fill works — start a fill per unvisited city, count the fills, O(n²). But I'll use Union-Find because it's the tool for dynamic connectivity: each city starts as its own set, every edge unions two sets, and I keep a running count that drops by one each time two separate sets merge. find uses path compression and union uses union by rank, so operations are effectively constant. Final count is the number of provinces. Both are O(n²) here since I scan the matrix, but Union-Find is the one that generalizes when edges arrive over time."*

## Related / follow-ups
- **Number of Connected Components in an Undirected Graph** (LC 323 — same, edge list instead of matrix)
- **Redundant Connection** (LC 684 — union until an edge closes a cycle)
- **Accounts Merge** (LC 721 — union-find over emails)
- **Graph Valid Tree** (LC 261 — n−1 edges and one component)
- **Number of Islands** (LC 200 — components on a grid)
