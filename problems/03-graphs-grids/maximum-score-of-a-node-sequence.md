# Maximum Score of a Node Sequence

> **LeetCode:** 2242. Maximum Score of a Node Sequence · **Difficulty:** 🔴 Hard · **Pattern:** Graph + top-K neighbors pruning · **Google frequency:** ⭐ high

---

## Problem

You're given an undirected graph. Each node `i` has a value `scores[i]`, and a list of `edges`. A **valid node sequence** is **four distinct nodes** `a — b — c — d` connected in a chain: `a-b`, `b-c`, and `c-d` must all be edges. Its score is `scores[a] + scores[b] + scores[c] + scores[d]`. Return the **maximum** score over all valid sequences, or **-1** if no valid sequence exists.

**Example:** `scores = [5,2,9,8,4]`, `edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]` → `24`
*(the chain `0 → 1 → 2 → 3` uses edges 0-1, 1-2, 2-3, four distinct nodes, and scores `5+2+9+8 = 24` — the best you can do here.)*

**Constraints that matter:** `n` up to `5·10⁴` nodes and up to `5·10⁴` edges. A node's degree can be huge — a single hub connected to tens of thousands of others (a "star"). That kills anything shaped like `O(V⁴)` (all four-tuples) **and** anything shaped like `O(E · deg²)` (fix an edge, then scan *all* neighbors on both ends). The whole game is realizing you never need more than a handful of the best neighbors.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "It's four nodes with three edges between them. Try every group of four distinct nodes, check the three edges exist, keep the biggest sum." That's `O(V⁴)` — dead on arrival at `V = 5·10⁴`. But hold onto the shape: a chain has a **middle**.
- **Where it hurts:** the four-tuple search treats all four positions as independent and re-discovers the same adjacency over and over. The real structure is `a-b-c-d`: two *endpoints* (`a`, `d`) hanging off a *middle edge* `(b, c)`. So the smarter move is: **iterate every edge and treat it as the middle**, then pick the best `a` from `b`'s neighbors and the best `d` from `c`'s neighbors. That's `O(E · deg²)` — still explosive, because a hub node has `deg` in the tens of thousands and you'd scan all of them.
- **The leap:** you don't need *all* of `b`'s neighbors as candidates for `a`. To maximize the sum you want the **highest-scoring** neighbor — and the only reason the highest one can fail is a **distinctness collision**: `a` must differ from `c` and from `d`. That's at most **two** blocked candidates. So the **top-3** highest-scoring neighbors of `b` always contain a legal choice for `a`. Same for `d` on node `c`. Precompute top-3 per node once; then each middle edge costs only `3 × 3 = 9` checks.
- **Pattern trigger:** **"pick the best few endpoints hanging off a fixed core, with a small distinctness constraint"** → **top-K neighbor pruning**. The transferable move: when only a *bounded number* of candidates can ever be excluded, you only need to keep `K = (excluded + 1)` best options — the rest can never be the answer.

---

## ① Brute Force

Try every ordered group of four distinct nodes; check all three edges exist via an edge set; keep the max sum.

```python
def maximumScore_brute(scores, edges):
    n = len(scores)
    edge_set = set()
    for u, v in edges:
        edge_set.add((u, v))
        edge_set.add((v, u))   # undirected: store both directions

    best = -1
    for a in range(n):
        for b in range(n):
            if b == a or (a, b) not in edge_set:
                continue
            for c in range(n):
                if c in (a, b) or (b, c) not in edge_set:
                    continue
                for d in range(n):
                    if d in (a, b, c) or (c, d) not in edge_set:
                        continue
                    best = max(best, scores[a] + scores[b] + scores[c] + scores[d])
    return best
```

**Why it's the natural first attempt:** the problem literally describes four nodes in a chain, so enumerating four nodes and verifying the chain is the most direct translation of the spec.

**Why it's not enough:** it's `O(V⁴)` in the worst case. At `V = 5·10⁴` that's `~6·10¹⁸` — you won't finish before the heat death of the interview. Even pruning with the edge set doesn't save the asymptotics on a dense graph. We're throwing away the one piece of structure that matters: the chain has a **middle edge**, and the endpoints only need to be the *best* neighbors, not *all* of them.

