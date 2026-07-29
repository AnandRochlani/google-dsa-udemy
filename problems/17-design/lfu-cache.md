# LFU Cache

> **LeetCode:** 460. LFU Cache · **Difficulty:** 🔴 Hard · **Pattern:** Design (hash maps + buckets of doubly linked lists) · **Google frequency:** medium

---

## Problem

Design a **Least-Frequently-Used cache** with fixed `capacity`:

- `get(key)` — return the value if present, else `-1`. A successful get **increments that key's use-count**.
- `put(key, value)` — insert/update (an update also increments the count). If full, **evict the key with the smallest use-count**; if several keys tie for the smallest count, **evict the least-recently-used among them**.

**Both operations must run in average O(1).**

**Example:**
```
LFUCache cache = new LFUCache(2)
put(1, 1)        // counts: {1:1}
put(2, 2)        // counts: {1:1, 2:1}
get(1)   -> 1    // key 1 count → 2. counts: {1:2, 2:1}
put(3, 3)        // full. min count is 1 (key 2) → evict 2. counts: {1:2, 3:1}
get(2)   -> -1   // evicted
get(3)   -> 3    // key 3 count → 2. counts: {1:2, 3:2}
put(4, 4)        // full. min count 2, tie between 1 and 3 → evict LRU of them = 1
get(1)   -> -1   // evicted
get(3)   -> 3
get(4)   -> 4
```

**Constraints that matter:** up to `2 × 10⁵` calls, **O(1) required per operation**. LFU is strictly harder than LRU because eviction depends on *two* keys ranked by frequency, and *within* a frequency class you still need LRU tie-breaking. Doing all of that in O(1) is the whole challenge.

---

## 🧠 Intuition — how you'd actually arrive at this

> Same design method as LRU: match each required operation to a structure. LFU just adds a **second ranking dimension** (frequency), so we layer LRU *inside* each frequency level.

What must be O(1):

1. **Value lookup by key** → `key → (value, freq, node)` **hash map**. Standard.
2. **"Bump a key's frequency"** → move it from its current frequency group to the next one, O(1).
3. **"Find the eviction victim"** → the least-frequently-used key; on ties, the least-recently-used within that lowest frequency.

- **The core idea:** group keys **by frequency**. Keep a hash map `freq → bucket`, where each bucket holds all keys that currently have exactly that frequency. Track `min_freq`, the smallest frequency present. Eviction always comes from `bucket[min_freq]`.
- **Within a bucket, break ties by recency.** Which structure gives O(1) removal from either end *and* O(1) removal of an arbitrary key? The **doubly linked list** — exactly the LRU trick. So each bucket is an LRU list: most-recent at the head, least-recent at the tail. On a tie, evict the tail of `bucket[min_freq]`.
- **Bumping a key from freq `f` to `f+1`:** unlink its node from `bucket[f]` (O(1), doubly linked list), add it to the head of `bucket[f+1]` (O(1)), update its stored freq. If `bucket[f]` became empty *and* `f == min_freq`, then `min_freq += 1`.
- **Why `min_freq` only ever needs `+= 1` on a bump:** when we empty out the current minimum bucket by promoting its last key, that key moved to `f+1`, so the new minimum is exactly `f+1`. No search needed — that's what keeps it O(1). On a fresh `put`, the new key has freq 1, so `min_freq` resets to 1.

**Pattern trigger:** *"rank by frequency in O(1), LRU tie-break"* → **hash map + `freq → doubly linked list` buckets + a `min_freq` counter**. It's LRU with one more axis. In Python, each bucket can be an `OrderedDict` (a ready-made hash-map-over-DLL) to avoid hand-writing node splicing.

---

## ① Brute Force

Store each key's `(value, freq, insertion_time)`. On eviction, scan every entry to find the minimum `(freq, time)`.

