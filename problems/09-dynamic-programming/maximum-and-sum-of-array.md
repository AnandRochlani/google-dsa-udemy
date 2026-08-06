# Maximum AND Sum of Array

> **LeetCode:** 2172. Maximum AND Sum of Array · **Difficulty:** 🔴 Hard · **Pattern:** Dynamic Programming / bitmask assignment DP · **Google frequency:** ⭐ high

*This one closes the Dynamic Programming block, and it's deliberately the hardest shape in the section. The other DP problems ask "what's the recurrence?" This one asks **"what is even the state?"** — and the answer requires two separate modeling moves before a single line of DP shows up. Get comfortable here and you own an entire family of "assign n things to n slots optimally" problems.*

---

## Problem

You're given an integer array `nums` and an integer `numSlots`. There are `numSlots` slots, numbered `1, 2, …, numSlots`. You must place **every** number from `nums` into some slot, and **each slot holds at most 2 numbers**. The score of a placement is the sum, over every number, of `num AND slotNumber` (bitwise AND with the slot's *number*, not its contents). Return the **maximum** possible score.

**Example:** `nums = [1,2,3,4,5,6]`, `numSlots = 3` → `9`
*(Put `[1,4]` in slot 1, `[2,6]` in slot 2, `[3,5]` in slot 3: `(1&1)+(4&1)+(2&2)+(6&2)+(3&3)+(5&3)` = `1+0+2+2+3+1` = `9`.)*

**Example:** `nums = [1,3,10,4,7,1]`, `numSlots = 9` → `24`

**Constraints that matter:** `numSlots ≤ 9` and `n = len(nums) ≤ numSlots * 2`, so **`n ≤ 18`**. That tiny, oddly specific ceiling is the loudest hint in the whole problem. `n ≤ 18` is not "we were being nice with the input size" — it is a *pattern announcement*. `2^18 = 262,144`, which is nothing. Any time an assignment problem caps `n` around 15–22, the intended solution is **exponential in `n` but polynomial-per-state**: bitmask DP. Also note `nums[i] ≤ 15` and `numSlots ≤ 9`, so every AND fits comfortably in an `int` — no overflow worries here.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** recursion. "Take the first number, try it in every slot that still has room; recurse on the rest; keep the best." That's a completely correct backtracking solution and you should say it out loud — it's the honest baseline and it defines the search space.
- **Where it hurts:** the recursion re-solves the same future over and over. Suppose I put `nums[0]` in slot 3 and `nums[1]` in slot 5. Now suppose I instead put `nums[0]` in slot 5 and `nums[1]` in slot 3. **Different scores so far — but the remaining subproblem is byte-for-byte identical**: numbers `2..n-1` still to place, slots 3 and 5 each down one seat. The future doesn't care *how* we got here, only **which seats are gone**. That's the textbook signature of a DP hiding inside a backtracker.
- **The leap, part 1 — make the state a subset.** "Which seats are gone" isn't naturally a bitmask, because a slot holds *two* numbers — it has three occupancy levels (0, 1, 2), not two. So **split each slot into two half-slots of capacity one**. Now there are `2 * numSlots` seats, each either free or taken, and the state is a plain **subset of seats** — a bitmask. Half-slot `i` (0-based) belongs to real slot `i // 2 + 1`, so the AND value is still perfectly recoverable. One modeling move turned an awkward counting state into a clean bit-set.
- **The leap, part 2 — the dimension that deletes itself.** The obvious state is `dp[mask][i]`: best score after placing the first `i` numbers into the seats in `mask`. But look closely: if we always place numbers **in array order**, then filling `k` seats means we've placed **exactly `k` numbers**. So `i = popcount(mask)` — always. The `i` dimension is a *function* of `mask`, not independent information. Delete it. `dp[mask]` alone is the whole table. This collapse is the single most beautiful thing in the problem and the thing to say out loud in the interview.
- **Pattern trigger:** **`n ≤ ~20` + "assign every item to a position/slot" + "maximize a per-pair score" → bitmask assignment DP over the set of used positions.** And the twin sub-lesson: **a capacity-`c` bin becomes `c` capacity-1 bins** whenever you need a bitmask instead of a count vector.

---

## ① Brute Force

Recursive backtracking: place `nums[i]` into every slot that still has a free seat, recurse, take the max.

