# 🎬 Recording Script — Number of Provinces
**Pattern: Tries & Union-Find · LeetCode 547 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none for the concept — this is the gentle *introduction* to Union-Find. The reusable class built here carries into the next two problems.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a scatter of dots (cities). Lines connect some into clusters. Three distinct clusters glow in three colors.]**

> Count the friend-groups in a social network. Count the clusters of connected servers. Count the "provinces" of connected cities. It's the same question — *how many separate groups are there* — and Google asks it in a dozen disguises.
>
> You can flood-fill it with DFS, and honestly, for a static input that's fine. But this problem is the doorway to a tool every strong engineer keeps in their pocket: **Union-Find** — merge groups and check "same group?" in *near-constant* time. Once you have it, a whole family of problems becomes trivial.
>
> By the end you'll have a clean, reusable Union-Find class — the exact one you'll paste into the next two problems. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, a 3×3 matrix and three city-dots, two joined.]**

> One line: **count the connected groups of cities** — a province is a set of cities linked directly or through others.
>
> Tiny example: three cities, given as a connection matrix.

```
isConnected = 1 1 0
              1 1 0
              0 0 1
```

> Row 0 says city 0 connects to city 1. City 2 connects to nobody but itself. So: `{0,1}` is one province, `{2}` is another. Answer: **2.** Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — let them feel the mechanism)*

**[VISUAL: DFS flood fill — pick city 0, paint it and everything reachable one color; count 1. Move to an unpainted city, paint its blob; count 2.]**

> The natural first approach: flood fill. Pick an unvisited city, DFS to everything reachable, paint the whole blob as one province. Then find the next unpainted city and repeat. The number of times you *start* a new fill is your answer.
>
> **[VISUAL: fill {0,1} → count=1. Fill {2} → count=2.]**
>
> Two fills → 2 provinces. This is correct, and for our 200×200 matrix it's a perfectly good O(n²). So why reach past it?

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. New connections start *streaming in* one at a time; each time, DFS re-runs the whole fill from scratch — a "re-run" counter climbs. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's when flood fill hurts — not on a static matrix, but when connections **arrive over time.** Every new edge, you'd re-run the entire DFS to re-answer "how many groups now?" That's wasteful.
>
> **LEARNER:** So I want to *maintain* the group count as edges come in, without recomputing from scratch. But how do I know, cheaply, whether two cities are already in the same group?
>
> **TEACHER:** That's the exact question Union-Find answers. Pause and predict: **if every city started as its own tiny group, and each connection merged two groups into one, how would a running counter tell you the number of groups at any instant?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: each city as a dot pointing to itself (its own root). An edge merges two: one dot's arrow re-points to the other's root. Sets drawn as little trees.]**

> Here's the aha, and the analogy is *company org charts*. Every city starts as its own one-person company, its own boss — its own **root**. A connection says "merge these two companies." To merge, you make one company's boss report to the other's boss. Now they share a top boss — same group.
>
> Two operations:
> - **`find(x)`** — climb from `x` up to the root boss that *names* its group.
> - **`union(a, b)`** — find both roots; if different, point one root at the other. Two groups become one, so *decrement a running count.*
>
> **[VISUAL: start count=3 for {0},{1},{2}. union(0,1) → point 1's root at 0 → count drops to 2. That's it.]**
>
> Start with `count = number of cities`. Every real merge drops it by one. At the end, `count` *is* the number of provinces. No re-scanning — the count is always live.

---

## 5b. KEEPING IT FAST — PATH COMPRESSION + UNION BY RANK — `4:30`
*(the depth that makes Union-Find "near O(1)")*

**[VISUAL: a tall skinny tree (bad) flattening as `find` re-points nodes straight at the root. Beside it, union-by-rank hanging a short tree under a taller one.]**

> Now the part that makes Union-Find *fast*. Naively, those trees can grow tall and skinny, and `find` crawls up slowly. Two tricks fix it:
>
> - **Path compression:** while `find` climbs to the root, it re-points nodes *straight at the root* along the way. The tree flattens itself every time you query it.
> - **Union by rank:** always hang the *shorter* tree under the taller one, so trees stay bushy, not stringy.
>
> Together they make every `find` and `union` effectively **O(α(n))** — inverse Ackermann, which is basically a constant — under 5 for any input you'll ever see. That's the "near O(1)" you'll say out loud.

---

## 6. THE KEY MOVE (signaling) — `5:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Union-Find: merge sets, find roots. Count of distinct roots = number of groups. Near O(1) with path compression + union by rank."]**

> The key move: **merge sets, find roots; the number of distinct roots is the number of groups — and with path compression plus union by rank, it's near constant per operation.**
>
> Trigger phrase: *"count connected components / are these two in the same group / merge groups"* → Union-Find.

---

## 7. CODE IT — LIVE & CHUNKED — `6:00`
*(cognitive load — build in pieces)*
*(This is THE reusable class — build it carefully; it returns in the next two problems.)*

**[VISUAL: empty editor. Type chunk 1 — the constructor.]**

