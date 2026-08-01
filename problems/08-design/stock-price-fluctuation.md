# Stock Price Fluctuation

> **LeetCode:** 2034. Stock Price Fluctuation · **Difficulty:** 🟡 Medium · **Pattern:** Design / stale-entry handling (timestamp map + ordered multiset) · **Google frequency:** ⭐ high

---

## Problem

A stream of stock-price records arrives, each a `(timestamp, price)` pair — **possibly out of order**, and a timestamp you've already seen can arrive **again with a new price**, meaning the earlier record was wrong and this is a **correction**. Design a `StockPrice` class:

- `update(timestamp, price)` — record (or correct) the price at `timestamp`.
- `current()` — the price at the **latest** timestamp seen so far.
- `maximum()` — the **highest** price across all timestamps, *after* corrections.
- `minimum()` — the **lowest** price across all timestamps, *after* corrections.

**Example** (LeetCode's own):
```
update(1, 10)   // t=1 → 10
update(2, 5)    // t=2 → 5
current()  -> 5     // latest timestamp is 2
maximum()  -> 10    // the max lives in the PAST, at t=1
update(1, 3)    // correction! t=1 was never 10 — it was 3
maximum()  -> 5     // the phantom 10 is gone; max is now t=2's 5
update(4, 2)
minimum()  -> 2
```

*(The whole problem is that `update(1, 3)`: a correction can retroactively destroy your current maximum.)*

**Constraints that matter:** up to `10⁵` total calls, prices and timestamps up to `10⁹`. With `10⁵` records live, an `O(n)` scan inside `maximum()`/`minimum()` gives `10⁵ × 10⁵ = 10¹⁰` operations worst case → TLE. Every operation must be **O(log n) or better**. And because corrections exist, a running `max_so_far` variable is dead on arrival — when the max itself gets corrected downward, you'd need the second max, which a single variable never kept.

---

## 🧠 Intuition — how you'd actually arrive at this

> The problem is really two sub-problems welded together: *"what's the truth per timestamp?"* (a hash map) and *"what's the max/min of the current truths?"* (an ordered collection that survives deletions).

- **First instinct:** a dict `timestamp → price` plus a `latest` timestamp variable. `update` overwrites, `current` is one lookup. For `maximum`/`minimum`… just scan all the values. Correct, trivially handles corrections — and O(n) per query.
- **Where it hurts:** every `maximum()` call re-scans prices that haven't changed since the last call. The tempting patch — keep a running `max_price` — **breaks on corrections**: when `update(1, 3)` retracts the 10 that *was* the max, the running variable has no idea what the runner-up was. Same story for a plain max-heap: the corrected 10 is still sitting at the top, now a lie.
- **The leap:** the set of *live* prices only changes by **one removal + one insertion** per update (retract the stale price for that timestamp, insert the corrected one). So keep the live prices in a structure that supports insert, **delete-by-value**, and min/max — an **ordered multiset** (Python `SortedList`, Java `TreeMap` with counts). The hash map tells you *which* stale value to delete: `rec[timestamp]` is exactly the price the correction retracts.
- **Pattern trigger:** *"design a class where past entries can be invalidated, but you must still answer max/min/top"* → **stale-entry handling**, and there are exactly two idioms: **eager deletion** in an ordered multiset (remove the stale value the moment the correction arrives), or **lazy deletion** with heaps (push corrections as new entries, and at query time pop the top *while* it disagrees with the hash map's truth). Multiset = simpler invariant, tighter memory; lazy heaps = the same trick as Max Stack / task schedulers. Knowing *both* names is the transferable lesson — this pair reappears any time a priority structure meets in-place updates.

---

## ① Brute Force

Hash map of truths + full scan for every max/min query.

```python
class StockPriceBrute:
    def __init__(self):
        self.rec = {}       # timestamp -> latest (corrected) price
        self.latest = 0     # newest timestamp seen

    def update(self, timestamp: int, price: int) -> None:
        self.rec[timestamp] = price          # overwrite = correction handled
        self.latest = max(self.latest, timestamp)

    def current(self) -> int:
        return self.rec[self.latest]

    def maximum(self) -> int:
        return max(self.rec.values())        # O(n) scan, every single call

    def minimum(self) -> int:
        return min(self.rec.values())        # O(n) scan, every single call
```

**Why it's the natural first attempt:** the dict *is* the source of truth, so scanning it can't be wrong — corrections are free because overwriting the key is the correction.

**Why it's not enough:** `10⁵` calls with up to `10⁵` live records means a worst case near `10¹⁰` comparisons — TLE. The scan recomputes an answer that barely changed: between two `maximum()` calls, maybe one price moved. All that re-scanning is wasted work.

**Complexity:** `update`/`current` Time `O(1)`; `maximum`/`minimum` Time `O(n)`. Space `O(n)` (n = distinct timestamps).

---

## ② Optimised Solution

Keep the same truth map, and *additionally* mirror the live prices in an **ordered multiset**. On a correction, **eagerly delete** the stale price from the multiset before inserting the new one — the map tells us exactly which value went stale.

```python
from sortedcontainers import SortedList

class StockPrice:
    def __init__(self):
        self.rec = {}                 # timestamp -> latest (corrected) price
        self.prices = SortedList()    # multiset of all LIVE prices
        self.latest = 0               # newest timestamp seen

    def update(self, timestamp: int, price: int) -> None:
        if timestamp in self.rec:
            self.prices.remove(self.rec[timestamp])   # retract the stale price
        self.rec[timestamp] = price
        self.prices.add(price)
        self.latest = max(self.latest, timestamp)

    def current(self) -> int:
        return self.rec[self.latest]

    def maximum(self) -> int:
        return self.prices[-1]        # largest live price

    def minimum(self) -> int:
        return self.prices[0]         # smallest live price
```

*(`SortedList` is Python's stand-in for a balanced-BST multiset — `add`/`remove` in `O(log n)`, ends readable in `O(1)`.)*

**Walk the example:**

| Call | `rec` after | `prices` after | `latest` | returns |
|---|---|---|---|---|
| `update(1,10)` | {1:10} | [10] | 1 | — |
| `update(2,5)` | {1:10, 2:5} | [5, 10] | 2 | — |
| `current()` | — | — | 2 | `rec[2]` = **5** ✅ |
| `maximum()` | — | — | — | `prices[-1]` = **10** ✅ |
| `update(1,3)` | {1:3, 2:5} | remove 10 → add 3 → [3, 5] | 2 (1 < 2) | — |
| `maximum()` | — | — | — | `prices[-1]` = **5** ✅ |
| `update(4,2)` | {1:3, 2:5, 4:2} | [2, 3, 5] | 4 | — |
| `minimum()` | — | — | — | `prices[0]` = **2** ✅ |

The correction row is the whole problem: `rec[1]` told us the stale value was 10, so we surgically removed **one copy** of 10 and the phantom maximum died instantly.

**Why it's correct:** invariant — *`prices` always holds exactly one entry per timestamp in `rec`: that timestamp's most recent price.* Every `update` preserves it (new timestamp → one insert; correction → one remove of the old truth + one insert of the new). Given the invariant, `prices[-1]`/`prices[0]` are by definition the max/min over current truths, and `rec[latest]` is the price at the newest timestamp. Duplicates are safe: if two timestamps both hold price 7 and one is corrected, `remove(7)` deletes one copy and the other timestamp's 7 survives — exactly right, because a multiset counts *occurrences*, not values.

**The lazy-deletion alternative (know it by name):** two heaps of `(price, timestamp)` pairs; `update` just pushes onto both (never deletes); `maximum()` pops the top *while* `heap_top.price != rec[heap_top.timestamp]` — a stale entry from before a correction — then reads the top. Same `O(log n)` amortized (each entry is popped at most once), no third-party dependency, but the heaps hold one entry per **update call**, not per timestamp, and every query starts with a "is the top a lie?" loop. Great answer when the interviewer bans `SortedList`; the multiset is the cleaner primary.

**Complexity:** `update` Time `O(log n)`; `current`/`maximum`/`minimum` Time `O(1)` (`O(log n)` overall per op is the safe claim). Space `O(n)`, n = distinct timestamps.

---

## ③ Space Optimization

**Already optimal — here's why.** Any correct structure must remember the price at *every* distinct timestamp: a future `update` can correct the current maximum away, making the runner-up the answer — and the runner-up of the runner-up, and so on. So `Ω(distinct timestamps)` is forced by the queries themselves; our `O(n)` (one map entry + one multiset entry per timestamp) meets that floor with constant factor 2.

```python
# No smaller variant exists: corrections can dethrone any current max/min,
# so every timestamp's live price must stay queryable. O(n) is the floor.
# Note the multiset even BEATS the lazy-heap variant on space:
#   multiset  -> one entry per DISTINCT timestamp (corrections replace)
#   lazy heaps-> one entry per UPDATE CALL (corrections accumulate until popped)
```

**Complexity:** Time unchanged, Space `O(n)` — the floor.

> Naming the floor is the strong move: *"I can't beat O(n) space, because any timestamp's price can become the max after future corrections — the structure must keep them all."*

---

## Java (for Java interviewers)

`TreeMap<price, count>` is Java's ordered multiset: `firstKey()`/`lastKey()` give min/max in `O(log n)`, and the count handles duplicate prices across timestamps.

```java
class StockPrice {
    private final Map<Integer, Integer> rec = new HashMap<>();        // timestamp -> latest price
    private final TreeMap<Integer, Integer> prices = new TreeMap<>(); // price -> count (multiset)
    private int latest = 0;

    public void update(int timestamp, int price) {
        Integer stale = rec.put(timestamp, price);      // returns old price if correction
        if (stale != null) {                            // retract exactly one copy
            int c = prices.get(stale);
            if (c == 1) prices.remove(stale);
            else prices.put(stale, c - 1);
        }
        prices.merge(price, 1, Integer::sum);           // insert the new truth
        latest = Math.max(latest, timestamp);
    }

    public int current() { return rec.get(latest); }
    public int maximum() { return prices.lastKey(); }
    public int minimum() { return prices.firstKey(); }
}
```

---

## Complexity Summary

| Approach | update | current | maximum / minimum | Space |
|---|---|---|---|---|
| Brute force (map + scan) | O(1) | O(1) | O(n) | O(n) |
| Optimised (map + ordered multiset) | O(log n) | O(1) | O(1)–O(log n) | O(n) — one entry per distinct timestamp |
| Lazy two heaps | O(log U) | O(1) | amortized O(log U) | O(U) — one entry per update call |

*(n = distinct timestamps, U = total update calls; space is already optimal — see ③.)*

---

## Say it out loud (interview narration)

> *"There are two questions hiding here: the truth per timestamp, and the max/min over those truths. The truth is a hash map — timestamp to price — and overwriting a key is how corrections happen; with a `latest` variable, `current` is O(1). The dangerous part is max and min: a running variable or a plain heap breaks the moment a correction retracts the current maximum, because neither kept the runner-up. So I mirror the live prices in an ordered multiset. On a correction the map tells me exactly which stale value to delete — remove one copy, insert the new price, O(log n) — and max and min are just the ends of the multiset. Space is O(n) and that's the floor: any timestamp's price can become the max after future corrections, so they all must stay queryable. If I couldn't use a multiset, I'd do lazy deletion with two heaps — push every update, and at query time pop the top while it disagrees with the map."*

Clarifying questions to ask before coding — exactly what Google's rubric rewards: *"Can the same timestamp be updated more than once — and is the latest write always the truth?"* and *"Can records arrive out of timestamp order?"* Both are yes, and both answers shape the design.

## Related / follow-ups
- **Max Stack (716)** — the canonical lazy-deletion problem: two structures + soft-deleted entries reconciled at read time.
- **Snapshot Array (1146)** — same section: versioned truth per index instead of per timestamp.
- **Time Based Key-Value Store (981)** — timestamped truth with retrieval *at* a past time instead of corrections.
- **Find Median from Data Stream (295)** — two heaps over a stream; add lazy deletion and you get its harder sibling, Sliding Window Median (480).
- **Design a leaderboard (1244)** — scores change in place while you answer top-K: the same stale-entry dilemma.
