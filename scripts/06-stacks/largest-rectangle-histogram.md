# 🎬 Recording Script — Largest Rectangle in Histogram
**Pattern: Stacks (Monotonic) · LeetCode 84 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the monotonic stack from Next Greater Element & Daily Temperatures — now in *both* directions.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a histogram of bars `[2, 1, 5, 6, 2, 3]`. A rectangle sweeps across, resizing, hunting for the biggest area. A red "TLE" flickers on a brute-force attempt.]**

> This one shows up in Google final rounds, and it breaks people. *"Given a histogram, find the largest rectangle you can fit inside it."*
>
> **[VISUAL: the winning rectangle snaps over bars 5 and 6 — height 5, width 2, area 10.]**
>
> The catch: a rectangle's height is capped by the *shortest* bar it covers. So every rectangle is a negotiation between height and width. The brute force tries every span — O(n²) — and times out. The elegant answer is *one* monotonic-stack pass where the entire rectangle for a bar gets computed in the instant you pop it. It feels like magic the first time. By the end, you'll see it's not. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: bars `[2, 1, 5, 6, 2, 3]` with index labels. Height axis on the left.]**

> The problem in one line: **find the largest-area rectangle that fits inside the histogram**, where the rectangle's height can't exceed any bar it spans.
>
> Tiny example: `[2, 1, 5, 6, 2, 3]`. The best rectangle sits on bars at index 2 and 3 — heights 5 and 6. If I want to cover both, my height is capped at 5 — the shorter one — and my width is 2. Area `5 × 2 = 10`.
>
> **[VISUAL: try a taller-but-narrower rectangle on bar 3 alone: 6 × 1 = 6. Then the width-2 one: 10. The 10 wins.]**
>
> Could I go taller? Bar 3 alone is height 6, but width 1 — area 6. Less. The answer is `10`. The whole tension: **taller means narrower, wider means shorter.** We need the best trade.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:35`
*(worked example — let them feel the waste)*

**[VISUAL: fix a left edge; extend right; a running "min height" line drops as a shorter bar appears; area recomputed each step.]**

> Brute force: pick every possible rectangle. Fix a left edge, extend right one bar at a time, track the minimum height so far, and at each step compute `min_height × width`.
>
> Start at bar 2 (height 5). Extend to bar 3 — min is still 5, width 2, area 10. Extend to bar 4 (height 2) — min drops to 2, width 3, area 6. Every extension, recompute.
>
> **[VISUAL: nested loops light up; a comparisons counter climbs fast; n = 100,000 → ~5 billion.]**
>
> It's correct — it literally enumerates every span. But it's two nested loops over n bars — O(n²). At 100k bars, five billion iterations. Time Limit Exceeded. We're recomputing minimums over overlapping spans endlessly.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight one bar; two arrows point outward — "how far left?" and "how far right?". A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Let's reframe to escape the O(n²). Instead of every span, think per *bar*: let each bar be the **shortest** bar of its rectangle. Then that rectangle's height is fixed — the bar's own height — and the only question is width: **how far left and how far right can this bar extend before it hits a shorter bar?**
>
> **LEARNER:** Okay, so for each bar I find the nearest shorter bar on each side… but scanning for that is O(n) per bar. Isn't that just O(n²) again, wearing a different hat?
>
> **TEACHER:** *Exactly* the right worry — and it's the whole crux. "Nearest smaller element on each side" by scanning *is* O(n²). Pause and think: **we already have a tool that finds the nearest smaller element in one pass. Which one — and could a single pass somehow give us BOTH sides at once?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:35`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a stack column labeled "bars, increasing height, bottom→top". Sweep the histogram left to right; tiles = indices, heights shown.]**

