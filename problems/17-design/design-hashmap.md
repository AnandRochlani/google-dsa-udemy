# Design HashMap

> **LeetCode:** 706. Design HashMap · **Difficulty:** 🟢 Easy · **Pattern:** Design (buckets + chaining) · **Google frequency:** medium

---

## Problem

Implement a hash map from scratch — **without** using any built-in hash table library. Support:

- `put(key, value)` — insert or update the value for `key`.
- `get(key)` — return the value for `key`, or `-1` if absent.
- `remove(key)` — delete the mapping for `key` if present.

Keys and values are non-negative integers.

**Example:**
```
MyHashMap map = new MyHashMap()
put(1, 1)
put(2, 2)
get(1)      -> 1
get(3)      -> -1   // not present
put(2, 1)          // update existing key 2
get(2)      -> 1
remove(2)
get(2)      -> -1   // removed
```

**Constraints that matter:** up to `10⁴` calls; keys in `[0, 10⁶]`. Average **O(1) per operation** is the expectation. A naive array indexed directly by key would be `10⁶` slots — wasteful and it doesn't generalize to non-integer keys — so the interviewer wants to see a real **hash + collision strategy**, not `arr[key]`.

---

## 🧠 Intuition — how you'd actually arrive at this

> This problem *is* the primitive that LRU/LFU and half of all interview solutions lean on. Building it shows you understand why hash maps are "O(1)."

- **First instinct:** "keys are integers, just make a giant array `arr[key]`." That's **direct addressing** — works, but needs `10⁶` slots for `10⁴` entries (99% empty) and collapses the moment keys aren't small integers. It also isn't really "designing a hash map."
- **The compression step:** map any key into a small, fixed number of slots with a **hash function** — the simplest being `key % B` for `B` buckets. Now the table is size `B` (say 1000), not `10⁶`.
- **Where it hurts:** two different keys can hash to the same bucket — a **collision** (`1` and `1001` both give `% 1000 == 1`). We must store multiple entries per bucket without losing any.
- **The leap — separate chaining:** each bucket holds a small **list of (key, value) pairs**. `put`/`get`/`remove` hash to the bucket, then scan that one short list. With a decent bucket count and roughly uniform keys, each list holds ~`n/B` items — a small constant — so operations are **average O(1)**.
- **Pattern trigger:** *"build a map / avoid collisions"* → **array of buckets + chaining**, where each bucket is a list you linearly scan. (The alternative, open addressing / linear probing, stores entries directly in the array and probes to the next slot on collision — worth naming as an alternative.)

---

## ① Brute Force

Direct addressing: one array with a slot for every possible key, `-1` meaning empty.

```python
class MyHashMapBrute:
    def __init__(self):
        self.arr = [-1] * (10**6 + 1)   # a slot for every possible key

    def put(self, key: int, value: int) -> None:
        self.arr[key] = value

    def get(self, key: int) -> int:
        return self.arr[key]

    def remove(self, key: int) -> None:
        self.arr[key] = -1
```

**Why it's the natural first attempt:** keys are bounded integers, so you *can* index directly — every operation is a genuine O(1) array access.

**Why it's not enough:** it allocates `10⁶ + 1` slots regardless of how few keys you store — **O(key-range) space**, mostly wasted — and the technique dies for large or non-integer keys. The interviewer wants a hash function and collision handling, not this.

**Complexity:** Time O(1) per op, Space **O(K)** where K is the key range (`10⁶`).

---

## ② Optimised Solution

Fixed number of buckets; hash with `key % B`; each bucket is a list of `[key, value]` pairs (separate chaining).

```python
class MyHashMap:
    def __init__(self):
        self.B = 1009                       # a prime bucket count reduces clustering
        self.buckets = [[] for _ in range(self.B)]

    def _hash(self, key: int) -> int:
        return key % self.B

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value             # update existing
                return
        bucket.append([key, value])         # new key

    def get(self, key: int) -> int:
        bucket = self.buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)               # unlink from chain
                return
```

**Walk the example** with `B = 1009`:

