# 🎬 Recording Script — Non-overlapping Intervals
**Pattern: Greedy & Intervals · LeetCode 435 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Merge Intervals & Insert Interval — both sorted by *start*. This one flips to sorting by *end*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a timeline with five overlapping meeting bars fighting for the same slot. A hand plucks one out; the rest snap into a clean non-overlapping row.]**

> You've got a pile of meetings that overlap, and one conference room. You can't attend clashing meetings — so some have to go. The question: **what's the fewest you can cancel so the rest never overlap?**
>
> Your gut says "sort them and greedily keep some." Good instinct. But there's a twist that catches almost everyone: in the last two videos we sorted by *start*. Here, sorting by start gives you a **wrong answer**. You have to sort by **end**.
>
> By the end you'll not just know that — you'll be able to *prove* why the earliest-finishing meeting is always the safe greedy choice. That proof is what separates a hire from a maybe. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, four bars on a timeline: `[1,2] [2,3] [3,4]` neatly end-to-end, plus `[1,3]` spanning across the first two.]**

> One line: **remove the minimum number of intervals so the rest don't overlap.**
>
> Tiny example: `[1,2]`, `[2,3]`, `[3,4]`, and `[1,3]`. Look at the picture — `[1,2]`, `[2,3]`, `[3,4]` sit end to end perfectly. But `[1,3]` sprawls across the first two, clashing with both.
>
> So the answer is **1** — remove `[1,3]`, and the other three live in peace. Notice: bars that only *touch* at an endpoint, like `[1,2]` and `[2,3]`, don't count as overlapping. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a branching tree — each interval forks into "keep" and "drop". Branches explode: 2, 4, 8, 16 leaves.]**

> The brute-force instinct: for each interval, either keep it or drop it, and find the combination that leaves the most non-overlapping intervals. Then removals = total minus that max.
>
> **[VISUAL: the keep/drop tree doubling at each level.]**
>
> But look — every interval doubles the tree. Four intervals, sixteen combinations. Twenty intervals? Over a million. That's O(2ⁿ) — exponential. Dead on arrival for any real input.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze the exploding tree. Reframe text slides in: "min remove  =  max keep". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** First, reframe. "Remove the fewest" is the same as "**keep the most** non-overlapping intervals." Answer = total minus max kept. Now it's a packing problem: fit as many compatible meetings as you can.
>
> **LEARNER:** So it's greedy — keep meetings one by one. But greedy always scares me. **How do we KNOW the greedy choice is safe?** What if keeping one meeting now blocks two better ones later?
>
> **TEACHER:** That is *exactly* the right fear, and we're going to answer it head-on in a minute. First, pause and predict: **if you could keep only meetings that don't clash, which single property of a meeting makes it the "safest" one to keep first?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the four bars reorder by their *right* edge — sorted by end: `[1,2] [2,3] [1,3] [3,4]`. A vertical "last kept end" line starts at −∞ and marches right.]**

> Here's the analogy: it's a day of back-to-back meetings and you want to attend as many as possible. Which one do you commit to first? **The one that finishes earliest** — because it frees you up soonest, leaving the most room for everything after.
>
> So: **sort by end time.** Then sweep, tracking the end of the last meeting you kept. For each interval, if it **starts at or after** that last end, it doesn't clash — keep it, and move your "last end" forward. If it starts *before* — it overlaps the one you kept, so it's a removal.
>
> **[VISUAL: sweep. Keep `[1,2]` → last end = 2. Keep `[2,3]` (2 ≥ 2) → last end = 3. `[1,3]` starts at 1 < 3 → drop. Keep `[3,4]` (3 ≥ 3) → last end = 4.]**
>
> Kept three, removed one. And notice — the greedy never had to look ahead or backtrack. Each choice was local.

---

## 5b. WHY THE GREEDY IS SAFE (the exchange argument) — `4:10`
*(confronting the misconception head-on)*

**[VISUAL: two candidate "next picks" drawn — one ending at time 3, one ending at time 6. A shaded "room left after" region: the earlier-ending one leaves a bigger shaded region.]**

> Back to that fear: *how do we know keeping the earliest finisher never costs us?* Here's the proof, and it's clean.
>
> Suppose among your remaining choices, the earliest-ending interval is A, ending at time 3. Some other valid pick B ends later, at 6. Claim: **you never lose by taking A over B.** Why? A's end is ≤ B's end. So *anything* that would fit after B — starting at 6 or later — also fits after A, because A finished even sooner. A leaves at least as much room as B, never less.
>
> So take any optimal solution, and wherever it picked a later-finisher, swap in the earliest-finisher instead — the count never drops. That's the **exchange argument**: greedy can always be matched to optimal. That's *how we know* it's safe. Not a hunch — a swap you can always make.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Sort by END → greedily keep the earliest finisher → count the rest as removed."]**

