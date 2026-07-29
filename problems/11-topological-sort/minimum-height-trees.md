# Minimum Height Trees

> **LeetCode:** 310. Minimum Height Trees · **Difficulty:** 🟡 Medium · **Pattern:** Topological Sort (leaf-trimming) · **Google frequency:** medium

---

## Problem

You're given a tree (a connected, undirected, acyclic graph) with `n` nodes labeled `0` to `n-1` and `n-1` edges. If you root the tree at some node, its **height** is the number of edges on the longest root-to-leaf path. Return **all** root labels that produce a tree of *minimum possible height*. The answer has one or two nodes.

**Example:** `n = 4`, `edges = [[1,0],[1,2],[1,3]]` → `[1]` *(rooting at the center node 1 gives height 1; any leaf gives height 2).*
`n = 6`, `edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]` → `[3, 4]`.

**Constraints that matter:** up to `2×10⁴` nodes. Trying every node as a root and BFS-ing its height is `O(n²)` — too slow. The insight: the best roots are the **center(s)** of the tree, and you can find them by peeling leaves inward, which is `O(n)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Root at every node, measure the height, keep the minimum." Correct but `O(n²)` — each of `n` roots costs an `O(n)` BFS.
- **Where it hurts / the reframe:** the roots that minimize height are the tree's **centroids** — the middle of its longest path (the *diameter*). A path graph of length `L` has its center in the middle; rooting anywhere else just makes one side longer. A tree has **at most two centroids** (one if the diameter has an even number of edges, two if odd).
- **The leap (topological leaf-trimming):** the leaves — nodes with only one connection — are the *worst* possible roots. So peel them all off simultaneously. That exposes a new layer of leaves; peel those too. Keep peeling, layer by layer, contracting the tree toward its middle. Whatever survives when `≤ 2` nodes remain **is** the center(s).
- **Why this is topological sort:** it's Kahn's algorithm on an *undirected* graph using **degree** instead of in-degree. A leaf is a node of **degree 1** (degree = number of edges touching it). You repeatedly remove degree-1 nodes and decrement their neighbors — exactly Kahn's BFS, trimming from the outside in.
- **Pattern trigger:** **"find the center / minimize eccentricity in a tree"** → **BFS leaf-trimming (topological peeling by degree).**

---

## ① Brute Force

Try each node as the root; BFS to find its height; track the minimum height and all nodes achieving it.

```python
from collections import deque

def find_min_height_trees_brute(n, edges):
    if n == 1:
        return [0]
    adj = {i: [] for i in range(n)}
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)

    def height(root):
        seen = {root}
        q = deque([root]); h = -1
        while q:
            h += 1
            for _ in range(len(q)):
                node = q.popleft()
                for nb in adj[node]:
                    if nb not in seen:
                        seen.add(nb); q.append(nb)
        return h

    heights = [height(r) for r in range(n)]
    best = min(heights)
    return [r for r in range(n) if heights[r] == best]
```

**Why it's the natural first attempt:** the problem literally asks "which roots give minimum height," so measuring every root's height is the direct reading.

**Why it's not enough:** `n` separate BFS traversals, each `O(n)`, is `O(n²)`. At `n = 2×10⁴` that's ~4×10⁸ operations → too slow.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution

Trim leaves layer by layer until ≤ 2 nodes remain — those are the centroids.

```python
from collections import deque

def find_min_height_trees(n, edges):
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]

    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)

    # initial leaves: degree 1
    leaves = deque(i for i in range(n) if len(adj[i]) == 1)
    remaining = n
    while remaining > 2:
        layer_size = len(leaves)
        remaining -= layer_size
        for _ in range(layer_size):
            leaf = leaves.popleft()
            nb = adj[leaf].pop()          # a leaf has exactly one neighbor
            adj[nb].remove(leaf)          # detach the leaf
            if len(adj[nb]) == 1:         # neighbor is now a leaf
                leaves.append(nb)

    return list(leaves)                   # 1 or 2 centroids left
```

**Walk the example** `n = 6`, `edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`:

- Adjacency: `0:{3}, 1:{3}, 2:{3}, 3:{0,1,2,4}, 4:{3,5}, 5:{4}`. Degrees: leaves are `0,1,2,5`.
- `remaining = 6`. Layer 1 = `[0,1,2,5]` (size 4) → `remaining = 2`. Trim each: removing 0,1,2 shrinks `3` to `{4}` (now degree... after removing 0,1,2, node 3 = {4}); removing 5 shrinks `4` to `{3}`. Both 3 and 4 become degree 1 and get queued.
- `remaining == 2`, loop stops. Surviving `leaves = [3, 4]` → **`[3, 4]`** ✅.

**Why it's correct:** a min-height root must sit at the center of the tree's longest path. Removing all current leaves shortens every longest path by one at *both* ends simultaneously, so the center is preserved. When `≤ 2` nodes remain, you've reached that center — one node if the diameter is even, two if odd.

**Complexity:** Time `O(n)` — each node is trimmed once, each edge touched a constant number of times. Space `O(n)`.

---

## ③ Space Optimization

`O(n)` space is required to hold the adjacency structure of a tree with `n-1` edges — you can't know a node's degree without storing its connections. The leaf queue and degree tracking are also `O(n)` in the worst case (a star graph has `n-1` initial leaves). So `O(n)` is the floor.

A minor tweak: instead of `set()` adjacency you can keep an integer `degree[]` array plus a normal adjacency list, decrementing `degree[nb]` on each trim and enqueuing when it hits 1. Same `O(n)` asymptotics, slightly lower constant factor and no set operations — a reasonable thing to mention, but not an asymptotic win.

> Space is already optimal at `O(n)` — a tree with `n` nodes needs its adjacency stored to reason about degrees; nothing here grows beyond that.

---

## Java (for Java interviewers)

```java
import java.util.*;

public List<Integer> findMinHeightTrees(int n, int[][] edges) {
    if (n == 1) return List.of(0);
    if (n == 2) return List.of(0, 1);

    List<Set<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new HashSet<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }

    Deque<Integer> leaves = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (adj.get(i).size() == 1) leaves.offer(i);

    int remaining = n;
    while (remaining > 2) {
        int layer = leaves.size();
        remaining -= layer;
        for (int i = 0; i < layer; i++) {
            int leaf = leaves.poll();
            int nb = adj.get(leaf).iterator().next();
            adj.get(nb).remove(leaf);
            if (adj.get(nb).size() == 1) leaves.offer(nb);
        }
    }
    return new ArrayList<>(leaves);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (BFS from every root) | O(n²) | O(n) |
| Leaf-trimming (topological peel) | O(n) | O(n) |

---

## Say it out loud (interview narration)

> *"Rooting at every node and measuring height is O(n²) — too slow at 2×10⁴. The key insight is that the best roots are the tree's center, the middle of its longest path, and there are at most two of them. So I peel leaves layer by layer: a leaf is a degree-1 node, and it's the worst possible root, so I remove all current leaves at once, which exposes the next layer. That's Kahn's algorithm on an undirected graph using degree instead of in-degree. I keep trimming until two or fewer nodes remain — those survivors are the centroids. It's O(n) time and space."*

## Related / follow-ups
- **Course Schedule / II** (Kahn's algorithm on a directed graph — same peeling idea by in-degree)
- **Tree Diameter** (the centers sit at the midpoint of the diameter)
- **Find the Celebrity** (another degree-based elimination)
