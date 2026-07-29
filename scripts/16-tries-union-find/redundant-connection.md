# 🎬 Recording Script — Redundant Connection
**Pattern: Tries & Union-Find · LeetCode 684 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Number of Provinces — same reusable `UnionFind` class. Here we use the `find(u) == find(v)` signal instead of the count.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: nodes being wired into a clean tree, one edge at a time. Then one extra wire snaps across and closes a loop — the cycle flashes red.]**

> You've got what *should* be a tree — nodes wired together with no loops. But someone added exactly **one extra wire**, and now there's a cycle. Your job: find the one edge to cut to make it a tree again. If several would work, return the one added **last**.
>
> The brute-force instinct — "remove each edge and check if the rest still connects" — is O(n²) and fiddly. But there's a one-line signal hiding here, and you already have the tool for it from last video.
>
> By the end you'll spot the redundant edge in a single linear pass with Union-Find. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, three nodes 1,2,3 and edges appearing: [1,2], [1,3], then [2,3] closing a triangle.]**

> One line: **a tree had one extra edge added, making exactly one cycle — return the edge to remove, preferring the last one in the input.**
>
> Tiny example: `edges = [[1,2], [1,3], [2,3]]`. Edges 1–2 and 1–3 already tie nodes 1, 2, 3 into a tree. Then 2–3 arrives — but 2 and 3 are *already* connected through node 1. So 2–3 closes the triangle. Answer: **`[2,3]`.** Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: for each edge from the end, remove it, rebuild the graph, run a DFS to test connectivity. Multiple full rebuilds; a "graph rebuilds" counter climbs.]**

> Brute force: for each edge — starting from the last — temporarily remove it, rebuild the graph from the others, and DFS to check if its two endpoints are *still* connected. If they are, that edge was redundant.
>
> **[VISUAL: remove [2,3], rebuild, DFS from 2 to 3 → still connected via 1 → [2,3] is redundant.]**
>
> It works, but look at the cost: you rebuild the whole graph and run a fresh DFS *per candidate edge*. That's O(n²), and you re-derive connectivity from scratch every single time.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight that connectivity is rebuilt from zero each time. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste: we throw away everything we knew about connectivity and recompute it for each edge.
>
> **LEARNER:** So instead of removing edges and re-checking, I should *add* them one by one and watch connectivity build up. But how does adding an edge tell me it's the redundant one?
>
> **TEACHER:** You're one inch away. Pause and predict: **as I add edges in order and merge groups, what's special about an edge whose two endpoints are ALREADY in the same group?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: Union-Find sets drawn as trees. Edges added one at a time: [1,2] merges, [1,3] merges — all one set. Then [2,3]: find(2) and find(3) both point to the same root → the edge glows red.]**

> Here's the aha: **add edges in order and maintain connectivity with Union-Find.** For each edge `(u, v)`:
>
> - If `u` and `v` are in **different** sets → this edge genuinely connects two pieces → `union` them.
> - If `u` and `v` are **already in the same set** → there's *already a path* between them → adding a direct edge creates a **second path** → that's a cycle. **This is the redundant edge.**
>
> **[VISUAL: [1,2] → union. [1,3] → union, now {1,2,3}. [2,3] → find(2)=find(3)=root 1 → SAME → return [2,3].]**
>
> And why is the *first* such edge the answer the problem wants? Because in a tree-plus-one-edge graph there's exactly one cycle, and the single edge that closes it — the last one of that cycle to be added in input order — is precisely the "return the last one" the problem asks for. Processing in order hands it to us for free.

---

## 5b. WHY "ALREADY CONNECTED" MEANS "CYCLE" — `4:00`
*(nailing the core logical step)*

**[VISUAL: two nodes with an existing path drawn between them (dotted), then a new direct edge added — the dotted path + new edge form a loop.]**

> Let me make the core step airtight, because it's the whole problem. If `find(u) == find(v)` *before* we add edge `(u,v)`, that means earlier edges already built a path from `u` to `v`. Now the new direct edge `u–v` is a *second, independent* route between them. Two distinct paths between the same pair of nodes — that is, by definition, a cycle. So "already in the same set" and "this edge closes a cycle" are the exact same statement. One `find` comparison detects it.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Process edges in order. First edge where find(u) == find(v) is the redundant one."]**

> The key move: **process edges in order; the first edge whose endpoints already share a root is the cycle-closer — return it.**
>
> Trigger phrase: *"detect the edge that closes a cycle / when does adding an edge break the tree property"* → Union-Find, checking `find(u) == find(v)` before each union.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*
*(Same reusable class — this time we only need find + union, no count.)*

