# Range Module

> **LeetCode:** 715. Range Module · **Difficulty:** 🔴 Hard · **Pattern:** Sorted disjoint-interval structure (TreeMap / bisect) · **Google frequency:** ⭐ high

---

## Problem

Design a `RangeModule` that tracks a set of covered numbers on the number line and supports three operations on **half-open** intervals `[left, right)` — covering `left` up to but **not including** `right`:

- `addRange(left, right)` — mark every number in `[left, right)` as covered. Numbers already covered stay covered.
- `queryRange(left, right)` — return `true` **iff every single number** in `[left, right)` is currently covered. Partial coverage is `false`.
- `removeRange(left, right)` — mark every number in `[left, right)` as *not* covered, leaving everything outside untouched.

**Example:**

```
addRange(10, 20)       # covered: [10,20)
removeRange(14, 16)    # covered: [10,14) and [16,20)
queryRange(10, 14) → true    # fully inside [10,14)
queryRange(13, 15) → false   # 14 and 15 are the hole we just punched
queryRange(16, 17) → true    # fully inside [16,20)
```

**Constraints that matter:** `0 <= left < right <= 10^9`, and up to `10^4` calls total. That `10^9` is the whole story. **You cannot index by coordinate.** A byte-per-number array is a gigabyte; a Python `list` of booleans is eight. And `addRange(0, 10^9)` would be a *billion* writes — for one call. The number of *operations* is tiny (`10^4`), the number of *positions* is enormous. That mismatch is the problem telling you exactly what to do: **stop storing points, start storing intervals.**

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Coverage is just a set of numbers — keep a boolean array, or a `set`." Perfectly reasonable, and you should say it out loud. It's also the version that dies on the constraints, and *naming why it dies* is half the interview.
- **Where it hurts:** the cost is tied to the **coordinate range**, not the **work you actually did**. After ten thousand calls you can have at most ~ten thousand "things", but the array insists on tracking a billion cells. You're paying for empty space.
- **The leap:** after any sequence of operations, the covered set is always a **union of disjoint intervals** — and there can never be more of them than the number of calls you've made. `addRange(0, 10^9)` doesn't produce a billion cells; it produces **one interval**. So store the intervals, sorted by start, kept **disjoint and non-touching**. Every operation becomes: binary-search to the affected slice, splice a tiny replacement in.
- **The second leap (the one people miss):** keep the invariant *aggressively normalized*. Not just disjoint — **non-touching**. `[10,14)` and `[14,20)` must be stored as the single `[10,20)`. If you allow touching intervals, `queryRange(10, 20)` has to walk a chain to prove full coverage. If you forbid them, coverage of `[left, right)` can only come from **one** interval, and the query collapses to a single binary search plus one comparison. *Normalize on write so reads are trivial* — that's the real design lesson.
- **Pattern trigger:** **"huge coordinate range + few operations + range mark/unmark/query"** → **ordered map of disjoint intervals** (`TreeMap` in Java, `bisect` over sorted lists in Python). The transferable move: *when the value range dwarfs the operation count, index the operations, not the values.*

---

## ① Brute Force

Track coverage literally: one boolean per number.

```python
class RangeModuleBrute:
    LIMIT = 10 ** 9                       # the problem's upper bound on coordinates

    def __init__(self):
        self.covered = [False] * self.LIMIT   # 💥 ~8 GB in CPython, before we do anything

    def addRange(self, left: int, right: int) -> None:
        for x in range(left, right):          # up to 10^9 iterations for ONE call
            self.covered[x] = True

    def queryRange(self, left: int, right: int) -> bool:
        return all(self.covered[left:right])  # scans the whole span

    def removeRange(self, left: int, right: int) -> None:
        for x in range(left, right):
            self.covered[x] = False
```

**Why it's the natural first attempt:** it's the *definition* of the problem, transcribed. "Covered" is a property of each number, so store a flag per number. Nothing is subtle, nothing is wrong — logically it returns the right answers every time.

