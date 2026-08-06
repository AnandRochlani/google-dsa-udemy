# Sort Integers by The Power Value

> **LeetCode:** 1387. Sort Integers by The Power Value · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming / memoization on a recursive sequence (top-down DP) + custom sort · **Google frequency:** medium

*If "Maximum Number of Points with Cost" was DP as *speed*, this is DP as *memory*. There's no clever recurrence to discover here — the recurrence is handed to you in the problem statement. The entire lesson is: **you've computed this value before; stop computing it again.** That's the single sentence that defines top-down DP, and this problem is the cleanest place in the course to feel it.*

---

## Problem

Every integer `x` has a **power value**: the number of steps it takes to reach `1` under this rule — if `x` is even, `x` becomes `x / 2`; if `x` is odd, `x` becomes `3 * x + 1`. (Yes, that's the Collatz sequence. The problem guarantees every number in range reaches 1.)

Given `lo`, `hi`, and `k`, take all the integers in `[lo, hi]`, sort them by **power value ascending**, breaking ties by **value ascending**, and return the `k`-th one (**1-indexed**).

**Example:** `lo = 12, hi = 15, k = 2` → `13`

Let's earn that. Walk 12 by hand:

```
12 → 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
   ↓   ↓   ↓    ↓   ↓    ↓   ↓   ↓   ↓
   1   2   3    4   5    6   7   8   9      power(12) = 9
```

Note step 3: `3` is odd, so `3 → 3*3+1 = 10`. The sequence goes **up** before it comes down. That detail matters later.

| x | chain | power |
|---|---|---|
| 12 | 12→6→3→10→5→16→8→4→2→1 | **9** |
| 13 | 13→40→20→10→5→16→8→4→2→1 | **9** |
| 14 | 14→7→22→11→34→17→52→26→13→40→…→1 | **17** |
| 15 | 15→46→23→70→35→106→53→160→80→40→…→1 | **17** |

Sorted by `(power, value)`: `[12, 13, 14, 15]`. The 2nd element is **13**. ✅

Edge case worth pinning: `lo = 1, hi = 1, k = 1` → **1**. Only one candidate, and `power(1) = 0` — zero steps, because we're already there.

**Constraints that matter:** `1 ≤ lo ≤ hi ≤ 1000`, `1 ≤ k ≤ hi - lo + 1`. Only a thousand numbers — so brute force *passes*, and that's exactly the trap. The constraint that actually bites is invisible: **chain values are not bounded by `hi`**. In `[1, 1000]` the largest intermediate value reached is **250,504** (from `x = 703`). Size your cache to `hi` and you'll index straight out of bounds. That's the bug this problem is really testing.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** the problem *tells* you the algorithm. Write `power(x)` as a loop, call it for every number in `[lo, hi]`, sort with a custom key, return index `k - 1`. Ten lines. It's correct and it passes. Say it out loud immediately — you've solved the problem in 30 seconds and now you have 40 minutes to make it good.
- **Where it hurts:** look at the table above. `13`'s chain ends `…→10→5→16→8→4→2→1`. `12`'s chain ends `…→10→5→16→8→4→2→1`. **Identical tails.** We walked `10 → 1` twice. And `14`'s chain runs into `13` after 8 steps — so we re-walk all 9 of `13`'s steps. And `15` runs into `40`, which `13` already visited. Across `[1, 1000]`, brute force takes **59,542** individual chain steps. But there are only **2,228 distinct values** ever visited. We're doing ~27× the necessary work, and every bit of it is re-deriving something we already knew.
- **The leap:** `power(x) = 1 + power(next(x))`, with `power(1) = 0`. That's a recurrence with **overlapping subproblems** — the definition of a DP. So cache it. The moment a chain touches a value that's already in the cache, it stops dead and reads the answer. Chains don't just overlap occasionally; Collatz chains **funnel** — everything eventually collapses into the same handful of tails. The cache pays for itself on the second number you evaluate.
- **The trap the leap creates:** the natural cache is an array of size `hi + 1`, because "we only care about `[lo, hi]`". Wrong. `3 * x + 1` overshoots — `15` climbs to `160` on the way down to 1, and `703` climbs to `250,504`. The cache must be keyed by *any* value the chain can reach, so use a **dict/HashMap** (or an array sized to a proven bound, if you can defend the bound). This is the single most common way candidates ship a broken version of this problem.
- **Pattern trigger:** **a value defined recursively in terms of exactly one other value, evaluated for many starting points → memoize the function, not the range.** The states aren't `[lo, hi]` — they're "every value the recursion can touch." Getting that distinction right *is* the problem.

---

## ① Brute Force

Compute every chain from scratch, independently, with a plain loop. No memory between calls.

```python
def getKth_brute(lo, hi, k):
    def power(x):
        steps = 0
        while x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            steps += 1
        return steps

    return sorted(range(lo, hi + 1), key=lambda x: (power(x), x))[k - 1]
```

**Why it's the natural first attempt:** the problem statement *is* this code. `power` is a transcription of the spec, and Python's `sorted` is stable with a tuple key that encodes "power ascending, then value ascending" exactly. Nothing here is wrong, and at `hi ≤ 1000` it runs in about a tenth of a second.

**Why it's not enough:** it re-walks ground it has already covered, over and over. Concretely, for `[12, 15]` alone: 52 chain steps taken, but only 29 distinct values ever visited. Scale to `[1, 1000]` and it's 59,542 steps for 2,228 distinct values. Nothing about the *starting point* changes what `power(10)` is — yet we recompute it every single time a chain passes through 10. In an interview, shipping this without naming the repetition is the difference between "solved it" and "hire."

**Complexity:** Time `O(n · L)` where `n = hi - lo + 1` and `L` is the average chain length (up to **178** steps in this range, at `x = 871`), plus `O(n log n · L)` if the sort re-invokes `power` — Python's `key=` calls it once per element, which is the version above. Space `O(n)` for the list.

---

## ② Optimised Solution

Turn `power` into a memoized recursion. One dict, three extra lines, and every chain that touches a known value stops immediately.

```python
def getKth(lo, hi, k):
    memo = {1: 0}                       # base case: power(1) = 0

    def power(x):
        if x in memo:                   # already solved this subproblem
            return memo[x]
        nxt = x // 2 if x % 2 == 0 else 3 * x + 1
        memo[x] = 1 + power(nxt)        # recurrence: one step + the rest
        return memo[x]

    # sort by (power ascending, value ascending); Python evaluates key once per item
    return sorted(range(lo, hi + 1), key=lambda x: (power(x), x))[k - 1]
```

**Walk the example** — `lo = 12, hi = 15, k = 2`, watching the cache fill:

| x | walk until we hit the cache | cache hit | power | new entries |
|---|---|---|---|---|
| 12 | 12→6→3→10→5→16→8→4→2 | `1` (=0) | 9 | 9 |
| 13 | 13→40→20 | **`10` (=6)** | 3 + 6 = **9** | 3 |
| 14 | 14→7→22→11→34→17→52→26 | **`13` (=9)** | 8 + 9 = **17** | 8 |
| 15 | 15→46→23→70→35→106→53→160→80 | **`40` (=8)** | 9 + 8 = **17** | 9 |

That second row is the whole lesson. `13` walks **three** steps and then collides with `10`, which `12` already paid for. It reads `6` off the shelf and returns `9` — it never touches `5, 16, 8, 4, 2, 1`. Same for `14` (crashes into `13`) and `15` (crashes into `40`). Total: 29 cached values instead of 52 walked steps, and the ratio only widens as the range grows.

Sorted by `(power, value)` → `[(9,12), (9,13), (17,14), (17,15)]` → `[12, 13, 14, 15]`, and `k = 2` gives index 1 → **13**. ✅
And `lo = 1, hi = 1, k = 1`: the range is `[1]`, `power(1) = 0` straight from the base case, index 0 → **1**. ✅

**Why it's correct:** the recurrence `power(x) = 1 + power(next(x))` is exact — one step to get to `next(x)`, then however many that value needs — and `power(1) = 0` grounds it. Memoization changes *when* a value is computed, never *what* it is, because `power(x)` depends only on `x`. The sort key `(power(x), x)` encodes the two-level ordering directly: Python compares tuples left to right, so ties on power fall through to value ascending, exactly as specified. `k` is 1-indexed, so we return index `k - 1`.

**Complexity:** Time `O(D + n log n)` where `D` is the number of **distinct** values the recursion ever touches (2,228 for `[1, 1000]`) — each is computed once and read thereafter — plus the sort. Space `O(D)` for the cache.

### The iterative version (no recursion limit, same cache)

Chains here top out at 178 steps, which fits under Python's default recursion limit of 1000 — but "fits" isn't "safe," and if the interviewer widens the range you're one `RecursionError` from a bad day. Walk the chain onto an explicit stack, then unwind it filling the cache backwards:

```python
def getKth(lo, hi, k):
    memo = {1: 0}

    def power(x):
        stack = []
        while x not in memo:            # climb until we land on something known
            stack.append(x)
            x = x // 2 if x % 2 == 0 else 3 * x + 1
        steps = memo[x]                 # the known anchor
        while stack:                    # unwind: each value is one step further out
            steps += 1
            memo[stack.pop()] = steps
        return steps

    return sorted(range(lo, hi + 1), key=lambda x: (power(x), x))[k - 1]
```

Identical results, identical complexity, zero stack risk. This is the version I'd write in a real interview — and saying *why* out loud ("recursion depth is unbounded in principle, so I'll manage the stack myself") is free signal.

### If the interviewer says "don't sort the whole range"

Fair push. You only need the `k`-th smallest, so a size-`k` heap gets you `O(n log k)` instead of `O(n log n)`:

```python
import heapq

# ... same memoized power() ...
return heapq.nsmallest(k, range(lo, hi + 1), key=lambda x: (power(x), x))[-1]
```

Worth mentioning; rarely worth writing. With `n ≤ 1000` the sort is not the bottleneck — but knowing the alternative exists is the answer they're fishing for.

---

## ③ Space Optimization

Here's the honest framing, and it's the opposite of the usual one: **the cache is not overhead — the cache *is* the optimization.** Everywhere else in this section we hunt for ways to shrink memory. Here we deliberately *spent* memory to buy time, and that trade is the entire point of the lesson.

So can you drop it back to `O(1)`? Yes — and the answer is section ①. Recompute every chain from scratch, hold nothing:

```python
def getKth_no_cache(lo, hi, k):
    def power(x):                       # O(1) auxiliary space — two variables
        steps = 0
        while x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            steps += 1
        return steps
    return sorted(range(lo, hi + 1), key=lambda x: (power(x), x))[k - 1]
```

That's `O(1)` auxiliary space (beyond the `O(n)` list you have to sort) at the cost of ~27× the chain steps. At `hi ≤ 1000` it passes. At `hi = 10^6` it doesn't. **Name the trade instead of pretending one side is strictly better** — that's the senior answer.

One thing you *cannot* do is shrink the cache to an array of size `hi + 1`:

```python
# ✗ THE BUG EVERYONE SHIPS
memo = [0] * (hi + 1)     # hi = 1000... but x = 703 climbs to 250,504.
                          # IndexError — or, in Java, ArrayIndexOutOfBoundsException.
```

`3 * x + 1` overshoots the range by design. `15` reaches `160`; `703` reaches `250,504`. The cache is keyed by *reachable values*, not by *input values*, and those are different sets. Dict, or a defended bound. There is no third option.

**Complexity:** Time `O(n · L + n log n)`, Space `O(1)` auxiliary — the no-cache variant, offered as a conscious trade, not an improvement.

---

## Java (for Java interviewers)

Java makes the trap explicit, because `int[] memo = new int[hi + 1]` compiles happily and then explodes at runtime. Use a `HashMap`. Also note `Integer[]` (not `int[]`) so `Arrays.sort` accepts a comparator.

```java
class Solution {
    // Chain values are NOT bounded by hi: 15 reaches 160, 703 reaches 250,504.
    // A fixed array sized to hi would go out of bounds — the cache must be a map.
    private final Map<Integer, Integer> memo = new HashMap<>();

    private int power(int x) {
        if (x == 1) return 0;                       // base case
        Integer cached = memo.get(x);
        if (cached != null) return cached;          // already solved
        int next = (x % 2 == 0) ? x / 2 : 3 * x + 1;
        int steps = 1 + power(next);                // power(x) = 1 + power(next(x))
        memo.put(x, steps);
        return steps;
    }

    public int getKth(int lo, int hi, int k) {
        Integer[] nums = new Integer[hi - lo + 1];
        for (int i = 0; i < nums.length; i++) nums[i] = lo + i;

        Arrays.sort(nums, (a, b) -> {
            int pa = power(a), pb = power(b);
            return pa != pb ? Integer.compare(pa, pb)   // power ascending
                            : Integer.compare(a, b);    // tie → value ascending
        });

        return nums[k - 1];                             // k is 1-indexed
    }
}
```

Java's comparator calls `power` repeatedly during the sort (unlike Python's `key=`, which calls it once per element) — which is *fine*, precisely because it's memoized. Every call after the first is a hash lookup. That's a nice thing to point out unprompted: the cache doesn't just speed up the chains, it makes the comparator cheap too.

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recompute every chain) | O(n · L + n log n) | O(1) auxiliary |
| Optimised (memoized `power` + sort) | O(D + n log n) | O(D) |
| Optimised + heap instead of sort | O(D + n log k) | O(D + k) |
| "Space-optimised" (drop the cache) | O(n · L + n log n) | O(1) auxiliary |

