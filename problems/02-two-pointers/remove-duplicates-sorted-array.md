# Remove Duplicates from Sorted Array

> **LeetCode:** 26. Remove Duplicates from Sorted Array · **Difficulty:** 🟢 Easy · **Pattern:** Two Pointers · **Google frequency:** ⭐ high

---

## Problem

You're given an array `nums` **sorted in ascending order**. Remove the duplicates **in place** so each value appears once, keep the relative order, and return `k` — the number of unique elements. The first `k` slots of `nums` must hold those unique values. What's left after index `k` doesn't matter.

**Example:** `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]` → return `5`, and `nums` starts with `[0, 1, 2, 3, 4, ...]`.

**Constraints that matter:** the array is **sorted** (so duplicates are always adjacent), and you must do it **in place** — no allocating a second array. That "in place" word is what forces the two-pointer write trick instead of just filtering into a new list.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "Collect the unique values into a set or a new list, then copy them back." Easy to write, and it's the brute force. But it allocates extra memory — which the problem explicitly forbids.
- **Where it hurts:** you're building a whole second container to answer a question about *ordering within the array you already have*. And you're ignoring the biggest gift: the array is **sorted**, so every duplicate sits **right next to** its twin. You never need a set to detect a repeat — just look at the neighbor.
- **The leap:** keep two pointers walking the **same** array. A slow pointer `write` marks "the last spot I've finalized as unique." A fast pointer `read` scans ahead. Whenever `read` finds a value **different** from the one at `write`, it's a new unique — bump `write` and copy it there. Duplicates just get skipped by `read`. Because uniques always come *before or at* the read position, overwriting in place never clobbers data you still need.
- **Pattern trigger:** **in-place array compaction on sorted/adjacent data** → **slow/fast (read/write) two pointers**. The signal is "keep some elements, drop others, in place, order preserved."

---

## ① Brute Force

Copy uniques into a new list, then write them back over the original.

```python
def remove_duplicates_brute(nums):
    seen = []
    for x in nums:
        if not seen or seen[-1] != x:   # sorted, so just check the last kept
            seen.append(x)
    for i in range(len(seen)):
        nums[i] = seen[i]
    return len(seen)
```

**Why it's the natural first attempt:** "filter to uniques, then put them back" is the most direct reading of the task.

**Why it's not enough:** `seen` is a second O(n) array. The problem says *in place* precisely to rule this out. It works, but it fails the memory constraint an interviewer is testing.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

One array, two pointers. `write` is where the next unique goes; `read` scans everything.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 0                     # nums[0..write] are the finalized uniques
    for read in range(1, len(nums)):
        if nums[read] != nums[write]:
            write += 1
            nums[write] = nums[read]
    return write + 1              # count = last index + 1
```

**Walk the example** `[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`:

| read (val) | nums[write] | new? | action | array front |
|---|---|---|---|---|
| 1 (0) | 0 | no | skip | `[0,...]` |
| 2 (1) | 0 | yes | write=1, nums[1]=1 | `[0,1,...]` |
| 3 (1) | 1 | no | skip | `[0,1,...]` |
| 4 (1) | 1 | no | skip | `[0,1,...]` |
| 5 (2) | 1 | yes | write=2, nums[2]=2 | `[0,1,2,...]` |
| 6 (2) | 2 | no | skip | `[0,1,2,...]` |
| 7 (3) | 2 | yes | write=3, nums[3]=3 | `[0,1,2,3,...]` |
| 8 (3) | 3 | no | skip | `[0,1,2,3,...]` |
| 9 (4) | 3 | yes | write=4, nums[4]=4 | `[0,1,2,3,4,...]` |

Return `write + 1 = 5`. ✅

**Why it's correct:** the invariant is "`nums[0..write]` are exactly the distinct values seen so far, in order." `write` never runs ahead of `read`, so writing to `nums[write]` only ever overwrites a slot we've already read past — no live data is lost. Since the array is sorted, `nums[write]` is always the most recent unique, so one comparison detects any duplicate.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

Already O(1) space — that *is* the optimization the problem is after. Two integer pointers, everything happens inside the input array. There's no set, no copy, nothing that scales with `n`. The jump from brute force to this is precisely trading the O(n) `seen` list for a single `write` index.

> Say it out loud: *"Sorted means duplicates are adjacent, so I don't need a set — a write pointer compacting in place gives O(1) space."*

---

## Java (for Java interviewers)

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int write = 0;
    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[write]) {
            write++;
            nums[write] = nums[read];
        }
    }
    return write + 1;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (copy uniques) | O(n) | O(n) |
| Optimised (read/write pointers) | O(n) | O(1) |
| Space-optimised | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"The naive way copies uniques into a new list and writes them back, but that's O(n) extra space and the problem wants it in place. Since the array's sorted, duplicates are adjacent, so I use a slow write pointer and a fast read pointer: whenever read sees a value different from the last one I kept, I advance write and copy it there. One pass, O(n) time, O(1) space, and I return write + 1 as the unique count."*

## Related / follow-ups
- **Remove Duplicates from Sorted Array II** (keep at most two of each)
- **Remove Element** (drop a target value in place — same write-pointer trick)
- **Move Zeroes** (compact non-zeros forward, zeros to the back)
- **Merge Sorted Array** (two pointers, write from the back)