**[VISUAL: empty editor. Type chunk 1 — the trimmed class.]**

> Same Union-Find as last time — we don't even need the `count` here, just `find` and `union`.

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
```

> **[VISUAL: add chunk 2 — union returns a boolean signal.]** The trick: `union` returns `False` when the two were *already* connected — that boolean *is* our cycle detector.

```python
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                # already connected → cycle!
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True
```

> **[VISUAL: add chunk 3 — the driver, four lines.]** Walk the edges; the first `union` that returns `False` is the answer.

```python
def findRedundantConnection(edges):
    uf = UnionFind(len(edges) + 1)      # nodes are 1..n; index 0 unused
    for u, v in edges:
        if not uf.union(u, v):          # False → they were already connected
            return [u, v]
    return []
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: full code; spotlight lines.]**

> Why each piece.
>
> `UnionFind(len(edges) + 1)` — the nodes are labeled 1 through n, so we size the arrays to `n+1` and just ignore index 0. Cleaner than subtracting 1 everywhere.
>
> `if not uf.union(u, v): return [u, v]` — `union` returns `True` on a real merge, `False` when the endpoints already shared a root. That `False` means "this edge would create a cycle," so it's exactly the redundant edge. We return immediately.
>
> **LEARNER:** Why return the *first* `False` and not keep scanning for a later one? The problem says return the *last* edge in the input.
>
> **TEACHER:** Beautiful trap, and here's why the first `False` *is* the last-in-input answer. There's only one cycle. As we process edges in order, every edge of that cycle merges fine — until the one that *closes* it, which is the last of the cycle's edges to appear in the input. That closing edge is the first — and only — one where `union` fails. First failure and "last edge of the cycle in input order" are the same edge. So we're done the moment it fails.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: three nodes, sets merging, then the red flash on [2,3].]**

> Run it on `[[1,2],[1,3],[2,3]]`. Every node starts its own set.

| edge | find(u) vs find(v) | union? | sets after |
|---|---|---|---|
| (1,2) | 1 ≠ 2 | merge | {1,2}, {3} |
| (1,3) | find(1)=1 ≠ 3 | merge | {1,2,3} |
| (2,3) | find(2)=1, find(3)=1 → **equal** | **False** → return **[2,3]** ✅ |

> The moment 2 and 3 were found to already share root 1, we returned `[2,3]`. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:35`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(n²). Union-Find: O(n · α(n)) ≈ O(n).]**

> Say it: *"The remove-and-DFS brute force is O(n²) — a graph rebuild and traversal per edge. Union-Find is a single pass: each edge does one `find`/`union` at O(alpha of n), effectively constant, so O(n) total. Space is O(n) for the parent and rank arrays."*
>
> Headline: *"One linear pass, no graph rebuilding — the first edge whose endpoints already connect is the cycle."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:05`
*(depth + honesty)*

**[VISUAL: parent + rank arrays; note "O(n), inherent".]**

> Space is O(n) — the `parent` (and `rank`) arrays, and you can't beat it since you must remember every node's set.
>
> Same lever as before: you could drop `rank` and rely on path compression alone — O(log n) amortized instead of O(α(n)) — to use one array. But `rank` is only O(n) and buys the near-constant guarantee. Say it: *"Already optimal at O(n) time and space, a single pass with no rebuild."*

---

## 12. YOUR TURN (active recall) — `9:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Graph Valid Tree (LC 261)". A graph being checked for tree-ness.]**

> Before the next video, try **Graph Valid Tree**, LC 261. A graph is a valid tree if it has exactly `n−1` edges *and* no cycle *and* one component. Use Union-Find: if any edge ever fails to union, there's a cycle → not a tree. Same signal, flipped use.
>
> Ten minutes first.

---

## 13. LOCK IT IN — `10:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Add edges in order, union each** — build connectivity incrementally.
> 2. **`find(u) == find(v)` before union means a cycle** — that edge is redundant.
> 3. **First failure = last cycle edge in input** — exactly what's asked.
>
> Memory peg: **the edge that connects two nodes already connected is the one that closes the loop.**

---

## 14. CLIFFHANGER — `10:35`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Accounts Merge" — email addresses clustering by person.]**

> So far the "nodes" were plain integers. But Union-Find really sings when the things you're merging are messier — like emails scattered across duplicate user accounts, where two accounts are the same person if they share *any* email. The clever move? Make the *emails* the nodes. Next up, the capstone of this chapter: Accounts Merge. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
