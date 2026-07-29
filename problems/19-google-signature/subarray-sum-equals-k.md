# Subarray Sum Equals K

> **LeetCode:** 560. Subarray Sum Equals K · **Difficulty:** 🟡 Medium · **Pattern:** Prefix Sum + Hash Map · **Google frequency:** ⭐ high

---

## Problem

Given an integer array `nums` and an integer `k`, return the **total number of contiguous subarrays** whose elements sum to exactly `k`. The array may contain **negative numbers, zeros, and positives**, and subarrays must be contiguous (a run of adjacent elements).

**Example:** `nums = [1, 1, 1]`, `k = 2` → `2` *(the subarrays `[1,1]` at indices 0–1 and 1–2 both sum to 2).*

**Example:** `nums = [1, -1, 0]`, `k = 0` → `3` *(the subarrays `[1,-1]`, `[1,-1,0]`, and `[0]` all sum to 0 — notice the negatives and the zero.)*

**Constraints that matter:** `n` can be up to ~2·10⁴ and values range from -1000 to 1000. The killer detail is **negatives are allowed.** That single fact rules out the sliding-window trick you'd reach for on an all-positive array, and it's the whole reason this problem is interesting. `n` up to 2·10⁴ also means O(n²) (~4·10⁸) is borderline-to-slow — the O(n) solution is what earns the hire.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Look at every possible subarray, add up its elements, check if it equals `k`." That's every start paired with every end — the brute force. It works, but it re-adds the same numbers over and over.
- **Where it hurts:** Recomputing each subarray's sum from scratch is the waste. If I already know the sum of `nums[0..j-1]`, I shouldn't re-add everything to get `nums[0..j]`. That screams **prefix sums** — carry a running total as I sweep left to right.
- **The leap:** Let `prefix[j]` be the sum of everything up to index `j`. The sum of the subarray from `i+1` to `j` is just `prefix[j] - prefix[i]`. I want that to equal `k`, so I want `prefix[j] - prefix[i] = k`, which rearranges to `prefix[i] = prefix[j] - k`. So standing at position `j`, the question becomes: **how many earlier prefixes equal `currentPrefix - k`?** Each one marks a subarray ending here that sums to `k`. Store a **count of every prefix sum seen so far** in a hash map, and answer that question in O(1).
- **Why not two pointers / sliding window?** This is the trap, and naming it out loud is a strong-hire move. A sliding window only works when extending the window makes the sum move **monotonically** in one direction — true when all numbers are positive (grow the window → sum only goes up; shrink → only goes down). With **negatives**, adding an element can *decrease* the sum and removing one can *increase* it. The "shrink from the left when we overshoot" rule breaks, because overshooting is no longer permanent — a later negative could pull us right back to `k`. So the window has no reliable direction to shrink. **Sliding window is fundamentally the wrong tool here; prefix-sum counting is the right one.**
- **Pattern trigger:** **"count subarrays with a given sum" + negatives allowed** → **prefix sum stored in a hash map.** Burn that pairing in.

---

## ① Brute Force

Try every subarray. Use a running inner sum so we don't triple-nest.

```python
def subarray_sum_brute(nums, k):
    count = 0
    n = len(nums)
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]        # extend the subarray [i..j]
            if total == k:
                count += 1
    return count
```

**Why it's the natural first attempt:** it's the literal reading of the problem — "check every contiguous subarray." The inner running `total` already avoids a third loop.

**Why it's not enough:** it's still `n(n+1)/2` subarrays → O(n²). On a 2·10⁴-element hidden test that's ~2·10⁸ operations — sluggish, and needless, because we keep recomputing sums we've effectively already seen.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

One pass. Keep a running prefix sum and a hash map counting how many times each prefix sum has occurred. At each element, look up `prefix - k`.

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1                 # empty prefix: sum 0 has happened once
    for num in nums:
        prefix += num
        count += seen[prefix - k]   # how many earlier prefixes = prefix - k?
        seen[prefix] += 1           # record this prefix for future lookups
    return count
