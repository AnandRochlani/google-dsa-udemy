# 🎬 Recording Script — Koko Eating Bananas (Binary Search on the Answer)
**Pattern: Modified Binary Search · LeetCode 875 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the *boundary* template from First Bad Version (`while lo < hi`, `hi = mid`, return `lo`).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: piles of bananas `[3, 6, 7, 11]`, a clock reading "8 hours", and a big glowing question mark over a number labeled `k = eating speed`.]**

> Koko the monkey has piles of bananas and 8 hours before the guards come back. Each hour she picks one pile and eats up to `k` bananas from it. Find the **slowest** speed `k` that still clears every pile in time.
>
> Here's what trips people: there's no array of speeds to search. The answer `k` isn't sitting in the input anywhere — you have to *invent* it. And it could be anything from 1 up to a billion.
>
> So how do you binary-search a number that isn't in any array? That's the whole lesson — the single most powerful pattern in this section. Google *loves* it. By the end, "binary search the answer" will feel obvious. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: piles `3 6 7 11`, `h = 8`. Below: "speed k = ? bananas/hour". A note: "if a pile has fewer than k left, she eats it and waits out the hour."]**

> One line: **find the minimum integer speed `k` so the total hours to eat all piles is ≤ `h`.** One rule to internalize — she won't switch piles mid-hour, so a pile of 7 at speed 4 takes *two* hours: 4, then 3.
>
> Tiny example — piles `[3, 6, 7, 11]`, 8 hours. The answer is `4`. Don't trust me yet — we'll earn it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: a speed dial starting at 1, ticking up. For each speed, hours computed pile by pile; a red ✗ or green ✓.]**

> Brute force: try every speed from 1 up, stop at the first that fits.
>
> `k = 1`: hours = 3+6+7+11 = 27. Way over 8. ✗
> `k = 2`: 2+3+4+6 = 15. ✗
> `k = 3`: 1+2+3+4 = 10. Still over. ✗
> `k = 4`: 1+2+2+3 = 8. Fits! ✓ Return 4.
>
> Four tries here. But the speed range runs up to the biggest pile.
>
> **[VISUAL: max pile balloons to 1,000,000,000; the dial spins hopelessly; each tick is itself an O(n) sum.]**
>
> Piles up to a billion means up to a billion speeds to try, and *each* try re-sums all the piles. That's ten-to-the-thirteen operations. Instant timeout. We're scanning a giant range one integer at a time — sound familiar?

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: a horizontal speed axis 1 … max, each speed stamped ✗ or ✓: `✗ ✗ ✗ ✓ ✓ ✓ …`. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Look at the *feasibility* across speeds, not the piles. Line up every speed and mark whether Koko finishes: `✗ ✗ ✗ ✓ ✓ ✓`. Pause and predict two things: **First — could a speed of 5 ever be too slow if 4 already works? Second — what does that shape `✗✗✗✓✓✓` remind you of from two lessons ago?**
>
> **LEARNER:** If 4 works, 5 is even faster, so 5 *has* to work too — you can't finish slower by eating faster. And that shape… that's `F F F T T T`. It's First Bad Version. It's a boundary.
>
> **TEACHER:** Yes. Feasibility only flips once, from ✗ to ✓, and never back. It's monotonic. Which means we can *binary-search the speed* — and we never needed an array at all.

---

## 5. BUILD THE INTUITION (the aha) — `3:35`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two panels. Left: "search INSIDE the array" (old lessons). Right: "search the ANSWER RANGE [1, max pile]" with lo/mid/hi markers riding a speed axis, no array beneath.]**

