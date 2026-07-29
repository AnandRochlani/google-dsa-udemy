# 3Sum

> **LeetCode:** 15. 3Sum · **Difficulty:** 🟡 Medium · **Pattern:** Two Pointers · **Google frequency:** ⭐ high

---

## Problem

Given an integer array `nums`, return **all unique triplets** `[a, b, c]` such that `a + b + c == 0`. The same triplet must not appear twice in the answer (order within a triplet doesn't matter for uniqueness).

**Example:** `nums = [-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]` *(both sum to 0; note `-1` is reused across different triplets but each triplet is listed once).*

**Constraints that matter:** `n` can be up to ~3000. A cubic O(n³) triple loop is ~2.7×10¹⁰ operations → too slow. We need O(n²). Also: **duplicate handling** is half the problem — the array can contain repeats and we must not emit the same triplet twice.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "Try every group of three and keep the ones that sum to zero." Three nested loops. That's the brute force, and it's O(n³).
- **Where it hurts:** the innermost loop is doing a *linear search* for "the third number that makes this sum zero" — over and over, from scratch, ignoring any structure. That's the same wasted re-scanning we kill in every two-pointer problem. Plus you have to dedup triplets afterward, which is fiddly.
- **The leap (two moves):** First, **sort the array.** Sorting is cheap (O(n log n)) and unlocks everything. Second, realize 3Sum is really **"fix one number, then 2Sum the rest."** If I pin `nums[i]`, I need two other numbers summing to `-nums[i]`. On a *sorted* subarray, that 2Sum is the classic two-pointer squeeze — O(n) instead of O(n²) hashing/looping. Fixing each of the `n` elements and doing an O(n) squeeze gives O(n²) total. Sorting also makes **dedup trivial**: identical values sit next to each other, so I just skip over neighbors I've already used.
- **Pattern trigger:** **"find a combination summing to a target" + duplicates to manage** → **sort, fix the outer element(s), two-pointer the inner search.** This "reduce k-Sum to (k-1)-Sum by fixing one" idea generalizes to 4Sum and beyond.

---

## ① Brute Force

Three nested loops over all triplets; dedup with a set of sorted tuples.

```python
def three_sum_brute(nums):
    n = len(nums)
    result = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    result.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in result]
```

**Why it's the natural first attempt:** "all triplets that sum to zero" reads literally as three nested loops.

**Why it's not enough:** O(n³) blows up at n=3000 (~2.7×10¹⁰ checks → TLE). The set-of-tuples also spends extra memory just to fight duplicates, a problem sorting would have solved for free.

**Complexity:** Time `O(n³)`, Space `O(n)` (for the dedup set / output).

---

## ② Optimised Solution

Sort. Fix each `nums[i]` as the first element, then two-pointer the rest for `-nums[i]`. Skip duplicates as you go.

```python
def three_sum(nums):
    nums.sort()
    n = len(nums)
    result = []
    for i in range(n - 2):
        if nums[i] > 0:                 # smallest is positive → no zero-sum possible
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue                    # skip duplicate anchor
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                # skip duplicate seconds / thirds
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1               # need a bigger sum
            else:
                right -= 1              # need a smaller sum
    return result
```

**Walk the example.** Sorted: `[-4, -1, -1, 0, 1, 2]`.

| i (val) | target = -val | left..right squeeze | triplet |
|---|---|---|---|
| 0 (-4) | 4 | pairs top out at 1+2=3 < 4 → none | — |
| 1 (-1) | 1 | (0=-1)+(5=2)=1 ✅ → `[-1,-1,2]`; then (2=-1)+(4=1)=0 ✅ → `[-1,0,1]` | 2 found |
| 2 (-1) | — | duplicate anchor, **skip** | — |
| 3 (0) | 0 | (4=1)+(5=2)=3 >0 → shrink, pointers cross | — |

Result: `[[-1, -1, 2], [-1, 0, 1]]`. ✅

**Why it's correct:** for a fixed `i`, the two-pointer squeeze over sorted `nums[i+1..]` finds *every* pair summing to `-nums[i]` and never misses one (same invariant as 2Sum on a sorted array: too-big → move right in, too-small → move left in). Sorting guarantees equal values are adjacent, so the three `skip duplicate` guards ensure each distinct triplet is emitted exactly once. The `nums[i] > 0` break is a shortcut: once the anchor is positive, the two larger numbers can't bring the sum back to zero.

**Complexity:** Time `O(n²)` (an O(n) squeeze for each of n anchors; the sort is O(n log n) and doesn't dominate), Space `O(1)` extra (ignoring the output list).

---

## ③ Space Optimization

Already O(1) auxiliary space — and here's the teaching moment. The brute force needed a **set of tuples** just to suppress duplicate triplets, which costs O(n) memory *and* the overhead of hashing. By **sorting first**, duplicates become adjacent, so a couple of `while … == previous` skips dedup in place with zero extra structures.

> Say it out loud: *"Sorting isn't only for the two-pointer squeeze — it also lets me dedup by skipping neighbors, so I drop the O(n) hash set the brute force needed."*

(The output list itself is unavoidable — it's the answer, not scratch space. In-place sort mutates the input, which is standard and allowed here.)

---

## Java (for Java interviewers)

```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    int n = nums.length;
    for (int i = 0; i < n - 2; i++) {
        if (nums[i] > 0) break;
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int left = i + 1, right = n - 1;
        while (left < right) {
            int total = nums[i] + nums[left] + nums[right];
            if (total == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                left++;
                right--;
                while (left < right && nums[left] == nums[left - 1]) left++;
                while (left < right && nums[right] == nums[right + 1]) right--;
            } else if (total < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (triple loop) | O(n³) | O(n) (dedup set) |
| Optimised (sort + two pointers) | O(n²) | O(1) extra |
| Space-optimised | O(n²) | O(1) extra |

---

## Say it out loud (interview narration)

> *"Brute force is three nested loops, O(n³) — too slow at n=3000, and I'd need a set to dedup. Instead I sort, which is O(n log n) and basically free here. Then I fix each number and reduce the problem to 2Sum on the sorted rest: a two-pointer squeeze that's O(n) per anchor, so O(n²) overall. Sorting also makes dedup easy — I just skip equal neighbors for the anchor and the two pointers, so no hash set and O(1) extra space."*

## Related / follow-ups
- **Two Sum II** (the inner squeeze this problem is built on)
- **3Sum Closest** (track the nearest sum instead of exactly zero)
- **4Sum** (fix two elements, two-pointer the rest — O(n³))
- **3Sum Smaller** (count triplets below a target)
