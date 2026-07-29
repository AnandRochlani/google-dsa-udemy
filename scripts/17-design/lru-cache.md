# 🎬 Recording Script — LRU Cache

**Pattern: Design (hash map + doubly linked list) · LeetCode 146 · Medium ⭐ · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hash-map O(1) lookup (Two Sum lesson) + linked-list pointer surgery.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an Google interview room. The whiteboard reads "Design an LRU Cache — O(1) get AND put." A cursor blinks. A 15-minute timer starts counting down.]**

> This is the single most-asked design question at Google. *"Build a cache that forgets the least-recently-used thing — and every operation has to be O(1)."*
>
> Here's what trips people up: they can get *fast lookup* easily. They can get *ordering* easily. What they can't do — under pressure, on a whiteboard — is get **both at once**.
>
> By the end of this video you'll see the one move that fuses two data structures into a single machine where every operation is constant time. And once you see it, you'll never un-see it — it powers half the design questions Google asks. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence up top: "A fixed-size cache that evicts the least-recently-used key." Below, a box labeled "capacity = 2".]**

> Here's the whole thing in one line: **a cache with a fixed capacity that, when it's full, throws out whatever you touched longest ago.**
>
> Two operations. `get(key)` — give me the value, and *using it* counts as "recently used." `put(key, value)` — store it, and if that pushes us over capacity, **evict the least-recently-used key first.**
>
> Tiny example — capacity 2. Watch this exact sequence; we'll trace it by hand.

**[VISUAL: a call list appears — put(1,1), put(2,2), get(1), put(3,3), get(2). The last line get(2) has a "?" next to it.]**

> Five calls. That last one — `get(2)` — returns something surprising. Hold onto that question.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a simple list of keys, labeled "order: LRU on left, MRU on right". An "operations" counter, top-right.]**

> Let's do what your brain does first. Keep a list of keys in the order you used them — least-recent on the left, most-recent on the right. And a separate dictionary for the actual values.
>
> `put(1,1)` — list is `[1]`. `put(2,2)` — list is `[1, 2]`. Now `get(1)` — I return the value, but I also have to mark 1 as most-recent. So I *find* 1 in the list, *remove* it, and *append* it to the end: `[2, 1]`.
>
> **[VISUAL: highlight the "find 1" step scanning left-to-right across the list, then the shift as everything after it slides down.]**
>
> See that "find and remove"? On a list, that's a **scan** to locate it, then a **shift** to close the gap. Now `put(3,3)` — we're full, so evict the left end, key 2, then append 3.
>
> **[VISUAL: the operations counter ticks up on every scan and shift.]**
>
> It works. It gives the right answers. But watch that counter — every single `get` and `put` is scanning and shifting the list.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the "find 1 and remove it" step, the scan arrow highlighted red. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So where's the pain? That "find the key and move it to the end." Finding it in a list is O(n) — you scan. Removing from the middle is O(n) — you shift. With up to 200,000 calls, that's tens of billions of operations. The interviewer said O(1), and we just wrote O(n).
>
> **LEARNER:** Okay but hold on — the dictionary already finds the value in O(1). Why can't the dictionary *also* handle the ordering? Why do I even need a list?
>
> **TEACHER:** That is exactly the right question, and it's the crux of the whole problem. Pause here and sit with it: **a dictionary gives you instant lookup but no notion of order. A list gives you order but slow removal. What single structure lets you pull an item out of the middle and slap it on the end — both in O(1)?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: split the requirement into two boxes. Box 1: "Find value by key → O(1)". Box 2: "Move any item to 'most recent', drop the 'least recent' → O(1)".]**