```

**Walk the example** `nums = [1, 2, 3]`, `k = 3`:

| num | prefix | need (`prefix - k`) | `seen[need]` | count | `seen` after |
|---|---|---|---|---|---|
| — | 0 | — | — | 0 | `{0:1}` |
| 1 | 1 | -2 | 0 | 0 | `{0:1, 1:1}` |
| 2 | 3 | 0 | 1 | 1 | `{0:1, 1:1, 3:1}` |
| 3 | 6 | 3 | 1 | 2 | `{0:1, 1:1, 3:1, 6:1}` |

Answer `2` — the subarrays `[1,2]` and `[3]`. Notice the `{0:1}` seed: it's what lets a prefix that *itself* equals `k` (like `1+2=3`) count as a valid subarray from the start.

**Why the `{0:1}` seed matters:** a subarray that begins at index 0 has no earlier prefix to subtract. Seeding sum-0-seen-once represents the "empty prefix before the array," so those from-the-start subarrays get counted.

**Why it's correct:** every subarray ending at the current index and summing to `k` corresponds to exactly one earlier prefix equal to `prefix - k`. Counting occurrences (not just presence) handles repeats — the same prefix value can appear multiple times, and each one is a distinct valid subarray. We record each prefix *after* the lookup so we never pair an index with itself.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ③ Space Optimization

Can we drop the map? **No — and being honest about that is the point.** In the worst case every prefix sum is distinct (e.g. an all-positive array), so the map genuinely holds up to `n` entries. There's no rolling-variable trick that recovers "how many earlier prefixes equalled this value" without remembering them.

```python
# No meaningful space reduction here — the map is doing essential work.
# O(n) space is the honest, correct answer.
```

**Complexity:** Time `O(n)`, Space `O(n)`.

> Contrast with the two-pointer problems where O(1) space is achievable: those rely on **sorted or all-positive** structure that lets you *discard* information as you go. Here, with negatives, any earlier prefix might still be needed, so we can't throw anything away. Say that out loud:
>
> *"I can't get below O(n) space — negatives mean any past prefix could still form a valid subarray, so I have to remember all of them. That's the honest bound."*

---

## Java (for Java interviewers)

```java
public int subarraySum(int[] nums, int k) {
    int count = 0, prefix = 0;
    Map<Integer, Integer> seen = new HashMap<>();
    seen.put(0, 1);                          // empty prefix
    for (int num : nums) {
        prefix += num;
        count += seen.getOrDefault(prefix - k, 0);
        seen.merge(prefix, 1, Integer::sum);
    }
    return count;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Optimised (prefix sum + hash map) | O(n) | O(n) |
| Space-optimised | O(n) | O(n) *(can't beat it — negatives forbid discarding prefixes)* |

---

## Say it out loud (interview narration)

> *"Brute force checks every subarray — O(n²). To do better I use prefix sums: the sum from i+1 to j is prefix[j] minus prefix[i], so a subarray equals k exactly when I've seen an earlier prefix equal to currentPrefix minus k. I keep a hash map counting prefix sums, seeded with {0:1} for subarrays starting at index 0, and at each step add up how many matching earlier prefixes exist. That's one pass, O(n) time. And I'd flag it: I can't use a sliding window here because the array has negatives — extending the window doesn't move the sum monotonically, so there's no reliable direction to shrink. Space is O(n) and I can't beat that, because any earlier prefix might still be needed."*

## Related / follow-ups
- **Continuous Subarray Sum** (LC 523 — prefix sum mod k in a map)
- **Subarray Sums Divisible by K** (LC 974 — count by remainder)
- **Contiguous Array** (LC 525 — map first index of each running balance)
- **Minimum Size Subarray Sum** (LC 209 — all-positive, so sliding window *does* work — the instructive contrast)
- **Maximum Size Subarray Sum Equals k** (LC 325 — same map trick, store earliest index)
