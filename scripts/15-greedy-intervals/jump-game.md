# 🎬 Recording Script — Jump Game
**Pattern: Greedy & Intervals · LeetCode 55 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the greedy mindset from the interval lessons — commit to a locally-best move, prove it stays globally right.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a row of stepping stones over water, each stone labeled with a number. A stick figure at the far left eyeing the far right. One stone in the middle reads "0" and glows ominously.]**

> You're on the first of a row of stones. Each stone has a number — the *maximum* you can jump from it. Can you make it to the last stone?
>
> The trap answer is to try every possible sequence of jumps — and that explodes into exponential paths. Even the "smart" dynamic-programming fix is O(n²).
>
> But here's the thing: you don't care *which* path you take. You only care *can you get there*. And that one shift collapses the whole problem into a single number and one pass. By the end of this video, O(n) time, O(1) space, and you'll know exactly why it's airtight. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, five tiles: `[2, 3, 1, 1, 4]` with indices 0–4 underneath. A second row shows the counter-example `[3, 2, 1, 0, 4]`.]**

> One line: **starting at index 0, where each value is your max jump length, can you reach the last index?**
>
> Example one: `[2, 3, 1, 1, 4]`. From index 0 you can jump up to 2. Jump 1 step to index 1, which lets you jump up to 3 — enough to land on index 4, the end. **True.**
>
> Counter-example: `[3, 2, 1, 0, 4]`. No matter what, you get stuck on that index-3 stone with a `0` — it traps you. Index 4 is unreachable. **False.** Hold both.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: a branching tree from index 0 — every jump length forks a new branch. Branches re-explore the same indices; a "revisits" counter climbs.]**

> Brute force: from index 0, try every jump — 1 step, or 2 steps — and recurse from each landing, asking "can I reach the end from here?"
>
> **[VISUAL: the tree fanning out, many branches landing on the same index 2, re-exploring it.]**
>
> It's correct. But look — different paths keep landing on the *same* index and re-exploring everything past it. Even if you memoize to kill the repeats, each index still tries up to its full jump range, so you're at O(n²). And worse: you're carefully tracking *paths* when the question never asked about paths.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze the tree. Highlight that all we ever asked was "reachable?" not "which route?". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste: we're memorizing routes. But the problem only asks *reachable or not* — the exact sequence of hops is irrelevant.
>
> **LEARNER:** Sure, but to know if the end is reachable, don't I still need to know which stones I can actually stand on? That feels like tracking paths again.
>
> **TEACHER:** Almost — but here's the crack. You don't need the *set* of reachable stones, just the *frontier*. Pause and predict: **if you sweep left to right, what single number would tell you everything you need — the farthest index you could possibly have reached so far?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the array `[2,3,1,1,4]` with a horizontal "reach" bar that extends rightward as the sweep advances. A vertical cursor `i` moves across.]**

> Here's the aha — think of it like the range of a flashlight beam. Sweep left to right holding one number, `furthest` — the farthest index you can reach using everything seen so far.
>
> At each index `i`:
> - **If `i` is beyond `furthest`, you're stuck.** No earlier stone could launch you this far, so there's an unbridgeable gap — the end is unreachable. Return false.
> - **Otherwise `i` is reachable,** so from here you might extend your range: `furthest = max(furthest, i + nums[i])`.
> - The moment `furthest` covers the last index, you're done — return true.
>
> **[VISUAL: `[2,3,1,1,4]`. i=0: furthest = 0+2 = 2. i=1: 1 ≤ 2 ok, furthest = max(2, 1+3) = 4 ≥ last → true!]**
>
> And why is one number enough? Because reachability is **downward-closed** — if you can reach index `k`, you can reach every index below `k` too, just by jumping shorter. So the reachable stones are always an unbroken prefix, and `furthest` marks its right edge. No set, no paths — one scalar captures all of it.

---

## 5b. WHY THE GREEDY IS SAFE — `4:10`
*(confronting the "how do we KNOW" head-on)*

**[VISUAL: a filled bar from 0 to `furthest`, solid green — "every index in here is genuinely reachable".]**

> That downward-closed property is the whole safety proof, so let's make it explicit — because the natural worry with any greedy is *how do we KNOW we're not skipping a better move?*
>
> Here we never skip anything. The invariant is: **at every step, `furthest` equals the largest index reachable using indices we've already passed.** Every index `i ≤ furthest` is *provably* reachable, so it's always valid to stand on it and extend from it. And the instant `i > furthest`, there is *no* stone in `[0..furthest]` that can jump across the gap — by definition, `furthest` was the best any of them could do. So false is certain, not a guess. That's why the single rolling max is airtight.

---

## 6. THE KEY MOVE (signaling) — `4:55`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Track the furthest reachable index; if `i` ever passes it, you're stuck."]**

> The key move: **sweep once, keep the furthest reachable index; if your cursor ever gets ahead of it, the end is unreachable.**
>
> Trigger phrase: *"can I reach / how far can I get, with per-step ranges"* → greedy furthest-reach. One rolling max beats a whole DP array.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> One variable — the furthest we can reach — starts at 0.

