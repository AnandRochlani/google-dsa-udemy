# Median of Two Sorted Arrays (Partition Binary Search)

> **LeetCode:** 4. Median of Two Sorted Arrays · **Difficulty:** 🔴 Hard · **Pattern:** Modified Binary Search · **Google frequency:** medium

---

## Problem

Given two sorted arrays `nums1` (size `m`) and `nums2` (size `n`), return the **median** of the combined `m + n` elements. Must run in **O(log(m + n))**.

**Example:** `nums1 = [1, 3]`, `nums2 = [2]` → merged `[1, 2, 3]`, median `2.0`.
`nums1 = [1, 2]`, `nums2 = [3, 4]` → merged `[1, 2, 3, 4]`, median `(2 + 3) / 2 = 2.5`.

**Constraints that matter:** `m + n` up to ~2000, but the problem **explicitly demands O(log(m + n))** — so even an O(m + n) merge is the "wrong" answer to the question asked. The trick isn't finding the merged array; it's finding the right **partition** without merging.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Merge the two sorted arrays (like merge-sort's merge step), then pick the middle." That's O(m + n) time and O(m + n) space — clean and correct, and a fine thing to *state first*.
- **Where it hurts:** The problem wants **O(log(m + n))**. Merging touches every element; we're doing linear work when the inputs are already sorted — the same "sorted input, not exploiting it fully" smell as ordinary binary search.
- **The leap:** The median is defined entirely by a **partition**. Imagine cutting the *combined* sorted order into a **left half** and a **right half** of (nearly) equal size, where **every element on the left ≤ every element on the right**. The median then depends only on the elements *touching the cut*. Crucially, a cut is fully determined by **how many elements we take from `nums1`** — say `i` — because the count from `nums2` is forced: `j = half − i`. So we only need to find the right `i`. And `i` lives in `[0, m]`, a range we can **binary-search**: if the cut is "too far left in nums1" (a left element of nums1 exceeds a right element of nums2), move `i` right; otherwise move it left. Feasibility is monotonic in `i`.
- **Pattern trigger:** **"combine two sorted arrays / find an order-statistic in O(log)"** → **binary-search the partition point of the smaller array.** The transferable idea: don't search for a value or merge — search for the *cut* that balances the two halves.

---

## ① Brute Force

Merge, then index the middle.

```python
def findMedianSortedArrays_brute(nums1, nums2):
    merged = []
    i = j = 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i]); i += 1
        else:
            merged.append(nums2[j]); j += 1
    merged += nums1[i:]
    merged += nums2[j:]

    total = len(merged)
    mid = total // 2
    if total % 2 == 1:
        return float(merged[mid])
    return (merged[mid - 1] + merged[mid]) / 2
```

**Why it's the natural first attempt:** the median is defined on the *merged* array, so merging is the literal reading. Correct and easy to reason about.

**Why it's not enough:** O(m + n) time and O(m + n) space — violates the required O(log(m + n)), and does linear work over already-sorted data.

**Complexity:** Time `O(m + n)`, Space `O(m + n)` (or O(1) extra if you count without materializing).

---

## ② Optimised Solution

Binary-search the partition of the **smaller** array. Four sentinel-guarded border values keep the edge cases (empty side of a cut) clean.

```python
def findMedianSortedArrays(nums1, nums2):
    # Always binary-search the SMALLER array → i range is small, and j stays in bounds.
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    total_left = (m + n + 1) // 2      # size of the combined LEFT half (+1 handles odd total)

    left, right = 0, m                 # i = how many elements we take from nums1: [0, m]
    while left <= right:
        i = left + (right - left) // 2 # cut in nums1: i elements on the left
        j = total_left - i             # cut in nums2 is forced by i

        # Border values around each cut; ±inf sentinels handle empty sides.
        left1  = nums1[i - 1] if i > 0 else float('-inf')
        right1 = nums1[i]     if i < m else float('inf')
        left2  = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j]     if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            # Correct partition found.
            if (m + n) % 2 == 1:
                return float(max(left1, left2))          # odd: median is top of left half
            return (max(left1, left2) + min(right1, right2)) / 2   # even: avg of the two middles
        elif left1 > right2:
            right = i - 1              # took too many from nums1 → move cut LEFT
        else:  # left2 > right1
            left = i + 1               # took too few from nums1 → move cut RIGHT

    return 0.0  # unreachable for valid inputs
```

**The three ideas that make it work:**
1. **Search the smaller array** so `i ∈ [0, m]` is the tighter range and the forced `j = total_left − i` never goes out of `nums2`'s bounds.
2. **±∞ sentinels** let a cut sit at position `0` or `m` (nothing on the left/right of that array) without a pile of special-case `if`s.
3. **The correctness test** `left1 <= right2 and left2 <= right1` says: *every element left of both cuts ≤ every element right of both cuts.* That's exactly the "left half ≤ right half" property the median needs.

**Walk the example** `nums1 = [1, 3]`, `nums2 = [2]`. After the swap-to-smaller step `nums2` is size 1 vs nums1 size 2, so they swap → `nums1 = [2]` (m=1), `nums2 = [1, 3]` (n=2). `total_left = (1 + 2 + 1)//2 = 2`. Search `i ∈ [0, 1]`:

| left | right | i | j = 2−i | left1 | right1 | left2 | right2 | test | action |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 2 | −∞ | 2 | nums2[1]=3 | +∞ | left2(3) ≤ right1(2)? **no** | left = 1 |
| 1 | 1 | 1 | 1 | 2 | +∞ | nums2[0]=1 | nums2[1]=3 | 2≤3 ✓ and 1≤+∞ ✓ | **found** |

Total `m + n = 3` is odd → median `max(left1, left2) = max(2, 1) = 2` → **`2.0`** ✅

**Why it's correct (loop invariant):** the two arrays are sorted, so *within* each array the left border ≤ right border automatically. A partition is valid iff the **cross** conditions also hold (`left1 ≤ right2` and `left2 ≤ right1`). If `left1 > right2`, we took too many small-side elements from `nums1` — the valid `i` is strictly smaller, so `right = i − 1` never discards it (monotonic feasibility). Symmetric for the other branch. The range `[left, right]` always contains the correct `i`; it strictly shrinks; the loop ends exactly when both cross conditions hold.

**Complexity:** Time `O(log(min(m, n)))`, Space `O(1)`.

---

## ③ Space Optimization

Already **O(1)** — we compute only four border values per iteration and never build the merged array. That's the leap over brute force: the median is decided by the **four elements straddling the cut**, so materializing all `m + n` values is pure waste.

> And by binary-searching the *smaller* array, the time bound tightens from O(log(m + n)) to **O(log(min(m, n)))** — a free improvement that also keeps the forced index `j` in bounds. Worth naming out loud.

---

## Java (for Java interviewers)

```java
public double findMedianSortedArrays(int[] nums1, int[] nums2) {
    if (nums1.length > nums2.length) { int[] t = nums1; nums1 = nums2; nums2 = t; }
    int m = nums1.length, n = nums2.length;
    int totalLeft = (m + n + 1) / 2;

    int left = 0, right = m;
    while (left <= right) {
        int i = left + (right - left) / 2;
        int j = totalLeft - i;

        int left1  = (i > 0) ? nums1[i - 1] : Integer.MIN_VALUE;
        int right1 = (i < m) ? nums1[i]     : Integer.MAX_VALUE;
        int left2  = (j > 0) ? nums2[j - 1] : Integer.MIN_VALUE;
        int right2 = (j < n) ? nums2[j]     : Integer.MAX_VALUE;

        if (left1 <= right2 && left2 <= right1) {
            if (((m + n) & 1) == 1) return Math.max(left1, left2);
            return (Math.max(left1, left2) + Math.min(right1, right2)) / 2.0;
        } else if (left1 > right2) {
            right = i - 1;
        } else {
            left = i + 1;
        }
    }
    return 0.0;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (merge) | O(m + n) | O(m + n) |
| Optimised (partition binary search) | O(log(min(m, n))) | O(1) |

---

## Say it out loud (interview narration)

> *"The easy version merges both arrays and takes the middle — O(m+n) time and space. But they want O(log(m+n)), so I don't merge: I look for the partition that splits the combined order into a left and right half where every left element ≤ every right element. A cut is fully determined by how many elements I take from the smaller array, i, and that forces j = half − i. So I binary-search i in [0, m]. I check the four border values around the two cuts: if left1 > right2 I took too many from nums1 and move the cut left, otherwise right. When both cross-conditions hold, the median comes from those four borders. O(log(min(m,n))) time, O(1) space — I use ±infinity sentinels so the empty-side edge cases stay clean."*

## Related / follow-ups
- **Merge Sorted Array** (LC 88 — the merge step this avoids)
- **Kth Smallest Element in a Sorted Matrix** (LC 378 — order statistics via binary search)
- **Find K-th Smallest Pair Distance** (LC 719 — binary search on the answer + partition counting)
