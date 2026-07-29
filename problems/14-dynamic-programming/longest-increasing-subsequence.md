# Longest Increasing Subsequence

> **LeetCode:** 300. Longest Increasing Subsequence · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming (+ patience sorting) · **Google frequency:** ⭐ high

---

## Problem

Given an integer array `nums`, return the length of the **longest strictly increasing subsequence**. A subsequence keeps the original order but may drop elements (they need not be contiguous).

**Example:** `nums = [10, 9, 2, 5, 3, 7, 101, 18]` → `4`. One such subsequence is `[2, 3, 7, 18]` (also `[2, 3, 7, 101]`).

**Constraints that matter:** `1 ≤ nums.length ≤ 2500` for the classic version. `O(n²)` (~6M ops) passes here — but the follow-up explicitly asks for **O(n log n)**, and that patience-sorting solution is the reason this problem is famous.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision / subproblem.** Ask a focused question: *"What's the longest increasing subsequence that **ends exactly at index `i`**?"* Call it `dp[i]`. To end at `i`, the element before `nums[i]` in the subsequence is some earlier `nums[j]` with `j < i` and `nums[j] < nums[i]`. So you extend the best such subsequence by one:

> **dp[i] = 1 + max( dp[j] )** over all `j < i` with `nums[j] < nums[i]` (or `dp[i] = 1` if none qualifies).

The answer is `max(dp)` — the LIS can end anywhere.

**(b) Notice overlapping subproblems.** A pure recursion of "best subsequence ending at i" would recompute the same `dp[j]` values across many `i`'s. Storing them removes the repetition.

**(c) Memoization / (d) tabulation.** Because `dp[i]` depends only on smaller indices, just fill the array left to right. That's the `O(n²)` DP: for each `i`, scan all `j < i`.

**(e) The real leap — beat O(n²) with patience sorting → O(n log n).** The `O(n²)` step is "scan back for the best predecessor." Replace it with a clever structure. Maintain an array `tails`, where `tails[k]` = the **smallest possible tail value** of any increasing subsequence of length `k+1` seen so far. Key facts:
- `tails` is always **sorted ascending** (a longer subsequence's minimal tail is ≥ a shorter one's).
- For each new `x`: **binary-search** for the leftmost tail `≥ x` and overwrite it with `x` (keeping tails as small as possible so future elements can extend more). If `x` is bigger than all tails, append it — the LIS just grew.
- The **length of `tails`** is the LIS length. (`tails` itself is *not* a valid subsequence, but its length is correct.)

**State & recurrence (memorize this):**
- **DP state:** `dp[i]` = length of the LIS ending at index `i`; `dp[i] = 1 + max(dp[j] : j<i, nums[j]<nums[i])`; answer `= max(dp)`.
- **Patience invariant:** `tails[k]` = min tail of an increasing subsequence of length `k+1`; answer `= len(tails)`.

---

## ① Brute Force

Try every subsequence (include/exclude each element) and keep the longest increasing one.

```python
def lis_brute(nums):
    def helper(i, prev):
        if i == len(nums):
            return 0
        skip = helper(i + 1, prev)
        take = 0
        if nums[i] > prev:                       # strictly increasing
            take = 1 + helper(i + 1, nums[i])
        return max(skip, take)
    return helper(0, float('-inf'))
```

**Why it's the natural first attempt:** every element is either in the subsequence or not — the direct include/exclude recursion.

**Why it's not enough:** 2ⁿ subsequences, and the same `(i, prev)` states recur. Exponential.

**Complexity:** Time `O(2ⁿ)`, Space `O(n)` (stack).

---

## ② Optimised Solution — O(n²) DP

`dp[i]` = LIS ending at `i`; for each `i`, look back at all valid `j`.

```python
def lis_dp(nums):
    n = len(nums)
    dp = [1] * n                     # each element alone is length 1
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**A small filled table** for `nums = [10, 9, 2, 5, 3, 7, 101, 18]`:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| nums[i] | 10 | 9 | 2 | 5 | 3 | 7 | 101 | 18 |
| dp[i] | 1 | 1 | 1 | 2 | 2 | 3 | 4 | 4 |

`dp[5]=3` from `2→5→7` (or `2→3→7`); `dp[6]=4` extends that with 101. Answer `max(dp) = 4`. ✅

**Why it's correct:** `dp[i]` considers every legal predecessor and takes the longest — since predecessors have smaller indices and are already final, the choice is optimal.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ③ Space Optimization / Speed — O(n log n) patience sorting

The DP space is already `O(n)` and can't drop (the answer needs `max(dp)` across all ends). The bigger win is **cutting the time** with the `tails` array plus binary search:

```python
from bisect import bisect_left

def lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)     # leftmost tail >= x (strictly increasing)
        if i == len(tails):
            tails.append(x)           # x extends the longest subsequence
        else:
            tails[i] = x              # keep tails as small as possible
    return len(tails)
```

**Walk** `[10, 9, 2, 5, 3, 7, 101, 18]` — `tails` after each element:

| x | tails | note |
|---|---|---|
| 10 | [10] | append |
| 9 | [9] | replace 10 |
| 2 | [2] | replace 9 |
| 5 | [2, 5] | append |
| 3 | [2, 3] | replace 5 |
| 7 | [2, 3, 7] | append |
| 101 | [2, 3, 7, 101] | append |
| 18 | [2, 3, 7, 18] | replace 101 |

`len(tails) = 4`. ✅ (Note tails `[2,3,7,18]` is a real LIS here, but in general tails is only guaranteed to have the *right length*, not to be an actual subsequence.)

**Why it's correct:** `bisect_left` finds the shortest subsequence whose tail is ≥ `x` and lowers that tail to `x`, which can only help future extensions; appending when `x` exceeds all tails is the only way the LIS length grows.

**Complexity:** Time `O(n log n)`, Space `O(n)`.

> For **strictly** increasing use `bisect_left`; for **non-decreasing** (allow equals) use `bisect_right`. That one-line swap is a classic follow-up.

---

## Java (for Java interviewers)

```java
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int x : nums) {
        int lo = 0, hi = size;
        while (lo < hi) {                 // binary search: leftmost tail >= x
            int mid = (lo + hi) >>> 1;
            if (tails[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = x;
        if (lo == size) size++;
    }
    return size;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (subsequences) | O(2ⁿ) | O(n) |
| DP (ending-at-i) | O(n²) | O(n) |
| Patience sorting + binary search | O(n log n) | O(n) |

---

## Say it out loud (interview narration)

> *"Let dp[i] be the longest increasing subsequence ending at i; I look back at every smaller-valued earlier element and extend its best — that's O(n²). To hit the O(n log n) follow-up, I keep a tails array where tails[k] is the smallest tail of any length-(k+1) increasing subsequence. For each number I binary-search for the first tail that's ≥ it and overwrite it, or append if it's bigger than everything. The length of tails is the answer."*

## Related / follow-ups
- **Russian Doll Envelopes** (2-D LIS: sort by width, LIS on heights)
- **Number of LIS** (track count alongside length)
- **Longest Non-Decreasing Subsequence** (`bisect_right` instead of `bisect_left`)
- **Maximum Length of Pair Chain / Longest Chain** (greedy or LIS variant)
