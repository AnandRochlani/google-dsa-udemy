# 🎬 Recording Script — Insert Delete GetRandom O(1)

**Pattern: Design (dynamic array + index hash map) · LeetCode 380 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hash-map O(1) membership (Design HashMap) + array indexing.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: three requirement cards flip up: "insert O(1)" ✅, "delete O(1)" ✅, "getRandom O(1)" — the third card flickers red and won't settle.]**

> This one's a classic Google trap, and it's devious because it looks trivial. *"Build a set with insert, delete, and get-a-random-element — all O(1)."*
>
> Here's the sting: each requirement *alone* is easy. A hash set nails insert and delete in O(1). An array nails random-pick in O(1). But **no single structure does all three** — a set can't pick a random element without copying itself, and an array can't delete a value from the middle without shifting.
>
> The answer is a two-structure combo with one gorgeous trick — the *swap-with-last*. Learn it once and you'll reuse it forever. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below: insert(1)→true, remove(2)→false, insert(2)→true, getRandom()→"1 or 2, each ½".]**

> One line: **a set where `insert`, `remove`, and `getRandom` are all average O(1)** — and `getRandom` must be *uniformly* random.
>
> `insert(val)` returns true if it was new. `remove(val)` returns true if it was there. `getRandom()` returns any current element, each equally likely.
>
> Keep your eye on `getRandom` — "uniformly random in O(1)" is the constraint that fights everything else.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: a Python `set {1, 2, 3}`. For getRandom, it copies every element into a fresh list, then picks.]**

> First instinct: use a hash set. Insert, remove, membership — all O(1). Three of four requirements, free.
>
> Now `getRandom`. A set has no *positions* — you can't say "give me element number 2." So to pick randomly, you copy the whole set into a list, then index that.

**[VISUAL: the set copying 3 elements... then imagine it copying 200,000 elements, a progress bar crawling, on EVERY getRandom call.]**

> It works on three elements. But that copy is **O(n)** — and it happens on *every single* `getRandom`. With hundreds of thousands of calls, you're re-copying the entire set constantly. That's the wall.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the copy step. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The pain: a hash set has no indexable positions, so uniform random sampling forces an O(n) copy every time.
>
> **LEARNER:** So keep the elements in an **array** instead — then `getRandom` is just `arr[random index]`, O(1). But then how do I delete a value from the middle without shifting everything down?
>
> **TEACHER:** You've just found both halves of the puzzle — array for random, and the delete is the crux. Pause and think about one freedom this problem gives you: **it's a set, so order doesn't matter. If you need to delete something from the middle of an array but you don't care about order... what's the cheapest way to fill the hole?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it)*

**[VISUAL: array [10, 20, 30, 40]. Delete 20 at index 1: the LAST element 40 jumps into index 1, then the tail is popped. Result [10, 40, 30].]**

