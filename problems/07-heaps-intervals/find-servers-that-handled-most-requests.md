# Find Servers That Handled Most Number of Requests

> **LeetCode:** 1606. Find Servers That Handled Most Number of Requests · **Difficulty:** 🔴 Hard · **Pattern:** Two heaps + ordered set · **Google frequency:** ⭐ high

---

## Problem

You have `k` servers numbered `0 … k-1`. Requests come in one at a time. The `i`-th request (0-indexed) arrives at time `arrival[i]` and takes `load[i]` time to finish, so the server that takes it is busy on `[arrival[i], arrival[i] + load[i])`. Assignment follows a strict rule:

- The `i`-th request **prefers** server `i % k`.
- If that server is busy, probe the **next higher id**, wrapping past `k-1` back to `0`, and hand it to the **first free** server you hit.
- If you probe all `k` servers and every one is busy, the request is **dropped**.

A server is *busiest* if it handled the most requests. Return the **ids** of all busiest servers, in any order.

**Example:** `k = 3`, `arrival = [1,2,3,4,5]`, `load = [5,2,3,3,3]` → `[1]`
*(Server 1 ends up handling two requests; everyone else handles one, and request 4 gets dropped because all three servers are busy.)*

**Constraints that matter:** `k` up to `10^5` and `arrival` up to `10^5` requests, with `arrival` **strictly increasing**. That kills the obvious "scan all `k` servers per request" approach — worst case `O(n·k)` ≈ `10^{10}`, a guaranteed TLE. The strictly-increasing arrivals are the gift: a server freed by an earlier request is *definitely* free by the time a later one lands, so we can release servers lazily instead of re-checking clocks.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** keep an `end[]` array — `end[s]` = the time server `s` becomes free. For request `i`, start at `i % k` and walk forward (wrapping) until you find a server whose `end <= arrival[i]`. Assign it, bump its count. It's a direct translation of the rules, and it's *correct*.
- **Where it hurts:** that inner walk can touch all `k` servers on every request. When most servers are busy, you probe almost the whole ring each time — `O(n·k)`. With `k` and `n` both `10^5`, that's `10^{10}` operations. The wasted work is **re-scanning busy servers you already know are busy**, over and over.
- **The leap:** split the world into two sets — **busy** and **free** — and stop looking at busy ones entirely. Keep busy servers in a **min-heap keyed by end time**, so the *soonest-to-finish* is always on top. Before serving request `i`, pop every server whose end time is `<= arrival[i]` and drop it back into the free set. Now the free set holds *exactly* the servers available right now. To honor "first free id at or after `i % k`, wrapping," the free set needs to answer **"smallest id ≥ target, else wrap to smallest id overall"** fast — that's an **ordered set** with a binary search (`ceiling` / `bisect`).
- **Pattern trigger:** *"assign to the next available resource in a ring, by a time rule"* → **min-heap of in-use resources keyed by free-time + an ordered set of idle resources**. The transferable move is **lazy release**: don't poll every resource's clock; let the heap tell you who's free the moment you need someone. Because arrivals only move forward in time, a server released once stays valid — no re-checking.

---

## ① Brute Force

Track each server's free-time in an array. For every request, probe up to `k` servers starting at `i % k`, wrapping, and take the first one that's idle.

```python
def busiest_servers_brute(k, arrival, load):
    end = [0] * k          # end[s] = time server s becomes free (0 = free now)
    count = [0] * k        # requests handled per server
    for i, start in enumerate(arrival):
        for probe in range(k):
            s = (i % k + probe) % k      # walk the ring from the preferred id
            if end[s] <= start:          # first free server wins
                end[s] = start + load[i]
                count[s] += 1
                break
        # if the loop finds nobody, the request is silently dropped
    best = max(count)
    return [s for s, c in enumerate(count) if c == best]
```

**Why it's the natural first attempt:** it's the problem statement typed out line for line — prefer `i % k`, probe forward, take the first free one, drop if none.

**Why it's not enough:** the inner `for probe in range(k)` is the killer. When servers are saturated, nearly every request scans close to all `k` servers before finding one (or giving up). That's `O(n·k)`. With `n = k = 10^5` you're at `10^{10}` operations — comfortably past the time limit. You're re-inspecting servers you *already know* are busy, request after request.

