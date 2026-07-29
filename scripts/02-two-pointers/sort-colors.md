# 🎬 Recording Script — Sort Colors
**Pattern: Two Pointers (three-way partition) · LeetCode 75 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** two pointers carving regions — now stretched to THREE pointers, one pass.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. `nums.sort()` typed, then crossed out with a red "no library sort" stamp. Below it: "…in ONE pass?"]**

> Google on-site. *"This array only has 0s, 1s, and 2s. Sort it in place — no library sort."*
>
> You know it's only three values, so you count them and refill. Clean, O(n). The interviewer smiles and says: *"Can you do it in a single pass?"* — and now the easy counting trick isn't enough.
>
> By the end of this video you'll own the Dutch National Flag algorithm — three pointers, one pass — plus the *one* subtle line where everyone's code breaks. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, colored tiles: `2  0  2  1  1  0` (red/white/blue).]**

> The whole problem in one line: **the array holds only 0s, 1s, and 2s — rearrange it in place so all 0s come first, then all 1s, then all 2s.**
>
> Here's our tiny example — `[2, 0, 2, 1, 1, 0]`. Six tiles. The finished array is `[0, 0, 1, 1, 2, 2]`. Hold that target — we'll build it live, in one sweep.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the six tiles. A counts box `[_,_,_]` fills during pass 1; the array refills during pass 2. Two big "PASS 1 / PASS 2" labels.]**

> Let's do the smart-but-not-smart-enough idea: counting sort.
>
> **Pass one** — tally. Scan all six: two 0s, two 1s, two 2s. Counts are `[2, 2, 2]`.
>
> **Pass two** — refill. Write two 0s, then two 1s, then two 2s. Done: `[0, 0, 1, 1, 2, 2]`.
>
> **[VISUAL: highlight that we walked all six tiles twice — two full sweeps stacked.]**
>
> Correct, O(n), O(1) space. But look — we touched every element *twice*. Once to count, once to write. With only three values, that second sweep feels like it should be avoidable.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The two sweep-arrows both highlighted red, labeled "2 passes". A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** Where's the waste? We read the whole array just to *count*, then read it again to *write*. Two passes for values so simple we could place each one the instant we see it.
>
> **LEARNER:** But how do I place a value in its final spot when I don't yet know how many 0s or 1s come later? The counting pass exists precisely to learn those boundaries.
>
> **TEACHER:** That's the tension to crack. Pause the video and think: **what if I don't need exact counts — just three moving boundaries: everything before here is a 0, everything after there is a 2, and I shove each element toward its side as I go?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the array split into three shaded zones: green "0s done" on the left, grey "unknown" middle, blue "2s done" on the right. Three pointers `low`, `mid`, `high`.]**

> **TEACHER:** Here's the leap. Instead of counting, carve the array into three growing regions with three pointers.
>
> `low` is the wall just past the finalized 0s. `high` is the wall just before the finalized 2s. `mid` is your scanner, inspecting one element at a time in the shrinking unknown middle.
>
> Think of sorting laundry into three baskets — darks left, whites right, and you pick up one item at a time from the pile in the middle. As `mid` scans:
> - See a **0**? It belongs at the front — swap it down to `low`, and both `low` and `mid` step forward.
> - See a **1**? It's already in the middle zone — just step `mid` forward.
> - See a **2**? It belongs at the back — swap it up to `high`, and shrink `high`.
>
> **[VISUAL: walk the first two moves of `[2,0,2,1,1,0]` — the 2 swaps to the back, the 0 swaps to the front.]**
>
> **LEARNER:** On the 0 and the 1 you advanced `mid`. On the 2 you didn't. Why the difference?
>
> **TEACHER:** That's *the* subtle line. When you swap a 2 to the back, the value you pulled *in* from `high` hasn't been looked at yet — it could be a 0, 1, or 2. So you must re-inspect that same `mid` slot. Advance it and you'd skip an unexamined value. When you swap a 0 down, the value coming in is from below `mid` — already sorted — so it's safe to move on.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "0 → swap to low, mid++ · 1 → mid++ · 2 → swap to high, DON'T move mid."]**

> Burn this in: **0 swaps to the low wall and mid advances; 1 just advances mid; 2 swaps to the high wall and mid stays put.**
>
> That's the Dutch National Flag. Any "partition in place around three or fewer buckets, one pass" is this move.

---

## 7. CODE IT — LIVE & CHUNKED — `5:25`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Three pointers. `low` and `mid` at the front, `high` at the back.

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
```

> **[VISUAL: add chunk 2, highlight it.]** The 0 case — swap down, advance both.

```python
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
```

> **[VISUAL: add chunk 3.]** The 1 case — leave it, just scan on.

```python
        elif nums[mid] == 1:
            mid += 1
