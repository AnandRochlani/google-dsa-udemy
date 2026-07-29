# The Earliest Moment When Everyone Become Friends

> **LeetCode:** 1101. The Earliest Moment When Everyone Become Friends · **Difficulty:** 🟡 Medium · **Pattern:** Union-Find (Disjoint Set Union) · **Google frequency:** ⭐ high

---

## Problem

You're given `n` people, labelled `0` to `n-1`, and a list of `logs`. Each log is `[timestamp, personA, personB]` and means: at that timestamp, A and B became friends. Friendship is **transitive** — if A knows B and B knows C, then A is "acquainted" with C, even if they never met directly. Return the **earliest timestamp** at which *every* person is acquainted with *every* other person (the whole group is one connected friend-circle). If that never happens, return `-1`.

**Example:** `n = 6`, `logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],[20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]]` → `20190301`

*(By `20190301` the two clumps `{0,1,5}` and `{2,3,4}` finally merge into one group of six. Everything after that is redundant.)*

**Constraints that matter:** `logs` can hold up to `10^4` entries and `n` up to `100`. The logs arrive **in arbitrary timestamp order**, so you must sort them — sorting is what lets "the first moment everyone connects" actually mean *earliest in time*. Once sorted, the real question is a stream of `merge these two groups / are they already together?` operations — which is the exact fingerprint of Union-Find.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Build a friendship graph. Add edges in time order. After each new friendship, check whether the whole graph is connected — a BFS or DFS from person 0 that reaches all `n` people." That's correct, and it's the natural first move.
- **Where it hurts:** you re-run a full graph traversal after *every single log*. Adding one edge barely changes the picture, yet you re-walk the entire graph from scratch each time — thousands of near-identical traversals. The connectivity answer changes slowly; your work does not.
- **The leap:** you don't need the whole picture — you only need one number: **how many separate friend-groups are left?** Start with `n` groups (everyone alone). Every log either **merges two different groups** (the count drops by one) or joins two people **already in the same group** (the count doesn't move). The instant the count hits **1**, everyone is in a single circle — and because you're processing logs in time order, that's the *earliest* such moment. No traversal. Just a running counter.
- **Pattern trigger:** *"a stream of `connect(a, b)` operations + a running `are these two in the same group?` question"* → **Union-Find (Disjoint Set Union)**. The transferable move: when a problem is about **groups merging over time** and you never need to *split* them, reach for DSU — near-constant time per merge, and the group count falls out for free.

---

## ① Brute Force

Add friendships in timestamp order into an adjacency list; after each one, run a fresh BFS/DFS from person `0` and count how many people it reaches. The first time it reaches all `n`, return that timestamp.

```python
from collections import defaultdict, deque

def earliestAcq_brute(logs, n):
    logs.sort(key=lambda log: log[0])          # earliest first
    graph = defaultdict(list)
    for t, a, b in logs:
        graph[a].append(b)
        graph[b].append(a)
        # --- after every edge, re-check full connectivity from scratch ---
        seen = {0}
        q = deque([0])
        while q:
            node = q.popleft()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        if len(seen) == n:                     # everyone reachable → done
            return t
    return -1
```

**Why it's the natural first attempt:** "is everyone connected?" *is* a graph-reachability question, and BFS from a source is the reflex answer to reachability.

**Why it's not enough:** you rebuild the reachability picture after every edge. With `m` logs each BFS costs up to `O(n + m)`, so the whole thing is `O(m · (n + m))`. Almost all of that is re-derived work — the groups you found last time are still exactly the same groups, minus one merge. You're recomputing a slowly-changing answer from zero, over and over.

**Complexity:** Time `O(m · (n + m))`, Space `O(n + m)` for the graph.

---

## ② Optimised Solution

Keep only a **count of groups** and a Disjoint Set Union structure. Sort logs by time, `union` each pair, and drop the count by one on every *real* merge. Return the timestamp of the merge that brings the count to `1`.

```python
def earliestAcq(logs, n):
    parent = list(range(n))    # each person starts as their own group's root
    rank = [0] * n             # tree height hint, for union-by-rank

    def find(x):
        # path compression (halving): shorten the chain to the root as we climb
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False               # already the same group → not a merge
        if rank[ra] < rank[rb]:        # hang the shorter tree under the taller
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True                    # a genuine merge happened

    logs.sort(key=lambda log: log[0])  # process friendships EARLIEST first
    components = n                     # everyone starts alone
    for t, a, b in logs:
        if union(a, b):
            components -= 1            # two groups became one
            if components == 1:       # single friend-circle → everyone acquainted
                return t
    return -1                         # ran out of logs, still split
```

**Walk the example** `n = 6` with the sorted logs above:

| Timestamp | union | Merge? | `components` after |
|---|---|---|---|
| 20190101 | (0,1) | ✅ real | 5 |
| 20190104 | (3,4) | ✅ real | 4 |
| 20190107 | (2,3) | ✅ real | 3 |
| 20190211 | (1,5) | ✅ real | 2 |
| 20190224 | (2,4) | ❌ same group already | 2 |
| 20190301 | (0,3) | ✅ real → **count hits 1** | 1 → **return 20190301** |

