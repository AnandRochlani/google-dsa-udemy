# 🎬 Recording Script — Design HashMap

**Pattern: Design (buckets + chaining) · LeetCode 706 · Easy · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** every problem where we said "just use a hash map" — this is what's underneath.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a montage flashes — Two Sum, LRU, LFU — each with the phrase "just use a hash map" stamped on it. Then a record-scratch freeze: "...but WHY is it O(1)?"]**

> Every problem so far, we leaned on the same magic words: *"just use a hash map — O(1) lookup."* We treated it like a spell.
>
> Now Google calls the bluff: *"Build one. From scratch. No `dict`, no `HashMap`."*
>
> This is tagged Easy, but it's secretly the most important problem in the set — because when you've built the thing everything else stands on, you finally understand **why** all those O(1)s were true. And you'll see the one idea that makes a million-slot problem fit in a thousand slots. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, a call list: put(1,1), put(2,2), get(1)→1, get(3)→-1, put(2,1), get(2)→1, remove(2), get(2)→-1.]**

> One line: **implement `put`, `get`, and `remove` for integer keys — without any built-in hash table.**
>
> `put(key, value)` inserts or updates. `get(key)` returns the value or `-1` if it's not there. `remove(key)` deletes it. Keys are non-negative integers, up to a million.
>
> Watch `put(2,2)` then `put(2,1)` — the second one *updates* key 2, doesn't duplicate it. And `remove(2)` then `get(2)` gives `-1`. Simple contract. The interest is entirely in *how* we back it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a giant array stretching off-screen, indices 0 to 1,000,000. Two lonely filled slots at index 1 and 2; the rest gray and empty.]**

> Here's the first instinct — and it *works*. Keys are integers, so just make an array with a slot for every possible key. `put(2,2)`? Set `arr[2] = 2`. `get(2)`? Return `arr[2]`. Every operation is a genuine O(1) array access.

**[VISUAL: the array fills only 2 slots out of a million; a "wasted" meter reads 99.9998%.]**

> But look at the array. Keys go up to a million, so we allocated a **million-slot** array — to store maybe a handful of keys. Ninety-nine-point-nine percent empty. This is called *direct addressing*, and it's a memory catastrophe. Worse — the instant keys aren't small integers, say strings, it collapses entirely.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the vast empty array. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The pain: the array's size is tied to the **range of possible keys**, not the number of keys we actually store. A million slots for ten entries.
>
> **LEARNER:** So shrink the array — say a thousand slots — and do `key % 1000` to pick a slot? That squashes any key into range.
>
> **TEACHER:** That's exactly the leap — and it opens a brand-new problem. Pause and predict: **if I map key `1` and key `1001` both into slot `1` with `% 1000`... what happens to the first one when the second arrives?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: keys 1 and 1001 both flying into slot 1. A "COLLISION" spark. Then slot 1 grows a little list holding BOTH pairs.]**

> **TEACHER:** Two different keys can land in the same slot — that's a **collision**. `1` and `1001` both hash to slot 1. If we just overwrite, we lose data. So we can't store a single value per slot.
>
> The fix — **separate chaining**: each slot holds a small **list of key-value pairs**. When two keys collide, they *coexist* in that slot's list. To `get`, hash to the slot, then scan that one short list comparing the full key.
>
> **[VISUAL: analogy — a wall of mailboxes (the buckets). Multiple tenants sharing one mailbox each drop a labeled envelope inside; the mail carrier reads labels to find yours.]**
>
> Think of a wall of a thousand mailboxes. Your key picks your mailbox by `key % 1000`. Several people might share a mailbox — so inside, each envelope is labeled with its full key. To find yours, open the box and read the few labels inside. With a decent number of boxes and keys spread evenly, each box holds only a couple of envelopes — so the scan is a tiny constant. That's why it's **average O(1)**.

---

## 6. THE KEY MOVE (signaling) — `4:25`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Array of buckets + hash to a bucket + scan that bucket's short list."]**

> The key move: **a fixed array of buckets, a hash function to pick the bucket, and a short list per bucket to absorb collisions.** Hash to find the bucket, scan the list to find the key. That three-part recipe — table, hash, chaining — *is* a hash map.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Init with a prime bucket count.]**

> Set up the buckets. A **prime** count reduces clustering.

```python
class MyHashMap:
    def __init__(self):
        self.B = 1009                       # prime bucket count
        self.buckets = [[] for _ in range(self.B)]

    def _hash(self, key):
        return key % self.B
```

> **[VISUAL: add put(), highlight the update-vs-append branch.]** `put` — if the key's already in its bucket, update in place; otherwise append.

```python
    def put(self, key, value):
        bucket = self.buckets[self._hash(key)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value             # update existing
                return
        bucket.append([key, value])         # new key
```

> **[VISUAL: add get().]** `get` — hash, scan, compare the full key.

