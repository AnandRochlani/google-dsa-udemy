# Maximum Split of Positive Even Integers

> **LeetCode:** 2178. Maximum Split of Positive Even Integers · **Difficulty:** 🟡 Medium · **Pattern:** Greedy math construction · **Google frequency:** medium

---

## Problem

You're given an integer `finalSum`. Split it into a list of **distinct positive even integers** that add up to exactly `finalSum`, and make that list **as long as possible**. Return any list achieving the maximum length. If no such split exists, return an empty list.

Three words carry all the weight: **distinct** (no repeats), **positive even** (2, 4, 6, … — never 0, never odd), and **maximum** (you're optimising the *count* of parts, not their values). Any maximal list is accepted — order doesn't matter.

**Example:** `finalSum = 12` → `[2, 4, 6]` *(three distinct evens summing to 12; you can't do four, because the four smallest distinct evens are 2+4+6+8 = 20 > 12)*

**Example:** `finalSum = 28` → `[2, 4, 6, 16]` *(four parts. 2+4+6+8 = 20 fits, but 2+4+6+8+10 = 30 overshoots — so four is the ceiling, and the leftover 8 gets folded into the last part)*

**Example:** `finalSum = 7` → `[]` *(7 is odd; any sum of even numbers is even, so it's impossible)*

**Constraints that matter:** `1 <= finalSum <= 10^10`. That upper bound is the whole story. It's far past 32-bit `int` territory in Java — you need `long` — and it obliterates any idea of enumerating subsets of even numbers. There are ~5×10⁹ candidate evens below 10¹⁰; a search over their subsets isn't slow, it's *never finishing*. The bound also quietly tells you the answer is small: as we'll see, it can hold at most about **√finalSum ≈ 10⁵** numbers.

---

## 🧠 Intuition — how you'd actually arrive at this

- **The gate, before anything else:** a sum of even numbers is **always even**. So if `finalSum` is odd, the answer is `[]` — no search required, no cleverness required. Notice this in the first ten seconds and say it out loud; it's the clarifying-question moment that separates "started coding immediately" from "thought first."
- **First instinct:** treat it as a subset-sum. Line up 2, 4, 6, 8, … and search for the largest subset summing to `finalSum`. Correct, and completely dead — the search space is exponential in a candidate list of billions.
- **Where it hurts:** the search is spending all its effort choosing *which* evens, when the objective doesn't care about values at all. You're maximising **how many parts**, and every part costs you budget. That's the mismatch.
- **The leap:** if you want the **most** parts, make each part as **small** as possible. The smallest distinct positive even is 2, then 4, then 6 — so just take them in that order, spending as little budget per part as you can. Greedy, no search. Keep going while the remaining budget can still afford the next even number.
- **The one wrinkle:** the loop stops with some leftover that's too small to buy the next even number — but too big to just throw away. The fix is one line: **dump the leftover onto the last number you took.** That keeps the count (you didn't add or remove a part), keeps the sum exact, keeps the number even (even + even = even), and keeps it the largest in the list so distinctness survives. That single line is the entire problem.
- **Pattern trigger:** **"maximise the number of pieces under a fixed budget"** → **take the cheapest legal piece, repeatedly, then absorb the remainder.** You'll meet this exact shape again in Fibonacci-sum decompositions, coin-change constructions, and greedy interval packing. Whenever the objective counts *items* and each item has a *cost*, buy cheap first.

---

## ① Brute Force

Treat it as subset-sum over the even numbers: for each even number in turn, either take it or skip it, and keep the longest combination that hits `finalSum` exactly.

```python
import sys
sys.setrecursionlimit(10000)

def maximumEvenSplit_brute(finalSum):
    if finalSum % 2:
        return []                                  # odd → impossible, bail immediately

    best = []

    def dfs(remaining, nxt, chosen):
        nonlocal best
        if remaining == 0:                         # exact hit — is it the longest so far?
            if len(chosen) > len(best):
                best = chosen[:]
            return
        if nxt > remaining:                        # next even already overshoots
            return
        chosen.append(nxt)                         # branch 1: take `nxt`
        dfs(remaining - nxt, nxt + 2, chosen)
        chosen.pop()
        dfs(remaining, nxt + 2, chosen)            # branch 2: skip `nxt`

    dfs(finalSum, 2, [])
    return best

# maximumEvenSplit_brute(12) -> [2, 4, 6]
# maximumEvenSplit_brute(28) -> [2, 4, 6, 16]
# maximumEvenSplit_brute(7)  -> []
```

**Why it's the natural first attempt:** "distinct numbers from a fixed pool summing to a target" is the classic subset-sum silhouette, and take/skip recursion is the reflex it triggers. It also gives you the right answers on small inputs, which is genuinely useful — it's how you'd sanity-check a greedy you don't fully trust yet.

**Why it's not enough:** the recursion branches twice per candidate even number, so it's **O(2^(finalSum/2))**. At `finalSum = 60` it's already crawling; at `10^10` it would still be running after the heat death of the sun. And note the deeper problem: this thing is *searching* for a choice the math already determines. All that branching is wasted on a decision that has one obviously-best answer at every step.

**Complexity:** Time `O(2^(finalSum/2))`, Space `O(√finalSum)` recursion depth on the successful path (much worse on failing branches).

---

## ② Optimised Solution

Skip the search entirely. Walk `i = 2, 4, 6, …`, taking each one while the remaining budget can still afford it. When you stop, add whatever remainder is left to the **last** number you took.

```python
def maximumEvenSplit(finalSum):
    if finalSum % 2:
        return []                     # sum of evens is even → odd target is impossible

    res = []
    i = 2
    while i <= finalSum:              # can the remaining budget still afford `i`?
        res.append(i)                 # buy the cheapest unused even number
        finalSum -= i                 # spend it
        i += 2                        # next cheapest
    res[-1] += finalSum               # dump the leftover onto the largest part
    return res

# maximumEvenSplit(12) -> [2, 4, 6]
# maximumEvenSplit(28) -> [2, 4, 6, 16]
# maximumEvenSplit(7)  -> []
```

*(`res` can only be empty when `finalSum == 0`, and the constraints guarantee `finalSum >= 1`, so `res[-1]` is always safe. If you ever reuse this where 0 is possible, guard it.)*

**Walk `finalSum = 28`** step by step — note that `finalSum` is doubling as the "remaining budget":

| Step | `i` | `i <= remaining`? | `res` after | remaining |
|---|---|---|---|---|
| start | 2 | — | `[]` | 28 |
| take 2 | 2 | 2 ≤ 28 ✓ | `[2]` | 26 |
| take 4 | 4 | 4 ≤ 26 ✓ | `[2,4]` | 22 |
| take 6 | 6 | 6 ≤ 22 ✓ | `[2,4,6]` | 16 |
| take 8 | 8 | 8 ≤ 16 ✓ | `[2,4,6,8]` | 8 |
| stop | 10 | 10 ≤ 8 ✗ | `[2,4,6,8]` | **8 left over** |
| absorb | — | — | `[2,4,6,`**`16`**`]` | 0 |

Sum check: 2+4+6+16 = 28 ✓, all distinct ✓, all positive even ✓, **4 parts**.

And `finalSum = 12`: take 2 (rem 10), take 4 (rem 6), take 6 (rem 0), stop at `i = 8 > 0`. Leftover is 0, so the absorb line is a no-op → `[2, 4, 6]`, **3 parts** ✓.

**Why absorbing the remainder is safe** — this is the part interviewers actually probe, so prove it, don't assert it. Say the loop took `2, 4, …, 2m` and stopped with remainder `r`.

1. **`r` is even.** `finalSum` was even and every number we subtracted was even, so the leftover is even. Therefore `2m + r` is even. ✓
2. **`r` is small.** The loop stopped precisely because `r < 2m + 2`, the next even we'd have needed.
3. **Distinctness survives.** The new last element is `2m + r ≥ 2m`, which is already strictly greater than every earlier element (the largest of which is `2m − 2`). Growing the maximum can't create a collision — it only pushes it further from the pack. ✓
4. **The count is unchanged.** We modified an existing element; we didn't add or drop one. So the length we achieved in the loop is the length we return. ✓

**Why that length is the maximum** — the exchange argument. Suppose *any* valid split uses `k` distinct positive even numbers. The `k` cheapest distinct positive evens are `2, 4, …, 2k`, summing to `k(k+1)`. Swap any split's parts down to that cheapest prefix and the total can only shrink, so every valid `k` must satisfy:

```
k(k + 1) <= finalSum
```

That's a hard ceiling on `k`, set by arithmetic alone. Now look at what the greedy achieves: it took `m` numbers and stopped, meaning `m(m+1) <= finalSum` (it could afford them) **and** `finalSum − m(m+1) < 2m + 2`, which rearranges to `finalSum < (m+1)(m+2)` (it couldn't afford one more). So `m` is exactly the largest integer satisfying the ceiling. **Greedy hits the bound — nothing can beat it.**

*(Verified: for every `finalSum` from 1 to 200, this greedy's length matches an exhaustive take/skip search, and for every even `finalSum` up to 4000 the returned length `k` satisfies `k(k+1) <= finalSum < (k+1)(k+2)`.)*

**Complexity:** Time `O(√finalSum)`, Space `O(√finalSum)` for the output. Since `m(m+1) <= finalSum`, the loop runs about `√finalSum` times. Put a number on it: at `finalSum = 10^10` the answer holds **99,999 numbers** — a hundred-thousand-element list, built in a hundred thousand operations. That's microseconds, from an input that looked like it demanded a search over billions.

---

## ③ Space Optimization

**Already optimal — and here's the honest why.** The output is `O(√finalSum)` numbers, and *the output is the deliverable*. You're asked to **return the list**, so materializing every element isn't overhead you chose — it's the answer itself. There is no rolling-variable trick, because the thing you'd be trying to shrink is the thing the problem demands you produce.

Beyond the list, the working memory is genuinely `O(1)`: two `long`s, `i` and the shrinking remainder. Nothing else grows.

```python
# No space-optimised variant exists — the O(√finalSum) list IS the required answer.
# Auxiliary memory beyond the output is O(1): just `i` and the remaining budget.
#
# If the problem instead asked only "how MANY parts?", you could answer in O(1) space
# (and O(1) time) with the closed form: the largest k with k(k+1) <= finalSum, i.e.
#     k = int((math.isqrt(4 * finalSum + 1) - 1) // 2)   # for even finalSum
# That's the tell that the O(√finalSum) here is output-bound, not algorithm-bound.
```

**Complexity:** Time `O(√finalSum)`, Space `O(√finalSum)` output-bound, `O(1)` auxiliary.

> Say it out loud: *"Space is O(√finalSum), but that's the list I'm required to return, not overhead — my auxiliary memory is O(1), just a counter and a running remainder. If you only wanted the count, I could give it to you in O(1) time and space with a square root, which shows the √ here is the output size, not the work."*

---

## Java (for Java interviewers)

```java
public List<Long> maximumEvenSplit(long finalSum) {
    List<Long> res = new ArrayList<>();
    if (finalSum % 2 != 0) return res;          // odd target → impossible

    long i = 2;
    while (i <= finalSum) {                     // can the remaining budget afford `i`?
        res.add(i);                             // buy the cheapest unused even
        finalSum -= i;                          // spend it
        i += 2;                                 // next cheapest
    }
    int last = res.size() - 1;
    res.set(last, res.get(last) + finalSum);    // absorb the leftover into the largest
    return res;
}
```

**The Java-specific trap:** `finalSum` goes to `10^10`, which overflows a 32-bit `int` (max ≈ 2.1×10⁹). The signature uses `long`, and so must `i` and the list's element type — `List<Long>`, not `List<Integer>`. Mixing an `int i` into that loop is a silent wrong-answer on the large tests. Verified output: `12 → [2,4,6]`, `7 → []`, `28 → [2,4,6,16]`, and `10^10 → 99999 parts summing to exactly 10000000000`.

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (take/skip subset search) | O(2^(finalSum/2)) | O(√finalSum) depth |
| Optimised (greedy + absorb remainder) | O(√finalSum) | O(√finalSum) — the output |
| Space-optimised | — (none exists) | O(√finalSum) output-bound, O(1) auxiliary |

*(The answer holds `k` numbers where `k(k+1) <= finalSum`, so `k ≈ √finalSum`. At `finalSum = 10^10`, `k = 99,999`.)*

---

## Say it out loud (interview narration)

> *"First: a sum of even numbers is always even, so if `finalSum` is odd I return an empty list immediately — no work needed. Otherwise, I want the most parts, and every part costs budget, so I make each part as cheap as possible: take 2, then 4, then 6, subtracting each from the remainder while the remainder can still afford the next one. When I stop, there's a leftover that's too small to buy another even number — I add it to the last number I took. That's safe because the leftover is even, so the last element stays even, and it only grows the maximum, so all the numbers stay distinct. For maximality: any split of size k needs at least 2+4+…+2k = k(k+1), so k(k+1) ≤ finalSum is a hard ceiling, and my loop stops exactly at that ceiling — it can't be beaten. Time and space are O(√finalSum), about 10⁵ elements at the 10^10 limit, and that space is the output I'm asked to return, so my auxiliary memory is O(1). In Java I'd use `long` throughout — 10^10 overflows `int`."*

Before you write a line, ask the one clarifying question that proves you read the spec: *"If `finalSum` is odd there's no valid split at all, so I return an empty list — confirming that's expected rather than an error?"* Surfacing the impossible case *before* coding is exactly what Google's rubric rewards, and it costs you five seconds.

## Related / follow-ups
- **LC 1414. Find the Minimum Number of Fibonacci Numbers Whose Sum Is K** — the mirror image: greedy over a fixed number family again, but taking the **largest** piece each time because you're *minimising* the count. Same lever, opposite direction — and a great pair to study together.
- **LC 2952. Minimum Number of Coins to be Added** — greedy construction over a reachable range, with the same "what's the cheapest thing I can add next" instinct.
- **LC 881. Boats to Save People** — greedy packing under a capacity budget; the exchange argument for why greedy is optimal follows the same template used above.
- **LC 455. Assign Cookies** — the simplest possible version of "spend the cheapest resource first to maximise the count." If the exchange argument here felt slippery, prove it on this one first.
- **Follow-up to expect:** *"What if the parts had to be distinct **odd** numbers?"* Then the parity gate changes — `k` odd numbers sum to something with the parity of `k`, so feasibility depends on `finalSum` and `k` together, and the smallest-`k` prefix becomes `1+3+…+(2k−1) = k²`. Same greedy skeleton, new arithmetic.