**Complexity:** Time `O(V⁴)`, Space `O(E)` for the edge set.

---

## ② Optimised Solution

**Fix the middle edge, keep only the top-3 neighbors per node.** For every edge `(b, c)`, the endpoint `a` is a neighbor of `b` and `d` is a neighbor of `c`; to maximize the sum, `a` and `d` only ever need to come from each node's three highest-scoring neighbors.

```python
def maximumScore(scores, edges):
    n = len(scores)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # For each node, keep only its 3 highest-scoring neighbors.
    # (Why 3? a candidate can be blocked by at most 2 other nodes in the
    #  sequence, so the 3rd-best is always still a legal fallback.)
    top = [sorted(nbrs, key=lambda x: scores[x], reverse=True)[:3]
           for nbrs in adj]

    best = -1
    for b, c in edges:                 # every edge, treated as the MIDDLE b-c
        for a in top[b]:               # endpoint off b
            if a == c:                 # a must differ from c
                continue
            for d in top[c]:           # endpoint off c
                if d == b or d == a:   # d must differ from b and from a
                    continue
                best = max(best, scores[a] + scores[b] + scores[c] + scores[d])
    return best
```

**Walk one example** — `scores = [5,2,9,8,4]`, `edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]`.

First, adjacency and the top-3 (by score) per node:

| Node | score | neighbors (score) | top-3 neighbors |
|---|---|---|---|
| 0 | 5 | 1(2), 2(9) | `[2, 1]` |
| 1 | 2 | 0(5), 2(9), 3(8) | `[2, 3, 0]` |
| 2 | 9 | 1(2), 3(8), 0(5), 4(4) | `[3, 0, 4]` |
| 3 | 8 | 2(9), 1(2) | `[2, 1]` |
| 4 | 4 | 2(9) | `[2]` |

Now iterate edges as the middle. The winning one is edge `(2, 3)` — `b=2 (score 9)`, `c=3 (score 8)`:

| middle `(b,c)` | pick `a` from `top[b]` (≠ c, d) | pick `d` from `top[c]` (≠ b, a) | sum |
|---|---|---|---|
| `(2,3)` | `a=0` (top[2] is `[3,0,4]`; skip 3 = c) | `d=1` (top[3] is `[2,1]`; skip 2 = b) | `5+9+8+2 = 24` |
| `(1,2)` | `a=3` (top[1] `[2,3,0]`; skip 2 = c) | `d=0` (top[2] `[3,0,4]`; skip 3 = a) | `8+2+9+5 = 24` |
| `(2,4)` | — | `top[4] = [2]`, only 2 = b → no legal `d` | — |

Every branch that produces a full chain tops out at **24**, and `0 → 1 → 2 → 3` is one realizing chain. ✅

**Why it's correct:** the only optimization is *pruning* the candidate lists, so we must prove pruning never drops the answer. Fix any middle edge `(b, c)`. For the endpoint `a`, we want the neighbor of `b` with the largest score, subject to `a ∉ {c, d}` (it's automatically `≠ b` since it's a neighbor). At most **two** nodes — `c` and `d` — can be forbidden. So among `b`'s **three** highest-scoring neighbors, at least one survives, and it's the best legal choice. Keeping fewer than 3 could drop the true best; keeping more than 3 is never needed. The identical argument holds for `d` off node `c` (blocked by `b` and `a`). Iterating each edge once as the middle covers every chain, because a chain is exactly *a middle edge plus one endpoint on each side*, and the sum is symmetric so orientation doesn't matter.

**Complexity:** Time `O(V + E·log(deg))` to build the top-3 lists (a sort per node, but you can use a bounded selection), plus `O(E · 9)` for the main loop → `O(E log deg)` overall. Space `O(V + E)` for the adjacency and the (constant-per-node) top lists.

---

## ③ Space Optimization

**Already at the floor for the working memory, and here's the honest why.** You must store the graph somehow to know who's adjacent to whom — that's `O(V + E)`, unavoidable input structure. Beyond that, the extra memory is tiny: the `top` lists hold **at most 3 entries per node**, so they're `O(V)`, i.e. `O(1)` *per node*. There's no rolling-window trick to shave it, because "who are my best neighbors" is a per-node fact you genuinely have to keep for every node.