> **TEACHER:** Here's the method for *every* design problem: take each thing you must do fast, and match it to the structure that does it fast. Then fuse them.
>
> Requirement one — *find a value by its key, instantly.* That's the textbook job of a **hash map**. Done, no debate.
>
> Requirement two is the hard one — *mark any item as most-recently-used, and evict the least-recently-used, both in O(1).* This is an ordering problem with a nasty twist: I need to yank an item out of the **middle** and move it to the front.
>
> **LEARNER:** Right, and that's what killed the array — removing from the middle shifts everything.
>
> **TEACHER:** Exactly. And a *singly* linked list doesn't save you either — to unlink a node you need the node *before* it, and finding that is another O(n) scan. But a **doubly linked list**? Each node knows its own `prev` and its own `next`.

**[VISUAL: three nodes in a row, each with prev/next arrows. Highlight the middle one. Show `node.prev.next = node.next` and `node.next.prev = node.prev` — the two arrows re-route around it, and it's out. A little "O(1)" pops up.]**

> Given the node itself, I splice it out in two pointer assignments — constant time, no scanning. So: keep most-recently-used at the head, least-recently-used at the tail. Touch an item? Splice it out, re-insert at the head. Need to evict? Grab the tail. Both O(1).

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence — the fusion)*

**[VISUAL: the hash map on the left, the doubly linked list on the right. An arrow from a map entry "key 2" points AT the actual list node for 2. Boxed caption: "The map stores the NODE, not the value."]**

> Here's the fusion — the sentence to burn in: **the hash map's value isn't the data, it's the linked-list node itself.**
>
> `key → node`. So `get(2)` is: hash map hands me the node in O(1), then I splice that node to the head in O(1). Eviction is: read the tail node, delete its key from the map, unlink it.
>
> **[VISUAL: highlight that the tail node also stores its own key. Caption: "node stores its key so eviction can clean the map."]**
>
> And one detail that saves you: store the **key inside the node** too. When you evict via the tail, you need to delete that entry from the map — and only the node knows which key it was. **Hash map for lookup, doubly linked list for order, fused by shared nodes.** That's the whole design.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type the Node class only.]**

> Let's build it. First, the node — value, key, and two pointers.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key          # stored so eviction can clean the map
        self.val = val
        self.prev = None
        self.next = None
```

> **[VISUAL: add the constructor, highlight the two sentinel lines.]** Now the cache. The trick that kills every edge case: **sentinel head and tail** — two dummy nodes so the real list always sits *between* them and we never touch a `None`.

```python
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                 # key -> Node
        self.head = Node()            # most-recent side (dummy)
        self.tail = Node()            # least-recent side (dummy)
        self.head.next = self.tail
        self.tail.prev = self.head
```

> **[VISUAL: add the two helpers, animate each on the node diagram.]** Two tiny helpers — the pointer surgery. Remove a node, and add a node right after head.

```python
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
```

> **[VISUAL: add get(), highlight the remove-then-add pair.]** Now `get`. Miss? Return -1. Hit? Grab the node, splice it out, re-add at front — that's the "mark as recently used."

```python
    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val
