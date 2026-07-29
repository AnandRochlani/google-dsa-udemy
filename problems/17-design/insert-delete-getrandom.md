# Insert Delete GetRandom O(1)

> **LeetCode:** 380. Insert Delete GetRandom O(1) · **Difficulty:** 🟡 Medium · **Pattern:** Design (dynamic array + index hash map) · **Google frequency:** medium

---

## Problem

Design a set that supports all three in **average O(1)**:

- `insert(val)` — add `val`; return `True` if it wasn't already present, else `False`.
- `remove(val)` — remove `val`; return `True` if it was present, else `False`.
- `getRandom()` — return a **uniformly random** element currently in the set.

**Example:**
```
RandomizedSet s = new RandomizedSet()
insert(1)     -> true    // {1}
remove(2)     -> false   // 2 not present
insert(2)     -> true    // {1, 2}
getRandom()   -> 1 or 2, each with probability 1/2
remove(1)     -> true    // {2}
insert(2)     -> false   // already present
getRandom()   -> 2       // only element left
```

**Constraints that matter:** up to `2 × 10⁵` calls, **O(1) required for all three**. The tension is that `getRandom` wants an **array** (random index in O(1)), but `insert`/`remove`/membership want a **hash set** (O(1) lookup). No single structure gives all three — a hash set can't pick a uniform random element in O(1), and an array can't remove an arbitrary value in O(1). We must combine them.

---

## 🧠 Intuition — how you'd actually arrive at this

> Match each operation to the structure that makes it O(1), then reconcile the conflict.

- **`getRandom` in O(1)** → the elements must live in a **contiguous array**, so we can do `arr[random_index]`. A hash set has no positional indexing, so you can't sample it uniformly in O(1).
- **`insert` / membership in O(1)** → we need a **hash map** to know instantly whether a value is present. Appending to an array is O(1), good.
- **The conflict — `remove` in O(1):** removing an arbitrary value from an array is normally O(n) because deleting from the middle shifts everything. That's the crux.
- **The leap — swap-with-last:** we don't care about *order* in a set. So to delete a value from the middle, **overwrite it with the last element**, then `pop()` the (now duplicated) last slot. Removing the tail of an array is O(1), and a swap is O(1). To find *where* the value sits so we can overwrite it, keep a hash map **`value → its index in the array`**. After the swap, update the moved element's index in that map.
- **Pattern trigger:** *"O(1) insert/delete **and** O(1) random access"* → **dynamic array + `value → index` hash map, delete via swap-with-last**. The swap-with-last trick is the signature move; remember it.

---

## ① Brute Force

Use a hash set for O(1) insert/remove/membership, and materialize a list for `getRandom`.

```python
import random

class RandomizedSetBrute:
    def __init__(self):
        self.s = set()

    def insert(self, val: int) -> bool:
        if val in self.s:
            return False
        self.s.add(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.s:
            return False
        self.s.remove(val)
        return True

    def getRandom(self) -> int:
        return random.choice(list(self.s))   # O(n): builds a list every call
```

**Why it's the natural first attempt:** a `set` nails insert, remove, and membership in O(1) — three of four requirements for free.

**Why it's not enough:** `random.choice(list(self.s))` copies the whole set into a list on **every** call → **O(n)** per `getRandom`. A Python `set` has no way to index a random element without materializing it, so this violates the O(1) requirement.

**Complexity:** insert/remove O(1), **getRandom O(n)**, Space O(n).

---

## ② Optimised Solution

Array `nums` holds the values; `pos` maps `value → index`. Delete by swapping the victim with the last element.

```python
import random

class RandomizedSet:
    def __init__(self):
        self.nums = []          # the elements, contiguous for random access
        self.pos = {}           # value -> index in nums

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        idx = self.pos[val]
        last = self.nums[-1]
        # move the last element into the hole left by val
        self.nums[idx] = last
        self.pos[last] = idx
        # drop the now-duplicated tail
        self.nums.pop()
        del self.pos[val]
        return True

    def getRandom(self) -> int:
        return self.nums[random.randint(0, len(self.nums) - 1)]
```

**Walk an example:**

- `insert(1)` → `nums=[1]`, `pos={1:0}`, returns `True`.
- `insert(2)` → `nums=[1,2]`, `pos={1:0, 2:1}`, `True`.
- `insert(3)` → `nums=[1,2,3]`, `pos={1:0, 2:1, 3:2}`.
- `remove(1)` → `idx=0`, `last=3`. Put `3` at index `0`: `nums=[3,2,3]`, `pos={1:0→del, 2:1, 3:0}`. Pop tail: `nums=[3,2]`, `pos={2:1, 3:0}`. Returns `True`.
- `getRandom()` → `random index in [0,1]` → `3` or `2`, each 1/2.

Notice `remove(1)` never shifted the array — it swapped the tail `3` into position `0` and popped. The `pos` map was updated so `3` now points to index `0`.

**Why it's correct:** `pos[val]` always gives the current index of `val` in `nums`, an invariant maintained on both insert (append + record index) and remove (the only element that moves is the former last one, and we fix its index). `getRandom` picks a uniformly random index over a *dense* array with no gaps, so every present element is equally likely.

**Complexity (per operation):** insert, remove, getRandom all **average O(1)** (amortized for the array append). Space **O(n)**.

---

## ③ Space Optimization

Already optimal — **O(n)**. You're storing each element once in the array and once in the index map, a constant factor times the number of elements, which you must hold to answer membership and random queries. Nothing scales with the value range or the call count.

> There's no in-place trick to shave this: the array is required for O(1) random sampling and the hash map is required for O(1) membership/locate. Removing either breaks a requirement. Say that explicitly — recognizing that the two structures are *both load-bearing* is the point.

**Follow-up worth mentioning — duplicates allowed (LeetCode 381, `RandomizedCollection`):** change `pos` to map `value → a set of indices`. On remove, pull any one index from the set and swap-with-last as before, being careful to update the moved element's index set. Same idea, one layer deeper.

---

## Java (for Java interviewers)

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
        nums.remove(nums.size() - 1);   // pop tail (O(1) for ArrayList end)
        pos.remove(val);
        return true;
    }

    public int getRandom() {
        return nums.get(rand.nextInt(nums.size()));
    }
}
```

---

## Complexity Summary

| Approach | insert | remove | getRandom | Space |
|---|---|---|---|---|
| Set + list on each getRandom | O(1) | O(1) | O(n) | O(n) |
| Array + index map (swap-with-last) | O(1) | O(1) | O(1) | O(n) |

---

## Say it out loud (interview narration)

> *"getRandom in O(1) forces me to keep the elements in a contiguous array so I can index a random slot. Insert and membership want a hash map. The hard part is remove — deleting from the middle of an array is O(n) because of shifting. But it's a set, order doesn't matter, so I swap the victim with the last element and pop the tail — both O(1). To find where the victim lives I keep a value-to-index map, and after the swap I update the moved element's index. All three operations are average O(1), space O(n). If duplicates were allowed I'd map each value to a set of indices instead."*

## Related / follow-ups
- **Insert Delete GetRandom O(1) — Duplicates allowed** (381) — `value → set of indices`.
- **Design HashMap / HashSet** (706 / 705) — the map primitive underneath.
- **Random Pick with Weight** (528) — prefix sums + binary search for weighted sampling.
- **LRU Cache** (146) — same "two structures fused by shared references" idea.
