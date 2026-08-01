# 🎬 Recording Script — Meeting Rooms III
**Pattern: Two heaps (free rooms + busy rooms) · LeetCode 2402 · Hard · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the min-heap from Meeting Rooms II, and the half-open interval rule from My Calendar I — both come back here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor with a room-scheduling simulation. Submit → a red "Wrong Answer — expected 0, got 1" banner slams in.]**

> Google onsite. The interviewer says: *"n rooms, a list of meetings. A meeting takes the lowest-numbered free room — and if nothing's free, it waits for the earliest room to open up. Which room hosts the most meetings?"*
>
> You simulate it. Clean code. Passes the sample. You submit — **Wrong Answer.**
>
> Here's the brutal part: your algorithm was right. You missed *one clause in the spec* — when a meeting waits, its end time **slides**. It keeps its full duration, just shifted later. Miss that, and every delayed meeting corrupts the timeline after it.
>
> By the end of this video you'll have that clause nailed, plus the two-heap pattern that turns this Hard into a machine — and it's a pattern Google reuses across a whole family of scheduling problems. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, two room boxes labeled 0 and 1, and four meetings listed:]**

```
n = 2 rooms
meetings = [0,10], [1,5], [2,7], [3,4]
answer → room 0
```

> The whole problem in one line: **process meetings in start order; each takes the lowest-numbered free room, or waits for the earliest room to free up — return the room that hosted the most.**
>
> Two rules with teeth. Rule one: a ready meeting grabs the **lowest-numbered** available room. Rule two: if nobody's free, it waits for the room that opens **earliest** — ties go to the lower room number — and it keeps its **original duration**, so its end time slides by however long it waited.
>
> And it's half-open, `[start, end)` — a meeting ending at 10 and one starting at 10 don't clash. Same rule as My Calendar I.
>
> Our tiny example: two rooms, four meetings. The answer is room **0** — and how it wins is sneakier than it looks. Hold that thought.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: two arrays on screen — `room_free = [0, 0]` and `count = [0, 0]`. A "rooms scanned" counter at top-right, ticking as arrows sweep across the room list.]**

> Let's do what your brain does first: an array `room_free`, one slot per room, saying when each room opens up. For every meeting, scan the rooms.
>
> Meeting `[0,10]`. Scan left to right — room 0 is free at time 0. Take it. `room_free = [10, 0]`. Counter ticks.
>
> Meeting `[1,5]`. Scan again — room 0 busy till 10, room 1 free. Take room 1. `room_free = [10, 5]`.
>
> **[VISUAL: each scan sweeps an arrow across ALL rooms; the counter climbs.]**
>
> Meeting `[2,7]`. Scan — nobody's free. Now a **second** scan: who opens earliest? Room 1, at time 5. The meeting waits till 5, then runs its full 5 units: `room_free[1]` becomes `5 + 5 = 10`.
>
> Meeting `[3,4]`. Scan — nobody free. Scan again — both rooms open at 10, tie goes to room 0. It waits till 10, runs its 1 unit. `room_free = [11, 10]`. Final count: two meetings each — tie, so room **0**.
>
> **[VISUAL: the counter freezes, then morphs into "m × n = 10^5 × n" with a red glow.]**
>
> Right answer. But look at that counter — every meeting swept the *entire* room list, sometimes twice. That's `O(m·n)`.

---

