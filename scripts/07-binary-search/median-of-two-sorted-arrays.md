# 🎬 Recording Script — Median of Two Sorted Arrays (Partition Binary Search)
**Pattern: Modified Binary Search · LeetCode 4 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the value template (LC 704) and the "search the answer / monotonic feasibility" leap (Koko). This is the boss fight.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: two sorted strips `nums1 = [1,3]` and `nums2 = [2]`. A red tag: "O(log(m+n)) required." A tempting "merge them" arrow appears — then gets crossed out.]**

> This is the one that ends interviews. Two sorted arrays, find the median of the combined set, in O(log). The obvious move — merge them, grab the middle — is O(m+n), and they *explicitly* forbid it.
>
> So you're stuck: how do you find the median *without ever merging*? People flail here for twenty minutes.
>
> The escape is beautiful, and it's a pattern you already met with Koko: stop searching for a value. Search for a **cut** — the single place to slice both arrays so the left half and right half are perfectly balanced. Find that cut, and the median falls out of four numbers. By the end, this Hard will feel mechanical. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:50`
*(concrete before abstract)*

**[VISUAL: `nums1 = [1,2]`, `nums2 = [3,4]` → merged `[1,2,3,4]` with the two middles `2,3` glowing → "median = (2+3)/2 = 2.5". Then `[1,3]`,`[2]` → `[1,2,3]` → "median = 2".]**

> One line: **the median is the middle of the two arrays combined** — the middle element if the total is odd, the average of the two middles if it's even.
>
> Two tiny examples. Even total: `[1,2,3,4]`, median is `(2+3)/2 = 2.5`. Odd total: `[1,2,3]`, median is `2`. We'll solve the odd one by hand later. Note: we only ever need the numbers *near the middle* — hold that thought.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:35`
*(worked example — let them feel the waste)*

**[VISUAL: two-pointer merge of `[1,3]` and `[2]` building `[1,2,3]` cell by cell; a "work" counter ticking every element touched.]**

> Brute force: merge like the merge step of merge-sort. Pointer on each array, take the smaller, repeat. `1`, then `2`, then `3`. Now grab the middle — `2`. Correct, and honestly a fine thing to *say first* in the room.
>
> But feel the cost: we touched **every** element to build the full merged array — O(m+n) time, and O(m+n) space to hold it.
>
> **[VISUAL: arrays swell to a thousand each; the merge crawls through all 2000, but a spotlight sits only on the two middle elements.]**
>
> Here's the waste, sharp and clear: we built two thousand elements to read *two* of them. Everything except the middle was pure overhead. And it violates the O(log) demand.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: merged `[1,2,3,4]` with a vertical dashed line dropped between `2` and `3`: LEFT = {1,2}, RIGHT = {3,4}. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Forget merging. Just picture the *idea* of the combined sorted order, and drop one vertical line down the middle — call everything on the left the "left half," everything right the "right half," equal sizes. The median lives entirely at that line: the two numbers touching it.
>
> **LEARNER:** Sure, but to place that line correctly, don't I have to know the merged order first? Which puts me right back to merging.
>
> **TEACHER:** That's the trap — and the way out is the whole trick. Pause and predict: **a valid line splits the combined set so every left number is ≤ every right number. What's the *minimum* information that pins down where that line falls — do I really need all the values, or just… how many I take from each array?**

---

## 5. BUILD THE INTUITION (the aha) — `3:45`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two arrays stacked. A cut in nums1 after `i` elements; a cut in nums2 after `j`. Four border cells glow: left1 (last of nums1's left), right1 (first of nums1's right), left2, right2. A label: "j is FORCED: j = total_left − i".]**

> Here's the aha in three moves.
>
> **Move one — a cut per array.** Slice `nums1` after `i` elements and `nums2` after `j` elements. The two left pieces together form the combined left half. Four numbers sit on the border: `left1` and `right1` around `nums1`'s cut, `left2` and `right2` around `nums2`'s cut. The median depends only on these four.
>
> **Move two — `j` is not free.** The combined left half must hold a fixed count — half of everything. If I take `i` from `nums1`, the rest *must* come from `nums2`: `j = total_left − i`. So I only have **one** knob to turn: `i`. Pick `i`, and `j` is forced.
>
> **[VISUAL: a dial labeled `i` from 0 to m; turning it slides both cuts in lockstep because j tracks i.]**
>
> **Move three — the right `i` is monotonic, so binary-search it.** A cut is *valid* when the halves don't cross: `left1 <= right2` **and** `left2 <= right1` — every left number ≤ every right number. Now watch the monotonic part: if `left1 > right2`, I grabbed *too many* small elements from `nums1` — I must slide `i` **left**. If `left2 > right1`, too few — slide `i` **right**. The correct `i` sits at a boundary in `[0, m]`. That's binary search — just like Koko, we search the answer knob `i`, not the arrays.
>
> **[VISUAL: analogy — two zippers of different lengths; you slide ONE zipper pull and the other is forced to match so the teeth interlock evenly.]**
>
> Think of two zippers. You only pull one; the other's position is dictated. You slide until the teeth interlock cleanly — that clean interlock is `left ≤ right`.

