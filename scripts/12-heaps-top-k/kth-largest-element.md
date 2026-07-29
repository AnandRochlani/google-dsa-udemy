# 🎬 Recording Script — Kth Largest Element in an Array
**Pattern: Heaps & Top-K · LeetCode 215 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the heap chapter opener.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a million numbers streaming down the screen. A caption: "Find the 5th largest." Then a full sort animation churns through all million — a spinner, "sorting 1,000,000…".]**

> Google asks: *"Find the kth largest number in this array."* The fifth largest out of a million.
>
> Your hand goes straight to `sort`, grab index k. It works. It's also doing something faintly absurd — putting a *million* numbers in perfect order just to answer a question about *one* of them.
>
> There's a structure that keeps only the handful you care about and throws the rest away as it goes. It's called a heap, and by the end of this video it'll be your reflex for anything that smells like "top K." Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: tiles `3 2 1 5 6 4`, k = 2. Below, sorted descending: `6 5 4 3 2 1`, the `5` circled as "2nd largest".]**

> The problem in one line: **return the kth largest element** — the value that lands at position k in descending order.
>
> Tiny example: `[3, 2, 1, 5, 6, 4]`, k = 2. Sorted big-to-small that's `6, 5, 4…` — the 2nd largest is `5`.
>
> One trap in the wording: it's the kth largest in *sorted order*, not the kth *distinct* value. Duplicates count. Hold onto `5` as our target.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the six tiles fully sorting into `6 5 4 3 2 1`, every element moving, then a finger lands on index 1.]**

> The obvious move: sort descending, return index k-1.
>
> `[3,2,1,5,6,4]` sorts to `[6,5,4,3,2,1]`. Index 1 is `5`. Done — correct.
>
> But watch what we touched. To find one number, we fully ordered *all six* — and positions 3, 4, 5 of that sorted array? We never even looked at them. On a million elements, that's a million-log-million operation to answer a question about the boundary between two groups.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze the sorted array. The top-2 glow green; the bottom-4 fade gray with a label "wasted work". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste: I only care about the boundary between the top k and everything below. The exact ordering *within* the losers is irrelevant — I sorted it for nothing.
>
> **LEARNER:** Okay, but to *know* which k are the winners, don't I have to compare against everything anyway? How do I keep just the top k without sorting to find them?
>
> **TEACHER:** Exactly the tension. Pause and predict: **what if I held a small container of only k numbers — the k biggest I've seen so far — and each new number either kicks out the weakest one or gets rejected? What structure makes "who's the weakest of my k" instant?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: a small triangle — a heap — with its smallest value sitting at the root (top). New numbers arrive; when the heap exceeds size 2, the root pops off and rolls away.]**

> **TEACHER:** Meet the **min-heap.** Picture a little triangle where the *smallest* element is always sitting right at the top, instantly available. Python's `heapq` is exactly this. Push and pop each cost O(log k) — cheap when k is small.
>
> Now the trick. Keep a min-heap holding only the **k largest numbers seen so far.** Its top is the *smallest of those k.*
>
> **LEARNER:** Wait — why would I want a *min*-heap to track the *largest* elements? That feels backwards.
>
> **TEACHER:** It's the clever part. The top of the min-heap is the weakest member of my elite club. When a new number arrives bigger than that weakest member, it deserves in — so I pop the weakling and push the newcomer. Anything smaller than the top can't belong in the top k, so I reject it. The top is my *bouncer.*
>
> And here's the payoff: once every number has been processed, the smallest of the k largest *is* the kth largest overall. The bouncer is the answer.

---

## 6. THE KEY MOVE (signaling) — `4:25`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Keep a min-heap of size k. Its top = the kth largest."]**

> Burn this in: **keep a size-k min-heap of the largest elements; the top is the kth largest.** Push everything, pop whenever the heap exceeds k, and the survivor sitting at the root is your answer.
>
> Cost: O(n log k) instead of O(n log n). When k is tiny and n is huge, that's a landslide.

---

## 7. CODE IT — LIVE & CHUNKED — `5:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1.]**

> `heapq` is Python's min-heap. Start empty.

```python
import heapq

def find_kth_largest(nums, k):
    heap = []                       # min-heap; heap[0] is the smallest kept
```

> **[VISUAL: chunk 2, highlight the overflow pop.]** Push each number; if the club grows past k, evict the weakest.

```python
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:           # keep only the k largest
            heapq.heappop(heap)     # drop the smallest of them
```

> **[VISUAL: chunk 3.]** The top is the answer.

```python
    return heap[0]                  # smallest of the top k == kth largest
```