> The key move: **sort by end, greedily keep the earliest finisher, remove everything that clashes with it.**
>
> This is *activity selection* — one of the most reusable greedy patterns there is. And the lesson underneath: **your sort key follows what you're optimizing.** Merge sorted by start; this sorts by end. Choose deliberately.

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Sort by end, and set up a counter plus the last kept end.

```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda iv: iv[1])   # sort by END
    kept = 0
    last_end = float("-inf")
```

> **[VISUAL: add chunk 2, highlight.]** Sweep. Keep when compatible; advance the frontier.

```python
    for start, end in intervals:
        if start >= last_end:              # no clash → keep it
            kept += 1
            last_end = end
        # else: overlaps the last kept one → it's removed
    return len(intervals) - kept
```

> That's it. Notice we never build a "kept list" — we only *count*, because the problem asks for a number.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why each piece.
>
> `sort(key end)` — the entire greedy rests on this. Sort by start instead and the "earliest finisher" logic breaks.
>
> `last_end = -inf` — so the very first interval always passes the compatibility test.
>
> `if start >= last_end` — the compatibility check.
>
> **LEARNER:** Why `>=` and not strict `>`? Wouldn't `>` be safer?
>
> **TEACHER:** No — and this is the endpoint subtlety from the problem statement. Meetings that only *touch* — one ends at 2, the next starts at 2 — do **not** overlap. `start >= last_end` lets that handoff through: `2 >= 2` is true, so we keep it. Switch to strict `>` and you'd wrongly throw away a perfectly valid meeting.
>
> And we return `total − kept` because "min removed" is just the complement of "max kept" — the reframe from the start, cashed in.

---

## 9. DRY-RUN THE CODE — `7:55`
*(worked example — prove it, close the loop)*

**[VISUAL: sorted-by-end bars `[1,2] [2,3] [1,3] [3,4]`; trace table filling.]**

> Run it. Sorted by end: `[1,2]`, `[2,3]`, `[1,3]`, `[3,4]`.

| interval | `start ≥ last_end`? | action | kept | last_end |
|---|---|---|---|---|
| `[1,2]` | 1 ≥ −∞ ✅ | keep | 1 | 2 |
| `[2,3]` | 2 ≥ 2 ✅ | keep | 2 | 3 |
| `[1,3]` | 1 ≥ 3 ❌ | remove | 2 | 3 |
| `[3,4]` | 3 ≥ 3 ✅ | keep | 3 | 4 |

> Kept 3 of 4 → removals = 4 − 3 = **1**. Exactly the `[1,3]` we spotted at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:50`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(2ⁿ). Greedy: O(n log n).]**

> Say it: *"Brute force is O(2^n) — keep-or-drop on every interval. The greedy sorts by end, that's n-log-n, then one linear sweep, so O(n log n) overall, dominated by the sort. Extra space is O(1)."*
>
> And drop the money line: *"The greedy is provably optimal by an exchange argument — the earliest finisher leaves the most room, so swapping it into any optimal solution never lowers the count."* Interviewers love hearing *why*, not just *what*.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: just two variables circled — `kept` and `last_end`. Note: "O(1)".]**

> This one's genuinely tight. After the sort, we hold exactly two things: a counter and the last kept end. Nothing grows with the input.
>
> Say it out loud: *"Beyond the sort's own scratch space, it's O(1) — just a counter and one frontier value. There's nothing to optimize away."* Naming that an algorithm is *already* optimal, and why, is itself the mature answer.

---

## 12. YOUR TURN (active recall) — `10:10`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Arrows to Burst Balloons (LC 452)". Balloons as intervals on a line, arrows shooting up.]**

> Before the next video, try **Minimum Number of Arrows to Burst Balloons**. Balloons are intervals; one arrow bursts all balloons its x-position passes through. Minimize arrows. It's the *exact same* earliest-end greedy — you're just counting groups instead of removals. See if you can spot the twin.
>
> Ten minutes before you peek.

---

## 13. LOCK IT IN — `10:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Min remove = max keep** — reframe first.
> 2. **Sort by END, keep the earliest finisher** — activity selection.
> 3. **The exchange argument** — earliest finish leaves the most room, so greedy = optimal.
>
> Memory peg: **finish earliest, keep the most.**

---

## 14. CLIFFHANGER — `11:10`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Meeting Rooms II" with several bars stacked at the same instant.]**

> Here we *removed* clashing meetings. But what if you can't cancel any — you have to *hold them all*, and instead you're buying conference rooms? Now the question is: how many rooms at once? That's peak overlap, and it needs a completely different tool — a min-heap. Next up: Meeting Rooms II. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));  // by END
    int kept = 0;
    long lastEnd = Long.MIN_VALUE;
    for (int[] iv : intervals) {
        if (iv[0] >= lastEnd) {
            kept++;
            lastEnd = iv[1];
        }
    }
    return intervals.length - kept;
}
```
