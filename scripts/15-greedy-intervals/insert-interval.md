# 🎬 Recording Script — Insert Interval
**Pattern: Greedy & Intervals · LeetCode 57 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Merge Intervals (LC 56) — the sort-then-sweep skeleton.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tidy calendar — meeting bars neatly laid out left to right, no overlaps. A new bar drops in from the top and lands across two of them, turning them red.]**

> You just solved Merge Intervals, so your instinct here is easy: to insert one new meeting, just append it and re-run the whole merge.
>
> That *works*. But there's a catch the interviewer is watching for — the list you're inserting into is *already sorted and non-overlapping*. If you re-sort it, you're paying for order you were handed for free.
>
> By the end of this video, you'll insert that new interval in a single linear pass, no sort at all — and you'll know exactly why that's the answer they want. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, five sorted non-overlapping bars on a timeline: `[1,2] [3,5] [6,7] [8,10] [12,16]`. A separate new bar `[4,8]` floats above.]**

> One line: **drop a new interval into an already-sorted, non-overlapping list, merging wherever it touches.**
>
> Here's the example. Five neat bars, in order, no overlaps. The new one is `[4,8]`. Look where it lands — it stretches across `[3,5]`, `[6,7]`, and `[8,10]`. It's going to swallow all three into one bar.
>
> The answer: `[1,2]`, then the merged `[3,10]`, then `[12,16]`. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: the new bar appended messily to the end, then the whole list re-sorting with a spinning "sort" badge, then a full merge sweep.]**

> The obvious move, straight from last lesson: append `[4,8]` to the end, sort the whole thing, then run Merge Intervals.
>
> **[VISUAL: "sort" badge spins over the six bars.]**
>
> It gives the right answer. But watch what that sort is doing — it's re-establishing an ordering that was *already there*. Five of these six bars were in perfect order. We shuffled them just to put them right back.
>
> That sort costs us n-log-n. And it's completely wasted work.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The "sort" badge gets a red strike through it. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is that sort. The input was already sorted — we threw the gift away.
>
> **LEARNER:** Okay, but the new interval could land anywhere. How do I merge it in without sorting to find its spot?
>
> **TEACHER:** Great question — and here's the setup. Because the list is sorted, the intervals fall into three clean groups relative to the new one. Pause and predict: **what are the three kinds of interval — the ones totally before the new one, the ones that overlap it, and the ones totally after?** How would you tell them apart with a single comparison each?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the timeline splits into three colored zones around the new bar `[4,8]`. Zone 1 (before) = `[1,2]`. Zone 2 (overlapping) = `[3,5] [6,7] [8,10]`. Zone 3 (after) = `[12,16]`.]**

> Here's the aha. Sweep left to right and split the timeline into three zones around the new interval `[4,8]`, start = 4, end = 8.
>
> **Zone 1 — everything totally before it.** An interval is safely before if it *ends before* the new one starts: its end < 4. `[1,2]` ends at 2, that's before 4 — copy it as-is, it can't overlap.
>
> **Zone 2 — everything that overlaps.** An interval overlaps if its *start* is at or before the new end, 8. `[3,5]` starts at 3 ≤ 8, overlaps. `[6,7]` starts at 6 ≤ 8, overlaps. `[8,10]` starts at 8 ≤ 8, overlaps. For each, I grow the new interval — pull its start down to the `min`, push its end up to the `max`. After absorbing all three, `[4,8]` has become `[3,10]`.
>
> **Zone 3 — everything totally after.** `[12,16]` starts at 12, past 10 — copy as-is.
>
> **[VISUAL: emit one merged bar `[3,10]` between zones 1 and 3.]**
>
> And here's the beautiful part: because the input is sorted, those overlapping intervals are guaranteed to be **one unbroken run**. You can never have a non-overlapping interval trapped between two overlapping ones. So it's three simple phases, one pass.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Copy-before · absorb-overlap (min start, max end) · copy-after — one pass, no sort."]**

> The key move: **copy the ones before, absorb the overlapping run into the new interval, copy the ones after — all in one linear pass, no sort.**
>
> Pre-sorted input plus insert-one is the signal. Recognizing you can drop the log factor is the whole point.

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Set up the result and pull the new interval's start and end into `s` and `e`.

```python
def insert(intervals, newInterval):
    result = []
    i, n = 0, len(intervals)
    s, e = newInterval[0], newInterval[1]
```

> **[VISUAL: add chunk 2, highlight.]** Zone 1 — copy every interval that ends before the new one starts.

```python
    while i < n and intervals[i][1] < s:
        result.append(intervals[i])
        i += 1
```

> **[VISUAL: add chunk 3.]** Zone 2 — absorb the overlapping run, growing `s` and `e`, then emit the merged interval once.

```python
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    result.append([s, e])
```

> **[VISUAL: add chunk 4.]** Zone 3 — copy the rest.