> "Nearest smaller element" is the textbook **monotonic stack** job — the same tool from the last two lessons. Reminder: a *monotonic stack* keeps its values sorted, only ever increasing or only ever decreasing bottom to top. Last time we kept it decreasing; here we keep it **increasing** in height.
>
> Here's the beautiful part — one pass gives us *both* boundaries. Keep a stack of bar indices with increasing heights. When a new bar arrives that's **shorter** than the top, that's the trigger: pop the top bar and finalize *its* rectangle right now. Because at that exact moment we know **both** its walls:
>
> - The new, shorter bar is its **right boundary** — the first shorter bar to its right.
> - The bar now exposed *beneath* it on the stack is its **left boundary** — the first shorter bar to its left.
>
> **[VISUAL: sweep [2,1,5,6,2,3]. Push 0(h2). i=1(h1) < top → pop bar 0. Right wall = index 1, left wall = nothing (stack empty). Width = 1. Area 2. Push 1.]**
>
> Watch. Push bar 0, height 2. Bar 1, height 1 — shorter than the top! Pop bar 0. Its right wall is bar 1; to its left the stack is empty, so it extends to the very edge. Width 1, area 2.
>
> **[VISUAL: push 1,2,3 (heights 1,5,6 — increasing, all pushed). i=4(h2) < top 6 → pop bar 3: right wall=4, left wall=bar 2. width = 4−2−1 = 1, area 6. Still < ... pop bar 2(h5): right wall=4, left wall=bar 1. width = 4−1−1 = 2, area 10!]**
>
> Bars 1, 5, 6 — increasing — all pushed. Then bar 4, height 2. Shorter than the top, bar 3 (height 6). Pop bar 3: right wall is bar 4, left wall is the bar now exposed beneath — bar 2. Width is `4 − 2 − 1 = 1`. Area 6. Still shorter than the new top, bar 2 (height 5)? Yes. Pop bar 2: right wall bar 4, left wall bar 1. Width `4 − 1 − 1 = 2`. Area **10.** There it is.
>
> **[VISUAL: highlight the width formula: `width = right − left − 1`. The two walls glow.]**
>
> The instant we pop, both walls are known, so the rectangle is computed in O(1). That's the magic — the increasing stack means everything between the two walls was *taller* than the popped bar, so it can span that whole width at its own height.

---

## 6. THE KEY MOVE (signaling) — `5:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Increasing stack. Shorter bar arrives → pop & measure: width = right − left − 1."]**

> Burn this in: **keep an increasing stack of bar indices; when a shorter bar arrives, pop the top and measure its rectangle — the new bar is the right wall, the exposed bar beneath is the left wall, width is `right − left − 1`.**
>
> The pop *event* is where the area gets finalized. That's the sentence that unlocks the whole family of "span limited by nearest-smaller-on-each-side" problems.

---

## 7. CODE IT — LIVE & CHUNKED — `6:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. A stack of indices, a running best, and — the clever bit — a trailing zero appended to the heights.

```python
def largest_rectangle(heights):
    stack = []                     # indices, heights increasing bottom -> top
    best = 0
    for i, h in enumerate(heights + [0]):
```

> **[VISUAL: highlight the `+ [0]`.]** That trailing `0` is a sentinel — shorter than every real bar, so at the end it forces every remaining bar to pop and get measured. Nothing left un-finalized.
>
> **[VISUAL: add chunk 2, highlight it. Stack column on the right.]** Now the pop-and-measure loop.

```python
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]          # the bar we're finalizing
            left = stack[-1] if stack else -1      # nearest shorter bar to the left
            width = i - left - 1                   # span between the two walls
            best = max(best, height * width)
        stack.append(i)
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:15`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as named.]**

> Let's walk the *why*.
>
> `heights[stack[-1]] >= h` — while the top bar is at least as tall as the incoming one, it's time to finalize it, because the incoming bar is its right wall.
>
> `left = stack[-1] if stack else -1` — after popping, whatever's now on top is the nearest shorter bar to the left. If the stack is empty, this bar reaches all the way to the left edge, which we represent as index `-1`.
>
> `width = i - left - 1` — the span strictly *between* the two walls. Both walls are shorter, so the popped bar fills everything between them at its own height.
>
> `heights + [0]` sentinel — flushes the stack at the end so every bar is measured.
>
> **LEARNER:** Two things bug me. First — why `>=` when popping, not `>`? And second — that `width = i − left − 1`, with the empty-stack case using `left = −1`. Walk me through why the `−1` gives the right width.
>
> **TEACHER:** Both are the real subtleties, good. **The `>=`:** when a new bar *ties* the top's height, we still pop. Why is that safe? Because any area the tied bar could have contributed gets fully recovered when *it* gets popped later — it, in turn, will span across. Treating equal-height as a right boundary loses nothing, and it keeps the logic uniform. **The `−1`:** picture bar 1 in our example, height 1 — when the sentinel pops it, the stack is empty, so `left = −1`. Width is `i − left − 1 = 6 − (−1) − 1 = 6`. That's the full width of all six bars — correct, because height-1 is the shortest bar and genuinely spans the entire histogram. The `−1` is a virtual wall just off the left edge, so the formula `right − left − 1` counts every real bar in between.

---

## 9. DRY-RUN THE CODE — `8:45`
*(worked example — prove it, close the loop)*

**[VISUAL: histogram with trailing 0 at index 6; stack column of indices growing/shrinking; trace table filling.]**

> Let's run the real code on `[2, 1, 5, 6, 2, 3]` with the sentinel `0` at index 6. Stack holds indices; heights in parentheses.

