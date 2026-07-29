# Merge Intervals

> **LeetCode:** 56. Merge Intervals · **Difficulty:** 🟡 Medium · **Pattern:** Greedy & Intervals · **Google frequency:** ⭐ high

---

## Problem

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return the non-overlapping intervals that cover all the input intervals.

**Example:** `intervals = [[1,3], [2,6], [8,10], [15,18]]` → `[[1,6], [8,10], [15,18]]` *(because `[1,3]` and `[2,6]` overlap — they touch at 2–3 — so they collapse into `[1,6]`).*

**Constraints that matter:** `n` up to ~10⁴, and coordinates up to 10⁴. A naive "compare every pair and keep merging until nothing changes" is O(n²) or worse; sorting gets us to O(n log n). Note intervals arrive **in arbitrary order** — that's the whole reason we have to sort first.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Two intervals merge if they overlap, so let me compare every pair, merge the ones that touch, and repeat until the set stops changing." That works but it's messy — one merge can create a new overlap with a third interval, so you loop again and again.
- **Where it hurts:** The overlaps are scattered because the input is unordered. `[8,10]` sits between two intervals that belong together. You keep re-scanning to find who overlaps whom.
- **The leap:** **Sort by start time.** Once sorted, any interval that overlaps the one you're currently building must come *immediately next* — there's nowhere else for it to hide, because everything after it starts even later. So you sweep left to right holding one "current" merged interval: if the next interval starts at or before `current.end`, they overlap, so stretch `current.end` to the max of the two ends. Otherwise there's a gap — freeze `current` into the answer and start a fresh one.
- **Pattern trigger:** **"merge / overlap / combine intervals"** → **sort by start, then sweep, overlap when `next.start <= current.end`.** This sort-then-sweep skeleton is the backbone of almost every interval problem.

---

## ① Brute Force

Repeatedly scan all pairs; whenever two overlap, merge them and restart. Stop when a full pass makes no merge.

```python
def merge_brute(intervals):
    intervals = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        result = []
        used = [False] * len(intervals)
        for i in range(len(intervals)):
            if used[i]:
                continue
            a, b = intervals[i]
            for j in range(i + 1, len(intervals)):
                if used[j]:
                    continue
                c, d = intervals[j]
                if a <= d and c <= b:          # they overlap
                    a, b = min(a, c), max(b, d)
                    used[j] = True
                    changed = True
            result.append([a, b])
        intervals = result
    return intervals
```

**Why it's the natural first attempt:** it's the literal definition of the task — "find any two overlapping intervals and fuse them" — applied until convergence.

**Why it's not enough:** each pass is O(n²), and a chain of overlaps can force many passes → up to O(n³). It also ignores the structure that ordering would give us.

**Complexity:** Time `O(n³)` worst case, Space `O(n)`.

---

## ② Optimised Solution

Sort by start, sweep once, and extend the current interval whenever the next one overlaps.

```python
def merge(intervals):
    intervals.sort(key=lambda iv: iv[0])       # sort by start
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last = merged[-1]
        if start <= last[1]:                   # overlap → extend
            last[1] = max(last[1], end)
        else:                                  # gap → new interval
            merged.append([start, end])
    return merged
```

**Walk the example** `[[1,3], [2,6], [8,10], [15,18]]`:

| next interval | `merged[-1]` before | `start <= last.end`? | action | `merged` after |
|---|---|---|---|---|
| — | — | — | seed | `[[1,3]]` |
| `[2,6]` | `[1,3]` | 2 ≤ 3 ✅ | extend end to max(3,6)=6 | `[[1,6]]` |
| `[8,10]` | `[1,6]` | 8 ≤ 6 ❌ | gap → append | `[[1,6],[8,10]]` |
| `[15,18]` | `[8,10]` | 15 ≤ 10 ❌ | gap → append | `[[1,6],[8,10],[15,18]]` |

**Why it's correct:** after sorting by start, every interval's start is ≥ all previous starts. So the only interval that can overlap the current merged block is the very next one; if *it* doesn't overlap (`start > last.end`), nothing further can either, because later starts are even larger. Taking `max` of the ends guarantees we never shrink a block — e.g. `[1,9]` then `[2,5]` stays `[1,9]`, not `[1,5]`.

**Complexity:** Time `O(n log n)` (dominated by the sort), Space `O(n)` for the output (or `O(log n)` auxiliary for the sort itself).

---

## ③ Space Optimization

The output list is inherent — we have to return the merged intervals, and in the worst case (no overlaps at all) that's `n` intervals, so `O(n)` output is unavoidable.

What you *can* do is merge **in place** on the sorted array, using a write pointer, so you allocate no extra list beyond the answer:

```python
def merge_inplace(intervals):
    intervals.sort(key=lambda iv: iv[0])
    w = 0                                   # index of last written interval
    for start, end in intervals[1:]:
        if start <= intervals[w][1]:
            intervals[w][1] = max(intervals[w][1], end)
        else:
            w += 1
            intervals[w] = [start, end]
    return intervals[:w + 1]
```

> Beyond that, space is already optimal: sorting is the only heavy step and Python's Timsort uses `O(n)` auxiliary; an in-place heapsort would make the *auxiliary* space `O(1)`, but the returned list is still `O(n)` because the problem demands we hand back the intervals. Say so out loud — recognizing that the output size itself is the floor is the mature answer.

**Complexity:** Time `O(n log n)`, Space `O(1)` auxiliary beyond the output.

---

## Java (for Java interviewers)

```java
public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> merged = new ArrayList<>();
    for (int[] iv : intervals) {
        if (merged.isEmpty() || iv[0] > merged.get(merged.size() - 1)[1]) {
            merged.add(iv);
        } else {
            merged.get(merged.size() - 1)[1] =
                Math.max(merged.get(merged.size() - 1)[1], iv[1]);
        }
    }
    return merged.toArray(new int[merged.size()][]);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (repeat-until-stable) | O(n³) | O(n) |
| Optimised (sort + sweep) | O(n log n) | O(n) output |
| In-place sweep | O(n log n) | O(1) aux |

---

## Say it out loud (interview narration)

> *"The intervals come unordered, so overlaps are scattered — that's what makes the brute-force pair-merging loop ugly and O(n³). My key move is to sort by start time. After that, anything that overlaps my current block has to be the very next interval, so I sweep once, holding one merged interval: if the next start is ≤ my current end, I stretch the end to the max of the two; otherwise there's a gap, so I close this block and open a new one. That's O(n log n), all from the sort. The output has to be O(n) since we return the intervals, but I can merge in place to keep the extra space O(1)."*

## Related / follow-ups
- **Insert Interval** (LC 57 — merge one new interval into an already-sorted list, no full sort needed)
- **Non-overlapping Intervals** (LC 435 — sort by *end*, greedily keep the most)
- **Meeting Rooms II** (LC 253 — count max concurrent overlaps)
- **Interval List Intersections** (LC 986 — two-pointer over two sorted interval lists)
