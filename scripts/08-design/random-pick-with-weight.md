# 🎬 Recording Script — Random Pick with Weight

**Pattern: Prefix sum + binary search · LeetCode 528 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** binary search on a sorted array — now *we* build the sorted array ourselves.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an interview whiteboard. "w = [1, 3] → return index 1 three times as often as index 0." A candidate writes `bag = [0, 1, 1, 1]` — the interviewer calmly adds one line: "w[0] = 100,000,000". The bag visual explodes off the screen, memory meter goes red.]**

> Google phone screen. The interviewer says: *"Here's an array of weights. Give me a `pickIndex` that returns index `i` with probability proportional to `w[i]`."*
>
> And you see it instantly — make a bag! One copy of index 0, three copies of index 1, pick uniformly. It works. You're feeling great.
>
> Then the interviewer says: *"One of the weights is a hundred million."* And your bag just tried to allocate a hundred million integers… for **one** index.
>
> The real solution needs zero extra copies of anything — it's a **dart thrown at a number line**, and it lands in `O(log n)`. By the end of this video you'll own that trick, plus the sneaky off-by-one inside it that quietly skews the probabilities if you get it wrong. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below it, `w = [1, 3]` with two calls: pickIndex() → 0 (25%), pickIndex() → 1 (75%).]**

> One line: **build a class whose `pickIndex()` returns index `i` with probability `w[i]` divided by the sum of all weights.**
>
> Tiny example — just two weights: `w = [1, 3]`. Total weight is 4. Index 0 owns 1 of it, index 1 owns 3. So `pickIndex()` should return 0 about **25%** of the time and 1 about **75%** of the time. Not exactly alternating, not uniform — *proportional*.
>
> And here's the constraint that matters: the array can be ten thousand long, and `pickIndex` gets called ten thousand times. So we can afford one honest pass to *build* something — but every *pick* after that has to be fast. Build once, query many. That gap is the entire design signal.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: `w = [1, 3]` on top. Below, the bag being filled slot by slot: `[0, 1, 1, 1]`. A "memory slots" counter ticks 1… 2… 3… 4.]**

> Let's do what your brain does first: the bag. For every index, drop `w[i]` copies of it into a list. One `0`, three `1`s — the bag is `[0, 1, 1, 1]`. Now pick a uniform random slot. Four slots, three of them say `1` — so index 1 comes back 75% of the time. Correct, dead simple, and honestly a fine first thing to *say out loud*.
>
> **[VISUAL: `w = [1, 3]` morphs into `w = [1000000, 3000000]`. The bag starts filling… and filling… counter spins to 4,000,000, screen scrolls helplessly.]**
>
> Now watch it break. Same two indices — but weights of a million and three million. The bag needs **four million slots** to represent **two numbers**.
>
> We're paying for the *magnitude* of the weights, not the *count* of them. Two indices should cost two of something — not four million.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the bloated bag. The three `1`-slots merge and compress into a single bracket labeled "index 1 owns THIS much". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at what the bag is really doing. Those three slots for index 1 aren't three different facts — they're **one fact, stored three times**: *"index 1 owns 3 units out of 4."*
>
> **LEARNER:** So the only thing that matters is *how much* each index owns — not the individual copies. We should store the amounts, not the slots… but then how do you pick randomly from *amounts*?
>
> **TEACHER:** That's the exact right question. Pause the video. If each index owns a **chunk of territory**, and you throw a dart at random — what do you need to know about each chunk to figure out *whose* territory the dart hit?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it)*

**[VISUAL: a horizontal number line 0 → 4. Segment `[0, 1)` in blue labeled "index 0", segment `[1, 4)` in orange labeled "index 1". A dart animates in and lands at 2.6 — the orange segment flashes.]**

> **TEACHER:** Here's the picture that solves it. Lay the weights out as **segments on a number line**, end to end. Index 0 owns from 0 to 1 — width 1. Index 1 owns from 1 to 4 — width 3. The whole line runs from 0 to `total = 4`.
>
> Now throw a dart at a uniform random point on that line. Whichever segment it lands in — that's your answer. A segment three times as wide catches the dart three times as often. **Same probabilities as the bag — and we never built a single slot.**
>
> **[VISUAL: the segment boundaries get flags: 1 and 4. Caption: "all we store: where each segment ENDS."]**
>
> And what do we actually need to store? Just where each segment **ends**. Index 0's segment ends at 1. Index 1's ends at 4. That list — `[1, 4]` — is the running total of the weights: `1`, then `1 + 3`. That's a **prefix-sum array**. Two indices, two numbers. Doesn't matter if the weights are 1-and-3 or a-million-and-three-million — still two numbers.
>
> **LEARNER:** Okay, but once the dart lands at, say, 2.6 — finding *which* segment contains it means scanning the ends left to right, doesn't it? That's O(n) per pick, and picks are the hot path.
>
> **TEACHER:** It would be — except look at that ends array. Running totals of **positive** weights only ever go up. `[1, 4]` is *sorted, guaranteed*. And "find where a value fits in a sorted array" — that's not a scan. That's **binary search**. The dart-throw becomes `O(log n)`.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "prefix sums = segment ends · dart = randint(1, total) · binary search the first end ≥ dart."]**

