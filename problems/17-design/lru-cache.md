# LRU Cache

> **LeetCode:** 146. LRU Cache · **Difficulty:** 🟡 Medium · **Pattern:** Design (hash map + doubly linked list) · **Google frequency:** ⭐ high

---

## Problem

Design a data structure that behaves like a **Least-Recently-Used cache** with a fixed `capacity`. It supports two operations:

- `get(key)` — return the value if the key exists, else `-1`. Using a key counts as *recently used*.
- `put(key, value)` — insert or update. If inserting pushes the size over `capacity`, **evict the least-recently-used key** first.

**Both operations must run in average O(1).**

**Example:**
```
LRUCache cache = new LRUCache(2)   // capacity 2
put(1, 1)        // cache: {1=1}
put(2, 2)        // cache: {1=1, 2=2}
get(1)   -> 1    // 1 is now most-recently-used; order: [2, 1]
put(3, 3)        // capacity full → evict LRU (key 2). cache: {1=1, 3=3}
get(2)   -> -1   // 2 was evicted
put(4, 4)        // evict LRU (key 1). cache: {3=3, 4=4}
get(1)   -> -1
get(3)   -> 3
get(4)   -> 4
```

**Constraints that matter:** up to `2 × 10⁵` calls, and the interviewer *explicitly* requires **O(1) per operation**. That single sentence dictates the entire design — anything that scans or sorts on each call (O(n)) fails. We need two things simultaneously in O(1): **look up a key by value**, and **know / update which key is least-recently-used**.

---

## 🧠 Intuition — how you'd actually arrive at this

> Design problems are solved by matching *each required operation* to a data structure that gives it in the target complexity, then fusing those structures so they share the same nodes.

Break the requirement into the two things we must do fast:

1. **"Find the value for a key in O(1)"** → that's the textbook job of a **hash map**. Done.
2. **"Find and remove the least-recently-used item in O(1), and mark any item as most-recently-used in O(1)"** → this is an *ordering* problem. We need a structure where we can (a) pop from one end (the LRU), (b) push to the other end (most recent), and (c) **pull an arbitrary node out of the middle and move it to the front** — all in O(1).

- **Why an array/list fails:** removing from the middle or the front shifts everything → O(n).
- **Why a singly linked list fails:** to unlink a node you need its *predecessor*, and finding that is O(n).
- **The leap:** a **doubly linked list**. Each node knows its `prev` and `next`, so given a node you can splice it out in O(1) (`node.prev.next = node.next; node.next.prev = node.prev`). Keep most-recently-used at the head, least-recently-used at the tail.

- **The fusion:** but how do we get *to* the node for a given key in O(1) so we can splice it? Store, in the hash map, **not the value but the linked-list node itself**: `key → node`. Now `get`/`put` is: hash-map lookup to grab the node (O(1)), splice it out and move it to the head (O(1)). Eviction is: read the tail node, delete its key from the map, unlink it (O(1)).

**Pattern trigger:** *"O(1) lookup **and** O(1) ordering/eviction"* → **hash map + doubly linked list**, where the map's values are the list's nodes. This exact combo also powers LFU and many "recently used" designs. Use **sentinel head/tail dummy nodes** so you never write a null check for the edges.

---

## ① Brute Force

Store the items in an ordered list (or `dict`), and track recency by position. On `get`, find the key and move it to the end. On eviction, remove from the front.

```python
class LRUCacheBrute:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.order = []          # list of keys, LRU at front, MRU at end
        self.store = {}          # key -> value

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.order.remove(key)   # O(n) scan + shift
        self.order.append(key)   # mark most-recently-used
        return self.store[key]

    def put(self, key: int, value: int) -> None:
        if key in self.store:
            self.order.remove(key)          # O(n)
        elif len(self.store) >= self.capacity:
            lru = self.order.pop(0)         # O(n) shift
            del self.store[lru]
        self.store[key] = value
        self.order.append(key)
```

**Why it's the natural first attempt:** it maps directly to the words "keep an order, move used items to the back, drop from the front."

**Why it's not enough:** `list.remove(key)` and `list.pop(0)` are both **O(n)** — they scan and shift. Every operation is O(n), so with 2×10⁵ calls this is ~10¹⁰ work → **Time Limit Exceeded**, and it violates the explicit O(1) requirement.

**Complexity:** Time `O(n)` per operation, Space `O(capacity)`.

---

## ② Optimised Solution

Hash map `key → node`, plus a doubly linked list ordered most-recent (head) to least-recent (tail). Sentinel `head`/`tail` nodes remove all edge-case null checks.

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}                       # key -> Node
        self.head = Node()                  # sentinel: most-recent side
        self.tail = Node()                  # sentinel: least-recent side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: "Node") -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: "Node") -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)                  # unlink from current spot
        self._add_front(node)               # re-insert as most-recent
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self._remove(self.map[key])     # will re-add at front
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev            # node just before tail sentinel
            self._remove(lru)
            del self.map[lru.key]           # why we store key IN the node
        return
