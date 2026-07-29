# 🎬 Recording Script — Merge k Sorted Lists
**Pattern: Heaps & Top-K · LeetCode 23 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** size-k heap (Kth Largest, K Closest); the tuple-comparison warning from K Closest.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: three sorted linked lists stacked: 1→4→5, 1→3→4, 2→6. Their heads pulse. A single merged list assembles below one node at a time.]**

> A genuine Google Hard, and a favorite: *"Here are k linked lists, each already sorted. Merge them into one sorted list."*
>
> The tempting move — dump everything into an array and sort — works, but it throws away the gift you were handed: each list is *already sorted.* Re-sorting sorted data is like reshuffling a deck someone already put in order.
>
> The elegant answer uses a heap to pick the next-smallest across all k lists in one continuous sweep. And it's where a nasty little Python crash finally shows up — the one I warned you about last lesson. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: lists [[1,4,5],[1,3,4],[2,6]] → [1,1,2,3,4,4,5,6]. Edge cases: [] → [], [[]] → [].]**

> The problem in one line: **merge k sorted linked lists into one sorted linked list; return its head.**
>
> Tiny example: `[1,4,5]`, `[1,3,4]`, `[2,6]` merge to `1,1,2,3,4,4,5,6`. Watch the duplicate 1s and 4s — they'll matter. And mind the empty cases: no lists, or a list that's empty, both give an empty result.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: all 8 values pour into a flat array [1,4,5,1,3,4,2,6]; it churns through a full sort; then rebuilds into a new list.]**

> The brute force: walk every list, dump all values into one array, sort it, build a fresh linked list.
>
> `[1,4,5,1,3,4,2,6]` → sort → `[1,1,2,3,4,4,5,6]` → rebuild. Correct, easy to get right.
>
> But look — we had eight values already arranged in three sorted runs, and we blended and re-sorted them from scratch at O(N log N). We paid full sorting price for data that was *begging* to be merged.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The three list heads (1, 1, 2) glow; a spotlight asks "which is smallest?". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the wasted knowledge: at any moment, the very next value for the merged list is the *smallest of the current heads* — because each list is sorted, nothing behind a head can beat it. I don't need to sort everything; I need to repeatedly find the min among just k candidates.
>
> **LEARNER:** So the real subproblem is "find the smallest among k things, over and over, cheaply." That's... exactly what a heap is for.
>
> **TEACHER:** You just derived it. Pause and predict: **if I put the k list heads in a min-heap, pop the smallest, and append it — what do I have to push back in so the next pop is still correct?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration — derive it)*

**[VISUAL: a small triangle heap holding the three heads (1,1,2). Pop the top 1 → it appends to output → that node's next (4) is pushed back in. The heap re-settles.]**

> **TEACHER:** Put the k heads in a **min-heap** keyed on value. Pop the smallest — that's the next node in the merged list, guaranteed. Then here's the move: push that node's `.next` back into the heap, so the list it came from stays represented.
>
> Pop 1 from list two, append it, push its successor 3. Pop the next smallest, append, push *its* successor. The heap always holds exactly one live candidate per still-nonempty list, and it never grows beyond k.
>
> **LEARNER:** Why does the heap never exceed size k? I keep pushing things in.
>
> **TEACHER:** Because every pop is matched by *at most one* push — the successor. One out, at most one in. Start with k, stay at k. So each operation is O(log k), one per node → **O(N log k)** total. The heap only ranks k things at a time, never all N — that's the whole win over O(N log N).

---

## 6. THE KEY MOVE (signaling) — `4:40`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Min-heap of the k heads. Pop smallest → append → push its .next."]**

> Burn it in: **hold the k current heads in a min-heap; pop the smallest, append it, and push its `.next`.** Repeat until the heap is empty. It's the engine behind external merge sort — how databases merge sorted files too big for memory.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 0 — the node class.]**

> Standard linked-list node.

```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

> **[VISUAL: chunk 1, highlight the tuple `(node.val, i, node)`.]** Seed the heap with the non-empty heads. Note the middle field — I'll explain it in a second; it's load-bearing.

```python
def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:                                # skip empty lists
            heapq.heappush(heap, (node.val, i, node))
```

> **[VISUAL: chunk 2, the dummy head.]** A dummy head makes appending painless.

```python
    dummy = tail = ListNode()
```

> **[VISUAL: chunk 3, the merge loop.]** Pop smallest, splice it on, push its successor.

```python
    while heap:
        val, i, node = heapq.heappop(heap)      # smallest current head
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight the tuple, then the dummy, then the push.]**

