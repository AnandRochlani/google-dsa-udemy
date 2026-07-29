# 🎬 Recording Script — Minimum Height Trees
**Pattern: Topological Sort (leaf-trimming) · LeetCode 310 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Kahn's BFS on directed graphs (Course Schedule) — earlier lesson.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree of nodes. It gets "picked up" by different nodes as the root — each time the tree dangles to a different height. A counter shows the height changing: 3, 2, 3…]**

> Here's a deceptively deep one Google likes: *"You've got a tree. Pick a node to be the root. Which choice makes the tree as short as possible?"*
>
> Your first instinct — try every node, measure the height, keep the best — is correct and will get you a "too slow." At twenty thousand nodes it times out.
>
> The fast answer flips the whole thing inside out: instead of asking "which node is the best *root*," you ask "which nodes are the *worst*" — and peel them away. By the end you'll see why the leaves are the enemy, and why trimming them finds the center in one pass. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: "n = 4, edges = [[1,0],[1,2],[1,3]]". A star: node 1 in the center connected to 0, 2, 3. Answer: [1].]**

> The problem in one line: **return every node that, used as the root, gives the minimum possible tree height.** Height is the longest root-to-leaf path in edges.
>
> Tiny example: node 1 sits in the middle, connected to 0, 2, and 3. Root at 1 → height 1, everything is one hop away. Root at any leaf → height 2. So the answer is `[1]`.
>
> One important fact the problem promises: the answer is always **one or two nodes.** Never three. Tuck that away.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a 6-node tree. A BFS fans out from node 0, then restarts from node 1, then node 2… a "BFS runs" counter climbing.]**

> The brute force: root at every node, BFS to find that root's height, track the minimum.
>
> Root at 0 — BFS the whole tree, height comes out 3. Restart. Root at 1 — BFS the *whole tree again*, height 2. Restart. Root at 2 — again…
>
> **[VISUAL: each root triggers a full fan-out; counter hits 6 full BFS traversals.]**
>
> Every one of the `n` roots costs a full O(n) BFS. That's O(n squared). At n = 20,000, that's four hundred million operations. Time limit exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. A path graph 0—1—2—3—4 with heights labeled at each root: 4,3,2,3,4. The middle node 2 glows. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at a simple path — five nodes in a line. Root at an end, height 4. Root at the middle, height 2. The best root is dead center. Rooting anywhere else just makes one side longer.
>
> **LEARNER:** So the answer is basically the *middle* of the tree — but a tree isn't a straight line. What even is the "middle" of a branchy tree?
>
> **TEACHER:** That's the right question. Pause and predict: **if the best roots live in the center, and the worst roots are the leaves on the outside — how could you find the center without measuring anything, just by repeatedly removing the outermost nodes?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it)*

**[VISUAL: the 6-node tree. All degree-1 leaves flash red and get peeled off simultaneously. A new layer of leaves is exposed and flashes. Repeat until 1-2 nodes remain.]**

> **TEACHER:** Here's the leap. The leaves — nodes with a single connection — are the *worst* possible roots; they're as far from center as you can get. So peel them all off at once.
>
> That exposes a new layer of leaves. Peel those too. Each peel shrinks the tree inward from *every* end at the same time — like peeling an onion toward its core. Whatever survives when two or fewer nodes remain **is** the center.
>
> **LEARNER:** Peeling leaves layer by layer, from a queue… that's Kahn's algorithm again, isn't it?
>
> **TEACHER:** It is — with one word swapped. Directed graphs used **in-degree**. Here the graph is undirected, so we use plain **degree** — the number of edges touching a node. A leaf is a node of **degree 1.** Remove it, decrement its neighbor's degree, and if the neighbor drops to 1, it's a new leaf. Same drain, outside-in.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Peel degree-1 leaves layer by layer until ≤ 2 nodes remain — those are the centers."]**

> The key move: **repeatedly strip all degree-1 leaves until two or fewer nodes are left. The survivors are the centroids — the best roots.**
>
> One center if the tree's longest path has an even number of edges, two if it's odd. Never three — which is exactly the guarantee the problem gave us.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1 — the two base cases.]**

> Handle the trivial trees first — one or two nodes are already the answer.

```python
from collections import deque

def find_min_height_trees(n, edges):
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
```

> **[VISUAL: chunk 2.]** Build an undirected adjacency set, then collect the initial leaves — degree 1.

