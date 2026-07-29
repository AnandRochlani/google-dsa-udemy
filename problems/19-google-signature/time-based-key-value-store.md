# Time Based Key-Value Store

> **LeetCode:** 981. Time Based Key-Value Store · **Difficulty:** 🟡 Medium · **Pattern:** Hash Map + Binary Search · **Google frequency:** ⭐ high

---

## Problem

Design a class that stores multiple values for the same string key, each stamped with an integer `timestamp`, and can answer *time-travel* lookups — "what was this key's value **at or before** a given moment?"

Two operations:

- `set(key, value, timestamp)` — store `value` for `key` at time `timestamp`.
- `get(key, timestamp)` — return the value that was set for `key` with the **largest timestamp `≤` the query timestamp**. If no such write exists (or the key was never set), return `""`.

**The gift in the constraints:** for a given key, all `set` calls arrive with **strictly increasing timestamps**. So each key's history is *already sorted* by timestamp — we never have to sort it ourselves.

**Example:**
```
TimeMap kv = new TimeMap()
set("foo", "bar", 1)      // foo: [(1,"bar")]
get("foo", 1)   -> "bar"  // exact hit at t=1
get("foo", 3)   -> "bar"  // no write at 3; largest ≤ 3 is t=1 → "bar"
set("foo", "bar2", 4)     // foo: [(1,"bar"), (4,"bar2")]
get("foo", 4)   -> "bar2" // exact hit at t=4
get("foo", 5)   -> "bar2" // largest ≤ 5 is t=4 → "bar2"
get("foo", 0)   -> ""     // nothing at or before t=0
```

**Constraints that matter:** up to `2 × 10⁵` combined calls, and any single key can collect a huge history. A `get` that linearly scans a key's whole history is O(n) per call → up to ~10¹⁰ work across all calls → **Time Limit Exceeded**. Because each history is sorted, we can do **binary search** and answer each `get` in O(log n).

---

## 🧠 Intuition — how you'd actually arrive at this

> Design problems are solved by matching *each required operation* to a data structure that delivers it in the target complexity — then noticing the property (here: sorted-by-time) that upgrades the slow operation.

- **First instinct:** "One key can have many values over time — so map each key to a *list* of its `(timestamp, value)` writes. `set` appends; `get` walks the list looking for the right timestamp." That list-per-key idea is exactly right. The naive `get` just scans that list.
- **Where it hurts:** `get` scans the *entire* history of a key on every call. If a hot key has been `set` 100,000 times and you `get` it 100,000 times, that's 10¹⁰ operations. You're re-reading the same sorted list from scratch every single query.
- **The leap:** the writes for a key arrive with **strictly increasing timestamps**, so the appended list is **already sorted by timestamp**. And "find the largest timestamp `≤` the query" on a sorted array is the textbook job of **binary search**. Concretely it's an **upper bound** (first timestamp strictly greater than the query) **minus one** — the slot just before it is the answer.
- **Pattern trigger:** *"sorted data + find the rightmost element `≤` a target"* → **binary search** (specifically, `bisect_right` then step back one). Burn in the pairing: **sorted timestamps ⇒ binary search the history.**

---

## ① Brute Force

Map each key to a list of `(timestamp, value)` pairs. On `get`, scan the list and keep the last value whose timestamp is `≤` the query.

```python
class TimeMap:
    def __init__(self):
        self.store = {}                      # key -> list of (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        ans = ""
        for ts, val in self.store[key]:      # scan the whole history
            if ts <= timestamp:
                ans = val                    # keep the latest valid one
            else:
                break                        # list is sorted → we can stop
        return ans
```

**Why it's the natural first attempt:** it's the literal reading of the problem — keep every write, then look through them for the one you want.

**Why it's not enough:** `get` is **O(n)** in the length of that key's history. On a hot key with 10⁵ writes queried 10⁵ times, that's ~10¹⁰ comparisons → **Time Limit Exceeded**. We're scanning a *sorted* list linearly — leaving the whole point on the table.

**Complexity:** `set` O(1), `get` O(n) per call, Space O(n total writes).

---

## ② Optimised Solution

Same `key → sorted list` layout — but `get` uses **binary search** instead of a scan. We want the rightmost timestamp `≤` the query, which is `bisect_right` (first index whose timestamp is strictly greater) **minus one**.

```python
import bisect

class TimeMap:
    def __init__(self):
        self.times = {}                      # key -> list of timestamps (sorted)
        self.vals = {}                       # key -> list of values (parallel)

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.times:
            self.times[key] = []
            self.vals[key] = []
        self.times[key].append(timestamp)    # arrives in increasing order → stays sorted
        self.vals[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.times:
            return ""
        # first index with timestamp strictly > query
        i = bisect.bisect_right(self.times[key], timestamp)
        if i == 0:
            return ""                        # every write is after the query
        return self.vals[key][i - 1]         # step back one → largest ts ≤ query
```

> Splitting into parallel `times` / `vals` lists lets `bisect` search the raw timestamp array directly. You can also keep a single list of `(timestamp, value)` tuples and search with a key — either is fine; the parallel arrays are the cleanest with `bisect`.

**Walk the example.** History for `"foo"` after both sets: `times = [1, 4]`, `vals = ["bar", "bar2"]`.

