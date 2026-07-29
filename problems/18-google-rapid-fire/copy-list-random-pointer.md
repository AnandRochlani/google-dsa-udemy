# Copy List with Random Pointer

> **LeetCode:** 138. Copy List with Random Pointer · **Difficulty:** 🟡 Medium · **Pattern:** Hash Map (old→new) / interleaving · **Google frequency:** ⭐ high

---

## Problem

A linked list where each node has a `next` pointer **and** a `random` pointer that points to *any* node in the list or to `None`. Return a **deep copy**: a brand-new list of new nodes whose `next` and `random` wiring mirrors the original, sharing no nodes with it.

**Example:** `head = [[7,null],[13,0],[11,4],[10,2],[1,0]]` (each pair is `[value, random_index]`) → an identical, independent list. E.g. node `13`'s random points to node `7` (index 0) in the copy, not the original.

**Constraints that matter:** up to `1000` nodes. The trap is the **random pointer**: when you create a copy of node A and want to set its `random` to the copy of node B, that copy of B **may not exist yet** (B could be later in the list). You need a way to answer "given an original node, what's its clone?" — for a node you might not have created at that moment.

---

## 🧠 Intuition — how you'd actually arrive at this

- **Why the naive copy fails:** walking the list and copying `next` is easy. But `random` can jump *forward* to a node you haven't cloned yet, so you can't set `copy.random` in a single forward pass — the target clone doesn't exist.
- **The question to answer fast:** "for original node X, give me its clone." That's a lookup keyed by node identity → a **hash map** `original → clone`.
- **The two-pass hash-map plan:** Pass 1, create every clone and record `map[original] = clone` (wire nothing yet). Now *every* clone exists. Pass 2, for each original, set `clone.next = map[original.next]` and `clone.random = map[original.random]` — both lookups resolve because all clones already exist. Forward-jumping randoms are no longer a problem.
- **The leap to O(1) space — interleaving:** instead of a map, weave each clone **right after its original**: `A → A' → B → B' → C → C'`. Now the clone of any node `X` is simply `X.next`, so `X'.random = X.random.next` — the map is *encoded in the list structure itself*. Three passes: interleave, wire randoms, then unweave to separate the two lists.
- **Pattern trigger:** *"copy/relate a structure with arbitrary cross-references"* → **hash map from old to new**; and *"eliminate the map by threading clones into the original"* is the classic O(1)-space follow-up.

---

## ① Brute Force

Two passes with a hash map — the clean, correct baseline (this is what most people should write first).

```python
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random

def copyRandomList_hashmap(head):
    if not head:
        return None
    old_to_new = {}

    # Pass 1: clone every node, no pointers wired yet.
    cur = head
    while cur:
        old_to_new[cur] = Node(cur.val)
        cur = cur.next

    # Pass 2: wire next and random using the map.
    cur = head
    while cur:
        clone = old_to_new[cur]
        clone.next = old_to_new.get(cur.next)      # None if cur.next is None
        clone.random = old_to_new.get(cur.random)
        cur = cur.next

    return old_to_new[head]
```

**Why it's the natural first attempt:** it directly solves the forward-random problem — create all clones first, then wire, so every target already exists.

**Why it's "brute" here:** it's correct and O(n) time, but it uses **O(n) extra space** for the map. That's the thing the follow-up asks us to remove.

**Complexity:** Time `O(n)`, Space `O(n)`.

*(A dictionary-free-looking one-pass `defaultdict` variant exists but still uses O(n) space — same class.)*

---

## ② Optimised Solution

Same two-pass idea, stated as the reference solution. `map[original] → clone`, then wire both pointers. (Shown above; repeated here as the "the map version is the go-to" answer, since it's the one interviewers most often accept.)

```python
def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}
    cur = head
    while cur:                                   # pass 1: clones
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                                   # pass 2: wire
        old_to_new[cur].next = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next
    return old_to_new[head]
```

**Walk the example** `[[7,null],[13,0],[11,4],[10,2],[1,0]]`:
- Pass 1 creates clones `7' 13' 11' 10' 1'`, map `{7:7', 13:13', ...}`.
- Pass 2 on node `13` (random → node `7`): `13'.random = map[7] = 7'`. On node `11` (random → node `1`, index 4): `11'.random = 1'`. Every random resolves via the map regardless of position.

**Why it's correct:** after pass 1 the map contains a clone for every original, so in pass 2 both `map[cur.next]` and `map[cur.random]` are guaranteed present (or `None` maps to `None`). The copy's topology exactly mirrors the original.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ③ Space Optimization — interleaving, O(1) extra

Encode the old→new mapping *inside the list* by placing each clone right after its original, so no hash map is needed.

```python
def copyRandomList_interleave(head):
    if not head:
        return None

    # Pass 1: A -> A' -> B -> B' -> ...  (clone woven after each original)
    cur = head
    while cur:
        clone = Node(cur.val)
        clone.next = cur.next
        cur.next = clone
        cur = clone.next            # jump to the next original

    # Pass 2: set clone.random using the interleaving.
    cur = head
    while cur:
        if cur.random:
            cur.next.random = cur.random.next   # clone of cur.random is cur.random.next
        cur = cur.next.next

    # Pass 3: unweave the two lists back apart.
    cur = head
    dummy = Node(0)
    copy_prev = dummy
    while cur:
        clone = cur.next
        cur.next = clone.next       # restore original list
        copy_prev.next = clone      # build copy list
        copy_prev = clone
        cur = cur.next
    return dummy.next
```

**Trace the key line:** after pass 1 the list is `7 7' 13 13' 11 11' ...`. For original `13` whose `random` is `7`, the clone of `7` is `7.next = 7'`, so `13.next.random = 13'.random = 13.random.next = 7.next = 7'`. Exactly right — the "give me the clone of X" lookup became `X.next`.

**Why it's correct:** interleaving guarantees `clone(X) == X.next` for every node during passes 2–3, so `clone.random = X.random.next` wires randoms correctly. Pass 3 carefully restores each original's `next` while stitching the clones into their own list, leaving the input unmodified.

**Complexity:** Time `O(n)`, Space **`O(1)` extra** (no map — the clones are the only new allocations, which the output requires anyway).

> Interview line: *"The hash-map version is O(n) space. I can get O(1) by weaving each clone right after its original — then the clone of any node is just node.next, so I set randoms without a map, and unweave at the end."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space (extra) |
|---|---|---|
| Hash map (old → new), two passes | O(n) | O(n) |
| Interleaving (clone after original) | O(n) | **O(1)** |

---

## Say it out loud (interview narration)

> *"The random pointer can jump to a node I haven't cloned yet, so I can't wire it in one pass. The clean fix is a hash map from each original node to its clone: pass one creates all the clones, pass two wires next and random by looking them up — O(n) time and space. To hit O(1) space I weave each clone directly after its original, so the clone of any node is just node.next; I set randoms as node.next.random = node.random.next, then unweave the two lists. Same O(n) time, no map."*

## Related / follow-ups
- **Clone Graph** (133) — same old→new hash-map deep-copy idea on a graph.
- **Copy List with Random Pointer** interleaving — the O(1)-space technique here.
- **Linked List Cycle** (141) — pointer manipulation fundamentals.
- **Merge Two Sorted Lists** (21) — dummy-node stitching, as in pass 3.
