# 🎬 Recording Script — Task Scheduler
**Pattern: Heaps & Top-K (greedy + counts) · LeetCode 621 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** max-heap via negation (K Closest, Median); counting (Top K Frequent).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a CPU timeline. Tasks A A A B B B must be scheduled with cooldown gaps. Idle slots appear as gray blocks: A B _ A B _ A B. A counter: "total time = 8".]**

> Google, OS flavor: *"A CPU runs tasks. The same task can't run twice within a cooldown of `n` seconds — it either waits, or the CPU sits idle. What's the minimum time to finish everything?"*
>
> Most people reach for a heap here, and that's a completely valid, hireable answer. But this problem has a secret: the entire thing collapses into a *single line of arithmetic* once you see what's really driving it. We'll build the heap version first — because it teaches the greedy idea — then earn the formula. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: tasks = ["A","A","A","B","B","B"], n = 2. One valid schedule laid out: A B idle A B idle A B, 8 slots. Below: same tasks, n = 0 → 6.]**

> The problem in one line: **return the minimum total time to run all tasks, given a cooldown of `n` between two runs of the same task.**
>
> Tiny example: three A's, three B's, cooldown `n = 2`. One optimal schedule is `A B idle A B idle A B` — 8 units. With `n = 0`, no gaps needed, just 6. Hold the 8.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a clock ticking second by second; at each tick, all 26 task types get scanned for "available and highest count"; idle seconds tick by one at a time.]**

> The literal simulation: tick by tick, at each second scan all task types for the one with the highest remaining count whose cooldown has expired. Run it, or idle if nobody's ready.
>
> Second 1: A is highest → run A, put it on cooldown. Second 2: A still cooling, B is highest → run B. Second 3: both cooling → forced idle. Second 4: A's cooldown expired → run A…
>
> **[VISUAL: the clock crawls through every second including the idle ones, a "×26 scan" badge flashing each tick.]**
>
> It works, but it literally loops over every single second — including idle ones — scanning all task types each time. When cooldowns force long stretches of idle, we're crawling through dead air one second at a time.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The task piles A:3, B:3 shown as bars; the tallest bar pulses. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Let's find what actually drives the answer. The task with the *highest count* is the bottleneck — it's the one that keeps hitting its cooldown and forcing gaps. Scheduling it as early and often as legally possible spreads its copies out, and the other tasks fill the gaps it creates.
>
> **LEARNER:** So the greedy rule is: each slot, run the *available* task with the greatest remaining count. And "give me the max repeatedly" is exactly a max-heap's job.
>
> **TEACHER:** You've got the engine. Pause and predict: **if I process one full cooldown window — `n+1` slots — at a time, popping the most-frequent available tasks and requeuing the ones with copies left, how does that guarantee no task violates its cooldown?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it)*

**[VISUAL: a max-heap triangle of counts [3,3] at the top. A window of n+1 = 3 slots. Pop A, pop B, then the window's 3rd slot is idle; survivors -1 requeue.]**

> **TEACHER:** Here's the frame. A cooldown of `n` means a window of `n+1` slots is exactly one cooldown period. If I run task A at the *start* of a window, it's legal to run A again at the start of the *next* window — the window width guarantees the gap.
>
> So: each round, take up to `n+1` distinct tasks from a **max-heap of remaining counts** — the most frequent first. Decrement each, set the survivors aside, and after the window, push the survivors back. Any window slot with nobody available becomes a forced idle, and we count it.
>
> **LEARNER:** Why *distinct* tasks within the window — why can't I just run A three times in a row if it's the biggest pile?
>
> **TEACHER:** Because that's the cooldown itself — the same task can't repeat inside one window. Popping distinct tasks per window *is* how the heap enforces the rule. The bottleneck task appears once per window, and the windows are spaced exactly a cooldown apart. That's why greedy-highest-first is optimal: it packs the bottleneck as tightly as the rules allow.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Max-heap of counts. Each round, run n+1 distinct top tasks; idle any empty slot; requeue survivors."]**

> The key move: **greedily run the highest-count available task each slot, processing one `n+1` window at a time with a max-heap; idle any slot with nothing ready, and requeue tasks that still have copies.**

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1.]**

> Count the tasks, then build a max-heap of counts — negate, since `heapq` is min-only.

```python
import heapq
from collections import Counter

def least_interval(tasks, n):
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]    # max-heap via negation
    heapq.heapify(heap)
    time = 0
```

> **[VISUAL: chunk 2, the window loop.]** Process one cooldown window per outer round.

```python
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
```

> **[VISUAL: chunk 3.]** After the window, the survivors come off cooldown — push them back.