## 4. THE PAIN POINT + PREDICT — `2:50`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The two scan-arrows highlighted, each labeled with the question it keeps re-asking: "lowest free id?" and "earliest to free?". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste. Every single meeting, I re-derive the answers to the *same two questions* from scratch: "which free room has the lowest number?" and "which busy room opens first?" Full sweep, every time.
>
> **LEARNER:** Hang on though — the constraints say `n` is at most a hundred. Ten to the fifth meetings times a hundred rooms… that actually passes. Why am I not done?
>
> **TEACHER:** It passes *here*, and in the room you should say exactly that — knowing your solution fits the limits is a real signal. But the very next sentence out of the interviewer's mouth will be *"what if there were a million rooms?"* So here's your think: I keep re-asking two fixed questions — **what data structure answers "give me the minimum" in log time instead of a scan?** Pause the video.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:40`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the room list splits into TWO piles — a green "FREE" pile ordered by room id, and a red "BUSY" pile ordered by end time. Each pile shaped like a heap triangle with the minimum glowing on top.]**

> **TEACHER:** A heap. But here's the twist that makes this problem — you need **two** of them, because the two questions rank the rooms by *different things*.
>
> "Lowest free room number" — that's a min-heap of **room ids**. Smallest id sits on top, pop it in log time.
>
> "Earliest room to open" — that's a min-heap of **(end_time, room_id)** pairs. Earliest end time sits on top.
>
> Think of a car rental desk. One rack holds keys for cars *on the lot*, sorted by parking spot — grab the nearest. A separate board tracks cars *out on rental*, sorted by return time — if the lot's empty, you know exactly which car comes back first. Two racks, two orderings, same cars.
>
> **LEARNER:** Do I really need two, though? Couldn't one heap of `(end_time, room_id)` do it all — a free room is just one whose end time already passed?
>
> **TEACHER:** Tempting — and it breaks on rule one. Say rooms 3 and 1 are both free. One heap keyed by end time would hand you whichever *finished first* — maybe room 3. But the rule says the meeting takes the **lowest id**, room 1. Free rooms are ranked by *id*; busy rooms are ranked by *end time*. Two different orderings over the same rooms means two heaps. That split **is** the trick.
>
> **[VISUAL: rooms migrate from the red pile to the green pile as a clock sweeps forward, labeled "retire finished rooms".]**
>
> One piece of glue: before each meeting, any busy room whose end time has passed gets *retired* — popped off busy, pushed onto free. Then the tops of the two heaps answer both questions instantly.

---

## 6. THE KEY MOVE (signaling) — `5:05`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "assign by one priority, reclaim by another ⇒ two heaps."]**

> Burn this in: **when resources are handed out by one priority and taken back by another — two heaps, one per ordering.**
>
> Here it's rooms: assigned by lowest id, reclaimed by earliest end time. The moment a problem ranks the same objects two different ways, that's your trigger. And the bonus: Python tuples compare element by element, so `(end_time, room_id)` breaks end-time ties by lower id automatically — which is *exactly* the tie-break the problem demands. The data structure enforces the spec for free.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Setup first: sort by start, all rooms begin free, and note — the list `0` to `n−1` is already a valid heap.

```python
import heapq

def mostBooked(n, meetings):
    meetings.sort()                         # process in start order
    free = list(range(n))                   # min-heap of available room ids
    heapq.heapify(free)                     # [0, 1, ..., n-1] is already a heap
    busy = []                               # min-heap of (end_time, room_id)
    count = [0] * n
```

> **[VISUAL: add chunk 2, highlight the while loop.]** For each meeting, step one: the retire loop. Any busy room done by `start` goes back to the free pile.

```python
    for start, end in meetings:
        # 1. retire every room that has freed up by `start` → back to `free`
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)
```

> **[VISUAL: add chunk 3.]** Step two-a: if a room's free, take the lowest id and the meeting runs on time.

```python
        # 2a. a room is free → take the lowest id, run for the full [start, end)
        if free:
            room = heapq.heappop(free)
            heapq.heappush(busy, (end, room))
```

> **[VISUAL: add chunk 4, highlight `free_at + (end - start)`.]** Step two-b — the Wrong-Answer line from the cold open. Nobody's free: pop the earliest-freeing room, and push back its free time **plus the meeting's own duration**. The end slides.

```python
        # 2b. none free → wait for the earliest-freeing room; keep the duration
        else:
            free_at, room = heapq.heappop(busy)
            heapq.heappush(busy, (free_at + (end - start), room))

        count[room] += 1