**Complexity:** Time `O(n·k)`, Space `O(k)`.

---

## ② Optimised Solution

Keep two structures. A **min-heap `busy`** of `(end_time, server_id)` so the earliest-finishing server surfaces first. A **sorted set `free`** of idle server ids. Before each request, **lazily release** every server that's finished by now (`end_time <= arrival[i]`) from `busy` into `free`. Then find the target with one binary search: the smallest free id `>= i % k`, or wrap to the smallest free id overall.

```python
import heapq
from sortedcontainers import SortedList

def busiest_servers(k, arrival, load):
    free = SortedList(range(k))     # ids of servers available right now, sorted
    busy = []                       # min-heap of (end_time, server_id)
    count = [0] * k

    for i, start in enumerate(arrival):
        # ── 1. lazily release: everyone finished by 'start' is free again ──
        while busy and busy[0][0] <= start:
            _, sid = heapq.heappop(busy)
            free.add(sid)

        if not free:
            continue                # all k servers busy → drop request i

        # ── 2. first free id >= i % k, else wrap to the smallest free id ──
        prefer = i % k
        j = free.bisect_left(prefer)
        if j == len(free):          # nothing >= prefer → wrap around
            j = 0
        sid = free[j]

        # ── 3. assign ──
        free.remove(sid)
        heapq.heappush(busy, (start + load[i], sid))
        count[sid] += 1

    best = max(count)
    return [s for s, c in enumerate(count) if c == best]
```

**Walk the example** `k = 3`, `arrival = [1,2,3,4,5]`, `load = [5,2,3,3,3]`:

| i | arrival | release (end ≤ arrival) | free before | prefer = i%3 | bisect → id | assign (end) | count |
|---|---|---|---|---|---|---|---|
| 0 | 1 | — | `[0,1,2]` | 0 | id 0 | server 0, ends 6 | `[1,0,0]` |
| 1 | 2 | — | `[1,2]` | 1 | id 1 | server 1, ends 4 | `[1,1,0]` |
| 2 | 3 | — | `[2]` | 2 | id 2 | server 2, ends 7 | `[1,1,1]` |
| 3 | 4 | server 1 (ends 4) → free | `[1]` | 0 | none ≥ 0? id 1 wraps in | server 1, ends 7 | `[1,2,1]` |
| 4 | 5 | — (ends 6,7,7 all > 5) | `[]` | 1 | free empty | **dropped** | `[1,2,1]` |

Final `count = [1, 2, 1]`. Max is 2 at server **1** → return `[1]`. ✅

Notice request 3: `prefer = 0`, but the only free server is id `1`. `bisect_left([1], 0)` returns `0`, so we land on id `1` directly — the "next higher id" rule. Request 4 finds `free` empty and drops, exactly as the rules demand.

**Why it's correct:** the min-heap always exposes the server that frees up soonest, so popping while `busy[0][0] <= start` releases *precisely* the servers idle at time `start` — no more, no less. That's sound because arrivals are strictly increasing: once released, a server stays valid for every later request. The wraparound probe is captured in two lines — `bisect_left(prefer)` gives the first free id `>= prefer`; if that index runs off the end, no free id is `>= prefer`, so the ring wraps and the smallest free id (index `0`) is the answer. Empty `free` means all `k` are busy → drop. Every rule maps to one clean step.

**Complexity:** Time `O(n log k)` — each request does `O(log k)` heap and ordered-set operations, and each server is released at most once amortized. Space `O(k)` — the heap, the free set, and the count array are all bounded by `k`.

> **If `SortedList` isn't allowed** (no `sortedcontainers` in the environment), use the **two-heap trick** for `free`. Keep the free ids in *two* min-heaps split at `i % k`: `avail_hi` holds free ids `>= i % k`, `avail_lo` holds the rest. Prefer popping from `avail_hi`; if it's empty, wrap and pop from `avail_lo`. Because `i % k` shifts by one each step you re-partition lazily as you go. Same `O(n log k)`, just more bookkeeping — reach for `SortedList` first and mention this as the fallback.

---

## ③ Space Optimization

