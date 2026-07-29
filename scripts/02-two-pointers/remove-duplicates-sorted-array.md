# 🎬 Recording Script — Remove Duplicates from Sorted Array
**Pattern: Two Pointers · LeetCode 26 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** two pointers — but this time both move the *same* direction (read/write).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. `seen = []` typed, then `nums = seen` — and a red banner slides in: "Wrong Answer — you were told IN PLACE".]**

> Google phone screen. *"This array is sorted. Remove the duplicates — in place — and tell me how many unique values are left."*
>
> You do the natural thing: collect the uniques into a new list, copy them back. It even gives the right numbers. And the interviewer says two words that sink it: *"In place."* No new array allowed.
>
> By the end of this video you'll have the one-pass, zero-extra-memory answer — using two pointers in a formation you haven't seen yet. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, tiles: `0  0  1  1  2`]**

> The whole problem in one line: **the array is sorted — squash each value down to a single copy, in place, keeping the order, and return how many uniques there are.**
>
> Here's our tiny example — `[0, 0, 1, 1, 2]`. Three distinct values. So the answer we're driving toward is **3**, with the front of the array reading `0, 1, 2`. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the tiles `0 0 1 1 2`. A second empty row labeled `seen` fills up as we scan. A memory counter climbs.]**

> Let's do what your brain does first. Walk the array, and every time you see a value that isn't already the last one you kept, drop it in a new list called `seen`.
>
> `0` — new, add it. Next `0` — same as last, skip. `1` — new, add. Next `1` — skip. `2` — new, add. Now `seen` is `[0, 1, 2]`. Copy it back over the front of `nums`. Return 3.
>
> **[VISUAL: the `seen` row highlighted, memory counter reading "+O(n)".]**
>
> Correct answer. But look — we built a whole second array to reorganize an array we already had in our hands. That's the memory the interviewer just forbade.

---

## 4. THE PAIN POINT + PREDICT — `2:10`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the `seen` list; red bracket labels it "O(n) extra". A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** Where's the waste? We allocated a second list just to hold uniques we could have written straight back into the original.
>
> **LEARNER:** But if I overwrite the original array while I'm still reading it, won't I clobber values I haven't looked at yet?
>
> **TEACHER:** That's the real fear, and it's a good one. Pause the video and sit with it: **the array is sorted — every duplicate sits right next to its twin. Can I use that fact to write uniques to the front without ever destroying data I still need to read?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:50`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the tiles `0 0 1 1 2`. Two pointers appear, BOTH near the front: a slow `write` and a fast `read`.]**

> **TEACHER:** Here's the leap. Because the array is sorted, we never need a `set` to detect a repeat — a duplicate is *always* the value sitting right before it. Just glance at the neighbor.
>
> So use two pointers moving the *same* direction. A slow one, `write`, marks the last spot I've locked in as unique. A fast one, `read`, scouts ahead. Think of a librarian: `read` is your finger scanning the shelf, `write` is where the next keeper book goes.
>
> **[VISUAL: `write` sits on index 0, `read` walks forward. When `read` finds a value different from `nums[write]`, `write` bumps up one and copies it.]**
>
> Whenever `read` finds a value *different* from what's at `write`, that's a fresh unique — bump `write` forward one slot and copy it there. Duplicates? `read` just walks past them.
>
> **LEARNER:** And the clobbering worry?
>
> **TEACHER:** Watch the pointers: `write` always lags *behind* `read`. So the slot we write into was already read past — the value there is dead to us. You can never overwrite something you still need.

---

## 6. THE KEY MOVE (signaling) — `4:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Slow WRITE pointer keeps uniques · fast READ pointer scans · copy only on a new value."]**

> Burn this in: **a slow write pointer holds the uniques, a fast read pointer scans ahead, and you only copy when read finds something new.**
>
> This read/write pair is *the* pattern for in-place compaction — remove element, move zeroes, all of them.

---

## 7. CODE IT — LIVE & CHUNKED — `4:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Guard the empty case, then set `write` at the front.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 0                     # nums[0..write] are the finalized uniques
```

> **[VISUAL: add chunk 2, highlight it.]** Now `read` scans from index 1 to the end.

```python
    for read in range(1, len(nums)):
        if nums[read] != nums[write]:
            write += 1
            nums[write] = nums[read]
