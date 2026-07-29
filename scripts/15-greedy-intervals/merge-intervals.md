# 🎬 Recording Script — Merge Intervals
**Pattern: Greedy & Intervals · LeetCode 56 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the *first* interval problem. It sets up the sort-then-sweep skeleton every later one reuses.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a calendar app. Four overlapping meeting blocks stacked messily on a day view, times jumbled. A red "double-booked" badge blinks.]**

> Your calendar looks like this. Meetings piled on top of each other, some overlapping, some not — and someone asks: *"What blocks of time am I actually busy?"*
>
> This is Merge Intervals, and Google asks it constantly. The trap is that the meetings arrive in random order, so the overlaps are scattered everywhere. You *can* brute-force it — but you'll write an ugly loop that re-scans forever.
>
> By the end of this video you'll have a single clean sweep that does it in one pass, and — more important — you'll own the one idea that unlocks *every* interval problem after this. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, four interval bars drawn on a horizontal timeline: `[1,3]`, `[2,6]`, `[8,10]`, `[15,18]`, each a colored bar spanning its start-to-end on a number line 0…18.]**

> The whole problem in one line: **combine every group of overlapping intervals into one.**
>
> Here's our tiny example — four intervals, drawn as bars on a timeline. Look at `[1,3]` and `[2,6]`: they touch and overlap between 2 and 3, so they're really one busy block from 1 to 6. `[8,10]` sits alone. `[15,18]` sits alone.
>
> So the answer is three bars: `[1,6]`, `[8,10]`, `[15,18]`. Hold that picture — we'll get there by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: the four bars, but now in the messy *input* order. Arrows shoot between every pair checking for overlap; a "comparisons" counter ticks up. When a merge happens, a new bar appears and arrows restart from the top.]**

> Let's do what your brain does first: compare every pair, and whenever two overlap, fuse them. `[1,3]` vs `[2,6]`? Overlap — merge to `[1,6]`. Now the set changed, so… start over. `[1,6]` vs `[8,10]`? No. vs `[15,18]`? No.
>
> **[VISUAL: counter ticking, arrows restarting after each merge.]**
>
> See the problem? Every time I merge, a new interval appears that might overlap something I already checked — so I loop again and again. Pairs times passes. That's O(n²), sometimes worse.
>
> And it's all because the intervals are in a jumbled order. The overlaps are hiding all over the list.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the jumbled bars. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So here's the waste: the overlaps are scattered, so I keep re-scanning to find who belongs with whom.
>
> **LEARNER:** Right, but they're just given in random order. There's nothing to exploit — you kind of *have* to check everything, no?
>
> **TEACHER:** That's the exact instinct we break. Pause the video and ask yourself one question: **what could I do to these intervals *first* so that any two that overlap are guaranteed to sit right next to each other?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the four bars slide and reorder by their left edge — sorted by start: `[1,3]`, `[2,6]`, `[8,10]`, `[15,18]`. A left-to-right sweep line begins moving across the timeline.]**

> The clue: nobody said they were sorted — so **sort them by start time** ourselves. Watch what that unlocks.
>
> Once sorted, every interval starts at or after the one before it. So think of walking left to right, holding one "current" merged block in your hand. Any interval that could overlap your current block *has to be the very next one* — there's nowhere else for it to hide, because everything after it starts even later.
>
> Trace it. Current = `[1,3]`. Next is `[2,6]`. Does 2 land at or before my current end, 3? Yes — they overlap. So I stretch my block's end to the max of 3 and 6, giving `[1,6]`. Next is `[8,10]`. Does 8 land at or before 6? No — there's a gap. So `[1,6]` is finished; freeze it, and `[8,10]` becomes my new current block. Same for `[15,18]`.
>
> **[VISUAL: the sweep line passing each bar; current block stretching on overlap, freezing and starting fresh on a gap. Comparisons counter crawls: 1, 2, 3.]**
>
> Same answer. One pass. No restarting.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Sort by start → sweep → overlap when next.start ≤ current.end."]**

> Burn this line in: **sort by start, then sweep — the next interval overlaps when its start is ≤ your current end.**
>
> That sentence is the backbone of nearly every interval problem you'll ever see. Merge, insert, count rooms — they all start here.

---

## 7. CODE IT — LIVE & CHUNKED — `4:50`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, sort by start and seed the answer with the first interval.

```python
def merge(intervals):
    intervals.sort(key=lambda iv: iv[0])   # sort by start
    merged = [intervals[0]]
```

> **[VISUAL: add chunk 2, highlight it.]** Now sweep the rest. For each one, look at the last block we're building.

```python
    for start, end in intervals[1:]:
        last = merged[-1]
```

> **[VISUAL: add chunk 3.]** The whole decision — overlap or gap.

```python
        if start <= last[1]:               # overlap → extend
            last[1] = max(last[1], end)
        else:                              # gap → start a new block
            merged.append([start, end])
    return merged
```

