# 🎬 Recording Script — Binary Search (The Canonical Template)
**Pattern: Modified Binary Search · LeetCode 704 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the template every other lesson in this section reuses. Learn it cold.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A one-line `for` loop scanning an array. A LeetCode note pulses red: "Expected: O(log n). Your solution: O(n)."]**

> Here's a problem so basic it feels like a freebie: find a number in a sorted array. You write a five-line loop, it returns the right index, all tests green.
>
> And the interviewer says: "That's O(n). I asked for O(log n." Silence.
>
> The array was *sorted* and you scanned it like a phone book you read cover to cover. By the end of this video you'll have one template — the same nine lines you'll reuse in every problem this section — that turns "look at everything" into "throw away half, every single step." Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, six index-labeled tiles: `-1 0 3 5 9 12` with indices `0..5`. `target = 9` in a box.]**

> The whole problem in one line: **the array is sorted, find the index of `target`, or return −1.**
>
> Tiny example — six numbers, already in order. We want `9`. It's sitting at index `4`. Easy for your eyes. The question is how a machine finds it *without* looking at all six.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the six tiles. A single marker walks left to right, one tile at a time. A "looks" counter ticks: 1, 2, 3, 4, 5.]**

> Let's do what your brain does first. Start at the left. `-1`? No. `0`? No. `3`? No. `5`? No. `9`? Yes — index 4. Five looks.
>
> Now feel the waste: after we checked `-1` and it wasn't `9`, we learned *one* thing — index 0 is out. One element ruled out per look.
>
> **[VISUAL: counter morphs to "10,000 looks" over a giant array bar.]**
>
> With ten thousand elements, that's up to ten thousand looks. And we completely ignored the biggest gift on screen: **the array is sorted.**

---

## 4. THE PAIN POINT + PREDICT — `2:00`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the sorted tiles. A finger points at the middle tile `5`. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Each look kills exactly one candidate. On sorted data that's a crime. Pause the video and predict: **if I only get to peek at the middle element `5`, and my target is `9` — what does that one peek tell me about the *left half* of the array?**
>
> **LEARNER:** Well… `9` is bigger than `5`, and everything left of `5` is even smaller than `5`… so `9` can't be anywhere on the left. All of it's gone.
>
> **TEACHER:** Exactly. One peek just deleted half the array. That's the whole idea.

---

## 5. BUILD THE INTUITION (the aha) — `2:45`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: sorted tiles with three markers: `lo` at index 0, `hi` at index 5, `mid` at index 2 (value 3). Then the left half `[-1, 0, 3]` greys out and slides off.]**

> Think of a paper dictionary. You don't read from "aardvark" to find "monsoon" — you flop it open in the middle, see you're too early, and ignore the entire first half. Then repeat in what's left.
>
> That's binary search. Three markers: **`lo`** at the far left, **`hi`** at the far right, **`mid`** in between. Look at `nums[mid]`. Because it's sorted, comparing it to `target` tells you which *half* the answer lives in — and you throw the other half away.
>
> **[VISUAL: mid=2 → value 3 < 9, so tiles 0–2 grey out. New window is `[5, 9, 12]`, lo jumps to index 3.]**
>
> `mid` is `3`, target is `9`, `3 < 9` — so the answer's in the right half. `lo` jumps to just past `mid`. The live window is now three tiles. Peek again, halve again. `n → n/2 → n/4 →` … you reach one element in **log₂ n** steps. Ten thousand elements? Fourteen peeks. Not ten thousand.

---

## 6. THE KEY MOVE (signaling) — `3:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Sorted + monotonic → peek the middle, discard the half that can't hold the answer."]**

> Burn this in: **when the search space is monotonic, one peek at the middle lets you throw away half.** "Monotonic" just means: as you move right, the truth only changes one way — here, values only go up. That consistency is what makes a peek trustworthy. Every problem in this section is a variation on this one move.

---

## 7. CODE IT — LIVE & CHUNKED — `4:05`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build the template you'll memorize. First the bounds — and read the comment, it's the whole secret.

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1      # INCLUSIVE window: answer is somewhere in [lo, hi]
```

> **[VISUAL: add chunk 2, highlight it.]** Now the loop condition, and the overflow-safe midpoint.

```python
    while lo <= hi:                # <= : a window of one element is still worth checking
        mid = lo + (hi - lo) // 2  # same as (lo+hi)//2 but can't overflow
