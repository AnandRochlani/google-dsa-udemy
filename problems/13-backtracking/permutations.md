# Permutations

> **LeetCode:** 46. Permutations · **Difficulty:** 🟡 Medium · **Pattern:** Subsets & Backtracking · **Google frequency:** ⭐ high

---

## Problem

Given an array `nums` of **distinct** integers, return **all the possible permutations** (every ordering). You can return them in any order.

**Example:** `nums = [1, 2, 3]` → `[[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]` *(all 3! = 6 orderings).*

**Constraints that matter:** `1 ≤ nums.length ≤ 6`. That `6` is the signal: there are `n!` permutations (`6! = 720`), so the output is **factorial-sized by definition**. You can't enumerate all orderings in less than `O(n!)` — that's inherent to the problem, not a weakness of your approach. The goal is to generate them cleanly, not to beat `O(n!)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Pick a first element, then a second from what's left, then a third..." At the first slot you have `n` choices, at the second `n-1`, and so on → `n × (n-1) × ... × 1 = n!` orderings. A shrinking set of choices per position is the backtracking tell.

- **The decision tree mental model:** the tree has `n` levels (one per position). The root branches `n` ways (which element goes first). Each of those branches `n-1` ways (which goes second), etc. A **leaf** — reached when `path` has length `n` — is one full permutation. Unlike subsets, we only record at **leaves**, because a permutation must use *every* element.

- **The difference from subsets:** in subsets we used a `start` index and only moved *forward* to avoid duplicates. In permutations **order matters and every element must appear**, so we can't move only forward — `[2,1,3]` and `[1,2,3]` are both wanted. Instead we track which elements are **already used** and pick any *unused* one at each step.

- **The backtracking skeleton — same rhythm:** **CHOOSE** an unused element (append to `path`, mark it used), **RECURSE** to fill the next position, then **UN-CHOOSE** (pop it, mark it unused) so the slot is free for the next candidate. The un-choose restores both the `path` and the `used` set for the sibling branch.

- **Pattern trigger:** **"generate all orderings / arrangements"** → backtracking with a `used` set (instead of a `start` index). Subsets/combinations = `start` index; permutations = `used` tracking. That's the fork in the road.

---

## ① Brute Force

The library / "generate everything" framing: Python's `itertools.permutations` produces all orderings directly.

```python
from itertools import permutations

def permute_brute(nums):
    return [list(p) for p in permutations(nums)]
```

**Why it's the natural first attempt:** it's the literal one-liner for "all orderings," and it's correct.

**Why we look further:** in an interview the point is to *show you can write the recursion*, and — more importantly — the hand-rolled version is the one you can **prune** or adapt (e.g. Permutations II with duplicates, or stopping early on a constraint). The library gives you no hook for that. Complexity is identical: `O(n · n!)`.

**Complexity:** Time `O(n · n!)`, Space `O(n · n!)` for output.

---

## ② Optimised Solution

Hand-rolled backtracking with a `used` boolean array. Record only at leaves.

```python
def permute(nums):
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):            # leaf: a full ordering
            result.append(path[:])            # snapshot
            return
        for i in range(len(nums)):
            if used[i]:
                continue                      # skip elements already in path
            path.append(nums[i])              # CHOOSE
            used[i] = True
            backtrack()                       # RECURSE
            path.pop()                        # UN-CHOOSE
            used[i] = False

    backtrack()
    return result
```

**Walk part of the decision tree** for `nums = [1, 2, 3]`:

```
path=[], used=[F,F,F]
  choose 1 -> path=[1], used=[T,F,F]
    choose 2 -> path=[1,2]
      choose 3 -> path=[1,2,3]  LEAF -> record [1,2,3]; undo
    undo 2
    choose 3 -> path=[1,3]
      choose 2 -> path=[1,3,2]  LEAF -> record [1,3,2]; undo
    undo
  undo 1
  choose 2 -> path=[2] ...  (produces [2,1,3], [2,3,1])
  choose 3 -> path=[3] ...  (produces [3,1,2], [3,2,1])
```

Each `used[i] = True` / `used[i] = False` pair mirrors the `path.append` / `path.pop`. After exploring "1 then 2 then 3," we undo back up and free element `2` so "1 then 3 then 2" can use it.

**Why it's correct:** at every position we consider *all* unused elements, so no ordering is skipped. Because an element is marked used the instant it's placed, no permutation repeats an element. Recording only at length `n` guarantees every result is a complete ordering.

**Complexity:** Time `O(n · n!)` — `n!` leaves, each an `O(n)` copy (the internal nodes add a lower-order term). Space `O(n)` auxiliary.

---

## ③ Space Optimization

The output holds `n!` permutations of length `n` → `O(n · n!)`, which is **inherent** (it's the answer). The auxiliary space is what we control.

**Output vs auxiliary space:** the `used` array is `O(n)`, `path` is `O(n)`, recursion depth is `O(n)` → total auxiliary `O(n)`. Already optimal.

**The in-place swap trick** removes even the `used` array by permuting `nums` itself: swap the current index into place, recurse, swap back (the un-choose).

```python
def permute_inplace(nums):
    result = []

    def backtrack(first):
        if first == len(nums):
            result.append(nums[:])            # snapshot the current arrangement
            return
        for i in range(first, len(nums)):
            nums[first], nums[i] = nums[i], nums[first]   # CHOOSE (swap in)
            backtrack(first + 1)                          # RECURSE
            nums[first], nums[i] = nums[i], nums[first]   # UN-CHOOSE (swap back)

    backtrack(0)
    return result
```

Same `O(n)` recursion depth, but no separate `used`/`path` lists — the array *is* the path. Auxiliary space is still `O(n)` asymptotically (the stack dominates), but it's a tidy trick worth naming: *"I can permute the array in place with swaps instead of carrying a used-array, undoing each swap on the way back up."*

---

## Java (for Java interviewers)

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, new ArrayList<>(), new boolean[nums.length], result);
    return result;
}

private void backtrack(int[] nums, List<Integer> path, boolean[] used, List<List<Integer>> result) {
    if (path.size() == nums.length) {
        result.add(new ArrayList<>(path));            // snapshot at leaf
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        path.add(nums[i]); used[i] = true;            // CHOOSE
        backtrack(nums, path, used, result);          // RECURSE
        path.remove(path.size() - 1); used[i] = false; // UN-CHOOSE
    }
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) | Space (output) |
|---|---|---|---|
| itertools | O(n · n!) | O(1) | O(n · n!) |
| Backtracking + used array | O(n · n!) | O(n) | O(n · n!) |
| In-place swaps | O(n · n!) | O(n) stack | O(n · n!) |

---

## Say it out loud (interview narration)

> *"There are n! orderings, so the output is factorial — that's inherent. I'll backtrack: at each position I try every element that hasn't been used yet, mark it used, recurse to fill the next slot, then pop it and unmark it to try the next candidate. When the path reaches length n I record a copy. The choose/un-choose on both the path and the used-array is what lets me reuse one shared state. Time is O(n·n!) dominated by the output; auxiliary space is O(n). If you want, I can drop the used-array entirely and permute the array in place with swaps, undoing each swap on the way back."*

## Related / follow-ups
- **Permutations II** (LC 47 — duplicates; sort, then skip `i>start && nums[i]==nums[i-1] && !used[i-1]`)
- **Subsets** (LC 78 — `start` index instead of `used`, record every node)
- **Next Permutation** (LC 31 — a single next ordering, done in-place, not backtracking)
- **Letter Combinations of a Phone Number** (LC 17 — permutation-style build over digit→letters)
