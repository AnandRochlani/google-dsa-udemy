# 🎬 Recording Script — 3Sum
**Pattern: Two Pointers · LeetCode 15 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the "pair with target sum" two-pointer squeeze (previous lesson).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. Three nested `for` loops already typed. A LeetCode "Time Limit Exceeded — test case 47/313" banner slides in red.]**

> You get asked this in an Google phone screen: *"Find all the triplets that add up to zero."*
>
> You write the obvious thing — three loops, check every combo. It works on the example. You hit run… and it dies. Time Limit Exceeded.
>
> Here's the thing: the *idea* was fine. The problem is it does a mountain of work it doesn't need to. By the end of this video, you'll turn those three loops into two — and you'll see exactly *why* the trick works, not just memorize it. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, six number tiles: `-1  0  1  2  -1  -4`]**

> The whole problem in one line: **find every unique group of three numbers that add up to zero.**
>
> And here's our tiny example — just six numbers. Keep your eye on these; we'll solve this exact set two different ways, by hand, so you feel the difference.
>
> Two triplets in here add to zero. Don't hunt for them yet — just hold that there are two.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the six tiles. Three colored markers i, j, k. A "comparisons" counter starting at 0, top-right.]**

> Let's do what your brain does first: check every possible trio.
>
> Marker `i` on the first number, `-1`. Now `j` and `k` walk every pair after it. `-1 + 0 + 1`? Zero! One found. `-1 + 0 + 2`? One. `-1 + 1 + 2`? Two. Keep going… every combination.
>
> **[VISUAL: markers jump through combos, counter ticking up fast — 5, 9, 14, 18…]**
>
> Then `i` moves to `0`, and `j`,`k` sweep *all over again*. Then `i` moves to `1`… again.
>
> Watch that counter. Six numbers, and we're already past 15 checks. Now imagine 3,000 numbers. That's this many operations —
>
> **[VISUAL: counter morphs into "≈ 27,000,000,000"]**
>
> Twenty-seven *billion*. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight `j` and `k` re-scanning the same tail region in a loop. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So where's the waste? Look at what `j` and `k` are doing: for every `i`, they blindly re-scan the whole rest of the list, trying every pair from scratch. They never *use* anything they learned.
>
> **LEARNER:** Okay but — the numbers are just in random order. What is there to even use? It kind of *has* to try everything, no?
>
> **TEACHER:** That's the exact instinct we have to break. Pause the video for a second and sit with it: **what could we do to this list *first* that would suddenly tell `j` and `k` which direction to move — instead of guessing every pair?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the tiles animate into sorted order: `-4  -1  -1  0  1  2`]**

> **TEACHER:** Here's the clue: nothing said the array was sorted — so let's *sort it ourselves*. That's cheap, and watch what it unlocks.
>
> **LEARNER:** Wait, won't sorting make it *slower*? That's extra work we didn't have before.
>
> **TEACHER:** Feels that way — but hold that thought, because the sort costs us n-log-n once, and it's about to save us a whole *dimension* of work. Watch.
>
> Now the trick from last lesson. Remember "pair with a target sum"? On a *sorted* list, you put one finger at each end and squeeze: sum too big, move the right finger down; too small, move the left finger up. No re-scanning — the sorted order tells you which way to go.
>
> So here's the leap: **3Sum is just 2Sum with one number pinned down.**
>
> **[VISUAL: pin an anchor on the first `-1`. Two "hands" (left/right pointers) appear over the rest of the list.]**
>
> Pin the anchor on `-1`. Now I need two numbers from the rest that add up to… **positive 1** — because -1 plus 1 is zero. And finding two numbers that hit a target in a sorted list? That's the two-finger squeeze. We already know it. It's O(n), not re-checking everything.
>
> Let's trace it. Anchor `-1`, target `1`. Left hand on `-1`, right hand on `2`. `-1 + 2 = 1`. Hit! That's the triplet `-1, -1, 2`. Move both hands in. Now `0 + 1 = 1`. Hit again! `-1, 0, 1`. There are our two triplets — and look at the counter.
>
> **[VISUAL: comparisons counter this time crawls — 3, 4, 5. Side-by-side with the old "27 billion".]**
>
> Same answer. A fraction of the work.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Sort → fix one number → two-pointer the rest."]**

> Burn this one line into memory: **sort, fix one number, then two-pointer the rest.**
>
> That's the entire pattern. Every "find numbers that sum to a target" problem — 3Sum, 4Sum, all of them — is this same move, just with more anchors.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in small pieces. First, sort, and set up where the answers go.

```python
def three_sum(nums):
    nums.sort()
    n = len(nums)
    result = []
```

> **[VISUAL: add chunk 2, highlight it.]** Now loop the anchor — each number gets a turn being the pinned one.

```python
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue          # skip a repeated anchor — we already did it
```

> **[VISUAL: add chunk 3.]** Here's the two-finger squeeze on the rest of the list.

