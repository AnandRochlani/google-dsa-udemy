# 🎬 Recording Script — Longest Increasing Subsequence
**Pattern: Dynamic Programming (+ patience sorting) · LeetCode 300 · Medium · Target length ~14 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the "define the subproblem, then look back" DP recipe from Coin Change / House Robber; binary search from the search lessons.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: the array `10 9 2 5 3 7 101 18`. A wandering highlight tries to pick a rising run, keeps backtracking. A clock ticks.]**

> Find the **longest run of numbers that increases** — but the numbers don't have to be next to each other, you just can't reorder them. In `10, 9, 2, 5, 3, 7, 101, 18`, the answer is 4: `2, 3, 7, 18`.
>
> The natural DP for this is O(n²), and honestly, that passes a lot of interviews. But this exact problem is *famous* for a follow-up that most people can't derive on the spot: an **n-log-n** solution that seems to come out of nowhere. Today you'll build the O(n²) yourself, and then I'll show you the n-log-n trick in a way that finally makes sense — not memorized, understood. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: `nums = [10, 9, 2, 5, 3, 7, 101, 18]`. One line: "Longest strictly increasing subsequence — keep order, may skip elements."]**

> One line: **the longest subsequence whose values strictly increase.** "Subsequence" means keep the original left-to-right order, but you're free to drop elements.
>
> Our example: `[10, 9, 2, 5, 3, 7, 101, 18]`. One winner is `2, 3, 7, 18` — length **4**. (Also `2, 3, 7, 101`.) Notice they're scattered across the array; that scattering is what makes this trickier than the earlier DPs.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — define the subproblem)*

**[VISUAL: index 5 (value 7) glows. A question: "Longest increasing subsequence that ENDS exactly here?"]**

> The tricky part of this problem is even *defining* the subproblem. The answer can end anywhere, so here's the focusing move: ask a narrower question — **"what's the longest increasing subsequence that ends *exactly* at index `i`?"** Call it `dp[i]`.
>
> Why "ends at i"? Because then the choice is clean. To end at `nums[i]`, whatever came right before it in the subsequence is some earlier `nums[j]` that's smaller. So I look at every `j < i` with `nums[j] < nums[i]`, take the best `dp[j]`, and add one for `nums[i]` itself:
>
> **[VISUAL: boxed — `dp[i] = 1 + max( dp[j] )` over all j < i with nums[j] < nums[i]; else dp[i]=1.]**
>
> And since the overall LIS can end anywhere, the final answer is `max(dp)` across all `i`. Let me trace a couple. `dp` for the 2 is 1. For the 5, look back — 2 is smaller, so `dp = 1 + 1 = 2`. For the 7, back at 2, 5, 3 — best is 2, so `dp = 3`.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: for the O(n²) DP, arrows fan back from each i to every earlier j. The arrow-count counter climbs — 1, 3, 6, 10, 15…]**

