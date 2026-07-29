# Meeting Rooms II

> **LeetCode:** 253. Meeting Rooms II · **Difficulty:** 🟡 Medium · **Pattern:** Greedy & Intervals · **Google frequency:** ⭐ high

---

## Problem

Given an array of meeting time intervals `[start, end]`, return the **minimum number of conference rooms** required so that no two overlapping meetings share a room.

**Example:** `intervals = [[0,30], [5,10], [15,20]]` → `2` *(the meeting `[0,30]` runs the whole time; `[5,10]` needs a second room while it's live; `[15,20]` can reuse the room `[5,10]` freed at 10 — so 2 rooms total).*

**Constraints that matter:** `n` up to ~10⁴. The answer is exactly the **maximum number of meetings that are ever simultaneously in progress** — the peak concurrency. Everything reduces to computing that peak efficiently, in O(n log n).

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each meeting, count how many others overlap it, and the max is the answer." That's O(n²) and asks the wrong question — you don't need per-meeting overlap counts, you need the single busiest instant.
- **Reframe to a timeline:** Picture events on a time axis. Every **start** is `+1` room in use; every **end** is `−1`. Walk time in order and track the running count — its **peak** is the rooms you need. This "sweep line" turns the geometry into a running sum.
- **The heap version (most common answer):** Sort meetings by **start**. Keep a **min-heap of end times** of meetings currently occupying rooms. For each new meeting, if the earliest-ending ongoing meeting has already finished (`heap top <= new.start`), pop it — that room is free and reusable. Then push the new meeting's end. The heap's size at any moment = rooms in use; its **maximum size** is the answer. (Or simply: heap size at the end, since we only ever pop one before pushing one.)
- **Why the earliest end?** The meeting that frees up soonest is the only one that could possibly make room for the next start — so it's the one to check. That's why we keep ends in a *min*-heap.
- **Pattern trigger:** **"max concurrent intervals / rooms / CPUs / peak overlap"** → **sweep line (+1/−1) or min-heap of end times.** Peak-concurrency is the recognition signal.

---

## ① Brute Force

For every meeting, scan all others and count overlaps; the maximum overlap count (including itself) is the rooms needed.

```python
def min_rooms_brute(intervals):
    rooms = 0
    for i in range(len(intervals)):
        s_i, e_i = intervals[i]
        count = 0
        for j in range(len(intervals)):
            s_j, e_j = intervals[j]
            # meeting j is in progress during meeting i's start
            if s_j <= s_i < e_j:
                count += 1
        rooms = max(rooms, count)
    return rooms
```

**Why it's the natural first attempt:** "how many meetings overlap this one" is the literal reading of the room requirement.

**Why it's not enough:** O(n²) comparisons, and it re-derives concurrency from scratch at every meeting instead of sweeping once.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

**Min-heap of end times.** Sort by start; reuse a room when its meeting has ended.

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda iv: iv[0])       # by start
    heap = []                                  # min-heap of end times
    for start, end in intervals:
        if heap and heap[0] <= start:          # earliest room freed up
            heapq.heapreplace(heap, end)       # pop earliest end, push new
        else:
            heapq.heappush(heap, end)          # need a new room
    return len(heap)
```

**Walk the example** `[[0,30], [5,10], [15,20]]` (already sorted by start):

| meeting | heap top (earliest end) | free? | action | heap (ends) | rooms |
|---|---|---|---|---|---|
| `[0,30]` | — | — | push 30 | `[30]` | 1 |
| `[5,10]` | 30 | 30 ≤ 5? ❌ | push 10 | `[10, 30]` | 2 |
| `[15,20]` | 10 | 10 ≤ 15? ✅ | replace 10 → 20 | `[20, 30]` | 2 |

Final heap size = **2**. ✅

**Alternative — sweep line** (equally standard, sometimes cleaner):

```python
def minMeetingRooms_sweep(intervals):
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = peak = 0
    i = j = 0
    while i < len(starts):
        if starts[i] < ends[j]:                # a meeting starts before one ends
            rooms += 1
            i += 1
            peak = max(peak, rooms)
        else:                                  # a meeting ended → free a room
            rooms -= 1
            j += 1
    return peak
```

**Why it's correct:** the heap holds exactly the meetings currently occupying rooms; we only ever add a room when no ongoing meeting has ended by the new start, so the heap size tracks true concurrency and its peak is the minimum rooms. The sweep-line version computes the same peak by merging the sorted start/end events with a `+1/−1` counter. Using `<` (strict) in the sweep encodes that a meeting ending exactly when another starts can hand off the same room.

**Complexity:** Time `O(n log n)` (sort + heap ops), Space `O(n)` for the heap.

---

## ③ Space Optimization

The `O(n)` is inherent to both approaches: the heap can hold all `n` meetings when they all overlap (e.g. `[[0,10],[1,10],...]`), and the sweep line needs the two sorted event arrays. You can't get below `O(n)` extra in the worst case because the peak itself can be `n`.

> The sweep-line version has a small edge: after sorting into `starts` and `ends`, it uses only integer pointers and a counter — but those two sorted arrays are still `O(n)`. So both are `O(n)`; there's no `O(1)` version. Recognizing that peak concurrency can be `n` (hence the space floor is `n`) is the honest answer.

**Complexity:** Time `O(n log n)`, Space `O(n)`.

---

## Java (for Java interviewers)

```java
public int minMeetingRooms(int[][] intervals) {
    if (intervals.length == 0) return 0;
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));  // by start
    PriorityQueue<Integer> heap = new PriorityQueue<>();           // min-heap of ends
    for (int[] iv : intervals) {
        if (!heap.isEmpty() && heap.peek() <= iv[0]) {
            heap.poll();            // reuse the freed room
        }
        heap.offer(iv[1]);
    }
    return heap.size();
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (per-meeting overlap count) | O(n²) | O(1) |
| Min-heap of end times | O(n log n) | O(n) |
| Sweep line (sorted starts/ends) | O(n log n) | O(n) |

---

## Say it out loud (interview narration)

> *"The number of rooms is just the peak number of meetings happening at once. Brute force counts overlaps per meeting in O(n²). Better: sort by start and keep a min-heap of end times of ongoing meetings. For each new meeting, if the earliest-ending one has already finished, I pop it — that room is reusable — then push the new end. The heap size is rooms in use, so its size at the end is the answer, O(n log n). Equivalently I can sweep a +1/−1 counter over sorted start and end events and take the peak. Both are O(n) space because when everything overlaps, the peak is n."*

## Related / follow-ups
- **Meeting Rooms I** (LC 252 — can one person attend all? just check any overlap)
- **Merge Intervals** (LC 56 — sort by start, sweep)
- **Car Pooling** (LC 1094 — same +1/−1 sweep with capacities)
- **My Calendar III** (LC 732 — running max concurrency as bookings arrive)
- **Employee Free Time** (LC 759 — merge then find gaps)
