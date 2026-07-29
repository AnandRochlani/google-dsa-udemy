# First Bad Version (Boundary Search)

> **LeetCode:** 278. First Bad Version · **Difficulty:** 🟢 Easy · **Pattern:** Modified Binary Search · **Google frequency:** ⭐ high

---

## Problem

You have `n` versions `[1, 2, …, n]`. At some point one version broke and **every version after it is also bad**. You're given an API `isBadVersion(v)` that returns `True`/`False`. Find the **first** bad version, calling the API as few times as possible.

**Example:** `n = 5`, and the first bad version is `4` → `isBadVersion` returns `F, F, F, T, T` for versions 1–5 → answer `4`.

**Constraints that matter:** `n` can be up to ~2³¹−1 (~2 billion), so the API call is expensive and a linear scan (up to 2 billion calls) is hopeless. The array of results is **monotonic**: once it flips to bad, it stays bad — `F F F T T T`. That single boolean flip is exactly what binary search hunts for.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Call `isBadVersion(1)`, `(2)`, `(3)`… return the first one that's bad." A linear scan of the version numbers — O(n) API calls.
- **Where it hurts:** `n` is ~2 billion. Up to 2 billion API calls is far too many, and each call is the costly operation the problem is measuring. Every call only rules out one version.
- **The leap:** The results form a **sorted boolean sequence**: `F F F T T T`. There's exactly one flip point, and *that flip is the answer*. Finding a flip in a monotonic sequence is textbook binary search — probe the middle version. If it's **bad**, the first bad version is at `mid` or **to its left**, so keep `mid` as a candidate (`right = mid`). If it's **good**, the answer is strictly to the **right** (`left = mid + 1`). Each call halves the range.
- **Pattern trigger:** **"find the first/leftmost element satisfying a monotonic condition"** → **boundary binary search (lower bound).** The tell is the `F…F T…T` shape — you're not matching a value, you're locating the **boundary** between false and true.

---

## ① Brute Force

Ask every version in order.

```python
def firstBadVersion_brute(n):
    for v in range(1, n + 1):
        if isBadVersion(v):
            return v
    return -1
```

**Why it's the natural first attempt:** "first bad one" reads literally as "scan until the first True."

**Why it's not enough:** up to `n` (~2 billion) API calls — O(n). The API cost is the whole point of the problem, and this maximizes it. It ignores that the sequence is monotonic.

**Complexity:** Time `O(n)` API calls, Space `O(1)`.

---

## ② Optimised Solution

Boundary binary search. Note the template shift from value-search: **`right = mid`, not `mid - 1`**, because `mid` might *be* the answer and we don't want to discard it.

```python
def firstBadVersion(n):
    left, right = 1, n              # search space: version numbers [1, n]
    while left < right:            # < (not <=): stop when the range is one element
        mid = left + (right - left) // 2
        if isBadVersion(mid):
            right = mid           # mid is bad → answer is mid or to its LEFT (keep mid)
        else:
            left = mid + 1        # mid is good → answer is strictly to the RIGHT
    return left                    # left == right → the single surviving boundary
```

**Why this template differs from LC 704:**
- **`while left < right`** (strict): we're converging on a single boundary index, not probing for a match, so we stop when one candidate remains and return it.
- **`right = mid`** (not `mid - 1`): when `mid` is bad, it's still a *possible* answer — discarding it could skip the true first-bad version.
- **`mid` floors toward `left`**, so with `left < right` we always have `mid < right`; the `left = mid + 1` branch guarantees progress and prevents an infinite loop.

**Walk the example** `n = 5`, first bad = `4` (results `F F F T T`):

| left | right | mid | isBadVersion(mid) | action |
|---|---|---|---|---|
| 1 | 5 | 3 | F | left = 4 |
| 4 | 5 | 4 | T | right = 4 |
| — | — | — | left(4) == right(4) | **return 4** ✅ |

**Why it's correct (loop invariant):** *"the first bad version is always within `[left, right]`."* Initially the whole range. If `mid` is bad, everything right of `mid` is also bad (monotonicity), so the earliest bad one is at `mid` or left — we keep `[left, mid]`. If `mid` is good, everything left of and including `mid` is good, so the answer is in `[mid+1, right]`. The invariant holds; the range strictly shrinks; when `left == right` that lone index *is* the boundary.

**Complexity:** Time `O(log n)` API calls, Space `O(1)`.

---

## ③ Space Optimization

Already **O(1)** — just two integer bounds. Nothing grows with `n`; the search space is the *range* `[1, n]`, which we track with two numbers, not by materializing any array.

> Note `mid = left + (right - left) // 2` rather than `(left + right) // 2`: with `n` near 2³¹, `left + right` could overflow in fixed-width-integer languages like Java. Python ints are unbounded, but keep the safe form as a habit.

---

## Java (for Java interviewers)

```java
public int firstBadVersion(int n) {
    int left = 1, right = n;
    while (left < right) {
        int mid = left + (right - left) / 2;   // overflow-safe
        if (isBadVersion(mid)) right = mid;     // keep mid as candidate
        else left = mid + 1;
    }
    return left;
}
```

---

## Complexity Summary

| Approach | Time (API calls) | Space |
|---|---|---|
| Brute force (linear) | O(n) | O(1) |
| Optimised (boundary binary search) | O(log n) | O(1) |

---

## Say it out loud (interview narration)

> *"The results are monotonic — good, good, good, then bad forever — so I'm looking for the flip point, which is exactly what binary search does. I probe the middle version: if it's bad, the first bad one is here or to the left, so I keep mid in the range with right = mid; if it's good, I move left past it. I use `while left < right` and return left, because I'm converging on a single boundary, not matching a value. That's O(log n) API calls instead of O(n)."*

## Related / follow-ups
- **Search Insert Position** (LC 35 — lower bound of a value)
- **Find First and Last Position** (LC 34 — two boundary searches)
- **Sqrt(x)** (LC 69 — boundary search over the answer range)
- **Binary Search** (LC 704 — the value-matching template to contrast against)