```

> **[VISUAL: add chunk 3.]** And the count is just the last unique index, plus one.

```python
    return write + 1              # count = last index + 1
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:30`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `write = 0` — index 0 is already a unique by definition; there's nothing before it to duplicate. So we start `write` there and let `read` begin at 1.
>
> `if nums[read] != nums[write]` — this single comparison is the whole trick. Because the array is sorted, `nums[write]` is always the most recent unique we kept, so if the new value differs, it *must* be a brand-new one.
>
> **LEARNER:** Why compare against `nums[write]` and not against `nums[read - 1]`, the actual previous element?
>
> **TEACHER:** Great question — they happen to agree here, but `nums[write]` is the safer mental model: it's *the last value we committed to the output*. Comparing to the last kept unique is exactly the invariant we care about, and it generalizes to the "keep at most two" variant where `read-1` would mislead you.
>
> `write += 1` then `nums[write] = nums[read]` — advance the write cursor, drop the new value in. `write` always trails `read`, so this never eats live data.
>
> `return write + 1` — `write` is the last filled index, and indices start at zero, so the count is one more.

---

## 9. DRY-RUN THE CODE — `6:35`
*(worked example — prove it, close the loop)*

**[VISUAL: `[0, 0, 1, 1, 2]` with a trace table filling row by row; the array front updates live.]**

> Let's run the actual code on our five numbers.

| read (val) | nums[write] | new? | action | array front |
|---|---|---|---|---|
| 1 (0) | 0 | no | skip | `[0, ...]` |
| 2 (1) | 0 | yes | write=1, nums[1]=1 | `[0, 1, ...]` |
| 3 (1) | 1 | no | skip | `[0, 1, ...]` |
| 4 (2) | 1 | yes | write=2, nums[2]=2 | `[0, 1, 2, ...]` |

> Loop ends. Return `write + 1 = 3`. Front of the array reads `0, 1, 2` — exactly what we called at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:15`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n) time / O(n) space. Ours: O(n) time / O(1) space.]**

> Say it to the interviewer: *"Both are O(n) time — one scan of the array. The brute force is O(n) space because it builds a second list of uniques. Mine is O(1) space — two integer pointers, everything happens inside the input array. I return write plus one as the unique count."*
>
> Same time, better space, in place — that's the checkmark.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:50`
*(depth + honesty)*

**[VISUAL: brute-force `seen` list crossed out; ours with just two index arrows.]**

> This beat *is* the upgrade. We traded the whole O(n) `seen` list for one `write` index. Nothing else scales with `n`. It's already O(1) — there's nothing left to cut.
>
> Say it in the room: *"Sorted means duplicates are adjacent, so I don't need a set — a write pointer compacting in place gives O(1) space."* That one line shows you understood *why* the constraint mattered.

---

## 12. YOUR TURN (active recall) — `8:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Move Zeroes (LC 283)". A blank editor.]**

> Before the next video, try **Move Zeroes**. Same read/write formation — but now you compact all the *non-zero* values to the front and let the zeros fall to the back. The write pointer holds the non-zeros; read scans everything.
>
> Don't peek. Ten minutes of struggle first. That's what locks the pattern in.

---

## 13. LOCK IT IN — `8:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Sorted → duplicates are neighbors.** No set needed — check the last kept value.
> 2. **Read/write pointers = in-place compaction.** Slow write keeps, fast read scans.
> 3. **Write always trails read**, so overwriting never destroys live data.
>
> And the memory peg — when you see *"in place"* and *"keep some, drop some, order preserved,"* reach for the **slow writer, fast reader**: the librarian's finger and the keeper shelf.

---

## 14. CLIFFHANGER — `9:00`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Container With Most Water".]**

> We've squeezed from both ends, and we've raced two pointers in the same direction. But here's a nastier one: two pointers at the ends where, each step, you have to *choose* which one to move — and choose wrong and you lose the answer forever. The water-container problem. Same two pointers, a real decision. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int write = 0;
    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[write]) {
            write++;
            nums[write] = nums[read];
        }
    }
    return write + 1;
}
```
