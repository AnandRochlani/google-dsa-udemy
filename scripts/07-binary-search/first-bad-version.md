# 🎬 Recording Script — First Bad Version (Boundary Search)
**Pattern: Modified Binary Search · LeetCode 278 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the canonical `[lo, hi]` template (LC 704). This lesson introduces the *boundary* variant.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a git commit history, versions 1…n. One commit glows red; everything after it turns red too. A counter: "API calls: 1,000,000,000…" spinning.]**

> A build broke. Some version shipped a bug, and every version after it is broken too. You've got an `isBadVersion` check — but it's a slow, expensive API call, and there are up to **two billion** versions.
>
> The naive move — check version 1, 2, 3… — could fire two billion API calls. That's not a solution, that's an outage.
>
> But look at the shape: good, good, good, then bad, bad, bad — forever. There's exactly one flip. And finding a flip in that shape is binary search wearing a slightly different hat. By the end you'll find it in about 31 calls instead of two billion — with a template tweak you'll reuse for "search the answer" problems later. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: five tiles labeled versions 1–5, each showing `F F F T T`. A box: "first bad = ?"]**

> One line: **versions are `1..n`; once one is bad, all later ones are bad; find the first bad one with as few API calls as possible.**
>
> Tiny example — `n = 5`, and the results read `F F F T T`. Your eye sees it instantly: the first `T` is version `4`. That's the answer. We want the machine to find that flip without asking every version.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: a marker checks each version left to right; "API calls" counter ticks 1,2,3,4 then stops at the first T.]**

> Brute force: ask in order. `isBadVersion(1)`? F. `(2)`? F. `(3)`? F. `(4)`? T — stop, return 4. Four calls here.
>
> Fine for `n = 5`. But the flip could be near the *end*.
>
> **[VISUAL: n balloons to 2,000,000,000; the marker crawls; counter races toward a billion.]**
>
> If the first bad version is number 1.9 billion, that's 1.9 billion expensive API calls. Each call rules out just one version. On a monotonic sequence, that's the same crime as scanning a sorted array.

---

## 4. THE PAIN POINT + PREDICT — `2:05`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on `F F F T T`. A finger taps the middle, version 3. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Each call kills one candidate. But the sequence is *monotonic* — once it goes bad it stays bad. Pause and predict: **I test the middle version, 3, and it comes back Good. What does that one call tell me about versions 1, 2, and 3 — and where must the first bad one be?**
>
> **LEARNER:** If 3 is good, and it only flips *once*… then 1 and 2 are good too. So the first bad version has to be somewhere to the right of 3.
>
> **TEACHER:** Exactly — one call just cleared three versions. That's the halving, and now we hunt in the right half.

---

## 5. BUILD THE INTUITION (the aha) — `2:50`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: `lo` at version 1, `hi` at version 5, `mid` at 3. mid=Good → versions 1–3 grey out, lo jumps to 4. Then mid=4 → Bad → KEEP 4, hi moves to 4.]**

> Think of a light switch on a long hallway wire — off, off, off, then on, and it never turns back off. You're finding the switch. You don't walk the whole wire; you probe the middle. Dark there? The switch is further down. Lit? The switch is here or behind you.
>
> Same here. Probe `mid`. If it's **Good**, the flip is strictly to the right — `lo = mid + 1`. If it's **Bad**, the flip is at `mid` *or* to its left — and here's the crucial difference from last lesson: **`mid` itself might be the answer**, so we do *not* throw it away. We set `hi = mid`, keeping `mid` alive as a candidate.
>
> **[VISUAL: side-by-side callout — LC 704: "hi = mid - 1 (discard mid)"; here: "hi = mid (KEEP mid)". A big yellow "boundary, not match".]**
>
> That's the whole shift. In LC 704 we were *matching a value*, so once we checked `mid` we tossed it. Here we're locating a *boundary*, and the boundary could *be* `mid` — tossing it could skip the true first-bad version.

---

## 6. THE KEY MOVE (signaling) — `4:00`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Boundary search: bad → hi = mid (keep it); good → lo = mid + 1. Loop while lo < hi, return lo."]**

> Burn this in: **when you're finding the leftmost thing that satisfies a condition, keep the maybe-answer — `hi = mid`, not `mid - 1`.** And the loop becomes `while lo < hi`, returning `lo`. You're converging on one boundary, not testing for a hit.

---

## 7. CODE IT — LIVE & CHUNKED — `4:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> The search space is the *version numbers* `1..n` — we never build an array, just track two bounds.

```python
def firstBadVersion(n):
    lo, hi = 1, n              # boundary lives somewhere in [1, n]
```

> **[VISUAL: add chunk 2, highlight the strict `<`.]** Loop while more than one candidate remains.

```python
    while lo < hi:            # STRICT < : stop when exactly one version is left
        mid = lo + (hi - lo) // 2
```

> **[VISUAL: add chunk 3 — the two-way boundary decision, no equality branch.]** Probe, then keep or discard.

