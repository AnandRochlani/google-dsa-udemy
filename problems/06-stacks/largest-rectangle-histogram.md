# Largest Rectangle in Histogram

> **LeetCode:** 84. Largest Rectangle in Histogram · **Difficulty:** 🔴 Hard · **Pattern:** Stacks · **Google frequency:** medium

---

## Problem

Given an array `heights` where each entry is the height of a bar of width `1` in a histogram, find the area of the **largest rectangle** that can be formed within the histogram. The rectangle's height is limited by the shortest bar it spans.

**Example:** `heights = [2, 1, 5, 6, 2, 3]` → `10`. The best rectangle spans bars at indices 2 and 3 (heights 5 and 6) with height `5` and width `2` → area `5 × 2 = 10`.

**Constraints that matter:** `1 ≤ n ≤ 10⁵` and heights up to `10⁴`. O(n²) (~10¹⁰) is too slow — we want **O(n)**. The core difficulty: a rectangle's height is the **minimum bar** over its span, so you must find, for each bar, how far it can extend left and right before hitting something shorter.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Try every rectangle." Fix a left edge, extend right, track the minimum height so far, and multiply `min_height × width` at each step. That's every subarray — O(n²).
- **Reframe that helps:** every maximal rectangle is *capped by some bar* — pick a bar and let it be the **shortest** bar of the rectangle. Then the rectangle's height is that bar's height, and its width is: how far left can I go before a **shorter** bar, plus how far right, minus… i.e. `height[i] × (right_smaller − left_smaller − 1)`. So the whole problem reduces to: **for each bar, find the nearest shorter bar to its left and to its right.**
- **Where the naïve version hurts:** finding "nearest shorter bar on each side" by scanning is O(n) per bar → O(n²) again. That "nearest smaller element" scan is doing repeated work over the same bars.
- **The leap:** "nearest smaller element" is the textbook **monotonic stack** job. Keep a stack of bar indices with **increasing heights** (a *monotonic stack* = values only ever increase, or only ever decrease, from bottom to top; here, increasing). When a new bar is **shorter** than the top of the stack, that new bar is the "right boundary" (first shorter bar to the right) for the bar being popped — and the element now beneath it on the stack is that bar's "left boundary." So the moment we pop a bar, **we know both its boundaries** and can compute its full rectangle in O(1).
- **Pattern trigger:** **"rectangle / span limited by the nearest smaller element on each side"** → **monotonic increasing stack**. The pop event is where the area gets finalized.

---

## ① Brute Force

For each pair (or each left edge), track the running minimum height and compute area.

```python
def largest_rectangle_brute(heights):
    n = len(heights)
    best = 0
    for i in range(n):
        min_h = heights[i]
        for j in range(i, n):
            min_h = min(min_h, heights[j])   # min bar over span [i, j]
            best = max(best, min_h * (j - i + 1))
    return best
```

**Why it's the natural first attempt:** it directly enumerates every possible rectangle span `[i, j]`, and maintaining `min_h` incrementally is a small optimization over recomputing it.

**Why it's not enough:** two nested loops over n bars → **O(n²)**. At n = 10⁵ that's ~5 × 10⁹ iterations → **Time Limit Exceeded**.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

One pass with a monotonic **increasing** stack of indices. When a bar shorter than the stack top arrives, pop and finalize the popped bar's rectangle. A sentinel `0` appended at the end flushes everything.

```python
def largest_rectangle(heights):
    stack = []                     # indices, heights increasing bottom -> top
    best = 0
    # append a trailing 0 so every real bar gets popped and measured
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]          # the bar we're finalizing
            # left boundary = the new stack top (nearest shorter bar to the left);
            # if stack empty, this bar extends all the way to the left edge
            left = stack[-1] if stack else -1
            width = i - left - 1                   # span between the two shorter bars
            best = max(best, height * width)
        stack.append(i)
    return best
```

**Walk `heights = [2, 1, 5, 6, 2, 3]`** (with the trailing sentinel `0` at index 6). Stack holds indices; heights in parentheses:

| i | h | pops → area computed | stack after |
|---|---|---|---|
| 0 | 2 | — | `[0]` (2) |
| 1 | 1 | pop 0 (2≥1): h=2, left=-1, width=1−(−1)−1=1, area=**2** | `[1]` (1) |
| 2 | 5 | — | `[1,2]` (1,5) |
| 3 | 6 | — | `[1,2,3]` (1,5,6) |
| 4 | 2 | pop 3 (6≥2): h=6, left=2, width=4−2−1=1, area=6; pop 2 (5≥2): h=5, left=1, width=4−1−1=2, area=**10** | `[1,4]` (1,2) |
| 5 | 3 | — | `[1,4,5]` (1,2,3) |
| 6 | 0 | pop 5 (3≥0): h=3,left=4,width=6−4−1=1,area=3; pop 4 (2≥0): h=2,left=1,width=6−1−1=4,area=8; pop 1 (1≥0): h=1,left=−1,width=6−(−1)−1=6,area=6 | `[6]` |

Best seen = **10** (from popping bar 2, height 5, width 2). ✅

**Why it's correct:** the stack keeps indices in increasing-height order. When bar `i` is shorter than the top, bar `i` is the **first shorter bar to the right** of the popped bar, and the element now on top is the **first shorter bar to the left** (everything between them was ≥ the popped height, so the popped bar can span that whole width at its own height). `width = i − left − 1` is exactly that maximal span. The trailing `0` guarantees every remaining bar is eventually popped and measured. Using `>=` when popping handles equal heights correctly — a bar of equal height is treated as a valid right boundary, and any area it would have contributed is recovered when *it* gets popped later, so nothing is missed.

**Complexity:** Time `O(n)` — each index is pushed once and popped once. Space `O(n)` for the stack.

---

## ③ Space Optimization

The **O(n) stack is inherent**. Worst case is a strictly increasing histogram (`[1, 2, 3, …, n]`): no bar is ever shorter than the top until the sentinel, so all n indices sit on the stack simultaneously. You genuinely need to remember every un-finalized bar, so you can't drop below O(n) auxiliary space for the single-pass method.

```python
# No sub-O(n) space trick here — the stack size is forced by increasing runs.
```

Alternative *formulations* (not smaller in space):

- **Two explicit boundary arrays** — precompute `left_smaller[i]` and `right_smaller[i]` with two monotonic-stack passes, then one pass for areas. Cleaner to reason about, but it uses **more** memory (two O(n) arrays + the stack). Same O(n) class, strictly more constant factor.
- **Divide and conquer** — recurse on the minimum bar. O(n log n) average but **O(n²)** worst case, and O(n) recursion stack. Worse.

> Honest verdict: *"The stack is O(n) and that's unavoidable for an increasing histogram — every bar stays unresolved until the end. I'll keep the single-pass stack; it's optimal on time and can't beat O(n) space."*

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## Java (for Java interviewers)

```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();   // indices, increasing heights
    int best = 0, n = heights.length;
    for (int i = 0; i <= n; i++) {
        int h = (i == n) ? 0 : heights[i];       // trailing sentinel
        while (!stack.isEmpty() && heights[stack.peek()] >= h) {
            int height = heights[stack.pop()];
            int left = stack.isEmpty() ? -1 : stack.peek();
            int width = i - left - 1;
            best = Math.max(best, height * width);
        }
        stack.push(i);
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (every span) | O(n²) | O(1) |
| Optimised (monotonic stack) | O(n) | O(n) |
| Two boundary arrays | O(n) | O(n) (larger constant) |
| Divide & conquer | O(n log n) avg / O(n²) worst | O(n) |

---

## Say it out loud (interview narration)

> *"Every rectangle is capped by its shortest bar, so for each bar I want the largest width it can span at its own height — which is bounded by the nearest shorter bar on each side. Finding 'nearest smaller element' by scanning is O(n²). The monotonic stack does it in one pass: I keep indices with increasing heights, and the moment a shorter bar arrives, the bar I pop has that shorter bar as its right boundary and the new stack top as its left boundary, so I compute its full rectangle right there — height times (i − left − 1). A trailing zero flushes the stack so every bar is measured. That's O(n) time; the stack is O(n) and that's inherent because an increasing histogram keeps every bar unresolved until the end."*

## Related / follow-ups
- **Maximal Rectangle** (LC 85) — run this histogram algorithm on each row of a binary matrix
- **Trapping Rain Water** (LC 42) — monotonic stack, "trap water between bars"
- **Daily Temperatures** (LC 739) / **Next Greater Element** (LC 496) — the nearest-greater cousins
- **Sum of Subarray Minimums** (LC 907) — nearest-smaller boundaries used for contribution counting
- **Remove K Digits** (LC 402) — monotonic stack to build the smallest number
