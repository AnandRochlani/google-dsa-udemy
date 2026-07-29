# 🎬 Recording Script — Minimum Size Subarray Sum
**Pattern: Sliding Window (dynamic) · LeetCode 209 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the fixed-size "roll the window" move from Maximum Average Subarray (LC 643, previous lesson). This time the window *changes size*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. Two nested loops. A LeetCode "Time Limit Exceeded — test 61/62" banner slides in red.]**

> Google phone screen: *"Find the **shortest** run of numbers that adds up to at least the target."*
>
> Last lesson our window was always the same size — `k`. Easy. But here nobody tells you the size. The answer might be 2 numbers long. Might be 200. So your brain reaches for the brute force: try every start, extend until you hit the target. It works on the example. You submit… Time Limit Exceeded.
>
> By the end of this video you'll have a window that *breathes* — it grows when it's starving, shrinks when it's bloated — and it finds the answer in a single pass. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, six tiles: `2  3  1  2  4  3`, and a label `target = 7`.]**

> The whole problem in one line: **return the length of the shortest run of consecutive numbers whose sum is at least the target.** If nothing reaches it, return 0.
>
> Tiny example — six numbers, target 7. Look for the shortest stretch summing to 7 or more.
>
> One quiet detail that matters enormously: **every number is positive.** No zeros, no negatives. Hold that thought — it's the property that makes the whole trick legal, and I'll show you exactly where.
>
> The answer here is 2, from `[4, 3]`. Don't hunt for it — just hold that the best is length 2.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: the six tiles. A start-marker, a running sum, and an "adds" counter top-right.]**

> Let's do what your brain does first: from every start, extend right until the sum reaches 7.
>
> Start at index 0. `2` → 2. `2+3` → 5. `2+3+1` → 6. `2+3+1+2` → 8. Got it — length 4.
>
> **[VISUAL: marker jumps to index 1; the sum resets to 0.]**
>
> Now start at index 1. `3` → 3. `3+1` → 4. `3+1+2` → 6. `3+1+2+4` → 10. Length 4 again.
>
> **[VISUAL: highlight `3, 1, 2` — they glow: they were just summed in the PREVIOUS pass too.]**
>
> Stop right there. I just re-added `3, 1, 2` — I summed those exact numbers *one pass ago* as part of start-0. And I'll re-add overlapping stretches for start 2, start 3… every single restart throws away work I already did.
>
> **[VISUAL: counter climbing fast.]**
>
> Six numbers and the adds are piling up. At a hundred thousand numbers that's `O(n²)` — billions of operations. Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The overlapping `3,1,2` pulsing across two passes. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste named plainly: every time I pick a new start, I nuke the sum and rebuild it, re-adding numbers I *just* looked at.
>
> **LEARNER:** But the window size isn't fixed anymore. Last time I could roll a fixed `k`. Here I don't even know how wide the answer is — how can I reuse anything when the width keeps changing?
>
> **TEACHER:** That's exactly the knot to untie. So pause and think: instead of two *pointers restarting*, what if I had a `left` and a `right` that both only *move forward* — `right` to add numbers, `left` to remove them — so no number is ever visited twice? **When would I grow the window, and when would I shrink it?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a single window with two edges, `left` and `right`, over the tiles. A sum readout above it.]**

> Here's the leap. Keep **one** window with two edges. And give it two instincts:
>
> **Too small? Grow.** If the window's sum is under the target, it's starving — push `right` forward and swallow the next number.
>
> **Big enough? Shrink.** The moment the sum hits the target, the window is *valid* — record its length. But maybe it's fatter than it needs to be. So pull `left` inward, dropping numbers from the back, as long as the sum *stays* at or above target — recording the length each time it's still valid. A shorter valid window is strictly better.
>
> **[VISUAL: window inflates rightward to 8, then deflates from the left, sum readout updating live.]**
>
> Think of it like an **accordion**. Squeeze air in from the right until it plays the note. Then press it closed from the left, as tight as you can, while the note still sounds.
>
> **LEARNER:** Hang on — when I shrink, how do I know a number I dropped wasn't the one holding the note? What if removing it was a mistake?
>
> **TEACHER:** *This* is where "all positive" pays off. Every number is positive, so **adding always grows the sum and removing always shrinks it** — no surprises. When I drop a number and the sum falls below target, I know for certain the window is now too small, so I stop shrinking and go back to growing. Nothing I removed was secretly propping up a bigger sum. Negatives would break that guarantee — and you'd need a totally different tool. Positivity is the permission slip for the accordion.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Grow right to become valid → shrink left while it stays valid → record the shortest."]**

> Burn this in: **grow `right` until the window is valid, then shrink `left` while it stays valid — recording the shortest each time.**
>
> That grow-then-shrink shape is the *dynamic* sliding window. Every "shortest / longest window satisfying a condition" problem is a remix of this one move.

---

## 7. CODE IT — LIVE & CHUNKED — `5:25`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Set up `left`, a running sum, and the best length as infinity — so any real window beats it.

```python
def min_subarray_len(target, nums):
    left = 0
    window_sum = 0
    best = float("inf")
```

> **[VISUAL: add chunk 2, highlight it.]** Grow: march `right` across the array, adding each new element.

```python
    for right in range(len(nums)):
        window_sum += nums[right]           # grow: swallow the new element
```