```python
    def get(self, key):
        bucket = self.buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1
```

> **[VISUAL: add remove().]** `remove` — find the pair, pop it out of its chain.

```python
    def remove(self, key):
        bucket = self.buckets[self._hash(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: full class; spotlight lines.]**

> Why each piece.
>
> `self.B = 1009`, a prime — primes scatter keys more evenly across buckets, avoiding the clustering you'd get if the bucket count shared factors with the keys. Fewer collisions, shorter chains.
>
> In `put`, we scan the bucket *before* appending — that's what makes `put(2,2)` then `put(2,1)` an update, not a duplicate. At most one pair per key.
>
> Everywhere, we compare `pair[0] == key` — the **full** key, not just the hash.
>
> **LEARNER:** Why re-check the full key? They're already in the same bucket — didn't the hash prove they match?
>
> **TEACHER:** No — the hash only proves they landed in the same *bucket*. `1` and `1001` share a bucket but are different keys. The hash narrows you to a short list; the full-key comparison is what actually identifies *your* entry. Skip it and you'd return `1001`'s value when asked for `1`.

---

## 9. DRY-RUN THE CODE — `7:15`
*(worked example — prove it, show a collision)*

**[VISUAL: buckets 1, 2, 3 drawn; pairs move in and out.]**

> Run the example, B = 1009.

| Call | bucket | result |
|---|---|---|
| put(1,1) | 1 → [[1,1]] | — |
| put(2,2) | 2 → [[2,2]] | — |
| get(1) | scan bucket 1 → found | **1** |
| get(3) | bucket 3 empty | **-1** |
| put(2,1) | bucket 2, key 2 exists → update | [[2,1]] |
| get(2) | bucket 2 | **1** |
| remove(2) | bucket 2 → pop | [] |
| get(2) | bucket 2 empty | **-1** |

> Now the collision proof: `put(1010, 9)` — `1010 % 1009 = 1` — lands in bucket 1 too. Bucket 1 becomes `[[1,1], [1010,9]]`. Both live there; `get(1)` still returns 1 because we compare the full key. Collision handled, no data lost.

---

## 10. COMPLEXITY, OUT LOUD — `8:00`
*(transfer to interview)*

**[VISUAL: two rows — Direct addressing: O(1) time, O(key-range) space. Chaining: avg O(1), O(n+B) space.]**

> Out loud: *"With a good bucket count and roughly uniform keys, each chain holds about n-over-B items — a small constant — so `put`, `get`, and `remove` are **average O(1)**. Worst case, if every key collides into one bucket, it degrades to O(n). Space is O(n plus B) — proportional to what I actually store plus the bucket array, **not** the key range."*
>
> That "average O(1), worst O(n), and here's why" sentence — that's the answer to *"why is a hash map O(1)?"* you can now give with authority.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:40`
*(depth + honesty)*

**[VISUAL: side by side — brute O(10⁶) vs chaining O(10⁴), a 100× bar shrink. Then a note: "resize when load factor > 0.75".]**

> Chaining already crushes the brute force on space — O(n plus B) versus O(key-range), a hundred-fold shrink for these limits. Two honest refinements to name:
>
> **Bucket count is a time/space dial.** More buckets → shorter chains → faster, but more empty-array overhead. Real hash maps **resize** — double B and rehash — when the load factor `n/B` crosses about 0.75, keeping chains short as they grow. Here a fixed prime is fine.
>
> **The alternative — open addressing.** Instead of per-bucket lists, store entries right in the array and *probe* to the next slot on a collision. Saves the list objects, but deletion needs tombstones and it degrades badly when full. Chaining is simpler to get right under interview pressure. Naming both shows you know the landscape.

---

## 12. YOUR TURN (active recall) — `9:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Design HashSet (LC 705)". Blank editor.]**

> Before the next video, try **Design HashSet** — same structure, but store *only keys*, no values. It's this problem with the value field deleted. If you can rebuild it from memory in five minutes, you truly own the hash-map internals.
>
> Then, for bonus: sketch how you'd add **resizing**. Don't peek.

---

## 13. LOCK IT IN — `9:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Direct addressing wastes O(key-range)** — a hash function compresses keys into a small table.
> 2. **Collisions are inevitable → separate chaining**, a short list per bucket, compare the full key.
> 3. **Average O(1)** rests on short chains — good bucket count, uniform keys, and resizing in production.
>
> The memory peg — *"a hash map is a wall of mailboxes: hash picks your box, a labeled list inside sorts out the collisions."*

---

## 14. CLIFFHANGER — `10:15`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Insert Delete GetRandom O(1)".]**

> You now know why a hash map gives O(1) lookup. But here's a twist it *can't* do alone: pick a **uniformly random** element in O(1). A hash set has no positions to index into. Next up, we pair the map with an array and pull off a swap trick that makes insert, delete, *and* random-pick all constant time. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