> And if you want the one-liner in the room: `heapq.nlargest(k, nums)[-1]` — same size-k heap underneath.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> Walk the *why*.
>
> `heappush` then the size check — we let the heap momentarily hit k+1, then immediately pop the smallest. That "push then trim" keeps exactly the k largest at all times.
>
> **LEARNER:** Why push *first* and then check size? Why not check if the number even deserves to be added before pushing?
>
> **TEACHER:** You *can* — compare `num > heap[0]` first and only push-pop if so. It saves a few operations. But "push then trim if over k" is one fewer branch to get wrong under pressure, and it's the same O(log k). Both are fine; I teach the simpler one.
>
> `heap[0]` — in a min-heap the root is index 0, always the smallest. After processing everything, that smallest-of-the-k-largest is precisely the kth largest. No final sort needed.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: `[3,2,1,5,6,4]`, k=2, a trace table; the heap drawn as a tiny triangle updating each row.]**

> Run it, k = 2.

| num | push → heap | size > 2? pop | heap after |
|---|---|---|---|
| 3 | [3] | no | [3] |
| 2 | [2,3] | no | [2,3] |
| 1 | [1,3,2] | yes → pop 1 | [2,3] |
| 5 | [2,3,5] | yes → pop 2 | [3,5] |
| 6 | [3,5,6] | yes → pop 3 | [5,6] |
| 4 | [4,6,5] | yes → pop 4 | [5,6] |

> Final heap `[5,6]`, top `heap[0] = 5` → **`5`.** ✅ Exactly the target we circled at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:45`
*(transfer to interview)*

**[VISUAL: "Sort: O(n log n). Heap: O(n log k). Quickselect: O(n) avg."]**

> Out loud: *"Sorting is O(n log n) for a single rank. The size-k heap is O(n log k) — n pushes, each O(log k), and O(k) space. When k is much smaller than n, that beats sorting. If they want average linear time and I can mutate the array, I'd reach for quickselect — O(n) average."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:20`
*(depth + honesty)*

**[VISUAL: quickselect partitioning around a pivot; only one side recursed into, the other grayed out.]**

> The heap costs O(k) — small and the whole point over sorting. But if you want *time* optimality and can reorder the input, **quickselect** runs in average O(n) with O(1) extra space:

```python
import random

def find_kth_largest_quickselect(nums, k):
    target = len(nums) - k          # index of kth largest in ascending order
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        pivot = nums[random.randint(lo, hi)]
        lt, gt, i = lo, hi, lo
        while i <= gt:              # 3-way partition around pivot
            if nums[i] < pivot:
                nums[lt], nums[i] = nums[i], nums[lt]; lt += 1; i += 1
            elif nums[i] > pivot:
                nums[gt], nums[i] = nums[i], nums[gt]; gt -= 1
            else:
                i += 1
        if target < lt:      hi = lt - 1
        elif target > gt:    lo = gt + 1
        else:                return nums[target]
```

> Say the trade-off out loud: **heap = O(n log k), stable, worst-case-safe; quickselect = O(n) average but O(n²) worst case, and it mutates the array.** Offer the heap as the safe default, quickselect as the "if you want average linear" upgrade. And the heap is the *only* option if the numbers *stream in* and you can't hold them all.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Kth Largest Element in a Stream (LC 703)". A blank editor.]**

> Before the next video, try **Kth Largest Element in a Stream.** Numbers arrive one at a time and you answer "kth largest so far" after each. This is where the size-k heap *shines* — quickselect can't do it, because you never have the whole array at once. You already have the core; just keep the heap alive across calls.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Top K ≠ full sort.** You only need the boundary, not the order.
> 2. **Size-k MIN-heap tracks the k LARGEST** — its top is the bouncer and the answer.
> 3. **O(n log k) heap vs. O(n) quickselect** — know both, and when each wins.
>
> The peg: **"I only need the top K" → reach for a size-K heap.**

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: tiles `1 1 1 2 2 3` with little count badges: 1×3, 2×2, 3×1. A blurred title: "Top K Frequent Elements".]**

> We ranked numbers by their *value.* But what if you have to rank them by something you compute first — like how *often* each one appears? "Give me the two most frequent." Now the heap has to be keyed on a count, not the number itself — and there's an even sneakier O(n) trick when the score is a bounded integer. That's the next one: Top K Frequent Elements. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.PriorityQueue;

public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();   // min-heap by default
    for (int num : nums) {
        heap.offer(num);
        if (heap.size() > k) heap.poll();                  // drop smallest
    }
    return heap.peek();                                    // kth largest
}
```