```

> **[VISUAL: add chunk 5.]** Finally, the winner — most meetings, and a strict greater-than so ties keep the lowest id.

```python
    # most meetings, ties → lowest id (strict > keeps the first/lowest)
    best = 0
    for r in range(n):
        if count[r] > count[best]:
            best = r
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:35`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `meetings.sort()` — the rules are defined over meetings *in start order*. Process out of order and "was a room free at this start?" has no meaning.
>
> `while busy and busy[0][0] <= start` — the invariant of the whole function lives here: when this loop finishes, `free` holds exactly the rooms idle at time `start`, and `busy` holds everyone still occupied. Every decision after it leans on that.
>
> **LEARNER:** Why `<=` and not `<`? A room whose meeting ends exactly *at* my start time — isn't it still wrapping up?
>
> **TEACHER:** Half-open intervals — same rule you learned in My Calendar I. `[start, end)` means the room owns nothing *at* `end`. Ends at 10, and time 10 is already free. Write `<` and a room finishing at exactly `start` stays stuck in busy — your meeting might wait, or take a worse room, for no reason. One character, wrong answer.
>
> `free_at + (end - start)` — read it as *when the room opens, plus my full duration*. Push plain `end` instead and a delayed meeting gets silently shortened — the cold-open bug.
>
> **LEARNER:** One more. In the else branch, when two busy rooms free up at the same time — where's the code that picks the lower room number? I don't see a tie-break anywhere.
>
> **TEACHER:** Sharp eyes — there isn't one, and that's the point. The heap holds tuples, and tuples compare position by position: end times first, and *only on a tie*, room ids. `(10, 0)` sorts before `(10, 1)`, so the heap's top already respects the rule. The tie-break isn't missing — it's baked into the key.
>
> `count[r] > count[best]` — **strict**. An equal count never displaces an earlier room, so the final tie also resolves to the lowest id, exactly as the spec demands. Three tie-breaks in this problem, and not one of them is an `if`.

---

## 9. DRY-RUN THE CODE — `9:05`
*(worked example — prove it, close the loop)*

**[VISUAL: the two heap piles animating live; a trace table filling row by row.]**

> Let's run the real code on our four meetings and watch the heaps do the work.

| Meeting | Retire (end ≤ start) | `free` before | Decision | `busy` after | `count` |
|---|---|---|---|---|---|
| `[0,10]` | none | `[0,1]` | free → room **0**, runs `[0,10)` | `[(10,0)]` | `[1,0]` |
| `[1,5]` | none (10 > 1) | `[1]` | free → room **1**, runs `[1,5)` | `[(5,1),(10,0)]` | `[1,1]` |
| `[2,7]` | none (5 > 2) | `[]` | none free → pop `(5,1)`; delayed end `5 + (7−2) = 10` → room **1** | `[(10,0),(10,1)]` | `[1,2]` |
| `[3,4]` | none (10 > 3) | `[]` | none free → pop `(10,0)` — tie 10 vs 10, tuple picks id 0; delayed end `10 + (4−3) = 11` → room **0** | `[(10,1),(11,0)]` | `[2,2]` |

> Row three is the sliding end: `[2,7]` waited on room 1 until 5, kept its five units, and now ends at 10 — not 7.
>
> Row four is the tuple tie-break earning its keep: both rooms free at 10, and `(10,0) < (10,1)` hands the meeting to room 0 with zero extra code.
>
> Final count `[2, 2]` — tie — strict `>` keeps room **0**. Exactly the answer we promised at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(m·n + m log m). Ours: O(m log m + m log n). A note: "retire loop = each room retired at most once per meeting it hosted".]**

> Say it the way you'd say it in the room: *"Brute force re-scans all n rooms per meeting — O(m·n). With two heaps, sorting costs O(m log m), and each meeting does a constant number of heap operations on heaps of size at most n — O(m log n). The retire loop looks nested, but a room is only retired once per meeting it hosted, so it's amortized into the same bound. Total: O(m log m + m log n)."*
>
> Naming the amortized argument for that while-loop — unprompted — is the moment a Hard starts sounding routine.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:35`
*(depth + honesty)*

**[VISUAL: the two heaps side by side; a bracket over both labeled "|free| + |busy| = n, always". A "shrink it?" thought bubble → red ✗.]**

> Quick one, and honesty scores here.
>
> Space is `O(n)` — and here's the clean part: every room lives in *exactly one* of the two heaps at any instant, so their combined size is always exactly `n`. Two heaps don't cost double.
>
> Can it shrink? **No — and say why:** *"I can't answer 'lowest free room' or 'soonest to open' without holding every room's state, so O(n) is the floor."* Naming the floor beats mumbling past it.

---

## 12. YOUR TURN (active recall) — `11:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Process Tasks Using Servers (LC 1882)". A blank editor.]**

> Before the next video, try **Process Tasks Using Servers**. It's this exact skeleton wearing a different shirt — a free heap of servers keyed by weight and index, a busy heap keyed by when each server finishes. If you can re-derive the two-heap split there yourself, you own this pattern.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `11:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Two questions, two orderings, two heaps** — free rooms ranked by id, busy rooms by end time; retire finished rooms before every meeting.
> 2. **A delayed meeting keeps its duration** — push `free_at + (end − start)`, never plain `end`.
> 3. **Let the keys do the tie-breaking** — `(end_time, room_id)` tuples and a strict `>` handle every tie in the spec with zero branches.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "assign by one priority, reclaim by another → two heaps."]**
>
> The instant a problem hands out resources by one rule and takes them back by a different one, your hand should already be reaching for a pair of heaps.
>
> *(GCA reminder — for the interview itself: before you code, ask the one clarifying question that shows you read the spec — "a delayed meeting keeps its original duration, so its end slides, right?" — then narrate the path: brute force, the two re-asked questions, the two-heap split. Google scores General Cognitive Ability, and narrating your approach plus asking sharp clarifying questions is half the rubric — the trick alone is not.)*

---

## 14. CLIFFHANGER — `11:55`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Amount of New Area Painted Each Day" — a number line with overlapping paint strokes, the fresh paint glowing, the overlap grayed out.]**

> Today we tracked which *rooms* were free. Next problem flips it: you're painting stretches of a number line, day after day, and paint never counts twice — so now the resource you're tracking is **the timeline itself**, and you need to know which pieces of it are still bare. A heap of rooms won't save you when the thing being claimed is an infinite line. That's *Amount of New Area Painted Each Day* — and the trick for skipping what's already painted is one of the slickest moves in this whole section. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
