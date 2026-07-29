# K Closest Points to Origin

> **LeetCode:** 973. K Closest Points to Origin · **Difficulty:** 🟡 Medium · **Pattern:** Heaps & Top-K · **Google frequency:** ⭐ high

---

## Problem

Given an array of `points` where `points[i] = [xi, yi]` on the 2D plane, and an integer `k`, return the `k` points closest to the origin `(0, 0)`. Distance is the usual Euclidean distance. The answer may be in any order and is guaranteed unique.

**Example:** `points = [[1,3],[-2,2]]`, `k = 1` → `[[-2,2]]` *(dist² = 8 vs 10, so [-2,2] is closer).*
`points = [[3,3],[5,-1],[-2,4]]`, `k = 2` → `[[3,3],[-2,4]]`.

**Constraints that matter:** `n` up to `10⁴`. Sorting all points by distance is `O(n log n)`; a size-`k` heap gives `O(n log k)`, and quickselect gives `O(n)` average. Also key: **never take the square root** — compare `x² + y²` directly, since squaring preserves order and avoids float error.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Compute every point's distance, sort by it, take the first `k`." Correct, `O(n log n)`. But — same story as every top-K problem — you sorted all `n` when you only need the closest `k`.
- **Drop the square root:** distance is `√(x² + y²)`, but `√` is monotonic, so ordering by `x² + y²` gives the identical ranking. Skip the sqrt — it's slower and introduces floating-point imprecision. Compare **squared distances** as integers.
- **The leap (max-heap of size k):** to keep the `k` *closest* points, use a **max-heap** — a structure whose *largest* element is at the top — keyed on squared distance, capped at size `k`. The top is the *farthest* of your current closest-k. When a new point is nearer than that farthest one, evict the top and insert the newcomer. Python's `heapq` is a *min*-heap, so you simulate a max-heap by **negating the distance**. Each op is `O(log k)` → `O(n log k)` total.
- **The faster option (quickselect):** partition points around a pivot distance and recurse only into the half containing rank `k`. `O(n)` average.
- **Pattern trigger:** **"the k closest / smallest by a score"** → **a size-K max-heap** (evict the worst), or **quickselect** for average linear time.

---

## ① Brute Force

Compute squared distance for every point, sort, slice.

```python
def k_closest_sort(points, k):
    points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)   # squared distance
    return points[:k]
```

**Why it's the natural first attempt:** "k closest" reads as "sort by distance, take k." Direct and correct.

**Why it's not enough:** it fully orders all `n` points — `O(n log n)` — when only the closest `k` matter. For small `k` and large `n`, the size-`k` heap does asymptotically less work.

**Complexity:** Time `O(n log n)`, Space `O(1)`–`O(n)`.

---

## ② Optimised Solution

Max-heap of size `k` keyed on (negated) squared distance.

```python
import heapq

def k_closest(points, k):
    heap = []                                   # max-heap via negation
    for x, y in points:
        dist = x * x + y * y                    # squared distance, no sqrt
        heapq.heappush(heap, (-dist, x, y))     # negate → largest dist on top
        if len(heap) > k:                       # keep only k closest
            heapq.heappop(heap)                 # evict the farthest
    return [[x, y] for (_, x, y) in heap]
```

**Walk the example** `points = [[3,3],[5,-1],[-2,4]]`, `k = 2`:

- `[3,3]`: dist² = 18 → push `(-18,3,3)`; heap size 1.
- `[5,-1]`: dist² = 26 → push `(-26,5,-1)`; heap `[(-26,..),(-18,..)]`, size 2.
- `[-2,4]`: dist² = 20 → push `(-20,-2,4)`; size 3 > 2 → pop the max (top = most-negative = `-26`, the farthest at dist² 26) → heap holds `(-20,-2,4)` and `(-18,3,3)`.
- Result: `[[-2,4],[3,3]]` → **`[[3,3],[-2,4]]`** (any order) ✅.

**Why it's correct:** the heap always holds the `k` closest points processed so far; its top is the farthest of them. A new point is only kept if it's closer than that farthest one, so evicting the top never discards a genuinely-closer point.

**Complexity:** Time `O(n log k)`, Space `O(k)`.

---

## ③ Space Optimization

The heap is `O(k)` — the intended small footprint versus sorting's `O(n)`. If you want average `O(n)` *time* with `O(1)` extra space (and may reorder the input), use **quickselect** on squared distance:

```python
import random

def k_closest_quickselect(points, k):
    def dist(p):
        return p[0] ** 2 + p[1] ** 2

    lo, hi = 0, len(points) - 1
    while lo < hi:
        pivot = dist(points[random.randint(lo, hi)])
        i, lt, gt = lo, lo, hi
        while i <= gt:                          # 3-way partition by distance
            d = dist(points[i])
            if d < pivot:
                points[lt], points[i] = points[i], points[lt]; lt += 1; i += 1
            elif d > pivot:
                points[gt], points[i] = points[i], points[gt]; gt -= 1
            else:
                i += 1
        if k <= lt:      hi = lt - 1
        elif k > gt + 1: lo = gt + 1
        else:            break                  # rank k lands in the pivot block
    return points[:k]
```

Trade-off to voice: **heap = O(n log k) time, O(k) space, worst-case-safe; quickselect = O(n) average but O(n²) worst case and it mutates the input.** The heap is also the natural fit if points *stream in* and you can't hold them all. Offer the heap as the default, quickselect as the average-linear upgrade.

> The heap's `O(k)` space is the deliberate cost of not sorting; quickselect trims it to `O(1)` but gives up the safe worst case.

---

## Java (for Java interviewers)

```java
import java.util.PriorityQueue;

public int[][] kClosest(int[][] points, int k) {
    // max-heap by squared distance (largest distance on top)
    PriorityQueue<int[]> heap = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1]));
    for (int[] p : points) {
        heap.offer(p);
        if (heap.size() > k) heap.poll();       // evict the farthest
    }
    int[][] result = new int[k][2];
    for (int i = 0; i < k; i++) result[i] = heap.poll();
    return result;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Sort by distance | O(n log n) | O(1)–O(n) |
| Max-heap of size k | O(n log k) | O(k) |
| Quickselect | O(n) avg, O(n²) worst | O(1) |

---

## Say it out loud (interview narration)

> *"First, I compare squared distances — x² + y² — not the actual distance, since the square root is monotonic and skipping it avoids float error. Sorting is O(n log n), but I only need the closest k, so I keep a max-heap of size k keyed on squared distance. Python's heapq is a min-heap, so I negate the distance to get a max-heap; the top is the farthest of my current k. If a new point is closer than that, I evict the top and insert it. O(n log k) time, O(k) space. If they want average linear time and I can reorder the input, quickselect partitions by distance and recurses into the half with rank k — O(n) average."*

## Related / follow-ups
- **Kth Largest Element** (same size-k heap / quickselect toolkit)
- **Top K Frequent Elements** (heap by frequency)
- **Find K Closest Elements** (closest to a target value in a sorted array — binary search + two pointers)
