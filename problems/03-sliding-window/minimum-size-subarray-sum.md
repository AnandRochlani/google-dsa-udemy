# Minimum Size Subarray Sum

> **LeetCode:** 209. Minimum Size Subarray Sum · **Difficulty:** 🟡 Medium · **Pattern:** Sliding Window · **Google frequency:** ⭐ high

---

## Problem

Given an array of **positive** integers `nums` and a positive `target`, return the **length of the shortest contiguous subarray** whose sum is **≥ target**. If no such subarray exists, return `0`.

**Example:** `nums = [2, 3, 1, 2, 4, 3]`, `target = 7` → `2` *(the subarray `[4, 3]` sums to 7, and nothing shorter reaches 7).*

**Constraints that matter:** `n` up to ~10⁵ → `O(n²)` (~10¹⁰) is too slow, we want `O(n)`. Crucially, **all values are positive** — that's the property that makes the window trick valid (adding an element only ever *increases* the sum, removing one only ever *decreases* it).

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For every starting index, keep adding elements to the right until the running sum hits `target`, record that length, then try the next start." That's the brute force — try all subarrays.
- **Where it hurts:** Start at index 0, you extend `[2] → [2,3] → [2,3,1] → [2,3,1,2]` to reach 7 (length 4). Now start at index 1 and you throw *all that away* and rebuild `[3] → [3,1] → ...`. But you already knew the sum of `[3,1,2]` from the previous pass — you're recomputing overlapping subarrays from scratch.
- **The leap:** Here the answer window's **size isn't fixed** — that's the twist versus LC 643. So use a **variable-size (dynamic) window** with two moving pointers, `left` and `right`. **Grow** the window by advancing `right` and adding elements until the sum is `≥ target`. The moment it is, **shrink** from the `left` — remove elements as long as the sum *stays* `≥ target`, recording the length each time — because a shorter window with the same property is strictly better. Then keep growing again. Each pointer only ever moves *forward*.
- **Why positivity matters:** because every number is positive, growing the window strictly increases the sum and shrinking strictly decreases it. That monotonic behaviour is what lets us confidently shrink: once the sum drops below `target`, we *must* grow again — no risk that a removed element was secretly making things worse. (With negatives, this breaks, and you'd need prefix sums + a deque or binary search.)
- **Pattern trigger:** **"shortest / longest subarray satisfying a condition" + values that make the condition monotonic** → **dynamic Sliding Window** (grow-then-shrink, two pointers moving one direction).

---

## ① Brute Force

Try every start; extend right until the sum reaches `target`; track the shortest.

```python
def min_subarray_len_brute(target, nums):
    n = len(nums)
    best = float("inf")
    for start in range(n):
        total = 0
        for end in range(start, n):
            total += nums[end]
            if total >= target:
                best = min(best, end - start + 1)
                break            # can't get shorter from this start
    return best if best != float("inf") else 0
```

**Why it's the natural first attempt:** it's the direct "check every subarray" reading — for each start, find the earliest end that works.

**Why it's not enough:** the outer loop is `n` starts, the inner loop can extend up to `n` elements, and consecutive starts re-sum overlapping stretches you already saw. That's `O(n²)` — billions of operations at `n = 10⁵` → **Time Limit Exceeded.**

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

One dynamic window. Grow with `right`, and whenever the sum is big enough, shrink from `left` while recording the best length.

```python
def min_subarray_len(target, nums):
    left = 0
    window_sum = 0
    best = float("inf")
    for right in range(len(nums)):
        window_sum += nums[right]           # grow: add the new right element
        while window_sum >= target:         # shrink while still valid
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1
    return best if best != float("inf") else 0
```

**Walk the example** `nums = [2, 3, 1, 2, 4, 3]`, `target = 7`:

| right (val) | window_sum after add | shrink? | window during shrink | best |
|---|---|---|---|---|
| 0 (2) | 2 | no | `[2]` | ∞ |
| 1 (3) | 5 | no | `[2,3]` | ∞ |
| 2 (1) | 6 | no | `[2,3,1]` | ∞ |
| 3 (2) | 8 | yes → drop 2 (sum 6) | record len 4 `[2,3,1,2]` | 4 |
| 4 (4) | 6 + 4 = 10 | yes → drop 3 (7), drop 1 (6) | record len 4 `[3,1,2,4]`, then len 3 `[1,2,4]` | 3 |
| 5 (3) | 6 + 3 = 9 | yes → drop 2 (7), drop 4 (3) | record len 3 `[2,4,3]`, then len 2 `[4,3]` | **2** |

Answer: `2`. ✅

**Why it's correct:** the `while` loop shrinks the window to the *smallest* size that still satisfies `sum ≥ target` for the current `right`, and records the length at each valid step. Because all values are positive, once `window_sum` drops below `target` no further shrink can bring it back — so we've found the shortest window ending at (or before) `right`. Doing this for every `right` covers every position. `left` and `right` each advance at most `n` times total.

**Complexity:** Time `O(n)` (each index is added once and removed once — amortised O(1) per step), Space `O(1)`.

---

## ③ Space Optimization

Already optimal on space — **and here's why.** We hold three scalars: `left`, `window_sum`, and `best`. No hash map, no prefix array, nothing that scales with `n`. That's `O(1)`.

> A **prefix-sum + binary-search** solution also solves this in `O(n log n)` time but needs an `O(n)` prefix array. The sliding window is *both faster (O(n)) and lighter (O(1))* here — so unless the array had negatives (which would break the monotonic shrink), there's no reason to prefer it. Say that trade-off out loud.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
public int minSubArrayLen(int target, int[] nums) {
    int left = 0, windowSum = 0, best = Integer.MAX_VALUE;
    for (int right = 0; right < nums.length; right++) {
        windowSum += nums[right];              // grow
        while (windowSum >= target) {          // shrink while valid
            best = Math.min(best, right - left + 1);
            windowSum -= nums[left];
            left++;
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Optimised (dynamic window) | O(n) | O(1) |
| Prefix sum + binary search | O(n log n) | O(n) |

---

## Say it out loud (interview narration)

> *"Brute force checks every subarray — O(n²), too slow. But the window size here isn't fixed, so I use a dynamic window with two pointers: I grow to the right adding elements until the sum hits target, then I shrink from the left as long as it stays valid, recording the shortest length each time. This works because all values are positive — adding only grows the sum, removing only shrinks it — so the shrink is safe. Each pointer moves forward at most n times, so it's O(n) time, O(1) space. If there were negatives I'd fall back to prefix sums plus a deque."*

## Related / follow-ups
- **Maximum Average Subarray I** (LC 643 — fixed window instead of variable)
- **Longest Substring Without Repeating Characters** (LC 3 — dynamic window, shrink on a violation)
- **Minimum Window Substring** (LC 76 — dynamic window with need/have counts)
- **Subarray Sum Equals K** (LC 560 — has negatives, so window breaks → prefix-sum hash map)