> **[VISUAL: add chunk 3 — the shrink loop.]** Now the accordion squeeze. While the window is valid, record its length and drop from the left.

```python
        while window_sum >= target:         # while still valid...
            best = min(best, right - left + 1)
            window_sum -= nums[left]        # drop the leftmost
            left += 1
```

> **[VISUAL: add chunk 4.]** And translate "never found one" back to 0.

```python
    return best if best != float("inf") else 0
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*.
>
> `best = float("inf")` — infinity is a placeholder that any real length beats, so the first valid window becomes the record with no special-casing. And if it stays infinity, we never found one → return 0.
>
> The `for` adds one element per step — that's the grow.
>
> The `while` is the star. Notice it's a `while`, not an `if` — because one growth step might let us shrink *several* times. We keep squeezing and recording until the window would go invalid.
>
> **LEARNER:** That `while` inside the `for` — isn't that a nested loop? That's O(n²) again, the exact thing we were running from.
>
> **TEACHER:** Best question in the lesson. It *looks* quadratic, but count the pointer moves instead of the loop nesting. `right` advances `n` times, total. `left` also advances at most `n` times, total — it can never pass `right` or go backward. So across the *entire* run, the two pointers take at most `2n` steps combined. Every element is added exactly once and removed at most once. That's O(n), amortized. The nested shape hides a linear reality.
>
> `right - left + 1` — that's the current window's length; `+1` because both ends are inclusive.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: `[2,3,1,2,4,3]`, target 7, trace table filling row by row.]**

> Let's run the code on our six numbers.

| right (val) | sum after add | shrink? | window recorded | best |
|---|---|---|---|---|
| 0 (2) | 2 | no | — | ∞ |
| 1 (3) | 5 | no | — | ∞ |
| 2 (1) | 6 | no | — | ∞ |
| 3 (2) | 8 | yes → drop 2, sum 6 | `[2,3,1,2]` len 4 | 4 |
| 4 (4) | 6+4 = 10 | yes → drop 3 (7), drop 1 (6) | `[3,1,2,4]` len 4, then `[1,2,4]` len 3 | 3 |
| 5 (3) | 6+3 = 9 | yes → drop 2 (7), drop 4 (3) | `[2,4,3]` len 3, then `[4,3]` len 2 | **2** |

> Answer: 2 — the window `[4, 3]`. Exactly what we said was hiding at the start. Loop closed. Watch how at `right=4` and `right=5` the `while` fired *twice* in one step — that's the accordion squeezing as tight as it can.

---

## 10. COMPLEXITY, OUT LOUD — `9:25`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²). Ours: O(n). A note: "left + right each move ≤ n".]**

> **TEACHER:** Say it to the interviewer: *"Brute force restarts the sum from every index — O(n²), times out at 10⁵. Instead I use one dynamic window: grow `right` to add, shrink `left` while the sum still clears the target, tracking the shortest. It looks nested, but each pointer only moves forward at most n times, so it's O(n) time, O(1) space."*
>
> Then land the insight that proves you understand it: *"This is safe **because all values are positive** — adding only grows the sum, removing only shrinks it, so the shrink can't overshoot."* That one sentence separates memorizers from understanders.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:00`
*(depth + honesty)*

**[VISUAL: three scalars — `left`, `window_sum`, `best`. A prefix-sum + binary-search version shown, then crossed out.]**

> We hold three numbers — `left`, the running sum, the best. Nothing scales with input. O(1) space.
>
> The honest alternative: **prefix sums plus binary search** solves it in O(n log n) time but needs an O(n) prefix array. Slower *and* heavier. So the window wins on both counts here — *unless* the array had negatives, which would break the monotonic shrink and force you back to prefix sums. Saying "prefix sums are the fallback the moment negatives appear" shows you know *why* your solution works, not just that it does.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Longest Substring Without Repeating Characters (LC 3)". A blank editor.]**

> Before the next video, try **Longest Substring Without Repeating Characters**. Same dynamic window — but flipped. Here we shrank when the window got *big enough*; there you'll shrink when the window becomes *invalid* (a duplicate appears), and you're chasing the **longest**, not the shortest.
>
> Write the grow-then-shrink skeleton from memory first. That effortful recall is what locks the pattern in.

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **"Shortest/longest window satisfying a condition" → dynamic window.** Two pointers, both moving forward only.
> 2. **Grow `right` to fix "too small"; shrink `left` to fix "too big / too long."** Record on the valid side.
> 3. **The shrink is only safe because values are positive** — monotonic sum. Negatives break it; reach for prefix sums.
>
> Memory peg: the window is an **accordion** — pump air in from the right until it sounds the note, then squeeze it shut from the left while the note still plays.

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Longest Substring Without Repeating Characters".]**

> We just shrank a window to make it *smaller*. Next up we flip the goal: keep the window as *large* as possible, and only shrink when it breaks a rule — the first duplicate character. Same two pointers, opposite instinct, and a hash map joins the party to remember what we've seen. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int minSubArrayLen(int target, int[] nums) {
    int left = 0, windowSum = 0, best = Integer.MAX_VALUE;
    for (int right = 0; right < nums.length; right++) {
        windowSum += nums[right];              // grow
        while (windowSum >= target) {          // shrink while valid
            best = Math.min(best, right - left + 1);
            windowSum -= nums[left];
            left++;
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}
```