> Here's the leap, and it's a big one. In every earlier problem, the thing we searched *lived in an array* — a value, a grid cell, a version. **Here, we binary-search over the answer value itself.** The search space is the *range of possible speeds*, `[1, max pile]`. There is no array. We invent the axis.
>
> **[VISUAL: analogy — a thermostat dial. Too cold = ✗, comfortable = ✓. You don't try every degree; you jump to the middle, feel it, and turn toward comfort.]**
>
> Think of a thermostat you're tuning to the *lowest* comfortable setting. You don't sweep every degree. You jump to the middle, ask "comfortable yet?", and halve.
>
> Our "comfortable?" question is: **at speed `mid`, does Koko finish in `h` hours?** That's a helper — sum up `ceil(pile / mid)` across piles, an O(n) pass. That helper *replaces* the array peek. It's our comparator.
>
> **[VISUAL: speed range [1,11], mid=6 → hours=6 ≤ 8 → ✓ → the faster half (7..11) greys out; since 6 works, KEEP 6, hi = 6.]**
>
> `mid = 6`: finishes in 6 hours, fits. So 6 works — but maybe something *slower* also works, and we want the slowest. So we keep 6 as a candidate and search the slower half. That's the exact boundary move from First Bad Version: `hi = mid`.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Minimize X with a monotonic feasible(X)? Binary-search X's RANGE; feasible() is your comparator; keep the working mid → hi = mid."]**

> Burn this in: **when you're asked to minimize or maximize a value, and `feasible(value)` flips once from false to true — binary-search the value's range, using the feasibility check as your comparison.** You're not searching the input. You're searching the answer.

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 — the feasibility helper first.]**

> First the comparator — how many hours does speed `k` need?

```python
def minEatingSpeed(piles, h):
    def hours_needed(k):
        # ceil(p / k) with pure integer math — no float rounding bugs on huge values
        return sum((p + k - 1) // k for p in piles)
```

> **[VISUAL: add chunk 2, highlight the bounds — the answer range, not an array.]** Now the search space: speeds from 1 to the biggest pile.

```python
    lo, hi = 1, max(piles)      # speed can't be 0; never need faster than the biggest pile
```

> **[VISUAL: add chunk 3 — the boundary loop, identical shape to First Bad Version.]** Same boundary template — `< `, `hi = mid`, return `lo`.

```python
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if hours_needed(mid) <= h:
            hi = mid            # mid works → try SLOWER, but keep mid as candidate
        else:
            lo = mid + 1        # mid too slow → need FASTER
    return lo                   # slowest speed that finishes in time
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:10`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight `(p + k - 1) // k`, then `hi = mid`, then the bounds.]**

> Two things earn a real explanation.
>
> First, `(p + k - 1) // k`. That's `ceil(p / k)` done in integers. Why not `math.ceil(p / k)`? Because with piles up to a billion, floating-point division can round wrong at the edges and hand you an off-by-one. Integer ceil is exact. Say that in the room — it signals you've been burned before.
>
> **LEARNER:** Hold on — why is `hi = max(piles)` a safe ceiling? Why not `sum(piles)` to be safe, or `max(piles) + 1`?
>
> **TEACHER:** Good instinct to question the bounds — that's where these bugs hide. At speed `max(piles)`, every pile is eaten in exactly one hour, so Koko needs exactly `len(piles)` hours. The problem guarantees `h >= len(piles)`, so `max(piles)` *always* finishes — it's guaranteed feasible. There's zero reason to go faster; a bigger pile doesn't exist to justify it. So `max(piles)` is the tightest correct upper bound. Padding it to `+1` isn't wrong, just wasteful.
>
> **LEARNER:** And `hi = mid`, not `mid - 1` — same reason as First Bad Version?
>
> **TEACHER:** Exactly the same. When `mid` works, `mid` might *be* the slowest feasible speed. `mid - 1` could leap past the answer. The `while lo < hi` with a floored `mid` guarantees the window still shrinks, so no infinite loop — it's the boundary template, unchanged. The only thing that's new today is *what* the axis represents: a speed, not an index.

---

## 9. DRY-RUN THE CODE — `8:30`
*(worked example — prove it, close the loop)*

**[VISUAL: speed axis [1,11]; trace table; the discarded half greys each row.]**

> Real code, `piles = [3, 6, 7, 11]`, `h = 8`, range `[1, 11]`.

