# The Number of Weak Characters in the Game

> **LeetCode:** 1996. The Number of Weak Characters in the Game · **Difficulty:** 🟡 Medium · **Pattern:** Sort + running max (greedy sweep) · **Google frequency:** ⭐ high

---

## Problem

You're given `properties`, where `properties[i] = [attack_i, defense_i]` for the i-th game character. A character `i` is **weak** if there exists *some other* character `j` that beats it on **both** stats at once — that is, `attack_j > attack_i` **and** `defense_j > defense_i`. Both comparisons are **strict**. Count how many characters are weak.

**Example:** `properties = [[1,5],[10,4],[4,3]]` → `1` *(the character `[4,3]` is weak — `[10,4]` has both a bigger attack (10 > 4) and a bigger defense (4 > 3). Nobody dominates `[10,4]` or `[1,5]`.)*

**Constraints that matter:** `n` up to `10^5`, and each stat up to `10^5`. That `10^5` kills the obvious answer: comparing every pair is `n²` ≈ `10^10` operations — a guaranteed Time Limit Exceeded. The size is *screaming* "get me to `O(n log n)`," which is the universal hint for **sort first, then sweep once.**

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each character, look at everyone else and check if somebody beats it on both stats." That's the definition read literally — a double loop. It's correct, and it's `O(n²)`. On `10^5` characters it dies.
- **Where it hurts:** the inner loop re-scans the *entire* array for every character, asking the same question over and over: "is there anyone with a bigger attack **and** a bigger defense?" We're re-deriving the same global facts `n` times. The waste is that we never *organize* the characters — we brute-search an unsorted pile every single time.
- **The leap:** two conditions are hard to satisfy at once, so **freeze one of them by sorting.** Sort by attack **descending**. Now walk left to right. By the time you reach character `i`, everyone you've already seen has an attack that is `≥ attack_i`. So the attack condition is *almost* handled for free — the only question left is defense. If **any** already-seen character had a strictly bigger defense, `i` is weak. And "was there a bigger defense among everyone seen so far?" is just a **running maximum**. One variable. One pass.
- **The subtle trap — and the tie-break that fixes it:** "already seen has attack `≥ attack_i`" includes the `=` case, and weak requires attack **strictly** greater. If a character with the *same* attack but higher defense sits before `i`, it would wrongly inflate our running max and mark `i` weak. The fix is the whole trick: among characters with **equal attack, sort defense ascending.** Then within any equal-attack group, defenses only *climb* as we sweep, so an earlier same-attack character can never have a bigger defense than a later one — it can never trigger a false weak. The only way the running max exceeds the current defense is if a **strictly-greater-attack** character (from an earlier group) set it. Exactly what we want.
- **Pattern trigger:** **"dominance on two dimensions + n too big for `n²`"** → **sort on one dimension, sweep a running max on the other.** The transferable move: *collapse a 2-D condition into a 1-D sweep by sorting away one dimension — and let the tie-break enforce the strict-vs-non-strict boundary.*

---

## ① Brute Force

For every character, scan all the others; if anyone beats it on both stats, it's weak.

```python
def numberOfWeakCharacters_brute(properties):
    n = len(properties)
    weak = 0
    for i in range(n):
        ai, di = properties[i]
        for j in range(n):
            aj, dj = properties[j]
            if aj > ai and dj > di:   # strictly bigger on BOTH → i is dominated
                weak += 1
                break                 # one dominator is enough; stop
    return weak
```

**Why it's the natural first attempt:** it's the definition typed out verbatim — "is there a `j` that dominates `i`?" — so it's obviously correct and easy to reason about.

**Why it's not enough:** the nested loop is `O(n²)`. With `n = 10^5` that's `10^10` comparisons — tens of seconds, far past the limit. Every inner pass re-answers a global question ("does a dominator exist?") from scratch, throwing away everything the previous passes learned.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

Sort by **attack descending**, breaking ties by **defense ascending**. Sweep left to right, holding the largest defense seen so far. Any character whose defense is below that running max is weak.

```python
def numberOfWeakCharacters(properties):
    # attack DESC, and for equal attack, defense ASC (the crucial tie-break)
    properties.sort(key=lambda p: (-p[0], p[1]))

    weak = 0
    max_def = 0                       # best defense among everyone seen so far
    for _, defense in properties:
        if defense < max_def:
            # someone earlier had a STRICTLY bigger attack (earlier group)
            # AND a strictly bigger defense → this character is dominated
            weak += 1
        else:
            max_def = defense         # new high-water mark for defense
    return weak
```

**Walk one example** — `properties = [[1,5],[10,4],[4,3]]`:

After sorting by `(-attack, defense)` the order is `[10,4], [4,3], [1,5]`.

| Step | Character | `defense < max_def`? | Action | `max_def` after | weak |
|---|---|---|---|---|---|
| 1 | `[10,4]` | `4 < 0`? no | update max | `4` | 0 |
| 2 | `[4,3]`  | `3 < 4`? **yes** | weak++ | `4` | 1 |
| 3 | `[1,5]`  | `5 < 4`? no | update max | `5` | 1 |

Answer: **1**. `[4,3]` is dominated by `[10,4]` (seen earlier, strictly bigger attack, and its defense 4 > 3). ✅

Now the tie-break example — `[[1,1],[2,1],[2,2],[1,2]]`. Sorted by `(-attack, defense)`: `[2,1], [2,2], [1,1], [1,2]`.

