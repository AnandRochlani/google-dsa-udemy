# Task Scheduler

> **LeetCode:** 621. Task Scheduler · **Difficulty:** 🟡 Medium · **Pattern:** Heaps & Top-K (greedy + counts) · **Google frequency:** ⭐ high

---

## Problem

Given a list of CPU `tasks` (labeled `A`–`Z`) and an integer `n`, each task takes one unit of time. Between two runs of the **same** task there must be at least `n` units of gap. In each unit the CPU either runs one task or sits **idle**. Return the **minimum total time** to finish all tasks.

**Example:** `tasks = ["A","A","A","B","B","B"]`, `n = 2` → `8`.
One optimal schedule: `A B idle A B idle A B` → 8 units.
`tasks = ["A","A","A","B","B","B"]`, `n = 0` → `6` *(no gap needed).*

**Constraints that matter:** up to `10⁴` tasks, `0 ≤ n ≤ 100`. The answer is driven entirely by the **most frequent task** — it's the bottleneck that forces idle gaps. Only the 26 letter counts matter, so this collapses to a tiny math formula (or a clean heap simulation).

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** simulate time tick by tick — at each unit, run the most-frequent task that's currently "cool" (past its cooldown). That greedy choice is correct, and a heap makes "most frequent available task" cheap.
- **Why most-frequent-first is right:** the task with the highest count is the one that will most often be blocked waiting for its cooldown. Scheduling it as early and often as possible spreads its copies out and lets other tasks fill the gaps it creates. Always run the currently-available task with the greatest remaining count.
- **The heap realization:** a **max-heap** — largest on top — of remaining counts lets you grab the most frequent available task in `O(log 26)`. Each round you pop up to `n+1` distinct tasks (one full cooldown window), decrement them, and push back the ones with counts left. If the heap empties mid-window before you finish all tasks, the elapsed idle time still counts.
- **The math shortcut:** you don't even need to simulate. Let `maxFreq` be the highest count and `numMax` the number of tasks tied at that count. Lay out the `maxFreq` copies of the most frequent task as row anchors, creating `maxFreq − 1` gaps of size `n` between them. The frame size is `(maxFreq − 1) × (n + 1) + numMax`. If there are enough *other* tasks to fill every idle slot, no idles are needed and the answer is just `len(tasks)`. So the answer is `max(len(tasks), frame)`.
- **Pattern trigger:** **"schedule / arrange with a cooldown, minimize idle"** → **greedy on the highest-count item**, realized with a **max-heap** or a closed-form count formula.

---

## ① Brute Force

Tick-by-tick simulation with an explicit cooldown clock: at each time unit, scan all task types for the one with the highest remaining count whose cooldown has expired; run it or idle.

```python
from collections import Counter

def least_interval_brute(tasks, n):
    counts = Counter(tasks)
    next_free = {t: 0 for t in counts}     # earliest time each task may run
    remaining = len(tasks)
    time = 0
    while remaining:
        # pick the available task with the largest remaining count
        best = None
        for t, c in counts.items():
            if c > 0 and next_free[t] <= time:
                if best is None or c > counts[best]:
                    best = t
        if best is None:                   # nothing available → idle
            time += 1
            continue
        counts[best] -= 1
        remaining -= 1
        next_free[best] = time + n + 1     # cooldown
        time += 1
    return time
```

**Why it's the natural first attempt:** it directly enacts the rules — advance one tick at a time, respect cooldowns, greedily run the biggest pile.

**Why it's not enough:** each time unit scans all ≤26 task types, and the total time can include many idle ticks, so it's `O(time × 26)`. It's not asymptotically terrible (26 is constant), but it's clumsy — it literally loops over idle seconds one at a time, which the formula collapses instantly.

**Complexity:** Time `O(total_time × 26)`, Space `O(26)`.

---

## ② Optimised Solution — max-heap simulation

Process one cooldown window (`n+1` slots) per outer round using a max-heap of remaining counts.

```python
import heapq
from collections import Counter

def least_interval(tasks, n):
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]    # max-heap via negation
    heapq.heapify(heap)

    time = 0
    while heap:
        temp = []                           # tasks run this window, to requeue
        for _ in range(n + 1):              # one full cooldown window
            if heap:
                c = heapq.heappop(heap)     # most frequent available (negated)
                if c + 1 < 0:               # still has copies left after this run
                    temp.append(c + 1)      # (c is negative; +1 = one fewer)
            time += 1                        # a run or a forced idle
            if not heap and not temp:
                break                        # everything done; stop early
        for c in temp:
            heapq.heappush(heap, c)         # tasks come off cooldown for next window
    return time
```

**Walk the example** `tasks = ["A","A","A","B","B","B"]`, `n = 2`:

