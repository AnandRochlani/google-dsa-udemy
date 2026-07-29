# 🎬 Recording Script — LFU Cache

**Pattern: Design (hash maps + buckets of doubly linked lists) · LeetCode 460 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** LRU Cache (hash map + doubly linked list fusion) — watch that first.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: the LRU diagram from last lesson — map + doubly linked list. A red stamp slams on: "NOT ENOUGH." A new rule appears: "evict least-FREQUENTLY-used; ties → least-recently-used."]**

> Last lesson we built an LRU cache — evict what you touched longest ago. Google's follow-up turns the screw: *"Now evict what you've used the **fewest** times. And if two keys are tied on count, break the tie by recency."*
>
> That one word — *frequently* — makes this a **Hard**. Because now eviction depends on ranking by **two** things at once, and you still have to do everything in O(1).
>
> Here's the beautiful part: the answer isn't a new invention. It's an LRU cache hidden *inside* every frequency level. By the end, you'll see LFU as LRU with one extra axis. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, "capacity = 2" and a call list: put(1,1), put(2,2), get(1), put(3,3), get(2)?]**

> One line: **a fixed-capacity cache that evicts the least-frequently-used key, and on ties, the least-recently-used among them.**
>
> Every `get`, and every `put` that updates, **increments a key's use-count**. When the cache is full, we throw out the key with the smallest count — and if several share that smallest count, the oldest-used one goes.
>
> Tiny example — capacity 2. Watch closely: after `get(1)`, key 1's count climbs to 2 while key 2 stays at 1. So when `put(3,3)` needs room, key **2** is the victim. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — let them feel the waste)*

**[VISUAL: a table — each key with its (value, count, last-used-tick). On eviction, a scan sweeps every row hunting the minimum.]**

> Brute force first. Store each key with two extra fields: its **count**, and a **tick** — a global timestamp for recency tie-breaking. `get` bumps the count and stamps the tick.
>
> Now `put(3,3)` on a full cache. To evict, I have to find the key with the smallest count, breaking ties by the smallest tick. So I **scan every entry** and take the minimum.
>
> **[VISUAL: the scan arrow sweeps all rows; a "scan cost O(n)" tag flashes on every put.]**
>
> It's correct. But every eviction is a full O(n) sweep. With 200,000 calls, that's the same tens-of-billions wall we hit with LRU's list — and again, the interviewer *said* O(1).

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the eviction scan. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The pain is the eviction scan — hunting the minimum count across everything, every time. And even once you find the min count, you *still* need the least-recently-used among the ties.
>
> **LEARNER:** With LRU, the doubly linked list kept things in recency order so the tail was always the victim. Can't I just... keep them sorted by count the same way?
>
> **TEACHER:** Close — but a single sorted order can't hold *two* rankings at once, and counts change constantly. Pause and think about it differently: **what if I don't sort at all — what if I group keys into buckets by their exact count, and always evict from the smallest-count bucket?** How would I find that smallest bucket in O(1), and break ties inside it?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration + analogy — derive it)*

**[VISUAL: keys sorted into labeled bins: "count 1: [ ... ]", "count 2: [ ... ]". A pointer labeled min_freq points at bin 1.]**

> **TEACHER:** Same design method as LRU — match each fast operation to a structure. Here's the layering.
>
> One: **value lookup by key** — a hash map, `key → (value, count)`. Standard.
>
> Two: **group keys by their count.** A second map, `count → bucket`, where each bucket holds every key currently at that exact count. And a single pointer, `min_freq`, tracking the smallest count present. Eviction *always* comes from `bucket[min_freq]` — no scanning.
>
> **[VISUAL: zoom into bucket 2, which contains keys 1 and 3 in a little ordered strip — oldest on the left.]**
>
> Three: **inside each bucket, break ties by recency.** And what structure gives O(1) removal from either end *and* O(1) removal of an arbitrary key? The **doubly linked list** — the exact LRU trick. So each bucket *is* a mini LRU list: most-recent at the head, least-recent at the tail. On a tie, evict the tail of `bucket[min_freq]`.
>
> **LEARNER:** So it's literally an LRU cache per frequency level?
>
> **TEACHER:** That's the whole idea. LFU is a stack of LRU lists, indexed by count.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(the crisp rules — including the min_freq trick)*