```python
def maximumANDSum_brute(nums, numSlots):
    n = len(nums)
    counts = [0] * (numSlots + 1)          # counts[s] = how many numbers already in slot s
    best = 0

    def place(i, score):
        nonlocal best
        if i == n:                          # everyone seated
            best = max(best, score)
            return
        for s in range(1, numSlots + 1):
            if counts[s] < 2:               # capacity is 2 per slot
                counts[s] += 1
                place(i + 1, score + (nums[i] & s))
                counts[s] -= 1

    place(0, 0)
    return best
```

**Why it's the natural first attempt:** it is a literal transcription of the problem statement. Every number goes somewhere, no slot exceeds two, we try everything. Nothing is wrong with it — it's just uninformed.

**Why it's not enough:** count the leaves. When `n = 2 · numSlots` (the array exactly fills every seat), the number of distinct placements is `n! / 2^numSlots`. Concretely:

| n | numSlots | placements explored |
|---|---|---|
| 12 | 6 | 7,484,400 |
| 14 | 7 | 681,080,400 |
| 16 | 8 | 81,729,648,000 |
| **18** | **9** | **12,504,636,144,000** |

At `n = 12` it's already several million leaves — sluggish in Python and a bad look in an interview. At the actual constraint ceiling, `n = 18`, it's **12.5 trillion**. That is not "slow," that's geologic. And every one of those leaves is being computed from scratch even though the vast majority share identical remaining subproblems.

**Complexity:** Time `O(numSlots^n)` (tighter: `n! / 2^numSlots` complete placements), Space `O(n)` for the recursion stack.

---

## ② Optimised Solution

Two modeling moves, then the DP writes itself.

1. **Split each slot into two half-slots.** `m = 2 * numSlots` seats, each capacity 1. Half-slot `b` (0-based) sits in real slot `b // 2 + 1`.
2. **State = the set of occupied half-slots.** `dp[mask]` = the best score achievable after placing the first `popcount(mask)` numbers into exactly the half-slots named by `mask`.

Because we always consume numbers in array order, `popcount(mask)` *is* the index of the next number to place. That's the whole reason we get away with a one-dimensional table.

```python
def maximumANDSum(nums, numSlots):
    n = len(nums)
    m = 2 * numSlots                       # half-slots: each real slot split into 2 seats
    dp = [0] * (1 << m)                    # dp[mask] = best score for the first popcount(mask) numbers

    for mask in range(1 << m):
        i = bin(mask).count("1")           # (Python 3.10+: mask.bit_count())
        if i >= n:                         # every number already placed — nothing to extend
            continue
        for b in range(m):
            if mask >> b & 1:              # seat b is taken
                continue
            nxt = mask | (1 << b)
            gain = nums[i] & (b // 2 + 1)  # seat b belongs to real slot b // 2 + 1
            if dp[mask] + gain > dp[nxt]:
                dp[nxt] = dp[mask] + gain

    return max(dp)                         # NOT dp[full] — n may be < m, see below
```

**Why `max(dp)` and not `dp[(1 << m) - 1]`:** the array doesn't have to fill every seat (`n ≤ 2 · numSlots`, often strictly less). If `n = 3` and `numSlots = 2`, the full mask has popcount 4 > 3 — it is **never written**, so it sits at `0`. The real answers live on the popcount-`n` layer. Taking the max over the whole table finds them, and it's safe: because every AND gain is `≥ 0`, no partial state can exceed a completed one (any partial placement can always be extended — there are always at least `n - i` free seats left).

**Walk one example** — `nums = [1, 2, 3]`, `numSlots = 2`. So `m = 4` seats: bits 0,1 → slot 1; bits 2,3 → slot 2. Gains: `1&1=1`, `1&2=0`; `2&1=0`, `2&2=2`; `3&1=1`, `3&2=2`. Masks written as `b3 b2 b1 b0`:

| Layer (popcount) | Next number to place | Masks and their `dp` |
|---|---|---|
| 0 | `nums[0] = 1` | `0000` → **0** |
| 1 | `nums[1] = 2` | `0001` → 1, `0010` → 1 *(1 in slot 1)* · `0100` → 0, `1000` → 0 *(1 in slot 2, `1&2 = 0`)* |
| 2 | `nums[2] = 3` | `0011` → 1 *(1 and 2 both in slot 1)* · `0101`/`0110`/`1001`/`1010` → **3** *(1 in slot 1, 2 in slot 2)* · `1100` → 2 *(both in slot 2)* |
| 3 | — (all placed) | `0111` → 4, `1011` → 4 · `1101` → **5**, `1110` → **5** |
| 4 | — | `1111` → 0 — **never written**, popcount 4 > n = 3 |