- `counts = {A:3, B:3}`, heap = `[-3, -3]`. Window size `n+1 = 3`.
- **Round 1:** pop `A(-3)` → run A, `-2` left → temp `[-2]`; pop `B(-3)` → run B, `-2` left → temp `[-2,-2]`; heap now empty, but `temp` non-empty so we take an **idle** (3rd slot). `time = 3`. Requeue `[-2,-2]`.
- **Round 2:** run A (`-1` left), run B (`-1` left), idle. `time = 6`. Requeue `[-1,-1]`.
- **Round 3:** run A (`0` left, not requeued), run B (`0` left); heap and temp now empty → `break` after the 2nd slot. `time = 8`.
- → **`8`** ✅ (`A B idle A B idle A B`).

**Why it's correct:** running the highest-count available task each slot maximally spreads the bottleneck task; a window of `n+1` slots is exactly one cooldown period, so a task run at the window's start is legal to run again at the next window's start. Idle slots are only "spent" when no task is available — which the `time += 1` inside the loop naturally accounts for.

**Complexity:** Time `O(total_time)` with `O(log 26) = O(1)` heap ops — effectively `O(N + idle)`. Space `O(26) = O(1)`.

---

## ③ Space Optimization — the O(1) math formula

The heap is already `O(1)` space (≤26 counts), but you can skip the simulation entirely with a closed form — cleaner and `O(N)` time with no per-tick loop:

```python
from collections import Counter

def least_interval_math(tasks, n):
    counts = Counter(tasks)
    max_freq = max(counts.values())
    num_max = sum(1 for c in counts.values() if c == max_freq)
    # frame built around the most frequent task's copies:
    frame = (max_freq - 1) * (n + 1) + num_max
    return max(len(tasks), frame)
```

**How the formula works:** picture `max_freq` copies of the most frequent task as anchors, with `max_freq − 1` gaps of width `n` between them: `(max_freq − 1) × (n + 1)` slots, plus `num_max` for the tasks tied at the top that share the final column. Other tasks slot into the gaps. If there are *more* tasks than the frame has room for, every idle gets filled and the answer is simply `len(tasks)` — hence the `max(...)`.

**Check the example:** `max_freq = 3` (A and B), `num_max = 2`, `n = 2` → `frame = (3−1)×(2+1) + 2 = 6 + 2 = 8`, and `len(tasks) = 6`, so `max(6, 8) = 8` ✅. For `n = 0`: `frame = 2×1 + 2 = 4`, `max(6, 4) = 6` ✅.

**Complexity:** Time `O(N)` (just the counting), Space `O(1)`.

> Both approaches are `O(1)` space; the formula additionally removes the tick-by-tick loop, so it's the tightest solution. The heap is worth knowing because it generalizes when you must output the actual schedule, not just its length.

---

## Java (for Java interviewers)

```java
import java.util.*;

// max-heap simulation
public int leastInterval(char[] tasks, int n) {
    int[] counts = new int[26];
    for (char t : tasks) counts[t - 'A']++;

    PriorityQueue<Integer> heap = new PriorityQueue<>(Collections.reverseOrder());
    for (int c : counts) if (c > 0) heap.offer(c);

    int time = 0;
    while (!heap.isEmpty()) {
        List<Integer> temp = new ArrayList<>();
        for (int i = 0; i < n + 1; i++) {
            if (!heap.isEmpty()) {
                int c = heap.poll();
                if (c - 1 > 0) temp.add(c - 1);
            }
            time++;
            if (heap.isEmpty() && temp.isEmpty()) break;
        }
        heap.addAll(temp);
    }
    return time;
}
```

*(Or the one-liner math version: `frame = (maxFreq - 1) * (n + 1) + numMax; return Math.max(tasks.length, frame);`)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Tick-by-tick simulation | O(total_time × 26) | O(26) |
| Max-heap by window | O(total_time) | O(26) |
| Math formula | O(N) | O(1) |

---

## Say it out loud (interview narration)

> *"The bottleneck is the most frequent task — it forces the idle gaps — so I greedily schedule the highest-count available task each slot. With a max-heap of remaining counts, I process one cooldown window of n+1 slots per round, popping the most frequent tasks, decrementing them, and requeuing the survivors after the window; any slot with nothing available becomes idle. That's O(N) time and O(1) space since there are only 26 letters. But I can skip the simulation entirely: with maxFreq copies of the top task I get maxFreq−1 gaps of size n, so the frame is (maxFreq−1)(n+1) plus the number of tasks tied at the max. If there are more tasks than that frame holds, every idle gets filled and the answer is just the number of tasks — so it's max(len(tasks), frame)."*

## Related / follow-ups
- **Reorganize String** (same "spread the most frequent apart" greedy, n = 1)
- **Rearrange String k Distance Apart** (generalized cooldown with heap)
- **Top K Frequent Elements** (heap keyed on counts)
