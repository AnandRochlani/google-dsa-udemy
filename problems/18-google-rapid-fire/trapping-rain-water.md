# Trapping Rain Water

> **LeetCode:** 42. Trapping Rain Water · **Difficulty:** 🔴 Hard · **Pattern:** Prefix max arrays → Two Pointers · **Google frequency:** ⭐ high

---

## Problem

Given `n` non-negative integers representing an **elevation map** where each bar has width `1`, compute how much **rain water** it can trap after raining.

**Example:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]` → `6`.
The dips between taller bars fill with water; summing across the map gives 6 units.

**Constraints that matter:** `n` up to `2 × 10⁴`, values up to `10⁵`. An O(n²) "for each bar scan both sides" solution is ~4×10⁸ — risky. The problem is really about a **per-column insight** that unlocks O(n), then a space trick that gets to O(1).

---

## 🧠 Intuition — how you'd actually arrive at this

- **The key per-column insight:** think column by column, not about "pools." The water sitting *above bar `i`* is bounded by the **tallest wall to its left** and the **tallest wall to its right**. Water can rise only as high as the **shorter** of those two walls (the taller one would overflow past the shorter). So:
  `water[i] = min(maxLeft[i], maxRight[i]) − height[i]` (clamped at 0).
  Sum that over all bars.
- **Brute force from the insight:** for each `i`, scan left for its max and right for its max. Correct, but re-scans the whole array for every bar → O(n²).
- **The leap #1 — precompute the walls:** the "tallest to the left" and "tallest to the right" for every index can each be built in **one sweep**. `prefixMax` left-to-right, `suffixMax` right-to-left. Then one more pass applies the formula. Three linear passes → O(n), at the cost of two O(n) arrays.
- **The leap #2 — two pointers, O(1) space:** you don't actually need the full arrays. Walk two pointers inward, tracking `leftMax` and `rightMax` seen so far. **The shorter side is the bottleneck**, so whichever pointer sits at the smaller wall can have its water computed *now* — its answer depends only on the max from its own side, which we already know is the limiting one. Move that pointer inward. This collapses the two arrays into two scalars.
- **Pattern trigger:** *"amount bounded by min of left-max and right-max"* → **prefix/suffix maxima**, then *"the shorter wall decides, so advance it"* → **two pointers, O(1) space**. Same prefix-max idea as Product Except Self, same "move the shorter side" idea as Container With Most Water.

---

## ① Brute Force

For each bar, find the tallest wall on each side by scanning, then apply the formula.

```python
def trap_brute(height):
    n = len(height)
    total = 0
    for i in range(n):
        left_max = max(height[:i+1]) if i >= 0 else 0    # tallest to the left (incl. i)
        right_max = max(height[i:]) if i < n else 0      # tallest to the right (incl. i)
        total += min(left_max, right_max) - height[i]
    return total
```

**Why it's the natural first attempt:** it's the per-column insight written literally — for each bar, look left, look right, take the min minus the bar's own height.

**Why it's not enough:** each of the `n` iterations rescans up to the whole array → **O(n²)**. At n = 2×10⁴ that's ~4×10⁸ operations, and every bar recomputes maxima that overlap its neighbors' — pure redundancy.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution — prefix/suffix max arrays

Precompute, for every index, the max to its left and the max to its right; then one pass sums the trapped water.

```python
def trap_arrays(height):
    n = len(height)
    if n == 0:
        return 0
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    total = 0
    for i in range(n):
        total += min(left_max[i], right_max[i]) - height[i]
    return total
