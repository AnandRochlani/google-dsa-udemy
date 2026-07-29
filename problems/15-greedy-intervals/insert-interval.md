# Insert Interval

> **LeetCode:** 57. Insert Interval · **Difficulty:** 🟡 Medium · **Pattern:** Greedy & Intervals · **Google frequency:** ⭐ high

---

## Problem

You're given a list of **non-overlapping** intervals sorted by start time, and a single `newInterval`. Insert `newInterval` into the list so the result is still sorted and non-overlapping (merging where necessary). Return the updated list.

**Example:** `intervals = [[1,3], [6,9]]`, `newInterval = [2,5]` → `[[1,5], [6,9]]` *(the new interval overlaps `[1,3]`, so they fuse into `[1,5]`; `[6,9]` is untouched).*

Another: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]` → `[[1,2],[3,10],[12,16]]` *(the new interval swallows `[3,5]`, `[6,7]`, `[8,10]`).*

**Constraints that matter:** the input is **already sorted and non-overlapping** — that's the gift. Because of it, we do **not** need to sort (no O(n log n)); a single linear pass in O(n) suffices, and that's what an interviewer is looking for.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Just append `newInterval`, then run the full Merge Intervals algorithm." Correct, but it re-sorts a list that was already sorted — throwing away the fact that the input is ordered. That's O(n log n) when O(n) is available.
- **Where it hurts:** You're re-establishing order you were *handed for free*.
- **The leap:** Sweep once and split the timeline into three zones relative to `newInterval`:
  1. **Left of it:** intervals that end *before* `newInterval` starts (`end < new.start`) — these can't overlap, copy them as-is.
  2. **Overlapping it:** intervals where `start <= new.end` and `end >= new.start` — absorb them by expanding `newInterval` to `min` of starts and `max` of ends.
  3. **Right of it:** intervals that start *after* `newInterval` ends (`start > new.end`) — copy them as-is.
  The trick is to emit `newInterval` (now possibly grown) exactly once, right between zones 1 and 3.
- **Pattern trigger:** **"already-sorted intervals + insert/merge one"** → **linear three-zone sweep, no re-sort.** Recognizing that pre-sorted input removes the log factor is the interview signal.

---

## ① Brute Force

Append the new interval and reuse the general Merge Intervals routine (sort, then sweep).

```python
def insert_brute(intervals, newInterval):
    intervals = intervals + [newInterval]
    intervals.sort(key=lambda iv: iv[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**Why it's the natural first attempt:** if you already solved Merge Intervals, this is a one-line reduction — just add the new interval and re-merge.

**Why it's not enough:** the `sort` is O(n log n), but the input was *already sorted*. We're paying a log factor for order we already had. Fine as a fallback answer, but not the intended one.

**Complexity:** Time `O(n log n)`, Space `O(n)`.

---

## ② Optimised Solution

One linear pass, three zones: copy-before, merge-overlap, copy-after.

```python
def insert(intervals, newInterval):
    result = []
    i, n = 0, len(intervals)
    s, e = newInterval[0], newInterval[1]

    # Zone 1: intervals strictly before newInterval
    while i < n and intervals[i][1] < s:
        result.append(intervals[i])
        i += 1

    # Zone 2: absorb every interval that overlaps newInterval
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    result.append([s, e])

    # Zone 3: intervals strictly after newInterval
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

**Walk the example** `[[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]` (`s=4, e=8`):

| phase | interval | test | action |
|---|---|---|---|
| Zone 1 | `[1,2]` | end 2 < 4 ✅ | copy → `[[1,2]]` |
| Zone 1 | `[3,5]` | end 5 < 4 ❌ | stop Zone 1 |
| Zone 2 | `[3,5]` | start 3 ≤ 8 ✅ | s=min(4,3)=3, e=max(8,5)=8 |
| Zone 2 | `[6,7]` | start 6 ≤ 8 ✅ | s=3, e=max(8,7)=8 |
| Zone 2 | `[8,10]` | start 8 ≤ 8 ✅ | s=3, e=max(8,10)=10 |
| Zone 2 | `[12,16]` | start 12 ≤ 10 ❌ | stop Zone 2 → append `[3,10]` |
| Zone 3 | `[12,16]` | — | copy → result `[[1,2],[3,10],[12,16]]` |

**Why it's correct:** because the input is sorted and non-overlapping, the intervals split cleanly into the three contiguous zones — everything that overlaps `newInterval` forms one unbroken run (you can't have a non-overlapping interval sandwiched between two overlapping ones). Expanding `s`/`e` with `min`/`max` across that run yields exactly the merged interval, emitted once.

**Complexity:** Time `O(n)` (each interval visited once), Space `O(n)` for the output.

---

## ③ Space Optimization

The output list is inherent — we return up to `n+1` intervals, so `O(n)` output space is the floor. There's no auxiliary structure to trim: we already use only a few integer variables (`i`, `s`, `e`) beyond the result.

> Already optimal on *auxiliary* space: `O(1)` extra beyond the returned list. Unlike Merge Intervals there's no sort, so there isn't even sort scratch space to worry about. This is the cleanest possible interval solution — one pass, constant extra memory.

**Complexity:** Time `O(n)`, Space `O(1)` auxiliary beyond output.

---

## Java (for Java interviewers)

```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> result = new ArrayList<>();
    int i = 0, n = intervals.length;
    int s = newInterval[0], e = newInterval[1];

    while (i < n && intervals[i][1] < s) result.add(intervals[i++]);

    while (i < n && intervals[i][0] <= e) {
        s = Math.min(s, intervals[i][0]);
        e = Math.max(e, intervals[i][1]);
        i++;
    }
    result.add(new int[]{s, e});

    while (i < n) result.add(intervals[i++]);

    return result.toArray(new int[result.size()][]);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (append + re-sort) | O(n log n) | O(n) |
| Optimised (three-zone sweep) | O(n) | O(n) output |

---

## Say it out loud (interview narration)

> *"The easy answer is to append the new interval and re-run Merge Intervals — but that sorts a list that's already sorted, so it's O(n log n) for no reason. Instead I sweep once and split into three zones: copy every interval that ends before the new one starts, then absorb the contiguous run that overlaps by taking min of starts and max of ends, emit that merged interval once, and copy the rest. Because the input is sorted and non-overlapping, the overlapping intervals are guaranteed to be one unbroken run — so it's a clean O(n) pass with O(1) extra space."*

## Related / follow-ups
- **Merge Intervals** (LC 56 — the general unsorted version this reduces to)
- **Non-overlapping Intervals** (LC 435 — greedy removal)
- **Interval List Intersections** (LC 986 — two-pointer merge of two lists)
- **My Calendar I** (LC 729 — insert with a "reject if overlap" rule)