> Three lines of logic. That's the entire algorithm.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `intervals.sort(key start)` — the whole foundation. Without it, the "overlap has to be the next one" guarantee collapses, and we're back to O(n²).
>
> `merged = [intervals[0]]` — seed with the first block so we always have a "current" to compare against.
>
> `if start <= last[1]` — this is the sweep rule. If the next start lands at or before the current end, the bars touch, so they merge.
>
> **LEARNER:** Quick one — why `max(last[1], end)`? If they overlap, isn't the new interval's end always bigger?
>
> **TEACHER:** Sharp catch, and no — this is the bug everyone ships. Picture `[1,9]` then `[2,5]`. They overlap, but `[2,5]` is *swallowed inside* `[1,9]`. If I just set the end to 5, I'd shrink my block to `[1,5]` and lose everything from 5 to 9. Taking the `max` says: never let a merged block get shorter.
>
> And the `else` — a real gap means this block is done, so we freeze it and open a fresh one.

---

## 9. DRY-RUN THE CODE — `7:25`
*(worked example — prove it, close the loop)*

**[VISUAL: sorted bars with a trace table filling row by row, sweep line moving.]**

> Let's run the actual code on our four intervals.

| next | `merged[-1]` before | `start ≤ end`? | action | `merged` after |
|---|---|---|---|---|
| — | — | — | seed | `[[1,3]]` |
| `[2,6]` | `[1,3]` | 2 ≤ 3 ✅ | end = max(3,6) = 6 | `[[1,6]]` |
| `[8,10]` | `[1,6]` | 8 ≤ 6 ❌ | gap → append | `[[1,6],[8,10]]` |
| `[15,18]` | `[8,10]` | 15 ≤ 10 ❌ | gap → append | `[[1,6],[8,10],[15,18]]` |

> Output: `[[1,6],[8,10],[15,18]]`. Exactly the three bars we saw at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²)+. Ours: O(n log n). A note: "sort dominates".]**

> Say it the way you would to the interviewer: *"Brute force is at least O(n squared) because merges can cascade and force repeated passes. My version sorts once — that's n-log-n — then a single linear sweep, so O(n log n) overall, dominated entirely by the sort."*
>
> That framing — name the brute force, name the improvement, name what dominates — is exactly what earns the checkmark.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:55`
*(depth + honesty)*

**[VISUAL: the output list highlighted; a note "output is the floor". Then a write-pointer version overwriting the input array in place.]**

> Honest answer: the output list is unavoidable. In the worst case — nothing overlaps — we return all `n` intervals, so O(n) output is the floor. Naming that floor is itself a skill.
>
> But the *auxiliary* space you can shrink. Instead of a new list, merge in place with a write pointer — overwrite the sorted array as you go and slice at the end.

```python
def merge_inplace(intervals):
    intervals.sort(key=lambda iv: iv[0])
    w = 0
    for start, end in intervals[1:]:
        if start <= intervals[w][1]:
            intervals[w][1] = max(intervals[w][1], end)
        else:
            w += 1
            intervals[w] = [start, end]
    return intervals[:w + 1]
```

> Say it in the room: *"Output has to be O(n), but I can keep auxiliary space O(1) by merging in place with a write pointer."*

---

## 12. YOUR TURN (active recall) — `9:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Insert Interval (LC 57)". A pre-sorted list of bars with one new bar to slot in.]**

> Before the next video, try **Insert Interval**. This time the list is *already sorted and non-overlapping*, and you insert one new interval. Ask yourself: since it's pre-sorted, can you skip the sort entirely and do it in one linear pass?
>
> Struggle with it for ten minutes before you watch. That struggle is what moves this from "I saw it" to "I own it."

---

## 13. LOCK IT IN — `10:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Sort by start** — it's what makes overlaps become neighbors.
> 2. **Overlap when `next.start ≤ current.end`** — the one comparison.
> 3. **Take the `max` of the ends** — never let a merged block shrink.
>
> And the memory peg — when you see intervals in *any* order, your hand should move first: **sort by start, then sweep.**

---

## 14. CLIFFHANGER — `10:35`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Insert Interval" — with the list already sorted.]**

> Sorting was the price of admission here. But what if the intervals arrive *already sorted*, and you just need to drop one new one into the mix? Paying for a full sort would be throwing away a gift. Next up: Insert Interval — same sweep, but we get to be smarter about the sort. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> merged = new ArrayList<>();
    for (int[] iv : intervals) {
        if (merged.isEmpty() || iv[0] > merged.get(merged.size() - 1)[1]) {
            merged.add(iv);
        } else {
            merged.get(merged.size() - 1)[1] =
                Math.max(merged.get(merged.size() - 1)[1], iv[1]);
        }
    }
    return merged.toArray(new int[merged.size()][]);
}
```