```

**Walk part of the example** `[0,1,0,2,1,0,1,3,2,1,2,1]`:
- `left_max  = [0,1,1,2,2,2,2,3,3,3,3,3]`
- `right_max = [3,3,3,3,3,3,3,3,2,2,2,1]`
- At `i=2` (height 0): `min(1,3) − 0 = 1`. At `i=5` (height 0): `min(2,3) − 0 = 2`. At `i=4` (height 1): `min(2,3) − 1 = 1`... summing all columns gives **6**.

**Why it's correct:** `min(left_max[i], right_max[i])` is the water level the shorter of the two bounding walls permits at column `i`; subtracting `height[i]` gives the water resting on that bar (non-negative because `left_max[i] ≥ height[i]`). Summing over columns totals the trapped water.

**Complexity:** Time `O(n)` (three passes). Space `O(n)` for the two arrays.

---

## ③ Space Optimization — two pointers, O(1)

Replace the two arrays with two pointers and two running maxima. Process whichever side is shorter, because that side's water is already fully determined.

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    total = 0
    while left < right:
        if height[left] < height[right]:
            # left wall is the shorter side → left_max is the true bound here
            left_max = max(left_max, height[left])
            total += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            total += right_max - height[right]
            right -= 1
    return total
```

**Walk it** on `[0,1,0,2,1,0,1,3,2,1,2,1]` (abbreviated):
- `left=0(0), right=11(1)`: `height[left] < height[right]` → `left_max=0`, add `0`, left→1.
- `left=1(1), right=11(1)`: not `<` → `right_max=1`, add `0`, right→10.
- `left=1(1), right=10(2)`: `<` → `left_max=1`, add `0`, left→2.
- `left=2(0)`: `<` → add `left_max−0 = 1`, left→3. (total 1)
- `left=3(2), right=10(2)`: not `<` → `right_max=2`, add `0`, right→9.
- `left=3(2), right=9(1)`: not `<` → add `right_max−1 = 1`, right→8. (total 2)
- ...continuing accumulates the remaining columns to **6**.

**Why it's correct:** when `height[left] < height[right]`, we *know* there exists a wall on the right (at `right`, or taller) that is at least `height[left]`, so the left side's bound is `left_max` regardless of what's further right. Thus the water at `left` is `left_max − height[left]`, computable now. The symmetric argument holds when the right side is the shorter one. Each step finalizes exactly one column and advances one pointer, so no column is missed or double-counted.

**Complexity:** Time `O(n)` (single pass), Space **`O(1)`** (two indices, two maxima).

> This is the answer to give: *"min of left-max and right-max minus the height, and since the shorter wall is always the binding constraint, I walk two pointers inward processing whichever side is lower — O(n) time, O(1) space."*

**Alternative worth naming — a monotonic stack** also solves it in O(n) time / O(n) space by resolving water in horizontal layers as bars pop; the two-pointer version is preferred for its O(1) space.

---

## Java (for Java interviewers)

```java
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0, total = 0;
    while (left < right) {
        if (height[left] < height[right]) {
            leftMax = Math.max(leftMax, height[left]);
            total += leftMax - height[left];
            left++;
        } else {
            rightMax = Math.max(rightMax, height[right]);
            total += rightMax - height[right];
            right--;
        }
    }
    return total;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (scan both sides per bar) | O(n²) | O(1) |
| Prefix + suffix max arrays | O(n) | O(n) |
| Monotonic stack | O(n) | O(n) |
| Two pointers | O(n) | **O(1)** |

---

## Say it out loud (interview narration)

> *"Water above a bar is bounded by the tallest wall on each side, and it can only rise to the shorter of the two — so water at i is min(leftMax, rightMax) minus height[i]. Brute force scans both sides per bar, O(n²). I can precompute leftMax and rightMax in two sweeps for O(n) time but O(n) space. To get O(1), I use two pointers: whichever side currently has the shorter wall is the binding constraint, so I can finalize that column's water from the running max on its side and move that pointer inward. Single pass, O(n) time, O(1) space."*

## Related / follow-ups
- **Container With Most Water** (11) — also "move the shorter wall," but maximizing area, not summing.
- **Product of Array Except Self** (238) — same prefix/suffix precomputation idea.
- **Trapping Rain Water II** (407) — 2-D grid; needs a min-heap (priority queue) from the border inward.
- **Largest Rectangle in Histogram** (84) — the monotonic-stack cousin.