> **TEACHER:** This DP works, and it's already a huge win over trying all 2ⁿ subsequences. But feel the cost: for each `i`, I scan *every* earlier element looking for the best predecessor. Element 8 scans 7 back, element 7 scans 6 back… that's the arithmetic series — O(n²) comparisons.
>
> **LEARNER:** Honestly O(n²) feels fine? For n up to a couple thousand that's a few million ops. Why would I ever need better?
>
> **TEACHER:** For *this* problem, in a real interview, you often would — the follow-up card literally says "now do it in O(n log n)." And the reason it's a legendary follow-up is that the trick is genuinely non-obvious.
>
> So predict, because this one's hard: **that inner "scan back for the best predecessor" is the bottleneck. What structure lets you *search* instead of *scan*?** You've used it before. Pause.
>
> *(4-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:45`
*(elaboration + analogy — derive the n-log-n)*

**[VISUAL: a card game. Cards dealt one at a time onto piles; a new card goes on the leftmost pile whose top is ≥ it. Title: "Patience."]**

> **TEACHER:** The keyword you were reaching for is **binary search** — and to unlock it, I need a *sorted* thing to search in. Here's the beautiful idea, and it comes from a card game called Patience.
>
> Keep an array called `tails`. `tails[k]` holds the **smallest possible tail value** of any increasing subsequence of length `k+1` we've seen so far. Two facts make it work:
>
> One — `tails` is **always sorted ascending**. A longer subsequence's minimal tail can't be smaller than a shorter one's.
>
> Two — for each new number `x`: binary-search for the leftmost tail that's `≥ x`, and **overwrite it with `x`**. Why overwrite? Because a *smaller* tail for the same length can only help future numbers extend it. If `x` is bigger than every tail, it **extends** the longest run — append it, and the LIS just grew by one.
>
> **[VISUAL: walk `[10,9,2,5,3,7,101,18]`; tails evolves: [10] → [9] → [2] → [2,5] → [2,3] → [2,3,7] → [2,3,7,101] → [2,3,7,18].]**
>
> Watch: 10 → `[10]`. 9 replaces 10 → `[9]`. 2 replaces 9 → `[2]`. 5 is bigger than all, append → `[2,5]`. 3 replaces 5 → `[2,3]`. 7 appends → `[2,3,7]`. 101 appends → `[2,3,7,101]`. 18 replaces 101 → `[2,3,7,18]`.
>
> The **length** of `tails` is the answer: 4. Each step was a binary search — O(log n) — over n numbers. That's O(n log n).

---

## 6. THE KEY MOVE (signaling) — `5:30`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "tails[k] = smallest tail of a length-(k+1) run. Binary-search each number in; append or replace. Answer = len(tails)."]**

> The line: **keep the smallest possible tail for each achievable length; binary-search each new number to either extend the longest run or lower an existing tail.** The number of piles is the LIS length.
>
> One honesty note to say out loud: the `tails` array is *not* itself a valid subsequence in general — only its **length** is guaranteed correct. Claiming otherwise is a classic interview stumble.

---

## 7. CODE IT — LIVE & CHUNKED — `6:15`
*(cognitive load — build both, small pieces)*

**[VISUAL: editor. Type the O(n²) DP first.]**

> Let's write the O(n²) DP first — always have it in your pocket; it's easy and it always works.

```python
def lis_dp(nums):
    n = len(nums)
    dp = [1] * n                     # each element alone is a run of length 1
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

> **[VISUAL: new function; type the n-log-n.]** Now the patience version. Python's `bisect_left` *is* our binary search.

```python
from bisect import bisect_left

def lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)    # leftmost tail >= x
        if i == len(tails):
            tails.append(x)          # x extends the longest run
        else:
            tails[i] = x             # x lowers this length's tail
    return len(tails)
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:45`
*(elaboration — why each line exists)*

**[VISUAL: the patience function; spotlight each line.]**

> The *why* on the n-log-n:
>
> `bisect_left(tails, x)` — finds the leftmost position where a tail is `≥ x`. That's the shortest run whose tail we can improve by swapping in `x`.
>
> `i == len(tails)` → append — `x` beat every tail, so it stretches the longest run by one. This is the *only* line that grows the answer.
>
> `else tails[i] = x` — overwrite. Same LIS length, but now a smaller tail sits there, ready to welcome future numbers.
>
> **LEARNER:** The overwrite bugs me. If I stomp on a tail, don't I destroy some subsequence I'd already built?
>
> **TEACHER:** Feels destructive, but no — `tails[i]` was only ever a *summary*: "the best tail for a run of this length." Lowering it never shortens any run; it just makes that length *easier to extend* later. The runs you actually care about are still implicitly there. We're tracking lengths and best tails, not reconstructing the sequence — that's the mental shift.
>
> **LEARNER:** And strict vs non-strict — `bisect_left` vs `bisect_right`?
>
> **TEACHER:** One-line swap. `bisect_left` gives **strictly** increasing (equal values replace, never extend). Want **non-decreasing**, allowing equals? Use `bisect_right`. Classic follow-up, and now you can answer it in a sentence.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the tails trace table filling row by row.]**

