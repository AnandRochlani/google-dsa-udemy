# My Calendar I

> **LeetCode:** 729. My Calendar I · **Difficulty:** 🟡 Medium · **Pattern:** Intervals / balanced BST (TreeMap) · **Google frequency:** ⭐ high

---

## Problem

Design a `MyCalendar` class that books events without ever **double-booking**. Each event is a half-open interval `[start, end)` — it covers `start` up to but **not including** `end`. Call `book(start, end)`; return `true` and record the event if it does **not** overlap any event already on the calendar, otherwise return `false` and record nothing.

Two half-open intervals `[s1, e1)` and `[s2, e2)` overlap **iff** `s1 < e2 AND s2 < e1`. Because the ends are exclusive, an event that starts exactly where another ends — `[10, 20)` then `[20, 30)` — does **not** conflict; they just touch.

**Example:**

```
book(10, 20) → true    # calendar empty, goes in
book(15, 25) → false   # 15 < 20 and 10 < 25 → overlaps [10,20), rejected
book(20, 30) → true    # starts exactly where [10,20) ends → touches, no overlap
```

**Constraints that matter:** up to `10^4` calls to `book`, with `0 <= start < end <= 10^9`. So `10^4` bookings, each potentially scanning all prior ones, is `10^8` in the worst case — borderline but the real signal Google wants is: *can you get each `book` down to `O(log n)`?* The values go to `10^9`, so you cannot index by time — you need an ordered structure keyed by the interval start.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Keep a list of everything I've booked. When a new event comes in, walk the list and check it against each one." That's completely correct and you should say it out loud — it's the honest baseline. The only question the interviewer is really asking is how you shrink the per-booking cost.
- **Where it hurts:** every `book` re-scans **all** prior intervals, even the ones nowhere near the new event. If I'm booking `[500, 510)`, I don't care about an event at `[0, 5)` — but the brute force checks it anyway. That's `O(n)` wasted work per call, `O(n²)` total.
- **The leap:** an overlap can only come from an interval that's *close* in time. If I keep my bookings **sorted by start**, then the only two candidates that could possibly clash with a new `[start, end)` are (1) the booking with the **largest start ≤ start** — the one just to my left — and (2) the booking with the **smallest start > start** — the one just to my right. Binary-search to those two neighbors, check just them, done. Everything else is provably too far away.
- **Pattern trigger:** **"insert into a set of intervals, reject on overlap, values too big to bucket"** → **ordered map / balanced BST keyed by start** (`TreeMap` in Java, `SortedList`/`bisect` in Python). The transferable move: *sort by one endpoint so a conflict can only hide in your immediate neighbors, then binary-search to them.*

---

## ① Brute Force

Keep every booked interval in a plain list. On each `book`, scan them all and apply the overlap test `s1 < e2 and s2 < e1`.

```python
class MyCalendar:
    def __init__(self):
        self.events = []                      # list of (start, end)

    def book(self, start: int, end: int) -> bool:
        for s, e in self.events:              # check against every prior event
            if start < e and s < end:         # the overlap condition
                return False                  # conflict → reject, record nothing
        self.events.append((start, end))      # no conflict → record it
        return True
```

**Why it's the natural first attempt:** it's a direct translation of the problem — "does this new event hit anything I've already got?" — and the overlap check is the whole trick. Get this working first; it's a correct answer, just not the fast one.

**Why it's not enough:** every call touches every prior event, so `book` is `O(n)` and the sequence of `n` bookings is `O(n²)`. At `n = 10^4` that's `10^8` comparisons — it may squeak by, but it signals you stopped at the obvious. The waste is that most of those events are far away in time and could never overlap.

**Complexity:** Time `O(n)` per `book`, `O(n²)` total, Space `O(n)`.

---

## ② Optimised Solution

Keep the intervals **sorted by start**. To check a new `[start, end)`, binary-search for its position and inspect only the **left neighbor** (largest start ≤ `start`) and the **right neighbor** (smallest start > `start`). If neither overlaps, insert. Python's `sortedcontainers.SortedList` gives ordered insert + binary search in one structure.

```python
from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.events = SortedList()            # kept sorted by (start, end)

    def book(self, start: int, end: int) -> bool:
        # index where (start, end) would be inserted, keeping order
        i = self.events.bisect_left((start, end))

        # right neighbor: smallest start >= our start.
        # It overlaps iff its start < our end.
        if i < len(self.events) and self.events[i][0] < end:
            return False

        # left neighbor: the event just before i.
        # It overlaps iff its end > our start.
        if i > 0 and self.events[i - 1][1] > start:
            return False

        self.events.add((start, end))         # no conflict → record
        return True
```

**Walk one example** — the calls `book(10,20)`, `book(15,25)`, `book(20,30)`:

| Call | `events` before | `i` = bisect | Right neighbor check | Left neighbor check | Result | `events` after |
|---|---|---|---|---|---|---|
| `book(10,20)` | `[]` | 0 | none (i = len) | none (i = 0) | **true** | `[(10,20)]` |
| `book(15,25)` | `[(10,20)]` | 1 | none (i = len) | `events[0]=(10,20)`, `end 20 > start 15` → **overlap** | **false** | `[(10,20)]` |
| `book(20,30)` | `[(10,20)]` | 1 | none (i = len) | `events[0]=(10,20)`, `end 20 > start 20`? `20 > 20` is **false** → OK | **true** | `[(10,20),(20,30)]` |

