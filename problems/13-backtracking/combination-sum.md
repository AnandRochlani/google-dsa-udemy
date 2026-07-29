# Combination Sum

> **LeetCode:** 39. Combination Sum · **Difficulty:** 🟡 Medium · **Pattern:** Subsets & Backtracking · **Google frequency:** ⭐ high

---

## Problem

Given an array of **distinct** positive integers `candidates` and a `target`, return **all unique combinations** where the chosen numbers sum to `target`. The **same number may be reused unlimited times**. Two combinations are different only if the *multiset* of chosen numbers differs (order doesn't count).

**Example:** `candidates = [2, 3, 6, 7]`, `target = 7` → `[[2, 2, 3], [7]]` *(2+2+3 = 7 and 7 = 7; note `2` is reused).*

**Constraints that matter:** `1 ≤ candidates.length ≤ 30`, `2 ≤ candidates[i] ≤ 40`, `1 ≤ target ≤ 40`. The number of valid combinations can grow large, so the **output can be exponential** — inherent to "find every combination." The guarantee is that the count of combinations that sum to target fits comfortably (fewer than ~150), but the *search tree* is what we prune.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Try adding candidates one at a time and see which running sums hit the target." Since numbers can repeat, at each step I can either *use the current candidate again* or *move on to the next one*. That branching per candidate is the backtracking signature.

- **The decision tree mental model:** each node holds a current `path` and a `remaining` amount (`target − sum(path)`). From a node you branch on *which candidate to add next*. A **leaf that's a valid answer** is `remaining == 0`. A **dead leaf** is `remaining < 0` (overshot) — we prune it immediately.

- **Reuse ⇒ pass `i`, not `i+1`:** in Subsets/Combinations we recursed with `start = i + 1` to move strictly forward. Here a number can be used again, so we recurse with `start = i` — allowing the *same* candidate next time — but still never going *backward*. That "no backward" rule is what keeps combinations unique: `[2,2,3]` is generated once, never as `[3,2,2]` or `[2,3,2]`.

- **Pruning — the key move:** if `remaining − candidates[i] < 0`, adding `candidates[i]` overshoots, so skip it. **If we sort `candidates` first**, then once one candidate overshoots, *every later (larger) candidate* overshoots too — so we can `break` out of the loop entirely, chopping off whole branches instead of testing them one by one.

- **The backtracking skeleton — same rhythm:** **CHOOSE** a candidate (append, subtract from remaining), **RECURSE** with `start = i` (reuse allowed), then **UN-CHOOSE** (pop it back) to try the next candidate.

- **Pattern trigger:** **"find all combinations that reach a target, reuse allowed"** → backtracking with a `start` index (pass `i` to reuse) + a prune on `remaining`.

---

## ① Brute Force

An **unpruned** version: recurse on every candidate from `start`, only bailing when we've already gone negative — after the fact.

```python
def combination_sum_brute(candidates, target):
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return                            # overshot — but we already recursed to find out
        for i in range(start, len(candidates)):
            path.append(candidates[i])        # CHOOSE
            backtrack(i, remaining - candidates[i])   # RECURSE (i => reuse allowed)
            path.pop()                        # UN-CHOOSE
    backtrack(0, target)
    return result
```

**Why it's the natural first attempt:** it's the direct "try adding each candidate and check the sum" recursion, and it's fully correct.

**Why we look further:** it only detects an overshoot *after* making the recursive call and re-checking `remaining < 0`. It also keeps looping through larger candidates that are guaranteed to overshoot. Sorting + an early prune lets us stop those branches *before* descending. Same worst-case big-O, but dramatically fewer nodes visited in practice.

**Complexity:** Time `O(n^(target/min))` in the worst case (branching factor × depth bounded by target/smallest candidate), Space `O(target/min)` recursion depth + output.

---

## ② Optimised Solution

Sort first, then **prune with `break`**: the moment a candidate overshoots the remaining amount, all bigger candidates will too.

```python
def combination_sum(candidates, target):
    candidates.sort()                         # enables the break-prune
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])            # valid leaf — snapshot
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:     # PRUNE: this and all later (bigger) overshoot
                break
            path.append(candidates[i])        # CHOOSE
            backtrack(i, remaining - candidates[i])   # RECURSE with i => reuse allowed
            path.pop()                        # UN-CHOOSE

    backtrack(0, target)
    return result
```

**Walk part of the decision tree** for `candidates = [2, 3, 6, 7]` (already sorted), `target = 7`:

```
backtrack(0, rem=7)
  choose 2 -> backtrack(0, rem=5)
    choose 2 -> backtrack(0, rem=3)
      choose 2 -> backtrack(0, rem=1)
        2 > 1 -> break (prune 2,3,6,7)   -> dead
      choose 3 -> backtrack(1, rem=0)    -> record [2,2,3] ✅
      choose 6 > 3 -> break
    choose 3 -> backtrack(1, rem=2)
      3 > 2 -> break                     -> dead
    ...
  choose 3 -> backtrack(1, rem=4) ... (no hit)
  choose 6 -> backtrack(2, rem=1) -> 6>1 break
  choose 7 -> backtrack(3, rem=0)        -> record [7] ✅
```

The `break` fires whenever a candidate exceeds `remaining`, cutting off every larger sibling at once.

**Why it's correct:** passing `start = i` allows reuse but forbids going backward, so each combination is generated in exactly one non-decreasing order — unique, none missed. `remaining == 0` captures every valid sum; the `break` only discards candidates that *provably* can't fit (sorted, so `> remaining` ⇒ all following are too).

**Complexity:** Time `O(n^(target/min))` worst case (pruning cuts the constant hugely in practice), Space `O(target/min)` recursion depth + `O(k · #combos)` output.

---

## ③ Space Optimization

The output is inherent — you must store every valid combination. **Output vs auxiliary space:**

- **Output space:** `O(k · #combinations)` where `k` is the average combination length — unavoidable, it's the answer.
- **Auxiliary space:** the recursion stack plus the single `path`. The deepest the recursion goes is `target / min(candidates)` (all smallest candidates), so auxiliary space is `O(target / min)`. Nothing else grows.

Already optimal on auxiliary space — one mutated `path` list and the recursion stack, both bounded by the max combination length. Say it: *"My only extra memory is the recursion depth, capped at target over the smallest candidate, plus the path I mutate and undo — everything else is the required output."*

Sorting is `O(n log n)` time and `O(1)`/`O(log n)` extra space — a cheap price for the pruning payoff.

---

## Java (for Java interviewers)

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    Arrays.sort(candidates);                          // enables break-prune
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, 0, target, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] c, int start, int remaining,
                       List<Integer> path, List<List<Integer>> result) {
    if (remaining == 0) {
        result.add(new ArrayList<>(path));            // valid leaf
        return;
    }
    for (int i = start; i < c.length; i++) {
        if (c[i] > remaining) break;                  // PRUNE
        path.add(c[i]);                               // CHOOSE
        backtrack(c, i, remaining - c[i], path, result); // RECURSE (i => reuse)
        path.remove(path.size() - 1);                 // UN-CHOOSE
    }
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) | Space (output) |
|---|---|---|---|
| Unpruned backtracking | O(n^(T/min)) | O(T/min) | O(k · #combos) |
| Sorted + break-prune | O(n^(T/min)) worst, far fewer nodes in practice | O(T/min) | O(k · #combos) |

---

## Say it out loud (interview narration)

> *"I'll backtrack, building combinations that sum to the target. Because numbers can be reused, when I recurse I pass the same index `i` so the current candidate stays available, but I never go backward — that keeps every combination unique. I sort the candidates first so I can prune: the moment a candidate exceeds the remaining amount, every larger one does too, so I `break`. Choose a candidate and subtract it, recurse, then pop it to try the next. When remaining hits zero I record a copy. The output is exponential and inherent; my auxiliary space is just the recursion depth — target over the smallest candidate — plus the one path I mutate and undo."*

## Related / follow-ups
- **Combination Sum II** (LC 40 — each number used once + duplicates in input; `start = i+1` and skip same-level dupes)
- **Combination Sum III** (LC 216 — fixed count k, numbers 1–9, no reuse)
- **Subsets** (LC 78 — same `start`-index skeleton, no target)
- **Coin Change II** (LC 518 — *count* combinations for an amount; DP, not enumeration)