**[VISUAL: a key moving from bucket 1 to bucket 2 — unlinked from bin 1, dropped at the head of bin 2. min_freq updates.]**

> Two rules to burn in.
>
> **Bumping a key** from count `f` to `f+1`: splice it out of `bucket[f]`, drop it at the head of `bucket[f+1]`. Both O(1). And if `bucket[f]` just went empty *and* `f` was `min_freq`, then `min_freq += 1`.
>
> **Why min_freq only ever needs plus-one** — this is the clever bit that keeps it O(1): the only way to empty the minimum bucket is to promote its last key, and that key just landed in `f+1`. So the new minimum is exactly `f+1`. No search. And a brand-new key always enters at count 1, which resets `min_freq` to 1.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Imports + init. Note: each bucket is an OrderedDict — a ready-made hash-map-over-DLL, so we skip hand-writing node splicing.]**

> In Python we lean on `OrderedDict` for each bucket — it's already a hash map over a doubly linked list, so `popitem(last=False)` pops the oldest, O(1). Setup:

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.min_freq = 0
        self.key_map = {}                         # key -> [value, freq]
        self.freq_map = defaultdict(OrderedDict)  # freq -> {key: value}, LRU order
```

> **[VISUAL: add the _bump helper, animate a key hopping buckets.]** The heart — `_bump`: move a key up one frequency.

```python
    def _bump(self, key):
        value, freq = self.key_map[key]
        del self.freq_map[freq][key]              # leave current bucket
        if not self.freq_map[freq]:               # bucket emptied?
            del self.freq_map[freq]
            if self.min_freq == freq:
                self.min_freq += 1                # only ever +1
        self.freq_map[freq + 1][key] = value      # enter next bucket (at end = MRU)
        self.key_map[key] = [value, freq + 1]
```

> **[VISUAL: add get().]** `get` is just a lookup plus a bump.

```python
    def get(self, key):
        if key not in self.key_map:
            return -1
        self._bump(key)
        return self.key_map[key][0]
```

> **[VISUAL: add put(), highlight the eviction line.]** `put` — update-and-bump if present; otherwise evict if full, then insert at freq 1.

```python
    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.key_map:
            self.key_map[key][0] = value
            self.freq_map[self.key_map[key][1]][key] = value   # keep bucket value fresh
            self._bump(key)
            return
        if len(self.key_map) >= self.cap:
            evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)  # LRU of min bucket
            del self.key_map[evict_key]
        self.key_map[key] = [value, 1]
        self.freq_map[1][key] = value
        self.min_freq = 1                         # new key resets the minimum
```

---

## 8. EXPLAIN THE CODE (the WHY) — `8:15`
*(elaboration — why each line exists)*

**[VISUAL: full class; spotlight the min_freq lines.]**

> Why it holds together.
>
> `_bump` is the engine — every access routes through it. Splice out of the old bucket, drop into the next, update the stored freq. Because buckets are `OrderedDict`s, dropping a key at the end makes it the most-recent in its new bucket automatically.
>
> The `min_freq += 1` line. 
>
> **LEARNER:** That's the part I don't trust. How can you *know* the new minimum is `freq + 1`? What if the real minimum is way higher?
>
> **TEACHER:** Because of *when* this line fires: only when the bucket we just emptied was the minimum bucket, and we emptied it by promoting its final key to `freq + 1`. That promoted key is now sitting in bucket `freq + 1`, so a key with count `freq + 1` provably exists — it's the new floor. There's no gap to jump over, because you can't reach count `f+1` without passing through `f`. Every promotion is exactly one step.
>
> `popitem(last=False)` — pops the *oldest-inserted* key of `bucket[min_freq]`: least-frequently-used, and among ties, least-recently-used. That's the spec, exactly.

---

## 9. DRY-RUN THE CODE — `9:45`
*(worked example — prove it)*

**[VISUAL: table — key_map (key:freq), freq_map (freq:[keys oldest→newest]), min_freq — filling row by row.]**

> Capacity 2. Watch the buckets.

| Call | key_map (key:freq) | freq_map | min_freq |
|---|---|---|---|
| put(1,1) | {1:1} | 1:[1] | 1 |
| put(2,2) | {1:1, 2:1} | 1:[1,2] | 1 |
| get(1)→1 | {1:2, 2:1} | 1:[2], 2:[1] | 1 |
| put(3,3) full → evict bucket1 LRU = **2** | {1:2, 3:1} | 2:[1], 1:[3] | 1 |
| get(2)→**-1** | — | — | 1 |
| get(3)→3 | {1:2, 3:2} | 2:[1,3] | 2 |
| put(4,4) full, min=2, ties {1,3}, LRU = **1** | {3:2, 4:1} | 2:[3], 1:[4] | 1 |

> Two payoffs. At `put(3,3)`, key 2 sat alone in bucket 1 (the minimum), so it was evicted — answering our opening question. And at `put(4,4)`, keys 1 and 3 were *tied* at count 2; the tie broke to key **1** because it was at the front — oldest — of bucket 2. Least-frequent, then least-recent. Exactly the spec.

---

## 10. COMPLEXITY, OUT LOUD — `11:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute: get O(1), put O(n). Buckets: get O(1), put O(1). Space O(capacity).]**

