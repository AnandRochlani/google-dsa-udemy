# Jump Game

> **LeetCode:** 55. Jump Game · **Difficulty:** 🟡 Medium · **Pattern:** Greedy & Intervals · **Google frequency:** ⭐ high

---

## Problem

You're given an integer array `nums`. You start at index 0, and `nums[i]` is the **maximum** jump length from position `i`. Return `true` if you can reach the last index, otherwise `false`.

**Example:** `nums = [2,3,1,1,4]` → `true` *(from 0 jump 1 to index 1, then jump 3 to index 4 — the end).*
Counter: `nums = [3,2,1,0,4]` → `false` *(whatever you do you land on index 3, whose value 0 traps you; index 4 is unreachable).*

**Constraints that matter:** `n` up to ~10⁴. An exponential "try every jump length from every cell" blows up; even DP is O(n²). The greedy reaches O(n) time, O(1) space.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** recursion — "from index `i`, try every jump `1..nums[i]` and see if any path reaches the end." Correct but exponential; overlapping subproblems make it DP-able (O(n²)), still not great.
- **Where it hurts:** you're tracking *which specific path* you take. But the question is only "reachable or not" — the exact route is irrelevant. All you actually need is: **how far can I possibly get?**
- **The greedy leap:** sweep left to right maintaining a single number, `furthest` = the maximum index reachable so far. At each index `i`, **if `i > furthest`, you're stuck** — no earlier cell could launch you here, so the end is unreachable → `false`. Otherwise `i` is reachable, so update `furthest = max(furthest, i + nums[i])`. If `furthest` ever reaches the last index, return `true`.
- **Why greedy is safe:** reachability is "downward closed" — if index `k` is reachable, so is every index `≤ k` (just jump shorter). So the single scalar `furthest` fully captures the reachable prefix; there's no benefit to remembering individual paths.
- **Pattern trigger:** **"can I reach / maximize reach with per-step ranges"** → **greedy furthest-reach sweep.** One rolling max beats path-tracking DP.

---

## ① Brute Force

Recurse from index 0, trying every jump length; memoize reachability per index.

```python
def can_jump_brute(nums):
    n = len(nums)
    from functools import lru_cache

    @lru_cache(None)
    def reach(i):
        if i >= n - 1:
            return True
        for step in range(1, nums[i] + 1):
            if reach(i + step):
                return True
        return False

    return reach(0)
```

**Why it's the natural first attempt:** it's the direct "explore all jump choices" formulation, and memoization makes it correct and non-exponential.

**Why it's not enough:** each index still tries up to `nums[i]` next indices, so it's O(n²) time and O(n) memo space — and worse, it needlessly tracks *paths* when a single reach frontier suffices.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution

One pass tracking the furthest reachable index.

```python
def canJump(nums):
    furthest = 0
    for i, jump in enumerate(nums):
        if i > furthest:              # this index is unreachable
            return False
        furthest = max(furthest, i + jump)
        if furthest >= len(nums) - 1: # can already reach the end
            return True
    return True
```

**Walk the example** `nums = [2,3,1,1,4]`:

| i | nums[i] | `i > furthest`? | furthest before | furthest after = max(prev, i+nums[i]) |
|---|---|---|---|---|
| 0 | 2 | 0 > 0 ❌ | 0 | max(0, 0+2)=2 |
| 1 | 3 | 1 > 2 ❌ | 2 | max(2, 1+3)=4 ≥ 4 → **return true** ✅ |

Counter `nums = [3,2,1,0,4]`:

| i | nums[i] | `i > furthest`? | furthest after |
|---|---|---|---|
| 0 | 3 | 0 > 0 ❌ | max(0,3)=3 |
| 1 | 2 | 1 > 3 ❌ | max(3,3)=3 |
| 2 | 1 | 2 > 3 ❌ | max(3,3)=3 |
| 3 | 0 | 3 > 3 ❌ | max(3,3)=3 |
| 4 | 4 | 4 > 3 ✅ | **return false** ✅ |

**Why it's correct:** the invariant is that `furthest` equals the largest index reachable using only indices seen so far. Because reachability is downward-closed, every index `i <= furthest` is genuinely reachable, so updating from it is valid. The moment `i > furthest`, there's a gap no jump can cross, so the end is provably unreachable.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

Already optimal — the whole method **is** the space optimization over the DP. We collapsed an `O(n)` memo array into a single integer `furthest`.

> **Say it out loud:** *"I don't need a DP array — reachability is monotone, so one rolling max captures the entire reachable prefix. That's O(1) space."* Naming why the array is unnecessary (downward-closed reachability) is exactly the insight interviewers reward.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
public boolean canJump(int[] nums) {
    int furthest = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > furthest) return false;           // unreachable index
        furthest = Math.max(furthest, i + nums[i]);
        if (furthest >= nums.length - 1) return true;
    }
    return true;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (memoized recursion) | O(n²) | O(n) |
| Greedy furthest-reach | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"The exact path doesn't matter — only whether the end is reachable — and reachability is downward-closed, so I just track one number: the furthest index I can reach. I sweep left to right; if I ever stand on an index beyond my furthest reach, there's an unbridgeable gap so I return false. Otherwise I extend furthest by `i + nums[i]`, and the moment it covers the last index I return true. That collapses the O(n²) DP into an O(n) time, O(1) space greedy."*

## Related / follow-ups
- **Jump Game II** (LC 45 — minimum number of jumps; greedy over "current jump's reach")
- **Jump Game III** (LC 1306 — jump ±nums[i]; BFS/DFS reachability)
- **Gas Station** (LC 134 — another single-pass greedy reachability argument)
- **Video Stitching** (LC 1024 — furthest-reach greedy on intervals)
