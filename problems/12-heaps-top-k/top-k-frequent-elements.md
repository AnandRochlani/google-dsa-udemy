# Top K Frequent Elements

> **LeetCode:** 347. Top K Frequent Elements · **Difficulty:** 🟡 Medium · **Pattern:** Heaps & Top-K · **Google frequency:** ⭐ high

---

## Problem

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer may be returned in any order, and it's guaranteed to be unique.

**Example:** `nums = [1,1,1,2,2,3]`, `k = 2` → `[1, 2]` *(1 appears 3×, 2 appears 2×, 3 appears 1×).*
`nums = [1]`, `k = 1` → `[1]`.

**Constraints that matter:** `n` up to `10⁵`, and the problem explicitly nudges you: *"your algorithm must be better than O(n log n)."* That rules out "count, then fully sort by frequency" as the intended answer and points at a heap (`O(n log k)`) or bucket sort (`O(n)`).

---

## 🧠 Intuition — how you'd actually arrive at this

- **Step one is forced:** you need each element's frequency, so build a count map in one `O(n)` pass. No way around that.
- **First instinct for step two:** sort the distinct elements by frequency and take the top `k`. That's `O(m log m)` where `m` = distinct elements — the very `O(n log n)`-ish cost the problem tells you to beat.
- **The leap (heap of size k):** you only want the `k` most frequent, not a full ranking by frequency. Keep a **min-heap** — a structure whose *smallest* item sits at the top — keyed on frequency, capped at size `k`. The top is the least-frequent of your current top-k; when a more frequent element shows up, evict the top. That's `O(m log k)`.
- **The even-cleaner leap (bucket sort):** frequencies are bounded — an element can appear at most `n` times. So make `n+1` buckets indexed by frequency, drop each element into `bucket[freq]`, then walk buckets from high to low collecting until you have `k`. No comparisons, no log factor → `O(n)`.
- **Pattern trigger:** **"top K by some score"** → **count, then a size-K heap** (`O(n log k)`); and when the score is a **small bounded integer** (like a frequency ≤ n), **bucket sort** removes the log entirely → `O(n)`.

---

## ① Brute Force

Count frequencies, then fully sort the distinct elements by frequency and slice the top `k`.

```python
from collections import Counter

def top_k_frequent_sort(nums, k):
    count = Counter(nums)
    # sort distinct elements by frequency, descending
    ordered = sorted(count.keys(), key=lambda x: count[x], reverse=True)
    return ordered[:k]
```

**Why it's the natural first attempt:** "most frequent" reads as "sort by frequency and take the top few." It's correct and easy.

**Why it's not enough:** the sort is `O(m log m)` in the number of distinct elements `m` (up to `n`), i.e. `O(n log n)` — exactly what the problem asks you to beat. You're fully ordering when you only need the top `k`.

**Complexity:** Time `O(n log n)`, Space `O(n)`.

---

## ② Optimised Solution

Count, then keep a min-heap of size `k` keyed on frequency.

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)                       # O(n)
    heap = []                                   # min-heap of (freq, element)
    for element, freq in count.items():
        heapq.heappush(heap, (freq, element))
        if len(heap) > k:                       # keep only k most frequent
            heapq.heappop(heap)                 # evict lowest frequency
    return [element for freq, element in heap]
```

**Walk the example** `nums = [1,1,1,2,2,3]`, `k = 2`:

- `count = {1:3, 2:2, 3:1}`.
- Push `(3,1)` → heap `[(3,1)]`. Push `(2,2)` → `[(2,2),(3,1)]`. Push `(1,3)` → size 3 > 2 → pop smallest `(1,3)` → heap `[(2,2),(3,1)]`.
- Result elements: `[2, 1]` → **`[1, 2]`** (any order accepted) ✅.

**Why it's correct:** the heap holds the `k` highest-frequency elements seen so far; since it's ordered by `freq`, the top is always the weakest of the kept set, so evicting it on overflow never drops a true top-k element.

**Complexity:** Time `O(n + m log k)` (count + heap over `m ≤ n` distinct elements), Space `O(n)`.

---

## ③ Space Optimization

Space is dominated by the count map, which is `O(m)` distinct elements — unavoidable, since you must know every element's frequency. The heap adds only `O(k)`.

If you want to also **drop the `log k` from the time**, use **bucket sort** — frequencies are integers in `[1, n]`, so they can be bucketed instead of compared:

```python
from collections import Counter

def top_k_frequent_buckets(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
    for element, freq in count.items():
        buckets[freq].append(element)

    result = []
    for freq in range(len(nums), 0, -1):           # high frequency → low
        for element in buckets[freq]:
            result.append(element)
            if len(result) == k:
                return result
    return result
```

This is `O(n)` time and `O(n)` space — strictly better on time than the heap, at the cost of allocating `n+1` buckets. The honest trade-off: **heap = O(n log k) time, O(k) auxiliary; bucket sort = O(n) time but O(n) buckets.** When `k` is tiny relative to `n`, the heap's memory edge can matter; when you want guaranteed linear time, buckets win.

> The count map is the `O(n)` floor either way; the choice is heap (less memory, a log factor) vs. buckets (linear time, more memory).

---

## Java (for Java interviewers)

```java
import java.util.*;

public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> count = new HashMap<>();
    for (int n : nums) count.merge(n, 1, Integer::sum);

    // min-heap by frequency
    PriorityQueue<int[]> heap =
        new PriorityQueue<>((a, b) -> a[1] - b[1]);   // [element, freq]
    for (Map.Entry<Integer, Integer> e : count.entrySet()) {
        heap.offer(new int[]{e.getKey(), e.getValue()});
        if (heap.size() > k) heap.poll();
    }

    int[] result = new int[k];
    for (int i = 0; i < k; i++) result[i] = heap.poll()[0];
    return result;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Count + full sort | O(n log n) | O(n) |
| Count + size-k heap | O(n + m log k) | O(n) |
| Count + bucket sort | O(n) | O(n) |

*(m = number of distinct elements, ≤ n.)*

---

## Say it out loud (interview narration)

> *"First I count frequencies in one pass — that part's forced. Then I don't want to fully sort by frequency, since that's the O(n log n) they told me to beat. So I keep a min-heap of size k keyed on frequency: push each distinct element, and when the heap exceeds k, evict the lowest-frequency one. That's O(n + m log k). If they want strict linear time, I'd bucket sort instead — frequencies are bounded by n, so I drop each element into bucket[freq] and scan buckets from high to low until I've collected k. That's O(n) time, trading the log factor for n buckets of memory."*

## Related / follow-ups
- **Kth Largest Element** (size-k heap for a single rank)
- **K Closest Points to Origin** (heap by distance)
- **Sort Characters By Frequency** (same count-then-order idea)
- **Top K Frequent Words** (add lexicographic tie-breaking)
