# Pair with Target Sum (Sorted)

> **LeetCode:** 167. Two Sum II — Input Array Is Sorted · **Difficulty:** 🟢 Easy · **Pattern:** Two Pointers · **Google frequency:** ⭐ high

---

## Problem

Given an array of integers **sorted in ascending order** and a `target`, return the indices of the two numbers that add up to `target`. Exactly one solution exists, and you can't use the same element twice.

**Example:** `arr = [1, 3, 4, 6, 8, 11]`, `target = 10` → `[2, 3]` *(because 4 + 6 = 10).*

**Constraints that matter:** `n` can be up to ~10⁵. That means an O(n²) solution (~10¹⁰ operations) times out — we need O(n log n) or better. And the array is **sorted**, which is the gift the whole optimization hinges on.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each number, look for its partner (`target - num`) somewhere else in the array." The most literal version of that is checking every pair. That's the brute force.
- **Where it hurts:** For each of the `n` elements, you re-scan (almost) the whole array again. You're doing `n × n` work — and you're **completely ignoring that the array is sorted.** Any time a problem hands you sorted input and you don't use the order, that's a red flag you're leaving performance on the table.
- **The leap:** In a sorted array, the smallest number is on the far left and the largest on the far right. Put a pointer on each. Their sum is the *widest possible*. If that sum is **too big**, the only way to shrink it is to move the **right** pointer inward (to a smaller number). If it's **too small**, move the **left** pointer inward (to a bigger number). Each move eliminates an entire set of pairs you'd otherwise have checked.
- **Pattern trigger:** **sorted array + find a pair by value** → **Two Pointers**. Burn that pairing into memory; it's the recognition signal.

---

## ① Brute Force

Check every pair with two nested loops.

```python
def pair_sum_brute(arr, target):
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return [i, j]
    return [-1, -1]
```

**Why it's the natural first attempt:** it's the direct translation of "find two numbers that add up" — try all two-number combinations.

**Why it's not enough:** it does ~n²/2 comparisons and throws away the sorted-order gift. On the 6-element example it's instant; on a 10⁵-element hidden test it's ~5 billion comparisons → **Time Limit Exceeded.**

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

Use the sorted order. One pointer at each end, squeeze inward based on the sum.

```python
def pair_sum(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1      # need a bigger sum
        else:
            right -= 1     # need a smaller sum
    return [-1, -1]
```

**Walk the example** `[1, 3, 4, 6, 8, 11]`, target `10`:

| left (val) | right (val) | sum | action |
|---|---|---|---|
| 0 (1) | 5 (11) | 12 | > 10 → right-- |
| 0 (1) | 4 (8) | 9 | < 10 → left++ |
| 1 (3) | 4 (8) | 11 | > 10 → right-- |
| 1 (3) | 3 (6) | 9 | < 10 → left++ |
| 2 (4) | 3 (6) | 10 | == 10 → **return [2, 3]** ✅ |

**Why it's correct:** when `sum > target`, `arr[right]` is too large to pair with *anything* ≥ `arr[left]`, so discarding it (right--) can't skip a real answer. Symmetric for the left side. The two pointers together traverse the array once.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

Already optimal on space — **and here's the teaching moment.** Contrast the two O(n)-time solutions:

- **Hash-map approach** (the go-to when the array is *unsorted*): one pass, store seen values, look up the complement. **O(n) time but O(n) space.**
- **Two-pointer approach** (this one, valid because the array is *sorted*): **O(n) time, O(1) space** — just two integer indices.

So when the array is sorted, two pointers is *strictly better on memory*. Say it out loud:

> *"Because the array's sorted, I'll use two pointers instead of a hash map — same O(n) time, but O(1) space instead of O(n)."*

That sentence is the strong-hire signal: you didn't just solve it, you picked the cheapest-memory solution.

---

## Java (for Java interviewers)

```java
public int[] pairSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) return new int[]{left, right};
        else if (sum < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Optimised (two pointers) | O(n) | O(1) |
| Hash map (for unsorted input) | O(n) | O(n) |

---

## Say it out loud (interview narration)

> *"Brute force is every pair — O(n²), too slow at 10⁵. But the array's sorted, so I'll put a pointer at each end: if the sum's too big I move the right one in, too small I move the left one in, until they meet. That's O(n) time. And since I only need two indices, it's O(1) space — cheaper than the hash-map version I'd use if it weren't sorted."*

## Related / follow-ups
- **3Sum** (fix one element, two-pointer the rest)
- **Container With Most Water** (move the shorter wall)
- **Valid Palindrome** (two pointers from both ends)
- **Two Sum** (unsorted → hash map instead)
