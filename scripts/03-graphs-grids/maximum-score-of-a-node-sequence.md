# 🎬 Recording Script — Maximum Score of a Node Sequence
**Pattern: Graph + top-K neighbors pruning · LeetCode 2242 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** basic adjacency lists (Number of Islands / Course Schedule) — but here we prune the neighbors, not walk them all.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. Four clean nested `for` loops over nodes are typed out. A LeetCode "Time Limit Exceeded — 61 / 78" banner slams in red.]**

> The interviewer draws a graph. Nodes have values. She says: *"Find four nodes in a chain — `a` connects to `b`, `b` to `c`, `c` to `d` — that maximize the total value. Go."*
>
> You write the obvious thing: four loops, one per node, check the edges, keep the best sum. It's *correct*. It passes the small tests. You hit run on the big one and… Time Limit Exceeded.
>
> Here's the twist: you're enumerating four things when you only ever needed to enumerate **one** — plus the three best neighbors on each side. By the end of this video you'll know exactly why **top-3** is the magic number, and why top-1 quietly fails. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a tiny graph — 5 circles with values inside, edges drawn:]**

```
scores = [5, 2, 9, 8, 4]
edges  = 0-1, 1-2, 2-3, 0-2, 1-3, 2-4

        (0:5)───(1:2)
          │  ╲   │ ╲
          │   ╲  │  ╲
        (2:9)───┘  (3:8)
          │
        (4:4)
```

> The whole problem in one line: **find four distinct nodes in a chain `a-b-c-d` — every consecutive pair is an edge — that maximizes the sum of their values.** If no such chain exists, return `-1`.
>
> Here's our tiny graph — five nodes. The values are inside the circles: node 2 is the juicy one at 9, node 3 is 8.
>
> There's a chain worth **24** hiding in here. Don't hunt for it yet — just hold that the answer is 24.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the graph. A "tuples checked" counter, top-right, starting at 0. Arrows try random four-node groups; most flash red "not a chain".]**

> Let's do what your brain does first: pick every possible group of four distinct nodes, check whether they form a chain, and if so, add up their values.
>
> Try `0, 1, 2, 3`. Is `0-1` an edge? Yes. `1-2`? Yes. `2-3`? Yes. Valid chain. Sum is `5+2+9+8 = 24`. Counter ticks.
>
> **[VISUAL: chain 0→1→2→3 lights green; counter climbs.]**
>
> Try `0, 4, 1, 3`. Is `0-4` an edge? No. Dead. Try `4, 3, 1, 0`. `4-3`? No. Dead. Try `3, 0, 4, 1`… dead again.
>
> **[VISUAL: a storm of red "not a chain" flashes; the counter spins fast.]**
>
> Most groups aren't even chains — but we pay to check every single one. Four nested loops over `n` nodes is `n⁴`.
>
> **[VISUAL: counter morphs into "V⁴ ≈ 6·10¹⁸" with a scary red glow.]**
>
> At fifty thousand nodes, `n⁴` is six *quintillion*. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The valid chain `a-b-c-d` is spotlighted. The middle edge `b-c` pulses. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? We're treating all four nodes as independent. But look at the *shape* of a valid answer — it's a chain, and a chain has a **middle**. The pair `b-c` in the middle is just… an edge. And we already have a list of every edge.
>
> **LEARNER:** Wait — so instead of choosing four nodes, I loop over edges and call each one the middle? But then I still have to pick `a` on one side and `d` on the other. Isn't that back to scanning everybody?
>
> **TEACHER:** That's the exact right question, and it's the whole lesson. Pause the video. If you fix the middle edge `b-c`, and you want the biggest sum — **which neighbors of `b` should you even consider for `a`?** Think about it before I answer.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: fix the middle edge as `2-3`. Node 2's neighbors fan out with their scores: 3(8), 0(5), 4(4), 1(2). An arrow points to the biggest.]**

