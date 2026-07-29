# Search in Rotated Sorted Array

> **LeetCode:** 33. Search in Rotated Sorted Array · **Difficulty:** 🟡 Medium · **Pattern:** Modified Binary Search · **Google frequency:** ⭐ high

---

## Problem

A sorted array of **distinct** integers was **rotated** at some unknown pivot (e.g. `[0,1,2,4,5,6,7]` becomes `[4,5,6,7,0,1,2]`). Given the rotated array `nums` and a `target`, return its index, or `-1`. Must run in **O(log n)**.

**Example:** `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0` → `4`.
`nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 3` → `-1`.

**Constraints that matter:** `n` up to ~5000, but the problem **explicitly demands O(log n)** — so a linear scan is disqualified even though it'd pass the judge. The array is *almost* sorted: it's two sorted runs glued together. The whole trick is exploiting that.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "It's not fully sorted, so I can't binary search — just scan it." O(n). Works, but ignores the demand for O(log n) and the fact that the array is *mostly* ordered.
- **Where it hurts:** Plain binary search breaks because `nums[mid]` compared to `target` no longer tells you which half to keep — the rotation scrambled that. You feel stuck because the global sorted-ness is gone.
- **The leap:** Look closer at any `mid`. Split the array at `mid` into `[left..mid]` and `[mid..right]`. **At least one of those halves is still fully sorted** — the pivot can only sit in one of them. You can *detect* which half is sorted with a single comparison (`nums[left] <= nums[mid]` means the left half is clean). And once you know a half is sorted, you know its exact value range, so you can test in O(1) whether `target` lies inside it. If it does, search there; if not, search the other half.
- **Pattern trigger:** **rotated / partially-sorted array + O(log n)** → **binary search where each step first decides which half is monotonic.** The transferable idea: you don't need the *whole* space sorted, only enough local structure to eliminate half.

---

## ① Brute Force

Ignore the structure and scan.

```python
def search_brute(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```

**Why it's the natural first attempt:** the array "looks unsorted," so linear search feels like the only safe option.

**Why it's not enough:** O(n), and it explicitly violates the required O(log n). It leaves the two-sorted-runs structure completely unused.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ② Optimised Solution

Same `[left, right]` inclusive template as canonical binary search — but each iteration first figures out which half is sorted.

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        # Which half is sorted?
        if nums[left] <= nums[mid]:            # LEFT half [left..mid] is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1                # target is inside the sorted left half
            else:
                left = mid + 1                 # must be in the right half
        else:                                  # RIGHT half [mid..right] is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1                 # target is inside the sorted right half
            else:
                right = mid - 1                # must be in the left half
    return -1
```

**Why `nums[left] <= nums[mid]` (with `<=`):** when the window narrows to a single element, `left == mid`, and `nums[left] <= nums[mid]` is trivially true — correctly treating that trivial half as "sorted." Using `<` there would misclassify the edge case.

**Walk the example** `nums = [4, 5, 6, 7, 0, 1, 2]`, target `0`:

| left | right | mid | nums[mid] | sorted half | target in it? | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left [4..7] sorted | 0 in [4,7)? no | left = 4 |
| 4 | 6 | 5 | 1 | left [0..1] sorted (nums[4]=0 ≤ 1) | 0 in [0,1)? yes | right = 4 |
| 4 | 4 | 4 | 0 | — | nums[mid]==0 | **return 4** ✅ |

**Why it's correct (loop invariant):** *"if `target` exists, it's in `[left, right]`."* Each step identifies a **provably sorted** half whose full value range is known from its two endpoints, then keeps or discards it based on a range check that cannot be wrong. So we never drop the half that contains the target, and the window strictly shrinks each iteration.

**Complexity:** Time `O(log n)`, Space `O(1)`.

---

## ③ Space Optimization

Already **O(1)** — two indices, iterative loop, nothing scales with `n`. There's no auxiliary structure to trim.

> A common alternative is a two-pass approach: first binary-search for the pivot, then binary-search the correct run. Same O(log n) time and O(1) space, but two passes and more edge cases. The single-pass version above is cleaner — say you prefer it for fewer moving parts.

---

## Java (for Java interviewers)

```java
public int search(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[left] <= nums[mid]) {                 // left half sorted
            if (nums[left] <= target && target < nums[mid]) right = mid - 1;
            else left = mid + 1;
        } else {                                       // right half sorted
            if (nums[mid] < target && target <= nums[right]) left = mid + 1;
            else right = mid - 1;
        }
    }
    return -1;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (linear scan) | O(n) | O(1) |
| Optimised (one-pass binary search) | O(log n) | O(1) |
| Find-pivot then search (two-pass) | O(log n) | O(1) |

---

## Say it out loud (interview narration)

> *"Plain binary search breaks because the array's rotated — comparing target to mid doesn't tell me which side to keep. But here's the key: at any mid, one of the two halves is still fully sorted, and I can tell which by comparing nums[left] to nums[mid]. Once I know the sorted half's exact range, I check in O(1) whether the target falls inside it — if yes I go there, if no I go the other way. That's still halving each step, so O(log n) time, O(1) space."*

## Related / follow-ups
- **Search in Rotated Sorted Array II** (LC 81 — with duplicates; worst case degrades to O(n))
- **Find Minimum in Rotated Sorted Array** (LC 153 — locate the pivot itself)
- **Binary Search** (LC 704 — the clean template this builds on)
