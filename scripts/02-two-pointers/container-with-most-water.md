# 🎬 Recording Script — Container With Most Water
**Pattern: Two Pointers · LeetCode 11 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** two pointers from both ends — but now the *choice* of which to move is the whole game.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. Two nested `for` loops typed. A LeetCode "Time Limit Exceeded — 10⁵ elements" banner slides in red.]**

> Google on-site. *"These are vertical walls. Pick two, they hold water between them — find the pair that holds the most."*
>
> You write the obvious thing: try every pair of walls, compute the area, keep the biggest. It's right. On a hundred thousand walls it's five *billion* pairs. Time Limit Exceeded.
>
> The fix is two pointers — but here's the twist that trips people up: every single step you have to *decide* which pointer to move, and if you pick wrong you throw away the real answer. By the end of this video you'll know exactly which one to move and *why it's provably safe.* Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, five bars of heights `1  8  6  2  5` drawn as a little skyline.]**

> The whole problem in one line: **two walls plus the floor make a container; the water it holds is the width between them times the shorter wall. Find the maximum.**
>
> Here's our tiny skyline — heights `[1, 8, 6, 2, 5]`. Five bars. The water is capped by the *shorter* of the two walls, because it'd spill over the short one. Hold that fact — it's the entire problem.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the five bars. Two markers i, j jumping through every pair. A "pairs checked" counter ticking up.]**

> Let's do what your brain does first: check every pair.
>
> Bars 0 and 1: width 1, shorter wall is 1, area 1. Bars 0 and 2: width 2, shorter is 1, area 2. Bars 0 and 4: width 4, shorter is *still* 1 — area 4. Ugh, wall 0 is short, it caps everything.
>
> **[VISUAL: markers keep jumping; counter climbs 1, 2, 3… up to 10 pairs for just 5 bars.]**
>
> Five bars gives ten pairs. Now scale it: a hundred thousand bars is five *billion* pairs. And notice — we keep re-discovering that wall 0 is the bottleneck, pair after pair, learning nothing.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight all the pairs involving the short wall 0, all obviously bad. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** Where's the waste? We test every pair even though the answer is capped by the *shorter* wall — and most pairs are hopeless the moment we see they're pinned to a short one.
>
> **LEARNER:** Okay, but to find the *max* area, don't I genuinely have to look at every pair? Any pair could be the winner.
>
> **TEACHER:** That's the instinct to break — because there's structure hiding in "capped by the shorter wall." Pause the video and think: **if I start as wide as possible and I have to give up some width, which of the two walls should I abandon — and which could I never afford to move?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two "hands" — one on the leftmost bar, one on the rightmost. The widest possible container shaded blue.]**

> **TEACHER:** Here's the leap. Start as *wide as possible* — one pointer at each end. That's the maximum width available; every other pair is narrower.
>
> Now the only question: which pointer do I move inward? Moving inward *costs* width, guaranteed. So I only want to move the wall that might *buy* me something back in height.
>
> Think of two people holding a rope taut across a valley to catch rain. The water level can only rise to the *shorter* person's hands. If the taller person crouches, nothing changes — still capped by the short one, and now they're closer together. The *only* move that can help is the short person raising their hands.
>
> **[VISUAL: left bar (height 1) flashes as "the bottleneck". It steps inward; the taller right bar stays put.]**
>
> So the rule falls out: **always move the shorter wall inward.** Moving the taller one can only lose — width drops, the short wall still caps you. Moving the shorter one sacrifices width but is your one shot at a taller cap.
>
> **LEARNER:** But what if I move the short wall and the answer was actually with that short wall paired to something *inside*? Didn't I just throw it away?
>
> **TEACHER:** No — and this is the beautiful part. Any pair using that short wall with a wall still *inside* has the same short cap **and** less width. So it's strictly worse than the area we just measured. We lose nothing.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Start widest · always move the SHORTER wall inward."]**

> Burn this in: **start as wide as possible, and every step move the shorter wall inward.**
>
> Any "best pair where the value depends on the min or max of the two ends" — that's this move. The bottleneck endpoint is the one you advance.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Two pointers at the ends, a running best.

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Loop while they haven't met; measure the area right now.