| i | h | pops → area computed | stack after |
|---|---|---|---|
| 0 | 2 | — | `[0]` (2) |
| 1 | 1 | pop 0: h=2, left=−1, width=1, area **2** | `[1]` (1) |
| 2 | 5 | — | `[1,2]` (1,5) |
| 3 | 6 | — | `[1,2,3]` (1,5,6) |
| 4 | 2 | pop 3: h=6, left=2, width=1, area 6; pop 2: h=5, left=1, width=2, area **10** | `[1,4]` (1,2) |
| 5 | 3 | — | `[1,4,5]` (1,2,3) |
| 6 | 0 | pop 5: h=3, left=4, width=1, area 3; pop 4: h=2, left=1, width=4, area 8; pop 1: h=1, left=−1, width=6, area 6 | `[6]` |

> Best over the whole run = **10**, from popping bar 2 — height 5, width 2. Exactly the rectangle we spotted at the start. Loop closed, in a single O(n) pass.

---

## 10. COMPLEXITY, OUT LOUD — `10:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n²). Ours: O(n) time, O(n) space.]**

> Say it in the room: *"Brute force tries every span — O(n²), which times out at 100k. The monotonic stack finds each bar's nearest-shorter boundary on both sides in a single pass: every index is pushed once and popped once, so it's O(n) time. Space is O(n) for the stack."*
>
> And the killer sentence that shows you *understand* it: *"The pop event is where I finalize a rectangle — the incoming shorter bar is the right wall, the exposed bar beneath is the left wall, so I compute the full area right there in O(1)."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:45`
*(depth + honesty)*

**[VISUAL: a strictly increasing histogram `[1,2,3,4,5]`; every bar stacks up, tall column, nothing pops until the sentinel.]**

> Can we beat O(n) space? Honestly, no — and knowing *why* is the strong-hire detail.
>
> Worst case is a strictly increasing histogram — `[1, 2, 3, 4, 5]`. No bar is ever shorter than the top, so nothing pops until the sentinel at the very end. All n indices sit on the stack at once. You genuinely need to remember every un-finalized bar, so you can't drop below O(n) for the single-pass method.
>
> **LEARNER:** What about precomputing two boundary arrays — nearest-smaller-left and nearest-smaller-right — then one area pass? Cleaner to reason about, right?
>
> **TEACHER:** It *is* cleaner to explain, and it's a fine answer to *sketch* — but it uses *more* memory: two O(n) arrays plus the stacks to build them. Same O(n) class, strictly bigger constant. There's also a divide-and-conquer on the minimum bar, but it's O(n log n) average and O(n²) worst case — worse. Honest verdict for the room: *"The single-pass stack is O(n) time and O(n) space, and the space is unavoidable because an increasing histogram keeps every bar unresolved until the end. I'll keep it — it's optimal on time and can't beat O(n) space."*

---

## 12. YOUR TURN (active recall) — `12:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Maximal Rectangle (LC 85)". A binary matrix, each row becoming a histogram.]**

> Before the next video, try **Maximal Rectangle**, LC 85 — the boss's boss. You're given a binary matrix and must find the largest all-ones rectangle. The trick: treat each row as the base of a histogram of consecutive ones above it, and run *this exact algorithm* on every row. You already have the hard part.
>
> Fifteen minutes of struggle before you look. This is the one that proves you own the pattern.

---

## 13. LOCK IT IN — `12:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Reframe:** let each bar be the *shortest* bar of its rectangle → the problem becomes "nearest shorter bar on each side."
> 2. **Increasing monotonic stack** finds *both* walls in one pass — the pop event finalizes the rectangle.
> 3. **`width = right − left − 1`**, and a **trailing sentinel `0`** flushes everything; `left = −1` is the virtual wall past the edge.
>
> And the peg: **we pop while the new element beats the top** — and the instant a bar falls off, both its walls are standing right there, so measure it *now*.

---

## 14. CLIFFHANGER — `13:10`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Trapping Rain Water". Bars with blue water pooled between them.]**

> We used the stack to measure the biggest *solid* rectangle. Flip the question: what if you pour water over the bars — how much pools in the *dips* between them? Same monotonic stack, but now every pop measures a little trapped puddle instead of a rectangle. That's next: Trapping Rain Water. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();   // indices, increasing heights
    int best = 0, n = heights.length;
    for (int i = 0; i <= n; i++) {
        int h = (i == n) ? 0 : heights[i];       // trailing sentinel
        while (!stack.isEmpty() && heights[stack.peek()] >= h) {
            int height = heights[stack.pop()];
            int left = stack.isEmpty() ? -1 : stack.peek();
            int width = i - left - 1;
            best = Math.max(best, height * width);
        }
        stack.push(i);
    }
    return best;
}
```