```

**Walk the example** (`capacity = 2`). List shown head→tail (MRU→LRU):

| Call | Action | Map keys | List (MRU→LRU) |
|---|---|---|---|
| `put(1,1)` | add front | {1} | 1 |
| `put(2,2)` | add front | {1,2} | 2, 1 |
| `get(1)→1` | move 1 to front | {1,2} | 1, 2 |
| `put(3,3)` | add 3; size 3>2 → evict tail.prev=2 | {1,3} | 3, 1 |
| `get(2)→-1` | not in map | {1,3} | 3, 1 |
| `put(4,4)` | add 4; evict tail.prev=1 | {3,4} | 4, 3 |
| `get(1)→-1` | gone | {3,4} | 4, 3 |
| `get(3)→3` | move 3 to front | {3,4} | 3, 4 |
| `get(4)→4` | move 4 to front | {3,4} | 4, 3 |

Notice at `put(3,3)` the LRU was key `2` (it sat at the tail), exactly as required.

**Why it's correct:** the linked list's tail-to-head order *is* the recency order, and it's maintained as an invariant on every touch — any `get` or `put` on a key splices that node to the head, so the tail is always the genuine least-recently-used entry. Storing `key` inside the node is the crucial detail: when we evict via the tail we need to also delete the entry from the hash map, and only the node knows which key it belongs to.

**Complexity (per operation):** Time `O(1)` — one hash lookup plus a constant number of pointer rewires. Space `O(capacity)` — the map and the list hold at most `capacity` entries.

---

## ③ Space Optimization

Space is already optimal — **O(capacity)**, which is the minimum: you must physically store every cached entry, and the doubly linked list adds only two pointers per node (a constant factor), while the hash map adds one entry per key. Nothing grows beyond the number of items you're contractually holding.

There's a shortcut worth naming out loud: Python's `collections.OrderedDict` (and a plain `dict` in CPython 3.7+, which preserves insertion order) already implements a hash-map-over-a-doubly-linked-list internally. `move_to_end` and `popitem(last=False)` are O(1):

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)            # mark most-recent
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)     # evict least-recent (front)
```

> Say this explicitly in the interview: *"I can lean on `OrderedDict` for a clean O(1) solution, but let me also show the manual hash-map + doubly-linked-list version, since that's what `OrderedDict` is doing under the hood and it's what the interviewer usually wants to see."* Showing you know the shortcut **and** the internals is the strong-hire signal.

---

## Java (for Java interviewers)

```java
class LRUCache {
    private static class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }

    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0);   // MRU sentinel
    private final Node tail = new Node(0, 0);   // LRU sentinel

    public LRUCache(int capacity) {
        cap = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void remove(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    private void addFront(Node n) {
        n.next = head.next;
        n.prev = head;
        head.next.prev = n;
        head.next = n;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node n = map.get(key);
        remove(n);
        addFront(n);
        return n.val;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) remove(map.get(key));
        Node n = new Node(key, value);
        map.put(key, n);
        addFront(n);
        if (map.size() > cap) {
            Node lru = tail.prev;
            remove(lru);
            map.remove(lru.key);
        }
    }
}
```

*(Java also offers a one-liner: extend `LinkedHashMap` and override `removeEldestEntry`. Mention it, then show the manual version above — same reasoning as the `OrderedDict` note.)*

---

## Complexity Summary

| Approach | get | put | Space |
|---|---|---|---|
| Brute force (list + dict) | O(n) | O(n) | O(capacity) |
| Hash map + doubly linked list | O(1) | O(1) | O(capacity) |
| OrderedDict (same internals) | O(1) | O(1) | O(capacity) |

---

## Say it out loud (interview narration)

> *"The interviewer wants O(1) for both get and put, so I split the requirement: hash map gives me O(1) key lookup, and I need O(1) eviction of the least-recently-used item plus O(1) 'mark as most-recent.' That ordering with arbitrary-middle removal screams doubly linked list — head is most-recent, tail is least-recent, and splicing a node out is constant time because each node knows its prev and next. The trick that fuses them is storing the linked-list node itself as the hash map's value, and storing the key inside the node so eviction can clean up the map. I'll use sentinel head/tail nodes to kill the edge cases. Both operations are O(1), space is O(capacity), which is optimal since we have to hold the items anyway."*

## Related / follow-ups
- **LFU Cache** (460) — evict least-*frequently*-used; needs a frequency dimension on top of this.
- **Design HashMap** (706) — the map half of this design from scratch.
- **All O'one Data Structure** (432) — buckets of a doubly linked list, same fusion idea.
- **First Unique Number** (1429) — hash map + queue with lazy cleanup.
