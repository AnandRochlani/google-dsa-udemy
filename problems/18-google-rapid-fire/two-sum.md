# Two Sum

> **LeetCode:** 1. Two Sum · **Difficulty:** 🟢 Easy · **Pattern:** Hash Map (complement lookup) · **Google frequency:** ⭐ high

---

## Problem

Given an array of integers `nums` (**not sorted**) and a `target`, return the **indices** of the two numbers that add up to `target`. Exactly one solution exists, and you may not use the same element twice.

**Example:** `nums = [2, 7, 11, 15]`, `target = 9` → `[0, 1]` *(because 2 + 7 = 9).*

**Constraints that matter:** `n` up to `10⁴`. The array is **unsorted**, so we can't lean on two pointers the way the sorted variant (Two Sum II) does — sorting would cost O(n log n) *and* destroy the original indices we're asked to return. That pushes us toward a hash-map, one-pass O(n) solution.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "for each number, look for a partner that completes the target." The literal version checks every pair — the brute force.
- **Where it hurts:** for each element you re-scan the rest of the array searching for `target - num`. That inner search is the waste — you're *looking things up by value*, over and over.
- **The leap:** "look something up by value, instantly" is the definition of a **hash map**. As you walk the array, remember every number you've seen (mapping value → its index). For the current number `x`, its needed partner is `complement = target - x`. If you've *already seen* the complement, you're done — and because you stored the index, you can return both. One pass, each lookup O(1).
- **Why one pass suffices:** you don't need the complement to come *before* or *after* — whichever of the pair you reach *second* will find the first already sitting in the map. So checking the map *before* inserting the current element is enough, and it also prevents pairing an element with itself.
- **Pattern trigger:** *"find two things that combine to a target, unsorted"* → **hash map complement lookup**. Sorted instead? Two pointers. This value-pairing → hash-map reflex is one of the most reused ideas in interviews.

---

## ① Brute Force

Check every pair with two nested loops.

```python
def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**Why it's the natural first attempt:** it's the direct translation of "try all two-number combinations."

**Why it's not enough:** ~n²/2 comparisons. Fine on 4 elements; on a 10⁴ hidden test that's ~5×10⁷ — borderline — and the pattern generalizes badly. The repeated inner scan is pure redundancy: we keep asking "is `target - nums[i]` in the array?" without remembering answers.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

One pass; a hash map from value → index; check for the complement before inserting.

```python
def two_sum(nums, target):
    seen = {}                      # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i                # record current for future partners
    return []
```

**Walk the example** `nums = [2, 7, 11, 15]`, `target = 9`:

| i | x | complement = 9 − x | in `seen`? | action |
|---|---|---|---|---|
| 0 | 2 | 7 | no | store `2→0` → `seen={2:0}` |
| 1 | 7 | 2 | **yes** (index 0) | return `[0, 1]` ✅ |

We reached `7` second; its partner `2` was already in the map, so we return both indices without ever scanning ahead.

**Why it's correct:** for any valid pair `(a, b)`, consider whichever we visit *later*. At that moment the earlier one is already in `seen`, so the complement check fires and returns the right index pair. Checking before inserting guarantees we never match an element with itself.

**Complexity:** Time `O(n)` — one pass, O(1) lookups. Space `O(n)` — the map holds up to n entries.

---

## ③ Space Optimization

The O(n) hash map is **inherent for unsorted input** — there's no O(1)-space O(n)-time solution here. Naming why is the teaching moment:

- To get **O(1) space**, you'd sort first and use two pointers → **O(n log n) time**, and sorting scrambles positions, so you'd need to store the original indices (back to O(n) space) or return values instead of indices. For *this* problem (return indices, unsorted), the hash map's O(n) space buys you the better O(n) time.
- Contrast with **Two Sum II** (167), where the input is *already sorted*: there, two pointers give O(n) time and **O(1) space** — strictly better. The whole difference is the sorted precondition.

> Say it out loud: *"Unsorted and I must return indices, so I'll spend O(n) space on a hash map to get O(n) time. If it were sorted I'd switch to two pointers for O(1) space."* Choosing the structure to fit the precondition is the signal.

---

## Java (for Java interviewers)

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();   // value -> index
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all pairs) | O(n²) | O(1) |
| Hash map (one pass) | O(n) | O(n) |
| Sort + two pointers (loses indices) | O(n log n) | O(1)* |

*\*O(1) extra beyond the sort, but requires the input sorted or index bookkeeping.*

---

## Say it out loud (interview narration)

> *"Brute force is every pair, O(n²). The waste is repeatedly searching for target minus the current number, and 'search by value' means a hash map. So I walk once, and for each number I check whether its complement is already in the map — if so I return both indices, otherwise I store the current number and move on. Whichever of the pair I hit second finds the first waiting. That's O(n) time, O(n) space. The array's unsorted and I have to return indices, so the hash map is the right call; if it were sorted I'd use two pointers for O(1) space instead."*

## Related / follow-ups
- **Two Sum II — Input Array Is Sorted** (167) — two pointers, O(1) space.
- **3Sum** (15) — fix one element, two-pointer or hash the rest.
- **Two Sum III — Data structure design** (170) — add/find as an online design.
- **Subarray Sum Equals K** (560) — same complement-in-a-map idea on prefix sums.
- **Group Anagrams** (49) — another "hash a derived key" reflex.
