# 🎬 Recording Script — Find Servers That Handled Most Number of Requests
**Pattern: Two heaps + ordered set · LeetCode 1606 · Hard · Target length ~14 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** min-heap of end times (Meeting Rooms II) — but here we also need to pick *which* free server, by id.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean nested-loop solution is typed out — an outer loop over requests, an inner `for probe in range(k)`. A LeetCode "Time Limit Exceeded — 60 / 67" banner slams in red.]**

> Google onsite. The interviewer says: *"You've got k servers. Requests come in. Each request prefers a specific server, and if it's busy you walk to the next one. Tell me who handled the most."*
>
> You write the obvious thing — for each request, walk the ring of servers until you find a free one. It's *correct*. It passes 60 tests. Then test 61 has a hundred thousand servers and a hundred thousand requests, and… Time Limit Exceeded.
>
> Your code isn't wrong. It's just **re-scanning servers it already knows are busy**, over and over. By the end of this video you'll fix it with two structures — a heap and an ordered set — and you'll see the one property of the input that makes the fix bulletproof. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, three server boxes labelled 0, 1, 2, all green "free". A little table: arrival = [1,2,3,4,5], load = [5,2,3,3,3].]**

> The whole problem in one line: **each request prefers server `i % k`; if that one's busy, walk to the next higher id, wrapping around; if all are busy, drop it. Return the busiest servers.**
>
> Here's our tiny example — **three** servers, **five** requests. Request `i` arrives at `arrival[i]` and hogs its server for `load[i]` time. Keep your eye on this exact setup; we'll solve it by hand before we write a line of code.
>
> Spoiler you can hold onto: the answer is going to be **just server 1.** Don't chase why yet — just hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the three server boxes with a small "free at" clock under each, starting at 0. A "servers probed" counter, top-right, at 0. Requests drop in one at a time.]**

> Let's do what your brain does first. Keep a clock under each server — the time it's next free. For each request, start at the preferred id and walk forward until a clock says "free."
>
> Request 0, arrives at 1, prefers server 0. Free. Take it — server 0 busy until 1+5 = **6**.
>
> Request 1, arrives at 2, prefers server 1. Free. Busy until 2+2 = **4**.
>
> Request 2, arrives at 3, prefers server 2. Free. Busy until 3+3 = **6**… wait, 3+3 is **6**? Let me recheck — load is 3, so until 6. Hmm, actually it's `3+3 = 6`. Keep it simple: server 2 busy a while.
>
> **[VISUAL: correct the clock to show server 2 busy until 6; note load[2]=3 so end=6... actually arrival 3 + load 3 = 6.]**
>
> Request 3, arrives at 4, prefers server 0. Server 0's clock says 6 — **busy**. Probe server 1: its clock said 4, and it's now time 4, so it's **free again**. Take it.
>
> **[VISUAL: the probe arrow bounces off busy server 0, lands on server 1; "servers probed" counter ticks up by 2.]**
>
> See that bounce? On three servers it's cheap. But picture a hundred thousand servers, all busy, and every request walking almost the entire ring before it finds someone — or gives up. That counter explodes.
>
> **[VISUAL: counter morphs into "≈ n × k" with a scary red glow.]**

---

## 4. THE PAIN POINT + PREDICT — `2:50`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the probe arrow skidding across a long row of red "busy" servers before finding one green. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? Look at this probe. It's stepping over busy server after busy server — servers we *already knew* were busy — just to reach the free one.
>
> **LEARNER:** But we have to find a free server somehow. How do we skip the busy ones without looking at them?
>
> **TEACHER:** Exactly the right question. Here's your think: **what if we kept the free servers in one pile and the busy ones in another — and never even looked at the busy pile when assigning?** Pause the video. What structure lets you grab "the next free server by id" instantly, and what structure tells you *when* a busy server becomes free?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:35`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two containers appear. Left: a heap labelled "BUSY — sorted by finish time." Right: an ordered list labelled "FREE — sorted by id." Servers slide between them.]**