| lo | hi | mid | hours_needed(mid) | ≤ 8? | action |
|---|---|---|---|---|---|
| 1 | 11 | 6 | 1+1+2+2 = 6 | yes | hi = 6 (keep) |
| 1 | 6 | 3 | 1+2+3+4 = 10 | no | lo = 4 |
| 4 | 6 | 5 | 1+2+2+3 = 8 | yes | hi = 5 (keep) |
| 4 | 5 | 4 | 1+2+2+3 = 8 | yes | hi = 4 (keep) |
| — | — | — | lo(4) == hi(4) | — | **return 4** ✅ |

> Four feasibility checks — not a billion. Watch rows 3 and 4: speed 5 fits *and* speed 4 fits, and because we're minimizing we keep shrinking toward the slower one. When `lo` and `hi` meet at 4, that's the slowest speed that still fits 8 hours. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:30`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(max·n). Ours: O(n · log(max pile)), O(1) space. A "10^13 → ~34 checks × n" callout.]**

> Say it: *"I'm not searching the array — I'm searching for the answer, the speed, which lives in `[1, max pile]`. Feasibility is monotonic: if a speed works, every faster speed works. So I binary-search the speed range, and my comparison is an O(n) pass summing `ceil(pile / k)`. That's O(n log(max pile)) time, O(1) space — turning a billion-wide scan into about 34 checks."* That framing — "search the answer, feasibility is the comparator" — is the money sentence.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:15`
*(depth + honesty)*

**[VISUAL: two int bounds + a running sum; a note "the range [1, max pile] is never materialized".]**

> Already O(1) — two bounds plus a running sum inside the helper. And the deeper point: the win here was never about space. It was recognizing that **feasibility is monotonic**, which let a log-scan replace a linear scan over a billion candidates. The `hours_needed` helper is the comparator that tells binary search which half of the *speed* range to drop. Name the monotonicity out loud — that's the insight they're grading.

---

## 12. YOUR TURN (active recall) — `10:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Capacity To Ship Packages Within D Days (LC 1011)". Blank editor.]**

> Before next time, try **Capacity To Ship Packages Within D Days**. Identical shape: find the minimum ship capacity to deliver everything in `D` days. Ask yourself the three questions — *What's the answer range? Is feasibility monotonic? What's my feasible() check?* Nail those three and the boundary template just drops in. Struggle before peeking.

---

## 13. LOCK IT IN — `11:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Search the ANSWER, not the array** — when the answer is a number in a known range.
> 2. **The unlock is monotonic feasibility** — `feasible(x)` flips once, `✗✗✗✓✓✓`.
> 3. **`feasible()` replaces the array peek**; keep the working mid with `hi = mid`.
>
> The peg — hear **"minimum/maximum value such that…"** and think: **what's the range, is it monotonic, what's my check?** Then binary-search the answer.

---

## 14. CLIFFHANGER — `12:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Median of Two Sorted Arrays" — two sorted strips with a scissor-cut hovering, labeled "the partition".]**

> You've now searched inside arrays, over grids, and over invented answer ranges. The finale bends binary search the hardest: two sorted arrays, find the median, in O(log). You won't search for a value *or* a speed — you'll search for the perfect **cut** that splits both arrays into a balanced left and right half. It's the trickiest off-by-one gauntlet in the set, and once it clicks, nothing in binary search will scare you again. That's next.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int minEatingSpeed(int[] piles, int h) {
    int lo = 1, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);      // hi = max pile (always feasible)

    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (hoursNeeded(piles, mid) <= h) hi = mid; // works → try slower, keep mid
        else lo = mid + 1;                          // too slow → go faster
    }
    return lo;
}

private long hoursNeeded(int[] piles, int k) {
    long hours = 0;                                 // long: 10^4 piles × 10^9 overflows int
    for (int p : piles) hours += (p + k - 1) / k;   // ceil(p/k), integer math
    return hours;
}
```
