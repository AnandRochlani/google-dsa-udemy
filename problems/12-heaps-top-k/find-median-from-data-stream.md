# Find Median from Data Stream

> **LeetCode:** 295. Find Median from Data Stream · **Difficulty:** 🔴 Hard · **Pattern:** Heaps & Top-K (two heaps) · **Google frequency:** ⭐ high

---

## Problem

Design a data structure that supports two operations on a stream of integers:
- `addNum(num)` — add an integer to the running data set.
- `findMedian()` — return the median of all elements added so far.

The **median** is the middle value of the sorted data; with an even count it's the average of the two middle values.

**Example:**
```
addNum(1); addNum(2); findMedian() → 1.5
addNum(3);            findMedian() → 2.0
```

**Constraints that matter:** up to `5×10⁴` calls. Re-sorting on every `findMedian` is `O(n log n)` per query — far too slow across many queries. We want `addNum` in `O(log n)` and `findMedian` in `O(1)`, which two heaps deliver.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Keep the numbers in a list, sort when asked for the median." Each query is `O(n log n)` (or `O(n)` to insert into a sorted list). With `5×10⁴` interleaved adds and queries, that's quadratic-ish — too slow.
- **What is a median, really?** It's the boundary between the **smaller half** and the **larger half** of the data. I don't need the whole thing sorted — I only need instant access to the *largest of the small half* and the *smallest of the large half*.
- **The leap (two heaps):** keep two halves.
  - A **max-heap** (largest on top) holds the **smaller half** — its top is the biggest of the small numbers.
  - A **min-heap** (smallest on top) holds the **larger half** — its top is the smallest of the large numbers.
  - Keep them **balanced** (equal size, or the max-heap holding one extra). Then the median is either the max-heap's top (odd total) or the average of the two tops (even total) — `O(1)`.
- **The balancing dance:** to add a number, push it into one heap, then move the offending top across so ordering (`every small ≤ every large`) and the size invariant both hold. Each `addNum` is `O(log n)`; `findMedian` is `O(1)`.
- **Python detail:** `heapq` is a min-heap only, so simulate the max-heap by **negating** values on the way in and out.
- **Pattern trigger:** **"running median / keep track of a middle boundary in a stream"** → **two heaps, a max-heap for the low half and a min-heap for the high half, kept balanced.**

---

## ① Brute Force

Store everything; sort (or keep sorted) and read the middle on each query.

```python
import bisect

class MedianFinderBrute:
    def __init__(self):
        self.data = []                       # kept sorted

    def addNum(self, num):
        bisect.insort(self.data, num)        # O(n) shift to keep sorted

    def findMedian(self):
        n = len(self.data)
        mid = n // 2
        if n % 2:
            return float(self.data[mid])
        return (self.data[mid - 1] + self.data[mid]) / 2
```

**Why it's the natural first attempt:** the median is defined off the sorted order, so keeping the data sorted and indexing the middle is the literal implementation.

**Why it's not enough:** `bisect.insort` is `O(n)` per add because inserting into a Python list shifts elements. Across `n` adds that's `O(n²)`. (Plain "append then sort on query" is even worse — `O(n log n)` per query.)

**Complexity:** `addNum` `O(n)`, `findMedian` `O(1)`; overall `O(n²)`. Space `O(n)`.

---

## ② Optimised Solution

Two heaps: a max-heap `low` (smaller half) and a min-heap `high` (larger half).

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.low = []    # max-heap (store negated): smaller half
        self.high = []   # min-heap: larger half

    def addNum(self, num):
        # 1) push onto low (max-heap), then hand its top to high
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # 2) rebalance so low is never smaller than high (low holds the extra)
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])              # odd total: low has the middle
        return (-self.low[0] + self.high[0]) / 2    # even total: average the tops
```

**Why this exact sequence balances correctly:** every `addNum` pushes to `low`, then pops `low`'s max into `high` (guaranteeing `max(low) ≤ min(high)` — the ordering invariant). That can leave `high` one bigger, so the final `if` moves `high`'s min back to `low`. Net effect: sizes stay equal or `low` has exactly one extra.

**Walk it** — add `1, 2, 3`:

- `add(1)`: push `-1`→low `[-1]`; pop→push to high `[1]`; high bigger→move back → low `[-1]`, high `[]`. Median = `-low[0] = 1.0`.
- `add(2)`: push `-2`→low `[-2,-1]`; pop max (2)→high `[2]`; sizes low 1 / high 1, balanced → low `[-1]`, high `[2]`. Median = `(1 + 2)/2 = 1.5` ✅.
- `add(3)`: push `-3`→low `[-3,-1]`; pop max (3)→high `[2,3]`; high bigger→move min (2) back→ low `[-2,-1]`, high `[3]`. Median = `-low[0] = 2.0` ✅.

**Why it's correct:** the invariants — (1) every element in `low` ≤ every element in `high`, and (2) `len(low) == len(high)` or `len(low) == len(high)+1` — mean `low`'s top is always the lower-middle and `high`'s top the upper-middle. So the median is `low`'s top (odd) or the average of the two tops (even).

**Complexity:** `addNum` `O(log n)` (a constant number of heap ops), `findMedian` `O(1)`. Space `O(n)`.

---

## ③ Space Optimization

You must retain every number to answer future medians — the median of a stream depends on all of it — so `O(n)` space is the floor. The two heaps together hold exactly `n` elements; there's no redundancy to squeeze out.

The interesting *variant* is a follow-up: **if all numbers are in a small bounded range** (e.g. ages 0–100), you can replace the heaps with a **counting/bucket array of size R** and find the median by walking cumulative counts — `O(R)` per query but `O(R)` total space independent of `n`. And if numbers arrive but you only ever need an *approximate* median over a huge stream, reservoir-style sampling trades exactness for sub-linear space. Absent those special conditions, two heaps at `O(n)` space with `O(log n)` add is the optimal exact solution.

> Space is at the `O(n)` floor — an exact streaming median must remember every value; the two heaps store each element exactly once.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Operation | Brute (sorted list) | Two heaps |
|---|---|---|
| `addNum` | O(n) | O(log n) |
| `findMedian` | O(1) | O(1) |
| Space | O(n) | O(n) |

---

## Say it out loud (interview narration)

> *"The median is the boundary between the smaller half and the larger half, so I don't need everything sorted — just the top of each half. I keep two heaps: a max-heap for the lower half so its top is the largest small value, and a min-heap for the upper half so its top is the smallest large value. On each add I push into the max-heap, move its top into the min-heap to preserve ordering, then rebalance so the max-heap holds either an equal count or one extra. Then the median is the max-heap's top for an odd count, or the average of both tops for an even count. That's O(log n) per add and O(1) per query. In Python the max-heap is a min-heap with negated values."*

## Related / follow-ups
- **Sliding Window Median** (two heaps plus lazy deletion as the window moves)
- **IPO** (two heaps: one for affordable projects, one gated by capital)
- **Kth Largest Element in a Stream** (a single size-k heap — the simpler streaming cousin)
