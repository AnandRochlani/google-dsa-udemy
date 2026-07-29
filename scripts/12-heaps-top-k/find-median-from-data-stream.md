# 🎬 Recording Script — Find Median from Data Stream
**Pattern: Heaps & Top-K (two heaps) · LeetCode 295 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** single size-k heap; the negate-for-max-heap trick (K Closest).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: sensor readings streaming in endlessly. After each one a label updates: "median so far → ?". A naive version re-sorts the whole history each time, visibly lagging.]**

> Google systems-design flavor: *"Numbers arrive in a never-ending stream. At any moment, tell me the median of everything so far."*
>
> The obvious version re-sorts the whole history on every query. With fifty thousand interleaved adds and queries, that grinds to a halt.
>
> The elegant answer is one of the most satisfying ideas in this whole course: you split the data into two halves and guard the border with *two* heaps facing each other. The median is always sitting right where they touch. Let me show you. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: "addNum(1); addNum(2); findMedian() → 1.5" then "addNum(3); findMedian() → 2.0". A sorted strip [1,2] with the gap between them marked, then [1,2,3] with 2 circled.]**

> Two operations to design: **`addNum(x)`** drops a number into the running set, **`findMedian()`** returns the current median — the middle of the sorted data, or the *average* of the two middles when the count is even.
>
> Add 1, add 2 → sorted `[1,2]`, even count → median is the average, `1.5`. Add 3 → `[1,2,3]`, odd count → the middle, `2.0`. Hold both cases.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a growing sorted list; each addNum inserts into place with elements shifting right; then a finger reads the middle.]**

> The literal reading: keep the data sorted, read the middle on demand. Insert 1. Insert 2 — fine. Insert a number that belongs at the front — every element shifts right to make room.
>
> **[VISUAL: an insertion near the front pushes a long row of elements over by one.]**
>
> That shift is O(n) *per add* — inserting into a sorted array or list means moving everything after the insertion point. Across n adds, O(n squared). The median read is instant, but the *maintenance* is what kills us.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The sorted strip, with only the two middle elements highlighted; everything else dimmed. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the realization: to report the median, I don't actually need the whole thing sorted. I only need instant access to *two* values — the largest of the smaller half, and the smallest of the larger half. Everything else can stay unsorted.
>
> **LEARNER:** "Largest of the small half" and "smallest of the large half"… we have structures that hand you exactly those in O(1). A max-heap gives the largest, a min-heap the smallest.
>
> **TEACHER:** You're already there. Pause and predict: **if I split the numbers into a smaller half and a larger half, which heap holds which — and if I keep them balanced in size, where does the median live?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it)*

**[VISUAL: two triangle heaps meeting at a center line. Left: a MAX-heap (biggest at the top, pointing right at the border). Right: a MIN-heap (smallest at the top, pointing left at the border). The two tops kiss in the middle.]**

> **TEACHER:** Two heaps, back to back.
>
> A **max-heap** holds the **smaller half** — its top is the *biggest* of the small numbers, pressed right up against the middle.
>
> A **min-heap** holds the **larger half** — its top is the *smallest* of the large numbers, pressed against the middle from the other side.
>
> Keep them **balanced**: equal sizes, or let the max-heap carry one extra. Now the median is trivial. Even total → the two tops straddle the center, average them. Odd total → the max-heap has the extra element, and its top *is* the median.
>
> **LEARNER:** But when a new number comes in, how do I know which half it belongs to — and how do the sizes stay balanced?
>
> **TEACHER:** That's the whole dance, and there's a clean trick so you never have to *decide*. Push the newcomer into the max-heap, immediately hand the max-heap's top over to the min-heap — that guarantees ordering, every small ≤ every large. Then if the min-heap got too big, hand its top back. Two pushes, one conditional. The number auto-sorts into the right side. And Python's `heapq` is min-only, so the max-heap is a min-heap of *negated* values — the trick from K Closest.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Max-heap = small half, min-heap = large half, kept balanced. Median lives where they meet."]**

> The key move: **two heaps — a max-heap for the low half, a min-heap for the high half, kept balanced — and the median is always at the border where their tops meet.**

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1.]**

> Two heaps. `low` is the max-heap — we store negated values. `high` is the plain min-heap.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.low = []    # max-heap (store negated): smaller half
        self.high = []   # min-heap: larger half
