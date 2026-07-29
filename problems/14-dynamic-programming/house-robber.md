# House Robber

> **LeetCode:** 198. House Robber · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming · **Google frequency:** ⭐ high

---

## Problem

Houses along a street each hold some money, given as `nums`. You're a robber, but adjacent houses have connected alarms — **robbing two neighbours triggers the police.** Return the **maximum money** you can rob without ever hitting two adjacent houses.

**Example:** `nums = [2, 7, 9, 3, 1]` → `12`. Rob house 0 (2) + house 2 (9) + house 4 (1) = 12. (Robbing 7 + 3 = 10 is worse; 2 + 9 + 1 wins.)

**Constraints that matter:** `1 ≤ nums.length ≤ 100`, `0 ≤ nums[i] ≤ 400`. Small input, but the naive "try every valid subset" is exponential. The transferable skill is the **rob-or-skip decision** and collapsing the DP to **O(1) space**.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision at each house.** Stand at house `i` with the money from houses `0..i` on the table. You face exactly one binary choice: **rob house `i`, or skip it.**
- If you **rob** `i`: you gain `nums[i]`, but you're forbidden from house `i-1`, so the best you had before is whatever was optimal up to `i-2`.
- If you **skip** `i`: you gain nothing here, and you keep whatever was optimal up to `i-1`.

You want the better of the two:

> **rob(i) = max( nums[i] + rob(i-2),  rob(i-1) )**

**(b) Notice overlapping subproblems.** `rob(i)` calls `rob(i-1)` and `rob(i-2)`; `rob(i-1)` calls `rob(i-2)` and `rob(i-3)` — `rob(i-2)` is computed by both branches. Same exponential re-computation as Climbing Stairs. That's the DP trigger.

**(c) Add memoization (top-down).** Cache `rob(i)` so each index is solved once — the 2ⁿ tree collapses to `n` subproblems.

**(d) Convert to a bottom-up table.** Fill `dp[i]` for `i = 0 … n-1`:
`dp[i] = max(nums[i] + dp[i-2], dp[i-1])`, with `dp[0] = nums[0]` and `dp[1] = max(nums[0], nums[1])`.

**(e) Collapse to rolling variables.** `dp[i]` reads only `dp[i-1]` and `dp[i-2]` — the same two-back pattern as Fibonacci. Keep two variables and slide. **O(n) → O(1).**

**State & recurrence (memorize this):**
- **State:** `dp[i]` = max money robbable from houses `0..i`.
- **Recurrence:** `dp[i] = max(dp[i-1], nums[i] + dp[i-2])`.
- **Base:** `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`.

---

## ① Brute Force

Recurse the rob-or-skip choice directly, exploring both branches everywhere.

```python
def rob_brute(nums):
    def helper(i):
        if i < 0:
            return 0
        rob_here = nums[i] + helper(i - 2)   # rob i, skip i-1
        skip_here = helper(i - 1)            # skip i
        return max(rob_here, skip_here)
    return helper(len(nums) - 1)
```

**Why it's the natural first attempt:** it's the decision written literally — at each house, take the best of "rob it" vs "skip it."

**Why it's not enough:** every house forks into two recursive calls with no memory, so the tree is ~O(2ⁿ) and it recomputes `helper(i)` for the same `i` over and over.

**Complexity:** Time `O(2ⁿ)`, Space `O(n)` (stack).

---

## ② Optimised Solution

Build the table bottom-up; each subproblem solved once.

```python
def rob_dp(nums):
    n = len(nums)
    if n == 1:
        return nums[0]
    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, n):
        dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
    return dp[n - 1]
```

**A small filled table** for `nums = [2, 7, 9, 3, 1]`:

| i | nums[i] | dp[i] | reasoning |
|---|---|---|---|
| 0 | 2 | 2 | rob it |
| 1 | 7 | 7 | max(2, 7) |
| 2 | 9 | 11 | max(dp1=7, 9+dp0=11) |
| 3 | 3 | 11 | max(dp2=11, 3+dp1=10) |
| 4 | 1 | 12 | max(dp3=11, 1+dp2=12) |

Answer `dp[4] = 12`. ✅

**Why it's correct:** at every house the two options (rob → forced to `i-2`, or skip → inherit `i-1`) are exhaustive and each relies on an already-optimal subresult. Taking the max preserves optimality inductively.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ③ Space Optimization

**The key DP move.** Only `dp[i-1]` and `dp[i-2]` are ever read, so replace the array with two rolling variables:

```python
def rob(nums):
    prev2, prev1 = 0, 0        # dp[i-2], dp[i-1]
    for x in nums:
        prev2, prev1 = prev1, max(prev1, x + prev2)
    return prev1
```

Walk `[2, 7, 9, 3, 1]` — `prev1` after each step: `2 → 7 → 11 → 11 → 12`. Return `12`. ✅
(Starting both at 0 handles the base cases uniformly, so no special-casing `n == 1`.)

**Complexity:** Time `O(n)`, Space `O(1)`.

> Same "table only reaches two rows back" observation as Climbing Stairs — the difference is `max` (an optimization) instead of `+` (a count). Recognizing that both problems share one skeleton is the point.

---

## Java (for Java interviewers)

```java
public int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;    // dp[i-2], dp[i-1]
    for (int x : nums) {
        int cur = Math.max(prev1, x + prev2);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recursion) | O(2ⁿ) | O(n) |
| Memoized (top-down) | O(n) | O(n) |
| Tabulated (bottom-up) | O(n) | O(n) |
| Space-optimised (rolling vars) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"At each house I either rob it — taking its money plus the best up to two houses back — or skip it and keep the best up to the previous house. So dp[i] = max(dp[i-1], nums[i] + dp[i-2]). Naive recursion is O(2ⁿ) from recomputing subproblems, so I tabulate in O(n). And because I only ever look two houses back, I keep two rolling variables — O(1) space."*

## Related / follow-ups
- **House Robber II** (houses in a **circle** — run the line-DP twice: exclude first, exclude last, take the max)
- **House Robber III** (houses form a **binary tree** — DP on tree nodes returning (rob, skip) pairs)
- **Delete and Earn** (bucket by value, then it *is* House Robber)
- **Climbing Stairs** (identical two-back skeleton, sum instead of max)