```python
    while i < n:
        result.append(intervals[i])
        i += 1
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:20`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why each piece exists.
>
> Zone 1's test is `intervals[i][1] < s` — I compare the interval's *end* to the new *start*. Only if it ends before we begin is it safely clear.
>
> **LEARNER:** Wait — in Zone 1 you compare *ends*, but in Zone 2 you compare *starts*. Why the switch?
>
> **TEACHER:** Because the two zones ask opposite questions. Zone 1 asks "are you completely done before I start?" — that's about your *end*. Zone 2 asks "do you begin before I finish?" — that's about your *start*. Different question, different endpoint. That asymmetry is exactly what trips people up here.
>
> Zone 2 grows the interval with `min` of starts and `max` of ends — same "never shrink" idea from Merge Intervals, but now we also pull the *start* down since the new interval might begin earlier than what it absorbs.
>
> And we `append([s, e])` exactly once, right after the overlap run ends — that single emit is the merged block sitting cleanly between the before-zone and the after-zone.

---

## 9. DRY-RUN THE CODE — `7:35`
*(worked example — prove it, close the loop)*

**[VISUAL: the five bars, trace table filling row by row, `s`/`e` updating.]**

> Run it on `[[1,2],[3,5],[6,7],[8,10],[12,16]]`, new = `[4,8]`, so `s=4, e=8`.

| phase | interval | test | action |
|---|---|---|---|
| Zone 1 | `[1,2]` | end 2 < 4 ✅ | copy → `[[1,2]]` |
| Zone 1 | `[3,5]` | end 5 < 4 ❌ | stop Zone 1 |
| Zone 2 | `[3,5]` | start 3 ≤ 8 ✅ | s=3, e=8 |
| Zone 2 | `[6,7]` | start 6 ≤ 8 ✅ | s=3, e=8 |
| Zone 2 | `[8,10]` | start 8 ≤ 8 ✅ | s=3, e=10 |
| Zone 2 | `[12,16]` | start 12 ≤ 10 ❌ | stop → append `[3,10]` |
| Zone 3 | `[12,16]` | — | copy |

> Output: `[[1,2],[3,10],[12,16]]`. Exactly what we predicted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:25`
*(transfer to interview)*

**[VISUAL: two rows — Append + re-sort: O(n log n). Three-zone sweep: O(n).]**

> Say it out loud: *"The append-and-re-merge answer is O(n log n) because of the sort. But the input is already sorted and non-overlapping, so I don't need to sort — a single three-zone sweep touches each interval once. That's O(n) time."*
>
> Beating the log factor because you noticed the input was pre-sorted — that's the exact signal an interviewer is grading.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:55`
*(depth + honesty)*

**[VISUAL: the result list highlighted; a note "output = floor". Beside it, the variables `i, s, e` circled: "O(1) aux".]**

> The output holds up to `n+1` intervals, so O(n) output is the floor — same story as before.
>
> But look at the *auxiliary* space: just three integers, `i`, `s`, and `e`. No sort scratch, no extra structure. This is the cleanest interval solution in the whole set — one pass, constant extra memory.
>
> Say it: *"O(n) output, but O(1) auxiliary — and because there's no sort, there isn't even sort scratch space to account for."*

---

## 12. YOUR TURN (active recall) — `9:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Non-overlapping Intervals (LC 435)". Bars with a couple overlapping.]**

> Before the next video, try **Non-overlapping Intervals**: given intervals, find the *minimum* you must remove so none overlap. Here's a hint that'll bend your brain — you might sort by *end*, not start. Sit with why that could matter.
>
> Ten minutes of struggle first. Then watch.

---

## 13. LOCK IT IN — `10:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Pre-sorted input means skip the sort** — one pass, O(n).
> 2. **Three zones:** before (compare ends), overlapping (compare starts), after.
> 3. **Grow with min-start, max-end,** emit the merged block once.
>
> Memory peg: **before, overlap, after — one sweep, no sort.**

---

## 14. CLIFFHANGER — `10:30`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Non-overlapping Intervals" with a "sort by END?" sticky note.]**

> So far we've always sorted by *start*. But the next problem — removing the fewest intervals to kill all overlaps — is secretly the classic "activity selection" problem, and there, sorting by start gives you the wrong answer. You have to sort by **end**. Why does the sort key flip? That's the next one. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> result = new ArrayList<>();
    int i = 0, n = intervals.length;
    int s = newInterval[0], e = newInterval[1];

    while (i < n && intervals[i][1] < s) result.add(intervals[i++]);

    while (i < n && intervals[i][0] <= e) {
        s = Math.min(s, intervals[i][0]);
        e = Math.max(e, intervals[i][1]);
        i++;
    }
    result.add(new int[]{s, e});

    while (i < n) result.add(intervals[i++]);

    return result.toArray(new int[result.size()][]);
}
```