```

> **[VISUAL: add put(), highlight the eviction block.]** And `put`. If the key exists, unlink the old node. Make a new node, register it, add to front. Then — the eviction check.

```python
    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev          # node just before the tail sentinel
            self._remove(lru)
            del self.map[lru.key]         # THIS is why the node stores its key
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:45`
*(elaboration — why each line exists)*

**[VISUAL: the full class; spotlight each line as named.]**

> Let's walk the *why*.
>
> The sentinels — `head` and `tail` never hold real data. Because of them, `_add_front` and `_remove` never check "is this the first node? the last node?" There's always a node on both sides. That's four edge cases deleted for the price of two dummy nodes.
>
> `get` does remove-then-add-front. That pair *is* the recency update — the node was somewhere in the middle, now it's at the head, the freshest spot.
>
> In `put`, `self.tail.prev` — that's the real node closest to the tail sentinel, the genuine least-recently-used. We unlink it and — this line — `del self.map[lru.key]`. 
>
> **LEARNER:** Wait — why do we need the key *inside* the node for that? Can't we look it up?
>
> **TEACHER:** Look it up *how*? The map goes key → node, one direction. From the tail node I have the node, but I need its key to delete the map entry. There's no node → key lookup unless the node carries its own key. That one field is what makes eviction O(1) instead of an O(n) reverse search.
>
> **LEARNER:** Got it — the node has to remember who it is.
>
> **TEACHER:** Exactly.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the map and the list (head→tail = MRU→LRU) side by side, filling row by row.]**

> Back to our example, capacity 2. Watch the list, head-to-tail is most-to-least recent.

| Call | Action | Map keys | List (MRU→LRU) |
|---|---|---|---|
| put(1,1) | add front | {1} | 1 |
| put(2,2) | add front | {1,2} | 2, 1 |
| get(1)→1 | splice 1 to front | {1,2} | 1, 2 |
| put(3,3) | add 3; size 3>2 → evict tail.prev = **2** | {1,3} | 3, 1 |
| get(2)→**-1** | 2 was evicted | {1,3} | 3, 1 |

> There's the answer to our cliffhanger: `get(2)` returns **-1**. Why? At `put(3,3)` we were full. The least-recently-used key was **2** — because `get(1)` had just bumped 1 to the front, leaving 2 sitting at the tail. So 2 got evicted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute (list+dict): O(n) both. Ours: O(1) both. Space: O(capacity).]**

> Say it the way you'd say it to the interviewer: *"Both `get` and `put` are O(1) — one hash lookup plus a constant number of pointer rewires. The list version was O(n) per op because of the scan-and-shift; the doubly linked list makes middle-removal constant. Space is O(capacity) — the map and list hold at most `capacity` entries, which is optimal since we're contractually holding those items."*
>
> That's the sentence that earns the checkmark: brute force, why it fails, the fix, the cost.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:45`
*(depth + honesty — the shortcut)*

**[VISUAL: OrderedDict version, ~10 lines, next to the long version.]**

> Space is already optimal — O(capacity), you must hold the items. But there's a shortcut worth knowing, and it wins you points.
>
> Python's `OrderedDict` — and honestly a plain `dict` since 3.7 — is *already* a hash map layered over a doubly linked list internally. `move_to_end` and `popitem(last=False)` are both O(1).

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)
```

> Here's the move in the room: *"I can do this in ten lines with `OrderedDict` — but let me also show the manual hash-map-plus-doubly-linked-list, because that's exactly what `OrderedDict` is doing under the hood, and it's what you're really testing."* Knowing the shortcut **and** the internals — that's strong-hire.

---

## 12. YOUR TURN (active recall) — `11:30`
*(retrieval practice)*

**[VISUAL: "Your turn → LFU Cache (LC 460)". A blank editor.]**

> Before the next video, try **LFU Cache** — evict the least-*frequently*-used instead of least-recently-used. Same fusion instinct, but now you need a *second* ranking axis on top of this one.
>
> Don't peek. Wrestle with it for fifteen minutes. That struggle is what turns "I watched a video" into "I can build this cold on a whiteboard."

---

## 13. LOCK IT IN — `12:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Split the requirements, match each to a structure, then fuse.** That's the entire design playbook.
> 2. **Hash map for O(1) lookup + doubly linked list for O(1) reorder** — the map's values *are* the list's nodes.
> 3. **Sentinel head/tail** to delete edge cases; **store the key in the node** so eviction cleans the map.
>
> The memory peg — when you hear *"cache"* and *"O(1) eviction"*, your hand should already be drawing two boxes: **a map pointing at the nodes of a doubly linked list.**

---

## 14. CLIFFHANGER — `12:30`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "LFU Cache — evict by frequency". A second ranking axis fades in over the LRU diagram.]**

> But here's where LRU breaks. What if the rule isn't "least *recently* used" but "least *frequently* used" — and when two keys are tied on frequency, you fall back to recency? Now you need to rank by *two* things at once, still in O(1). That's the next one — and the answer is to hide an entire LRU cache *inside* each frequency bucket. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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

*(Java one-liner: extend `LinkedHashMap`, override `removeEldestEntry`. Mention it, then show the manual version — same reasoning as the `OrderedDict` note.)*