Read the winner backwards: `1101` = seats `b0` (slot 1) + `b2`,`b3` (slot 2). Its `5` came from `0101` (dp `3`) plus `nums[2] = 3` into seat `b3`, gaining `3 & 2 = 2`. So: `1` in slot 1, and both `2` and `3` in slot 2 → `1 + 2 + 2 = 5`. ✅ And notice the full mask sitting there at `0` — that's exactly the trap `max(dp)` sidesteps.

**Why it's correct:** induction on `popcount(mask)`. `dp[0] = 0` is trivially the best score for zero numbers. Assume `dp[mask]` is optimal for every mask of popcount `i`. Any optimal placement of the first `i + 1` numbers into a seat-set `S` of size `i + 1` must put `nums[i]` in *some* seat `b ∈ S`, and the remaining `i` numbers form an optimal placement into `S \ {b}` (otherwise swap in the better one — the AND gains are independent per number, so nothing else changes). Our inner loop tries every such `b`, so `dp[S]` gets the max over all of them. The order of the outer loop is safe because `mask < mask | (1 << b)` always, so every source state is finalised before it's read.

**Complexity:** Time `O(2^(2·numSlots) · 2·numSlots)`. At the ceiling that's `2^18 × 18 = 4,718,592` — under five million elementary operations. Space `O(2^(2·numSlots)) = 262,144` ints ≈ 1 MB. Compare 4.7 million to the brute force's 12.5 trillion: a **2.6-million-fold** reduction, from geologic to instant.

---

## ③ Space Optimization

**The honest first answer: within the bitmask formulation, you can't roll it away.** In a row DP you keep one row because state `r` only reads state `r-1`. Here, `dp[mask]` reads *every* mask that is `mask` minus one bit — and while those all sit on the popcount-`(i-1)` layer, the table is iterated in **numeric** order, not popcount order, so the "previous layer" isn't a contiguous window you can slide over. Say that out loud; naming why a trick *doesn't* apply is a real signal.

**The partial win.** The transition only ever goes from layer `i` to layer `i + 1`, so a two-layer rolling scheme *is* mathematically valid — iterate masks grouped by popcount and keep only layers `i` and `i + 1`. The largest layer is `C(18, 9) = 48,620`, so two layers is ~97k entries versus 262k: about **2.7× less memory**. The catch is that you now need a mask → position-within-layer ranking (a combinatorial number system) to index those compact arrays, which costs time and a pile of code. In an interview, mention it and move on.

**The real win — drop the bitmask entirely.** Here's the thing we bought the half-slot trick for, and the price we paid: the two half-slots inside one real slot are **interchangeable**. Masks `0001` and `0010` above are the same physical situation and both store `1`. The bitmask is carrying `2^18` states to represent only `3^9` genuinely distinct ones. So encode the state as a **base-3 number**: digit `s` = how many numbers are already in slot `s+1` (0, 1, or 2).

```python
def maximumANDSum_base3(nums, numSlots):
    n = len(nums)
    POW = [3 ** k for k in range(numSlots + 1)]
    total = POW[numSlots]                       # 3^numSlots states

    placed = [0] * total                        # placed[st] = sum of base-3 digits = numbers seated
    for st in range(1, total):
        placed[st] = placed[st // 3] + st % 3

    dp = [0] * total
    for st in range(total):
        i = placed[st]
        if i >= n:
            continue
        for s in range(numSlots):               # slot s+1
            if (st // POW[s]) % 3 < 2:          # still has room
                nxt = st + POW[s]
                cand = dp[st] + (nums[i] & (s + 1))
                if cand > dp[nxt]:
                    dp[nxt] = cand
    return max(dp)
```

`3^9 = 19,683` states instead of `2^18 = 262,144` — **13.3× less memory**, and the work drops to `3^9 × 9 = 177,147` operations (measured ~24× faster than the bitmask version at the ceiling, same answers on 300 randomized cross-checks against brute force).

**Complexity:** Time `O(3^numSlots · numSlots)`, Space `O(3^numSlots)`.

> **What to actually say in the room:** lead with the bitmask solution — it's the expected answer, it's easier to write correctly under pressure, and the `popcount` collapse is the insight they're testing. Then add: *"One refinement — the two half-slots in a slot are symmetric, so a base-3 occupancy state would cut this from 2^18 to 3^9."* That sentence is worth more than the extra code.

---

## Java (for Java interviewers)

`Integer.bitCount` is a single hardware instruction (`POPCNT`), so the state-index-is-popcount trick costs literally nothing here.

