# 🎬 Recording Script — Meeting Rooms II
**Pattern: Greedy & Intervals · LeetCode 253 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the interval sweep from Merge Intervals, and the min-heap from the Top-K / Heaps lessons.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an office floor plan. Meeting bars on a timeline overhead; as time sweeps, rooms light up green (in use). At one instant three rooms glow at once.]**

> Google loves this one: *"Here are the day's meetings. How many conference rooms do you need so nobody's ever double-booked?"*
>
> The instinct is to think about the meetings. But the real question is sneakier — it's not about any single meeting, it's about the **busiest instant** of the whole day. The moment the most meetings are running at once — *that's* your room count.
>
> By the end of this video you'll compute that peak in one clean pass with a min-heap, and you'll see the exact reason we track *end times* and not starts. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, three bars on a timeline: `[0,30]` (long), `[5,10]`, `[15,20]`.]**

> One line: **the minimum rooms equals the maximum number of meetings happening at the same time.**
>
> Tiny example: `[0,30]`, `[5,10]`, `[15,20]`. Look at the picture. `[0,30]` runs the whole day. While it's going, `[5,10]` starts — now two meetings overlap, so two rooms. Then `[5,10]` ends at 10. When `[15,20]` starts, `[0,30]` is still going but `[5,10]` is done — so `[15,20]` reuses that freed room.
>
> Peak overlap = 2. Answer: **2 rooms.** Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: for each bar, arrows fan out to count how many others cross its start. A "comparisons" counter climbs.]**

> Brute force: for each meeting, count how many others are running when it starts, and take the max. `[0,30]` — how many overlap it? Both others do at some point. `[5,10]` — overlaps `[0,30]`. And so on.
>
> **[VISUAL: nested arrows, counter climbing n×n.]**
>
> It works, but every meeting re-scans every other meeting — that's O(n²). And it keeps re-deriving concurrency from scratch. We're asking "who overlaps whom" over and over, when we only need *one* number: the peak.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The bars get chopped into "start" markers (green +1) and "end" markers (red −1) on the timeline. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste: we compute overlap per meeting, when all we want is the single busiest moment.
>
> **LEARNER:** So I want peak concurrency. But how do I find it without checking every pair — and how do I know a room is truly free to reuse?
>
> **TEACHER:** Perfect setup. Think of it as events on a timeline: every meeting **start** adds a room, every **end** frees one. Pause and predict: **if I walk time in order, adding one at each start and subtracting one at each end, what does the running count's highest point represent?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: sort meetings by start. A min-heap panel on the right showing "end times of ongoing meetings". Numbers push in and pop out as the sweep advances.]**

> Two equivalent ways to see it. Let me give you the one interviewers expect most — the **min-heap of end times.**
>
> Sort meetings by start. Keep a min-heap holding the *end times* of meetings currently in rooms. The heap's size = rooms in use right now. For each new meeting:
>
> - Peek the heap's smallest end — the meeting that frees up soonest. If that end is ≤ the new meeting's start, that room is already empty — **pop it, reuse the room.**
> - Then push the new meeting's end.
>
> **[VISUAL: `[0,30]` → push 30, heap `[30]`, size 1. `[5,10]` → top 30 > 5, no free room → push 10, heap `[10,30]`, size 2. `[15,20]` → top 10 ≤ 15, free! → pop 10, push 20, heap `[20,30]`, size 2.]**
>
> The heap's *maximum* size across the whole run is the answer. And notice why it's a *min*-heap: the only room that could possibly free up in time is the one whose meeting ends **earliest**. So we always check the smallest end. That's the whole reason for the heap.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Sort by start · min-heap of end times · reuse when earliest end ≤ new start · answer = heap size."]**

> The key move: **sort by start, keep a min-heap of end times; if the earliest end is ≤ the new start, reuse that room, else open a new one — the heap size is your rooms.**
>
> The trigger phrase: *"max concurrent — rooms, CPUs, servers, peak overlap"* → sweep line or min-heap of ends.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Handle empty input, then sort by start and set up the heap.

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda iv: iv[0])   # by start
    heap = []                              # min-heap of end times
```

> **[VISUAL: add chunk 2, highlight.]** For each meeting, reuse a freed room or open a new one.

```python
    for start, end in intervals:
        if heap and heap[0] <= start:      # earliest room already freed
            heapq.heapreplace(heap, end)   # pop earliest end, push new — reuse
        else:
            heapq.heappush(heap, end)      # need a new room
    return len(heap)