```python
    while left < right:
        area = (right - left) * min(height[left], height[right])
        best = max(best, area)
```

> **[VISUAL: add chunk 3.]** And the whole decision — move the shorter wall.

```python
        if height[left] < height[right]:
            left += 1          # short wall on the left — its only chance is to move
        else:
            right -= 1         # short (or equal) wall on the right — move it
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `left, right = 0, len(height) - 1` — start at the extremes. Maximum width first, so width only ever shrinks from here — which is exactly why moving the short wall is the only way to possibly gain.
>
> `area = (right - left) * min(...)` — width times the *shorter* wall. The `min` is the whole physics of the problem: water spills over the short side.
>
> `if height[left] < height[right]: left += 1` — move the shorter wall. This is the provably-safe discard.
>
> **LEARNER:** When the two walls are *equal*, your code takes the `else` and moves `right`. Does the tie-break matter?
>
> **TEACHER:** Nice catch — it doesn't. When they're equal, moving *either* one discards a pair capped by that same height with less width, so both choices are safe. Picking one consistently just keeps the code simple.
>
> `while left < right` — strict less-than. Once they meet, width is zero; there's no container left to measure.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: `[1, 8, 6, 2, 5]` skyline with a trace table filling row by row.]**

> Let's run the actual code on our five bars.

| left (h) | right (h) | width | area = w × min | best | move |
|---|---|---|---|---|---|
| 0 (1) | 4 (5) | 4 | 4 × 1 = 4 | 4 | left shorter → left++ |
| 1 (8) | 4 (5) | 3 | 3 × 5 = **15** | 15 | right shorter → right-- |
| 1 (8) | 3 (2) | 2 | 2 × 2 = 4 | 15 | right shorter → right-- |
| 1 (8) | 2 (6) | 1 | 1 × 6 = 6 | 15 | right shorter → right-- → meet |

> Pointers meet. Answer: **15** — the tall wall of height 8 paired with the 5, width 3. The brute force checks all ten pairs and lands on the same 15. We got there in four steps. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²) time / O(1) space. Ours: O(n) time / O(1) space.]**

> Say it to the interviewer: *"Brute force is O(n squared) — every pair. Two pointers is O(n): each step I move one pointer inward, so the two together travel the array once. Space is O(1) — just two indices and a running max."*
>
> One linear sweep replacing all-pairs — that's the strong-hire answer here.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:40`
*(depth + honesty)*

**[VISUAL: both approaches marked O(1) space; a big arrow labeled "the win was TIME" between O(n²) and O(n).]**

> Honesty beat: space was *never* the problem here. Both versions are O(1) — two indices, no growing structure.
>
> Say it out loud: *"Space is O(1) both ways. The entire gain is time — collapsing O(n²) pairs into one O(n) sweep by only ever moving the limiting wall."* Naming that the win was time, not space — and *why* — is the senior signal.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Trapping Rain Water (LC 42)". A blank editor.]**

> Before the next video, try **Trapping Rain Water**. Same two pointers from the ends, same "move the shorter side" instinct — but now instead of one big container, you sum the water trapped above *every* bar. It's the boss-level version of this idea.
>
> Don't peek. Ten minutes of struggle first — that's what moves it from "I saw it" to "I own it."

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Start widest** — a pointer at each end maximizes width up front.
> 2. **Water is capped by the shorter wall** — that's the whole physics.
> 3. **Always move the shorter wall** — it's the only provably-safe discard.
>
> And the memory peg — when the value of a pair depends on the *min* of its two ends, picture two people holding a rope: **only the short one raising their hands can lift the water.**

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Sort Colors".]**

> Two pointers at the ends. Two pointers racing the same way. Next we go up to *three* pointers at once — carving an array into three regions in a single pass, with one sneaky rule about when *not* to advance a pointer. It's the Dutch National Flag, and it's a favorite Google trap. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, best = 0;
    while (left < right) {
        int area = (right - left) * Math.min(height[left], height[right]);
        best = Math.max(best, area);
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return best;
}
```
