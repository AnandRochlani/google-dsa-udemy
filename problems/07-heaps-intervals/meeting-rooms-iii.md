# Meeting Rooms III

> **LeetCode:** 2402. Meeting Rooms III · **Difficulty:** 🔴 Hard · **Pattern:** Two heaps (free rooms + busy rooms) · **Google frequency:** ⭐ high

---

## Problem

You have `n` rooms numbered `0` to `n − 1`, and a list of `meetings` where `meetings[i] = [start, end]` means a meeting occupies the half-open interval `[start, end)`. All start times are **distinct**. Process the meetings **in order of start time** and follow these rules exactly:

- When a meeting is ready to start, it takes the **available room with the lowest number**.
- If **no room is free** at its start time, the meeting **waits** for the room that becomes free **earliest** (ties broken by **lowest room number**). The meeting keeps its **original duration** — so if it had to wait, its end time slides: `delayed_end = room_free_time + (end − start)`.

Return the number of the room that held the **most meetings**. If several rooms tie, return the **lowest-numbered** one.

**Example:** `n = 2`, `meetings = [[0,10],[1,5],[2,7],[3,4]]` → `0`
*(Both rooms end up hosting 2 meetings each; on a tie we return the lower id — room 0.)*

**Constraints that matter:** `1 ≤ n ≤ 100`, but `meetings.length` can be up to `10^5`, and `start`/`end` up to `10^7`. So `n` is tiny, `m` is large. A per-meeting scan of all rooms (`O(m·n)`) is *technically* fine at these limits — but the interviewer wants the scalable answer, which replaces the two linear scans with two heaps: `O(m log m + m log n)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** simulate it. Keep an array `room_end[room]` telling you when each room frees up, plus a `count[room]`. For each meeting (in start order), scan the rooms: if some room is already free, grab the lowest-numbered free one; otherwise scan for the room that frees soonest and delay the meeting onto it. That's a direct transcription of the rules, and it's *correct*.
- **Where it hurts:** every meeting does a full `O(n)` sweep of the rooms — twice in spirit (once to look for a free room, once to find the earliest-freeing one). With `m` up to `10^5` that's fine for `n ≤ 100`, but the moment `n` grows the `O(m·n)` scan is the bottleneck. The scan is repeatedly asking two questions — *"which free room has the lowest id?"* and *"which busy room frees earliest?"* — and re-deriving the answer from scratch each time.
- **The leap:** those two questions are exactly what **heaps** answer in `O(log)`. Keep **two** priority queues. One holds the **free** rooms, keyed by room id, so the smallest id pops first. The other holds the **busy** rooms as `(end_time, room_id)`, so the earliest-freeing room pops first (and Python's tuple order breaks end-time ties by room id — which is *exactly* the tie-break the problem asks for). Before each meeting, "retire" any busy rooms whose end time has already passed back into the free heap.
- **Pattern trigger:** **"assign resources by one priority, reclaim them by another"** → **two heaps**. The instant you see *"lowest-numbered available"* AND *"earliest to free up,"* those are two different orderings over the same rooms — one heap per ordering. That split is the whole trick.

---

## ① Brute Force

Simulate directly: an array of when each room frees, scanned linearly per meeting.

```python
def mostBooked_brute(n, meetings):
    meetings.sort()                 # process in start order
    room_free = [0] * n             # time each room becomes available
    count = [0] * n                 # meetings hosted per room

    for start, end in meetings:
        # is any room already free at `start`? take the lowest-numbered one
        chosen = -1
        for r in range(n):
            if room_free[r] <= start:
                chosen = r
                break               # rooms scanned low→high, so this is lowest id
        if chosen != -1:
            room_free[chosen] = end
        else:
            # nobody free — pick the room that frees earliest, ties → lowest id
            earliest = 0
            for r in range(1, n):
                if room_free[r] < room_free[earliest]:
                    earliest = r    # strict < keeps the lowest id on ties
            room_free[earliest] += (end - start)   # slide the duration on
            chosen = earliest
        count[chosen] += 1

    # most meetings, ties → lowest id
    best = 0
    for r in range(n):
        if count[r] > count[best]:
            best = r
    return best
