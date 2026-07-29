# 🎬 Recording Script — Clone Graph
**Pattern: Graphs (DFS/BFS traversal + old→new hash map) · LeetCode 133 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the grid problems taught us "visited" markers. Here the graph is *literal* — node objects with pointers — and "visited" grows one extra job.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a small graph of four connected node bubbles. A "copy" icon. Then a red stack-overflow error slams in.]**

> Google interview: *"Here's a node in a graph. Give me a deep copy of the whole thing — all new node objects, same connections."*
>
> You write the obvious recursive copy: to copy a node, copy its value, then copy each neighbor. Clean. You hit run… and it **stack-overflows.**
>
> Why? Because this graph has cycles — node 1 points to 2, and 2 points right back to 1. Your recursion bounces between them forever. By the end of this video you'll fix it with one hash map that does *two* jobs at once. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: a 4-node square graph:]**

```
   1 --- 2
   |     |
   4 --- 3
```

> One line: **return a brand-new copy of the graph — new node objects, identical structure.** Nothing shared with the original.
>
> Tiny example: four nodes in a square. `1` connects to `2` and `4`. `2` connects to `1` and `3`. And so on around the loop. Each node holds a value and a list of neighbors.
>
> The catch is right there in the picture: it's full of cycles. Every undirected edge is really a two-way loop — `1→2` *and* `2→1`. Hold onto that; it's the whole difficulty.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — feel the failure)*

**[VISUAL: recursion trace. copy(1) → copy(2) → copy(1) → copy(2)… arrows piling into a growing call stack.]**

> Let's trace the naive recursive copy by hand. "To copy node 1: make a new node, then copy each of its neighbors."
>
> Copy `1`. Its neighbors are `2` and `4`. So, copy `2`. But `2`'s neighbors are `1` and `3` — so copying `2` means copying `1` again. And copying `1` means copying `2` again…
>
> **[VISUAL: the call stack tower grows without bound; a "💥 stack overflow" tag.]**
>
> We never stop. And even if we somehow did, we'd make a *fresh* copy of node 1 every time we reached it from a different path — so the copy would have duplicate nodes instead of one shared node 1. It's not just slow. It's *wrong.*

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(generation effect — first pause)*