---

## 6. THE KEY MOVE (signaling) — `5:30`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Don't merge — binary-search the cut `i` in the SMALLER array; `j` is forced; valid when left1≤right2 AND left2≤right1."]**

> The one line: **binary-search how many elements the left half takes from the smaller array; the other array's count is forced; the cut is valid when both cross-conditions hold.** You search a *partition*, not a value, not a merge.

---

## 7. CODE IT — LIVE & CHUNKED — `6:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> First — always search the *smaller* array. That keeps `i`'s range tiny and keeps the forced `j` in bounds.

```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1          # guarantee nums1 is the smaller one
    m, n = len(nums1), len(nums2)
    total_left = (m + n + 1) // 2            # size of combined LEFT half (+1 handles odd total)
```

> **[VISUAL: add chunk 2, highlight the inclusive bounds `[0, m]`.]** Bounds are over the *cut position* `i`, which can be 0 (take nothing from nums1) through m (take all).

```python
    lo, hi = 0, m
    while lo <= hi:
        i = lo + (hi - lo) // 2              # cut nums1 after i elements
        j = total_left - i                  # cut in nums2 is forced
```

> **[VISUAL: add chunk 3 — the four sentinel-guarded borders.]** The four border values; `±inf` handles a cut sitting at the very edge.

```python
        left1  = nums1[i - 1] if i > 0 else float('-inf')   # nothing left of cut → -inf
        right1 = nums1[i]     if i < m else float('inf')     # nothing right of cut → +inf
        left2  = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j]     if j < n else float('inf')
```

> **[VISUAL: add chunk 4 — the validity test and the median extraction.]** Check the cross-conditions; if valid, read the median off the borders.

```python
        if left1 <= right2 and left2 <= right1:      # valid cut!
            if (m + n) % 2 == 1:
                return float(max(left1, left2))      # odd: median = top of left half
            return (max(left1, left2) + min(right1, right2)) / 2   # even: avg of the two middles
        elif left1 > right2:
            hi = i - 1                               # took too many from nums1 → cut LEFT
        else:  # left2 > right1
            lo = i + 1                               # took too few from nums1 → cut RIGHT
    return 0.0                                       # unreachable for valid inputs
```

---

## 8. EXPLAIN THE CODE (the WHY) — `8:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight `total_left`'s `+1`, the sentinels, then the two cross-conditions.]**

> The lines that carry the danger:
>
> `total_left = (m + n + 1) // 2` — the `+1` is what makes the *same* formula serve odd and even totals. For an odd total it puts the extra element on the *left*, so the median is simply the top of the left half — one clean rule for both cases.
>
> The `±inf` sentinels — when a cut sits at position 0, there's nothing to its left, so `left1` is `−inf`, which is `≤` anything and never breaks the test. At position `m`, `right1` is `+inf`. This is what saves you from a swamp of empty-side `if` statements. Binary search Hard problems drown in edge cases; sentinels are the life raft.
>
> **LEARNER:** The validity test — `left1 <= right2 and left2 <= right1`. Why those *cross* pairs? Why not just `left1 <= right1` and `left2 <= right2`?
>
> **TEACHER:** Beautiful question — this is the crux. Within one array, `left1 <= right1` is *automatic* — the array is sorted, so the element before the cut is already ≤ the one after. Checking that tells you nothing. The real risk is *across* the arrays: that some element on nums1's left slipped above something on nums2's right. So you check the **cross** pairs — `left1` against `right2`, and `left2` against `right1`. Those are the only two ways the combined "left ≤ right" can fail. Nail the cross pairs and the whole partition is valid.
>
> **LEARNER:** And when `left1 > right2`, why does `i` go *down*?
>
> **TEACHER:** `left1 > right2` means nums1's left border is too big — you pulled too many elements (or too-large ones) into the left half from nums1. Shrink `i`, taking fewer from nums1, and the forced `j` grows to compensate. That's `hi = i - 1`. The mirror case `left2 > right1` means you took too few from nums1, so `lo = i + 1`. Because feasibility is monotonic in `i`, that never discards the correct cut — same guarantee as every binary search this section.

---

## 9. DRY-RUN THE CODE — `10:15`
*(worked example — prove it, close the loop)*

**[VISUAL: `nums1 = [1,3]`, `nums2 = [2]`. First the swap-to-smaller step animates: nums2 is smaller, so they swap → nums1=[2] (m=1), nums2=[1,3] (n=2). Trace table fills.]**

> Real code on `nums1 = [1,3]`, `nums2 = [2]`. Step zero: nums2 is smaller, so swap — now `nums1 = [2]` (m=1), `nums2 = [1,3]` (n=2). `total_left = (1+2+1)//2 = 2`. Search `i` in `[0, 1]`.