```python
        if isBadVersion(mid):
            hi = mid          # bad → answer is mid or LEFT → KEEP mid
        else:
            lo = mid + 1      # good → answer is strictly RIGHT
    return lo                 # lo == hi → the lone surviving boundary
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:35`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight `hi = mid`, the `<`, and the `return lo`. A side box: "3 differences from LC 704".]**

> Three deliberate differences from the canonical template — and each one is an off-by-one waiting to bite.
>
> One: **`hi = mid`, not `mid - 1`.** A bad `mid` is still a *possible* first-bad version. `mid - 1` could leap right over the answer.
>
> Two: **`while lo < hi`, strict.** There's no "found it, return mid" branch — we never match, we converge. When `lo == hi`, one candidate remains and it *is* the boundary, so we stop and return it.
>
> **LEARNER:** Wait — with `hi = mid` and not `mid - 1`, doesn't `hi` risk getting stuck and looping forever? That's the exact hang you warned us about last time.
>
> **TEACHER:** Sharp, and here's why it's safe. `mid = lo + (hi - lo) // 2` *floors* — it always rounds toward `lo`. So while `lo < hi`, `mid` is strictly less than `hi`. The bad branch `hi = mid` therefore *strictly shrinks* `hi`. And the good branch `lo = mid + 1` strictly grows `lo`. Every path narrows the window, so it can't spin. The floor is doing quiet, load-bearing work.
>
> **LEARNER:** Then why return `lo` and not `hi`?
>
> **TEACHER:** At the end they're equal — `lo == hi` — so either works. I write `lo` by convention. The point is the loop only exits when they meet, and that meeting point is the flip.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it, close the loop)*

**[VISUAL: `n = 5`, results `F F F T T`. Trace table; the discarded half greys each row.]**

> Real code, `n = 5`, first bad is `4`.

| lo | hi | mid | isBadVersion(mid) | action |
|---|---|---|---|---|
| 1 | 5 | 3 | F | lo = 4 (drop 1–3) |
| 4 | 5 | 4 | T | hi = 4 (KEEP mid) |
| — | — | — | lo(4) == hi(4) | **return 4** ✅ |

> Two API calls instead of four — and for two billion versions, about 31 instead of two billion. Watch row two: `mid` came back Bad and we set `hi = mid`, *not* `mid - 1`. Had we discarded it, `hi` would drop to 3 and we'd return 5 — wrong. That single choice is the whole lesson.

---

## 10. COMPLEXITY, OUT LOUD — `7:25`
*(transfer to interview)*

**[VISUAL: rows — Linear: O(n) calls. Boundary search: O(log n) calls, O(1) space.]**

> Say it: *"The results are monotonic — good then bad forever — so I binary-search for the flip. If mid is bad, the answer is mid or left, so I keep mid with `hi = mid`; if good, I move `lo` past it. I use `while lo < hi` and return `lo` because I'm converging on a boundary, not matching a value. O(log n) API calls, O(1) space."* The phrase "converging on a boundary" tells them you know *which* binary search this is.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:55`
*(depth + honesty)*

**[VISUAL: two integer bounds; a note "no array ever built — the space IS the range [1, n]".]**

> Already O(1) — just two integers. And name this subtlety: we never materialize an array of two billion booleans. The "search space" is the *numeric range* `[1, n]`, tracked by two numbers. That idea — binary-searching a range you never build — is exactly what unlocks the next family of problems.

---

## 12. YOUR TURN (active recall) — `8:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Find First and Last Position of Element (LC 34)". Blank editor.]**

> Before next time, try **Find First and Last Position**. It's *two* of these boundary searches back to back — one for the leftmost match, one for the rightmost. If you can adapt `hi = mid` versus `lo = mid` for each end, you own the pattern. Struggle before peeking.

---

## 13. LOCK IT IN — `8:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **`F F F T T T` shape → you're finding a boundary, not matching a value.**
> 2. **Keep the maybe-answer: `hi = mid`.** Loop `while lo < hi`, return `lo`.
> 3. **Floored mid guarantees the window shrinks** — that's why `hi = mid` never hangs.
>
> The peg — see **"first/leftmost that satisfies a condition"** and reach for the boundary template: **keep mid, converge, return lo.**

---

## 14. CLIFFHANGER — `9:20`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Search a 2D Matrix" — a grid morphing into a single long sorted strip.]**

> You just searched a range you never built. Next we take that idea somewhere it looks impossible: a **2-D grid**. Rows and columns, not a line — surely binary search is out? Except… if you squint, the whole grid is secretly *one* sorted list. The trick is teaching one index to pretend it's two. That's next.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int firstBadVersion(int n) {
    int lo = 1, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;      // floor → mid < hi, keeps it shrinking
        if (isBadVersion(mid)) hi = mid;    // bad → keep mid as candidate
        else lo = mid + 1;                  // good → answer is strictly right
    }
    return lo;
}
```