```python
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    leaves = deque(i for i in range(n) if len(adj[i]) == 1)
    remaining = n
```

> **[VISUAL: chunk 3, the peel loop.]** Now peel, layer by layer, until 2 or fewer remain.

```python
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

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> Walk the *why*.
>
> The two base cases exist because the loop stops at `remaining > 2`; with n = 1 or 2 it would never run, and n = 2 has no single leaf to peel. Answer them directly.
>
> `adj` is a *set* per node, not a list, because we `remove` neighbors as we detach — set removal is O(1).
>
> The initial `leaves` are every degree-1 node — the whole outer rind at once.
>
> **LEARNER:** Why capture `layer_size = len(leaves)` *before* the inner loop? Why not just drain the queue until it's empty?
>
> **TEACHER:** Crucial. As we peel this layer, *new* leaves get appended to the same queue. If we drained until empty, we'd peel the next layer in the same pass and blow right past the center. Freezing `layer_size` peels exactly one ring, then re-checks `remaining`. That's what keeps both centers alive.
>
> `nb = adj[leaf].pop()` — a leaf has exactly one neighbor, so `pop` grabs it. Detach the leaf from that neighbor; if the neighbor is now degree 1, it joins the next ring.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: n = 6, edges [[3,0],[3,1],[3,2],[3,4],[5,4]]. Degrees shown, leaves highlighted, peeling animated.]**

> Run it on six nodes. Adjacency: `3` connects to `0,1,2,4`; `4` connects to `3,5`; the rest are leaves.

| step | remaining | leaves (ring) | after peeling |
|---|---|---|---|
| start | 6 | 0, 1, 2, 5 | detach all four |
| — | 2 | 3 (now deg 1), 4 (now deg 1) | loop stops |

> Removing 0, 1, 2 shrinks node 3 down to just `{4}` — degree 1. Removing 5 shrinks node 4 to just `{3}` — degree 1. `remaining` is now 2, the loop condition `> 2` fails, we stop.
>
> Survivors: **`[3, 4]`.** ✅ Two centers — the diameter here has an odd number of edges. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: "Brute: O(n²). Peel: O(n)."]**

> Out loud: *"Rooting at every node is O(n squared) — n BFS traversals, each O(n). The leaf-trimming peels each node exactly once and touches each edge a constant number of times, so it's O(n) time and O(n) space for the adjacency structure. It's Kahn's algorithm on an undirected graph, using degree instead of in-degree."*
>
> That last sentence connects it back to the pattern and signals you see the family resemblance — interviewers love that.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: adjacency structure labeled "required — n-1 edges". A note: "set() → degree[] array, same O(n)".]**

> Space is O(n) and that's the floor — a tree with n-1 edges needs its adjacency stored to know any node's degree. The leaf queue can hold up to n-1 nodes in a star graph, still O(n).
>
> One clean micro-optimization worth mentioning: instead of `set()` adjacency you can keep a normal adjacency list plus an integer `degree[]` array, decrementing `degree[nb]` on each trim and enqueuing when it hits 1. Same O(n) asymptotics, lower constant factor, no set operations. Not an asymptotic win — but a nice detail to voice.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Tree Diameter". A blank editor.]**

> Before the next video, try **Tree Diameter** — the longest path between any two nodes. Here's the tie-in: the centers you just found sit at the *midpoint* of that diameter. Two classic ways in — two BFS passes, or a DFS returning the deepest two branches. Spend ten minutes; feel how the center and the diameter are two views of the same thing.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Best roots = the tree's center(s)** — the middle of its longest path. One or two, never three.
> 2. **Peel degree-1 leaves layer by layer** — Kahn's on an undirected graph, degree in place of in-degree.
> 3. **Freeze the layer size** each round so you peel exactly one ring and stop at the center.
>
> The peg: **don't hunt for the best root — peel away the worst ones until only the center survives.**

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: the queue transforms — instead of nodes draining out, a small triangle-shaped heap appears, its root glowing. A blurred title: "Kth Largest Element".]**

> We've been draining queues — plain first-in-first-out. But what if the order you pull things out isn't the order they came in — what if you always need the *smallest*, or *largest*, or *most frequent* thing available, instantly, out of a churning pile? A queue can't do that. A **heap** can. That's the entire next chapter: heaps and top-K. First up — finding the kth largest number without sorting a thing. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