> The key move, one sentence: **prefix sums turn weights into segment boundaries on a number line; a random dart plus binary search finds the segment in log n.**
>
> Any problem shaped like *"cumulative ranges, then find which range a point falls into"* — weighted sampling, percentile lookups, anything with a distribution — this exact combo is your reflex.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type the imports + constructor skeleton.]**

> Let's build it in pieces. Constructor first — this is our "build once" phase. One running total, appended as we go.

```python
import random
import bisect

class Solution:
    def __init__(self, w):
        # prefix[i] = right edge of index i's segment on the number line
        self.prefix = []
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running          # == prefix[-1] == sum(w)
```

> **[VISUAL: run the constructor on w = [1, 3] live — prefix fills to [1, 4], total = 4, drawn under the number line from beat 5.]**
>
> For our example: after weight 1, `running` is 1 — append it. After weight 3, `running` is 4 — append it. `prefix = [1, 4]`, `total = 4`. Exactly the segment ends we drew. One O(n) pass, done forever.
>
> **[VISUAL: add pickIndex — two lines, each highlighted as it lands.]** Now the pick — the whole method is two lines.

```python
    def pickIndex(self):
        # dart at a uniform integer in [1, total]
        target = random.randint(1, self.total)
        # smallest i with prefix[i] >= target → the segment the dart lands in
        return bisect.bisect_left(self.prefix, target)
```

> Line one throws the dart: a uniform random integer `target` from **1** to `total` — inclusive on both ends, and note it starts at 1, not 0. Hold that thought; it's not an accident.
>
> Line two catches it: `bisect_left` finds the **smallest** index whose prefix value is greater than or equal to `target` — the first segment end that reaches the dart. That's the owner.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the number line with target-values written INSIDE the segments: index 0 owns {1}, index 1 owns {2, 3, 4}. The boundary value 4 pulses.]**

> Why is this right — and where's the trap?
>
> Think of `target` as picking one of `total` equally-likely integers: 1, 2, 3, 4. Index 0's segment covers exactly the value {1}. Index 1's covers {2, 3, 4}. One value out of four versus three out of four — that's the 25/75 we were asked for, exactly. In general, segment `i` covers the integers from `prefix[i-1] + 1` up through `prefix[i]` — which is exactly `w[i]` of them. Widths equal weights; the math is airtight.
>
> **LEARNER:** Wait — `bisect_left`, so the condition is `prefix[i] >= target`. Why greater-or-*equal*? If the dart lands exactly ON a boundary, say `target = 1` in our example, who owns it?
>
> **TEACHER:** *This* is the off-by-one from the cold open, so let's nail it. Ask who owns boundary value 1. Index 0's segment is the target-values `1` through `prefix[0] = 1` — a segment **includes its own right edge**. So `target = 1` belongs to index 0, and we need the *first* prefix that reaches-or-equals the target: `>=`, which is exactly `bisect_left`. Flip it to strict `>` — that's `bisect_right` — and `target = 1` would skip past index 0 and return index 1. You'd silently steal one unit of probability from every index and hand it to its neighbor. The code still runs, the tests still mostly pass — the *distribution* is just wrong.
>
> **LEARNER:** And that's also why `randint` starts at 1 and not 0? Because with a 0, nothing owns it — no segment includes a left edge of zero.
>
> **TEACHER:** Exactly. `target = 0` would be a dart landing before the line even starts. The range `[1, total]` and `bisect_left` are a matched pair — change either one alone and the boundaries shift by one. That's the whole trap, and now it's yours.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row, dart animating to each target on the number line.]**

> Let's run every possible dart for `w = [1, 3]`, `prefix = [1, 4]`, `total = 4` — all four values `randint(1, 4)` can produce.

| `target` | first `prefix[i] >= target` | index returned |
|---|---|---|
| 1 | `prefix[0] = 1` | **0** |
| 2 | `prefix[1] = 4` | **1** |
| 3 | `prefix[1] = 4` | **1** |
| 4 | `prefix[1] = 4` | **1** |

> One dart out of four returns index 0. Three out of four return index 1. That's 25% and 75% — *exactly* the spec, not approximately. Loop closed.
>
> **[VISUAL: second number line: w = [2, 5, 1, 4] → prefix = [2, 7, 8, 12]. A dart lands on 8; binary search brackets animate: lo/hi arrows.]**
>
> One more, bigger, to watch the binary search actually search. `w = [2, 5, 1, 4]` gives `prefix = [2, 7, 8, 12]`, total 12. Say the dart is `target = 8`. Search: `lo = 0`, `hi = 3`. Mid is 1 — `prefix[1] = 7`, that's less than 8, too small, go right: `lo = 2`. Mid is 2 — `prefix[2] = 8`, that reaches 8, keep it: `hi = 2`. `lo` meets `hi` at **2**. And check it: index 2's segment is target-values {8} — weight 1, and 8 is precisely it. Two probes instead of a scan. On ten thousand weights, that's about fourteen probes instead of ten thousand.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: table — Brute bag: build O(sum w), pick O(1), space O(sum w). Ours: build O(n), pick O(log n), space O(n).]**