> **TEACHER:** Two piles. On the right, a **FREE set** of server ids, kept sorted. On the left, a **BUSY min-heap** — but keyed by **finish time**, so the server that frees up *soonest* always sits on top.
>
> Now watch the rhythm. Before I handle a request that arrives at time `t`, I peek at the busy heap. Is the soonest finisher done by `t`? Pop it, drop it into the free set. Keep popping while the top is finished. It's like a coat check: I don't walk the whole rack — the next coat ready is always at the front.
>
> **[VISUAL: heap pops a server whose finish time ≤ t; it slides into the FREE set and turns green.]**
>
> **LEARNER:** Hold on. A server that finished at time 4 — when I get to a request at time 10, is it *definitely* still free? What if something grabbed it?
>
> **TEACHER:** Beautiful worry, and here's the key. Look at the arrivals: **1, 2, 3, 4, 5** — strictly increasing. Time only ever moves *forward*. So once a server's finish time slips past the current arrival, it's free for this request and every request after. It can never un-finish. That's the property that makes lazy release safe.
>
> **[VISUAL: the arrival timeline lights up with a one-way arrow: "time only moves forward ⇒ released stays released."]**
>
> **TEACHER:** So from the free set, I just need "the smallest id at or above `i % k`." That's a binary search. And if there's nothing at or above it? I **wrap** — take the smallest free id overall.

---

## 6. THE KEY MOVE (signaling) — `5:05`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Busy heap by finish-time (lazy release) + free set by id (ceiling, else wrap)."]**

> Burn this one line in: **busy servers live in a min-heap by finish time so you release them lazily; free servers live in an ordered set so you grab the next id with a binary search — ceiling, or wrap to the front.**
>
> That's the whole pattern. Any "assign the next available resource in a ring, by a time rule" problem — this is your reflex.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in pieces. First the two structures and the tally. `SortedList` gives us the ordered free set with binary search built in.

```python
import heapq
from sortedcontainers import SortedList

def busiest_servers(k, arrival, load):
    free = SortedList(range(k))     # idle ids, sorted — starts with all of them
    busy = []                       # min-heap of (end_time, server_id)
    count = [0] * k
```

> **[VISUAL: add chunk 2, highlight it.]** Now the loop. Step one — lazy release: pull every finished server back into free.

```python
    for i, start in enumerate(arrival):
        while busy and busy[0][0] <= start:
            _, sid = heapq.heappop(busy)
            free.add(sid)
```

> **[VISUAL: add chunk 3.]** If nobody's free, all k are busy — the request drops. One line.

```python
        if not free:
            continue                # all servers busy → drop this request
```

> **[VISUAL: add chunk 4, highlight the bisect + wrap.]** The heart: find the first free id at or above `i % k`; if the search runs off the end, wrap to index 0 — the smallest free id.

```python
        prefer = i % k
        j = free.bisect_left(prefer)
        if j == len(free):          # nothing >= prefer → wrap around the ring
            j = 0
        sid = free[j]
```

> **[VISUAL: add chunk 5.]** Assign: pull it out of free, push it onto the busy heap with its finish time, bump its count.

```python
        free.remove(sid)
        heapq.heappush(busy, (start + load[i], sid))
        count[sid] += 1
```

> **[VISUAL: add chunk 6.]** Finally, the busiest ids.

```python
    best = max(count)
    return [s for s, c in enumerate(count) if c == best]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:40`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `while busy and busy[0][0] <= start` — `busy[0]` is the heap top, the soonest finisher. We release *everyone* done by now, not just one. Drop the `while` and you'd leak free servers.
>
> `if not free: continue` — this single line *is* the "drop the request" rule. Empty free set means all k are busy.
>
> `j = free.bisect_left(prefer)` — first free id at or above the preferred one. That's the "next higher id" probe, done in one binary search instead of a walk.
>
> **LEARNER:** Wait — why `bisect_left`, and why does `j == len(free)` mean *wrap*? Shouldn't wrapping be more complicated than just index 0?
>
> **TEACHER:** Great catch. `bisect_left(prefer)` returns the position where `prefer` *would* slot in — so `free[j]` is the smallest id that's `>= prefer`. If `j` equals the length, there's nothing at or above `prefer`, which means every free server has a *smaller* id. Wrapping the ring means "start over from id 0 and go up," so the first one we'd hit is just the smallest free id — that's `free[0]`, index 0. The sorted order does the wraparound for us.
>
> `heapq.heappush(busy, (start + load[i], sid))` — finish time first in the tuple, so the heap orders by *when it frees up*. That ordering is the entire trick.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the three server boxes; a trace table filling row by row. free set and busy heap shown as chips beside each row.]**

> Let's run the actual code on `k=3`, `arrival=[1,2,3,4,5]`, `load=[5,2,3,3,3]` and watch the piles move.