> Here's the clean, reusable class. First, the setup: each node is its own root, ranks start at 0, and `count` is the number of sets.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))    # each node is its own root
        self.rank = [0] * n             # tree-height upper bound per root
        self.count = n                  # number of disjoint sets
```

> **[VISUAL: add chunk 2 — find with path compression.]** `find` climbs to the root and flattens as it goes.

```python
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x
```

> **[VISUAL: add chunk 3 — union by rank.]** `union` joins two roots, shorter under taller, and drops the count.

```python
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                # already same set
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra             # ra is the taller root
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1                 # two sets became one
        return True
```

> **[VISUAL: add chunk 4 — the driver.]** Now the problem itself: union every connected pair, return the count.

```python
def findCircleNum(isConnected):
    n = len(isConnected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):       # upper triangle — matrix is symmetric
            if isConnected[i][j] == 1:
                uf.union(i, j)
    return uf.count
```

---

## 8. EXPLAIN THE CODE (the WHY) — `8:15`
*(elaboration — why each line exists)*

**[VISUAL: full class; spotlight lines.]**

> Why each piece.
>
> `parent = list(range(n))` — everyone's their own boss initially, so `count = n` groups.
>
> In `find`, `self.parent[x] = self.parent[self.parent[x]]` — that's *path halving*, a compact path compression: each step points `x` at its grandparent, flattening the tree as we climb.
>
> **LEARNER:** In `union`, why the `if ra == rb: return False` guard? What breaks without it?
>
> **TEACHER:** Everything, subtly. If both endpoints are *already* in the same set and you skip that check, you'd decrement `count` anyway — over-counting merges and reporting too few groups. The guard says "these were already together, no merge happened, don't touch the count." It's the line that keeps `count` truthful.
>
> `if rank[ra] == rank[rb]: rank[ra] += 1` — the only time a tree gets taller is when you stack two equal-height trees. That's how rank stays an honest height bound.
>
> And the driver's `range(i+1, n)` — the matrix is symmetric, so we only scan the upper triangle. No need to process both `(i,j)` and `(j,i)`.

---

## 9. DRY-RUN THE CODE — `9:30`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3 cities, sets merging, count ticking down.]**

> Run it on the matrix. Start `count = 3`: sets `{0}, {1}, {2}`.

| pair | connected? | union result | count |
|---|---|---|---|
| (0,1) | 1 | merge {0},{1} | 3 → 2 |
| (0,2) | 0 | skip | 2 |
| (1,2) | 0 | skip | 2 |

> Final `count = 2`. Roots: `{0,1}` share one, `{2}` alone. Exactly the two provinces. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:15`
*(transfer to interview)*

**[VISUAL: rows — DFS: O(n²). Union-Find: O(n² · α(n)) ≈ O(n²).]**

> Say it: *"DFS flood fill is O(n²) — we visit each matrix cell. Union-Find is O(n² times alpha of n), and alpha is inverse Ackermann, effectively constant, so it's also O(n²) here. Space is O(n) for the parent and rank arrays."*
>
> Then the money line: *"Both are O(n²) on a static matrix — but I chose Union-Find because it generalizes: when edges arrive over time, it answers merges and 'same group?' in near-constant time without re-running DFS."* That's *why* you'd pick it.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:00`
*(depth + honesty)*

**[VISUAL: the two arrays parent + rank; a note "O(n) — can't go lower, must remember each node's set".]**

> Space is O(n) — the `parent` and `rank` arrays. You *can't* go below O(n): you must remember which set each of the `n` nodes belongs to.
>
> One honest lever: drop `rank` and use **union by size** (still one array) — or skip balancing entirely; path compression *alone* still gives O(log n) amortized. But `rank` is only O(n) and buys the near-constant guarantee, so keeping both heuristics is the textbook choice. Say it: *"Already optimal at O(n); the only trade is rank vs size vs nothing, a constant-factor call."*

---

## 12. YOUR TURN (active recall) — `11:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Connected Components (LC 323)". An edge list instead of a matrix.]**

> Before the next video, try **Number of Connected Components in an Undirected Graph**, LC 323. Same exact problem — but you're given an *edge list* instead of a matrix. Reuse today's `UnionFind` class verbatim; just loop the edges. It should feel like cheating.
>
> Ten minutes first.

---

## 13. LOCK IT IN — `12:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Each node starts its own set; every edge unions two; count drops per real merge.**
> 2. **`find` + path compression, `union` + union by rank** → near O(1).
> 3. **The `ra == rb` guard** keeps the count honest — no double-counting.
>
> Memory peg: **merge sets, count the roots — that's your number of groups.**

---

## 14. CLIFFHANGER — `12:35`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Redundant Connection" — a graph with one edge closing a loop, glowing red.]**

> Here, unions never conflicted — every edge merged two separate groups. But what if you're adding edges and one of them connects two cities that were *already* in the same group? That edge just created a **cycle**. Detecting that exact edge is its own classic problem — and Union-Find spots it in one line. Next up: Redundant Connection. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
