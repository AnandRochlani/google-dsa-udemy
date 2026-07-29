# 🎬 Recording Script — Subarray Sum Equals K
**Pattern: Prefix Sum + Hash Map · LeetCode 560 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the sliding-window / two-pointer squeeze from earlier lessons — we'll show exactly where it *breaks*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A tidy sliding-window solution typed out. It runs on `[1,1,1]` and passes green. Then a new test slides in: `[1,-1,0]` — and a red "Wrong Answer" banner drops.]**

> This is a Google favorite: *"Count the subarrays that add up to k."*
>
> You reach for the sliding window — grow the window, shrink it when you overshoot. Clean. It passes the easy test.
>
> Then they slip in **one negative number**… and your window falls apart. Wrong answer.
>
> By the end of this video you'll know *why* the window dies the second negatives show up — and the one hash-map idea that handles them without breaking a sweat. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, three tiles: `1  1  1`, and `k = 2`.]**

> The whole problem in one line: **count how many contiguous chunks of the array add up to exactly k.**
>
> Tiny example — three ones, k is 2. How many runs of neighbors sum to 2?
>
> **[VISUAL: highlight indices 0–1, then 1–2.]**
>
> `[1,1]` at the front — that's 2. `[1,1]` at the back — also 2. So the answer's **2**. Two overlapping windows. Hold that number.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the three tiles. A start marker `i` and end marker `j`. A "sums computed" counter, top-right.]**

> Let's do what your brain does first: try every possible chunk.
>
> Start at index 0. `[1]` is 1. `[1,1]` is 2 — one! `[1,1,1]` is 3. Now start at index 1. `[1]` is 1. `[1,1]` is 2 — two! Then start at index 2. `[1]` is 1.
>
> **[VISUAL: markers sweep every start/end pair, counter ticking 1,2,3,4,5,6.]**
>
> Six subarrays checked for three numbers. That's `n` starts times `n` ends — **O(n squared).** At twenty-thousand numbers, that's hundreds of millions of adds. Slow, and wasteful — watch *how* it's wasteful.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the running sums `1 → 2 → 3` for start 0, then start 1 recomputing `1 → 2` from scratch. A 4-second "🤔 your turn" timer.]**

> Look at the waste: when I restart at index 1, I throw away everything I learned starting at 0 and re-add from zero. I keep recomputing sums I've basically already seen.
>
> Pause the video. Here's the question: **if I keep one running total as I walk the array once — a prefix sum — what could I subtract to instantly know a chunk's sum without re-adding it?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a number line of running totals. As we sweep `[1,1,1]`, a bar labeled "prefix" fills: 0 → 1 → 2 → 3.]**

> Here's the unlock. Keep a **running total** — the prefix sum — as you sweep left to right. After the first 1 it's 1, then 2, then 3.
>
> Now the key algebra. The sum of a chunk from `i+1` to `j` is just **prefix at j minus prefix at i.** Two running totals, subtracted. No re-adding.
>
> **[VISUAL: two markers on the prefix bar; the gap between them lights up = a subarray sum.]**
>
> I want that gap to equal `k`. So `prefix[j] - prefix[i] = k`. Rearrange it — `prefix[i] = prefix[j] - k`.
>
> Read that out loud, because it's the whole video: **standing at j, I want to know how many earlier prefixes equal my current prefix minus k.** Every one of them is a chunk ending right here that sums to k.
>
> **[VISUAL: a hash map appears, filling with prefix→count as we sweep.]**
>
> So I keep a little hash map: every prefix sum I've seen, and how many times. At each step I just ask the map, *"have I seen `current minus k` before, and how often?"* That count is my answer for this position. One pass.

---

## 5b. THE MISCONCEPTION — "why not sliding window?" — `4:15`
*(confront the wrong-but-tempting idea head-on)*

**[VISUAL: split screen. Left: `[1,1,1]` with a happy sliding window. Right: `[1,-1,0]` with the same window overshooting, then a negative yanking it back.]**