**Why it's not enough:** two independent walls, and you should name both.

1. **Memory.** `10^9` booleans. In CPython a `list` of `bool` is ~8 bytes per slot → **~8 GB**. Even a tight `bytearray` is 1 GB. The allocation alone kills you before the first `addRange`.
2. **Time.** A single `addRange(0, 10**9)` is a billion writes. With `10^4` calls that's up to `10^13` operations — hours, not milliseconds.

And here's the insult: after `addRange(0, 10**9)` you've written a billion cells to represent **one fact** — "everything is covered." The work is proportional to the *size of the range*, when it should be proportional to the *number of ranges*.

**Complexity:** Time `O(right − left)` per operation — `O(R)` where `R = 10^9`. Space `O(R)`.

*(A `set` of covered integers swaps the fixed 8 GB for "only what's covered," but `addRange(0, 10**9)` still inserts a billion elements. Same wall, later.)*

---

## ② Optimised Solution

Keep the covered set as a list of **disjoint, non-touching, sorted, half-open intervals**. Two parallel sorted lists — `starts` and `ends` — let plain `bisect` find the affected slice, and a list-splice replaces it.

**The invariant (say this out loud before you code):**
> `starts` and `ends` are sorted, `starts[k] < ends[k]`, and `ends[k] < starts[k+1]` — strictly. Adjacent intervals never touch; touching ones were merged on write.

```python
import bisect

class RangeModule:
    def __init__(self):
        self.starts = []          # sorted starts of disjoint [start, end) intervals
        self.ends = []            # ends[k] pairs with starts[k]; ends[k] < starts[k+1]

    def addRange(self, left: int, right: int) -> None:
        # First interval that reaches us: end >= left  (>= so a TOUCHING one is absorbed)
        i = bisect.bisect_left(self.ends, left)
        # First interval strictly past us: start > right (> so a TOUCHING one is absorbed)
        j = bisect.bisect_right(self.starts, right)

        if i < j:                                   # intervals [i, j) all merge into us
            left = min(left, self.starts[i])        # leftmost start in the group
            right = max(right, self.ends[j - 1])    # rightmost end in the group

        self.starts[i:j] = [left]                   # splice the whole group out,
        self.ends[i:j] = [right]                    # put ONE merged interval back

    def queryRange(self, left: int, right: int) -> bool:
        # The only interval that could contain us: the last one starting at or before left
        k = bisect.bisect_right(self.starts, left) - 1
        return k >= 0 and self.ends[k] >= right     # one interval must cover it all

    def removeRange(self, left: int, right: int) -> None:
        # Strict this time: touching is NOT overlapping, so it must survive untouched.
        i = bisect.bisect_right(self.ends, left)    # first interval with end  >  left
        j = bisect.bisect_left(self.starts, right)  # first interval with start >= right

        new_s, new_e = [], []
        if i < j:
            if self.starts[i] < left:               # left fragment survives
                new_s.append(self.starts[i]); new_e.append(left)
            if self.ends[j - 1] > right:            # right fragment survives
                new_s.append(right); new_e.append(self.ends[j - 1])

        self.starts[i:j] = new_s                    # everything in between is deleted
        self.ends[i:j] = new_e
```

**Walk the example** — `addRange(10,20)`, `removeRange(14,16)`, then the three queries:

| Call | Intervals before | `i`, `j` | What happens | Intervals after |
|---|---|---|---|---|
| `addRange(10,20)` | `[]` | `i=0, j=0` | `i == j` → nothing to merge, pure insert | `[(10,20)]` |
| `removeRange(14,16)` | `[(10,20)]` | `i=0, j=1` | `10 < 14` → keep `(10,14)`; `20 > 16` → keep `(16,20)`; middle deleted | `[(10,14),(16,20)]` |
| `queryRange(10,14)` | `[(10,14),(16,20)]` | `k=0` | `ends[0]=14 >= 14` ✓ | → **true** |
| `queryRange(13,15)` | `[(10,14),(16,20)]` | `k=0` | `ends[0]=14 >= 15`? **no** | → **false** |
| `queryRange(16,17)` | `[(10,14),(16,20)]` | `k=1` | `ends[1]=20 >= 17` ✓ | → **true** |