```python
class LFUCacheBrute:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.store = {}          # key -> [value, freq, tick]
        self.tick = 0            # global counter for recency tie-break

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store[key][1] += 1          # bump freq
        self.tick += 1
        self.store[key][2] = self.tick   # mark recency
        return self.store[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        self.tick += 1
        if key in self.store:
            self.store[key][0] = value
            self.store[key][1] += 1
            self.store[key][2] = self.tick
            return
        if len(self.store) >= self.cap:
            # find (min freq, then min tick) — O(n) scan
            victim = min(self.store, key=lambda k: (self.store[k][1], self.store[k][2]))
            del self.store[victim]
        self.store[key] = [value, 1, self.tick]
```

**Why it's the natural first attempt:** it stores exactly the two ranking fields the spec mentions (frequency, then recency) and picks the min directly.

**Why it's not enough:** the eviction `min(...)` scans all entries → **O(n)** per `put`. With 2×10⁵ calls that's ~10¹⁰ work → **TLE**, and it violates the O(1) requirement.

**Complexity:** `get` O(1), `put` O(n) (eviction scan), Space O(capacity).

---

## ② Optimised Solution

`key_map: key → node`. `freq_map: freq → OrderedDict of key→node` (each an LRU list, newest inserted last). A `min_freq` pointer.

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.key_map = {}                       # key -> [value, freq]
        self.freq_map = defaultdict(OrderedDict)  # freq -> {key: value} in LRU order

    def _bump(self, key: int) -> None:
        value, freq = self.key_map[key]
        # remove from current freq bucket
        del self.freq_map[freq][key]
        if not self.freq_map[freq]:             # bucket emptied
            del self.freq_map[freq]
            if self.min_freq == freq:
                self.min_freq += 1              # only ever +1
        # add to freq+1 bucket (at the end = most-recent)
        self.freq_map[freq + 1][key] = value
        self.key_map[key] = [value, freq + 1]

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        self._bump(key)
        return self.key_map[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.key_map:
            self.key_map[key][0] = value
            self.freq_map[self.key_map[key][1]][key] = value  # keep bucket value fresh
            self._bump(key)
            return
        if len(self.key_map) >= self.cap:
            # evict LRU of the lowest-frequency bucket = first item inserted
            evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
            del self.key_map[evict_key]
        # insert new key at freq 1
        self.key_map[key] = [value, 1]
        self.freq_map[1][key] = value
        self.min_freq = 1                       # new key resets the minimum
```

**Walk the example** (`capacity = 2`). `freq_map` shown as `freq: [keys oldest→newest]`, `min_freq` tracked:

| Call | key_map (key:freq) | freq_map | min_freq |
|---|---|---|---|
| `put(1,1)` | {1:1} | 1:[1] | 1 |
| `put(2,2)` | {1:1, 2:1} | 1:[1,2] | 1 |
| `get(1)→1` | {1:2, 2:1} | 1:[2], 2:[1] | 1 |
| `put(3,3)` full, evict min_freq=1 LRU=2 | {1:2, 3:1} | 2:[1], 1:[3] | 1 |
| `get(2)→-1` | — | — | 1 |
| `get(3)→3` | {1:2, 3:2} | 2:[1,3] | 2 |
| `put(4,4)` full, min_freq=2 LRU=1 → evict 1 | {3:2, 4:1} | 2:[3], 1:[4] | 1 |
| `get(1)→-1` | — | — | 1 |
| `get(3)→3` | {3:3, 4:1} | 1:[4], 3:[3] | 1 |
| `get(4)→4` | {3:3, 4:2} | 3:[3], 2:[4] | 1... |

At `put(4,4)` keys 1 and 3 both had freq 2; the tie broke to key **1** because it sat at the front (oldest) of `bucket[2]` — exactly LRU-within-frequency.

**Why it's correct:** `min_freq` always names the lowest frequency currently present, because it only advances when the minimum bucket empties by promotion (new min is that bucket's freq + 1) and resets to 1 whenever a brand-new key arrives. `OrderedDict.popitem(last=False)` pops the oldest-inserted key, which is the LRU within that bucket. So eviction picks (min frequency, then min recency) — precisely the spec.

**Complexity (per operation):** Time **O(1)** — hash lookups plus `OrderedDict` insert/delete/popitem, all amortized O(1). Space **O(capacity)**.

---

## ③ Space Optimization

Already optimal — **O(capacity)**. Every stored key appears once in `key_map` and once in exactly one `freq_map` bucket, so the total is a constant factor times the number of held items, which you must store by definition. Empty buckets are deleted as soon as they drain (`del self.freq_map[freq]`), so `freq_map` never accumulates stale frequency levels.

> Honest note: LFU carries a *larger constant factor* than LRU — two hash maps plus per-bucket ordered structures — but the asymptotic space is the same O(capacity). There's no cheaper representation, because you genuinely need both the frequency axis and the recency axis to answer the eviction query in O(1).

---

## Java (for Java interviewers)

```java
class LFUCache {
    private final int cap;
    private int minFreq = 0;
    private final Map<Integer, Integer> values = new HashMap<>();   // key -> value
    private final Map<Integer, Integer> counts = new HashMap<>();   // key -> freq
    // freq -> keys in that bucket, LinkedHashSet preserves insertion (LRU) order
    private final Map<Integer, LinkedHashSet<Integer>> buckets = new HashMap<>();

    public LFUCache(int capacity) { cap = capacity; }

    public int get(int key) {
        if (!values.containsKey(key)) return -1;
        bump(key);
        return values.get(key);
    }

    public void put(int key, int value) {
        if (cap == 0) return;
        if (values.containsKey(key)) {
            values.put(key, value);
            bump(key);
            return;
        }
        if (values.size() >= cap) {
            LinkedHashSet<Integer> minBucket = buckets.get(minFreq);
            int evict = minBucket.iterator().next();   // oldest = LRU
            minBucket.remove(evict);
            values.remove(evict);
            counts.remove(evict);
        }
        values.put(key, value);
        counts.put(key, 1);
        buckets.computeIfAbsent(1, k -> new LinkedHashSet<>()).add(key);
        minFreq = 1;
    }

    private void bump(int key) {
        int f = counts.get(key);
        counts.put(key, f + 1);
        LinkedHashSet<Integer> cur = buckets.get(f);
        cur.remove(key);
        if (cur.isEmpty()) {
            buckets.remove(f);
            if (minFreq == f) minFreq++;
        }
        buckets.computeIfAbsent(f + 1, k -> new LinkedHashSet<>()).add(key);
    }
}
```

---

## Complexity Summary

| Approach | get | put | Space |
|---|---|---|---|
| Brute force (scan for min) | O(1) | O(n) | O(capacity) |
| Freq buckets + LRU lists | O(1) | O(1) | O(capacity) |

---

## Say it out loud (interview narration)

> *"LFU is LRU with a second ranking axis. I keep a hash map for O(1) value lookup, and I group keys into buckets by frequency: freq → an ordered list of keys, each bucket ordered by recency so I can break ties. A min_freq pointer tells me which bucket to evict from. A get or put bumps the key's frequency — I splice it out of its current bucket and drop it at the front of the next-higher one, all O(1) because these are doubly-linked-list-backed structures. The clever bit is that min_freq only ever increments: when I promote the last key out of the minimum bucket, the new minimum is exactly that freq plus one; and a brand-new key resets min_freq to 1. Eviction pops the oldest key of bucket[min_freq], which is the least-frequently-used and, among ties, the least-recently-used. Both ops O(1), space O(capacity)."*

## Related / follow-ups
- **LRU Cache** (146) — the simpler single-axis version; understand it first.
- **All O'one Data Structure** (432) — buckets of a doubly linked list keyed by count, inc/dec/getMax/getMin in O(1).
- **Design HashMap** (706) — the hash-map primitive underneath.
