# 🎬 Recording Script — Copy List with Random Pointer

**Pattern: Hash Map (old→new) / interleaving · LeetCode 138 · Medium ⭐ · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hash-map O(1) lookup (Two Sum) + linked-list pointer basics.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a linked list of 5 nodes. Blue `next` arrows go left-to-right. Then red `random` arrows appear — one jumps FORWARD across three nodes. The screen freezes on that forward arrow.]**

> Copying a linked list is a five-minute problem. Walk it, make a new node for each one, chain them up. Easy.
>
> Then Google adds one arrow — a `random` pointer that can jump to **any** node in the list. And suddenly your clean one-pass copy falls apart, because that arrow can point to a node **you haven't created yet.**
>
> **[VISUAL: the forward red arrow, with a "?" over its target — an empty dashed box.]**
>
> How do you set a pointer to something that doesn't exist? By the end of this video you'll have two answers — a clean one everybody accepts, and a slick O(1)-space one that makes interviewers lean forward. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below: three nodes `7 → 13 → 11`, with a red random arrow from `13` back to `7`, and one from `11` to `13`.]**

> The whole problem in one line: **make a deep copy of the list — brand-new nodes — where both the `next` wiring and the `random` wiring mirror the original.**
>
> "Deep copy" means the new list shares **zero** nodes with the old one. If node `13`'s random points to node `7` in the original, then in the copy, `13`-prime's random must point to `7`-**prime** — the clone of 7, not the original 7.
>
> Tiny example — three nodes. `13`'s random points back to `7`. `11`'s random points to `13`. Keep your eye on that `11`-to-`13` arrow — it points *backward*, but randoms can also point *forward*, and that's the whole trap.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — let them feel the pain)*

**[VISUAL: original list on top. Below it, we build clones left-to-right. When we try to wire a forward random, the target clone is a dashed empty box.]**

> Let's try the naive one-pass copy. Walk the original, and for each node make a clone and wire everything as we go.
>
> Clone `7`. Its random points to... itself? No — say `7`'s random is null, fine. Clone `13`. Its random points to `7` — and `7`-prime already exists, so wire it. So far so good.
>
> Now imagine a node early in the list whose random points to a node near the **end**.
>
> **[VISUAL: cloning node 2, its random arrow reaches forward to a dashed empty box labeled "clone of node 5 — doesn't exist yet".]**
>
> We're cloning node 2. Its random points to node 5. But we haven't reached node 5 yet — its clone doesn't exist. We're stuck. We cannot set this pointer in a single forward pass.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the dashed empty box. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** There's the pain. `next` always points to the node right after — easy. But `random` can jump *anywhere*, including to clones that don't exist yet. One forward pass can't wire it.
>
> **LEARNER:** So... could I just do two passes? First make all the clones, then go back and wire the randoms?
>
> **TEACHER:** You're already halfway to the answer — yes, two passes. But that raises the real question. Pause and think: **in pass two, when I'm at original node X and its random points to node Y, how do I find "the clone of Y" — instantly — for *any* Y in the list?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it)*

**[VISUAL: the phrase "given original node, get its clone" morphs into a hash map `original → clone`.]**

> **TEACHER:** The question we need answered fast is *"given an original node, hand me its clone."* A lookup keyed by node identity. That's a **hash map** — `original node → its clone`.
>
> So here's the plan. **Pass one:** walk the list and create every clone, storing `map[original] = clone`. Wire *nothing* yet — just populate the map. Now every clone exists.
>
> **[VISUAL: pass 1 — five originals, five clones below, dashed lines linking each pair through the map.]**
>
> **Pass two:** walk again. For each original, both its `next` and its `random` point to *some* original nodes — and every one of those now has a clone in the map. So `clone.next = map[original.next]`, `clone.random = map[original.random]`. Every lookup resolves, forward or backward, because all clones already exist.

**[VISUAL: pass 2 — wiring node 2's forward random. This time map[node 5] returns the real clone, arrow lands solidly.]**

> That forward-jumping random that broke us? No longer a problem. Its target clone is already in the map. The map turned an impossible one-pass wiring into two easy passes.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Clone all nodes FIRST (fill the map), then wire pointers via the map."]**

> The key move: **create every clone before you wire anything.** Pass one fills a map from old to new. Pass two wires `next` and `random` by looking up the map. Separating "create" from "connect" is what defeats the forward-reference problem — and it's a pattern you'll reuse for cloning *any* structure with cross-links, like a graph.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. The Node definition, then chunk 1.]**

> Let's code the map version — the one you should reach for first. Pass one: clone every node into the map.

```python
def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}

    cur = head
    while cur:                                # pass 1: clones only
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
```

> **[VISUAL: add pass 2, highlight the two wiring lines.]** Pass two: now wire both pointers through the map.

```python
    cur = head
    while cur:                                # pass 2: wire next + random
        old_to_new[cur].next = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next

    return old_to_new[head]
```

> That's the entire solution. Notice `.get()`, not `[]` — because `cur.next` or `cur.random` might be `None`, and `map.get(None)` cleanly returns `None`, exactly the wiring we want for the end of the list.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why it works.
>
> Pass one does *nothing* but create nodes and record them. That's the discipline — resist wiring here, because a forward random would send you to a clone that doesn't exist.
>
> By the time pass two runs, `old_to_new` has an entry for **every** original. So `old_to_new.get(cur.random)` always resolves — the target clone is guaranteed to be there.
>
> **LEARNER:** Why `old_to_new.get(cur.next)` instead of `old_to_new[cur.next]`?
>
> **TEACHER:** Because the last node's `next` is `None`, and `None` was never put in the map. `map[None]` would throw a KeyError; `map.get(None)` returns `None` — which is precisely the value we want to assign. Same for a random that points nowhere. One method call handles both the real nodes and the null edges.