- `put(1, 1)` → bucket `1 % 1009 = 1` → `[[1,1]]`.
- `put(2, 2)` → bucket `2` → `[[2,2]]`.
- `get(1)` → bucket `1`, scan → found → `1`.
- `get(3)` → bucket `3`, empty → `-1`.
- `put(2, 1)` → bucket `2`, key `2` already there → update value to `1` → `[[2,1]]`.
- `get(2)` → `1`.
- `remove(2)` → bucket `2`, pop the `[2,1]` pair → `[]`.
- `get(2)` → bucket `2` empty → `-1`.

A collision demo: `put(1010, 9)` also lands in bucket `1` (`1010 % 1009 == 1`), so that bucket becomes `[[1,1],[1010,9]]` — both coexist, and `get` distinguishes them by comparing the stored key.

**Why it's correct:** every key deterministically maps to one bucket, and within a bucket we compare the *full* key, so distinct keys never shadow each other even when they collide. Update-in-place keeps at most one pair per key.

**Complexity (per operation):** average **O(1 + n/B)** ≈ O(1) with a good bucket count and roughly uniform keys; worst case O(n) if every key hashes to one bucket. Space **O(n + B)** — proportional to entries stored plus the bucket array, not to the key range.

---

## ③ Space Optimization

The chaining version is already the space-efficient design — **O(n + B)** versus the brute force's **O(key-range)**. For `10⁴` entries that's ~`10⁴` vs ~`10⁶`, a 100× reduction, and it's the right asymptotic (you must store the entries you're asked to hold).

Two honest refinements you'd mention:

- **Bucket count is a time/space knob.** More buckets → shorter chains → faster, but more empty-array overhead. Production maps **resize** (double `B` and rehash) when the load factor `n/B` crosses ~0.75 to keep chains short; here a fixed prime like `1009` is fine for the given limits.
- **Open addressing** (linear/quadratic probing) stores entries directly in the array with no per-bucket lists, saving the list objects' overhead — but it complicates deletion (needs tombstones) and degrades badly at high load factor. Chaining is simpler to get right in an interview.

---

## Java (for Java interviewers)

```java
class MyHashMap {
    private static final int B = 1009;
    private final List<int[]>[] buckets;

    @SuppressWarnings("unchecked")
    public MyHashMap() {
        buckets = new List[B];
        for (int i = 0; i < B; i++) buckets[i] = new LinkedList<>();
    }

    private int hash(int key) { return key % B; }

    public void put(int key, int value) {
        List<int[]> bucket = buckets[hash(key)];
        for (int[] pair : bucket) {
            if (pair[0] == key) { pair[1] = value; return; }
        }
        bucket.add(new int[]{key, value});
    }

    public int get(int key) {
        for (int[] pair : buckets[hash(key)]) {
            if (pair[0] == key) return pair[1];
        }
        return -1;
    }

    public void remove(int key) {
        List<int[]> bucket = buckets[hash(key)];
        Iterator<int[]> it = bucket.iterator();
        while (it.hasNext()) {
            if (it.next()[0] == key) { it.remove(); return; }
        }
    }
}
```

---

## Complexity Summary

| Approach | put / get / remove | Space |
|---|---|---|
| Direct addressing (brute) | O(1) | O(key-range) ≈ 10⁶ |
| Buckets + chaining | avg O(1), worst O(n) | O(n + B) |

---

## Say it out loud (interview narration)

> *"Direct-indexing an array by key works but wastes a million slots and doesn't generalize, so I'll build a real hash map: a fixed array of buckets and a hash function, key mod bucket-count. Collisions are inevitable, so each bucket is a small list of key-value pairs — separate chaining. put/get/remove hash to a bucket then scan that one short list, comparing full keys so colliding keys don't shadow each other. With a prime bucket count and roughly uniform keys the chains stay short, so it's average O(1), and space is O(n plus bucket-count) instead of O(key-range). If I wanted production quality I'd resize and rehash when the load factor gets high."*

## Related / follow-ups
- **Design HashSet** (705) — same structure, store keys only.
- **LRU / LFU Cache** (146 / 460) — build on top of a hash map.
- **Two Sum** (1) — the canonical "why hash maps matter" problem.
- **Insert Delete GetRandom O(1)** (380) — hash map paired with an array.