| i | arrival | release | free before | prefer | id chosen | busy after (end) | count |
|---|---|---|---|---|---|---|---|
| 0 | 1 | — | `[0,1,2]` | 0 | **0** | 0→6 | `[1,0,0]` |
| 1 | 2 | — | `[1,2]` | 1 | **1** | 1→4, 0→6 | `[1,1,0]` |
| 2 | 3 | — | `[2]` | 2 | **2** | 1→4, 0→6, 2→6 | `[1,1,1]` |
| 3 | 4 | server 1 (end 4) | `[1]` | 0 | **1** (wrap) | 0→6, 2→6, 1→7 | `[1,2,1]` |
| 4 | 5 | — (6,6,7 all > 5) | `[]` | 1 | **drop** | unchanged | `[1,2,1]` |

> Row 3 is the money row. Prefer is 0, but the only free server is id 1. `bisect_left([1], 0)` returns 0 — it lands right on id 1. The wraparound rule, for free.
>
> Row 4: nothing finished by time 5, free set is empty — the request drops, exactly as promised.
>
> Final counts: `[1, 2, 1]`. Max is 2, at server **1**. Return `[1]` — the exact answer we called at the very start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n·k). Ours: O(n log k). A note: "each request: one heap op + one binary search = log k".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is O(n·k) because each request can probe the whole ring of servers. With the heap-plus-ordered-set, each request does an O(log k) binary search and O(log k) heap operations, and every server is released at most once amortized — so it's O(n log k) time. Space is O(k) for the heap, the free set, and the counts."*
>
> On the constraints — n and k up to ten to the fifth — that's the difference between ten billion operations and a couple million. That's the difference between TLE and Accepted.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:05`
*(depth + honesty)*

**[VISUAL: the heap + free set + count array; a "shrink below O(k)?" thought bubble appears, then gets a red ✗.]**

> Quick but important — and honesty scores points here.
>
> Can we go below `O(k)`? **No — and I can say exactly why.** I have to know the status of every one of the k servers — busy or free — and keep a request tally per server to find the busiest. That's inherently k-sized. And notice: nothing grows with the *number of requests*. A server is in exactly one pile at a time — busy or free — so the two structures together never exceed k entries. Requests just flow through.
>
> Say it out loud in the interview: *"Space is O(k), and that's the floor — I must track all k servers, and nothing scales with n."* Naming *why* it can't shrink is a stronger signal than silently accepting it.
>
> **LEARNER:** One thing — what if the environment doesn't have `sortedcontainers`?
>
> **TEACHER:** Then reach for the **two-heap trick**: split the free ids into two min-heaps at `i % k` — one for ids at or above the preferred, one for the rest. Prefer the first; if it's empty, wrap to the second. Same O(n log k), just more bookkeeping. Mention `SortedList` first, keep the two-heap version in your back pocket.

---

## 12. YOUR TURN (active recall) — `11:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Process Tasks Using Servers (LC 2073)". A blank editor.]**

> Before the next video, try **Process Tasks Using Servers**. It's the near-twin: two heaps again — free servers ranked by weight, busy servers ranked by when they free up — assigning tasks in order. Same "release the finished, pick the best free one" skeleton.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `12:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Brute force re-scans busy servers → O(n·k) → TLE.** The fix is to *never look at the busy pile* when assigning.
> 2. **Two structures:** a min-heap of busy servers by finish time (lazy release), an ordered set of free ids (binary search, wrap to front).
> 3. **Strictly increasing arrivals** are what make lazy release safe — released servers stay released.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Busy in a heap by finish-time, free in a set by id."]**
>
> When you see *"assign the next free resource in a ring, by a time rule,"* your hands should already be reaching for a heap and an ordered set.
>
> *(GCA reminder — for the interview itself: ask the clarifying question first — "I probe upward and wrap, and only drop if all k are busy, right?" Then state the brute force, name the wasted re-scanning out loud, and only then reach for the two structures. Google's General Cognitive Ability signal isn't the trick — it's you narrating the path from naive to optimal.)*

---

## 14. CLIFFHANGER — `13:20`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Merge k Sorted Lists" — k list-heads feeding into a single min-heap.]**

> We used a heap to always grab the *soonest-finishing* server. But what if the thing on top of the heap isn't a finish time — it's the *smallest value across k sorted streams*, and every time you pop one, you have to pull the next value from that same stream? That's the next one: **Merge k Sorted Lists.** Same heap reflex, a brand-new twist on what you push back. See you there.
