# 🎬 Recording Script — Search in Rotated Sorted Array
**Pattern: Modified Binary Search · LeetCode 33 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the canonical `[lo, hi]` binary-search template (LC 704, previous lesson).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a clean sorted bar `[0,1,2,4,5,6,7]`. Scissors snip it between 7 and 0; the pieces swap → `[4,5,6,7,0,1,2]`. A red "O(log n) required" tag.]**

> You nailed binary search last lesson. Then Google hands you this: the array *was* sorted — then someone rotated it. Cut it somewhere and swapped the two chunks. `[4,5,6,7,0,1,2]`.
>
> Your instinct screams: "It's not sorted anymore, binary search is dead, just scan it." And that scan is O(n) — the exact thing they told you not to do.
>
> Here's the twist that saves you: a rotated sorted array isn't random. It's **two sorted runs glued together**, and at every midpoint, one side is *still perfectly sorted*. By the end you'll binary-search this in O(log n) with the same template — plus one clever question asked each step. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: seven index-labeled tiles `4 5 6 7 0 1 2` (indices 0–6). `target = 0` boxed.]**

> One line: **a sorted array of distinct numbers got rotated; find the index of `target`, or −1, in O(log n).**
>
> Tiny example — seven tiles. We want `0`. Your eye finds it at index `4`. Notice the shape: it climbs `4,5,6,7`, then falls off a cliff to `0,1,2`. Two rising runs. Hold that picture.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: a marker walks left to right; "looks" counter ticks 1,2,3,4,5 until it lands on `0`.]**

> Brute force: walk it. `4`? no. `5`? no. `6`? no. `7`? no. `0`? yes — five looks. Works.
>
> But that's O(n), and worse — we threw away everything binary search taught us. We're treating a *mostly sorted* array like a bag of random numbers.
>
> **[VISUAL: the array bar grows to 5000 elements, counter blurs upward.]**
>
> Five thousand elements, up to five thousand looks. The interviewer's O(log n) demand is us leaving structure on the table.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: `lo` at 0, `hi` at 6, `mid` at 3 (value 7). A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Let's try plain binary search and watch it break. `mid` is index 3, value `7`. Target `0`. `7 > 0`, so plain logic says "go left." But the `0` is on the *right*. The peek **lied** — because the array isn't globally sorted.
>
> **LEARNER:** So the middle value is useless here? If comparing to `target` doesn't tell me the side, what's left to go on?
>
> **TEACHER:** Great question — that's the trap. The middle value alone can't tell you where `target` is. But it *can* tell you something else. Pause and predict: **look at the left half `[4,5,6,7]` versus the right half `[7,0,1,2]` — which one is still cleanly sorted, and how could you tell just from the endpoints?**

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: split at mid=3. Left half `[4,5,6,7]` glows green "sorted"; right half `[7,0,1,2]` glows amber "has the cliff". The pivot cliff between 7 and 0 flagged.]**

> Here's the unlock. Wherever you cut, the rotation cliff — the drop from `7` to `0` — sits in *exactly one* half. So **the other half is fully sorted.** Always. One clean, one broken.
>
> And you can tell which with a single comparison. If `nums[lo] <= nums[mid]`, the left half rises the whole way — it's the clean one. Otherwise the cliff is on the left, so the *right* half is clean.
>
> **[VISUAL: analogy card — a spiral staircase with one broken step. Split anywhere, and the unbroken flight has a known bottom and top.]**
>
> Now the payoff: once you know a half is sorted, you know its **exact range** from its two endpoints. So you ask a bulletproof O(1) question — "does `target` fall between them?" If yes, search that half. If no, the answer *must* be in the other half. Either way, half the array is gone. Binary search, back in business.
>
> **[VISUAL: left half is sorted [4..7]; target 0 not in [4,7); grey it out, lo jumps to index 4.]**
>
> Left half `[4..7]` is sorted. Is `0` in `[4, 7)`? No. So throw the whole left half away. `lo` jumps past `mid`. Done in one step what the scan took four to inch through.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "At each mid: find the SORTED half, ask if target lives in its known range, keep or drop it."]**

> The one line to remember: **one half is always sorted — identify it, check if the target is inside its range, and let that decide which half to keep.** You don't need the whole thing ordered. You just need enough local order to delete half.

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. The exact LC 704 skeleton types in first, greyed, to anchor the callback.]**

> Same skeleton as last lesson — inclusive bounds, `while lo <= hi`, overflow-safe mid.

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
```

> **[VISUAL: add chunk 2, highlight the `<=`.]** Now the new part — decide which half is sorted.

```python
        if nums[lo] <= nums[mid]:              # LEFT half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                   # target inside sorted left → keep it
            else:
                lo = mid + 1                   # else it's in the right half
