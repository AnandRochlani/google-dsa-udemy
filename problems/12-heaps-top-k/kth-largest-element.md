# Kth Largest Element in an Array

> **LeetCode:** 215. Kth Largest Element in an Array · **Difficulty:** 🟡 Medium · **Pattern:** Heaps & Top-K · **Google frequency:** ⭐ high

---

## Problem

Given an integer array `nums` and an integer `k`, return the **kth largest** element — the element that would sit at index `k-1` if the array were sorted in descending order. Note: it's the kth largest in *sorted order*, not the kth distinct value.

**Example:** `nums = [3,2,1,5,6,4]`, `k = 2` → `5` *(sorted desc: 6, 5, ... → 2nd is 5).*
`nums = [3,2,3,1,2,4,5,5,6]`, `k = 4` → `4`.

**Constraints that matter:** `n` up to `10⁵`, and `1 ≤ k ≤ n`. Sorting is `O(n log n)` and works fine, but if you only need *one* rank, you can beat it: a size-`k` heap gives `O(n log k)`, and quickselect gives `O(n)` average.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Sort descending, grab index `k-1`." Simple, correct, `O(n log n)`. Nothing wrong — but you sorted all `n` elements to answer a question about *one* of them.
- **Where it hurts:** you don't care about the full order. You only care about the boundary between the top `k` and the rest. Fully sorting is doing far more work than the question needs.
- **The leap (min-heap of size k):** a **min-heap** is a structure whose *smallest* element is always instantly available at the top (Python's `heapq` is a min-heap). Keep a heap of exactly the `k` largest elements seen so far. Its top is the *smallest of those k* — which, once you've processed everything, is precisely the kth largest overall. For each new number, if it's bigger than the heap's top, it belongs in the top-k, so evict the top and push it. Each push/pop is `O(log k)`, so total `O(n log k)`.
- **The even-faster option (quickselect):** partition the array around a pivot like quicksort, but only recurse into the side that contains rank `k`. Average `O(n)`, though worst case `O(n²)`.
- **Pattern trigger:** **"I need the top K / the kth something, not a full ordering"** → **a heap of size K** (`O(n log k)`), or **quickselect** when you want average `O(n)` and can accept the worst case.

---

## ① Brute Force

Sort and index.

```python
def find_kth_largest_sort(nums, k):
    nums.sort(reverse=True)     # descending
    return nums[k - 1]
```

**Why it's the natural first attempt:** "kth largest" maps directly onto "sort, then count from the top." It's the answer you'd reach for in three seconds.

**Why it's not enough:** it fully orders all `n` elements — `O(n log n)` — to extract a single rank. For large `n` with small `k` (say the 5th largest of a million numbers), that's wasteful; a heap does asymptotically less work.

**Complexity:** Time `O(n log n)`, Space `O(1)` (or `O(n)` depending on the sort).

---

## ② Optimised Solution

Maintain a min-heap holding the `k` largest elements seen so far.

```python
import heapq

def find_kth_largest(nums, k):
    heap = []                       # min-heap; heap[0] is the smallest kept
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:           # keep only the k largest
            heapq.heappop(heap)     # drop the smallest of them
    return heap[0]                  # smallest of the top k == kth largest
```

*(Even cleaner as a one-liner: `heapq.nlargest(k, nums)[-1]`, which uses this same size-k heap under the hood.)*

**Walk the example** `nums = [3,2,1,5,6,4]`, `k = 2`:

| num | push → heap | size > k? pop | heap after |
|---|---|---|---|
| 3 | [3] | no | [3] |
| 2 | [2,3] | no | [2,3] |
| 1 | [1,3,2] | yes → pop 1 | [2,3] |
| 5 | [2,3,5] | yes → pop 2 | [3,5] |
| 6 | [3,5,6] | yes → pop 3 | [5,6] |
| 4 | [4,6,5] | yes → pop 4 | [5,6] |

Final heap `[5,6]`, top `heap[0] = 5` → **`5`** ✅.

**Why it's correct:** the heap always contains exactly the `k` largest elements processed so far. Anything smaller than the current top can't be in the top-k, so evicting the top on overflow never discards a real answer. At the end, the top is the smallest of the `k` largest — the kth largest.

**Complexity:** Time `O(n log k)`, Space `O(k)`.

---

## ③ Space Optimization

The heap costs `O(k)` — genuinely small when `k ≪ n`, and the whole point of the size-`k` heap over sorting. If you're allowed to mutate the input and want *time* optimality, **quickselect** runs in average `O(n)` with `O(1)` extra space:

```python
import random

def find_kth_largest_quickselect(nums, k):
    target = len(nums) - k          # index of kth largest in ascending order
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        pivot = nums[random.randint(lo, hi)]
        # 3-way partition around pivot
        lt, gt, i = lo, hi, lo
        while i <= gt:
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

Quickselect is `O(n)` average, `O(n²)` worst case (mitigated by the random pivot), and `O(1)` extra space. The trade-off to state out loud: **heap = O(n log k) time but stable and worst-case-safe; quickselect = O(n) average but O(n²) worst case and it mutates the array.** In an interview, offer the heap as the safe default and quickselect as the "if you want average linear time" upgrade.

> The heap's `O(k)` space is the price of not sorting; quickselect trades it down to `O(1)` at the cost of a bad worst case.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Sort | O(n log n) | O(1)–O(n) |
| Min-heap of size k | O(n log k) | O(k) |
| Quickselect | O(n) avg, O(n²) worst | O(1) |

---

## Say it out loud (interview narration)

> *"Sorting and indexing is O(n log n), but I only need one rank, not the whole order. So I keep a min-heap of the k largest elements seen so far: push each number, and if the heap exceeds size k, pop the smallest. At the end the heap's top is the smallest of the top k — exactly the kth largest — in O(n log k) time and O(k) space. If they want average linear time and I can mutate the array, I'd switch to quickselect: partition around a random pivot and recurse only into the side holding rank k, O(n) average and O(1) space, with the caveat of an O(n²) worst case."*

## Related / follow-ups
- **Top K Frequent Elements** (heap by frequency, or bucket sort)
- **K Closest Points to Origin** (heap by distance)
- **Kth Largest Element in a Stream** (the heap shines when data arrives online)
- **Median of Two Sorted Arrays** (a different kind of order statistic)
