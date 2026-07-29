# 🎬 Recording Script — Maximum Average Subarray I
**Pattern: Sliding Window · LeetCode 643 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the *first* sliding-window lesson. Everything downstream is built on the one move you learn here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A tidy nested loop typed out. A LeetCode "Time Limit Exceeded — 40/50 test cases passed" banner slides in red.]**

> Here's a problem so simple it feels like a warm-up: *"Find the window of `k` numbers in a row with the biggest average."*
>
> You write two loops. Add up each window, keep the best. It's correct. You hit submit… and it dies. Time Limit Exceeded.
>
> The maddening part? Your logic was *right*. It's just doing a mountain of the same addition over and over. By the end of this video you'll delete that inner loop entirely — and you'll meet the single move that powers every sliding-window problem after this one. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, six number tiles: `1  12  -5  -6  50  3`, and a label `k = 4`.]**

> The whole problem in one line: **among all the runs of exactly `k` numbers in a row, return the largest average.**
>
> Here's our tiny example — six numbers, and `k` is 4. So every "window" is four in a row. `[1,12,-5,-6]`, then `[12,-5,-6,50]`, then `[-5,-6,50,3]`. Three windows total.
>
> And here's a freebie that shrinks the whole problem: since `k` is *fixed*, the average is just the sum divided by 4. Same 4 every time. So "biggest average" really means **"biggest sum."** Hold onto that — it's why we can stop thinking about division and just chase the sum.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the six tiles. A bracket sliding across, and an "additions" counter, top-right, starting at 0.]**

> Let's do what your brain does first: for each window, add up its four numbers.
>
> Window one, `[1, 12, -5, -6]`. Add them: `1 + 12 + -5 + -6` — that's four additions. Sum is 2.
>
> **[VISUAL: bracket slides one right; counter ticks 1,2,3,4.]**
>
> Window two, `[12, -5, -6, 50]`. Add again: `12 + -5 + -6 + 50`. Four more additions. Sum is 51.
>
> Window three, `[-5, -6, 50, 3]`. Four more. Sum is 42.
>
> **[VISUAL: counter reads "12 additions" for just 3 windows.]**
>
> Now look closely at windows one and two.
>
> **[VISUAL: highlight `12, -5, -6` — they glow in BOTH brackets.]**
>
> They share *three* of their four numbers — `12, -5, -6`. I just re-added those exact three. And I'll do it again in window three. That re-adding is the waste. Six numbers, twelve additions. Now picture a hundred thousand numbers with `k` in the thousands — that's billions of additions. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The shared `12, -5, -6` pulsing in both brackets. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So here's the exact waste: every time the window slides one step, I throw away the whole sum and rebuild it from scratch — even though only *one* number actually left and only *one* new number arrived.
>
> **LEARNER:** Right, but the sum is a single number — once I've slid, it's gone. Don't I *have* to re-add the four to know the new sum?
>
> **TEACHER:** That's the instinct to break. Pause the video and think: when the window slides from `[1,12,-5,-6]` to `[12,-5,-6,50]`, exactly what changed? One number walked out the left door. One walked in the right. **Can you get the new sum from the old sum using just those two numbers — no re-adding the middle?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the two windows stacked. An arrow shows `1` leaving on the left, `50` entering on the right. The middle three stay put and glow.]**

> Here's the aha, and it comes straight out of what we just saw.
>
> The middle three numbers — `12, -5, -6` — never changed. So their contribution to the sum never changed either. The *only* difference between the old window and the new one is: `1` left, and `50` joined.
>
> So instead of rebuilding, I **patch** the old sum. Take the old sum, 2. Subtract the number that left — the `1`. Add the number that entered — the `50`. `2 - 1 + 50 = 51`.
>
> **[VISUAL: the equation `2 − 1 + 50 = 51` writes itself. The "additions" counter for this step reads "2", not "4".]**
>
> Two operations. Not four. And it doesn't matter if `k` is 4 or 40,000 — it's *always* two operations, because only ever two numbers change.
>
> Think of it like a conveyor belt of exactly `k` items. It rolls one notch: one item drops off the back, one gets added at the front. You don't recount the whole belt — you just adjust for the one that left and the one that arrived. That's a sliding window.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "new sum = old sum − element leaving + element entering."]**

> Burn this one line in: **don't rebuild the window — roll it. New sum equals old sum, minus what leaves, plus what enters.**
>
> That sentence is the entire sliding-window pattern in one breath. Every problem in this section is a variation of *reuse the last window's work instead of recomputing it.*

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First: compute the very first window's sum once, and call it our best so far.

```python
def find_max_average(nums, k):
    window_sum = sum(nums[:k])   # first window — the ONLY full add we do
    best = window_sum
```

> **[VISUAL: add chunk 2, highlight it.]** Now roll the window. `right` is the new element coming in. The one leaving is exactly `k` steps behind it — `nums[right - k]`.

```python
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]  # add new, drop old
        best = max(best, window_sum)
```

