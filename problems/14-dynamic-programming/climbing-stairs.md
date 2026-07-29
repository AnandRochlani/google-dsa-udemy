# Climbing Stairs

> **LeetCode:** 70. Climbing Stairs · **Difficulty:** 🟢 Easy · **Pattern:** Dynamic Programming · **Google frequency:** ⭐ high

---

## Problem

You're climbing a staircase with `n` steps. Each time you can climb either **1** or **2** steps. In how many **distinct ways** can you reach the top?

**Example:** `n = 3` → `3`. The ways are `1+1+1`, `1+2`, `2+1`.

**Constraints that matter:** `1 ≤ n ≤ 45`. Small, but the *naive recursion* branches into `O(2ⁿ)` calls — at `n = 45` that's ~35 billion, which times out. The real lesson isn't the size; it's spotting that this is Fibonacci in disguise and collapsing it to **O(1) space**.

---

## 🧠 Intuition — how you'd actually arrive at this

> The DP discovery path, step by step.

**(a) Find the decision at each step.** Stand on the top step `n`. How did you get here? Only two possibilities: your **last move was a single step** (so you were on step `n-1`), or your **last move was a double step** (so you were on step `n-2`). There is no third way to land on `n`. So:

> **ways(n) = ways(n-1) + ways(n-2)**

Base cases: `ways(0) = 1` (one way to "stand" at the bottom — do nothing) and `ways(1) = 1`.

**(b) Notice overlapping subproblems.** Draw the recursion tree for `ways(5)`: it calls `ways(4)` and `ways(3)`; `ways(4)` calls `ways(3)` and `ways(2)`… `ways(3)` gets computed **twice**, `ways(2)` even more. The same subproblems recur exponentially. That repetition is the DP signal.

**(c) Add memoization (top-down).** Cache each `ways(i)` the first time you compute it; on the second request, return it in O(1). The tree of ~2ⁿ nodes collapses to `n` distinct subproblems.

**(d) Convert to a bottom-up table.** Instead of recursing down and caching on the way back up, fill an array `dp` from the bottom: `dp[i] = dp[i-1] + dp[i-2]`, starting from `dp[0] = dp[1] = 1`. This is the same recurrence, evaluated in dependency order.

**(e) Collapse the table to rolling variables.** Look at the recurrence: `dp[i]` only ever reads the **two previous** values. You never look further back. So you don't need the whole array — just keep two variables and slide them forward. **O(n) → O(1) space.**

**State & recurrence (memorize this):**
- **State:** `dp[i]` = number of distinct ways to reach step `i`.
- **Recurrence:** `dp[i] = dp[i-1] + dp[i-2]`.
- **Base:** `dp[0] = 1`, `dp[1] = 1`.

This is literally the Fibonacci sequence (shifted by one).

---

## ① Brute Force

The naive recursion — translate the recurrence directly, no caching.

```python
def climb_brute(n):
    if n <= 1:
        return 1
    return climb_brute(n - 1) + climb_brute(n - 2)
```

**Why it's the natural first attempt:** it's the recurrence written verbatim — "ways to n = ways to n-1 + ways to n-2."

**Why it's not enough:** it recomputes the same subproblems again and again. The call tree has ~2ⁿ nodes because nothing is remembered. At `n = 45` it's tens of billions of calls → **Time Limit Exceeded.**

**Complexity:** Time `O(2ⁿ)`, Space `O(n)` (recursion stack).

---

## ② Optimised Solution

Same recurrence, but build a table bottom-up so each subproblem is solved exactly once.

```python
def climb_dp(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**A small filled table** for `n = 5`:

| i | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| dp[i] | 1 | 1 | 2 | 3 | 5 | 8 |

`dp[2] = dp[1]+dp[0] = 2`, `dp[3] = dp[2]+dp[1] = 3`, … `dp[5] = 8`.

**Why it's correct:** every path to step `i` has a well-defined last move (a +1 from `i-1` or a +2 from `i-2`), and those two source sets are disjoint and exhaustive — so summing them counts each path exactly once.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ③ Space Optimization

**This is the key DP skill here.** The recurrence reads only `dp[i-1]` and `dp[i-2]`. Everything older is dead weight. Keep two rolling variables instead of the array:

```python
def climb(n):
    prev, curr = 1, 1          # ways(0), ways(1)
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

Walk `n = 5`: `(prev,curr)` goes `(1,1) → (1,2) → (2,3) → (3,5) → (5,8)`. Return `8`. ✅

**Complexity:** Time `O(n)`, Space `O(1)`.

> Whenever a DP recurrence only reaches back a **fixed number of rows**, you can drop the full table for a handful of variables. This "sliding window of the table" trick is one of the most-tested DP instincts.

---

## Java (for Java interviewers)

```java
public int climbStairs(int n) {
    int prev = 1, curr = 1;      // ways(0), ways(1)
    for (int i = 2; i <= n; i++) {
        int next = prev + curr;
        prev = curr;
        curr = next;
    }
    return curr;
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

> *"To land on step n, my last move was either +1 from n-1 or +2 from n-2, so ways(n) = ways(n-1) + ways(n-2) — that's Fibonacci. Naively recursing is O(2ⁿ) because it recomputes subproblems, so I'll build it bottom-up in O(n). And since each value only needs the previous two, I don't need the whole array — two rolling variables give me O(1) space."*

## Related / follow-ups
- **House Robber** (same two-back recurrence, with a max instead of a sum)
- **Fibonacci Number / Tribonacci** (identical structure, 2 or 3 back)
- **Min Cost Climbing Stairs** (add a cost per step — carry a running min)
- **Decode Ways** (Fibonacci-flavoured, but transitions are conditional)
