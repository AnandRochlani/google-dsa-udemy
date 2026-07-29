# 🎬 Recording Script — Trapping Rain Water

**Pattern: Prefix-max arrays → Two Pointers · LeetCode 42 · Hard ⭐ · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** prefix/suffix arrays (Product Except Self) + "move the shorter wall" (Container With Most Water).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a bar-chart skyline of an elevation map. Rain falls. Blue water pools in the dips between bars. A big "6" fades in over the puddles.]**

> This one has a reputation. *"Given a histogram of walls, how much rain gets trapped in the gaps?"* It shows up in Google **on-sites**, and people freeze — because they stare at the *puddles* and try to reason about pools and water levels, and it spirals.
>
> The unlock is to **stop thinking about puddles.** Think about one column of water at a time. Once you make that switch, a scary Hard problem collapses into a formula — and then into two pointers and a single loop.
>
> By the end you'll solve it in O(n) time and O(1) space, and be able to *explain why* the trick is correct. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: bars for `[0,1,0,2,1,0,1,3,2,1,2,1]`, each width 1. Water shaded in the dips.]**

> The problem in one line: **each number is the height of a wall of width 1 — how many units of rain pool in the valleys?**
>
> Here's our example — twelve bars. The answer is **6** units of trapped water. Don't count them yet. We're going to *derive* that 6, not eyeball it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — the per-column insight + the waste)*

**[VISUAL: zoom on one short bar at index 2, height 0. Arrows sweep LEFT to find the tallest wall, and RIGHT to find the tallest wall.]**

> Let's find the water above **one** bar — index 2, height 0. How high can water stack here?
>
> Look left: the tallest wall to the left is height 1. Look right: the tallest wall to the right is height 3. Water can only rise to the **shorter** of those two walls — because past the shorter one, it spills over. So the level here is `min(1, 3) = 1`. Subtract the bar's own height, 0, and this column holds **1** unit.

**[VISUAL: the formula appears: water[i] = min(leftMax, rightMax) − height[i]. Then it repeats for index 5, scanning left and right AGAIN.]**

> That's the per-column insight, and it's the whole problem: `water at i = min(tallest-left, tallest-right) − height[i]`. Do it for every bar, sum it up.
>
> But look at *how* I got each answer — for every single bar, I scanned all the way left and all the way right.

**[VISUAL: a "scans" counter exploding as we repeat the left/right sweep for bar after bar.]**

> Twelve bars, each rescanning the whole array. That's O(n²) — and at 20,000 bars it's hundreds of millions of operations, mostly recomputing the same maxima over and over.

---

## 4. THE PAIN POINT + PREDICT — `2:55`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze — highlight two adjacent bars both re-scanning nearly the same left region. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The formula's right. The waste is *recomputing* "tallest wall to the left" and "tallest wall to the right" from scratch for every bar. Neighbors share almost the same answer.
>
> **LEARNER:** So couldn't I just... compute all the left-maxes once, up front? Like, one pass storing the running tallest-so-far?
>
> **TEACHER:** That is exactly leap number one — you're thinking like the solution. Pause and take it further: **if I precompute "tallest to the left of every index" and "tallest to the right of every index" in advance, how many passes total does the whole problem take?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:40`
*(elaboration + analogy — derive it)*

**[VISUAL: two arrays being filled — leftMax left-to-right, rightMax right-to-left — beneath the bars.]**

> **TEACHER:** Leap one: precompute the walls. Sweep left-to-right, carrying the tallest seen so far — that's `leftMax[i]` for every index in **one** pass. Sweep right-to-left for `rightMax[i]` in one more. Then a third pass applies the formula and sums. Three linear passes → **O(n) time**. We spent two O(n) arrays to buy it.
>
> **LEARNER:** Nice — but two full extra arrays. Can we not?
>
> **TEACHER:** That's leap two, and it's the beautiful one. Look at the formula again: `min(leftMax, rightMax)`. The water at any bar is decided by the **shorter** of the two walls. So here's the idea — walk two pointers inward from both ends, keeping just a running `leftMax` and `rightMax` as two *numbers*.

**[VISUAL: two pointers at the ends. A caption: "The shorter wall is the binding constraint."]**

> The crucial realization: if the left bar is shorter than the right bar, then whatever giant wall lives out on the right, the left column's water is *already* determined — it's capped by `leftMax`, the smaller side, and nothing further right can change that. So I can finalize the left column **now** and step the left pointer in. When the right side is shorter, I finalize *that* column and step right in.

---

## 6. THE KEY MOVE (signaling) — `5:10`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Water at i = min(leftMax, rightMax) − height[i]. The shorter wall decides → advance that pointer."]**

> Two sentences to remember. One: **water above a bar is `min(leftMax, rightMax)` minus its own height.** Two: **the shorter wall is always the bottleneck, so whichever side is lower, process it and move that pointer inward.**
>
> That second sentence is the same "move the shorter side" move from Container With Most Water — if you've done that one, this rhymes.

---

## 7. CODE IT — LIVE & CHUNKED — `5:50`
*(cognitive load — build in pieces)*

**[VISUAL: first, the clear O(n)-space version — build it, since it mirrors the formula directly.]**

> Let me build the two-array version first, because it's the formula made literal — then we collapse it. Left maxima:

```python
def trap_arrays(height):
    n = len(height)
    if n == 0:
        return 0
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
```

> **[VISUAL: add right sweep + sum.]** Right maxima, then sum the formula.

