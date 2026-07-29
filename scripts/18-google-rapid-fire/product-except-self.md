# 🎬 Recording Script — Product of Array Except Self

**Pattern: Prefix / Suffix products · LeetCode 238 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this seeds the prefix/suffix idea reused in Trapping Rain Water.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: array [1,2,3,4]. A hand reaches for the "obvious" solution — multiply everything, divide by each element — then a big red ✗ slams down: "NO DIVISION."]**

> Here's an Google favorite with a trap built into the rules. *"Return an array where each slot is the product of all the other elements."* Easy — multiply everything, divide out each element. Done.
>
> Except the problem **bans division.** And there's a reason beyond cruelty: division breaks the instant there's a zero in the array. So you're forced to find the answer *without ever dividing* — and the technique you discover is one of the most reused patterns in interviews.
>
> By the end you'll do it in O(n) time and O(1) extra space, no division. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below: nums [1,2,3,4] → answer [24,12,8,6], each mapping drawn.]**

> One line: **`answer[i]` = the product of every element except `nums[i]`** — no division, and O(n) time.
>
> Tiny example — `[1, 2, 3, 4]`. `answer[0]` = 2·3·4 = 24. `answer[1]` = 1·3·4 = 12. Then 8, then 6. Result `[24, 12, 8, 6]`. Keep these four numbers up; we'll build that answer two ways.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: for each index i, a loop multiplies all the OTHER elements; overlapping ranges get re-multiplied.]**

> The division-free brute force: for each index, loop over everyone else and multiply.
>
> `answer[0]`: skip index 0, multiply 2·3·4 = 24. `answer[1]`: skip index 1, multiply 1·3·4 = 12. `answer[2]`: 1·2·4 = 8. Each answer is its own full pass.

**[VISUAL: highlight that computing answer[0] and answer[1] both re-multiply 3 and 4 — overlapping work in red.]**

> It obeys the no-division rule, and it's correct. But it's a nested loop — **O(n²)**. At 100,000 elements that's ten billion multiplications. And look at the overlap: computing slot 0 and slot 1 both re-multiply `3` and `4`. We keep recomputing overlapping ranges.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Split the array at index i into a LEFT region and a RIGHT region, colored. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is recomputing overlapping products. But here's the reframe that unlocks it: the "product of everything except `i`" naturally splits into two pieces — **everything to the left of `i`**, times **everything to the right of `i`.**
>
> **LEARNER:** And those left-products and right-products are *shared* between neighboring indices — like, the left-of-index-3 product contains the left-of-index-2 product.
>
> **TEACHER:** Exactly the observation. Pause and predict: **if the answer at `i` is (product of everything left) times (product of everything right), how many passes do I need to precompute all the lefts and all the rights?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it)*

**[VISUAL: two rows under the array — "prefix" (product before i) built left-to-right, "suffix" (product after i) built right-to-left. answer[i] = prefix[i] × suffix[i].]**

> **TEACHER:** Define two things. `prefix[i]` = the product of all elements *before* `i`. `suffix[i]` = the product of all elements *after* `i`. Then:
>
> `answer[i] = prefix[i] × suffix[i]` — no division anywhere.
>
> And each of those builds in a **single sweep**. Left-to-right, carry a running product — that fills every `prefix`. Right-to-left, carry a running product — that fills every `suffix`. Then multiply them slot by slot.
>
> **[VISUAL: prefix = [1,1,2,6], suffix = [24,12,4,1], product = [24,12,8,6]. The ends are 1 — highlight "empty product = 1".]**
>
> One subtlety that makes the ends work: `prefix[0]` is 1 and `suffix[last]` is 1 — the **empty product**. Nothing is to the left of the first element, and the product of nothing is 1. That's the boundary that keeps the formula clean. Two sweeps, done — O(n).

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "answer[i] = (product of everything left) × (product of everything right), built in two sweeps."]**

> The key move: **when the result at `i` depends on everything left AND everything right, precompute prefix and suffix in two sweeps.** It's division-free because you're *multiplying two partial products*, never dividing out one element. This prefix/suffix idea generalizes way past products — sums, maxes, you name it.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: the two-array version first — it mirrors the intuition directly.]**

> Two-array version first, straight from the picture.

```python
def product_except_self(nums):
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n

    for i in range(1, n):                 # prefix[i] = product of nums[0..i-1]
        prefix[i] = prefix[i - 1] * nums[i - 1]

    for i in range(n - 2, -1, -1):        # suffix[i] = product of nums[i+1..n-1]
        suffix[i] = suffix[i + 1] * nums[i + 1]

    return [prefix[i] * suffix[i] for i in range(n)]
```

> Clean and correct — but two extra arrays. The follow-up asks for **O(1) extra space**, so let's collapse it. The output array doesn't count against the budget, so we fold both sweeps into it and carry the suffix in a single variable.

