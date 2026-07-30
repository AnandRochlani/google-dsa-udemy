# Snapshot Array

> **LeetCode:** 1146. Snapshot Array · **Difficulty:** 🟡 Medium · **Pattern:** Design / versioned values + binary search · **Google frequency:** ⭐ high

---

## Problem

Design an array-like structure that can **remember its past**. Implement:

- `SnapshotArray(length)` — build an array of `length` slots, every one initialized to `0`.
- `set(index, val)` — set the value at `index` to `val` (in the *current*, not-yet-snapshotted state).
- `snap()` — take a snapshot of the whole array, return the **snap_id** for it, then increment the snapshot counter. The first `snap()` returns `0`, the next `1`, and so on.
- `get(index, snap_id)` — return the value at `index` **as it was at the moment** `snap_id` was taken.

**Example:**
```
SnapshotArray(3)      // array = [0, 0, 0]
set(0, 5)             // current array = [5, 0, 0]
snap()        -> 0    // snapshot #0 frozen; counter now 1
set(0, 6)             // current array = [6, 0, 0]  (does NOT affect snap 0)
get(0, 0)     -> 5    // index 0, at snapshot 0, was 5
```

**Constraints that matter:** `length` up to `5·10⁴`, and up to `5·10⁴` total calls across `set`/`snap`/`get`. That combination is the whole trap: if `snap()` copies the entire array, one snap is `O(length)` and a run of snaps is `O(length × snaps)` time *and* memory — easily `2.5·10⁹` cells. The design must make `snap()` cheap and store **only what actually changed**.

---

## 🧠 Intuition — how you'd actually arrive at this

> The word "snapshot" screams "save a copy." That instinct is the trap. The fix is to stop thinking about the *array* and start thinking about each *index* as a little timeline.

- **First instinct:** on every `snap()`, deep-copy the current array and stash it in a list of versions. `get(index, snap_id)` is then just `versions[snap_id][index]`. Dead simple, and dead slow — you copy `length` cells even if a single slot changed (or nothing changed at all).
- **Where it hurts:** the copies are almost entirely *duplicates*. If index 0 flips from 5 to 6 between snaps but the other 49,999 slots never move, you've re-stored 49,999 identical values per snapshot. The information content of a snapshot is only the handful of cells that changed — everything else is redundant.
- **The leap:** invert the storage. Instead of "for each snapshot, the whole array," keep **for each index, the history of its changes** — a list of `(snap_id, value)` records, appended *only* when `set()` actually touches that index. `snap()` then does no copying at all; it just hands back the current counter and ticks it up. To answer `get(index, snap_id)`, look inside that one index's history for the **latest record whose snap_id ≤ the queried snap_id** — and since we append in increasing snap_id order, that list is sorted, so it's a **binary search**.
- **Pattern trigger:** *"versioned reads — value of X as of time T"* → **per-key sorted history + binary search for the newest entry ≤ T**. The transferable move is *store deltas, not full states, and index them by version so a read is a log-time lookup.* This is the same shape as a time-based key-value store or a database's MVCC.

---

## ① Brute Force

Take `snap()` literally: copy the entire current array each time and keep every version.

```python
class SnapshotArrayBrute:
    def __init__(self, length: int):
        self.arr = [0] * length      # the live, current array
        self.snaps = []              # snaps[i] = full copy of arr at snapshot i

    def set(self, index: int, val: int) -> None:
        self.arr[index] = val

    def snap(self) -> int:
        self.snaps.append(self.arr[:])   # O(length) full copy — the killer
        return len(self.snaps) - 1

    def get(self, index: int, snap_id: int) -> int:
        return self.snaps[snap_id][index]
```

**Why it's the natural first attempt:** it's a literal reading of the spec — "take a snapshot" becomes "save a copy," and `get` is a trivial two-index lookup.

**Why it's not enough:** `snap()` is `O(length)` time and memory *every call*. With `length` and the number of snaps both up to `5·10⁴`, that's up to `2.5·10⁹` stored integers — out of time and out of memory. And it's almost all waste: consecutive snapshots differ by only the cells `set()` touched between them.

**Complexity:** `set` O(1); `snap` O(length); `get` O(1). Space O(length × snaps).

---

## ② Optimised Solution

Flip the storage from "per-snapshot arrays" to **"per-index change history."** Each index owns a list of `(snap_id, value)` records, appended only on a real `set`. Reads binary-search that list.

```python
import bisect

class SnapshotArray:
    def __init__(self, length: int):
        self.snap_id = 0
        # one history per index; seed with (snap_id=0, value=0) so every
        # index has a defined value at snapshot 0 with no special-casing.
        self.history = [[(0, 0)] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        records = self.history[index]
        if records[-1][0] == self.snap_id:
            # already wrote at this snap_id → overwrite, don't append a duplicate
            records[-1] = (self.snap_id, val)
        else:
            records.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1            # O(1): no copying, just bump the counter
        return self.snap_id - 1      # return the id we just froze

    def get(self, index: int, snap_id: int) -> int:
        records = self.history[index]
        # find the last record with record_snap_id <= snap_id.
        # bisect_right on the key (snap_id + 1) lands just past it; step back one.
        i = bisect.bisect_right(records, (snap_id, float('inf'))) - 1
        return records[i][1]
```

**Walk the example** `SnapshotArray(3)`:

| Call | `snap_id` | Effect | `history[0]` |
|---|---|---|---|
| construct | 0 | seed every index | `[(0,0)]` |
| `set(0, 5)` | 0 | last record's id == 0 → overwrite the seed | `[(0,5)]` |
| `snap()` → **0** | 0→1 | freeze snap 0, bump counter | `[(0,5)]` |
| `set(0, 6)` | 1 | last record's id is 0 ≠ 1 → append | `[(0,5), (1,6)]` |
| `get(0, 0)` | 1 | search `history[0]` for latest id ≤ 0 | reads `(0,5)` → **5** |