> Say it the way you'd say it in the room: *"The constructor is O(n) — one pass to build the prefix array. Each `pickIndex` is O(log n) — one binary search. The bag version had O(1) picks, but it paid O(sum of weights) in build time and memory — with a hundred-million weight, that's the difference between four kilobytes and four hundred megabytes."*
>
> Notice the honest trade: we gave up O(1) picks for O(log n) picks, and in exchange the memory stopped depending on the weight *values* entirely. Log of ten thousand is fourteen. That trade wins every time.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: the prefix array with a "shrink me?" thought bubble → red ✗. Caption: "the sorted array IS what binary search searches."]**

> Can we beat O(n) space? **No — and being able to say why is the point.**
>
> The prefix array isn't bookkeeping — it's the *search space*. Binary search needs the sorted boundary list to exist; that O(n) structure is literally what buys the O(log n) pick. Throw it away and your only option is re-scanning the weights on every pick — O(n) per query, on the hot path that's called ten thousand times. You'd be saving memory by torching the thing the memory was for.
>
> Say it out loud: *"Space is O(n) for the prefix array, and that's optimal — there's no rolling-variable trick, because I need the whole boundary list present to search it."* Naming *why* it can't shrink is a stronger signal than silently accepting it.

---

## 12. YOUR TURN (active recall) — `10:05`
*(retrieval practice)*

**[VISUAL: "Your turn → Random Pick with Blacklist (LC 710)". A blank editor.]**

> Before the next video, try **Random Pick with Blacklist** — pick uniformly from 0 to n−1, but certain values are banned. Same DNA as today: you're mapping a uniform random draw onto a distribution that isn't uniform-and-clean. Different mechanism — remapping instead of prefix sums — but the *"one random number in, the right answer out"* instinct is identical.
>
> Ten minutes, no peeking. The struggle is the workout.

---

## 13. LOCK IT IN — `10:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line: "weights are segments on a number line — throw a dart, binary-search the landing."]**

> Three takeaways:
> 1. **Never materialize the bag** — the cost tracks weight *values*, not weight *count*. Store amounts, not copies.
> 2. **Prefix sums are segment ends** — positive weights make the array strictly increasing, so binary search is legal.
> 3. **The boundary pair travels together** — `randint(1, total)` with `bisect_left`'s `>=`. Change either alone and you silently skew the distribution.
>
> The memory peg: **weights are segments on a number line — throw a dart, binary-search where it landed.**
>
> *(GCA reminder — for the interview itself: Google scores General Cognitive Ability, and half that rubric is you narrating the journey. State the bag idea first, name exactly why it dies — cost tracks magnitude, not count — then derive the number line out loud. And before you code, ask the one clarifying question that shows you read the spec: "weights are all positive, right? — that's what keeps the prefix array strictly increasing so binary search is well-defined." The question IS the signal.)*

---

## 14. CLIFFHANGER — `11:05`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "RLE Iterator" — a run-length-encoded array `[3,8, 0,9, 2,5]` unrolling into `8,8,8,5,5`, then a `next(n)` cursor jumping across it.]**

> Today we refused to expand weights into a giant bag — we stored boundaries instead. Next lesson, the *input itself* is a compressed bag: run-length encoding, where `[3, 8]` means "the value 8, three times," and you have to iterate through it — jumping forward `n` elements at a time — **without ever unrolling it**. Same enemy, magnitude-versus-count, but now it's an iterator you have to keep alive between calls. That's RLE Iterator. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.Random;

class Solution {
    private final int[] prefix;   // prefix[i] = right edge of segment i
    private final int total;
    private final Random rand = new Random();

    public Solution(int[] w) {
        prefix = new int[w.length];
        int running = 0;
        for (int i = 0; i < w.length; i++) {
            running += w[i];
            prefix[i] = running;
        }
        total = running;                       // == sum(w)
    }

    public int pickIndex() {
        int target = rand.nextInt(total) + 1;  // uniform in [1, total]
        // manual binary search: smallest i with prefix[i] >= target
        int lo = 0, hi = prefix.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (prefix[mid] < target) {
                lo = mid + 1;                  // mid too small — go right
            } else {
                hi = mid;                      // mid works — keep it, shrink right
            }
        }
        return lo;
    }
}
```

*(No `bisect` in Java — you write the binary search by hand, and the `hi = mid` — not `mid - 1` — is what makes it find the **smallest** qualifying index: we never discard `mid` when it already satisfies the threshold. Interviewers love asking why that line isn't `mid - 1`; now you know.)*
