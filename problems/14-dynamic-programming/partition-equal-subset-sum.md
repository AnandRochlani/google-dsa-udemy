# Partition Equal Subset Sum

> **LeetCode:** 416. Partition Equal Subset Sum · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming (0/1 Knapsack) · **Google frequency:** ⭐ high

---

## Problem

Given an array of positive integers `nums`, decide whether it can be split into **two subsets with equal sum**. Return `true`/`false`.

**Example:** `nums = [1, 5, 11, 5]` → `true`. Split into `[1, 5, 5]` and `[11]`, each summing to 11.

**Example:** `nums = [1, 2, 3, 5]` → `false`. Total is 11 (odd) — can't halve it.

**Constraints that matter:** `1 ≤ nums.length ≤ 200`, `1 ≤ nums[i] ≤ 100`. So total sum ≤ 20000. If the total is **odd**, answer is immediately `false`. Otherwise the question reduces to: *can some subset sum to `total / 2`?* — a **0/1 knapsack** (each number used at most once).

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Reframe, then find the decision.** Two equal subsets means each is exactly `total / 2`. So drop the "two subsets" framing — the real question is: **is there a subset summing to `target = total / 2`?** Now the decision per item is binary, just like House Robber: for each number, **include it in the subset, or don't.**

> **canMake(i, t)** = can we hit remaining target `t` using items `i, i+1, …`?
> `canMake(i, t) = canMake(i+1, t)  OR  canMake(i+1, t - nums[i])`
> (skip item i, or take it and reduce the target)

Base: `t == 0` → `True` (found it); `i` past the end with `t > 0` → `False`.

**(b) Notice overlapping subproblems.** The state is `(i, t)`. Many different include/exclude paths reach the same `(i, t)` — e.g. picking `{1,5}` or `{5,1}` both leave the same remaining target. Exponential recursion recomputes them → DP signal.

**(c) Memoize on `(i, t)`.** There are only `n × (target+1)` states, so caching makes it polynomial.

**(d) Bottom-up table.** `dp[i][t]` = can items up to `i` form sum `t`. But the cleaner, interview-favourite form is a **1-D boolean array** `dp[t]` = "is sum `t` achievable with the items seen so far?" Start `dp[0] = True`. For each number, update.

**(e) Space — the 1-D boolean trick (the key skill here).** Collapse the 2-D `dp[i][t]` to one row `dp[t]`. The catch: because each item is used **at most once** (0/1 knapsack), you must iterate `t` **from high to low**. Going low-to-high would let the same number be reused within one pass (that's the *unbounded* knapsack). The reverse iteration is the crux — memorize it.

**State & recurrence (memorize this):**
- **State:** `dp[t]` = is subset-sum `t` achievable using items processed so far.
- **Transition (per number `x`):** `dp[t] = dp[t] OR dp[t - x]` for `t` from `target` down to `x`.
- **Base:** `dp[0] = True`. **Answer:** `dp[target]`.

---

## ① Brute Force

Recurse include/exclude over every item; success if any path hits the target.

```python
def can_partition_brute(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2

    def helper(i, t):
        if t == 0:
            return True
        if i == len(nums) or t < 0:
            return False
        return helper(i + 1, t - nums[i]) or helper(i + 1, t)

    return helper(0, target)
```

**Why it's the natural first attempt:** each number is either in the subset or not — the literal include/exclude search.

**Why it's not enough:** 2ⁿ subsets, and the same `(i, t)` states recur across paths. Exponential without memoization.

**Complexity:** Time `O(2ⁿ)`, Space `O(n)` (stack).

---

## ② Optimised Solution — 2-D DP

`dp[i][t]` = can the first `i` numbers form sum `t`.

```python
def can_partition_2d(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True                     # sum 0 always achievable (empty subset)
    for i in range(1, n + 1):
        x = nums[i - 1]
        for t in range(1, target + 1):
            dp[i][t] = dp[i - 1][t]         # skip x
            if t >= x:
                dp[i][t] = dp[i][t] or dp[i - 1][t - x]   # take x
    return dp[n][target]
```

**A small filled table** for `nums = [1, 5, 11, 5]`, `target = 11` (T/F, columns t = 0…11):

| items \ t | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {} | T | · | · | · | · | · | · | · | · | · | · | · |
| {1} | T | T | · | · | · | · | · | · | · | · | · | · |
| {1,5} | T | T | · | · | · | T | T | · | · | · | · | · |
| {1,5,11} | T | T | · | · | · | T | T | · | · | · | · | T |
| {1,5,11,5} | T | T | · | · | · | T | T | · | · | · | T | **T** |

`dp[4][11] = True` (via `1+5+5`). ✅

**Why it's correct:** `dp[i][t]` is true iff we can hit `t` either without item `i` (`dp[i-1][t]`) or by using it (`dp[i-1][t-x]`) — exhaustive and non-overlapping over "use item i or not."

**Complexity:** Time `O(n × target)`, Space `O(n × target)`.

---

## ③ Space Optimization — 1-D boolean array

**The key DP skill.** Each row only depends on the row above, so keep a single boolean array and iterate `t` **downward** so each number is used at most once:

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for t in range(target, x - 1, -1):     # HIGH → LOW: 0/1 knapsack
            if dp[t - x]:
                dp[t] = True
        if dp[target]:                          # early exit
            return True
    return dp[target]
```

Processing `[1,5,11,5]`, the set of achievable sums grows: `{0} → {0,1} → {0,1,5,6} → {0,1,5,6,11,…} →` includes `11`. ✅

**Why the reverse loop matters:** if you looped `t` low→high, then after setting `dp[x]=True` you'd immediately use it again to set `dp[2x]`, effectively taking the same item twice (that's the *unbounded* knapsack, the wrong problem here). Iterating high→low reads only *old* (previous-item) values of `dp[t-x]`.

**Complexity:** Time `O(n × target)`, Space `O(target)`.

---

## Java (for Java interviewers)

```java
public boolean canPartition(int[] nums) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % 2 != 0) return false;
    int target = total / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int x : nums) {
        for (int t = target; t >= x; t--) {     // high -> low
            if (dp[t - x]) dp[t] = true;
        }
        if (dp[target]) return true;
    }
    return dp[target];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (include/exclude) | O(2ⁿ) | O(n) |
| Memoized (top-down, on (i,t)) | O(n × target) | O(n × target) |
| Tabulated 2-D | O(n × target) | O(n × target) |
| Space-optimised 1-D bool | O(n × target) | O(target) |

*(`target = sum/2`, so this is "pseudo-polynomial" — polynomial in the numeric value of the sum.)*

---

## Say it out loud (interview narration)

> *"Equal partition means each half sums to total/2 — so if the total's odd it's immediately false, otherwise it's just: can a subset hit total/2? That's a 0/1 knapsack. Each number is include-or-exclude, so dp[t] = dp[t] or dp[t−x]. I collapse the 2-D table to one boolean array and iterate the target from high to low, which guarantees each number is used at most once. That's O(n × target) time, O(target) space."*

## Related / follow-ups
- **Subset Sum** (the underlying problem — hit an exact target)
- **Target Sum** (assign ± signs — reduces to a subset-sum count)
- **Last Stone Weight II** (minimize |sum of two subsets| — same knapsack)
- **Coin Change** (knapsack cousin, but *unbounded* → iterate low→high)
