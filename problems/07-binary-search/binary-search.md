# Binary Search (The Canonical Template)

> **LeetCode:** 704. Binary Search · **Difficulty:** 🟢 Easy · **Pattern:** Modified Binary Search · **Google frequency:** ⭐ high

---

## Problem

Given an array of integers `nums` **sorted in ascending order** (all distinct), and a `target`, return the **index** of `target` if it exists, otherwise `-1`.

**Example:** `nums = [-1, 0, 3, 5, 9, 12]`, `target = 9` → `4` *(nums[4] == 9).*
`nums = [-1, 0, 3, 5, 9, 12]`, `target = 2` → `-1` *(not present).*

**Constraints that matter:** `n` up to ~10⁴ here, but the point of the problem is the **explicit requirement: you must run in O(log n).** A linear scan passes the judge, but it's the wrong answer to the *question being asked*. This is the template every other problem in this section reuses — learn it until it's muscle memory.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Walk the array left to right, return the index when I hit the target." That's a linear scan — O(n). Correct, simple, and it *ignores that the array is sorted.*
- **Where it hurts:** Every comparison only rules out **one** element. You look at `nums[0]`, it's not the target, you've eliminated exactly one candidate. With sorted data you can do far better than one-at-a-time.
- **The leap:** Look at the **middle** element. Because the array is sorted, comparing `target` to `nums[mid]` tells you which *half* the answer must be in. If `target < nums[mid]`, everything from `mid` rightward is too big — discard it. One comparison eliminates **half the array**, not one element. Repeat on the surviving half. `n → n/2 → n/4 → …` reaches 1 in **log₂ n** steps.
- **Pattern trigger:** **sorted array + "find a value" / "O(log n) required"** → **Binary Search**. The deeper trigger: any time the search space is **monotonic** (a yes/no or bigger/smaller decision that stays consistent as you move), you can halve it.

---

## ① Brute Force

Scan every element until you find the target.

```python
def search_brute(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1
```

**Why it's the natural first attempt:** it's the literal reading of "find the index of target" — look at each one.

**Why it's not enough:** it's O(n) and throws away the sorted-order gift. More importantly, the problem *demands* O(log n); a linear scan signals you didn't recognize the pattern. On sorted data, one comparison should buy you half the array, not one element.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ② Optimised Solution

Binary search. **Memorize this exact template** — the invariant it maintains is what keeps you off-by-one-safe.

```python
def search(nums, target):
    left, right = 0, len(nums) - 1     # INCLUSIVE bounds: answer is in [left, right]
    while left <= right:               # <= because [x, x] is a valid non-empty range
        mid = left + (right - left) // 2   # avoids overflow; floors toward left
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1             # target is strictly right of mid
        else:
            right = mid - 1            # target is strictly left of mid
    return -1
```

**The three rules that make it bug-proof:**
1. **Inclusive bounds** `[left, right]` — every index in that range is still a live candidate.
2. **`while left <= right`** — when `left == right` the range holds exactly one element, still worth checking. Loop ends only when `left > right` (empty range).
3. **Always move past `mid`** (`mid + 1` / `mid - 1`) — you just checked `mid`, so exclude it. This is what guarantees the range **strictly shrinks** every iteration, so the loop can't spin forever.

**Walk the example** `nums = [-1, 0, 3, 5, 9, 12]`, target `9`:

| left | right | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 3 | 3 < 9 → left = 3 |
| 3 | 5 | 4 | 9 | 9 == 9 → **return 4** ✅ |

Now target `2` (not present):

| left | right | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 3 | 3 > 2 → right = 1 |
| 0 | 1 | 0 | -1 | -1 < 2 → left = 1 |
| 1 | 1 | 1 | 0 | 0 < 2 → left = 2 |
| — | — | — | — | left(2) > right(1) → **return -1** ✅ |

**Why it's correct (loop invariant):** *"If `target` is in the array, it is always within `[left, right]`."* Initially that's the whole array. Each branch only discards a side that provably **cannot** contain the target (everything ≤ `mid` when `nums[mid] < target`, etc.), so the invariant holds after every step. The range strictly shrinks, so we either land on the target or the range empties out — and an empty range means it was never there.

**Complexity:** Time `O(log n)`, Space `O(1)`.

---

## ③ Space Optimization

Already optimal — **O(1) space.** The iterative version keeps only two integer indices (`left`, `right`); nothing grows with the input.

> A recursive binary search reads elegantly but costs **O(log n) stack space** for the call frames. The iterative template is strictly cheaper on memory for the same time complexity — prefer it, and say so out loud.

---

## Java (for Java interviewers)

```java
public int search(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;   // avoid int overflow
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (linear scan) | O(n) | O(1) |
| Optimised (binary search, iterative) | O(log n) | O(1) |
| Recursive binary search | O(log n) | O(log n) stack |

---

## Say it out loud (interview narration)

> *"A linear scan is O(n), but the array's sorted and the problem wants O(log n). So I binary-search: I keep an inclusive `[left, right]` window, check the middle, and since the data's sorted, one comparison tells me which half to throw away. I always move mid+1 or mid-1 so the window strictly shrinks — that's what avoids off-by-one bugs and infinite loops. It's O(log n) time, O(1) space with the iterative form."*

## Related / follow-ups
- **First Bad Version** (boundary search — find the leftmost true)
- **Search in Rotated Sorted Array** (binary search with a twist)
- **Search a 2D Matrix** (flatten the index, same template)
- **Find First and Last Position of Element** (lower/upper bound variants)