For `get(0, 0)`: `bisect_right([(0,5),(1,6)], (0, inf))` returns `1` (past the `(0,5)` record, before `(1,6)`), minus 1 = index `0`, whose value is `5`. ✅ Snapshot 0 correctly still says 5 even though the live value is now 6.

**Why it's correct:** every index carries a `(0, 0)` seed, so it always has a defined value at snapshot 0 — no "empty history" edge case. We only append when `set` runs, and always at the *current* `snap_id`, which never decreases — so each history list is **sorted by snap_id**. The overwrite-if-same-snap_id rule keeps at most one record per snapshot per index, so a later `set` in the same snapshot wins (correct: only the final value before the next `snap()` should be frozen). For a read, the value visible at `snap_id` is exactly the most recent write *at or before* that snapshot — the largest record id ≤ `snap_id` — which `bisect_right(...) - 1` finds in log time. Because we seeded id 0 and every real `snap_id` is ≥ 0, that index is never `-1`.

**Complexity:** `set` **O(1)** amortized (append or in-place overwrite); `snap` **O(1)**; `get` **O(log k)** where k = number of writes to *that* index. Space **O(total writes)** — one record per actual `set`, never per untouched cell.

---

## ③ Space Optimization

**Already essentially optimal — and worth saying why.** We store exactly one record per real `set` (with the same-snapshot overwrite collapsing redundant writes), plus one seed per index. That's `O(length + total set-calls)` — the seeds are unavoidable (every index must have a value) and each stored record represents genuine, non-redundant information: a value that some snapshot can still query. There's no full-array copy anywhere, so nothing scales with `length × snaps`.

Two honest micro-notes rather than a real asymptotic win:

```python
# 1. Drop the per-index seed and special-case "before any write" as 0:
#    get returns 0 when the binary search lands at -1. Saves `length` seed
#    records but adds a branch on every get. A wash — clarity usually wins.
#
# 2. Store two parallel lists (snap_ids[], values[]) per index instead of
#    tuples, so bisect runs on the raw ids with no (snap_id, inf) trick.
#    Same asymptotics; slightly less overhead per record.
```

**Complexity:** unchanged — `get` O(log k), space O(length + total writes).

> Say it out loud: *"Space is O(total writes), not O(length × snaps), because I store per-index deltas instead of whole-array copies. That's the point of the design — I can't do meaningfully better, because every record I keep is a value some snapshot can still legally ask for."*

---

## Java (for Java interviewers)

```java
class SnapshotArray {
    // one TreeMap per index: snap_id -> value, sorted by snap_id.
    // floorEntry(snap_id) gives the latest write at or before snap_id.
    private final TreeMap<Integer, Integer>[] history;
    private int snapId = 0;

    @SuppressWarnings("unchecked")
    public SnapshotArray(int length) {
        history = new TreeMap[length];
        for (int i = 0; i < length; i++) {
            history[i] = new TreeMap<>();
            history[i].put(0, 0);          // seed value 0 at snapshot 0
        }
    }

    public void set(int index, int val) {
        history[index].put(snapId, val);   // overwrites if same snapId already present
    }

    public int snap() {
        return snapId++;                   // return current id, then increment
    }

    public int get(int index, int snapId) {
        // floorEntry = greatest key <= snapId; never null thanks to the seed.
        return history[index].floorEntry(snapId).getValue();
    }
}
```

*(TreeMap's `put` already overwrites on an equal key, so the same-snapshot collapse is free. `floorEntry` is the direct analog of `bisect_right - 1`.)*

---

## Complexity Summary

| Approach | set | snap | get | Space |
|---|---|---|---|---|
| Brute force (copy whole array) | O(1) | O(length) | O(1) | O(length × snaps) |
| Per-index history + binary search | O(1) amortized | O(1) | O(log k) | O(length + total writes) |
| Space-tuned (drop seeds / parallel arrays) | O(1) | O(1) | O(log k) | O(length + total writes) |

*(k = number of writes to the queried index.)*

---

## Say it out loud (interview narration)

> *"The naive read of 'snapshot' is to copy the array on every snap, but with length and snap count both up to fifty thousand that's billions of cells — time and memory blow up. So I flip it: instead of storing a full array per snapshot, I store per index a sorted history of `(snap_id, value)` records, appended only when `set` actually changes that index. `snap()` then does no work — it just returns the current counter and increments it. For `get(index, snap_id)`, I binary-search that index's history for the latest record whose snap_id is at or below the queried one — bisect_right minus one, or floorEntry in Java. I seed each index with `(0, 0)` so there's always a defined value and no empty-list edge case, and I overwrite rather than append when two sets hit the same snapshot. That's O(1) set and snap, O(log k) get, and space proportional to real writes instead of length times snaps."*

Before coding, ask the one clarifying question that shows you read the spec: *"Does `snap()` return the id before or after incrementing — is the first snapshot id 0?"* Nailing that off-by-one early is exactly the kind of care Google's rubric rewards.

## Related / follow-ups
- **Time Based Key-Value Store** (981) — the near-twin: `set(key, value, timestamp)` and `get(key, timestamp)` returns the value at the largest timestamp ≤ query. Same sorted-history + binary-search skeleton.
- **Design a Text Editor / version control** — undo-redo and "value as of version" share the versioned-storage idea.
- **Random Pick with Weight** (528) — another "build a sorted array, binary-search it" design.
- **LRU Cache** (146) — a different design-with-a-data-structure staple Google likes to pair with this one.