```

**Why it's the natural first attempt:** it's the rules typed out verbatim — a person literally walks the room list looking for a spot, then for the soonest opening.

**Why it's not enough:** each meeting triggers up to two `O(n)` sweeps, so the whole thing is `O(m·n)`. With `n ≤ 100` that passes here, but it doesn't *generalize*, and in the room the interviewer will ask "what if there were a million rooms?" The scan keeps re-answering two fixed questions — lowest free id, earliest free time — that a heap answers in log time.

**Complexity:** Time `O(m·n)` (plus `O(m log m)` to sort), Space `O(n)`.

---

## ② Optimised Solution

Two heaps. `free` is a min-heap of available **room ids** (lowest pops first). `busy` is a min-heap of `(end_time, room_id)` (earliest-freeing pops first, ties by id — for free). Before each meeting, move every room that's already finished from `busy` back to `free`.

```python
import heapq

def mostBooked(n, meetings):
    meetings.sort()                         # process in start order
    free = list(range(n))                   # min-heap of available room ids
    heapq.heapify(free)                     # [0, 1, ..., n-1] is already a heap
    busy = []                               # min-heap of (end_time, room_id)
    count = [0] * n

    for start, end in meetings:
        # 1. retire every room that has freed up by `start` → back to `free`
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)

        # 2a. a room is free → take the lowest id, run for the full [start, end)
        if free:
            room = heapq.heappop(free)
            heapq.heappush(busy, (end, room))
        # 2b. none free → wait for the earliest-freeing room; keep the duration
        else:
            free_at, room = heapq.heappop(busy)
            heapq.heappush(busy, (free_at + (end - start), room))

        count[room] += 1

    # most meetings, ties → lowest id (strict > keeps the first/lowest)
    best = 0
    for r in range(n):
        if count[r] > count[best]:
            best = r
    return best