> **LEARNER:** Hold on. Counting subarrays with a target sum — that's *textbook* sliding window. Grow the window, and when the sum passes k, shrink from the left. Why are we dragging in a whole hash map?
>
> **TEACHER:** Best question in this lesson — and it's the exact trap. Sliding window only works when growing the window makes the sum move in **one direction.** All-positive array? Add a number, the sum *only* goes up. Overshoot k, shrink from the left, sum *only* comes down. Clean and monotonic.
>
> Now drop in a **negative.** Add an element and the sum can go *down.* Remove one and it can go *up.* "Overshoot, then shrink" is meaningless — because a later negative might pull you right back to k. The window has no reliable direction to shrink.
>
> **[VISUAL: on the right, the window overshoots k, "shrinks," and then a `-1` would've fixed it — a red X over the shrink.]**
>
> **LEARNER:** So the window isn't just harder here — it's straight-up *wrong.*
>
> **TEACHER:** Exactly. With negatives, sliding window is the wrong tool, full stop. Prefix-sum-in-a-map doesn't care about direction — it just counts what it's seen. That's why it survives the negatives.

---

## 6. THE KEY MOVE (signaling) — `5:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Seen a prefix equal to (current − k)? That's a subarray."]**

> Burn this one line in: **have I seen a prefix equal to current-minus-k? If yes — that's a subarray.**
>
> That sentence *is* the algorithm. Everything else is bookkeeping.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First the setup — a counter, a running prefix, and the map.

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1        # the empty prefix — sum 0 has happened once
```

> **[VISUAL: spotlight the `seen[0] = 1` line, a little star next to it.]** That `seen[0] = 1` is the one line everyone forgets. Park it — I'll explain it in the dry-run, and it'll click.
>
> **[VISUAL: add chunk 2, highlight it.]** Now the single pass. Grow the prefix, ask the map, then record.

```python
    for num in nums:
        prefix += num
        count += seen[prefix - k]   # how many earlier prefixes = prefix - k?
        seen[prefix] += 1           # log this prefix for the future
    return count
```

> Three lines in the loop. Add the number. Look up `prefix - k` and add that count. Then log the current prefix. That's it.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `prefix += num` — the running total. This is what lets us never re-add a chunk from scratch.
>
> `count += seen[prefix - k]` — the heart. `prefix - k` is the earlier prefix that would make a chunk ending *here* sum to k. The map tells us how many times we've hit that value — and each one is a separate valid subarray. That's why we count occurrences, not just yes/no.
>
> `seen[prefix] += 1` — log the current prefix so future positions can find it. And notice the **order**: we look up *before* we log. That stops us from pairing a prefix with itself and inventing an empty subarray.
>
> **LEARNER:** And that `seen[0] = 1` at the top — what's it actually for?
>
> **TEACHER:** It represents the empty prefix *before* the array starts. Think about a chunk that begins at index 0 — there's no earlier prefix to subtract. Seeding "sum 0, seen once" is what lets those from-the-very-start subarrays get counted. Without it, you undercount every time the running total lands exactly on k.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: `[1, -1, 0]`, `k = 0` — the negative case that broke the window in the cold open. A trace table fills row by row; the `seen` map shown updating beside it.]**

> Let's run it on the case that killed the sliding window: `[1, -1, 0]`, k is **0**. We said the answer's 3 — let's watch the map earn it.

| num | prefix | need (`prefix−k`) | `seen[need]` | count | `seen` after |
|---|---|---|---|---|---|
| — | 0 | — | — | 0 | `{0:1}` |
| 1 | 1 | 1 | 0 | 0 | `{0:1, 1:1}` |
| −1 | 0 | 0 | 1 | 1 | `{0:2, 1:1}` |
| 0 | 0 | 0 | 2 | 3 | `{0:3, 1:1}` |

> Trace it. After `-1`, prefix is back to 0; we need 0, and we've seen it once — that's the chunk `[1,-1]`. Count is 1.
>
> Then `0`: prefix stays 0, we need 0, and now we've seen it **twice** — so we add 2. That's `[0]` on its own *and* `[1,-1,0]`. Count jumps to 3.
>
> **[VISUAL: the three subarrays highlighted on the tiles: `[1,-1]`, `[0]`, `[1,-1,0]`.]**
>
> Three. Exactly what we promised — with a negative *and* a zero in play. No window gymnastics. The map just counted.

---

## 10. COMPLEXITY, OUT LOUD — `9:10`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²) time, O(1) space. Ours: O(n) time, O(n) space.]**

> Say it the way you'd say it in the room: *"Brute force is O(n squared) — every subarray. With a running prefix sum and a hash map counting prefixes, it's a single pass: O(n) time. Space is O(n) for the map."*
>
> One pass to replace a nested loop. That's the trade, and it's the one they want to hear.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: the map, full of distinct prefixes for an all-positive array — no way to shrink it. A crossed-out "O(1)?" ]**

> Can we drop the map and get to O(1)? **Honest answer: no.** And saying that clearly is itself a strong-hire signal.
>
> In the worst case — think all positives — every prefix sum is different, so the map genuinely holds up to n entries. And because negatives are allowed, *any* earlier prefix might still complete a future subarray, so we can't throw anything away.
>
> Say it out loud: *"I can't beat O(n) space here — negatives mean any past prefix could still matter, so I have to remember all of them."* Naming a limit you can't cross is as sharp as finding a trick.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Subarray Sums Divisible by K (LC 974)". A blank editor.]**

> Before the next video, try **Subarray Sums Divisible by K.** Same prefix-sum-in-a-map skeleton — but instead of counting exact prefixes, you group them by their **remainder mod k.**
>
> Don't peek at the solution. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **A subarray sum is `prefix[j] − prefix[i]`** — so wanting sum k means wanting an earlier prefix of `current − k`.
> 2. **Count prefixes in a hash map, seeded `{0:1}`** — count occurrences, look up before you log.
> 3. **Negatives kill the sliding window** — no monotonic direction to shrink. Prefix-map doesn't care.
>
> And the memory peg — when you see *"count subarrays summing to k"* with negatives in the mix: **seen a prefix equal to (current − k)? That's a subarray.**
>
> One more, for the interview itself — a quick **GCA reminder**: on the Google coding assessment, *say the sliding-window trap out loud before you rule it out.* "I'd normally window this, but negatives break monotonicity, so I'll use a prefix-sum map." That one sentence shows the graders you know *why*, not just *what* — and it's exactly the reasoning they score.

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Contiguous Array — equal 0s and 1s".]**

> The map just counted subarrays that hit an *exact* sum. But what if you don't want to *count* them — what if you need the **longest** subarray with some property, like equal zeros and ones? Same prefix-sum map… but now you store the *first index* you saw each value, not a count. Small twist, big payoff. That's next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int subarraySum(int[] nums, int k) {
    int count = 0, prefix = 0;
    Map<Integer, Integer> seen = new HashMap<>();
    seen.put(0, 1);                              // the empty prefix
    for (int num : nums) {
        prefix += num;
        count += seen.getOrDefault(prefix - k, 0);   // look up before logging
        seen.merge(prefix, 1, Integer::sum);         // log current prefix
    }
    return count;
}
```
