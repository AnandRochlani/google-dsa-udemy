# Number of Good Paths

> **LeetCode:** 2421. Number of Good Paths · **Difficulty:** 🔴 Hard · **Pattern:** Union-Find + process by increasing value · **Google frequency:** ⭐ high

---

## Problem

You're given a **tree** — `n` nodes, `n-1` edges, connected, no cycles. Each node `i` carries a value `vals[i]`. A path from node `a` to node `b` is **good** when:

1. The two **endpoints have equal value** (`vals[a] == vals[b]`), **and**
2. **Every node on the path** has value **≤ that endpoint value**.

A single node counts as a good path (endpoints are equal — it's the same node). Paths are undirected, so `a→b` and `b→a` are the **same** path — count each once. Return the total number of good paths.

**Example:** `vals = [1,3,2,1,3]`, `edges = [[0,1],[0,2],[2,3],[2,4]]` → `6`

The tree looks like this (node:value):

```
        1(3)
         |
        0(1)
         |
        2(2)
        / \
     3(1) 4(3)
```

- **5 single nodes** → 5 good paths right away.
- The pair **1 and 4** (both value 3): path is `1 → 0 → 2 → 4`, values `3,1,2,3`. Endpoints are 3, and every node on the way (1, 2) is ≤ 3. ✅ Good — that's the 6th.
- The pair **0 and 3** (both value 1): path is `0 → 2 → 3`, but node 2 has value **2 > 1**. ❌ The path climbs above the endpoint value, so it's *not* good.

Total = **6**.

**Constraints that matter:** `n` up to `3·10⁴`. The number of same-valued pairs can be `O(n²)` — checking every pair and walking its tree path is `O(n³)` worst case, far too slow. The values can be large (`vals[i]` up to `10⁵`), so we sort/group by value rather than index. The `O(n log n)` bound is what we're chasing, and it comes from **sorting**, not from the union-find itself.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For every pair of nodes with the same value, find the unique path between them and check that nothing on it exceeds that value." In a tree the path between two nodes is *unique*, so this is well-defined — and it's the obvious brute force. The pain is obvious too: quadratically many pairs, each needing a linear walk.
- **Where it hurts:** you keep re-walking overlapping paths, and you keep asking the same question — *"can these two same-valued nodes reach each other without stepping above their value?"* — from scratch every time. That "can they reach each other under a value ceiling" question is screaming **connectivity**. And connectivity under a growing set of allowed nodes is exactly what **Union-Find** was built for.
- **The leap:** flip the problem around. Instead of *"for this pair, is the path clean?"*, ask *"if I only allow nodes with value ≤ v to exist, which same-valued nodes end up in the same connected blob?"* Grow `v` from **smallest to largest**. Each time you raise the ceiling to `v`, you switch on all edges whose **both** endpoints are now allowed (both ≤ v), merging blobs. The moment two nodes of value exactly `v` sit in the same blob, the path between them is guaranteed clean — because *every node in that blob has value ≤ v by construction.* That's the whole trick.
- **Pattern trigger:** **"connectivity under a threshold that only ever grows"** → **Union-Find, processed in increasing order.** The transferable move: when a constraint is monotonic (a ceiling that only rises, an edge weight you sweep upward), sort by it and union as you sweep — you never have to undo anything. Same DNA as Kruskal's MST and "Checking Existence of Edge Length Limited Paths."

> **Why *increasing* value, specifically?** Because a blob built only from edges with both endpoints ≤ `v` can *only* contain nodes ≤ `v`, and the path between any two of its nodes stays inside the blob — so it *never* rises above `v`. That's precisely condition #2 of a good path, handed to you for free. Go the other direction (largest first) and a blob could contain a huge node sitting on the path between two small ones, silently breaking the ceiling. Ascending order makes "same blob" *equal* "clean path." That equivalence is the engine.

---

## ① Brute Force

For every pair of same-valued nodes, walk the unique tree path and check its maximum. Add `n` for the single-node paths.

```python
from collections import defaultdict

def numberOfGoodPaths_brute(vals, edges):
    n = len(vals)
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    def path_max(src, dst):
        # tree ⇒ unique path; DFS to find it, return the biggest value on it
        parent = {src: -1}
        stack = [src]
        while stack:
            node = stack.pop()
            if node == dst:
                break
            for nei in g[node]:
                if nei not in parent:
                    parent[nei] = node
                    stack.append(nei)
        mx, cur = 0, dst
        while cur != -1:            # walk back up the path
            mx = max(mx, vals[cur])
            cur = parent[cur]
        return mx

    ans = n                        # every node alone is a good path
    for i in range(n):
        for j in range(i + 1, n):
            if vals[i] == vals[j] and path_max(i, j) == vals[i]:
                ans += 1           # equal endpoints AND nothing on the path exceeds them
    return ans
```

**Why it's the natural first attempt:** it's a direct transcription of the definition. Same value at the ends, nothing bigger in between — check exactly that, for every candidate pair.

**Why it's not enough:** there are up to `O(n²)` same-valued pairs, and each `path_max` is an `O(n)` graph walk — `O(n³)` in the worst case (think: all nodes share one value). At `n = 3·10⁴` that's astronomically over the time limit. Worse, it re-discovers the same path segments again and again — pure repeated work, the classic sign there's structure to exploit.

**Complexity:** Time `O(n³)` worst case, Space `O(n)`.

---

## ② Optimised Solution

Sweep the value ceiling upward with **Union-Find**. Sort edges by the **larger** of their two endpoint values; that value is the moment the edge becomes "usable" (both ends allowed). Keep, per component, a **histogram of how many nodes hold each value**. When an edge merges two components at ceiling `v`, the new good paths are exactly `countA[v] × countB[v]` — every value-`v` node on one side pairs with every value-`v` node on the other.

```python
from collections import Counter

def numberOfGoodPaths(vals, edges):
    n = len(vals)
    parent = list(range(n))
    cnt = [Counter({vals[i]: 1}) for i in range(n)]   # per-root value histogram

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:          # path compression
            parent[x], x = root, parent[x]
        return root

    ans = n                               # each node is a good path by itself
    # sort edges by the LARGER endpoint value → process ceilings low to high
    for u, v in sorted(edges, key=lambda e: max(vals[e[0]], vals[e[1]])):
        ru, rv = find(u), find(v)
        peak = max(vals[u], vals[v])      # this edge's ceiling; one endpoint equals it
        # cross-pairs of peak-valued nodes become good paths as the blobs merge
        ans += cnt[ru][peak] * cnt[rv][peak]
        # union, merging the smaller histogram into the larger (small-to-large)
        if len(cnt[ru]) < len(cnt[rv]):
            ru, rv = rv, ru
        parent[rv] = ru
        cnt[ru].update(cnt[rv])           # fold rv's counts into ru
        cnt[rv] = None                     # free the merged-away histogram
    return ans
```

**Walk the example** `vals = [1,3,2,1,3]`, `edges = [[0,1],[0,2],[2,3],[2,4]]`.

Each edge's ceiling = `max` of its endpoint values: `0-1 → 3`, `0-2 → 2`, `2-3 → 2`, `2-4 → 3`. Sorted ascending: **`0-2`(2), `2-3`(2), `0-1`(3), `2-4`(3)**. Start `ans = 5` (the singles). Histograms start as `{value: 1}` per node.

| Step | Edge (peak) | roots found | `cnt[ru][peak]` × `cnt[rv][peak]` | new paths | merged histogram | `ans` |
|---|---|---|---|---|---|---|
| 1 | `0-2` (2) | {0}, {2} | `0 × 1` | 0 | `{1:1, 2:1}` | 5 |
| 2 | `2-3` (2) | {0,2}, {3} | `1 × 0` | 0 | `{1:2, 2:1}` | 5 |
| 3 | `0-1` (3) | {0,2,3}, {1} | `0 × 1` | 0 | `{1:2, 2:1, 3:1}` | 5 |
| 4 | `2-4` (3) | {0,1,2,3}, {4} | `1 × 1` | **1** | `{1:2, 2:1, 3:2}` | **6** |

Only step 4 pays off: the big blob already holds one value-3 node (node 1), node 4 is another value-3 node, `1 × 1 = 1` new good path — the `1 → 0 → 2 → 4` we spotted by hand. Final `ans = 6`. ✅

Notice step 2: when the blob `{0,2}` absorbs node 3 (value 1) at ceiling 2, we ask about value-**2** nodes and get `1 × 0 = 0` — correctly nothing, because node 3 isn't a value-2 node. The value-1 pairing of nodes 0 and 3 never fires, because their connecting path runs through node 2 (value 2), and by the time we'd care about value 1 (ceiling 1, processed first) that edge wasn't switched on yet. The ordering quietly enforces the ceiling.

**Why it's correct:** Two invariants.
1. **A component only ever contains nodes ≤ the current ceiling.** We add an edge only when *both* endpoints are ≤ `peak`, and we process peaks in increasing order — so every node ever merged in was ≤ some peak we've already reached. Therefore the unique tree-path between any two nodes *inside a component* stays inside that component and never exceeds the ceiling. "Same component" ⟹ "path satisfies condition #2."
2. **`countA[v] × countB[v]` counts each good pair exactly once.** Pairs already sitting together inside `A` were counted when `A` formed; same for `B`. Merging `A` and `B` creates *only* the cross pairs — every value-`v` node in `A` against every value-`v` node in `B`. Since each edge's `peak` equals at least one endpoint's value, we always query the histogram at the right value. Summed over all merges, the value-`v` nodes that end up in one final blob contribute `C(c, 2)` total pairs — assembled correctly one merge at a time — plus the `c` singles we seeded into `ans = n`.

**Complexity:** Time `O(n log n)` — sorting the `n-1` edges dominates; `find` is near-`O(1)` amortized with path compression, and small-to-large histogram merging costs `O(n log n)` total. Space `O(n)` for the parent array and histograms combined.

---

## ③ Space Optimization

**Already `O(n)` — and that's the floor.** You need the parent array (`O(n)`) and, across all live components, the value histograms — whose counts sum to `n`, so `O(n)` total, never more. There's no rolling-variable trick: the algorithm's correctness *depends* on remembering, per component, how many nodes of each value it holds, and those counts are the reused state.

```python
# No sub-O(n) variant exists. The DSU parent array is O(n), and the union of all
# per-component histograms holds exactly n counts total. Small-to-large merging keeps
# the TIME at O(n log n); it doesn't change that the state itself is inherently O(n).
```

One honest refinement worth naming out loud: because we sweep values upward and *never* look back at a value once we've passed it, you *could* collapse each component's histogram down to "count of nodes at the current peak only," recomputing per value-group instead of carrying a full `Counter`. That's the alternative *group-by-value* formulation — same `O(n)` space, same `O(n log n)` time, just a different bookkeeping style. Neither beats `O(n)`.

**Complexity:** Time `O(n log n)`, Space `O(n)` (optimal — the DSU plus value counts are irreducible).

> Say so plainly: *"Space is O(n) and that's optimal — I need union-find plus a per-component count of values, and those counts sum to n no matter how I slice it."* Naming why it can't shrink is the strong-hire move.

---

## Java (for Java interviewers)

```java
public int numberOfGoodPaths(int[] vals, int[][] edges) {
    int n = vals.length;
    parent = new int[n];
    // per-root histogram: value -> how many nodes of that value in the component
    List<Map<Integer, Integer>> cnt = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        parent[i] = i;
        Map<Integer, Integer> m = new HashMap<>();
        m.put(vals[i], 1);
        cnt.add(m);
    }
    // sort edges by the LARGER endpoint value → sweep the ceiling upward
    Arrays.sort(edges, (a, b) ->
        Math.max(vals[a[0]], vals[a[1]]) - Math.max(vals[b[0]], vals[b[1]]));

    long ans = n;                                   // each node alone
    for (int[] e : edges) {
        int ru = find(e[0]), rv = find(e[1]);
        int peak = Math.max(vals[e[0]], vals[e[1]]); // this edge's ceiling
        int cu = cnt.get(ru).getOrDefault(peak, 0);
        int cv = cnt.get(rv).getOrDefault(peak, 0);
        ans += (long) cu * cv;                       // cross-pairs of peak-valued nodes
        // small-to-large merge
        if (cnt.get(ru).size() < cnt.get(rv).size()) { int t = ru; ru = rv; rv = t; }
        parent[rv] = ru;
        Map<Integer, Integer> big = cnt.get(ru), small = cnt.get(rv);
        for (Map.Entry<Integer, Integer> en : small.entrySet())
            big.merge(en.getKey(), en.getValue(), Integer::sum);
        cnt.set(rv, null);
    }
    return (int) ans;
}

private int[] parent;

private int find(int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];   // path compression
        x = parent[x];
    }
    return x;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (per-pair path walk) | O(n³) | O(n) |
| Optimised (Union-Find, sweep by value) | O(n log n) | O(n) |
| Space-optimised | — (none exists) | O(n) — irreducible (DSU + value counts) |

*(n = number of nodes. The `log n` is the edge sort; the union-find is near-linear.)*

---

## Say it out loud (interview narration)

> *"In a tree the path between two nodes is unique, so a good path is just: two equal-valued endpoints where nothing in between is bigger. Brute force checks every same-valued pair and walks its path — O(n³), too slow. The key realization: 'can two same-valued nodes reach each other without exceeding their value?' is a connectivity question, and the value ceiling only ever needs to rise — that's Union-Find swept in increasing order. I sort edges by their larger endpoint value, and turn an edge on only when both ends are under the current ceiling. Because I go low-to-high, any component contains only nodes at or below the ceiling, so the path between two of its nodes never rises above it — 'same component' means 'clean path,' for free. I keep a per-component histogram of values; when a merge joins two blobs at ceiling v, the new good paths are countA[v] times countB[v]. Start the answer at n for the single nodes. Time is O(n log n) — dominated by the sort — and space is O(n), which is optimal."*

Before you code, ask the one clarifying question that proves you read it: *"It's a tree, right — so exactly one path between any two nodes, no path enumeration needed?"* That reframes the whole problem and is exactly the clarifying instinct Google's rubric rewards.

## Related / follow-ups
- **Checking Existence of Edge Length Limited Paths (LC 1697)** — same "sort by a threshold, sweep upward, union as you go" skeleton, offline queries instead of counting.
- **Kruskal's Minimum Spanning Tree** — the archetype: sort edges by weight, union in increasing order, never undo.
- **Number of Provinces / Redundant Connection (LC 547, 684)** — plain Union-Find warm-ups if the DSU mechanics feel shaky.
- **Making a Large Island (LC 827)** — Union-Find with per-component aggregates (size instead of a value histogram).
