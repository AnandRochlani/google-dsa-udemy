# 🎬 Recording Script — My Calendar I
**Pattern: Intervals / balanced BST (TreeMap) · LeetCode 729 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** binary search (`bisect`) and any ordered map — that's all the machinery you need.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a calendar week-view. Someone drops a meeting block onto it. Then another block lands right on top — both flash red "DOUBLE BOOKED".]**

> You're building a calendar. The one rule: never let two events overlap. Sounds trivial, right? Keep a list, check the new event against everything on it.
>
> And it *works* — until the interviewer says "now handle ten thousand bookings." Your list-scan crawls, and you feel the O(n²) closing in.
>
> Here's the promise: by the end of this video, every booking will cost you `O(log n)` instead of `O(n)` — and the whole fix is one idea about *where an overlap can possibly hide.* Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, three calls listed:]**

```
book(10, 20) → ?
book(15, 25) → ?
book(20, 30) → ?
```

> The whole problem in one line: **`book(start, end)` returns true and saves the event if it doesn't overlap anything already booked — otherwise false, and it saves nothing.**
>
> One catch that decides everything: the intervals are **half-open**. `[10, 20)` covers 10 up to but *not including* 20. So an event that ends at 20 and one that starts at 20 don't fight — they just touch.
>
> Keep those three calls on screen. We'll answer them by hand before we write a line of code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: an empty list `events = []`. A "comparisons" counter, top-right, at 0.]**

> Let's do what your brain does first: keep a list, and check every new event against all of them.
>
> `book(10, 20)` — list's empty, nothing to clash with. Goes in. `events = [(10,20)]`.
>
> **[VISUAL: (10,20) drops into the list.]**
>
> `book(15, 25)` — walk the list. Compare against `(10,20)`. Does 15-to-25 overlap 10-to-20? Yes — 15 is before 20. Reject. Counter ticks.
>
> `book(20, 30)` — walk the list again. Compare against `(10,20)`. Comparison number two. Touches at 20, no overlap. Goes in.
>
> **[VISUAL: counter shows the scans; a thought bubble: "what if the list had 10,000 events?"]**
>
> See the problem forming? With one event it's nothing. With ten thousand, *every* booking walks the *entire* list. That's O(n) a call, O(n²) total.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. A long list of events; the new booking (500, 510) highlighted. Faraway events at (0,5), (1000,1005) dimmed. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste. I'm booking `(500, 510)`. The brute force checks it against an event at `(0, 5)`. Against `(1000, 1005)`. Those could *never* overlap me — they're miles away in time. I'm comparing against events that don't matter.
>
> **LEARNER:** Okay but how do I know which ones matter without looking at all of them?
>
> **TEACHER:** That's exactly the question. Here's your think: **if I kept my events sorted by start time, how few of them would I actually need to check?** Pause the video. Picture the sorted line of events and the new one sliding into place.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: events drawn as bars on a timeline, sorted left to right. The new event (500,510) slides in; two glowing arrows point to the bar just left of it and the bar just right of it.]**

> **TEACHER:** Keep the events **sorted by start**. Now slide the new one into its spot on that line. Think about it — the only events that could possibly touch me are my **immediate neighbors**: the one just to my left, and the one just to my right.
>
> The neighbor to my left starts before me. The neighbor to my right starts after me. Everything further left starts even earlier and ended even earlier — can't reach me. Everything further right starts even later — starts after I'm done. **Two neighbors. That's all I check.**
>
> **[VISUAL: the two neighbor bars pulse green; every other bar fades out.]**
>
> It's like sliding a book onto a shelf. You don't check every book on the shelf to see if it fits — you look at the two books it lands *between*.
>
> **LEARNER:** Wait — two neighbors is enough? What if some earlier event was really long and stretched all the way into my slot?
>
> **TEACHER:** Great worry, and here's why it can't happen. Every event already on the calendar was accepted — meaning none of them overlap *each other*. So they're not just sorted by start, they're laid out end-to-end without crossing. A far-left event can't stretch past my left neighbor without having overlapped *that* neighbor first — which we'd never have allowed. The no-overlap invariant is what makes "just the two neighbors" airtight.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "sort by start ⇒ a conflict can only be your left or right neighbor ⇒ binary-search to them."]**

> Burn this in: **keep events sorted by start, and a conflict can only be your immediate left or right neighbor — so binary-search straight to those two.**
>
> And the overlap rule itself, memorize it cold: two half-open intervals `[s1,e1)` and `[s2,e2)` overlap **iff `s1 < e2 and s2 < e1`**. Both conditions, strict less-than. That single line is the heart of every interval problem you'll ever see.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Python's `SortedList` keeps things ordered *and* gives us binary search in one structure — perfect.

```python
from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.events = SortedList()          # sorted by (start, end)
```

> **[VISUAL: add chunk 2, highlight it.]** In `book`, first find *where* this event would slide in — that's the binary search.

```python
    def book(self, start, end):
        i = self.events.bisect_left((start, end))
```

> **[VISUAL: add chunk 3.]** Now the **right** neighbor — the event at index `i`. It overlaps me if *its* start comes before my end.

```python
        if i < len(self.events) and self.events[i][0] < end:
            return False
```