---

## 9. DRY-RUN THE CODE — `7:20`
*(worked example — prove it)*

**[VISUAL: `[[7,null],[13,0],[11,4],[10,2],[1,0]]` — pairs are [value, random-index]. Map fills, then randoms resolve.]**

> Run it on the classic example — five nodes, each tagged with where its random points.

> **Pass 1** creates clones `7' 13' 11' 10' 1'` and the map `{7:7', 13:13', 11:11', 10:10', 1:1'}`.
>
> **Pass 2**, a couple of key wirings:

| original | random points to | wire `clone.random =` | result |
|---|---|---|---|
| 13 | node 7 (index 0) | map[7] = 7' | 13'.random → 7' |
| 11 | node 1 (index 4) | map[1] = 1' | 11'.random → 1' (a forward jump!) |
| 7 | null | map[None] = None | 7'.random → None |

> Node 11's random jumps all the way forward to node 1 — and it resolves instantly, because `1'` was created back in pass one. The copy's topology exactly mirrors the original.

---

## 10. COMPLEXITY, OUT LOUD — `8:10`
*(transfer to interview)*

**[VISUAL: row — Hash map, two passes: O(n) time, O(n) space.]**

> Out loud: *"Two passes, each O(n), so O(n) time. The map holds one entry per node — O(n) extra space. That space is what the follow-up will ask me to remove."*
>
> And that's the perfect segue, because the interviewer's next words are almost always: *"Can you do it without the map?"*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:50`
*(depth — the O(1) interleaving trick)*

**[VISUAL: the list transforms — each clone woven right after its original: `7 → 7' → 13 → 13' → 11 → 11' ...`]**

> Yes — and here's the trick that impresses. Instead of a *separate* map, we hide the mapping **inside the list itself**. Weave each clone directly after its original: `7, 7-prime, 13, 13-prime, ...`.
>
> Now — watch this — the clone of any node `X` is simply `X.next`. The "map" is free; it's the list structure. So `X-prime`'s random is `X.random.next` — the node after X's random target.

```python
def copyRandomList_interleave(head):
    if not head:
        return None

    cur = head                              # pass 1: weave clone after each original
    while cur:
        clone = Node(cur.val)
        clone.next = cur.next
        cur.next = clone
        cur = clone.next

    cur = head                              # pass 2: randoms via the interleaving
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next

    cur = head                              # pass 3: unweave into two lists
    dummy = Node(0)
    copy_prev = dummy
    while cur:
        clone = cur.next
        cur.next = clone.next               # restore original
        copy_prev.next = clone              # build copy
        copy_prev = clone
        cur = cur.next
    return dummy.next
```

> **LEARNER:** Hold on — `cur.next.random = cur.random.next`. That line looks like magic. Why is that right?
>
> **TEACHER:** Unpack it slowly. `cur.next` is the clone of `cur` — because we wove it in right after. `cur.random` is some original node; and the clone of *that* is `cur.random.next` — same weaving rule. So we're saying: "clone-of-cur's random = clone-of-(cur's random target)." Exactly the deep-copy wiring, with no map — the `.next` link *is* the lookup.
>
> Pass three just unweaves: restore each original's `next`, and stitch the clones into their own list. Same O(n) time, but **O(1) extra space** — no map at all.
>
> The line to say: *"Map version is O(n) space; I can weave clones after originals so the clone of any node is just node-dot-next, wire randoms without a map, then unweave."*

---

## 12. YOUR TURN (active recall) — `10:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Clone Graph (LC 133)". A little graph with a cycle.]**

> Before the next video, try **Clone Graph**. Same exact instinct — an `old → new` hash map to deep-copy a structure with arbitrary cross-references — but now it's a graph with cycles, so you clone-and-wire as you traverse. If you own Copy List, Clone Graph is the same muscle.
>
> Fifteen minutes, no peeking.

---

## 13. LOCK IT IN — `11:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Separate "create all nodes" from "wire all pointers"** — that beats forward references.
> 2. **`old → new` hash map** is the go-to deep-copy tool for any cross-linked structure.
> 3. **Interleaving** encodes that map *inside* the list — clone of X is `X.next` — for O(1) space.
>
> The memory peg — when a copy has *arbitrary cross-pointers*, think: **clone everyone first, then connect the clones.**

---

## 14. CLIFFHANGER — `11:50`
*(open loop to next lesson)*

**[VISUAL: a blurred grid of 1s and 0s — an island map.]**

> So far we've been chasing pointers through lists. Next, the pointers become *coordinates* — a 2-D grid where blobs of land form islands, and you have to find the biggest one. The tool changes from a hash map to a flood fill, but the instinct — "explore everything reachable from here" — is about to feel very familiar. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Interleaving, O(1) extra space.
public Node copyRandomList(Node head) {
    if (head == null) return null;

    for (Node cur = head; cur != null; ) {           // weave clones in
        Node clone = new Node(cur.val);
        clone.next = cur.next;
        cur.next = clone;
        cur = clone.next;
    }
    for (Node cur = head; cur != null; cur = cur.next.next) {   // wire randoms
        if (cur.random != null) cur.next.random = cur.random.next;
    }
    Node dummy = new Node(0), copyPrev = dummy;       // unweave
    for (Node cur = head; cur != null; cur = cur.next) {
        Node clone = cur.next;
        cur.next = clone.next;
        copyPrev.next = clone;
        copyPrev = clone;
    }
    return dummy.next;
}
```

*(The hash-map version is often the expected answer — mention it, then offer the interleaving as the O(1)-space follow-up.)*