| lo | hi | i | j=2−i | left1 | right1 | left2 | right2 | test | action |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 2 | −∞ | 2 | nums2[1]=3 | +∞ | left2(3) ≤ right1(2)? **no** | lo = 1 |
| 1 | 1 | 1 | 1 | 2 | +∞ | nums2[0]=1 | nums2[1]=3 | 2≤3 ✓ and 1≤+∞ ✓ | **valid** |

> Total `m+n = 3` is odd → median = `max(left1, left2) = max(2, 1) = 2` → **`2.0`** ✅
>
> Watch row one: the cut took nothing from nums1, and `left2 = 3` outranked `right1 = 2` — too few from nums1, slide right. Row two interlocks cleanly. We read the answer off two of the four borders, never merging a thing. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `11:30`
*(transfer to interview)*

**[VISUAL: rows — Merge: O(m+n) time, O(m+n) space. Ours: O(log(min(m,n))) time, O(1) space.]**

> Say it: *"Merging is O(m+n) time and space. Instead I binary-search the partition of the smaller array — a cut is fixed by how many I take from nums1, `i`, and that forces `j`. I check the four border values around the two cuts; when both cross-conditions hold, the median is right there. Searching the smaller array makes it O(log(min(m,n))) time, O(1) space, and ±infinity sentinels keep the empty-edge cases clean."* That single sentence is a strong-hire answer to a Hard.

---

## 11. CAN WE USE LESS MEMORY? (space) — `12:15`
*(depth + honesty)*

**[VISUAL: brute force's O(m+n) merged array crossed out; ours computing just 4 border values.]**

> Already O(1) — we compute four borders per iteration and never build the merged array. That's the whole leap over brute force: the median is decided by **four elements straddling the cut**, so materializing all `m+n` values is pure waste.
>
> And name the bonus: by searching the *smaller* array, the bound tightens from O(log(m+n)) to **O(log(min(m,n)))** — a free improvement that *also* keeps the forced `j` in bounds. Two birds. Say it out loud; it shows you chose the search target deliberately.

---

## 12. YOUR TURN (active recall) — `12:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Kth Smallest Element in a Sorted Matrix (LC 378)". Blank editor.]**

> Before you close out this section, try **Kth Smallest Element in a Sorted Matrix**. It braids together everything here — it's an order-statistic like the median, and the clean solution *binary-searches the value range* and counts how many elements fall below each guess, straight out of the Koko playbook. If you can see it as "search the answer, count as the comparator," you've fused the whole section. Struggle before peeking.

---

## 13. LOCK IT IN — `13:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Don't merge — search a partition.** The median is four border numbers around a balanced cut.
> 2. **Search the smaller array; `j` is forced** by `total_left − i`. O(log(min(m,n))).
> 3. **Validity is the two CROSS conditions** `left1≤right2` and `left2≤right1`; `±inf` sentinels tame the edges.
>
> The peg — **find the cut, not the value.** When two sorted things must combine in O(log, binary-search the *partition*.

---

## 14. CLIFFHANGER — `14:20`
*(open loop to next lesson)*

**[VISUAL: a montage of all six section thumbnails — plain search, rotated, first-bad, 2D grid, Koko, median — snapping into one grid titled "Binary Search: 6 shapes, 1 idea".]**

> Step back and see what you built. Six problems, one idea: **the search space is monotonic, so every look throws away half.** You searched inside arrays, across a grid, over invented answer ranges, and just now for a partition. That's the entire pattern — and it's one of the highest-frequency families at Google.
>
> Next section, we leave sorted data behind and pick up a new lens: **sliding windows** — where the trick isn't halving the space, it's never re-doing work you've already done. Same obsession with waste, brand-new weapon. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public double findMedianSortedArrays(int[] nums1, int[] nums2) {
    if (nums1.length > nums2.length) { int[] t = nums1; nums1 = nums2; nums2 = t; }
    int m = nums1.length, n = nums2.length;
    int totalLeft = (m + n + 1) / 2;

    int lo = 0, hi = m;
    while (lo <= hi) {
        int i = lo + (hi - lo) / 2;          // cut in nums1
        int j = totalLeft - i;               // forced cut in nums2

        int left1  = (i > 0) ? nums1[i - 1] : Integer.MIN_VALUE;
        int right1 = (i < m) ? nums1[i]     : Integer.MAX_VALUE;
        int left2  = (j > 0) ? nums2[j - 1] : Integer.MIN_VALUE;
        int right2 = (j < n) ? nums2[j]     : Integer.MAX_VALUE;

        if (left1 <= right2 && left2 <= right1) {          // valid cut
            if (((m + n) & 1) == 1) return Math.max(left1, left2);
            return (Math.max(left1, left2) + Math.min(right1, right2)) / 2.0;
        } else if (left1 > right2) {
            hi = i - 1;                                     // cut left
        } else {
            lo = i + 1;                                     // cut right
        }
    }
    return 0.0;
}
```