```

> **[VISUAL: chunk 2, the balancing dance, highlight the two heappush lines.]** Add: push into `low`, shove `low`'s top across to `high`, then rebalance.

```python
    def addNum(self, num):
        # 1) push onto low (max-heap), then hand its top to high
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # 2) rebalance so low is never smaller than high (low holds the extra)
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))
```

> **[VISUAL: chunk 3.]** Median: if `low` has the extra, its top; else average the two tops.

```python
    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])              # odd total: low has the middle
        return (-self.low[0] + self.high[0]) / 2    # even total: average the tops
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:40`
*(elaboration — why each line exists)*

**[VISUAL: full class; animate the three-step add on one number.]**

> Walk the *why* — the `addNum` sequence is the whole puzzle.
>
> `heappush(low, -num)` — the newcomer enters the low half (negated, because `low` is a max-heap faked with a min-heap).
>
> `heappush(high, -heappop(low))` — immediately move `low`'s current maximum into `high`. This is the ordering guarantee: after it, *every* value in `low` is ≤ *every* value in `high`. We don't decide which half num belongs to — we let this shuffle sort it out.
>
> **LEARNER:** Hold on — if every add pushes to `low` then moves one to `high`, doesn't `low` end up empty and `high` holding everything?
>
> **TEACHER:** That's exactly what the `if` fixes. After the shuffle, `high` might be one bigger than `low`. The final line moves `high`'s smallest back to `low`. Net effect over the whole operation: sizes end equal, or `low` ends with exactly one extra. `low` is never *smaller* than `high` — which is why odd-count medians live at `low`'s top.
>
> `findMedian` reads that invariant: `low` bigger → odd count, its top is the middle; equal → even count, average both tops. The `float(...)` and `/2` keep it a proper decimal.

---

## 9. DRY-RUN THE CODE — `9:30`
*(worked example — prove it, close the loop)*

**[VISUAL: the two heaps side by side; each add animates push → transfer → rebalance; tops highlighted.]**

> Add 1, 2, 3.

| add | push low | move max → high | rebalance | low / high | median |
|---|---|---|---|---|---|
| 1 | [-1] | high [1], low [] | high bigger → move back | low [-1], high [] | -low[0] = **1.0** |
| 2 | [-2,-1] | pop 2 → high [2] | equal, no move | low [-1], high [2] | (1+2)/2 = **1.5** |
| 3 | [-3,-1] | pop 3 → high [2,3] | high bigger → move 2 back | low [-2,-1], high [3] | -low[0] = **2.0** |

> Medians: 1.0, then 1.5, then 2.0 — exactly the cases we set up. ✅ Every add is a constant number of heap operations. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `11:15`
*(transfer to interview)*

**[VISUAL: "Sorted list: add O(n), find O(1). Two heaps: add O(log n), find O(1)."]**

> Out loud: *"The sorted-list version is O(n) per add because of shifting — O(n squared) overall. Two heaps make `addNum` O(log n) — a constant number of pushes and pops — and `findMedian` O(1), just reading the two tops. Space is O(n), since I must retain every number. In Python the max-heap is a min-heap of negated values."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `12:00`
*(depth + honesty)*

**[VISUAL: the two heaps together labeled "exactly n elements, no redundancy". Then a small bucket array labeled "if values are bounded, O(R)".]**

> Space is O(n) and that's the floor — an *exact* streaming median depends on every value ever seen, so you must remember them all. The two heaps together hold exactly n elements; nothing is duplicated.
>
> Two variants worth naming, because knowing the boundary is a skill. **One:** if all numbers fall in a small bounded range — say ages 0 to 100 — replace the heaps with a **counting/bucket array of size R** and find the median by walking cumulative counts: O(R) per query but O(R) space *independent of n.* **Two:** if you only need an *approximate* median over a massive stream, reservoir sampling trades exactness for sub-linear space. Absent those conditions, two heaps at O(n) space with O(log n) add is the optimal exact solution.

---

## 12. YOUR TURN (active recall) — `12:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Sliding Window Median (LC 480)". A blank editor.]**

> Before the next video, try **Sliding Window Median.** Same two heaps, but now numbers *leave* as the window slides — so you need "lazy deletion": mark a value removed and only actually evict it when it surfaces at a heap top, rebalancing by count as you go. It's the two-heap idea under real pressure. Give it a genuine fight.

---

## 13. LOCK IT IN — `13:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **The median only needs the border** — largest of the low half, smallest of the high half.
> 2. **Two heaps: max-heap = low half, min-heap = high half, kept balanced.** `addNum` O(log n), `findMedian` O(1).
> 3. **The push-transfer-rebalance dance** auto-sorts each number into the right side.
>
> The peg: **running median → two heaps back to back, median lives where they meet.**

---

## 14. CLIFFHANGER — `13:55`
*(open loop to next lesson)*

**[VISUAL: CPU task icons A A A B B B with cooldown gaps; a clock ticking through idle slots. A blurred title: "Task Scheduler".]**

> Heaps have been about *finding* the extreme — the kth, the closest, the median. But they also power *greedy scheduling*: when you must repeatedly grab the "most urgent" item, run it, and put it on cooldown, a max-heap of counts is the engine. And then — plot twist — you'll see the whole thing collapse into a single line of arithmetic. That's the finale of the chapter: Task Scheduler. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.*;

class MedianFinder {
    // low: max-heap (smaller half), high: min-heap (larger half)
    private final PriorityQueue<Integer> low  = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Integer> high = new PriorityQueue<>();

    public void addNum(int num) {
        low.offer(num);
        high.offer(low.poll());              // hand low's max to high
        if (high.size() > low.size())
            low.offer(high.poll());          // keep low >= high in size
    }

    public double findMedian() {
        if (low.size() > high.size())
            return low.peek();               // odd total
        return (low.peek() + high.peek()) / 2.0;
    }
}
```