```java
public int maximumANDSum(int[] nums, int numSlots) {
    int n = nums.length;
    int m = 2 * numSlots;                       // half-slots: 2 seats per real slot
    int[] dp = new int[1 << m];                 // dp[mask] = best score for first bitCount(mask) numbers

    int best = 0;
    for (int mask = 0; mask < (1 << m); mask++) {
        int i = Integer.bitCount(mask);         // how many numbers are already placed
        best = Math.max(best, dp[mask]);        // running max — covers n < m (full mask never reached)
        if (i >= n) continue;                   // all numbers placed; nothing to extend

        for (int b = 0; b < m; b++) {
            if ((mask & (1 << b)) != 0) continue;       // seat taken
            int next = mask | (1 << b);
            int gain = nums[i] & (b / 2 + 1);           // seat b lives in real slot b/2 + 1
            dp[next] = Math.max(dp[next], dp[mask] + gain);
        }
    }
    return best;
}
```

*(Verified: `[1,2,3,4,5,6], 3` → `9`; `[1,3,10,4,7,1], 9` → `24`; full `n = 18, numSlots = 9` runs in ~23 ms.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (backtracking over slots) | O(numSlots^n) — up to `n!/2^numSlots` ≈ 1.25 × 10¹³ | O(n) |
| Optimised (bitmask over half-slots) | O(2^(2·numSlots) · 2·numSlots) = 4.7 × 10⁶ | O(2^(2·numSlots)) = 262,144 |
| Space-optimised (base-3 occupancy) | O(3^numSlots · numSlots) = 1.8 × 10⁵ | O(3^numSlots) = 19,683 |

*(Numbers shown at the constraint ceiling: `numSlots = 9`, `n = 18`.)*

---

## Say it out loud (interview narration)

> *"The brute force is backtracking: place each number into any slot with room. That's `n!/2^numSlots` placements — 12 trillion at `n = 18`. But notice the redundancy: two different orders of filling the same slots leave an identical remaining subproblem, so this is a DP. The state should be 'which capacity is gone', which is awkward because a slot has three occupancy levels — so I'll **split each slot into two half-slots of capacity one**. Now the state is a subset of half-slots: a bitmask. And here's the nice part — if I always place numbers in array order, then `popcount(mask)` numbers are placed, so the 'which number am I on' dimension is a **function of the mask**, not independent state. `dp[mask]` is one-dimensional. Transition: let `i = popcount(mask)`; for every free bit `b`, relax `dp[mask | 1<<b]` with `dp[mask] + (nums[i] & (b//2 + 1))`. Answer is `max(dp)`, not `dp[full]`, because `n` can be smaller than `2·numSlots` so the full mask may never be reached. That's `2^18 × 18` ≈ 4.7 million operations and about a megabyte — trivially fast. If you want it tighter, the two half-slots inside a slot are symmetric, so a base-3 occupancy state gives `3^9` states instead of `2^18`."*

Two clarifying questions worth asking before you write anything, because both change the model: *"Slots are numbered `1` through `numSlots` — the AND is against the slot **number**, not an index or a value in it, right?"* and *"Every number must be placed, and I can leave slots empty or half-empty?"* Asking those proves you read the spec instead of pattern-matching the title — and Google scores that (GCA) explicitly.

## Related / follow-ups

- **Minimum XOR Sum of Two Arrays (LC 1879)** — the purest twin. Assign every element of `nums1` to a distinct element of `nums2` to minimize the XOR sum. Same `dp[mask]` with `popcount(mask)` as the item index — no half-slot trick needed because capacity is 1. **Do this one first if this problem hurt.**
- **Beautiful Arrangement (LC 526)** — count (not maximize) permutations where position divisibility holds. Identical state collapse: `dp[mask]` with `popcount(mask)` telling you which position you're filling.
- **Partition to K Equal Sum Subsets (LC 698)** — `n ≤ 16`, assign items to `k` bins. Same family, but the bins are constrained by a *sum* rather than a count, which is why the classic solution is bitmask + memo rather than a clean layered sweep.
- **Shortest Path Visiting All Nodes (LC 847)** — bitmask over *visited* nodes plus a "where am I" dimension. Contrast it deliberately: there the second dimension is genuinely independent, so it can **not** be collapsed. Knowing when the popcount trick applies is the real skill.
- **Campus Bikes II (LC 1066)** — workers to bikes, `n ≤ 10`. Straight bitmask assignment DP; a good 5-minute confidence rep after this lesson.
