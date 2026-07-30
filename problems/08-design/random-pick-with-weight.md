# Random Pick with Weight

> **LeetCode:** 528. Random Pick with Weight · **Difficulty:** 🟡 Medium · **Pattern:** Prefix sum + binary search · **Google frequency:** ⭐ high

---

## Problem

You're given an array `w` of **positive** integer weights. Build a class that supports `pickIndex()`, which returns an index `i` at random — but *not* uniformly. Index `i` must come back with probability `w[i] / sum(w)`. A heavier weight means that index gets picked more often, in exact proportion to its size.

**Example:** `w = [1, 3]` → `pickIndex()` returns `0` about **25%** of the time and `1` about **75%** of the time *(total weight is 4; index 0 owns 1 of it, index 1 owns 3)*.

**Constraints that matter:** `w` can be up to `10^4` long and `pickIndex` may be called up to `10^4` times. So the constructor can afford an `O(n)` pass, but each `pickIndex` call should be fast — ideally `O(log n)`, not `O(n)`. That gap between "build once" and "query many times" is the whole design signal.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Weighted pick? Just make a big bag." For `w = [1, 3]`, build the array `[0, 1, 1, 1]` — one `0` and three `1`s — then pick a uniform random slot. Index `1` shows up three times as often. Correct, and dead simple.
- **Where it hurts:** the bag has `sum(w)` entries. If a single weight is a million, you've allocated a million slots for *one* index. Memory explodes, and so does the build time. The weights are the problem — we're paying for their *magnitude*, not their *count*.
- **The leap:** picture the weights as **segments on a number line**, laid end to end. Index 0 owns `[0, 1)`, index 1 owns `[1, 4)`. The whole line runs from 0 to `total = 4`. Now throw a dart at a uniform random point on that line. Whichever segment it lands in — that's your index. A segment three times as wide catches the dart three times as often. Same probabilities as the bag, but we never materialize the slots — we just need to know **where each segment ends**.
- **Pattern trigger:** "cumulative ranges + find which range a point falls into" → **prefix sums to define the ends, binary search to locate the point.** The prefix-sum array *is* the list of segment boundaries; binary search turns the dart-throw into `O(log n)`. Any "weighted / cumulative distribution + fast lookup" problem is this exact combo.

---

## ① Brute Force

Expand the weights into a bag with `w[i]` copies of `i`, then pick a uniform random element.

```python
import random

class Solution:
    def __init__(self, w):
        self.bag = []
        for i, weight in enumerate(w):
            self.bag.extend([i] * weight)   # w[i] copies of index i

    def pickIndex(self):
        return random.choice(self.bag)      # uniform over the expanded bag
```

**Why it's the natural first attempt:** it's a literal translation of "pick `i` with probability proportional to `w[i]`." More copies of `i` in the bag → more likely to land on `i`. Anyone can see it's correct at a glance.

**Why it's not enough:** the bag holds `sum(w)` elements. With weights up to `10^8`, that's hundreds of millions of integers for a handful of indices — you run out of memory before you even answer a query. The cost tracks the *values* of the weights, not the array length `n`, which is exactly the wrong thing to scale with.

**Complexity:** Time `O(sum(w))` to build, `O(1)` per pick; Space `O(sum(w))`.

---

## ② Optimised Solution

Keep the number-line picture, but store only the **segment boundaries**. Build a prefix-sum array `prefix` where `prefix[i] = w[0] + w[1] + … + w[i]` — that's the *right edge* of index `i`'s segment. The `total` is `prefix[-1]`. To pick: roll a uniform `target` in `[1, total]`, then binary-search for the **smallest** `i` with `prefix[i] >= target`. That index's segment is the one containing the dart.

```python
import random
import bisect

class Solution:
    def __init__(self, w):
        # prefix[i] = right edge of index i's segment on the number line
        self.prefix = []
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running                 # == prefix[-1] == sum(w)

    def pickIndex(self):
        # dart at a uniform integer in [1, total]
        target = random.randint(1, self.total)
        # smallest i with prefix[i] >= target  →  the segment the dart lands in
        return bisect.bisect_left(self.prefix, target)
```

**Walk one example** with `w = [1, 3]`, so `prefix = [1, 4]`, `total = 4`:

| `target` (from `randint(1,4)`) | segment it falls in | `bisect_left(prefix, target)` | index returned |
|---|---|---|---|
| 1 | `[0,1)` → edge 1 | first `prefix[i] >= 1` is `prefix[0]=1` | **0** |
| 2 | `[1,4)` → edge 4 | first `prefix[i] >= 2` is `prefix[1]=4` | **1** |
| 3 | `[1,4)` | first `prefix[i] >= 3` is `prefix[1]=4` | **1** |
| 4 | `[1,4)` | first `prefix[i] >= 4` is `prefix[1]=4` | **1** |

`target = 1` gives index 0; `target ∈ {2,3,4}` gives index 1. That's exactly **1 out of 4** for index 0 and **3 out of 4** for index 1 — the required 25% / 75%. ✅

