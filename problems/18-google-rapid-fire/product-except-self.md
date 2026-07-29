# Product of Array Except Self

> **LeetCode:** 238. Product of Array Except Self · **Difficulty:** 🟡 Medium · **Pattern:** Prefix / Suffix products · **Google frequency:** medium

---

## Problem

Given an integer array `nums`, return an array `answer` where `answer[i]` is the **product of all elements except `nums[i]`**. You must solve it **without using division**, and the expected time is **O(n)**.

**Example:** `nums = [1, 2, 3, 4]` → `[24, 12, 8, 6]`
*(answer[0] = 2·3·4 = 24, answer[1] = 1·3·4 = 12, answer[2] = 1·2·4 = 8, answer[3] = 1·2·3 = 6).*

**Constraints that matter:** `n` up to `10⁵`, so O(n²) times out. The **no-division** rule is deliberate — division would make it trivial (total product ÷ nums[i]) but breaks on zeros and is explicitly banned. And the follow-up asks for **O(1) extra space** (the output array doesn't count). Those two rules define the whole problem.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct (blocked):** "compute the total product, then divide out each element." Clean, O(n) — but **division is banned**, and it fails on zeros anyway. So we need the product-except-self *without* ever dividing.
- **First instinct (allowed):** for each `i`, multiply all the other elements. That's O(n²) — for every index we re-multiply almost the whole array.
- **Where it hurts:** the product of "everything except `i`" naturally splits into **everything to the left of `i`** times **everything to the right of `i`**. Those left- and right-products are shared across indices — we keep recomputing overlapping ranges.
- **The leap — prefix and suffix products:** define `prefix[i]` = product of all elements *before* `i`, and `suffix[i]` = product of all elements *after* `i`. Then `answer[i] = prefix[i] · suffix[i]` — no division, and each of `prefix`/`suffix` is built in one linear sweep. Left sweep fills prefixes, right sweep fills suffixes.
- **The space refinement:** we don't need two extra arrays. Write the prefix products directly into `answer` on the left-to-right pass, then do a right-to-left pass carrying a single running suffix value in a variable, multiplying it into `answer[i]` as you go. O(1) extra space.
- **Pattern trigger:** *"result at i depends on everything left and everything right"* → **prefix/suffix products (or sums)**, two sweeps. The two-sweep, fold-suffix-into-output move is the reusable trick.

---

## ① Brute Force

For each index, multiply all the other elements.

```python
def product_except_self_brute(nums):
    n = len(nums)
    answer = [1] * n
    for i in range(n):
        prod = 1
        for j in range(n):
            if j != i:
                prod *= nums[j]
        answer[i] = prod
    return answer
```

**Why it's the natural first attempt:** it's the literal reading — "product of all except this one" — done independently per index, and it obeys the no-division rule.

**Why it's not enough:** the nested loop is **O(n²)**. At n = 10⁵ that's 10¹⁰ multiplications → **Time Limit Exceeded**. It recomputes overlapping left/right products for every index.

**Complexity:** Time `O(n²)`, Space `O(1)` extra.

---

## ② Optimised Solution

Two sweeps: build prefix products, then multiply by suffix products.

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

**Walk the example** `nums = [1, 2, 3, 4]`:

| i | nums | prefix (product before i) | suffix (product after i) | answer = prefix·suffix |
|---|---|---|---|---|
| 0 | 1 | 1 | 2·3·4 = 24 | 24 |
| 1 | 2 | 1 | 3·4 = 12 | 12 |
| 2 | 3 | 1·2 = 2 | 4 | 8 |
| 3 | 4 | 1·2·3 = 6 | 1 | 6 |

Result `[24, 12, 8, 6]` ✅. `prefix[0]` and `suffix[n-1]` are `1` (empty product) — the boundary that makes the ends work.

**Why it's correct:** every element except `nums[i]` is either strictly left of `i` (folded into `prefix[i]`) or strictly right of `i` (folded into `suffix[i]`), and these two sets are disjoint and complete. Their product is exactly the product of everything but `nums[i]` — no division involved, and it handles zeros naturally (a zero just makes the appropriate prefixes/suffixes zero).

**Complexity:** Time `O(n)` (three linear passes). Space `O(n)` for the two auxiliary arrays.

---

## ③ Space Optimization — the O(1)-extra trick

The output array doesn't count against the space budget, so we fold both sweeps into it and carry the suffix in a single variable.

```python
def product_except_self_optimal(nums):
    n = len(nums)
    answer = [1] * n

    # Pass 1 (left→right): answer[i] = product of everything LEFT of i.
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # Pass 2 (right→left): multiply in the product of everything RIGHT of i.
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer
```

**Trace** `[1,2,3,4]`:
- After pass 1 (prefixes): `answer = [1, 1, 2, 6]` (running `prefix`: 1→1→2→6).
- Pass 2, `suffix` starts 1:
  - i=3: `answer[3] = 6·1 = 6`; suffix → 4
  - i=2: `answer[2] = 2·4 = 8`; suffix → 12
  - i=1: `answer[1] = 1·12 = 12`; suffix → 24
  - i=0: `answer[0] = 1·24 = 24`; suffix → 24
- `answer = [24, 12, 8, 6]` ✅

**Complexity:** Time `O(n)`, Space **`O(1)` extra** (only the `prefix`/`suffix` scalars beyond the required output).

> This is the version to write in the interview: it meets the explicit O(1)-extra-space follow-up. Say *"the output doesn't count, so I store prefixes in it on the way right, then fold in suffixes with a single running variable on the way left."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space (extra) |
|---|---|---|
| Brute force (product per index) | O(n²) | O(1) |
| Prefix + suffix arrays | O(n) | O(n) |
| Prefix in output + rolling suffix | O(n) | **O(1)** |

---

## Say it out loud (interview narration)

> *"Division would be trivial but it's banned and breaks on zeros, so I think of the answer at i as everything to its left times everything to its right. I do a left-to-right pass writing the running prefix product into the output, then a right-to-left pass carrying a single suffix variable and multiplying it into each slot. The empty product at the ends is just 1. That's O(n) time and O(1) extra space beyond the output array — no division, handles zeros for free."*

## Related / follow-ups
- **Trapping Rain Water** (42) — same left-max/right-max prefix idea, then a two-pointer O(1) collapse.
- **Range Sum Query — Immutable** (303) — prefix sums instead of products.
- **Maximum Product Subarray** (152) — track running max and min products.
- **Subarray Sum Equals K** (560) — prefix sums + hash map.
