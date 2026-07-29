# Sort Colors

> **LeetCode:** 75. Sort Colors · **Difficulty:** 🟡 Medium · **Pattern:** Two Pointers · **Google frequency:** ⭐ high

---

## Problem

You're given `nums` containing only `0`, `1`, and `2` (representing red, white, blue). Sort them **in place** so all `0`s come first, then all `1`s, then all `2`s. You may not use a library sort, and the classic ask is to do it in **one pass** with **O(1)** space.

**Example:** `nums = [2, 0, 2, 1, 1, 0]` → `[0, 0, 1, 1, 2, 2]`.

**Constraints that matter:** only **three** distinct values, must be **in place** (O(1) space), and ideally **one pass**. "Three values only" is the special structure — it's why we can beat a general comparison sort and even beat the obvious counting two-pass.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "Just sort it." `nums.sort()` — O(n log n). Or, smarter, since there are only three values: **count** how many 0s, 1s, 2s, then overwrite the array with that many of each. That counting version is O(n) but it's **two passes** (count, then fill).
- **Where it hurts:** the two-pass counting sort reads the whole array once just to tally, then writes it once. It works and it's O(n)/O(1), but the interviewer's follow-up is always *"can you do it in a single pass?"* You're touching each element twice when the values are so few you could place each one the instant you see it.
- **The leap:** partition the array into **three regions** as you sweep, using three pointers. `low` = the boundary just past the finalized 0s; `high` = the boundary just before the finalized 2s; `mid` = the current element under inspection. As `mid` scans: a `0` belongs at the front → swap it down to `low` and advance both; a `2` belongs at the back → swap it up to `high` and shrink `high` (but **don't** advance `mid` — the swapped-in value is unexamined); a `1` is already in the middle zone → just advance `mid`. When `mid` passes `high`, everything's placed. This is the **Dutch National Flag** algorithm (Dijkstra).
- **Pattern trigger:** **partition in place around a small fixed set of categories (≤3)** → **three pointers carving regions in one pass.** The signal is "few distinct buckets, sort/partition in place, one pass."

---

## ① Brute Force

Counting sort: tally each value, then overwrite. Correct, O(n), but **two passes**.

```python
def sort_colors_brute(nums):
    counts = [0, 0, 0]
    for x in nums:          # pass 1: count
        counts[x] += 1
    i = 0
    for val in range(3):    # pass 2: fill
        for _ in range(counts[val]):
            nums[i] = val
            i += 1
```

**Why it's the natural first attempt:** with only three values, counting-then-filling is the obvious O(n) idea, and it's genuinely good.

**Why it's not enough:** it reads the array twice. The canonical interview follow-up demands a **single pass**, which counting sort can't give you.

**Complexity:** Time `O(n)` (two passes), Space `O(1)`.

---

## ② Optimised Solution — Dutch National Flag

Three pointers, one pass. `low`/`high` bound the unsorted middle; `mid` inspects.

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # note: do NOT advance mid — re-inspect the swapped-in value
```

**Walk the example** `[2, 0, 2, 1, 1, 0]` (start `low=0, mid=0, high=5`):

| nums | low | mid | high | nums[mid] | action |
|---|---|---|---|---|---|
| `[2,0,2,1,1,0]` | 0 | 0 | 5 | 2 | swap mid↔high, high→4 |
| `[0,0,2,1,1,2]` | 0 | 0 | 4 | 0 | swap mid↔low, low→1, mid→1 |
| `[0,0,2,1,1,2]` | 1 | 1 | 4 | 0 | swap mid↔low, low→2, mid→2 |
| `[0,0,2,1,1,2]` | 2 | 2 | 4 | 2 | swap mid↔high, high→3 |
| `[0,0,1,1,2,2]` | 2 | 2 | 3 | 1 | mid→3 |
| `[0,0,1,1,2,2]` | 2 | 3 | 3 | 1 | mid→4 |
| `[0,0,1,1,2,2]` | 2 | 4 | 3 | — | mid > high → stop |

Result: `[0, 0, 1, 1, 2, 2]`. ✅

**Why it's correct — the invariant:** at all times `nums[0..low-1]` are all `0`, `nums[low..mid-1]` are all `1`, and `nums[high+1..]` are all `2`. The zone `nums[mid..high]` is the unknown region shrinking to nothing. On a `0` we grow the 0-block; on a `2` we grow the 2-block and re-examine the newcomer (which is why `mid` doesn't advance); a `1` is already correct. When `mid > high` the unknown region is empty → fully sorted.

**Complexity:** Time `O(n)` (single pass), Space `O(1)`.

---

## ③ Space Optimization

Already O(1) space — three integer pointers, all swaps in place, nothing grows with `n`. The real upgrade here isn't space (both approaches are O(1)); it's cutting **two passes down to one** by placing each element the moment you see it instead of tallying first.

> Say it out loud: *"Both are O(1) space, but Dutch National Flag does it in a single pass — I partition into three regions on the fly instead of counting then refilling."*

---

## Java (for Java interviewers)

```java
public void sortColors(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            int t = nums[low]; nums[low] = nums[mid]; nums[mid] = t;
            low++;
            mid++;
        } else if (nums[mid] == 1) {
            mid++;
        } else { // nums[mid] == 2
            int t = nums[mid]; nums[mid] = nums[high]; nums[high] = t;
            high--;
            // do not advance mid
        }
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (counting, 2 passes) | O(n) | O(1) |
| Optimised (Dutch flag, 1 pass) | O(n) | O(1) |
| Space-optimised | O(n) | O(1) |

*(A library sort would be O(n log n) — worse, and disallowed.)*

---

## Say it out loud (interview narration)

> *"The easy win is counting sort: only three values, so tally them and refill — O(n), O(1), but two passes. To do it in one pass I use the Dutch National Flag: a low pointer for the 0-boundary, a high pointer for the 2-boundary, and a mid pointer scanning. A 0 swaps down to low, a 2 swaps up to high, a 1 stays put. The one subtlety: after swapping a 2 to the back I don't advance mid, because the value I pulled in hasn't been checked yet. One pass, O(1) space."*

## Related / follow-ups
- **Sort Array By Parity** (two-way partition — evens then odds)
- **Move Zeroes** (partition non-zeros forward with a write pointer)
- **Partition Array** (quicksort's Lomuto/Hoare partition — same idea, arbitrary pivot)
- **Wiggle Sort** (in-place rearrangement with position rules)