And a merge run, to see `addRange` swallow a group and bridge a gap:

| Call | Before | `i`, `j` | Merged bounds | After |
|---|---|---|---|---|
| `addRange(10,14)` | `[]` | `0, 0` | — | `[(10,14)]` |
| `addRange(16,20)` | `[(10,14)]` | `1, 1` | — | `[(10,14),(16,20)]` |
| `addRange(12,17)` | `[(10,14),(16,20)]` | `0, 2` | `min(12,10)=10`, `max(17,20)=20` | `[(10,20)]` |
| `addRange(25,30)` | `[(10,20)]` | `1, 1` | — | `[(10,20),(25,30)]` |
| `addRange(20,25)` | `[(10,20),(25,30)]` | `0, 2` | `min(20,10)=10`, `max(25,30)=30` | `[(10,30)]` |

That last row is the payoff: `[20,25)` only *touches* its neighbors on both sides — no shared point at all — yet it correctly fuses three intervals into one. That's `bisect_left` on `ends` (`>=`) and `bisect_right` on `starts` (`>`) doing their job.

**Why it's correct:**

- **The slice is exactly right.** `ends` and `starts` are both sorted (the intervals are disjoint), so `bisect_left(ends, left)` gives the first interval with `end >= left`, and `bisect_right(starts, right)` gives the first with `start > right`. Every index in `[i, j)` satisfies **both** — i.e. touches or overlaps `[left, right)`. Nothing outside `[i, j)` can reach us: below `i`, `end < left`; at or above `j`, `start > right`.
- **`add` restores the invariant.** The merged interval spans from the smallest start in the group to the largest end, so it covers the group *and* `[left, right)`. Its left neighbor (index `i−1`) has `end < left ≤` the merged start, and its right neighbor has `start > right`, so both remain strictly separated. Non-touching survives.
- **`remove` restores it too.** The strict searches pick only intervals that genuinely *overlap*. `starts[i]` is the smallest start in that group and `ends[j−1]` the largest end, so the only pieces that can survive are the head `[starts[i], left)` and the tail `[right, ends[j−1])` — everything strictly between is fully inside `[left, right)` and gets deleted. Each surviving fragment is non-empty exactly when its guard passes.
- **`query` needs only one interval.** Because intervals never touch, coverage of `[left, right)` can't be assembled from two pieces — there'd be a gap between them. So it's covered iff **one** interval contains it, and the only candidate is the last one starting at or before `left`.

**Complexity:** `queryRange` is `O(log n)`. `addRange` / `removeRange` are `O(log n)` to locate plus `O(n)` for the list splice, where `n` = number of stored intervals (`n ≤ 10^4`). Space `O(n)`.

> **Why the `O(n)` splice is fine in practice:** an `addRange` that touches `m` intervals *destroys* `m` of them and creates one — so a long merge **shrinks** the structure. Each interval can be born once and merged away once, so total merge work across all calls is amortized `O(total calls)`. `removeRange` adds at most one net interval per call. `n` never exceeds the number of calls. At `10^4` calls the splice is memmove over a small list — genuinely faster than a fancier structure. Say that trade-off out loud; don't pretend the `O(n)` isn't there.