> **TEACHER:** Match each op to its structure. `getRandom` needs a contiguous **array** — `arr[random]`. Insert and membership need a **hash map**. The conflict is delete.
>
> Deleting from the middle of an array is O(n) *only if you insist on keeping order* — because you shift everyone left to close the gap. But it's a **set**. Order is irrelevant. So don't shift — **swap the victim with the last element, then pop the tail.**
>
> **[VISUAL: the swap animates — 40 slides into 20's slot, then the duplicated tail 40 is chopped off. "O(1)!" pops up.]**
>
> Removing the *last* element of an array is O(1). A swap is O(1). So middle-delete becomes O(1). But — to swap, I need to know *where* the victim sits. That's the fusion: a hash map `value → its index in the array`. Look up the index, swap with the tail, pop, and fix the moved element's index in the map.

---

## 6. THE KEY MOVE (signaling) — `4:40`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Array for random access + value→index map; delete = swap victim with last, pop, fix the map."]**

> The key move: **an array plus a `value → index` map, and delete by swap-with-last.** The array gives O(1) random and O(1) append; the map gives O(1) locate; the swap-with-last gives O(1) delete without shifting. Remember *swap-with-last* — it's the signature trick, and it shows up any time you need O(1) deletion from an unordered array.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Init.]**

> Two fields — the array and the index map.

```python
import random

class RandomizedSet:
    def __init__(self):
        self.nums = []          # the elements, contiguous
        self.pos = {}           # value -> index in nums
```

> **[VISUAL: add insert().]** `insert` — reject duplicates, else record the index and append.

```python
    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.nums)     # its index = current end
        self.nums.append(val)
        return True
```

> **[VISUAL: add remove(), highlight the swap block.]** `remove` — the swap-with-last dance.

```python
    def remove(self, val):
        if val not in self.pos:
            return False
        idx = self.pos[val]
        last = self.nums[-1]
        self.nums[idx] = last          # move last into the hole
        self.pos[last] = idx           # fix moved element's index
        self.nums.pop()                # drop the duplicated tail
        del self.pos[val]
        return True
```

> **[VISUAL: add getRandom().]** And `getRandom` — one indexed pick over a dense array.

```python
    def getRandom(self):
        return self.nums[random.randint(0, len(self.nums) - 1)]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: remove() spotlighted, the four lines numbered.]**

> The `remove` is where all the care lives. Four lines: grab the victim's index, copy the last element into that hole, **update the moved element's index in the map**, then pop the now-duplicated tail and delete the victim's map entry.
>
> **LEARNER:** That `self.pos[last] = idx` line — why is it so important? Feels like bookkeeping.
>
> **TEACHER:** It's the line everyone forgets, and it's fatal to skip. We physically moved `last` from the end into position `idx`. If the map still says `last` lives at the old tail index, the next `remove(last)` will swap the *wrong* slot and corrupt the array. The map is a promise: `pos[v]` is always `v`'s real index. Move an element, update its promise. 
>
> And `getRandom` works because the array is **dense** — no gaps, since swap-with-last never leaves holes. So a random index hits every element with equal probability. That density is exactly what the swap trick buys us.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it)*

**[VISUAL: nums array and pos map, side by side, updating per call.]**

> Trace it.

| Call | nums | pos | returns |
|---|---|---|---|
| insert(1) | [1] | {1:0} | true |
| insert(2) | [1,2] | {1:0, 2:1} | true |
| insert(3) | [1,2,3] | {1:0, 2:1, 3:2} | true |
| remove(1) | [3,2] | {2:1, 3:0} | true |
| getRandom() | [3,2] | — | 3 or 2, each ½ |

> Look at `remove(1)`: idx 0, last is 3. Put 3 at index 0 → `[3,2,3]`, set `pos[3]=0`, pop the tail → `[3,2]`, delete `pos[1]`. **No shifting happened** — 3 hopped into the hole, the map got fixed, done. The array stays dense, so `getRandom` is uniform.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Set + copy: getRandom O(n). Array + map: all O(1).]**

> Out loud: *"Insert, remove, and getRandom are all average O(1). Insert is an append plus a map write. Remove is a swap-with-last plus two map updates — no shifting. GetRandom is one indexed array read over a dense array. Space is O(n) — each element sits once in the array and once in the map."*
>
> The contrast: *"The set-and-copy approach was O(n) per getRandom because a set can't be indexed; the array fixes that, and swap-with-last keeps delete O(1)."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:40`
*(depth + honesty)*

**[VISUAL: the array and map both highlighted "load-bearing". A crossed-out attempt to drop either one.]**

> Space is already optimal — O(n) — and here's the point worth stating: **both structures are load-bearing.** The array is *required* for O(1) random sampling; the map is *required* for O(1) membership and locate. Drop either and a requirement breaks. There's no in-place trick to shave it. Recognizing that two structures are *each* necessary — and saying so — is the senior insight.
>
> **Follow-up they love — duplicates allowed** (LC 381, RandomizedCollection): change `pos` to map `value → a set of indices`. On remove, pull *any one* index from that set and swap-with-last as before, carefully updating the moved element's index set. Same idea, one layer deeper. Naming this shows you see where the problem goes next.

---

## 12. YOUR TURN (active recall) — `10:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Insert Delete GetRandom — Duplicates allowed (LC 381)".]**

> Before the next video, try exactly that follow-up — **RandomizedCollection**, duplicates allowed. Map each value to a *set* of indices and adapt the swap. It'll test whether you really understand why the index bookkeeping matters, because now there's more than one index per value.
>
> Fifteen minutes before you look.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **getRandom O(1) forces a contiguous array**; membership forces a hash map — combine them.
> 2. **Swap-with-last** turns middle-delete from O(n) into O(1) — legal because a set is unordered.
> 3. **Always fix the moved element's index** in the map after a swap.
>
> The memory peg — *"array for the dice roll, map for the lookup, and to delete: swap with the last and pop."*

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Logger Rate Limiter". A stream of log messages, some blocked.]**

> We've been fusing structures for *speed*. Next problem adds a new dimension: **time**. A logger that must suppress repeated messages within a 10-second window — "have I seen this recently?" It's a hash map again, but the value is a *timestamp*, and the whole game is one tricky boundary comparison. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class RandomizedSet {
    private final List<Integer> nums = new ArrayList<>();
    private final Map<Integer, Integer> pos = new HashMap<>();  // value -> index
    private final Random rand = new Random();

    public boolean insert(int val) {
        if (pos.containsKey(val)) return false;
        pos.put(val, nums.size());
        nums.add(val);
        return true;
    }

    public boolean remove(int val) {
        if (!pos.containsKey(val)) return false;
        int idx = pos.get(val);
        int last = nums.get(nums.size() - 1);
        nums.set(idx, last);            // move last into the hole
        pos.put(last, idx);
        nums.remove(nums.size() - 1);   // pop tail — O(1) at the end
        pos.remove(val);
        return true;
    }

    public int getRandom() {
        return nums.get(rand.nextInt(nums.size()));
    }
}
```