```python
def canJump(nums):
    furthest = 0
```

> **[VISUAL: add chunk 2, highlight.]** Sweep. If the current index is past our reach, we're stuck.

```python
    for i, jump in enumerate(nums):
        if i > furthest:              # unreachable — gap we can't cross
            return False
```

> **[VISUAL: add chunk 3.]** Otherwise extend the reach, and short-circuit the moment we cover the end.

```python
        furthest = max(furthest, i + jump)
        if furthest >= len(nums) - 1: # end is already reachable
            return True
    return True
```

> That's the entire algorithm — one loop, one number.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:35`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why each piece.
>
> `if i > furthest: return False` — this is the trap detector. If the cursor has walked past everything we can reach, there's a `0`-stone or a gap behind us that we can never clear.
>
> `furthest = max(furthest, i + jump)` — from index `i` we can reach `i + jump`. The `max` keeps the best reach we've ever had — a later stone with a small number shouldn't *shrink* our frontier.
>
> **LEARNER:** Why the `max`? If I'm moving forward, isn't `i + jump` always bigger than the old furthest anyway?
>
> **TEACHER:** No — and that's the bug people ship. Take `[5, 1, 1, 1, 1]`. At i=0, furthest jumps to 5. At i=1, `i + jump` is just `1 + 1 = 2`, which is *smaller* than 5. Without the `max`, you'd throw away the reach the big first jump gave you. The `max` says: a weak stone never costs you range you already earned.
>
> And the early `return True` — the instant `furthest` reaches the last index, nothing later matters. Cheap short-circuit.

---

## 9. DRY-RUN THE CODE — `7:40`
*(worked example — prove it, close the loop)*

**[VISUAL: both examples, trace tables side by side.]**

> Run the true case `[2,3,1,1,4]`:

| i | nums[i] | `i > furthest`? | furthest after = max(prev, i+nums[i]) |
|---|---|---|---|
| 0 | 2 | 0 > 0 ❌ | max(0, 2) = 2 |
| 1 | 3 | 1 > 2 ❌ | max(2, 4) = 4 ≥ 4 → **return True** ✅ |

> Now the false case `[3,2,1,0,4]`:

| i | nums[i] | `i > furthest`? | furthest after |
|---|---|---|---|
| 0 | 3 | 0 > 0 ❌ | max(0, 3) = 3 |
| 1 | 2 | 1 > 3 ❌ | max(3, 3) = 3 |
| 2 | 1 | 2 > 3 ❌ | max(3, 3) = 3 |
| 3 | 0 | 3 > 3 ❌ | max(3, 3) = 3 |
| 4 | 4 | 4 > 3 ✅ | **return False** ✅ |

> The `0` at index 3 froze `furthest` at 3, and index 4 fell past it. Exactly the trap we saw. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:35`
*(transfer to interview)*

**[VISUAL: rows — Memoized DP: O(n²) time, O(n) space. Greedy: O(n) time, O(1) space.]**

> Say it: *"The memoized recursion is O(n²) time and O(n) space because each index scans its whole jump range. The greedy sweep touches each index once and holds a single integer — O(n) time, O(1) space."*
>
> Naming that you collapsed an O(n²) DP into a linear scan is the headline.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:10`
*(depth + honesty)*

**[VISUAL: a full DP boolean array crossed out; replaced by one integer `furthest`.]**

> This whole solution *is* the space optimization. The DP version keeps an O(n) boolean array "is index i reachable." We deleted it.
>
> Say it out loud: *"I don't need a reachability array — reachability is monotone and downward-closed, so one rolling max captures the entire reachable prefix. That's O(1) space."* Naming *why* the array is unnecessary is the insight interviewers reward.

---

## 12. YOUR TURN (active recall) — `9:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Jump Game II (LC 45)". Same stones, now with a jump-counter.]**

> Before the next video, try **Jump Game II**: same array, but now find the *minimum number of jumps* to reach the end (assume you always can). The greedy shifts subtly — you track the reach of your *current* jump and only "spend" a jump when you run out of it. See if you can extend today's furthest-reach idea.
>
> Ten minutes of real struggle first.

---

## 13. LOCK IT IN — `10:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **The path doesn't matter** — only reachability, and it's downward-closed.
> 2. **One rolling max, `furthest`** — replaces the whole DP array.
> 3. **Stuck the instant `i > furthest`** — that's an uncrossable gap.
>
> Memory peg: **track how far you can reach; the moment you fall behind your own reach, you're done.**

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Implement Trie" — a tree of letters branching out.]**

> That's the greedy-and-intervals chapter. Next we switch gears entirely — from numbers on a line to *words* in a dictionary. How do you store thousands of words so that checking any prefix is instant, no matter how many words you have? The answer is a tree made of letters. Next chapter: the Trie. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean canJump(int[] nums) {
    int furthest = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > furthest) return false;           // unreachable index
        furthest = Math.max(furthest, i + nums[i]);
        if (furthest >= nums.length - 1) return true;
    }
    return true;
}
```