```python
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    total = 0
    for i in range(n):
        total += min(left_max[i], right_max[i]) - height[i]
    return total
```

> Now the O(1)-space collapse — this is the one to write in the interview.

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    total = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            total += left_max - height[left]      # left side is the bottleneck
            left += 1
        else:
            right_max = max(right_max, height[right])
            total += right_max - height[right]
            right -= 1
    return total
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:40`
*(elaboration — why each line exists)*

**[VISUAL: the two-pointer function; spotlight the `if` and the two updates.]**

> Why this is correct — this is the part interviewers push on.
>
> The `if height[left] < height[right]`: when the left bar is strictly shorter, we commit to the **left** column. First update `left_max` with the current bar, then add `left_max − height[left]`. That's the trapped water here.
>
> **LEARNER:** But we only looked at `left_max` — the running max of what we've *seen* on the left. What if there's a taller wall further right that we skipped? Doesn't that change the answer?
>
> **TEACHER:** This is the exact objection to nail. We're in the branch where `height[left] < height[right]`. So there *is* a wall on the right — at `right`, or something at least that tall behind it — that's taller than our left bar. That guarantees the right side is **not** the limiting one for this column; the left side's `left_max` is the true, final bound. Whatever's further right can only be *taller*, never lower than `height[right]`, so it can't lower our cap. That's why we can finalize now.
>
> `while left < right`, strict: when they meet, every column between them has already been finalized. Each iteration commits exactly one column and moves one pointer — nothing missed, nothing double-counted.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it)*

**[VISUAL: trace table for `[0,1,0,2,1,0,1,3,2,1,2,1]`, first several steps, running total.]**

> Let's run the two-pointer code and watch 6 emerge.

| left(val) | right(val) | branch | update | add | total |
|---|---|---|---|---|---|
| 0 (0) | 11 (1) | `0<1` left | left_max=0 | 0 | 0 |
| 1 (1) | 11 (1) | not `<` right | right_max=1 | 0 | 0 |
| 1 (1) | 10 (2) | `1<2` left | left_max=1 | 0 | 0 |
| 2 (0) | 10 (2) | `0<2` left | left_max=1 | **1** | 1 |
| 3 (2) | 10 (2) | not `<` right | right_max=2 | 0 | 1 |
| 3 (2) | 9 (1) | not `<` right | right_max=2 | **1** | 2 |

> ...and continuing the same way across the remaining bars accumulates the rest, landing on exactly **6**. Every step finalized one column from the running max on its shorter side. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:15`
*(transfer to interview)*

**[VISUAL: four rows — Brute O(n²)/O(1); Prefix arrays O(n)/O(n); Stack O(n)/O(n); Two pointers O(n)/O(1).]**

> Out loud: *"Brute force scans both sides per bar — O(n²). Precomputing leftMax and rightMax gives O(n) time but O(n) space. The two-pointer version keeps only two running maxima, so O(n) time and O(1) space — because the shorter wall is always the binding constraint, I can finalize a column the moment I'm on its lower side."*
>
> That progression — brute, arrays, then the pointer collapse — *is* the answer they want to hear.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:00`
*(depth + honesty)*

**[VISUAL: the two-pointer solution highlighted "O(1)". A note: "monotonic stack — also O(n), but O(n) space".]**

> We already hit the floor: **O(1) extra space** — two indices, two maxima. You can't do better; you must at least read the input.
>
> One honest alternative to name: a **monotonic stack** also solves this in O(n) time, resolving water in horizontal layers as taller bars pop shorter ones off the stack. But it needs O(n) space for the stack. Same time, worse space — so two pointers is the one to write. Mentioning the stack shows range; choosing the pointers shows judgment.

---

## 12. YOUR TURN (active recall) — `12:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Container With Most Water (LC 11)". Two walls, water between.]**

> Before the next video, try **Container With Most Water**. It's the sibling — two pointers, "move the shorter wall" — but instead of *summing* trapped water you *maximize* the area between two walls. Same pointer instinct, different objective. If you get why the shorter wall is safe to move here, you'll get that one fast.
>
> Fifteen minutes, no solutions first.

---

## 13. LOCK IT IN — `12:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Think per-column, not per-puddle** — `min(leftMax, rightMax) − height`.
> 2. **Precompute the walls in two sweeps** for O(n); the arrays are the honest intermediate step.
> 3. **The shorter wall is the bottleneck**, so two pointers collapse the arrays to O(1) space.
>
> The memory peg — *"the water over a bar is capped by the shorter of its two tallest walls, so walk in from the low side."*

---

## 14. CLIFFHANGER — `13:20`
*(open loop to next lesson)*

**[VISUAL: a blurred 2-D grid of heights — Trapping Rain Water II.]**

> Here's what breaks this. Take the elevation map and make it **two-dimensional** — a grid of heights, water pooling in a basin. Now "left wall and right wall" becomes a whole *border* pressing in from every direction, and two pointers can't handle it. You need a heap that always pops the lowest wall on the boundary. That's Trapping Rain Water II — the on-site-hard cousin. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0, total = 0;
    while (left < right) {
        if (height[left] < height[right]) {
            leftMax = Math.max(leftMax, height[left]);
            total += leftMax - height[left];
            left++;
        } else {
            rightMax = Math.max(rightMax, height[right]);
            total += rightMax - height[right];
            right--;
        }
    }
    return total;
}
```