> **The compact one-list variant** (worth knowing — it's the classic short answer). Store a *single* flat sorted list of boundaries `[s₁, e₁, s₂, e₂, …]`. Then **parity is the state**: even index = a start, odd index = an end, and a point is covered iff an odd number of boundaries are `≤` it.
>
> ```python
> import bisect
>
> class RangeModule:
>     def __init__(self):
>         self.b = []                                # flat sorted boundary list
>
>     def addRange(self, left: int, right: int) -> None:
>         i = bisect.bisect_left(self.b, left)
>         j = bisect.bisect_right(self.b, right)
>         # keep `left` only if it lands OUTSIDE a covered run (even index), same for `right`
>         self.b[i:j] = ([left] if i % 2 == 0 else []) + ([right] if j % 2 == 0 else [])
>
>     def queryRange(self, left: int, right: int) -> bool:
>         i = bisect.bisect_right(self.b, left)
>         j = bisect.bisect_left(self.b, right)
>         return i == j and i % 2 == 1               # no boundary inside, and we're in a run
>
>     def removeRange(self, left: int, right: int) -> None:
>         i = bisect.bisect_left(self.b, left)
>         j = bisect.bisect_right(self.b, right)
>         self.b[i:j] = ([left] if i % 2 == 1 else []) + ([right] if j % 2 == 1 else [])
> ```
>
> Half the code, identical behaviour (I cross-checked both against a brute-force boolean array). But the parity trick is hard to *defend* under questioning — lead with the explicit-intervals version, then offer this one as "and here's the compressed form."

---

## ③ Space Optimization

**Already optimal — and this is the whole point of the problem, so say it with confidence.**

The naive solution's space is `O(R)` where `R = 10^9` is the **coordinate range**. Ours is `O(n)` where `n` is the **number of disjoint intervals currently stored** — and `n` is bounded by the number of calls (`10^4`), because every `addRange` adds at most one interval and every `removeRange` splits at most one into two. `addRange(0, 10**9)` costs us **two integers**, not a gigabyte.

So the "space optimization" isn't a follow-up step you bolt on — it *is* the optimisation. We didn't compress a big structure; we changed what we store from *points* to *boundaries*, and the coordinate range fell out of the complexity entirely.

```python
# No further space-optimised variant exists.
# We already store only the O(n) interval boundaries — never the O(10^9) coordinates.
# You cannot go below O(n): each disjoint covered interval is an independent fact
# that a future queryRange can distinguish, so it must be remembered.
```

**Complexity:** Time `O(log n)` query, `O(log n + n)` add/remove. Space `O(n)`, independent of the `10^9` coordinate range.

> Say it out loud: *"My space is O(n) in the number of intervals, not O(10^9) in the coordinate range — that decoupling is the actual solution. And O(n) is the floor: two separated covered intervals are distinguishable by some future query, so I can't forget either one."* Naming *why* the floor exists beats hand-waving.

---

## Java (for Java interviewers)

`TreeMap<Integer, Integer>` mapping `start → end` is the canonical fit: `floorKey` finds the one interval that can reach us, and `subMap(...).clear()` is the splice.

```java
import java.util.TreeMap;

class RangeModule {
    // start -> end, for disjoint half-open [start, end) intervals. None ever touch.
    private final TreeMap<Integer, Integer> map = new TreeMap<>();

    public void addRange(int left, int right) {
        Integer s = map.floorKey(left);    // interval that might reach us from the left
        Integer e = map.floorKey(right);   // interval that might reach us from the right
        if (s != null && map.get(s) >= left) {
            left = s;                      // >= absorbs a merely TOUCHING interval
        }
        if (e != null && map.get(e) > right) {
            right = map.get(e);            // extend our end to swallow it
        }
        map.put(left, right);              // write the merged interval...
        map.subMap(left, false, right, true).clear();   // ...then delete everything it ate
    }

    public boolean queryRange(int left, int right) {
        Integer s = map.floorKey(left);    // the ONLY candidate, since none touch
        return s != null && map.get(s) >= right;
    }

    public void removeRange(int left, int right) {
        Integer s = map.floorKey(left);
        Integer e = map.floorKey(right);
        if (e != null && map.get(e) > right) {
            map.put(right, map.get(e));    // surviving right fragment [right, oldEnd)
        }
        if (s != null && map.get(s) > left) {
            map.put(s, left);              // surviving left fragment [oldStart, left)
        }
        map.subMap(left, true, right, false).clear();   // delete the middle
    }
}
```

Java wins on paper here: `subMap().clear()` is `O(log n + k)` for the `k` entries removed, so `add`/`remove` are truly `O(log n)` amortized — no `O(n)` array shift. Worth one sentence in the room.

---

## Complexity Summary

| Approach | `addRange` | `queryRange` | `removeRange` | Space |
|---|---|---|---|---|
| Brute force (boolean array) | O(R) | O(R) | O(R) | O(R) = 10⁹ |
| Optimised — sorted intervals + `bisect` | O(log n + n) splice | **O(log n)** | O(log n + n) splice | O(n) |
| Optimised — `TreeMap` / balanced BST | O(log n) amortized | O(log n) | O(log n) amortized | O(n) |
| Space-optimised | — (none exists) | — | — | O(n) — already range-independent |

*(n = number of stored disjoint intervals, bounded by the number of calls. R = 10⁹, the coordinate range.)*

---

## Say it out loud (interview narration)

> *"First, the constraint that decides everything: coordinates go to 10^9 but there are only 10^4 calls. So the obvious boolean-array-of-covered-points is out — that's a gigabyte of memory and a billion writes for a single `addRange(0, 10^9)`. The fix is to stop storing points and store **intervals**: the covered set is always a union of disjoint half-open ranges, and there can never be more of them than the number of calls I've made. I keep them sorted by start and — this is the key design choice — I keep them **non-touching**, merging `[10,14)` and `[14,20)` into `[10,20)` on write. Normalizing on write makes reads trivial: since no two intervals touch, `queryRange` can only be satisfied by a **single** interval, so it's one binary search for the last interval starting at or before `left`, then check its end reaches `right` — O(log n). `addRange` binary-searches the span of intervals that touch or overlap me, merges them into one, and splices it in. `removeRange` does the mirror image with **strict** comparisons, because touching isn't overlapping — it keeps the surviving left fragment and right fragment and deletes the middle. Space is O(n) in the number of intervals, completely independent of the 10^9 range — that decoupling is the whole solution. In Java I'd use a TreeMap with floorKey and subMap().clear(), which gives O(log n) amortized updates; in Python the list splice is O(n), but n is at most 10^4 and merges shrink the structure, so it's fast in practice."*

Before you write a line, ask the one clarifying question that proves you read the spec: *"These are half-open `[left, right)`, right — so after `addRange(10,20)` and `addRange(20,30)`, is `queryRange(10,30)` true?"* (It is — they fuse.) Half-open versus closed changes **every** comparison in this problem, and pinning it first is exactly the signal Google's rubric rewards.

## Related / follow-ups
- **My Calendar I (LC 729)** — the baby version: same sorted-interval structure, but you only *reject* on overlap instead of merging. Start here if this one felt heavy.
- **My Calendar II / III (LC 731, 732)** — overlaps allowed; now you count concurrency instead of maintaining disjointness. Leads to sweep-line.
- **Insert Interval (LC 57) / Merge Intervals (LC 56)** — the one-shot, offline version of `addRange`. Same merge logic, no data structure to maintain.
- **Amount of New Area Painted Each Day (LC 2158)** — `addRange` plus "how much was *newly* covered," which is the natural interviewer follow-up here.
- **Segment tree with lazy propagation / dynamic (implicit) segment tree** — the alternative answer when the interviewer asks *"what if there were 10^6 operations, so the O(n) splice actually hurt?"* A dynamic segment tree over `[0, 10^9)` with lazy "set / clear" tags gives true `O(log R)` per operation while only allocating nodes it touches. Mention it by name; you rarely have to code it.
- **Count Integers in Intervals (LC 2276)** — the same disjoint-interval bookkeeping, but you also maintain a running total of covered length.