> **[VISUAL: add chunk 3.]** And return the best *average* — divide by `k` right at the end, once.

```python
    return best / k
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `sum(nums[:k])` — this is the one and only time we add up a whole window from scratch. Everything after is patching.
>
> `range(k, len(nums))` — we start `right` at index `k`, not 0, because the first `k` elements are already inside the window we just built. `right` is the *first new arrival*.
>
> `nums[right] - nums[right - k]` — this is the whole trick, and it's worth staring at. `nums[right]` is the element entering. `nums[right - k]` is the element leaving — it sits exactly `k` positions back, because the window is always `k` wide. Add one, subtract the other. Two operations, forever.
>
> **LEARNER:** Wait — why `right - k` for the one that leaves, and not `right - k - 1` or something? I always trip on that off-by-one.
>
> **TEACHER:** Fair, and it's the exact spot people slip. When `right` enters, the window becomes `k + 1` wide for an instant — too big. To get back to `k`, we evict the oldest, which is the element `k` slots behind the newest. `right` minus `k`. Count it on the example: `right = 4`, `k = 4`, so we drop index 0 — the `1`. Exactly the number that should leave.
>
> And `best / k` lives at the very end because dividing every step is wasted work — biggest sum *is* biggest average, so we chase the sum and divide once.

---

## 9. DRY-RUN THE CODE — `7:00`
*(worked example — prove it, close the loop)*

**[VISUAL: `[1, 12, -5, -6, 50, 3]`, `k=4`, with a trace table filling row by row.]**

> Let's run the actual code on our six numbers and watch it land.

| step | entering (idx) | leaving (idx) | window_sum | best |
|---|---|---|---|---|
| init | — | — | `1+12-5-6` = 2 | 2 |
| right=4 | 50 (idx 4) | 1 (idx 0) | 2 + 50 − 1 = 51 | 51 |
| right=5 | 3 (idx 5) | 12 (idx 1) | 51 + 3 − 12 = 42 | 51 |

> Best sum is 51. Divide by `k`: `51 / 4 = 12.75`. That's the window `[12, -5, -6, 50]` — exactly the answer. And notice: after the first window, we did *two* operations per step. The loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n·k). Ours: O(n).]**

> **TEACHER:** Say it the way you would to the interviewer: *"Brute force re-sums every window, so it's O(n·k) — and with `k` in the thousands on a hundred-thousand-element array, that times out. But consecutive windows overlap in `k−1` elements, so instead of re-adding I slide: subtract the element leaving, add the element entering. One pass, constant work per step — O(n) time. Space is O(1)."*
>
> That contrast — "they overlap, so I reuse instead of recompute" — is the sentence that earns the checkmark.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:15`
*(depth + honesty)*

**[VISUAL: two scalars glowing — `window_sum`, `best`. A prefix-sum array shown, then crossed out.]**

> Quick, but say it out loud in the room. We hold exactly two numbers — the running sum and the best. Nothing grows with the input. That's O(1) space.
>
> There's a tempting alternative — a **prefix-sum array**, where any window's sum is a subtraction of two precomputed totals. It's also O(n) time — but it costs O(n) *extra* memory for the array. The sliding window gets the same speed for constant space. Naming that trade-off — "prefix sums work, but they cost O(n) memory I don't need here" — is a strong-hire detail.

---

## 12. YOUR TURN (active recall) — `8:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Maximum Sum Subarray of Size K". A blank editor.]**

> Before the next video, try **Maximum Sum Subarray of Size K** — return the biggest *sum* instead of the average. It's the identical machinery with the divide removed, so you're really testing whether the roll — minus what leaves, plus what enters — is in your fingers yet.
>
> Don't peek at a solution. Write the roll from memory. That struggle is what moves this from "I watched it" to "I own it."

---

## 13. LOCK IT IN — `9:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Fixed `k` + a sum or average → fixed-size sliding window.** The tell is the phrase "exactly k" or "of size k."
> 2. **Roll, don't rebuild.** New sum = old sum − leaving + entering. Two operations, always.
> 3. **The one leaving is `k` behind the one entering** — `nums[right - k]`. That's the off-by-one to remember.
>
> And the memory peg — picture a **conveyor belt of `k` items**: one drops off the back, one lands on the front, and you never recount the belt.

---

## 14. CLIFFHANGER — `9:30`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Minimum Size Subarray Sum".]**

> This window never changed size — always exactly `k`. But what if the problem doesn't *tell* you the size? What if it says "the *shortest* run of numbers that sums to at least 7" — and you have to *discover* how wide the window should be? Now the window has to breathe: grow when it's too small, shrink when it's too big. That's the next one — the *dynamic* window. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public double findMaxAverage(int[] nums, int k) {
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += nums[i];  // first window, once
    int best = windowSum;
    for (int right = k; right < nums.length; right++) {
        windowSum += nums[right] - nums[right - k];    // add new, drop old
        best = Math.max(best, windowSum);
    }
    return (double) best / k;
}
```