**[VISUAL: freeze on the copy(1)↔copy(2) loop. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So there are actually *two* problems tangled together. One: the cycle makes recursion infinite. Two: even without infinite looping, we'd duplicate any node reached by more than one path.
>
> **LEARNER:** The cycle part feels like the grid problems — I just need a *visited* set so I don't re-process node 1. Right?
>
> **TEACHER:** Half right — and the missing half is the whole lesson. A plain visited set says "yes, I've seen node 2." But when I'm wiring up node 1's neighbor list, "yes I've seen it" isn't enough — I need *the actual copy object* for node 2 to point at. Pause and predict: **what structure remembers not just "seen it" but "here's the specific copy I made"?** Three seconds.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — the map does double duty)*

**[VISUAL: a two-column table appears — left "original node," right "its clone." Rows fill in: 1→1', 2→2'…]**

> **TEACHER:** Here's the leap. Use a **hash map from each original node to its clone.** `old_to_new[original] = clone`. And that one map does **two jobs at once:**
>
> One — it's your **visited set.** "Is this original already in the map? Then I've cloned it; don't recurse again." That kills the infinite cycle.
>
> Two — it's your **lookup table.** "Give me the *one* clone that belongs to node 2." Every time node 2 shows up in someone's neighbor list, you fetch the same clone from the map. That kills the duplicate-node problem.
>
> **[VISUAL: cloning node 1; when recursion loops back to 1, the map lookup returns the existing 1' — a little "🔁 already cloned, reuse" badge, cycle arrow blocked.]**
>
> **LEARNER:** So the moment I create a clone, I record it in the map *before* I go touch its neighbors?
>
> **TEACHER:** Exactly — and the *ordering* is everything. Record the clone in the map **first**, *then* recurse into neighbors. That way, when the recursion inevitably loops back to this node, the map already has it, and we return the existing clone instead of spiraling. Record-before-recurse is what breaks the cycle.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable line)*

**[VISUAL: boxed line: "old→new hash map: visited set AND clone lookup. Record before you recurse."]**

> Burn it in: **a hash map from original to clone — it's your visited set and your clone lookup in one. Record the clone before recursing.**
>
> This exact move — original-to-copy map — powers "Copy List with Random Pointer" too. Same trick, different structure.

---

## 7. CODE IT — LIVE & CHUNKED — `5:25`
*(cognitive load — build in pieces)*

**[VISUAL: the Node class shown briefly, then empty editor.]**

> Quick reminder of the node shape, then we build.

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

> **[VISUAL: type chunk 1.]** The setup and the map.

```python
def clone_graph(node):
    if not node:
        return None
    old_to_new = {}                      # original node -> its clone
```

> **[VISUAL: add chunk 2, highlight the record-before-recurse line.]** The DFS.

```python
    def dfs(cur):
        if cur in old_to_new:
            return old_to_new[cur]       # already cloned → return that clone
        copy = Node(cur.val)
        old_to_new[cur] = copy           # RECORD before recursing — breaks cycles
        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
```

> **[VISUAL: add chunk 3.]** Kick it off.

```python
    return dfs(node)
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> The very first line of `dfs` — `if cur in old_to_new: return old_to_new[cur]` — is the cycle-breaker *and* the deduplicator. If we've made this node's clone, hand it back. Don't recurse, don't duplicate.
>
> `old_to_new[cur] = copy` **before** the neighbor loop — this ordering is non-negotiable. If you recursed into neighbors *first* and recorded the clone *after*, the cycle would loop back to `cur`, find it *not* in the map yet, and recurse again — infinite loop restored. Record first.
>
> The neighbor loop wires the clone's edges to the *clones* of the neighbors — fetched or freshly made via `dfs(nei)`. So the copied graph's edges point only at copied nodes. Nothing leaks from the original.
>
> **LEARNER:** Why does the map key on the *node object* itself, not its `val`? Wouldn't `val` be simpler?
>
> **TEACHER:** Here values happen to be unique, so `val` would work — but keying on the object identity is the robust choice: it's what actually distinguishes nodes even if values repeat, and it's O(1) since node objects are hashable by identity. Lean on identity, not on a lucky uniqueness of values.

---

## 9. DRY-RUN THE CODE — `7:55`
*(worked example — prove it)*

**[VISUAL: the square graph; the old→new map filling; cycle lookups flashing.]**

> Trace DFS from node `1` on the square `1-2-3-4`.

| call | in map? | action | map after |
|---|---|---|---|
| dfs(1) | no | make 1', record | {1:1'} |
| dfs(2) | no | make 2', record | {1:1', 2:2'} |
| dfs(1) | **yes** | return 1' (cycle broken) | — |
| dfs(3) | no | make 3', record | {…, 3:3'} |
| dfs(2) | yes | return 2' | — |
| dfs(4) | no | make 4', record | {…, 4:4'} |
| dfs(1),dfs(3) | yes | return 1', 3' | — |

> Every original cloned exactly once, every cycle short-circuited by a map hit. Return `1'` — a perfect, fully-independent copy of the square. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:55`
*(transfer to interview)*

**[VISUAL: Time O(V + E) · Space O(V).]**

> Say it: *"Each node is cloned once and each edge is walked once, so O(V plus E) time — vertices plus edges, the standard graph-traversal cost. Space is O(V) for the map, plus O(V) for the recursion stack or BFS queue."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:30`
*(depth + honesty)*

**[VISUAL: the map highlighted with a "🔒 mandatory" lock; DFS-stack vs BFS-queue toggle.]**

> Here's the honest answer: **the map is not optional.** It's doing the essential work — without it you either loop forever or duplicate nodes. So O(V) space is a hard floor for this problem, not a wasteful choice. Naming *why* it can't shrink is itself a strong answer.
>
> The only choosable part is the traversal frontier: DFS adds an O(V) call stack, BFS adds an O(V) queue — same big-O. Reach for **BFS if the graph might be deep enough to blow Python's recursion limit.** Here's that version.

```python
from collections import deque

def clone_graph_bfs(node):
    if not node:
        return None
    old_to_new = {node: Node(node.val)}
    q = deque([node])
    while q:
        cur = q.popleft()
        for nei in cur.neighbors:
            if nei not in old_to_new:
                old_to_new[nei] = Node(nei.val)     # first sight → clone
                q.append(nei)
            old_to_new[cur].neighbors.append(old_to_new[nei])
    return old_to_new[node]
```

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Copy List with Random Pointer (LC 138)". Blank editor.]**

> Your turn: **Copy List with Random Pointer.** A linked list where each node also points to a random other node. It's the *identical* trick — an original-to-copy hash map — on a list instead of a graph. If today clicked, this one falls fast.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Cycles break naive recursive copies** — you need a visited mechanism.
> 2. **A plain visited set isn't enough** — you need *identity*: the specific clone for each original. One hash map, both jobs.
> 3. **Record the clone before recursing** — that ordering is what actually breaks the cycle.
>
> Memory peg: **"clone a graph? Keep a phone book — original in, clone out."** Look up before you build; write the entry before you dial the neighbors.

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: a chain of 3-letter words, each differing by one letter, morphing hit→hot→dot→dog→cog. Title blurred: "Word Ladder (LC 127)".]**

> We've traversed grids and object graphs. But the graph doesn't have to be *given* to you — sometimes you have to *imagine* it. Next: turn a pile of words into a graph where each one-letter change is an edge, and find the shortest transformation from one word to another. It's our hardest one, and it hides a slick trick for building edges fast. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// class Node { public int val; public List<Node> neighbors; ... }

public Node cloneGraph(Node node) {
    if (node == null) return null;
    Map<Node, Node> oldToNew = new HashMap<>();
    return dfs(node, oldToNew);
}

private Node dfs(Node cur, Map<Node, Node> oldToNew) {
    if (oldToNew.containsKey(cur)) return oldToNew.get(cur);
    Node copy = new Node(cur.val);
    oldToNew.put(cur, copy);                  // record before recursing
    for (Node nei : cur.neighbors) {
        copy.neighbors.add(dfs(nei, oldToNew));
    }
    return copy;
}
```