```

> **[VISUAL: add chunk 3 — the mirror image.]** Otherwise the right half is the clean one.

```python
        else:                                  # RIGHT half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                   # target inside sorted right → keep it
            else:
                hi = mid - 1                   # else it's in the left half
    return -1
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight the `<=` in `nums[lo] <= nums[mid]`, and each range check.]**

> Walk the *why*. `nums[lo] <= nums[mid]` — if the left endpoint is at or below the mid, the left run never dipped, so it's sorted. Its range is exactly `[nums[lo], nums[mid]]`, so `nums[lo] <= target < nums[mid]` is a rock-solid "is it in here?" test. If yes, keep left; if not, the answer is forced into the right half.
>
> **LEARNER:** Why `<=` in `nums[lo] <= nums[mid]`? With `<`, wouldn't it still usually work? What edge case are you guarding?
>
> **TEACHER:** The killer edge case is a window of one, where `lo == mid`. Then `nums[lo]` and `nums[mid]` are the same element, and `nums[lo] < nums[mid]` is *false* — you'd wrongly declare the left half "unsorted" and take the wrong branch. `<=` makes a single-element half correctly count as sorted. In binary search these tie cases are where the bugs live, so the equals earns its keep.
>
> **LEARNER:** And that `< nums[mid]` — strict? Not `<=`?
>
> **TEACHER:** Strict on purpose. We already tested `nums[mid] == target` at the top and returned. So by the time we're here, `target` is *not* `nums[mid]` — including `nums[mid]` in the "keep left" range would be a lie. The comparisons are asymmetric because we peeled off the equal case first.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: `[4,5,6,7,0,1,2]`, target 0. Trace table; the discarded half greys each row.]**

> Real code, target `0`.

| lo | hi | mid | nums[mid] | sorted half | target in it? | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left [4..7] | 0 in [4,7)? no | lo = 4 |
| 4 | 6 | 5 | 1 | left [0..1] (nums[4]=0 ≤ 1) | 0 in [0,1)? yes | hi = 4 |
| 4 | 4 | 4 | 0 | — | nums[mid]==0 | **return 4** ✅ |

> Three peeks, and notice row two: even inside the "low" chunk, the sub-window `[0,1]` is itself a clean sorted run — the logic keeps holding as the window shrinks. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:45`
*(transfer to interview)*

**[VISUAL: rows — Scan: O(n). Ours: O(log n), O(1) space.]**

> Say it: *"Plain binary search breaks because rotation makes the mid value lie about which side to keep. But one half is always sorted — I detect it with `nums[lo] <= nums[mid]`, then do an O(1) range check to see if the target's inside it. Either way I drop half. O(log n) time, O(1) space."* That "one half is always sorted" sentence is what earns the nod.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:20`
*(depth + honesty)*

**[VISUAL: single-pass version beside a two-pass "find pivot, then search" version with more branches.]**

> Already O(1) — two indices, one pass. Honest alternative worth naming: some people do two passes — first binary-search for the pivot, then binary-search the correct run. Same O(log n), same O(1) space, but two passes and more edge cases to trip on. Say you prefer the single pass for fewer moving parts. Interviewers like fewer places to bug out.

---

## 12. YOUR TURN (active recall) — `9:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Find Minimum in Rotated Sorted Array (LC 153)". A blank editor.]**

> Before next time, try **Find Minimum in Rotated Sorted Array**. Same "one half is sorted" idea — but instead of hunting a target, you're locating the pivot itself, the bottom of the cliff. Ask: which half holds the drop? Wrestle it for ten minutes before peeking.

---

## 13. LOCK IT IN — `10:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **A rotated sorted array = two sorted runs; one half of any split is always clean.**
> 2. **Detect the sorted half with `nums[lo] <= nums[mid]`** — the `<=` covers the single-element tie.
> 3. **Range-check the target against the sorted half's endpoints** — that's the O(1) decision.
>
> The peg — see **"rotated"** and don't panic: **find the sorted half, ask if the target lives there.** Local order is enough to burn a half.

---

## 14. CLIFFHANGER — `11:05`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "First Bad Version" — a strip of cells reading `F F F T T T` with the flip glowing.]**

> So far we've been *matching a value* — is `nums[mid]` the target? Next problem changes the question entirely. You're not looking for a value at all — you're looking for a **boundary**, the exact spot where "good" flips to "bad" and never flips back. Same halving, but the template shifts in one subtle, off-by-one-dangerous way. That's next.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {                       // left half sorted
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {                                           // right half sorted
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```