```

**Walk the example** `n = 2`, `meetings = [[0,10],[1,5],[2,7],[3,4]]` (already sorted by start):

| Meeting | Retire (end ≤ start) | `free` before | Decision | `busy` after | `count` |
|---|---|---|---|---|---|
| `[0,10]` | none | `[0,1]` | free → room **0**, runs `[0,10)` | `[(10,0)]` | `[1,0]` |
| `[1,5]` | none (10 > 1) | `[1]` | free → room **1**, runs `[1,5)` | `[(5,1),(10,0)]` | `[1,1]` |
| `[2,7]` | none (5 > 2) | `[]` | none free → pop `(5,1)`; delayed end `5 + (7−2) = 10` → room **1** | `[(10,0),(10,1)]` | `[1,2]` |
| `[3,4]` | none (10 > 3) | `[]` | none free → pop earliest `(10,0)` (tie 10 vs 10 → id 0); delayed end `10 + (4−3) = 11` → room **0** | `[(10,1),(11,0)]` | `[2,2]` |

Final `count = [2, 2]`. Tie → lowest id → **room 0**. ✅

Notice the two tie-breaks that fell out for free: the `[3,4]` meeting waited on **room 0** because both rooms freed at time 10, and `(10, 0) < (10, 1)` in the heap. And the final answer picked room 0 over room 1 because `count[r] > count[best]` uses a **strict** `>`, so an equal count never displaces the lower id.

**Why it's correct:** the invariant is that at the moment we handle a meeting, `free` holds exactly the rooms idle at time `start`, and `busy` holds every occupied room keyed by when it frees. The retire loop guarantees that: any room whose `end_time ≤ start` is idle *now*, so we move it over — and because start times are strictly increasing, once a room is retired it stays correctly classified. Rule 1 (lowest free id) is the top of the `free` heap; the wait rule (earliest to free, ties by id) is the top of the `busy` heap, since tuple ordering compares `end_time` first, then `room_id`. A delayed meeting pushes `free_at + (end − start)` — the room's free time plus the meeting's own untouched **duration** — which is precisely the rule.

**Complexity:** Time `O(m log m + m log n)` — the sort, plus each meeting doing a constant number of heap ops on heaps of size ≤ `n`. Every room is retired at most once per meeting it hosted, so the retire loop is amortized `O(m log n)` total. Space `O(n)` for the two heaps and the counts.

---

## ③ Space Optimization

**Already optimal.** The two heaps together hold at most `n` rooms at any instant — a room is in exactly one of `free` or `busy` — and `count` is length `n`. That's `O(n)` auxiliary, and `n` is the number of rooms you must track, so there's nothing to shave: you cannot decide "lowest free id" or "earliest to free" without remembering the state of every room.

```python
# No leaner variant: |free| + |busy| = n at all times (each room is in one heap),
# and count is length n. O(n) is the floor — you must track every room's state.
```

**Complexity:** Time `O(m log m + m log n)`, Space `O(n)`.

> Say it out loud: *"Space is O(n) for the two heaps plus the count array, and that's optimal — every room is in exactly one heap, so the combined size is always n. I can't answer 'lowest free room' or 'soonest to open' without holding all n rooms' state."*

---

## Java (for Java interviewers)

```java
public int mostBooked(int n, int[][] meetings) {
    Arrays.sort(meetings, (a, b) -> Integer.compare(a[0], b[0]));   // by start

    // free rooms: min-heap by room id
    PriorityQueue<Integer> free = new PriorityQueue<>();
    for (int r = 0; r < n; r++) free.add(r);

    // busy rooms: min-heap by (endTime, roomId) — endTime first, then id
    PriorityQueue<long[]> busy = new PriorityQueue<>(
        (a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0])
                               : Long.compare(a[1], b[1]));
    long[] count = new long[n];

    for (int[] m : meetings) {
        long start = m[0], end = m[1];

        // 1. retire rooms that have freed up by `start`
        while (!busy.isEmpty() && busy.peek()[0] <= start) {
            free.add((int) busy.poll()[1]);
        }

        int room;
        if (!free.isEmpty()) {
            // 2a. lowest free id, full [start, end)
            room = free.poll();
            busy.add(new long[]{end, room});
        } else {
            // 2b. earliest-freeing room, keep the duration
            long[] top = busy.poll();
            room = (int) top[1];
            busy.add(new long[]{top[0] + (end - start), room});
        }
        count[room]++;
    }

    int best = 0;
    for (int r = 0; r < n; r++) {
        if (count[r] > count[best]) best = r;   // strict > keeps lowest id on ties
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (per-meeting room scan) | O(m·n + m log m) | O(n) |
| Optimised (two heaps) | O(m log m + m log n) | O(n) |
| Space-optimised | — (none exists) | O(n) |

*(m = number of meetings, n = number of rooms.)*

---

## Say it out loud (interview narration)

> *"Meetings are processed in start order, so first I sort by start. The rules ask two different questions about the rooms — 'which free room has the lowest number?' and 'which busy room frees up first?' — so I keep two heaps. A min-heap of free room ids answers the first; a min-heap of `(end_time, room_id)` answers the second, and its tuple ordering breaks earliest-free ties by the lower id for free, which is exactly the rule. Before each meeting I drain the busy heap of any room that's already finished back into the free heap. If a room's free, I take the smallest id and run the meeting normally. If not, I pop the soonest-freeing room and slide the meeting's full duration onto it. Then I count. At the end I take the room with the most meetings, and because I compare with a strict greater-than, ties naturally resolve to the lowest id. Sorting is O(m log m), the heap work is O(m log n), space is O(n) — and O(n) is optimal because every room lives in exactly one heap."*

Before coding, ask the one clarifying question that shows you read the spec: *"When a meeting has to wait, it keeps its original duration — so its end slides by however long it waited, right?"* That's the detail people trip on, and asking it up front is exactly what Google's rubric rewards.

## Related / follow-ups
- **Meeting Rooms II (LC 253)** — the min-heap warm-up: just count the *peak* number of concurrent rooms needed. Same interval-scheduling DNA, one heap.
- **Meeting Rooms (LC 252)** — can one person attend all meetings? Pure overlap check by sorting.
- **Process Tasks Using Servers (LC 1882)** — near-identical two-heap shape: a free-servers heap keyed by (weight, index) and a busy heap keyed by free-time.
- **Single-Threaded CPU (LC 1834)** — sort by availability, then a heap picks the next job; the "process in time order, pull from a heap" reflex transfers directly.
