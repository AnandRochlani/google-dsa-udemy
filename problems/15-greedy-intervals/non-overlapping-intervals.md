# Non-overlapping Intervals

> **LeetCode:** 435. Non-overlapping Intervals · **Difficulty:** 🟡 Medium · **Pattern:** Greedy & Intervals · **Google frequency:** medium

---

## Problem

Given an array of intervals, return the **minimum number of intervals you must remove** so that the rest are non-overlapping.

**Example:** `intervals = [[1,2], [2,3], [3,4], [1,3]]` → `1` *(remove `[1,3]`; the remaining `[1,2], [2,3], [3,4]` don't overlap — note intervals that only touch at an endpoint, like `[1,2]` and `[2,3]`, are considered non-overlapping).*

**Constraints that matter:** `n` up to ~10⁵ → we need O(n log n). "Minimum removals" is the same as "**maximum intervals we can keep** that don't overlap" — the classic **activity-selection** problem. That reframing is the whole key.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Try removing different intervals until nothing overlaps, minimizing removals." That's exponential — 2ⁿ subsets. Not viable.
- **Reframe:** Removing the *fewest* is the same as **keeping the most** non-overlapping intervals. Answer = `n − (max kept)`. Now it's an optimization: pack in as many compatible intervals as possible.
- **The greedy leap — sort by END, not start:** Think of intervals as meetings you want to attend back-to-back. To fit the most, always keep the meeting that **finishes earliest**, because it leaves the most room afterward for everything else. So sort by end time, walk left to right tracking the end of the last interval you kept; if the next interval **starts before** that end, it conflicts — drop it (count a removal); otherwise keep it and advance the "last end."
- **Why earliest-end is safe (exchange argument):** among all intervals that could be your next pick, the one ending soonest never blocks anything a later-ending choice would allow — its end is ≤ every alternative's end, so any interval compatible with a later-ending pick is also compatible with the earliest-ending one. Greedy never loses.
- **Pattern trigger:** **"max non-overlapping intervals / min removals / activity selection"** → **sort by END, greedily keep earliest finishers.** Contrast with Merge Intervals, which sorts by *start*. Choosing the sort key by what you're optimizing is the lesson.

---

## ① Brute Force

Try every subset (or recurse keep/drop on each interval), find the largest non-overlapping set, return `n − that`.

```python
def erase_brute(intervals):
    intervals.sort(key=lambda iv: iv[0])
    n = len(intervals)

    def best(i, last_end):
        if i == n:
            return 0
        # option 1: skip interval i
        res = best(i + 1, last_end)
        # option 2: keep it, if compatible
        if intervals[i][0] >= last_end:
            res = max(res, 1 + best(i + 1, intervals[i][1]))
        return res

    return n - best(0, float("-inf"))
```

**Why it's the natural first attempt:** "keep or drop each interval" is the obvious decision tree, and it does find the true maximum kept.

**Why it's not enough:** the keep/drop branching is O(2ⁿ). Even memoized on `(i, last_end)` the state space is awkward because `last_end` is continuous. The greedy below collapses all of it.

**Complexity:** Time `O(2ⁿ)`, Space `O(n)` recursion.

---

## ② Optimised Solution

Sort by end time; greedily keep every interval that starts at or after the last kept end.

```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda iv: iv[1])        # sort by END
    kept = 0
    last_end = float("-inf")
    for start, end in intervals:
        if start >= last_end:                   # compatible → keep it
            kept += 1
            last_end = end
        # else: overlaps the last kept one → this one is removed
    return len(intervals) - kept
```

**Walk the example** `[[1,2], [2,3], [3,4], [1,3]]`. Sorted by end → `[[1,2], [2,3], [1,3], [3,4]]`:

| interval | `start >= last_end`? (`last_end`) | action | kept | last_end |
|---|---|---|---|---|
| `[1,2]` | 1 ≥ −∞ ✅ | keep | 1 | 2 |
| `[2,3]` | 2 ≥ 2 ✅ | keep | 2 | 3 |
| `[1,3]` | 1 ≥ 3 ❌ | remove | 2 | 3 |
| `[3,4]` | 3 ≥ 3 ✅ | keep | 3 | 4 |

Kept 3 of 4 → removals = `4 − 3 = 1`. ✅

**Why it's correct:** the exchange argument — sorting by end and always taking the earliest finisher leaves maximal room for the remainder, and any optimal solution can be transformed into this greedy one without reducing the count. Using `>=` (not `>`) encodes that touching endpoints don't count as overlap.

**Complexity:** Time `O(n log n)` (the sort), Space `O(1)` beyond the sort.

---

## ③ Space Optimization

Already optimal. After sorting, we hold only two things: a running `kept` counter and `last_end`. No extra data structure grows with the input.

> **Say it out loud:** *"Beyond the sort, it's O(1) — just a counter and the last kept end."* The only variable cost is the sort's scratch space (`O(log n)` for an in-place sort). There's nothing to optimize away; naming that is the complete answer.

**Complexity:** Time `O(n log n)`, Space `O(1)` auxiliary.

---

## Java (for Java interviewers)

```java
public int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));  // by END
    int kept = 0;
    long lastEnd = Long.MIN_VALUE;
    for (int[] iv : intervals) {
        if (iv[0] >= lastEnd) {
            kept++;
            lastEnd = iv[1];
        }
    }
    return intervals.length - kept;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (keep/drop subsets) | O(2ⁿ) | O(n) |
| Optimised (sort by end + greedy) | O(n log n) | O(1) |

---

## Say it out loud (interview narration)

> *"Minimum removals equals maximum kept, so this is activity selection. The greedy insight is to sort by end time, not start — always keeping the interval that finishes earliest leaves the most room for the rest, and an exchange argument shows that's optimal. I sweep once tracking the end of the last interval I kept; if the next one starts before that end it conflicts, so I count it as removed, otherwise I keep it and advance. O(n log n) from the sort, O(1) extra. The `>=` versus `>` detail matters here since intervals that only touch don't overlap."*

## Related / follow-ups
- **Merge Intervals** (LC 56 — sort by *start* instead)
- **Minimum Number of Arrows to Burst Balloons** (LC 452 — same earliest-end greedy, counting groups instead of removals)
- **Maximum Length of Pair Chain** (LC 646 — identical activity-selection greedy)
- **Meeting Rooms II** (LC 253 — count max overlap rather than remove)