```

> **[VISUAL: add chunk 3 — the three-way decision.]** Peek, then discard a half.

```python
        if nums[mid] == target:
            return mid             # found it
        elif nums[mid] < target:
            lo = mid + 1           # target is strictly RIGHT → drop left half + mid
        else:
            hi = mid - 1           # target is strictly LEFT → drop right half + mid
    return -1                      # window emptied → not here
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:10`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line as it's named. A side box lists "3 rules."]**

> Three rules make this bug-proof — and binary search is *all* about the off-by-ones, so listen.
>
> Rule one: **inclusive bounds.** Every index inside `[lo, hi]` is still a live suspect. `hi` starts at `len - 1`, a real index, not `len`.
>
> Rule two: `lo <= hi`, not `<`. When `lo` equals `hi` the window is exactly one element — still a candidate, still check it.
>
> Rule three: always move *past* `mid` — `mid + 1` or `mid - 1`. You just checked `mid`; excluding it is what makes the window **strictly shrink** every loop.
>
> **LEARNER:** Hold on — why `mid + 1`? Why not just set `lo = mid`? It feels safer to keep it.
>
> **TEACHER:** That "safer" instinct is the classic infinite loop. Picture `lo = 3, hi = 4`. `mid` floors to `3`. If `nums[3] < target` and you write `lo = mid`, `lo` stays `3` forever — the window never shrinks, the loop spins. `mid + 1` guarantees progress. We already checked `mid`, so skipping it costs nothing and saves you from the hang.

---

## 9. DRY-RUN THE CODE — `6:15`
*(worked example — prove it, close the loop)*

**[VISUAL: `[-1, 0, 3, 5, 9, 12]`, target 9. Trace table fills row by row; the discarded half greys each step.]**

> Let's run the real code on our six numbers, target `9`.

| lo | hi | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 3 | 3 < 9 → lo = 3 (drop left half) |
| 3 | 5 | 4 | 9 | 9 == 9 → **return 4** ✅ |

> Two peeks. Now the not-found case, target `2`:

| lo | hi | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 3 | 3 > 2 → hi = 1 |
| 0 | 1 | 0 | −1 | −1 < 2 → lo = 1 |
| 1 | 1 | 1 | 0 | 0 < 2 → lo = 2 |
| — | — | — | lo(2) > hi(1) | **return −1** ✅ |

> When `lo` crosses past `hi`, the window is empty — it was never here. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:00`
*(transfer to interview)*

**[VISUAL: two rows — Linear scan: O(n). Binary search: O(log n). A tiny "14 vs 10,000" callout.]**

> Say it the way you'd say it in the room: *"A linear scan is O(n). But the array's sorted, so I binary-search — each comparison halves the remaining space, that's O(log n) time and O(1) space with the iterative form."* Log n of ten thousand is fourteen. That gap is the entire point of the problem.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:35`
*(depth + honesty)*

**[VISUAL: iterative version (two int vars) beside a recursive version with a stack of call frames growing.]**

> Already optimal on space — two integers, O(1). Naming the *absence* of a trick is a skill, so add this: you *could* write it recursively, but each recursive call parks a frame on the stack, costing O(log n) memory for the same time. The iterative template is strictly cheaper. Say that out loud — it shows you thought about it.

---

## 12. YOUR TURN (active recall) — `8:05`
*(retrieval practice)*

**[VISUAL: "Your turn → Search Insert Position (LC 35)". A blank editor.]**

> Before the next video, try **Search Insert Position**. Same template — but when the target isn't there, return where it *would* go. One tiny tweak to what you return. Struggle with it for ten minutes before peeking; that struggle is what welds the template into muscle memory.

---

## 13. LOCK IT IN — `8:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Inclusive `[lo, hi]`, `while lo <= hi`, move past mid.** That trio kills the off-by-ones.
> 2. **One peek deletes half** — only because the space is monotonic (sorted).
> 3. **Iterative beats recursive** on space: O(1) vs O(log n) stack.
>
> The memory peg — when you see **"sorted"** or **"O(log n) required,"** your hand should already be typing `lo, hi = 0, len - 1`. **Peek the middle, burn a half.**

---

## 14. CLIFFHANGER — `9:05`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Search in Rotated Sorted Array" — the sorted array bar visibly snapped and swapped: `[4,5,6,7,0,1,2]`.]**

> This template lives or dies on one assumption: the array is sorted, so `nums[mid]` tells you which half to keep. But what if someone takes that sorted array and *rotates* it — cuts it and swaps the pieces? Now peeking at the middle lies to you. Do we give up on binary search? No — we get sneakier. That's next.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;      // overflow-safe midpoint
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) lo = mid + 1;   // drop left half + mid
        else hi = mid - 1;                            // drop right half + mid
    }
    return -1;
}
```