```python
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
```

> **[VISUAL: add chunk 4, highlight the two inner whiles.]** And the part everyone forgets — skipping duplicate hands so we don't list the same triplet twice.

```python
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1     # sum too small → need bigger → move left up
            else:
                right -= 1    # sum too big → need smaller → move right down
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `nums.sort()` — this is the whole foundation. Without sorting, the two-finger logic is meaningless; "move toward a bigger number" only makes sense when they're in order.
>
> `range(n - 2)` — the anchor stops two from the end, because we always need at least two numbers to its right to make a trio.
>
> `if nums[i] == nums[i-1]: continue` — if this anchor value is the same as the last one, we'd generate the exact same triplets again. Skip it. This is *why* sorting also solves duplicates for free — equal values sit next to each other.
>
> The `total < 0` / `total > 0` branches — this is the squeeze. Too small? The only way up is a bigger number, so `left` moves right. Too big? `right` moves left. Sorted order guarantees that's the right direction.
>
> **LEARNER:** Quick one — the `while left < right`. Why strict less-than? Why not `<=`?
>
> **TEACHER:** Sharp catch. If `left` equals `right`, they're pointing at the *same* number — and we'd be adding one element to itself as if it were two different picks. That's not a real triplet. Strict `<` keeps the two hands on two distinct numbers.
>
> And those two inner `while` loops — after a hit, we shove both hands past any duplicates, so `-1, 0, 1` never gets printed twice.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: sorted `[-4, -1, -1, 0, 1, 2]` with a trace table filling row by row.]**

> Let's run the actual code on our six numbers and watch it land.

| i (val) | left,right (vals) | total | action |
|---|---|---|---|
| 0 (−4) | 1,5 (−1,2) | −3 | too small → left++ … never reaches 4 → none |
| 1 (−1) | 2,5 (−1,2) | 0 | **hit → [−1,−1,2]**, move both in |
| 1 (−1) | 3,4 (0,1) | 0 | **hit → [−1,0,1]**, move both in → cross |
| 2 (−1) | — | — | duplicate anchor → **skip** |
| 3 (0) | 4,5 (1,2) | 3 | too big → right-- → cross → none |

> Output: `[[-1,-1,2], [-1,0,1]]`. Exactly the two we said were hiding in there at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n³). Ours: O(n²). Sort: O(n log n), "doesn't dominate".]**

> **TEACHER:** Say it the way you would to the interviewer: *"Brute force is O(n cubed). Sorting is n-log-n, which is basically free here. Then for each of the n anchors I do a linear two-pointer scan — so O(n squared) overall. Space is O(1) extra, ignoring the output."*
>
> And remember the worry about sorting making it slower? There's your answer: n-log-n sits *underneath* n-squared — it doesn't even show up in the final Big-O. We paid a little to erase a whole nested loop.
>
> That sentence — brute force, then the improvement, then the cost — is exactly what earns the checkmark.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: brute-force version with a `set()` for dedup, crossed out; ours with no set.]**

> Quick but important. The brute force needed a hash set just to kill duplicate triplets — extra memory *and* hashing overhead.
>
> We don't. Because we sorted, duplicates are neighbors, so a couple of skip-lines dedup in place. No set. O(1) extra space.
>
> Say that out loud in the room: *"Sorting doesn't just enable the two pointers — it lets me dedup by skipping neighbors, so I drop the hash set entirely."* That's a strong-hire detail.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → 3Sum Closest (LC 16)". A blank editor.]**

> Before the next video, try **3Sum Closest**. Same setup — sort, fix one, two-finger the rest — but instead of hitting exactly zero, you track the sum *closest* to a target.
>
> Don't watch the solution first. Struggle with it for ten minutes. That struggle is literally what moves this from "I saw it" to "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Sorting is the unlock** — it enables both the squeeze *and* free dedup.
> 2. **k-Sum = fix one, then (k−1)-Sum.** 3Sum is 2Sum with an anchor.
> 3. **Skip duplicate neighbors** — for the anchor and both pointers.
>
> And the memory peg — when you see *"find numbers that sum to a target"* and the list can be sorted, your hand should already be moving: **pin one, squeeze the rest.**

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Container With Most Water".]**

> Two pointers just killed a cubic problem. But so far we've always squeezed *inward* from the ends. What if moving the pointers the wrong way loses the answer — where you have to *choose* which one to move based on which is smaller? That's the next one: the water-container problem. Same two pointers, sneakier decision. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    int n = nums.length;
    for (int i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int left = i + 1, right = n - 1;
        while (left < right) {
            int total = nums[i] + nums[left] + nums[right];
            if (total == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                left++; right--;
                while (left < right && nums[left] == nums[left - 1]) left++;
                while (left < right && nums[right] == nums[right + 1]) right--;
            } else if (total < 0) left++;
            else right--;
        }
    }
    return result;
}
```