```python
        for c in temp:
            heapq.heappush(heap, c)
    return time
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight the negation, the window loop, the early break.]**

> Walk the *why*.
>
> `[-c for c in ...]` then `heapify` — negated counts turn the min-heap into a max-heap, so `heappop` hands back the *most* frequent task. `c + 1` decrements it (c is negative, so +1 is one fewer copy); if it's still below zero, there are copies left, so it goes to `temp` to be requeued *after* the window — never within it, which is the cooldown.
>
> `time += 1` sits *inside* the window loop, next to the pop — so it ticks whether we ran a task or hit a forced idle. That single line is how idle time gets counted without a separate idle bookkeeping.
>
> **LEARNER:** What's the `if not heap and not temp: break` for? Doesn't the window always run `n+1` times?
>
> **TEACHER:** Sharp — that's the "don't pad the final window" guard. Once the heap *and* the requeue buffer are both empty, every task is placed; any remaining slots in this window would be *trailing* idles we don't need — the CPU just stops. Without that break, you'd overcount time at the very end. It only breaks when truly nothing is left, so mid-schedule idles still count correctly.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: heap [-3,-3], window size 3; each round animates pops, idle, requeue; time counter climbing.]**

> Run it: `A:3, B:3`, `n = 2`, window size 3.

| round | slot actions | time | requeue |
|---|---|---|---|
| 1 | run A (→-2), run B (→-2), idle (heap empty, temp not) | 3 | [-2,-2] |
| 2 | run A (→-1), run B (→-1), idle | 6 | [-1,-1] |
| 3 | run A (→0, done), run B (→0, done) → break, both empty | 8 | — |

> Total **8.** ✅ — matching `A B idle A B idle A B`. Note round 3 breaks after 2 slots, no trailing idle. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: "Simulation: O(total_time). Heap ops: O(log 26)=O(1). Space O(26)=O(1)."]**

> Out loud: *"There are only 26 task types, so every heap operation is O(log 26), effectively constant. The work is proportional to total time — runs plus idles — so it's about O(N + idle) time and O(1) space. Clean, and it generalizes if I ever need to output the actual schedule, not just its length."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:50`
*(depth + honesty — the O(1) formula)*

**[VISUAL: maxFreq copies of A as anchors with n-wide gaps between them; other tasks dropping into the gaps; the frame width measured.]**

> The heap is already O(1) space — 26 counts. But you can skip the simulation *entirely* with a closed-form formula, and it's the tightest answer:

```python
from collections import Counter

def least_interval_math(tasks, n):
    counts = Counter(tasks)
    max_freq = max(counts.values())
    num_max = sum(1 for c in counts.values() if c == max_freq)
    frame = (max_freq - 1) * (n + 1) + num_max
    return max(len(tasks), frame)
```

> Here's the picture. Lay the `max_freq` copies of the bottleneck task as anchors. Between them are `max_freq − 1` gaps, each `n+1` wide counting the anchor — that's `(max_freq − 1) × (n + 1)` slots. Add `num_max` for the tasks tied at the top sharing the final column. That's the *frame.*
>
> **LEARNER:** But what if there are so many *other* tasks that they overflow the gaps?
>
> **TEACHER:** Then there are no idles at all — every slot is a real task — and the answer is just `len(tasks)`. That's why it's `max(len(tasks), frame)`: the frame is the idle-constrained lower bound; when tasks are plentiful they fill every gap and the count of tasks wins.
>
> Check: `max_freq = 3`, `num_max = 2`, `n = 2` → `frame = 2×3 + 2 = 8`, `len = 6` → `max = 8` ✅. For `n = 0` → `frame = 2×1 + 2 = 4`, `max(6, 4) = 6` ✅. **O(N) time, O(1) space, no loop.**

---

## 12. YOUR TURN (active recall) — `10:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Reorganize String (LC 767)". A blank editor.]**

> Before the next video, try **Reorganize String** — rearrange a string so no two adjacent characters match. That's Task Scheduler with `n = 1`: spread the most frequent character apart using a max-heap of counts, always placing the top-two available. Same greedy, same heap. Ten minutes.

---

## 13. LOCK IT IN — `11:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **The most frequent task is the bottleneck** — it dictates the idle gaps.
> 2. **Greedy highest-first via a max-heap**, one `n+1` window per round, requeue survivors.
> 3. **The formula collapses it:** `max(len(tasks), (maxFreq−1)(n+1) + numMax)`.
>
> The peg: **schedule with cooldown → spread the biggest pile; frame it around the most frequent task.**

---

## 14. CLIFFHANGER — `11:45`
*(open loop to next lesson — chapter close)*

**[VISUAL: a montage of the chapter's heaps — size-k, max-heap, two-heaps — collapsing into one icon. A blurred title: "Dynamic Programming".]**

> That closes the heaps chapter. Notice the through-line: every problem was "I only need the *extreme* — the top, the closest, the middle, the most frequent — not the whole order," and a heap delivered it in O(log k) a shot. Whenever you catch yourself about to sort just to grab a few, that's the heap tapping your shoulder.
>
> Next chapter, the pattern that scares people most and rewards them the hardest — where the answer to a big problem is built from answers to smaller overlapping ones. Dynamic programming. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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

// or the O(1) math version:
//   int frame = (maxFreq - 1) * (n + 1) + numMax;
//   return Math.max(tasks.length, frame);
```
