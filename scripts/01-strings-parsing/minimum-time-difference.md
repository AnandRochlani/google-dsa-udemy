# 🎬 Recording Script — Minimum Time Difference
**Pattern: Sorting / Pigeonhole · LeetCode 539 · Medium · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** "sort, then the closest pair is next-door" (Minimum Absolute Difference) — but there's a twist here that sorting alone won't catch.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: two clock faces side by side — one reads 23:59, the other 00:00. A big question mark between them. Below, a slick answer "1439" fades in… then a red buzzer.]**

> Quick gut check. Two times: `23:59` and `00:00`. How far apart are they?
>
> Your brain says "well, 23:59 is basically the whole day, and 00:00 is zero, so… 1439 minutes." And that's the answer that fails the interview.
>
> Because these are times **on a clock**. Midnight is *one minute* after 23:59. The real answer is **1**. By the end of this video you'll have clean, correct code — and you'll never forget the one line that handles the midnight wrap. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, a tiny list of three time chips:]**

```
["00:00", "23:59", "06:30"]
```

> The whole problem in one line: **given a list of HH:MM times, find the smallest gap in minutes between any two of them.**
>
> Here's our tiny example — three times. Nothing fancy. The trap is baked in: `00:00` and `23:59` look far apart but they hug across midnight.
>
> Hold this list. We'll solve it by hand before we touch code — and the answer, keep it in your back pocket, is going to be **1**.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the three chips. Arrows drawn between every pair; a "comparisons" counter ticks up. Each arrow labeled with a raw abs-difference.]**

> Let's do what your brain does first: compare **every pair**, take the smallest gap.
>
> First convert each to minutes-since-midnight. `00:00` → `0`. `23:59` → `1439`. `06:30` → `390`.
>
> **[VISUAL: chips relabel to 0, 1439, 390.]**
>
> Now the pairs. `0` vs `390` → `390`. `390` vs `1439` → `1049`. `0` vs `1439` → … `1439`.
>
> **[VISUAL: the three arrows light up: 390, 1049, 1439. Counter reads 3.]**
>
> Smallest is `390`, so… the answer is 390? Six and a half hours? That *feels* wrong, and it is. Three times means three comparisons — fine here — but bump it to `n` times and it's `n²`. And worse: this naive pass just told us the wrong answer. Watch why.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the `0` and `1439` chips. A circular clock dial overlays them — `1439` sits one tick *before* `0`, going the short way. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the bug. We measured `0` to `1439` as `1439` — walking the *long* way around the day. But time is a **circle**. Go the short way and `1439` to `0` is a single minute.
>
> **LEARNER:** Okay but — if I just take `min(diff, 1440 - diff)` on every pair, doesn't that fix it? Why do I need anything cleverer?
>
> **TEACHER:** That patch *is* correct — and it's still `O(n²)`. We're comparing far-apart times that could never be the closest pair. So here's your think: **the values only ever range from 0 to 1439. What could I do to that list so I never have to check distant pairs at all?** Pause. What's the one move?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the three minute-values slide into sorted order on a number line: 0 … 390 … 1439. Then the line curls into a clock, joining 1439 back to 0.]**

> **TEACHER:** The move is **sort them**. `[0, 390, 1439]`.
>
> Once they're lined up, the closest pair is always **right next to each other**. Think of people standing in a queue by height — the two most similar heights are always neighbors, never someone at the front vs someone at the back. So I only check **adjacent** gaps. One pass, no `n²`.
>
> **[VISUAL: adjacent gaps light up: 0→390 = 390, 390→1439 = 1049.]**
>
> `0` to `390` is `390`. `390` to `1439` is `1049`. Smallest so far, `390`.
>
> **LEARNER:** But that's the same wrong answer as before! Sorting didn't catch the midnight thing.
>
> **TEACHER:** Exactly — and that's the whole lesson. Sorting finds every close pair **except one**: the pair that straddles midnight. The **last** time and the **first** time are neighbors too — across the top of the clock.
>
> **[VISUAL: the curled number line highlights the 1439 → 0 arc; label "(0 + 1440) − 1439 = 1".]**
>
> So I add one extra gap by hand: take the earliest, add a full day — `0 + 1440` — and subtract the latest, `1439`. That's `1`. *There's* our answer. Min of the adjacent gaps and that one wrap term: **1**.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "sort → check neighbors → PLUS the wraparound: (first + 1440) − last."]**

> Burn this in: **sort the times, the closest pair is adjacent — but always add the one gap sorting hides, the wraparound from last back to first.**
>
> Forget that second half and you'll pass the easy tests and fail on midnight. The wraparound *is* this problem.

---

## 7. CODE IT — LIVE & CHUNKED — `5:05`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only, highlight it.]**

> Build it in pieces. **Chunk one — the shortcut nobody expects.** There are only 1440 minutes in a day. So if we have more than 1440 times, two of them *must* land on the same minute — that's the pigeonhole principle. Instant zero.

```python
def find_min_difference(timePoints):
    if len(timePoints) > 1440:      # pigeonhole → a duplicate must exist
        return 0
```

> **[VISUAL: add chunk 2, highlight.]** Chunk two — convert each `"HH:MM"` to minutes since midnight, and sort.

```python
    def to_min(t):
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    mins = sorted(to_min(t) for t in timePoints)
```