**Already optimal at `O(k)` — and here's why there's no lower floor.** You must know, at any moment, which servers are busy and which are free, plus a per-server request tally to pick the busiest. All three — the `busy` heap, the `free` set, the `count` array — are bounded by the number of servers `k`, never by the number of requests `n`. Requests flow *through* these structures (each one enters `busy` and later leaves), so nothing accumulates with `n`.

```python
# No sub-O(k) variant exists: you must track the state of all k servers.
# The heap + free set never exceed k entries combined (a server is in exactly
# one of "busy" or "free"), and count[] is exactly k longs. That's the floor.
```

**Complexity:** Time `O(n log k)`, Space `O(k)`.

> Say it out loud: *"Space is O(k), and that's optimal — I have to know the status of every server and a count per server, and there are k servers. Nothing grows with the number of requests, because each request just moves a server from free to busy and back."* Naming why `O(k)` is the floor is the strong-hire move.

---

## Java (for Java interviewers)

Java's `TreeSet` gives you `ceiling(target)` — the smallest element `>= target` — which is exactly the wraparound probe, and a `PriorityQueue` is the min-heap.

```java
import java.util.*;

public List<Integer> busiestServers(int k, int[] arrival, int[] load) {
    TreeSet<Integer> free = new TreeSet<>();          // idle server ids, sorted
    for (int i = 0; i < k; i++) free.add(i);
    // min-heap of {endTime, serverId}
    PriorityQueue<int[]> busy = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    int[] count = new int[k];

    for (int i = 0; i < arrival.length; i++) {
        int start = arrival[i];

        // 1. lazily release every server finished by 'start'
        while (!busy.isEmpty() && busy.peek()[0] <= start) {
            free.add(busy.poll()[1]);
        }
        if (free.isEmpty()) continue;                 // all busy → drop

        // 2. first free id >= i % k, else wrap to the smallest free id
        int prefer = i % k;
        Integer sid = free.ceiling(prefer);
        if (sid == null) sid = free.first();          // wraparound

        // 3. assign
        free.remove(sid);
        busy.offer(new int[]{start + load[i], sid});
        count[sid]++;
    }

    int best = 0;
    for (int c : count) best = Math.max(best, c);
    List<Integer> res = new ArrayList<>();
    for (int i = 0; i < k; i++) if (count[i] == best) res.add(i);
    return res;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (probe the ring per request) | O(n·k) | O(k) |
| Optimised (min-heap + ordered set) | O(n log k) | O(k) |
| Space-optimised | — (none exists) | O(k) — already the floor |

*(n = number of requests, k = number of servers.)*

---

## Say it out loud (interview narration)

> *"The brute force is a direct read of the rules: an `end`-time array, and for each request I probe forward from `i % k` until I find a free server. It's correct but it's O(n·k) — when servers saturate I re-scan the whole ring every time, and with n and k both 10^5 that times out. The fix is to stop looking at busy servers. I keep two structures: a min-heap of busy servers keyed by their end time, and an ordered set of free server ids. Before each request I pop the heap for everyone finished by the arrival time and move them into the free set — that's safe because arrivals only increase. Then it's one binary search: the smallest free id at or above `i % k`, and if there's nothing there, I wrap to the smallest free id overall. Empty free set means drop the request. Each request is O(log k), so the whole thing is O(n log k) time and O(k) space, which is optimal since I have to track every server."*

Before you touch code, ask the one clarifying question that proves you read the spec: *"When the preferred server is busy, I probe upward and wrap around, and only drop the request if all k are busy — right?"* That, plus narrating brute-force → optimal out loud, is exactly what Google's General Cognitive Ability (GCA) signal rewards — the interviewer scores *how you think*, not just the final code.

## Related / follow-ups
- **Meeting Rooms II (LC 253)** — min-heap of end times to count overlapping intervals; same "release the soonest-to-finish first" reflex.
- **Task Scheduler (LC 621)** — resource assignment under a cooldown; heap-driven scheduling.
- **The Skyline Problem (LC 218)** — sweep + ordered structure keyed by a time coordinate.
- **Process Tasks Using Servers (LC 2073)** — near-twin: two heaps (free servers by weight, busy servers by free-time) assigning tasks in order.
- **Single-Threaded CPU (LC 1834)** — heap-based "pick the next job by a rule" scheduling.
