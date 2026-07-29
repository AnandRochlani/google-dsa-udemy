# Subsets

> **LeetCode:** 78. Subsets · **Difficulty:** 🟡 Medium · **Pattern:** Subsets & Backtracking · **Google frequency:** ⭐ high

---

## Problem

Given an array `nums` of **distinct** integers, return **all possible subsets** (the power set). The solution set must not contain duplicate subsets, and the order of subsets doesn't matter.

**Example:** `nums = [1, 2, 3]` → `[[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]` *(all 2³ = 8 subsets, including the empty set and the full set).*

**Constraints that matter:** `1 ≤ nums.length ≤ 10`. That tiny `10` is a *signal*: the answer itself has `2ⁿ` subsets, so at `n = 10` that's `1024` subsets — totally fine. **The output is exponential by definition** — there's no way to list every subset in less than `O(2ⁿ)`. That's not a flaw in your solution; it's inherent to the problem. Your job is to *enumerate them without waste*, not to beat `O(2ⁿ)`.

---

## 🧠 Intuition — how you'd actually arrive at this

> Subsets is the **canonical backtracking template** — learn it here and every other problem in this folder is a variation.

- **First instinct:** "I need every combination of 'in or out' for each element." For `[1,2,3]`, element `1` is either in the subset or not, `2` is either in or not, `3` is either in or not. That's a chain of **binary decisions** — `2 × 2 × 2 = 8` outcomes. A decision *per element* is the tell-tale sign of backtracking.

- **The decision tree mental model:** picture a tree. At the root you've picked nothing. At each level you decide the fate of the next element. Every **path from root to leaf** is one complete subset, and every **node along the way** is also a valid subset (since a subset can be any length). You want to *visit every node* of this tree.

- **The backtracking skeleton — burn this in:** at each step you **CHOOSE** an option (add an element to your current path), **RECURSE** (go deeper to decide the next element), then **UN-CHOOSE** (remove that element — "undo") so you can try the next option with a clean slate. That choose → recurse → un-choose rhythm is the entire pattern. The "un-choose" is what makes it *backtracking* rather than plain recursion: you rewind the state so the shared `path` list is correct for the sibling branch.

- **Why a `start` index?** To avoid duplicates like `[1,2]` and `[2,1]`, we only ever look *forward*. Once we've moved past element `i`, we never reconsider it. Each recursive call carries a `start` marking "you may only pick from here onward."

- **Pattern trigger:** the phrase **"generate all / find every valid ..."** (all subsets, all permutations, all combinations) → **backtracking**. When the *output* is a collection of *constructed things*, you're building a decision tree and walking it.

---

## ① Brute Force

The "generate everything then filter" framing: use the binary-counter idea explicitly. Every subset corresponds to an `n`-bit number `0 .. 2ⁿ-1`; bit `i` set means "include `nums[i]`."

```python
def subsets_bitmask(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):            # 0 .. 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):           # is bit i set?
                subset.append(nums[i])
        result.append(subset)
    return result
```

**Why it's the natural first attempt:** it maps directly onto "each element is in or out," and it's genuinely correct and clean for this exact problem.

**Why we look further:** it works, but it doesn't *generalize*. The moment the problem adds a constraint ("subsets that sum to k," "no two adjacent," "stop early when invalid"), the bitmask can't **prune** — it always builds all `2ⁿ` masks even when a partial choice is already doomed. Backtracking builds subsets incrementally, so it can abandon a bad branch before finishing it. Learn the backtracking version because it's the *reusable* one.

**Complexity:** Time `O(n · 2ⁿ)` (2ⁿ masks × up to n bits each), Space `O(n · 2ⁿ)` for output.

---

## ② Optimised Solution

The clean backtracking template. Record the current `path` at *every* node (not just leaves), and use `start` to only move forward.

```python
def subsets(nums):
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])            # every node is a valid subset — snapshot it
        for i in range(start, len(nums)):
            path.append(nums[i])          # CHOOSE nums[i]
            backtrack(i + 1)              # RECURSE, only elements after i
            path.pop()                    # UN-CHOOSE (undo) to try the next i

    backtrack(0)
    return result
```