*(`n = hi − lo + 1` candidates; `L` = average chain length, max 178 for `hi ≤ 1000`; `D` = distinct values the recursion touches, 2,228 for `[1, 1000]`. The `O(n)` list of candidates is required output-side work in every row.)*

---

## Say it out loud (interview narration)

> *"The power value is defined recursively — `power(x)` is one step plus `power` of the next value, with `power(1) = 0` — so this is a top-down DP the moment I notice the chains overlap. And they overlap heavily: 12's chain and 13's chain both funnel through 10, so the naive version re-walks the same tail for almost every number. My first pass is the honest brute force — a loop per number, sort by the tuple `(power, value)`, return index `k − 1` because `k` is 1-indexed. Then I memoize `power` in a hash map, and every chain stops the instant it touches a cached value. One thing I want to flag explicitly: the cache **cannot** be an array sized to `hi`, because `3x + 1` overshoots — in this range `703` climbs past 250,000 — so it has to be a map keyed by any reachable value. Time is the number of distinct values touched plus the sort; space is the cache, and that's a deliberate trade — I'm buying roughly 27× fewer chain steps with a couple thousand entries. If you'd rather I not sort the full range, a size-`k` heap gets it to O(n log k). I'd also write `power` iteratively with an explicit stack rather than recursion, so chain depth can't blow the call stack."*

Before you code, ask the clarifying question that proves you read the spec: *"Ties on power break by the **value**, ascending — and `k` is 1-indexed, not 0-indexed?"* Both are stated, both are easy to get backwards, and asking costs you five seconds.

## Related / follow-ups

- **Fibonacci Number (LC 509)** — the canonical "same subproblem, computed exponentially many times" demo. If the memo idea here felt obvious, that's because this is Fibonacci wearing a Collatz costume.
- **Climbing Stairs (LC 70)** — same top-down-to-bottom-up progression, but with a recurrence you can flatten into two rolling variables. Here you *can't*, because the state space isn't a contiguous range — a great contrast to articulate.
- **Integer Replacement (LC 397)** — nearly the same operation set (`/2`, `±1`), but now you **choose** at each odd step and minimize. Memoization plus a branch: the natural next difficulty step.
- **Kth Largest Element in an Array (LC 215)** — the "don't sort the whole thing" half of this problem, taken seriously: heap vs. quickselect.
- **Top K Frequent Elements (LC 347)** — the same shape as our sort key: compute a derived score per item, then order by `(score, tiebreak)`.