| `get` call | `bisect_right(times, t)` | index `i-1` | result |
|---|---|---|---|
| `get("foo", 1)` | `bisect_right([1,4], 1)` = 1 | `vals[0]` | `"bar"` |
| `get("foo", 3)` | `bisect_right([1,4], 3)` = 1 | `vals[0]` | `"bar"` |
| `get("foo", 4)` | `bisect_right([1,4], 4)` = 2 | `vals[1]` | `"bar2"` |
| `get("foo", 5)` | `bisect_right([1,4], 5)` = 2 | `vals[1]` | `"bar2"` |
| `get("foo", 0)` | `bisect_right([1,4], 0)` = 0 | `i == 0` | `""` |

**Why it's correct:** `bisect_right` returns the count of timestamps `≤` the query (equivalently, the first index strictly greater). So index `i - 1` is exactly the *largest* timestamp `≤ query`. If `i == 0`, no write happened at or before the query, so `""`. Because writes arrive strictly increasing, the list is sorted without any extra work, which is the precondition binary search needs.

**Complexity:** `set` O(1) amortized (append), `get` O(log n) per call, Space O(n total writes).

---

## ③ Space Optimization

Space is **already optimal — O(n) in the total number of writes**, and that's inherent: `get(key, t)` can ask about *any* past timestamp, so we must retain every `(timestamp, value)` ever set. There's nothing to throw away — no rolling window, no in-place trick — because any earlier write can still be the answer to a future time-travel query. Naming that out loud is the skill:

> *"Space is O(total writes) and that's unavoidable — a get can target any historical timestamp, so I have to keep the full history for each key. Nothing here compresses without losing answers."*

The interesting choice here isn't *less* space — it's how the binary search is written. Three equivalent framings, all O(log n):

- **`bisect.bisect_right` minus one** (above) — shortest, idiomatic Python. The library does the log-n search; you just step back one index.
- **Manual binary search** — write the loop yourself. This is what a Google interviewer usually wants to *see*, to confirm you can implement it, not just call it. (Shown in the Java section — same logic.)
- **`SortedList` / `TreeMap`** — a balanced-BST structure with a built-in `floor` query (Java's `TreeMap.floorKey`). Handy if writes could arrive *out* of timestamp order; overkill here since they're already increasing and a plain appended array stays sorted for free.

> Say it in the room: *"Since writes are strictly increasing, I don't even need a balanced tree — a plain list stays sorted on append, so binary search over the array is O(log n) with O(1) inserts. TreeMap would work too, but it's more machinery than this needs."*

---

## Java (for Java interviewers)

Two clean options. `TreeMap.floorKey` is the one-liner; the manual binary search is the version most interviewers want to watch you write — so here's that, since implementing it *is* the point.

```java
// Manual binary search — the version worth demonstrating.
class TimeMap {
    private final Map<String, List<int[]>> stampIndex = new HashMap<>();
    private final Map<String, List<String>> values = new HashMap<>();

    public TimeMap() { }

    public void set(String key, String value, int timestamp) {
        stampIndex.computeIfAbsent(key, k -> new ArrayList<>())
                  .add(new int[]{timestamp});
        values.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    }

    public String get(String key, int timestamp) {
        List<int[]> stamps = stampIndex.get(key);
        if (stamps == null) return "";
        int lo = 0, hi = stamps.size() - 1, ans = -1;
        while (lo <= hi) {                          // find rightmost ts <= timestamp
            int mid = (lo + hi) >>> 1;
            if (stamps.get(mid)[0] <= timestamp) {
                ans = mid;                          // candidate; try to go further right
                lo = mid + 1;
            } else {
                hi = mid - 1;                       // too big; go left
            }
        }
        return ans == -1 ? "" : values.get(key).get(ans);
    }
}
```

```java
// TreeMap.floorKey — the one-liner, if the interviewer is happy with a library structure.
class TimeMap {
    private final Map<String, TreeMap<Integer, String>> store = new HashMap<>();

    public void set(String key, String value, int timestamp) {
        store.computeIfAbsent(key, k -> new TreeMap<>()).put(timestamp, value);
    }

    public String get(String key, int timestamp) {
        TreeMap<Integer, String> tm = store.get(key);
        if (tm == null) return "";
        Integer floor = tm.floorKey(timestamp);     // largest key <= timestamp
        return floor == null ? "" : tm.get(floor);
    }
}
```

---

## Complexity Summary

| Approach | set | get | Space |
|---|---|---|---|
| Brute force (linear scan) | O(1) | O(n) | O(n total writes) |
| Hash map + binary search | O(1) | O(log n) | O(n total writes) |
| TreeMap / floorKey | O(log n) | O(log n) | O(n total writes) |

*(n = number of writes for the key being queried. TreeMap's `set` is O(log n) because it inserts into a balanced tree; the appended-array version keeps `set` at O(1) precisely because timestamps arrive sorted.)*

---

## Say it out loud (interview narration)

> *"I'll map each key to its list of writes. The naive get scans that whole list — O(n) — and with a hot key that times out. But the key detail is that timestamps arrive strictly increasing, so each key's history is already sorted. That means get is just 'find the rightmost timestamp at or before the query,' which is binary search — an upper bound minus one. So set is O(1), just an append, and get is O(log n). Space is O(total writes) and that's unavoidable, since a query can ask about any past timestamp. In Java I'd either write the binary search by hand or lean on TreeMap.floorKey — but I'd show the manual search since that's usually what you want to see."*

## Related / follow-ups
- **Search Insert Position** (35) — the bare `bisect` primitive this is built on.
- **Find First and Last Position in Sorted Array** (34) — lower/upper bound as two binary searches.
- **Snapshot Array** (1146) — same "value at a version" idea, binary-searched per index.
- **Online Stock Span** (901) — timestamped history, different aggregation.
