# Koko Eating Bananas (Binary Search on the Answer)

> **LeetCode:** 875. Koko Eating Bananas · **Difficulty:** 🟡 Medium · **Pattern:** Modified Binary Search · **Google frequency:** ⭐ high

---

## Problem

Koko has `piles` of bananas and `h` hours before the guards return. Each hour she picks **one** pile and eats up to `k` bananas from it; if the pile has fewer than `k`, she eats it all and stops for that hour (she won't switch piles mid-hour). Find the **minimum** integer eating speed `k` such that she finishes **all** piles within `h` hours.

**Example:** `piles = [3, 6, 7, 11]`, `h = 8` → `4`. *(At k=4: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 hours — just fits. k=3 would need 1+2+3+4 = 10 > 8.)*

**Constraints that matter:** `piles.length` up to ~10⁴, pile sizes up to ~10⁹, and `h` up to ~10⁹. The candidate speeds run from `1` to `max(piles)` (~10⁹) — **far too many to try one by one.** But notice: *feasibility is monotonic in `k`.* That's the door to binary search.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Try k = 1, does she finish in time? No. k = 2? … keep bumping k until she does." A linear sweep over speeds — return the first `k` that works.
- **Where it hurts:** `k` can be up to `max(piles)` ≈ 10⁹, and each feasibility check costs O(n). That's up to 10⁹ × 10⁴ operations — utterly hopeless. You're scanning a **huge answer range** one integer at a time.
- **The leap:** Two observations click together. (1) The thing we're searching for isn't inside the array — it's the **answer value `k`** itself, living in the range `[1, max(piles)]`. (2) Feasibility is **monotonic**: if speed `k` finishes in time, every speed `> k` also finishes (faster never hurts); if `k` is too slow, everything `< k` is too slow too. So `canFinish(k)` looks like `F F F … F T T T …` — a boundary! We want the **leftmost `T`**. Binary-search the *speed range*, using an O(n) hours-check as the "comparison."
- **Pattern trigger:** **"minimize/maximize some value X subject to a feasibility test that's monotonic in X"** → **binary search on the answer.** The tells: the answer is a number in a known range, brute force means trying every value, and `feasible(X)` flips once from false to true (or true to false). You binary-search *X*, not the input array.

---

## ① Brute Force

Try every speed from 1 upward; return the first that finishes in time.

```python
import math

def minEatingSpeed_brute(piles, h):
    def hours_needed(k):
        return sum(math.ceil(p / k) for p in piles)

    for k in range(1, max(piles) + 1):
        if hours_needed(k) <= h:
            return k
    return max(piles)   # k = max(piles) always finishes (1 pile/hour)
```

**Why it's the natural first attempt:** "find the minimum speed that works" reads as "check speeds in increasing order, stop at the first that works."

**Why it's not enough:** the speed range is up to ~10⁹ and each check is O(n) → up to ~10¹³ operations. Times out immediately. It ignores that feasibility is monotonic, so it never skips the doomed low speeds in bulk.

**Complexity:** Time `O(max(piles) · n)`, Space `O(1)`.

---

## ② Optimised Solution

Binary-search the **answer range** `[1, max(piles)]`, converging on the leftmost feasible speed — the same **boundary template** as First Bad Version (`while left < right`, `right = mid`).

```python
import math

def minEatingSpeed(piles, h):
    def hours_needed(k):
        # ceil(p / k) without float error: (p + k - 1) // k
        return sum((p + k - 1) // k for p in piles)

    left, right = 1, max(piles)        # speed can't be 0; never need more than the biggest pile
    while left < right:               # converge on a single boundary speed
        mid = left + (right - left) // 2
        if hours_needed(mid) <= h:
            right = mid               # mid works → answer is mid or SLOWER (keep mid)
        else:
            left = mid + 1            # mid too slow → need a FASTER speed
    return left                        # leftmost speed that finishes in time
```

**Two correctness details worth voicing:**
- **Integer ceil:** `(p + k - 1) // k` computes `ceil(p / k)` with pure integer math — avoids floating-point rounding bugs that `math.ceil(p / k)` can hit on huge values.
- **Boundary template:** because `mid` might *be* the minimum feasible speed, we set `right = mid` (not `mid - 1`) when it works, and use `while left < right` returning `left` — identical structure to First Bad Version.

**Walk the example** `piles = [3, 6, 7, 11]`, `h = 8`, range `[1, 11]`:

| left | right | mid | hours_needed(mid) | ≤ 8? | action |
|---|---|---|---|---|---|
| 1 | 11 | 6 | 1+1+2+2 = 6 | yes | right = 6 |
| 1 | 6 | 3 | 1+2+3+4 = 10 | no | left = 4 |
| 4 | 6 | 5 | 1+2+2+3 = 8 | yes | right = 5 |
| 4 | 5 | 4 | 1+2+2+3 = 8 | yes | right = 4 |
| — | — | — | left(4) == right(4) | — | **return 4** ✅ |

**Why it's correct (loop invariant):** *"the minimum feasible speed is always in `[left, right]`."* Feasibility is monotonic, so `hours_needed(mid) <= h` means every speed ≥ `mid` also works — the minimum is at `mid` or slower, keep `[left, mid]`. Otherwise every speed ≤ `mid` fails — the answer is in `[mid+1, right]`. The invariant holds and the range strictly shrinks; when `left == right`, that speed is the smallest that fits in `h` hours.

**Complexity:** Time `O(n · log(max(piles)))`, Space `O(1)`.

---

## ③ Space Optimization

Already **O(1)** — two integer bounds plus a running sum in `hours_needed`. The search space is the numeric range `[1, max(piles)]`, tracked with two numbers, never materialized.

> The magic is that we replaced a *linear scan over 10⁹ candidate speeds* with a *log-scan* — the `hours_needed` helper is the "comparator" that tells binary search which half of the speed range to drop. Recognizing that feasibility is monotonic is the entire unlock; the space was never the constraint.

---

## Java (for Java interviewers)

```java
public int minEatingSpeed(int[] piles, int h) {
    int left = 1, right = 0;
    for (int p : piles) right = Math.max(right, p);

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (hoursNeeded(piles, mid) <= h) right = mid;   // works → try slower
        else left = mid + 1;                             // too slow → go faster
    }
    return left;
}

private long hoursNeeded(int[] piles, int k) {
    long hours = 0;
    for (int p : piles) hours += (p + k - 1) / k;        // ceil(p/k), integer math
    return hours;
}
```

*(`hours` is a `long`: up to ~10⁴ piles each contributing up to ~10⁹ can overflow `int`.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (try every speed) | O(max(piles) · n) | O(1) |
| Optimised (binary search on answer) | O(n · log(max(piles))) | O(1) |

---

## Say it out loud (interview narration)

> *"I'm not searching inside the array — I'm searching for the answer, the speed k, which lives between 1 and max(piles). The key is that feasibility is monotonic: if speed k finishes in time, so does every faster speed. So `canFinish` looks like F F F T T T, and I binary-search for the leftmost T. My 'comparison' is an O(n) pass summing ceil(pile / k) hours. I keep mid when it works (right = mid) since it might be the minimum, and return left. That turns a 10⁹-wide scan into O(n log(max pile))."*

## Related / follow-ups
- **Capacity To Ship Packages Within D Days** (LC 1011 — same 'binary search the answer' shape)
- **Split Array Largest Sum** (LC 410 — minimize the max subarray sum)
- **Minimum Number of Days to Make m Bouquets** (LC 1482)
- **First Bad Version** (LC 278 — the boundary template reused here)