**Why `>=` and not `>`?** Ask which index "owns" a boundary value. Index `i`'s segment is `(prefix[i-1], prefix[i]]` in `target`-space — it *includes* its own right edge `prefix[i]`. When `target` equals a boundary, that hit belongs to the segment ending there, so we want the *first* prefix value that reaches or passes `target` → `>=` → `bisect_left`. Using `>` (i.e. `bisect_right`) would push a boundary hit onto the *next* index, shifting one unit of probability the wrong way. And because `target` starts at **1** (not 0), the very first unit of weight correctly maps into index 0's segment — the off-by-one that trips people up is handled by the `[1, total]` range lining up with `bisect_left`.

**Why it's correct:** the segment widths are exactly `w[i]` (segment `i` spans the `target` values `prefix[i-1]+1 … prefix[i]`, which is `w[i]` integers). `target` is uniform over `total` equally-likely integers, so the probability of landing in segment `i` is `width / total = w[i] / sum(w)` — precisely the spec. Binary search returns the unique segment because `prefix` is strictly increasing (weights are positive), so there's always exactly one smallest index meeting the threshold.

**Complexity:** constructor Time `O(n)`, each `pickIndex` Time `O(log n)`; Space `O(n)`.

---

## ③ Space Optimization

**Already optimal — and here's the honest why.** We store one prefix value per index: `O(n)`. You genuinely can't go lower, because binary search *needs* the sorted boundary array to exist — it's the structure that buys you `O(log n)` lookups. Drop it and you're back to scanning weights linearly per pick (`O(n)` per query), which is worse where it counts: queries are the hot path, called up to `10^4` times.

```python
# No smaller structure works. The prefix array IS the search space —
# it's O(n), and that O(n) is what turns each pick into O(log n).
# Trading it away to save memory would cost you the query speed you built it for.
```

**Complexity:** Time `O(n)` build / `O(log n)` pick, Space `O(n)`.

> Say it out loud: *"Space is O(n) for the prefix array, and that's optimal — the sorted array is exactly what enables the log-n binary search. There's no rolling-variable trick, because I need the whole boundary list present to search it."* Naming why it can't shrink is the strong-hire move.

---

## Java (for Java interviewers)

```java
import java.util.Random;

class Solution {
    private final int[] prefix;   // prefix[i] = right edge of segment i
    private final int total;
    private final Random rand = new Random();

    public Solution(int[] w) {
        prefix = new int[w.length];
        int running = 0;
        for (int i = 0; i < w.length; i++) {
            running += w[i];
            prefix[i] = running;
        }
        total = running;                       // == sum(w)
    }

    public int pickIndex() {
        int target = rand.nextInt(total) + 1;  // uniform in [1, total]
        // manual binary search: smallest i with prefix[i] >= target
        int lo = 0, hi = prefix.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (prefix[mid] < target) {
                lo = mid + 1;                  // mid too small — go right
            } else {
                hi = mid;                      // mid works — keep it, shrink right
            }
        }
        return lo;
    }
}
```

*(The `hi = mid` — not `mid - 1` — is what makes this find the **smallest** qualifying index: we never discard `mid` when it satisfies the threshold.)*

---

## Complexity Summary

| Approach | Time (build) | Time (pick) | Space |
|---|---|---|---|
| Brute force (expand bag) | O(sum w) | O(1) | O(sum w) |
| Optimised (prefix + binary search) | O(n) | O(log n) | O(n) |
| Space-optimised | — (none exists) | O(log n) | O(n) |

---

## Say it out loud (interview narration)

> *"The naive version expands the weights into a bag and picks uniformly — correct, but it scales with the sum of the weights, so a big weight blows up memory. The fix is to think of the weights as segments on a number line, each `w[i]` wide, laid end to end. I precompute a prefix-sum array — that's the right edge of each segment — in O(n) once. To pick, I throw a dart: a uniform random `target` in `[1, total]`, then binary-search for the smallest prefix value that reaches it. A wider segment catches more darts, so index `i` comes back with probability `w[i] / total`, exactly as required. Build is O(n), each pick is O(log n), space is O(n) — and I'd flag the `>=` vs `>` boundary decision out loud, since that's the off-by-one that quietly skews the distribution."*

Before coding, ask the one clarifying question that shows you read the spec: *"Weights are all positive integers, right? — that's what keeps the prefix array strictly increasing so binary search is well-defined."* Asking it early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Random Pick Index (LC 398)** — pick a random index of a target value; reservoir sampling instead of prefix sums.
- **Random Pick with Blacklist (LC 710)** — remap a shrunken uniform range; same "map a uniform draw onto a distribution" DNA.
- **Insert Delete GetRandom O(1) (LC 380)** — uniform random from a dynamic set; the design cousin.
- **Find K Closest Elements / any `bisect` problem** — same binary-search-on-a-sorted-prefix muscle.