| Step | Character | `defense < max_def`? | Action | `max_def` | weak |
|---|---|---|---|---|---|
| 1 | `[2,1]` | `1 < 0`? no | update | `1` | 0 |
| 2 | `[2,2]` | `2 < 1`? no | update | `2` | 0 |
| 3 | `[1,1]` | `1 < 2`? **yes** | weak++ | `2` | 1 |
| 4 | `[1,2]` | `2 < 2`? no | update | `2` | 1 |

Answer: **1**. Watch step 2: `[2,2]` shares its attack with `[2,1]`, but because we sorted defense **ascending**, `[2,1]` (defense 1) came *first* and set `max_def = 1` — so `[2,2]` (defense 2) is *not* flagged. If we'd sorted defense descending, `[2,2]` would've set `max_def = 2` before `[2,1]` arrived, and `[2,1]` would be wrongly counted weak against a character with *equal* attack. That's the bug the tie-break kills. ✅

**Why it's correct:** sorting attack descending guarantees that when we reach character `i`, every character already processed has `attack ≥ attack_i`. So `max_def` is the largest defense among a set that all out-attack-or-tie `i`. The ascending-defense tie-break ensures that within `i`'s *own* equal-attack group, no earlier member has a larger defense than `i` (defenses only rise inside a group), so those `=`-attack characters can never push `max_def` above `defense_i`. Therefore `defense_i < max_def` can only happen because a character from a *strictly earlier* group — one with `attack > attack_i` — had a strictly bigger defense. That's precisely the definition of weak, so we count exactly the weak characters, no more, no fewer.

**Complexity:** Time `O(n log n)` (the sort dominates; the sweep is `O(n)`), Space `O(1)` extra beyond the sort.

---

## ③ Space Optimization

**Already optimal on the sweep — and here's the honest accounting.** The sweep itself carries just two integers, `max_def` and `weak`, so its auxiliary space is `O(1)`. The only real memory cost is the **sort**: an in-place sort (Python's Timsort, Java's dual-pivot) uses `O(log n)` to `O(n)` stack/scratch depending on implementation, but we don't allocate any extra structure ourselves — no hash map, no heap, no second array. We mutate `properties` in place.

```python
# No extra data structure needed. We sort in place and sweep with two ints:
#   max_def  – running maximum defense seen so far
#   weak     – the answer counter
# Nothing grows with n during the sweep, so auxiliary space is O(1).
```

There's no way to beat `O(n log n)` time here without extra space, either: you *could* trade to `O(n)` time using **counting-sort on attack** (stats are bounded by `10^5`) plus a suffix-max of defense — but that spends `O(10^5)` auxiliary space to buy the log factor. For these constraints the sort-and-sweep is the clean, expected answer; naming the counting-sort alternative out loud is a nice bonus signal.

**Complexity:** Time `O(n log n)`, Space `O(1)` auxiliary (in-place sort).

> Say it out loud: *"The sweep is O(1) space — just two integers. The only memory is the in-place sort. I could drop to O(n) time with a counting sort on attack since stats are capped at 10^5, but that costs O(10^5) space, so for these limits the sort-and-sweep is the right trade."*

---

## Java (for Java interviewers)

```java
public int numberOfWeakCharacters(int[][] properties) {
    // attack DESC; for equal attack, defense ASC (the crucial tie-break)
    Arrays.sort(properties, (a, b) ->
        a[0] == b[0] ? a[1] - b[1] : b[0] - a[0]);

    int weak = 0;
    int maxDef = 0;                      // best defense among everyone seen so far
    for (int[] p : properties) {
        if (p[1] < maxDef) {
            weak++;                      // strictly bigger attack earlier + bigger defense
        } else {
            maxDef = p[1];               // new high-water mark
        }
    }
    return weak;
}
```

*(Note the tie-break in the comparator: `a[1] - b[1]` for equal attack sorts defense **ascending** — get this backwards and same-attack characters corrupt the count.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all pairs) | O(n²) | O(1) |
| Sort + running-max sweep | O(n log n) | O(1) auxiliary |
| Counting-sort + suffix-max (alt) | O(n + M) | O(M), M = 10^5 |

*(n = number of characters; M = the cap on a stat value.)*

---

## Say it out loud (interview narration)

> *"The literal definition is a double loop — for each character, is anyone strictly bigger on both stats? That's O(n²), and with n up to 10^5 it times out. So I'll collapse the two conditions into one. I sort by attack descending, which means by the time I reach a character, everyone I've already seen out-attacks it or ties it. Now the only open question is defense, and 'did anyone seen so far have a bigger defense?' is just a running maximum — one variable, one pass. The one subtlety is strictness: weak needs attack strictly greater, so I break ties by defense ascending. That way same-attack characters have their defenses climbing as I sweep, and an earlier equal-attack character can never falsely inflate my max. Sort is O(n log n), sweep is O(n), extra space O(1)."*

Before coding, ask the clarifying question that proves you read the spec: *"Both comparisons are strict, right — attack and defense both have to be strictly greater?"* That one question is what drives the ascending-defense tie-break, and naming it early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Russian Doll Envelopes (LC 354)** — same "dominate on two dimensions" DNA; sort one dim, then it becomes Longest Increasing Subsequence on the other.
- **Best Sightseeing Pair (LC 1014)** — collapse a two-index max into a single left-to-right sweep of a running best.
- **Maximum Profit / stock problems** — the running-max/running-min sweep after fixing an order.
- **Merge Intervals (LC 56)** — the other archetypal "sort first, then one linear pass does everything" problem.