> Out loud: *"Both operations are O(1) — hash lookups plus OrderedDict insert, delete, and popitem, all amortized constant. The min_freq pointer means eviction never scans; it only ever increments by one or resets to one. Space is O(capacity)."*
>
> Contrast the brute force honestly: *"The naive version was O(n) per put because eviction scanned for the minimum. Bucketing by frequency kills that scan."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:45`
*(depth + honesty)*

**[VISUAL: empty buckets being deleted the instant they drain. A note: "larger constant than LRU, same O(capacity)".]**

> Space is already optimal — **O(capacity)**. Each key lives once in `key_map` and once in exactly one bucket. And notice we `del` a bucket the moment it empties, so `freq_map` never hoards stale frequency levels.
>
> Honest caveat to say out loud: *"LFU carries a bigger constant factor than LRU — two maps plus a per-bucket ordered structure — but the asymptotic space is the same O(capacity). You genuinely need both the frequency axis and the recency axis to answer the eviction query in O(1); there's no cheaper representation."* Naming the constant-factor cost *and* why it's unavoidable is the senior move.

---

## 12. YOUR TURN (active recall) — `12:30`
*(retrieval practice)*

**[VISUAL: "Your turn → All O'one Data Structure (LC 432)". inc / dec / getMax / getMin.]**

> Before the next video, try **All O'one Data Structure**. Increment and decrement a key's count, and return the max-count and min-count keys — all O(1). It's the same skeleton: buckets keyed by count, each a doubly linked list, with pointers to the extremes. If you own LFU's bucket idea, this is a variation, not a new problem.
>
> Fifteen minutes on the whiteboard before you look.

---

## 13. LOCK IT IN — `13:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **LFU = LRU plus a frequency axis** — an LRU list inside each count bucket.
> 2. **Bucket by count + a `min_freq` pointer** replaces the O(n) eviction scan.
> 3. **`min_freq` only increments or resets to 1** — that's what keeps eviction O(1).
>
> The memory peg — *"stack LRU lists by frequency, and remember where the floor is."*

---

## 14. CLIFFHANGER — `13:35`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Design HashMap — from scratch".]**

> We've now leaned on the phrase "just use a hash map" three times — for O(1) lookup, over and over. But *what is* a hash map, really? Why is it O(1)? Next up we build one from scratch — no `dict`, no `HashMap` — buckets, a hash function, and collisions. Once you've built the thing everything else stands on, you'll understand exactly *why* all these designs work. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class LFUCache {
    private final int cap;
    private int minFreq = 0;
    private final Map<Integer, Integer> values = new HashMap<>();   // key -> value
    private final Map<Integer, Integer> counts = new HashMap<>();   // key -> freq
    // freq -> keys, LinkedHashSet preserves insertion (LRU) order
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
