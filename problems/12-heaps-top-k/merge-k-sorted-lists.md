# Merge k Sorted Lists

> **LeetCode:** 23. Merge k Sorted Lists · **Difficulty:** 🔴 Hard · **Pattern:** Heaps & Top-K · **Google frequency:** ⭐ high

---

## Problem

You're given an array of `k` linked lists, each already sorted in ascending order. Merge them into one sorted linked list and return its head.

**Example:** `lists = [[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`.
`lists = []` → `[]`. `lists = [[]]` → `[]`.

**Constraints that matter:** up to `k = 10⁴` lists, and up to `10⁴` nodes total (call it `N`). Concatenating everything and sorting is `O(N log N)`. The better structure exploits that each list is *already sorted*: a min-heap of the `k` list heads merges in `O(N log k)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Dump every node into an array, sort it, rebuild a list." Works, `O(N log N)`, but it throws away the fact that each input list is already sorted.
- **The key observation:** the global smallest unplaced node is always the head of *one* of the `k` lists. If I could cheaply find which of the `k` current heads is smallest, I'd append it, advance that list, and repeat. The bottleneck is "find the min among k things, repeatedly."
- **The leap (min-heap of k heads):** a **min-heap** keeps the smallest of a set instantly available at its top. Put the `k` list heads in a min-heap keyed on node value. Pop the smallest, append it to the output, and push that node's `next` (if any) back into the heap. The heap never holds more than `k` nodes, so each pop/push is `O(log k)`, and we do one per node → `O(N log k)`.
- **Why not `O(N log N)`?** Because the heap only ever ranks `k` candidates at a time, not all `N` nodes. When `k ≪ N`, `log k ≪ log N`.
- **The alternative (divide and conquer):** pairwise-merge the lists like merge sort — merge them in pairs, halving the count each round, `log k` rounds of `O(N)` work → also `O(N log k)`, with no heap needed.
- **Pattern trigger:** **"merge / pick the min across k sorted sources"** → **a min-heap of the k current heads** (`O(N log k)`), the same trick behind external merge sort.

---

## ① Brute Force

Collect all values, sort them, build a fresh list.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists_brute(lists):
    values = []
    for node in lists:
        while node:
            values.append(node.val)
            node = node.next
    values.sort()
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
```

**Why it's the natural first attempt:** flattening and sorting is the most obvious way to guarantee a sorted result, and it's easy to get right.

**Why it's not enough:** it ignores that each list is already sorted and pays `O(N log N)` to re-sort `N` values from scratch. It also allocates a full array of all values.

**Complexity:** Time `O(N log N)`, Space `O(N)`.

---

## ② Optimised Solution

Min-heap of the current heads; pop the smallest, push its successor.

```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:                                # skip empty lists
            # (value, tiebreaker index, node) — index avoids comparing nodes
            heapq.heappush(heap, (node.val, i, node))

    dummy = tail = ListNode()
    while heap:
        val, i, node = heapq.heappop(heap)      # smallest current head
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

**Note the tiebreaker `i`:** when two nodes have equal values, Python's tuple comparison would fall through to comparing the `ListNode` objects, which raises `TypeError`. The list index `i` breaks ties first, so nodes are never compared directly.

**Walk the example** `lists = [[1,4,5],[1,3,4],[2,6]]`:

- Heap seeded with heads: `(1,0,·), (1,1,·), (2,2,·)`.
- Pop `(1,0)` → output `1`; push its next `(4,0)`. Heap: `(1,1),(2,2),(4,0)`.
- Pop `(1,1)` → output `1`; push `(3,1)`. Heap: `(2,2),(4,0),(3,1)`.
- Pop `(2,2)` → output `2`; push `(6,2)`. Pop `(3,1)` → output `3`; push `(4,1)`.
- Pop `(4,0)` → `4`; push `(5,0)`. Pop `(4,1)` → `4`; list 1 ends. Pop `(5,0)` → `5`; list 0 ends. Pop `(6,2)` → `6`.
- Output: **`1→1→2→3→4→4→5→6`** ✅.

**Why it's correct:** at every step the heap holds exactly one candidate from each still-nonempty list — the current head. The global minimum among all unplaced nodes must be one of these heads (each list is sorted), so popping the heap's min always yields the next node in sorted order.

**Complexity:** Time `O(N log k)` — one heap op per node, heap size ≤ `k`. Space `O(k)`.

---

## ③ Space Optimization

The heap holds at most `k` entries → `O(k)` space, versus the brute force's `O(N)` value array. That's already the frugal option, and since we splice the *existing* nodes into the result (no new nodes allocated), there's no output overhead beyond the pointers.

A genuinely `O(1)`-extra-space alternative is **divide and conquer**: repeatedly merge lists in pairs using the standard two-list merge (which is `O(1)` extra), halving the number of lists each round over `log k` rounds:

```python
def merge_two(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next

def merge_k_lists_dc(lists):
    if not lists:
        return None
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            a = lists[i]
            b = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(a, b))
        lists = merged
    return lists[0]
```

Same `O(N log k)` time, but `O(1)` auxiliary (ignoring recursion — this version is iterative). Trade-off: divide-and-conquer avoids the heap and its tuple-tiebreaker fiddliness; the heap is more natural when lists **stream** or `k` is huge and you want incremental output.

> The heap is `O(k)`; divide-and-conquer trims that to `O(1)` extra while keeping the same time. Neither re-sorts already-sorted data, which is the whole win over brute force.

---

## Java (for Java interviewers)

```java
import java.util.PriorityQueue;

public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> heap =
        new PriorityQueue<>((a, b) -> a.val - b.val);   // min-heap by value
    for (ListNode node : lists)
        if (node != null) heap.offer(node);

    ListNode dummy = new ListNode(), tail = dummy;
    while (!heap.isEmpty()) {
        ListNode node = heap.poll();                    // smallest head
        tail.next = node;
        tail = tail.next;
        if (node.next != null) heap.offer(node.next);
    }
    return dummy.next;
}
```

*(Java's `PriorityQueue` compares nodes via the comparator on `val`, so there's no tuple-comparison pitfall — no tiebreaker index needed.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Flatten + sort | O(N log N) | O(N) |
| Min-heap of k heads | O(N log k) | O(k) |
| Divide & conquer (pairwise merge) | O(N log k) | O(1) extra |

*(N = total nodes across all lists, k = number of lists.)*

---

## Say it out loud (interview narration)

> *"Flattening and re-sorting is O(N log N) and wastes the fact that each list is already sorted. Instead I keep a min-heap of the k current heads: the global smallest unplaced node is always one of them. I pop the smallest, splice it onto my output, and push its next node back in. The heap never exceeds size k, so it's O(N log k). One gotcha in Python: I include the list index as a tiebreaker in the heap tuple so equal values don't force it to compare ListNode objects. Alternatively, divide-and-conquer merges lists pairwise in log k rounds for the same time with O(1) extra space."*

## Related / follow-ups
- **Merge Two Sorted Lists** (the k = 2 base case)
- **Kth Smallest Element in a Sorted Matrix** (heap over k sorted rows — same idea)
- **Smallest Range Covering Elements from K Lists** (min-heap across k sources)
- **Find K Pairs with Smallest Sums** (heap over sorted streams of pair sums)