At `20190224`, persons `2` and `4` are *already* in `{2,3,4}`, so the union is a no-op and the count stays at 2 — exactly the case the brute force would waste a whole BFS discovering. At `20190301` the last two groups fuse and we're done. ✅

**A `-1` case:** `n = 4`, `logs = [[1,0,1],[2,2,3]]`. After both merges you have `{0,1}` and `{2,3}` — count stuck at 2, no log ever joins them. Loop ends, return `-1`.

**Why it's correct:** `components` is an exact invariant — it always equals the true number of connected friend-groups, because it changes by exactly `−1` on each genuine merge and never otherwise. `count == 1` is precisely the definition of "everyone acquainted" (one component = one transitively-connected circle). And because logs are processed in ascending time, the *first* log that pushes the count to 1 is the *earliest real-world moment* it could happen — any later log is too late, any earlier point still had ≥ 2 groups. Path compression + union-by-rank keep each `find`/`union` at amortised `O(α(n))` — effectively constant.

**Complexity:** Time `O(m log m)` (sort dominates) + `O(m · α(n))` for the unions ≈ `O(m log m)`. Space `O(n)`.

---

## ③ Space Optimization

**Already optimal — and here's why.** DSU needs the `parent` array to know each node's group; that's `O(n)` and it's intrinsic — the structure *is* the parent pointers. The `rank` array is another `O(n)`, but it's what keeps the trees shallow so `find` stays near-constant. You can drop `rank` (union by whichever root you find first), but then trees can grow tall and `find` degrades toward `O(n)` — you'd be trading `O(n)` space for worse time. Not worth it.

```python
# No smaller structure exists: DSU is defined by its O(n) parent array.
# 'rank' is O(n) too but buys near-constant finds — dropping it costs time, not just space.
# The sort touches the input in place; total auxiliary space stays O(n).
```

**Complexity:** Time `O(m log m)`, Space `O(n)`.

> Say it out loud: *"Space is `O(n)` for the parent array, and that's the floor — the disjoint-set structure is literally those pointers. I keep the rank array too because it's what makes finds near-constant; dropping it would save `O(n)` space but degrade my time, so it's a bad trade."* Naming *why* you're already optimal is the strong-hire move.

---

## Java (for Java interviewers)

```java
public int earliestAcq(int[][] logs, int n) {
    Arrays.sort(logs, (x, y) -> Integer.compare(x[0], y[0]));  // earliest first

    int[] parent = new int[n];
    int[] rank = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;   // each person is its own root

    int components = n;                          // everyone starts alone
    for (int[] log : logs) {
        if (union(parent, rank, log[1], log[2])) {
            if (--components == 1) return log[0];  // one circle → all acquainted
        }
    }
    return -1;
}

private int find(int[] parent, int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];   // path halving
        x = parent[x];
    }
    return x;
}

private boolean union(int[] parent, int[] rank, int a, int b) {
    int ra = find(parent, a), rb = find(parent, b);
    if (ra == rb) return false;          // already together → not a merge
    if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
    parent[rb] = ra;
    if (rank[ra] == rank[rb]) rank[ra]++;
    return true;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (BFS after every edge) | O(m · (n + m)) | O(n + m) |
| Optimised (sort + Union-Find) | O(m log m + m·α(n)) ≈ O(m log m) | O(n) |
| Space-optimised | — (none exists) | O(n) (parent array is intrinsic) |

*(m = number of logs, n = number of people, α = inverse Ackermann — effectively constant.)*

---

## Say it out loud (interview narration)

> *"Friendship is transitive, so this is really a connectivity question over time. The obvious version builds a graph and re-runs BFS after every edge to ask 'is everyone connected yet?' — correct, but it recomputes a slowly-changing answer from scratch, `O(m·(n+m))`. The insight: I don't need the whole picture, just the number of separate groups. I sort logs by timestamp so 'earliest connected' means earliest in real time, start a Union-Find with `n` groups, and every time a log merges two *different* groups I drop the count. The moment it hits 1 there's a single friend-circle — that timestamp is the answer; if the loop ends above 1, it's `-1`. With path compression and union-by-rank each operation is near-constant, so the sort dominates at `O(m log m)`, space `O(n)`."*

Before coding, ask the one clarifying question that proves you read the spec: *"Friendship is transitive, right — so I'm looking for the moment the whole group becomes a single connected component, not the moment everyone has a direct edge?"* That's the detail people gloss over, and asking it early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Number of Connected Components in an Undirected Graph (LC 323)** — the static version: same DSU, just count groups at the end.
- **Number of Provinces (LC 547)** — friend-circles again, given as an adjacency matrix.
- **Graph Valid Tree (LC 261)** — DSU where a *redundant* union (a real cycle) is the signal you're hunting.
- **Accounts Merge (LC 721)** — DSU over strings/emails; the same merge-groups engine with a mapping layer on top.
- **Redundant Connection (LC 684)** — return the edge whose union finds both endpoints already connected.