> **TEACHER:** Here's the move. Fix the middle edge `b-c`. Now `a` is just a neighbor of `b`, and `d` is just a neighbor of `c`. To maximize the sum, you obviously want `a` to be `b`'s **highest-scoring** neighbor. Grab the best one. Done, right?
>
> **LEARNER:** Feels too easy. What if `b`'s best neighbor *is* `c`? Then it's already in the chain — I can't reuse it.
>
> **TEACHER:** Exactly the trap. The four nodes must be **distinct**. So `a`'s best neighbor might collide with `c`. Skip it, take the second-best. But — what if the second-best is `d`, the node we picked on the other side? Collision again. Skip it, take the **third**.
>
> **[VISUAL: node 2's neighbor list. Cross out 3 (it's c). Cross out the next if it's d. The third one glows "always safe".]**
>
> How many nodes can ever block `a`? Just two — `c` and `d`. Two blockers means: among the **top-3** highest-scoring neighbors of `b`, at least one is always legal. So you never need the 4th-best, the 5th-best, the ten-thousandth. **Just keep the top-3 per node.**
>
> Think of it like packing a carry-on with your three favorite jackets. Even if airport security makes you ditch two, you've still got one you love. Four jackets would be wasted space — two is the most you'll ever lose.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "fix the middle edge · keep top-3 neighbors per node · 9 checks each."]**

> Burn this one line in: **fix the middle edge, and each endpoint only needs the top-3 neighbors — because at most two others can block it.**
>
> That's the whole trick. Precompute top-3 once, then every edge costs a tiny `3 × 3 = 9` checks. Any problem where only a *bounded* number of candidates can be excluded — this is your reflex: **keep top-K, where K is blockers-plus-one.**

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in pieces. First, the adjacency list — who's connected to whom.

```python
def maximumScore(scores, edges):
    n = len(scores)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)         # undirected — both directions
```

> **[VISUAL: add chunk 2, highlight it.]** Now the one clever line: for each node, keep only its 3 highest-scoring neighbors.

```python
    top = [sorted(nbrs, key=lambda x: scores[x], reverse=True)[:3]
           for nbrs in adj]
```

> **[VISUAL: add chunk 3.]** Now loop every edge as the middle `b-c`, and try the top-3 on each side — skipping any collision.

```python
    best = -1
    for b, c in edges:
        for a in top[b]:
            if a == c:                    # a must differ from c
                continue
            for d in top[c]:
                if d == b or d == a:      # d differs from b and from a
                    continue
                best = max(best,
                           scores[a] + scores[b] + scores[c] + scores[d])
```

> **[VISUAL: add chunk 4, highlight the `return`.]** If we never found a full legal chain, `best` is still `-1`. Return it.