If you want to trim the constant, build each node's top-3 with a **fixed-size selection** (compare-and-keep-3) instead of sorting the whole neighbor list — that drops the per-node build from `O(deg log deg)` to `O(deg)` and keeps the same `O(V)` space:

```python
# top-3 without a full sort: one pass, keep the 3 best by score
top = [[] for _ in range(n)]
for u in range(n):
    for v in adj[u]:
        top[u].append(v)
        top[u].sort(key=lambda x: scores[x], reverse=True)
        del top[u][3:]          # never hold more than 3
```

**Complexity:** Time `O(V + E)` to build, `O(E)` for the scan; Space `O(V + E)` (graph-bound; `O(V)` auxiliary beyond the graph).

> Say it out loud: *"Space is O(V + E), but that's the graph I'm handed, not overhead — my extra memory is three neighbors per node, which is O(V). There's no smaller representation because adjacency is the input."* Naming the floor is as strong as finding a trick.

---

## Java (for Java interviewers)

```java
public int maximumScore(int[] scores, int[][] edges) {
    int n = scores.length;
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) {
        adj.get(e[0]).add(e[1]);
        adj.get(e[1]).add(e[0]);
    }

    // For each node, keep only its 3 highest-scoring neighbors.
    // A candidate can be blocked by at most 2 other nodes, so top-3 always
    // leaves a legal fallback.
    int[][] top = new int[n][];
    for (int u = 0; u < n; u++) {
        List<Integer> nbrs = adj.get(u);
        nbrs.sort((x, y) -> scores[y] - scores[x]);   // descending by score
        int k = Math.min(3, nbrs.size());
        top[u] = new int[k];
        for (int i = 0; i < k; i++) top[u][i] = nbrs.get(i);
    }

    int best = -1;
    for (int[] e : edges) {                 // every edge as the middle b-c
        int b = e[0], c = e[1];
        for (int a : top[b]) {
            if (a == c) continue;           // a must differ from c
            for (int d : top[c]) {
                if (d == b || d == a) continue;   // d differs from b and a
                best = Math.max(best,
                        scores[a] + scores[b] + scores[c] + scores[d]);
            }
        }
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all four-tuples) | O(V⁴) | O(E) |
| Fix middle edge, all neighbors | O(E · deg²) | O(V + E) |
| Optimised (middle edge + top-3) | O(E log deg) | O(V + E) |

*(V = nodes, E = edges, deg = max degree. Top-3 turns the `deg²` endpoint scan into a constant 9.)*

---

## Say it out loud (interview narration)

> *"A valid sequence is a chain `a-b-c-d`, so instead of enumerating four nodes — that's O(V⁴) — I'll fix the middle edge `(b, c)` and iterate every edge as the middle. Then `a` is a neighbor of `b` and `d` is a neighbor of `c`. To maximize, `a` should be `b`'s highest-scoring neighbor — but it might collide with `c` or `d`, so I keep the top-3 neighbors per node: a candidate can be blocked by at most two other nodes, so the third-best is always a safe fallback. Precompute top-3 once, then each edge costs nine checks. That's O(E log deg) time, O(V + E) space — the space is the graph itself, not overhead."*

Before coding, ask the one clarifying question that shows you read the spec: *"The four nodes have to be distinct, right? So `a` can't equal `d` even if both are neighbors of the middle?"* That distinctness detail is exactly why top-1 isn't enough and top-3 is — surfacing it early is what Google's GCA rubric rewards.

## Related / follow-ups
- **Maximum Star Sum of a Graph (LC 2497)** — same "keep only the top-K neighbors by value" pruning, applied to a star instead of a chain.
- **Largest Color Value in a Directed Graph (LC 2246)** — path-value optimization over graph structure.
- **Number of Ways to Arrive at Destination / shortest-path counting** — more "fix a structural core, then extend" reasoning on graphs.
- **Get the Maximum Score (LC 1537)** — combine best sub-choices across a constrained structure to maximize a sum.