> Walk the *why*, and this is where the Hard-ness hides.
>
> The dummy head — a throwaway node so `tail.next = ...` works uniformly from the very first append; we return `dummy.next` at the end, skipping the throwaway.
>
> Now the tuple `(node.val, i, node)`. Why the middle field `i`, the list index?
>
> **LEARNER:** Yeah — why not just `(node.val, node)`? The value is what I'm sorting by.
>
> **TEACHER:** Here's the trap, and it's the one from last lesson coming due. When two nodes have equal values — remember our two 1s — Python's tuple comparison is a tie on the first field, so it *falls through* to compare the next field. With `(val, node)` that next field is a `ListNode` object, and Python doesn't know how to order two ListNodes → `TypeError`, crash. Insert the list index `i` in the middle: it's a unique integer, it breaks every tie *before* Python ever reaches the node, so two nodes are never compared directly. That one integer is the difference between "accepted" and a runtime exception on a duplicate value.
>
> `if node.next: push` — keep the source list alive in the heap. When a list runs dry, we simply stop pushing for it, and it drops out naturally.

---

## 9. DRY-RUN THE CODE — `9:15`
*(worked example — prove it, close the loop)*

**[VISUAL: the heap triangle, tuples shown as (val, i); output list growing to the right.]**

> Run it. Seed heads: `(1,0), (1,1), (2,2)`.

| pop | append | push successor | heap after |
|---|---|---|---|
| (1,0) | 1 | (4,0) | (1,1),(2,2),(4,0) |
| (1,1) | 1 | (3,1) | (2,2),(3,1),(4,0) |
| (2,2) | 2 | (6,2) | (3,1),(4,0),(6,2) |
| (3,1) | 3 | (4,1) | (4,0),(4,1),(6,2) |
| (4,0) | 4 | (5,0) | (4,1),(5,0),(6,2) |
| (4,1) | 4 | — (list 1 ends) | (5,0),(6,2) |
| (5,0) | 5 | — (list 0 ends) | (6,2) |
| (6,2) | 6 | — | empty |

> Output: **`1→1→2→3→4→4→5→6`.** ✅ And notice the two ties on value 1 and value 4 — the index `i` settled them without touching a node. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `11:00`
*(transfer to interview)*

**[VISUAL: "Flatten+sort: O(N log N). Heap: O(N log k). D&C: O(N log k)."]**

> Out loud: *"N is total nodes, k is number of lists. Flatten-and-sort is O(N log N). The heap does one pop and at most one push per node, heap size capped at k, so O(N log k) — a real win when k is much smaller than N. Space is O(k) for the heap. In Python I add a list-index tiebreaker so equal values don't force it to compare ListNode objects."*
>
> That tiebreaker sentence, said unprompted, signals you've actually *run* this in Python — strong-hire texture.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:45`
*(depth + honesty — divide and conquer)*

**[VISUAL: lists pairing up: 4 lists → merge in pairs → 2 → merge → 1, over log k rounds.]**

> The heap is O(k), and we splice *existing* nodes, so no new-node overhead. For O(1) *extra* space, there's **divide and conquer** — merge the lists pairwise like merge sort, halving the count each round over log k rounds:

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

> Same O(N log k) time, O(1) auxiliary, and no heap — so no tuple-tiebreaker fiddliness. Trade-off to voice: **heap shines when lists *stream* or k is huge and you want incremental output; divide-and-conquer is leaner on memory and dodges the comparison pitfall.** Both refuse to re-sort already-sorted data — the whole point.

---

## 12. YOUR TURN (active recall) — `13:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Kth Smallest Element in a Sorted Matrix (LC 378)". A blank editor.]**

> Before the next video, try **Kth Smallest Element in a Sorted Matrix.** Each row is sorted — so it's *k sorted lists in disguise.* Seed a min-heap with the row heads and pop k times, pushing the next element in the row each pop. The exact engine you just built, on a grid. Ten minutes.

---

## 13. LOCK IT IN — `13:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Next merged node = smallest of the k current heads** — a min-heap finds it in O(log k).
> 2. **Pop, append, push its `.next`** — heap stays size k, total O(N log k).
> 3. **Add a tiebreaker index** in Python so equal values never compare raw nodes.
>
> The peg: **k sorted sources → min-heap of the heads; pop the min, push its next.**

---

## 14. CLIFFHANGER — `14:05`
*(open loop to next lesson)*

**[VISUAL: numbers streaming in one at a time; a split screen with TWO heaps facing each other, a dividing line down the middle. A blurred title: "Find Median from Data Stream".]**

> One heap gave us the min or the max on demand. But what if you need the *middle* — the running median — of numbers that never stop arriving, answered instantly after each one? A single heap can't straddle the center. The trick is audacious: run *two* heaps, back to back, a max-heap and a min-heap, balanced so the median is always sitting right where they meet. That's the next Hard: Find Median from Data Stream. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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

*(Java's `PriorityQueue` compares via the comparator on `val`, so there's no tuple-comparison pitfall — no tiebreaker index needed.)*