```python
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `sorted(...)[:3]` — this one slice is the difference between `deg²` and constant. It throws away every neighbor past the third-best. That's safe *only* because at most two nodes can block an endpoint.
>
> **LEARNER:** Hold on — why exactly **3**? Why not top-2, or top-1 with a fallback? Convince me the third one is really needed.
>
> **TEACHER:** Picture the worst case for `a`. Its single best neighbor happens to be `c` — blocked, it's in the chain already. Its second-best happens to be `d` — also blocked, that's the other endpoint. Two independent nodes, two hits. The **third**-best is the first one nobody else has claimed. Drop to top-2 and both your candidates could be `c` and `d`, leaving you with nothing — you'd miss a valid chain and return a wrong answer. Top-3 is the tight bound: blockers plus one.
>
> `if a == c` and `if d == b or d == a` — these are the distinctness guards. Four *distinct* nodes is in the spec; without these you'd count a chain that reuses a node.
>
> `for b, c in edges` — we iterate each edge **once** as the middle. We don't need the reverse `c, b`, because trying `a` off `b` and `d` off `c` already covers both extensions, and the sum is symmetric — flipping the chain gives the same total.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the graph, with each node showing its computed top-3 list. Then a trace table filling row by row.]**

> Let's run the actual code. First the top-3 lists — highest score first:

```
node 0 (5): neighbors 1(2), 2(9)          → top-3 [2, 1]
node 1 (2): neighbors 0(5), 2(9), 3(8)    → top-3 [2, 3, 0]
node 2 (9): neighbors 1(2),3(8),0(5),4(4) → top-3 [3, 0, 4]
node 3 (8): neighbors 2(9), 1(2)          → top-3 [2, 1]
node 4 (4): neighbor  2(9)                → top-3 [2]
```

> Now iterate edges as the middle. Watch the winner, edge `2-3`:

| middle `b-c` | pick `a` from `top[b]` | pick `d` from `top[c]` | sum |
|---|---|---|---|
| `2-3` | `top[2]=[3,0,4]`; skip 3 (=c) → **a=0** | `top[3]=[2,1]`; skip 2 (=b) → **d=1** | `5+9+8+2 = 24` |
| `1-2` | `top[1]=[2,3,0]`; skip 2 (=c) → **a=3** | `top[2]=[3,0,4]`; skip 3 (=a) → **d=0** | `8+2+9+5 = 24` |
| `2-4` | `top[2]=[3,0,4]` → a=3 | `top[4]=[2]`; only 2 (=b) → **no legal d** | skip |

> Notice edge `2-4`: node 4's *only* neighbor is 2, which is the middle itself — no valid `d`, so that branch just skips. And the max lands at **24** — the chain `0 → 1 → 2 → 3`, exactly the answer we promised at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: three rows — Brute: O(V⁴). Middle-edge, all neighbors: O(E·deg²). Ours: O(E log deg). A note: "top-3 → 9 checks per edge".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force enumerates four nodes — O(V⁴), hopeless. Fixing the middle edge but scanning all neighbors is O(E · deg²), and a hub node makes deg huge, so still too slow. Keeping only the top-3 neighbors makes each edge a constant nine checks — so the main loop is O(E), and building the top-3 lists is O(E log deg) with the sort. Space is O(V + E) for the graph."*
>
> That's the sentence that flips a Hard from "I hope" to "I've got this."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the adjacency list; a "shrink it?" thought bubble, then a red ✗ over the graph and a green ✓ over the top-3 lists.]**

> Quick but important — and honesty scores points.
>
> Can we shrink the space? **The graph itself is O(V + E) — that's the input, not overhead; I can't represent adjacency in less.** My *extra* memory is just the top-3 lists: three neighbors per node, so O(V). There's no rolling-window trick, because "who are my best neighbors" is a genuine per-node fact.
>
> One real refinement: instead of `sorted(...)[:3]`, build each top-3 with a single compare-and-keep-3 pass — that drops the build from O(deg log deg) per node to O(deg), same O(V) space.
>
> Say it out loud in the interview: *"Space is O(V + E), graph-bound; my auxiliary is three neighbors per node, O(V), and there's no smaller form because adjacency is the input."* Naming *why* it can't shrink is a stronger signal than silence.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Maximum Star Sum of a Graph (LC 2497)". A blank editor.]**

> Before the next video, try **Maximum Star Sum of a Graph**. Same weapon: you pick a center node and its `k` best neighbors to maximize a sum — pure **top-K neighbor pruning**, but with a positivity twist you'll have to spot.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **A chain has a middle** — fix the middle edge, don't enumerate four nodes.
> 2. **Each endpoint only needs its top-3 neighbors** — at most two others can block it.
> 3. **Distinctness is the whole reason** top-1 fails and top-3 works.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "bounded blockers ⇒ keep top-K, K = blockers + 1."]**
>
> When only a fixed number of candidates can ever be excluded, your hand should already be reaching for a top-K list — never the full neighbor scan.
>
> *(GCA reminder — for the interview itself: state the O(V⁴) brute force, name the "chain has a middle" insight out loud, *then* justify top-3 by counting the blockers. Google's General Cognitive Ability signal isn't the code — it's you narrating the path from naive to optimal and asking the distinctness question before you prune.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Largest Color Value in a Directed Graph" — a directed graph with a cycle drawn in red.]**

> Here the chain was tiny and fixed — exactly four nodes. But what happens when the path can be **any length**, the edges point one direction, and the graph might even loop back on itself? Suddenly "fix the middle" doesn't help, and you need topological order to even walk it safely. That's the next one: Largest Color Value in a Directed Graph. Same instinct — value along a path — but the whole machine changes. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int maximumScore(int[] scores, int[][] edges) {
    int n = scores.length;
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) {
        adj.get(e[0]).add(e[1]);
        adj.get(e[1]).add(e[0]);
    }

    // Keep only each node's 3 highest-scoring neighbors (top-3 = blockers + 1).
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
            if (a == c) continue;
            for (int d : top[c]) {
                if (d == b || d == a) continue;
                best = Math.max(best,
                        scores[a] + scores[b] + scores[c] + scores[d]);
            }
        }
    }
    return best;
}
```