```

> `heapreplace` is a pop-then-push in one step. And the final `len(heap)` *is* the peak — because we only ever pop one before pushing one, the heap never shrinks below its high-water mark.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:15`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why each piece.
>
> `sort by start` — we must process meetings in the order they begin, so "is a room free yet?" is a meaningful question.
>
> `heap[0] <= start` — the smallest end time. If the earliest-finishing ongoing meeting is already over by the time this one starts, its room is free.
>
> **LEARNER:** Hold on — why does `len(heap)` at the *end* give the peak? Couldn't the busiest moment have been earlier, and then meetings ended and the heap shrank?
>
> **TEACHER:** Beautiful objection, and here's the subtlety: in this code the heap **never shrinks**. Every iteration either pushes — heap grows by one — or does `heapreplace`, which pops one and pushes one, net zero. It never does a bare pop. So the size only ever climbs or holds. It ends at its maximum, which is exactly the peak concurrency. If we'd written a bare `heappop`, we'd have to track the max separately.
>
> `heapreplace` vs `push` — replace when a room frees (reuse), push when none does (new room). That branch *is* the room-allocation decision.

---

## 9. DRY-RUN THE CODE — `7:30`
*(worked example — prove it, close the loop)*

**[VISUAL: three bars, trace table, heap contents animating.]**

> Run it on `[[0,30],[5,10],[15,20]]`, already sorted by start.

| meeting | heap top | free? (top ≤ start) | action | heap (ends) | rooms |
|---|---|---|---|---|---|
| `[0,30]` | — | — | push 30 | `[30]` | 1 |
| `[5,10]` | 30 | 30 ≤ 5? ❌ | push 10 | `[10, 30]` | 2 |
| `[15,20]` | 10 | 10 ≤ 15? ✅ | replace 10 → 20 | `[20, 30]` | 2 |

> Final heap size = **2**. Exactly the peak we eyeballed. Loop closed.

---

## 9b. THE SWEEP-LINE TWIN — `8:15`
*(interleaving — a second lens on the same peak)*

**[VISUAL: two sorted arrays — starts and ends — with two pointers `i`, `j`. A +1/−1 counter and a `peak` tracker.]**

> There's an equally standard second solution worth knowing — the **sweep line**. Split all starts and all ends into two sorted lists. Walk them together: if the next start comes before the next end, a meeting begins → `rooms += 1`, bump the peak; otherwise a meeting ended → `rooms -= 1`.

```python
def minMeetingRooms_sweep(intervals):
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = peak = 0
    i = j = 0
    while i < len(starts):
        if starts[i] < ends[j]:      # a meeting starts before one ends
            rooms += 1
            i += 1
            peak = max(peak, rooms)
        else:                        # a meeting ended → free a room
            rooms -= 1
            j += 1
    return peak
```

> Same answer, same O(n log n). The strict `<` encodes the endpoint handoff — a meeting ending exactly when another starts passes the room along.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(n²). Heap: O(n log n). Sweep: O(n log n).]**

> Say it: *"Brute force counts overlap per meeting, O(n²). Sorting is n-log-n, and each meeting does one heap op that's log n, so O(n log n) overall. The sweep line is the same, just merging sorted start and end events with a +1/−1 counter."*
>
> Offering both — heap and sweep — and knowing they compute the same peak is a strong signal.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: a worst-case input where every meeting overlaps — heap fills to n. Note: "peak can be n → O(n) floor".]**

> Both are O(n) space, and here's the honest reason you *can't* beat it: if every meeting overlaps every other — think all-day meetings — the peak concurrency is `n` itself. The heap holds all `n` end times; the sweep needs two sorted arrays of size `n`. The answer can be `n`, so the space floor is `n`.
>
> Say it in the room: *"There's no O(1) version — when everything overlaps, the peak is n, so I need O(n) to represent it."* Recognizing the floor *is* the answer.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Car Pooling (LC 1094)". A road with pickup/dropoff points and a capacity meter.]**

> Before the next video, try **Car Pooling**. Passengers board and leave at points along a route; the car has a capacity. Can you complete every trip? It's the *exact same* +1/−1 sweep — except now each event adds or removes a *number* of passengers, and you check against capacity instead of counting rooms. Spot the twin.
>
> Ten minutes first.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Rooms = peak overlap** — reframe from meetings to the busiest instant.
> 2. **Min-heap of end times** — reuse the earliest-freeing room.
> 3. **Or sweep +1/−1** over sorted starts and ends, track the peak.
>
> Memory peg: **count the busiest instant — starts add a room, ends free one.**

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Jump Game" — an array of numbers with a stick figure hopping across.]**

> We've been sweeping *intervals* on a line. Next we keep the greedy mindset but drop the intervals entirely: you're standing on an array, each number is how far you can jump, and you want to know — can you even *reach the end*? Turns out one rolling number answers it. Next up: Jump Game. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