Notice the last row: `[10,20)` and `[20,30)` merely touch. The strict `>` (not `>=`) is exactly what lets touching intervals coexist — that's the half-open semantics baked into the comparison.

**Why it's correct:** the list is sorted by start, so any interval that could overlap `[start, end)` must sit adjacent to the insertion point. Anything left of the left neighbor has an even smaller start *and* (since prior inserts never overlapped) an end ≤ the left neighbor's end ≤ ... ≤ `start`, so it can't reach us. Anything right of the right neighbor has an even larger start ≥ the right neighbor's start ≥ `end`, so it starts after we end. Checking the two immediate neighbors is therefore sufficient — if both clear the test, no interval overlaps.

**Complexity:** Time `O(log n)` per `book` (binary search) plus `O(log n)` (`SortedList` insert), Space `O(n)`.

> **Clean simple-list version** (no third-party import — good when the interviewer says "standard library only"). Same idea with `bisect` over a parallel list; insertion is `O(n)` because a Python list shifts elements, but the *search* is `O(log n)` and the code is dead simple:
>
> ```python
> import bisect
>
> class MyCalendar:
>     def __init__(self):
>         self.events = []                     # sorted list of (start, end)
>
>     def book(self, start: int, end: int) -> bool:
>         i = bisect.bisect_left(self.events, (start, end))
>         if i < len(self.events) and self.events[i][0] < end:
>             return False                     # right neighbor starts before we end
>         if i > 0 and self.events[i - 1][1] > start:
>             return False                     # left neighbor ends after we start
>         self.events.insert(i, (start, end))  # O(n) shift, but keeps order
>         return True
> ```

---

## ③ Space Optimization

**Already optimal.** You must remember every accepted booking to reject future conflicts against it — there is no way to forget an event and still guarantee correctness — so `O(n)` space is the floor, not overhead. The `SortedList` stores exactly the `n` accepted intervals and nothing more.

```python
# No space-optimised variant exists: every accepted interval must be retained
# to test future bookings, so O(n) is the minimum possible.
```

**Complexity:** Time `O(log n)` per `book`, Space `O(n)`.

> Say it out loud: *"Space is O(n) and that's forced — I have to keep every event I accepted, because any of them could conflict with a future booking. There's nothing to roll away."* Naming why the floor exists beats hand-waving about "storing the events."

---

## Java (for Java interviewers)

`TreeMap<start, end>` is the textbook fit: `floorKey` gives the largest start ≤ ours (left neighbor), `ceilingKey` the smallest start ≥ ours (right neighbor). Both are `O(log n)`.

```java
import java.util.TreeMap;

class MyCalendar {
    private final TreeMap<Integer, Integer> calendar;   // start -> end

    public MyCalendar() {
        calendar = new TreeMap<>();
    }

    public boolean book(int start, int end) {
        Integer prevStart = calendar.floorKey(start);    // largest start <= start
        Integer nextStart = calendar.ceilingKey(start);  // smallest start >= start

        // left neighbor overlaps iff its end > our start
        if (prevStart != null && calendar.get(prevStart) > start) {
            return false;
        }
        // right neighbor overlaps iff its start < our end
        if (nextStart != null && nextStart < end) {
            return false;
        }

        calendar.put(start, end);                        // no conflict → record
        return true;
    }
}
```

---

## Complexity Summary

| Approach | Time (per `book`) | Space |
|---|---|---|
| Brute force (scan all) | O(n) | O(n) |
| Optimised — `SortedList` / `TreeMap` | O(log n) | O(n) |
| Simple-list `bisect` | O(log n) search, O(n) insert | O(n) |
| Space-optimised | — (none exists) | O(n) — must retain every event |

*(n = number of accepted bookings so far.)*

---

## Say it out loud (interview narration)

> *"First, let me pin the overlap rule: two half-open intervals `[s1,e1)` and `[s2,e2)` clash exactly when `s1 < e2 and s2 < e1` — and because the ends are exclusive, `[10,20)` and `[20,30)` don't clash, they touch. The brute force is a list I scan on every booking — O(n) per call, O(n²) total. To speed it up I keep the events sorted by start, so a conflict can only come from my two immediate neighbors: the one just left with the largest start ≤ mine, and the one just right. I binary-search to them and check only those two, which is O(log n) a booking. In Java that's a TreeMap with floorKey and ceilingKey; in Python a SortedList or a bisect into a sorted list. Space is O(n) and that's forced — I have to keep every accepted event to test future ones against it."*

Before you code, ask the one clarifying question that proves you read the spec: *"The intervals are half-open, right — so an event ending at 20 and one starting at 20 don't conflict?"* That's the detail people miss, and asking it early is exactly what Google's GCA rubric rewards.

## Related / follow-ups
- **My Calendar II (LC 731)** — allow double-booking but reject a **triple** booking; now you track overlap counts, not just presence.
- **My Calendar III (LC 732)** — return the maximum number of concurrent events (the "k-booking") — a sweep-line / difference-map problem.
- **Meeting Rooms II (LC 253)** — minimum rooms for a set of intervals; same overlap DNA, solved with a min-heap of end times.
- **Range Module (LC 715)** — track, add, and query arbitrary ranges — the industrial-strength version of interval bookkeeping.
