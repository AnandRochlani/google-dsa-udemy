# Maximum Average Subarray I

> **LeetCode:** 643. Maximum Average Subarray I · **Difficulty:** 🟢 Easy · **Pattern:** Sliding Window · **Google frequency:** medium

---

## Problem

You're given an array of integers `nums` and a number `k`. Find the **contiguous subarray of exactly `k` elements** that has the largest average, and return that average.

**Example:** `nums = [1, 12, -5, -6, 50, 3]`, `k = 4` → `12.75` *(the window `[12, -5, -6, 50]` sums to 51, and 51 / 4 = 12.75 — the best of any 4-in-a-row).*

**Constraints that matter:** `n` can be up to ~10⁵, and `1 ≤ k ≤ n`. Recomputing the sum of every window from scratch is `O(n·k)` — that's up to ~10¹⁰ operations and times out. We need `O(n)`. Also note: values can be **negative**, so you can't assume more elements = bigger sum.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "The average of a fixed-size window is just its sum divided by `k`, and `k` is fixed — so I really just need the window with the **biggest sum**. Let me slide a window of size `k` across the array, and for each position add up its `k` numbers and track the max." That's the brute force.
- **Where it hurts:** Look at two neighbouring windows. Window starting at index 0 is `[1, 12, -5, -6]`. Window starting at index 1 is `[12, -5, -6, 50]`. They **share three of their four elements** (`12, -5, -6`). But the brute force re-adds all four every single time. You're recomputing the overlap over and over — that's the wasted work.
- **The leap:** Don't rebuild the sum — **update** it. When the window slides one step right, exactly one element **leaves** on the left and one **enters** on the right. So `new_sum = old_sum - nums[left_that_left] + nums[right_that_entered]`. Two arithmetic operations instead of `k`. The shared middle never gets touched.
- **Pattern trigger:** **"contiguous subarray of a fixed size `k`" + something additive (sum/average)** → **fixed-size Sliding Window.** The recognition cue is the phrase *"exactly k"* (or *"of size k"*). Compute the first window once, then roll it.

---

## ① Brute Force

For every possible start position, add up the `k` elements and keep the best sum.

```python
def find_max_average_brute(nums, k):
    best = float("-inf")
    for start in range(len(nums) - k + 1):
        window_sum = 0
        for i in range(start, start + k):   # re-add all k elements
            window_sum += nums[i]
        best = max(best, window_sum)
    return best / k
```

**Why it's the natural first attempt:** it's the literal reading of the problem — "look at every window of size `k`, pick the biggest average."

**Why it's not enough:** the inner loop redoes `k` additions for each of the ~`n` windows, and consecutive windows overlap in `k-1` elements you keep re-summing. That's `O(n·k)`. On a 10⁵-element array with `k` in the tens of thousands, it's billions of operations → **Time Limit Exceeded.**

**Complexity:** Time `O(n·k)`, Space `O(1)`.

---

## ② Optimised Solution

Compute the first window's sum once. Then slide: subtract the element that leaves, add the element that enters.

```python
def find_max_average(nums, k):
    window_sum = sum(nums[:k])      # first window, computed once
    best = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]  # add new, drop old
        best = max(best, window_sum)
    return best / k
```

**Walk the example** `nums = [1, 12, -5, -6, 50, 3]`, `k = 4`:

| step | element entering (idx) | element leaving (idx) | window | window_sum | best |
|---|---|---|---|---|---|
| init | — | — | `[1,12,-5,-6]` | 2 | 2 |
| right=4 | 50 (idx 4) | 1 (idx 0) | `[12,-5,-6,50]` | 2 + 50 − 1 = 51 | 51 |
| right=5 | 3 (idx 5) | 12 (idx 1) | `[-5,-6,50,3]` | 51 + 3 − 12 = 42 | 51 |

Best sum is `51`, so the answer is `51 / 4 = 12.75`. ✅

**Why it's correct:** the window always holds exactly `k` consecutive elements. Sliding one step removes exactly the element now behind the window (`nums[right - k]`) and adds exactly the new front element (`nums[right]`) — so `window_sum` is always the true sum of the current window. Since `k` is constant, the largest sum gives the largest average. Negative numbers are handled naturally: we never assume growth, we just track the running max.

**Complexity:** Time `O(n)` (one pass, O(1) work per step), Space `O(1)`.

---

## ③ Space Optimization

Already optimal on space — **and worth saying why.** We only keep two numbers: the running `window_sum` and the `best` seen so far. Nothing grows with the input; there's no hash map, no extra array, no prefix-sum table. So it's `O(1)` space.

> A **prefix-sum array** is a valid alternative (`prefix[i]` = sum of the first `i` elements, then any window sum is a subtraction of two prefix values). It's also `O(n)` time — but it costs `O(n)` extra space for the prefix array. The sliding window gets the same time for `O(1)` space, so here it's strictly better. Naming that trade-off is the strong-hire signal.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
public double findMaxAverage(int[] nums, int k) {
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += nums[i];  // first window
    int best = windowSum;
    for (int right = k; right < nums.length; right++) {
        windowSum += nums[right] - nums[right - k];    // add new, drop old
        best = Math.max(best, windowSum);
    }
    return (double) best / k;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n·k) | O(1) |
| Optimised (sliding window) | O(n) | O(1) |
| Prefix sum | O(n) | O(n) |

---

## Say it out loud (interview narration)

> *"Since `k` is fixed, biggest average just means biggest sum of `k` in a row. Brute force sums every window from scratch — O(n·k), too slow at 10⁵. But neighbouring windows overlap in k−1 elements, so instead of re-adding I slide: subtract the element that leaves, add the one that enters — two operations per step, O(n) total. I only keep a running sum and a max, so it's O(1) space. I'd mention prefix sums as an alternative, but they'd cost O(n) memory for the same time."*

## Related / follow-ups
- **Maximum Sum Subarray of Size K** (return the sum instead of the average — identical mechanics)
- **Minimum Size Subarray Sum** (LC 209 — the window *size* varies, so it's a dynamic window)
- **Sliding Window Maximum** (LC 239 — fixed window but you track the max *element*, needs a deque)
- **Maximum Average Subarray II** (LC 644 — length *at least* k, needs binary search on the answer)