> **[VISUAL: add chunk 3, highlight the adjacent scan.]** Chunk three — the smallest gap between neighbors. `zip(mins, mins[1:])` pairs each with the next.

```python
    best = min(b - a for a, b in zip(mins, mins[1:]))
```

> **[VISUAL: add chunk 4, spotlight the wraparound line — make it glow.]** Chunk four — the star. The wraparound gap, then return the smaller.

```python
    wrap = (mins[0] + 1440) - mins[-1]
    return min(best, wrap)
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `if len(timePoints) > 1440: return 0` — pure pigeonhole. 1440 possible values, a 1441st entry forces a collision, and a collision means a zero gap. Free early exit.
>
> `int(h) * 60 + int(m)` — this is the unlock for the whole problem: turn a string clock time into a plain number line from 0 to 1439. Everything downstream is just arithmetic on integers.
>
> `sorted(...)` — this is what lets us check only neighbors instead of all pairs. Earns us `O(n log n)` instead of `O(n²)`.
>
> `min(b - a for a, b in zip(mins, mins[1:]))` — one clean pass over adjacent pairs. Since it's sorted, `b - a` is always non-negative, no `abs` needed.
>
> **LEARNER:** That wrap line — why `+ 1440`? Why not just `mins[-1] - mins[0]`?
>
> **TEACHER:** Because `mins[-1] - mins[0]` is the gap going the *long* way — down through the whole day. The wrap goes the *short* way, over the top of midnight. Adding 1440 to the first time lifts it "past" midnight so the subtraction measures that short arc. `(0 + 1440) − 1439 = 1`. That plus-1440 is the clock. Delete it and you've got a stopwatch, not a clock.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: the sorted list [0, 390, 1439]; a trace table filling row by row.]**

> Run the real code on our list. After convert-and-sort: `[0, 390, 1439]`.

| Step | Computes | Value |
|---|---|---|
| len > 1440? | 3 > 1440 → no | skip shortcut |
| adjacent gap 0→390 | `390 - 0` | 390 |
| adjacent gap 390→1439 | `1439 - 390` | 1049 |
| `best` | min(390, 1049) | **390** |
| wraparound | `(0 + 1440) - 1439` | **1** |
| return | min(390, 1) | **1** ✅ |

> The adjacent scan alone screamed `390`. The wraparound line quietly says `1` — and wins. Loop closed: the answer is the **1** we promised at second zero.

---

## 10. COMPLEXITY, OUT LOUD — `8:25`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²). Ours: O(n log n). A note: "sort dominates".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is `O(n²)` — all pairs. I sort instead, so the closest pair is adjacent and I only scan neighbors. The sort dominates: `O(n log n)` time, `O(n)` space for the minute list. And the pigeonhole check caps the input at 1440 before I even sort."*
>
> That sentence turns a Medium from "I think so" into "I've got this."

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:55`
*(depth + honesty)*

**[VISUAL: a row of 1440 tiny empty boxes; three of them flip to ✓ at positions 0, 390, 1439.]**

> Here's the upgrade that scores points. Can we beat `O(n log n)`? **Yes — and only because the value range is fixed.**
>
> Instead of sorting, make a **1440-slot boolean array** — one box per minute of the day. Mark each time's box. If a box is already marked, that's a duplicate — return zero on the spot. Then sweep the boxes left to right: they come out *pre-sorted*, for free. Same neighbor scan, same wraparound.
>
> That's `O(n)` time and `O(1)` space — the array is a fixed 1440, it never grows with `n`.
>
> Say it out loud in the interview: *"If I exploit the fixed 1440-value range, I can bucket into a boolean array and get linear time, constant space."* Leading with the sort but *naming* the bucket upgrade — that's the strong-hire signal.

---

## 12. YOUR TURN (active recall) — `9:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Absolute Difference (LC 1200)". A blank editor.]**

> Before the next video, try **Minimum Absolute Difference**. Same skeleton — sort, then the closest pair is adjacent — but *no* clock wrap to trip you up. It'll cement the "sort then look next-door" reflex without the midnight twist.
>
> Don't peek. Wrestle it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `9:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Convert `HH:MM` to minutes 0–1439**, then **sort** — the closest pair is always adjacent.
> 2. **Add the wraparound gap** `(first + 1440) − last` — the one pair sorting hides across midnight.
> 3. **Pigeonhole**: more than 1440 times → a duplicate must exist → answer is 0. And a 1440-bucket array gets you `O(n)` time, `O(1)` space.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "It's a clock, not a ruler — remember to wrap around midnight."]**
>
> When you see times and "smallest gap," your hand reaches for *sort the minutes* — and your other hand reaches for *the wraparound*.
>
> *(GCA reminder — for the interview itself: Google scores how you think out loud. Ask the clarifying question — "these wrap around midnight, right?" — before you write a line, then narrate brute force → sort → the wrap fix. Naming the wraparound out loud is worth more than the code that handles it.)*

---

## 14. CLIFFHANGER — `10:20`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Group Anagrams" — a pile of scrambled words sorting themselves into buckets.]**

> Today the trick was sorting *numbers* to make neighbors reveal the answer. But what if the thing you need to sort is **inside each string** — where two words are "the same" only after you rearrange their letters? That's next: Group Anagrams. Sorting again — but this time it's the *key*, not the list. See you there.