> **[VISUAL: add chunk 4.]** And the **left** neighbor — index `i-1`. It overlaps me if *its* end comes after my start.

```python
        if i > 0 and self.events[i - 1][1] > start:
            return False
```

> **[VISUAL: add chunk 5, highlight the add line.]** Both neighbors clear? Record it and return true.

```python
        self.events.add((start, end))
        return True
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:40`
*(elaboration — why each line exists)*

**[VISUAL: the full method; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `bisect_left((start, end))` — this finds the insertion point in `O(log n)`. Index `i` is where we'd land; `i` and `i-1` are our two suspects.
>
> `self.events[i][0] < end` — the right neighbor's *start* versus my *end*. If it starts before I finish, we collide. Notice it's strict `<`: if its start equals my end, we only touch — allowed.
>
> `self.events[i-1][1] > start` — the left neighbor's *end* versus my *start*. If it ends after I begin, we collide. Again strict `>`: if it ends exactly at my start, we touch — allowed.
>
> **LEARNER:** That's the part I'd get wrong — why `>` and not `>=`? Feels like ending at 10 and starting at 10 should clash.
>
> **TEACHER:** Because the interval is half-open — `[10, 20)` doesn't *include* 20. So an event ending at 20 owns nothing at 20, and an event starting at 20 owns 20 onward. Zero shared ground. Flip that `>` to `>=` and you'd reject `book(20, 30)` after `book(10, 20)` — a real bug. The strict comparison *is* the half-open rule, encoded.

---

## 9. DRY-RUN THE CODE — `7:50`
*(worked example — prove it, close the loop)*

**[VISUAL: the three calls; a trace table filling row by row.]**

> Let's run the real code on our three calls and close the loop from the start.

| Call | `events` before | `i` | Right check `events[i][0] < end` | Left check `events[i-1][1] > start` | Result |
|---|---|---|---|---|---|
| `book(10,20)` | `[]` | 0 | i = len, skip | i = 0, skip | **true** |
| `book(15,25)` | `[(10,20)]` | 1 | i = len, skip | `20 > 15` ✓ overlap | **false** |
| `book(20,30)` | `[(10,20)]` | 1 | i = len, skip | `20 > 20`? **no** | **true** |

> Look at that last row. `(10,20)` and `(20,30)` — the left neighbor ends at 20, we start at 20. `20 > 20` is false, so no overlap. They touch, and we allow it. Exactly the answers we predicted at second thirty. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n) per book, O(n²) total. Ours: O(log n) per book.]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force scans every prior event — O(n) per booking, O(n²) overall. By keeping events sorted by start, I binary-search to the two neighbors and check only those, so each booking is O(log n). Space is O(n) for the events."*
>
> One honest footnote: a `TreeMap` in Java, or `SortedList` in Python, gives O(log n) *insert* too. If you use a plain list with `bisect`, the search is O(log n) but the insert shifts elements — O(n). Say that trade-off out loud; interviewers love that you know it.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:20`
*(depth + honesty)*

**[VISUAL: the events list; a "drop old events?" thought bubble → red ✗.]**

> Quick one, and honesty scores here.
>
> Can we shrink the `O(n)` storage? **No — and I can say exactly why.** Every event I've accepted might conflict with a *future* booking, so I can't forget a single one. There's nothing to roll away; the events themselves are the state.
>
> Say it in the room: *"Space is O(n) and it's forced — I must retain every accepted event to test future ones against it."* Naming *why* the floor exists is a stronger signal than mumbling "we store the events."

---

## 12. YOUR TURN (active recall) — `9:55`
*(retrieval practice)*

**[VISUAL: "Your turn → My Calendar II (LC 731)". A blank editor.]**

> Before the next video, try **My Calendar II**. Now double-booking is *allowed* — you only reject a **triple** booking. Same interval DNA, but you'll have to track *how many* events overlap, not just whether any do.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Overlap rule:** `[s1,e1)` and `[s2,e2)` clash **iff `s1 < e2 and s2 < e1`** — both strict.
> 2. **Sort by start** and a conflict can only be your left or right neighbor — binary-search to them for `O(log n)`.
> 3. **Half-open means touching is fine** — the strict `<` and `>` encode that; `>=` would be a bug.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "sort by start → check your two neighbors."]**
>
> When you see "insert intervals, reject on overlap," your hand should already be reaching for an ordered map — TreeMap in Java, SortedList in Python — and checking just the two neighbors.
>
> *(GCA reminder — for the interview itself: open by asking "are these half-open?" then state the brute force, name the wasted far-away comparisons out loud, and only then reach for the sorted structure. Google's General Cognitive Ability signal isn't the trick — it's you narrating the path from naive to optimal and pinning the overlap rule before you write it.)*

---

## 14. CLIFFHANGER — `11:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "My Calendar III" — a timeline with events stacked 3-deep, a counter reading "max concurrent = 3".]**

> We rejected any overlap. But what if overlaps are allowed, and the real question becomes *"how many events are stacked on top of each other at the busiest moment?"* Neighbor-checking won't cut it anymore — you need to count concurrency across the whole timeline. That's My Calendar III, and it opens the door to the sweep-line technique. See you there.