```python
def product_except_self_optimal(nums):
    n = len(nums)
    answer = [1] * n

    prefix = 1                            # pass 1: answer[i] = product LEFT of i
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    suffix = 1                            # pass 2: multiply in product RIGHT of i
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the optimal version; spotlight the order of "read then update" in each pass.]**

> The two-array version is obvious; the O(1) one has a subtlety worth savoring.
>
> Pass one: `answer[i] = prefix` *then* `prefix *= nums[i]`. Order matters — we write the running product **before** folding in the current element, so `answer[i]` holds everything strictly to the *left*, not including `nums[i]`.
>
> Pass two: `answer[i] *= suffix` *then* `suffix *= nums[i]`. Same discipline — multiply in the running right-product before including the current element.
>
> **LEARNER:** Wait — why does reading before updating give me "everything except i"? Why doesn't `nums[i]` sneak into its own answer?
>
> **TEACHER:** Because at slot `i`, we assign `answer[i]` while `prefix` still only contains elements `0` through `i-1` — we haven't multiplied `nums[i]` in yet. Then we update `prefix`. Same on the way back with `suffix`. So `nums[i]` is folded into the running product *only after* it's done contributing to its neighbors, never into its own slot. Read-then-update is the whole trick.

---

## 9. DRY-RUN THE CODE — `7:50`
*(worked example — prove it)*

**[VISUAL: answer array evolving across both passes.]**

> Trace `[1,2,3,4]`.
>
> **Pass 1** (prefixes into `answer`), running `prefix` 1→1→2→6:

| i | answer[i] = prefix | prefix becomes |
|---|---|---|
| 0 | 1 | 1·1 = 1 |
| 1 | 1 | 1·2 = 2 |
| 2 | 2 | 2·3 = 6 |
| 3 | 6 | 6·4 = 24 |

> After pass 1: `answer = [1, 1, 2, 6]`.
>
> **Pass 2** (fold in suffixes), running `suffix` starts at 1:
> - i=3: `answer[3] = 6·1 = 6`; suffix → 4
> - i=2: `answer[2] = 2·4 = 8`; suffix → 12
> - i=1: `answer[1] = 1·12 = 12`; suffix → 24
> - i=0: `answer[0] = 1·24 = 24`
>
> `answer = [24, 12, 8, 6]` ✅. Exactly our target — no division ever happened.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: three rows — Brute O(n²)/O(1); Prefix+suffix arrays O(n)/O(n); Rolling O(n)/O(1) extra.]**

> Out loud: *"Brute force is O(n²). Prefix and suffix arrays give O(n) time but O(n) extra space. Folding the prefixes into the output and carrying the suffix in one variable keeps O(n) time at O(1) extra space — the output doesn't count against the budget."*
>
> That O(1)-extra version is the one to write, because the problem *explicitly* asks for it in the follow-up.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:40`
*(depth + honesty)*

**[VISUAL: the two auxiliary arrays crossed out; only the output array + two scalars remain.]**

> We already did the space optimization — it *is* the optimal solution. The two auxiliary arrays collapse into the output array plus two scalar variables, `prefix` and `suffix`. That's **O(1) extra**, the minimum, since we obviously need the output itself.
>
> Say it in the room: *"The output doesn't count, so I store prefixes in it on the way right, then fold in suffixes with a single running variable on the way left — O(n) time, O(1) extra space, and it handles zeros for free."* That last bit matters — a zero in the input just makes the appropriate prefixes or suffixes zero, no special-casing, which is exactly why division was banned.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Trapping Rain Water (LC 42)".]**

> Before the next video, try **Trapping Rain Water** — and yes, it uses this *exact* prefix/suffix idea. Water above each bar depends on the tallest wall to its left and the tallest to its right — a prefix-max and a suffix-max. Same two-sweep structure, then a two-pointer collapse to O(1) space. If you own this lesson, you're halfway through that Hard already.
>
> Fifteen minutes, no peeking.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Result depends on left-and-right → prefix/suffix in two sweeps.**
> 2. **Multiplying two partial products avoids division** — and handles zeros naturally.
> 3. **Fold prefixes into the output, carry the suffix in one variable** → O(1) extra space. Read before update.
>
> The memory peg — *"everything except me = everyone on my left, times everyone on my right."*

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: a blurred grid of 1s and 0s forming island shapes.]**

> We've been sweeping across one-dimensional arrays. Next, the data goes 2-D — a grid of land and water — and the question becomes "how big is the largest island?" The prefix trick won't help; we need to *explore* connected regions. Enter flood fill. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] answer = new int[n];

    int prefix = 1;                       // product of everything to the left
    for (int i = 0; i < n; i++) {
        answer[i] = prefix;
        prefix *= nums[i];
    }

    int suffix = 1;                       // product of everything to the right
    for (int i = n - 1; i >= 0; i--) {
        answer[i] *= suffix;
        suffix *= nums[i];
    }
    return answer;
}
```