> The full trace, one row per number:

| x | action | tails |
|---|---|---|
| 10 | append | [10] |
| 9 | replace 10 | [9] |
| 2 | replace 9 | [2] |
| 5 | append | [2, 5] |
| 3 | replace 5 | [2, 3] |
| 7 | append | [2, 3, 7] |
| 101 | append | [2, 3, 7, 101] |
| 18 | replace 101 | [2, 3, 7, 18] |

> `len(tails) = 4`. Return **4** — the length we found by hand. (Here `[2,3,7,18]` happens to be a real LIS, but remember: only the length is guaranteed.)

---

## 10. COMPLEXITY, OUT LOUD — `9:45`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(2ⁿ). DP: O(n²). Patience: O(n log n).]**

> To the interviewer: *"Brute force tries all 2ⁿ subsequences. The DP defines dp[i] as the LIS ending at i and scans back — O(n²) time, O(n) space. The patience-sorting version keeps a sorted tails array and binary-searches each element in — O(n log n) time, O(n) space."*
>
> Naming all three, and knowing *when* the follow-up wants the third, is what separates a pass from a strong-hire here.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:30`
*(depth + honesty — the strong beat)*

**[VISUAL: the dp array with max(dp) circled across ALL cells; a note: "answer needs every ending — can't drop to O(1)."]**

> Here's the honest twist on the space beat. Both versions are already O(n) space, and unlike Fibonacci we **can't** shrink to O(1) — the DP answer is `max(dp)` over *all* endings, so every cell can matter, and `tails` genuinely needs room for up to n piles.
>
> So on *this* problem, the interesting optimization isn't space — it's **time**. That's the reframe worth internalizing: the space-optimization instinct is "does my recurrence reach back a fixed window?" Here the answer is *no* — it reaches across everything — so instead of collapsing memory, you attack the runtime with a smarter data structure. Recognizing which lever applies is itself the skill.
>
> Say it out loud: *"Space stays O(n) — I need all endings, or all pile tails — so I optimize time instead, from O(n²) down to O(n log n) with binary search."*

---

## 12. YOUR TURN (active recall) — `11:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Russian Doll Envelopes (LC 354)". Nested envelopes.]**

> Before the next video: **Russian Doll Envelopes.** It's 2-D LIS. Here's the whole plan so you can attempt it: sort envelopes by width ascending — but for ties in width, sort *height descending* — then run plain LIS on the heights. That descending-tie trick stops two equal-width envelopes from nesting. Figure out *why* it works, then code the LIS you just learned on the height array.

---

## 13. LOCK IT IN — `11:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Define the subproblem as "ending at i"** — it makes the look-back recurrence clean. Answer is `max(dp)`.
> 2. **When the bottleneck is "scan back," ask if you can *search* instead** — sorted structure + binary search.
> 3. **`tails[k]` = smallest tail for length k+1;** its length is the LIS. The array itself isn't the subsequence.
>
> Memory peg — *"longest rising run, elements can be skipped"* → **patience piles: each number extends the longest pile or lowers a tail.**

---

## 14. CLIFFHANGER — `12:20`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Partition Equal Subset Sum". Two pans of a scale balancing.]**

> Every DP so far had a 1-D state — one index, one amount. Next, the decision is still just "take it or leave it," but the *state* grows a second dimension: not just *which* items, but *what sum* you're chasing. That's the knapsack, and Partition Equal Subset Sum is the cleanest door into it — with a reverse-loop trick that trips up almost everyone. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// O(n log n) patience sorting with an explicit binary search
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int x : nums) {
        int lo = 0, hi = size;
        while (lo < hi) {                 // leftmost tail >= x
            int mid = (lo + hi) >>> 1;
            if (tails[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = x;
        if (lo == size) size++;
    }
    return size;
}
```