**Walk part of the decision tree** for `nums = [1, 2, 3]`:

```
backtrack(0), path=[]        -> record []
  choose 1 -> path=[1]
    backtrack(1)             -> record [1]
      choose 2 -> path=[1,2]
        backtrack(2)         -> record [1,2]
          choose 3 -> [1,2,3] -> record [1,2,3]; pop -> [1,2]
        pop -> [1]
      choose 3 -> path=[1,3]
        backtrack(3)         -> record [1,3]; pop -> [1]
    pop -> []
  choose 2 -> path=[2] ... (records [2], [2,3])
  choose 3 -> path=[3] ... (records [3])
```

Notice the `path.append` / `path.pop` pairing: after fully exploring "1 then 2," we `pop` the 2 to explore "1 then 3." The single shared `path` list is *reused* — un-choose keeps it consistent.

**Why `path[:]` and not `path`?** `path` is one mutable list we keep editing. If we appended `path` itself, every entry in `result` would point to the *same* list and end up empty at the end. `path[:]` takes a **snapshot** (copy) of the current state.

**Why it's correct:** every subset is uniquely determined by its increasing sequence of indices. The `start`-forward loop generates exactly one such increasing sequence per subset — no duplicates, none missed. Recording at every node captures subsets of all lengths.

**Complexity:** Time `O(n · 2ⁿ)` — `2ⁿ` nodes, each doing an `O(n)` copy. Space `O(n)` auxiliary (recursion + path), plus `O(n · 2ⁿ)` for the output itself.

---

## ③ Space Optimization

The output *must* hold all `2ⁿ` subsets — that space is **inherent and unavoidable**; it's the answer, not overhead. The teaching point here is the **output space vs auxiliary space** distinction:

- **Output space:** `O(n · 2ⁿ)` to store the result. You can't shrink this — the problem asks for every subset.
- **Auxiliary space:** the *extra* memory your algorithm uses beyond the output. That's just the recursion stack (depth ≤ `n`) plus the single `path` list (length ≤ `n`) → **`O(n)`**.

So the backtracking solution is already optimal on auxiliary space: `O(n)`. When an interviewer asks "can you do better on space," the sharp answer is: *"The output is exponential and that's inherent, but my auxiliary space is just O(n) — one path list I mutate in place and undo, plus the O(n) recursion depth. Nothing else grows with the input."* Naming that distinction is the strong-hire move.

---

## Java (for Java interviewers)

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> path, List<List<Integer>> result) {
    result.add(new ArrayList<>(path));            // snapshot current subset
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);                        // CHOOSE
        backtrack(nums, i + 1, path, result);     // RECURSE
        path.remove(path.size() - 1);             // UN-CHOOSE
    }
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) | Space (output) |
|---|---|---|---|
| Bitmask | O(n · 2ⁿ) | O(1) | O(n · 2ⁿ) |
| Backtracking | O(n · 2ⁿ) | O(n) | O(n · 2ⁿ) |

---

## Say it out loud (interview narration)

> *"Each element is either in a subset or out, so there are 2ⁿ subsets — the output is exponential by nature, no way around that. I'll build them with backtracking: keep one `path` list, and at each step choose the next element, recurse to decide the rest, then pop it back off to try the next option. I record a copy of the path at every node, because every prefix is itself a valid subset. Using a `start` index that only moves forward means I never generate the same subset twice. Time is O(n·2ⁿ) dominated by the output; auxiliary space is just O(n) for the recursion and the one path list I mutate and undo."*

## Related / follow-ups
- **Subsets II** (LC 90 — duplicates in input; sort, then skip `nums[i] == nums[i-1]` at the same level)
- **Permutations** (LC 46 — order matters, use a `used` set instead of `start`)
- **Combinations** (LC 77 — subsets of fixed size k; prune by length)
- **Combination Sum** (LC 39 — subsets meeting a target)