```

> **[VISUAL: add chunk 4, highlight the missing `mid += 1`.]** The 2 case — swap up, shrink high, and *don't* touch mid.

```python
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # note: do NOT advance mid — re-inspect the swapped-in value
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:55`
*(elaboration — why each line exists)*

**[VISUAL: the full function; the invariant zones drawn under the array — `[0..low-1]`=0s, `[low..mid-1]`=1s, `[high+1..]`=2s.]**

> Let's walk *why*, not just what — through the invariant that makes it airtight.
>
> At every moment: everything before `low` is a 0, everything between `low` and `mid` is a 1, everything after `high` is a 2. The stretch from `mid` to `high` is the unknown, and it shrinks every step.
>
> `while mid <= high` — we keep going while there's still unknown territory. The instant `mid` passes `high`, that middle region is empty and the whole array is sorted.
>
> **LEARNER:** Why `mid <= high` with an equals, not strict less-than like the other two-pointer problems?
>
> **TEACHER:** Because `high` points at a slot that's still *unknown*, not yet finalized — so when `mid` and `high` land on the same index, that element still needs inspecting. Strict `<` would skip the very last unknown element and leave it possibly misplaced.
>
> The 0 branch swaps a confirmed-0 into the 0-zone and grows both walls. The 2 branch grows the 2-zone from the right — and skips advancing `mid` because the incoming value is unexamined. The 1 branch does nothing but scan, because a 1 is already home.

---

## 9. DRY-RUN THE CODE — `8:05`
*(worked example — prove it, close the loop)*

**[VISUAL: `[2, 0, 2, 1, 1, 0]` with a trace table filling row by row; the array mutates live.]**

> Let's run the actual code. Start `low=0, mid=0, high=5`.

| nums | low | mid | high | nums[mid] | action |
|---|---|---|---|---|---|
| `[2,0,2,1,1,0]` | 0 | 0 | 5 | 2 | swap mid↔high, high→4 |
| `[0,0,2,1,1,2]` | 0 | 0 | 4 | 0 | swap mid↔low, low→1, mid→1 |
| `[0,0,2,1,1,2]` | 1 | 1 | 4 | 0 | swap mid↔low, low→2, mid→2 |
| `[0,0,2,1,1,2]` | 2 | 2 | 4 | 2 | swap mid↔high, high→3 |
| `[0,0,1,1,2,2]` | 2 | 2 | 3 | 1 | mid→3 |
| `[0,0,1,1,2,2]` | 2 | 3 | 3 | 1 | mid→4 |
| `[0,0,1,1,2,2]` | 2 | 4 | 3 | — | mid > high → stop |

> Result: `[0, 0, 1, 1, 2, 2]`. Exactly our target — and notice on row 1 we swapped a 2 to the back but *didn't* move `mid`, so we caught the 0 that got pulled in. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:05`
*(transfer to interview)*

**[VISUAL: two rows — Counting: O(n) two passes / O(1). Dutch flag: O(n) one pass / O(1). A library sort greyed at O(n log n).]**

> Say it to the interviewer: *"Counting sort is O(n) time, O(1) space, but two passes. The Dutch National Flag is O(n) time, O(1) space, in a *single* pass — each element is touched once. A library sort would be O(n log n) — worse, and disallowed here."*
>
> Naming the one-pass improvement over counting is exactly the follow-up they're fishing for.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: both approaches marked O(1) space; a big arrow labeled "the win was PASSES: 2 → 1".]**

> Honesty beat: space isn't the story here — both counting sort and Dutch flag are O(1). Three integer pointers, all swaps in place.
>
> Say it out loud: *"Both are O(1) space. The real upgrade is cutting two passes to one — I place each element the moment I see it instead of tallying first."* Knowing *which axis* you improved — passes, not memory — is the senior signal.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Sort Array By Parity (LC 905)". A blank editor.]**

> Before the next video, try **Sort Array By Parity** — put all evens before all odds, in place. It's the *two-way* version of what we just did: only two buckets, so you only need two pointers, not three. Nail this and the three-pointer version will feel obvious.
>
> Don't peek. Ten minutes of struggle first — that's what locks it in.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Few buckets, in place, one pass → three-way partition.** That's the trigger.
> 2. **Three pointers:** `low` bounds the 0s, `high` bounds the 2s, `mid` scans.
> 3. **On a 2, don't advance `mid`** — the swapped-in value is still unexamined.
>
> And the memory peg — picture sorting laundry into three baskets one item at a time: **0 to the left basket, 2 to the right basket, and when you toss a 2 right, look again before grabbing the next.**

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new pattern title blurred in: "Sliding Window".]**

> We've now run two pointers every way they come — converging, chasing, and partitioning. But what happens when the two pointers don't just *scan* a fixed array — when the gap *between* them becomes a window that grows and shrinks to trap the answer? That's the Sliding Window pattern, and it's the next tool in your Google kit. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public void sortColors(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            int t = nums[low]; nums[low] = nums[mid]; nums[mid] = t;
            low++;
            mid++;
        } else if (nums[mid] == 1) {
            mid++;
        } else { // nums[mid] == 2
            int t = nums[mid]; nums[mid] = nums[high]; nums[high] = t;
            high--;
            // do not advance mid
        }
    }
}
```
