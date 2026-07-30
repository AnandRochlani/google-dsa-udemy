# Amount of New Area Painted Each Day

> **LeetCode:** 2158. Amount of New Area Painted Each Day · **Difficulty:** 🔴 Hard · **Pattern:** Interval union / Union-Find "jump pointer" · **Google frequency:** ⭐ high

---

## Problem

You're given `paint`, where `paint[i] = [start, end]` means on day `i` you paint the **half-open** segment `[start, end)` of an infinite number line — every unit cell `start, start+1, …, end-1`. Return an array `worklog` where `worklog[i]` is the amount of **newly** painted length on day `i` — cells that were *not* already painted on any earlier day. Cells painted before don't count again; you only get credit for fresh area.

**Example:** `paint = [[1,4],[4,7],[5,8]]` → `[3,3,1]`

*(Day 0 paints cells 1,2,3 — all new → 3. Day 1 paints 4,5,6 — all new → 3. Day 2 paints 5,6,7 — but 5 and 6 are already painted, only 7 is fresh → 1.)*

**Constraints that matter:** up to `n = 5·10⁴` days, and each coordinate can be as large as `5·10⁴`. The naive "mark every cell you touch, every day" is `O(n · range)` in the worst case — a day that repaints a huge already-painted span still scans every cell. When many days overlap on the same wide region, that quadratic blowup is exactly what times out. The target is to touch each cell **once across the whole run**, not once per day.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** keep a `set` (or boolean array) of painted cells. Each day, loop `start … end-1`; for every cell not yet in the set, add it and bump the day's counter. Dead simple, obviously correct.
- **Where it hurts:** the loop walks *every* cell in `[start, end)` — even the ones already painted. Picture 50,000 days that all paint `[0, 50000]`. Day 0 does real work; days 1 through 49,999 each re-scan 50,000 cells and paint **nothing**. That's 2.5 billion wasted touches. The waste is the *re-scanning of runs we've already filled.*
- **The leap:** what if, standing on a painted cell, I could **teleport past the entire painted run** in one hop instead of stepping through it? The first time I paint cell `x`, I leave behind a pointer: "next time someone lands on `x`, send them to `x+1`." Chain those pointers and a solid painted block collapses into a single jump straight to its far end. Each cell installs its "skip me" pointer exactly once — so the total work across all days is bounded by the number of cells ever painted, not the sum of the day lengths.
- **Pattern trigger:** **"repeatedly fill intervals, skip what's already filled, find the next free slot fast"** → **Union-Find with a "next unpainted" jump pointer** (a.k.a. the DSU find-successor trick). The transferable move: `parent[x]` doesn't mean "group leader," it means **"the next free coordinate at or after `x`."** Path compression makes each lookup near-`O(1)` amortized. Same skeleton shows up in "find the next available seat/slot" problems.

---

## ① Brute Force

Track painted cells in a set; each day, walk the segment and count cells that are new.

```python
def amountPainted_brute(paint):
    painted = set()
    worklog = []
    for start, end in paint:
        count = 0
        for x in range(start, end):        # walk EVERY cell in [start, end)
            if x not in painted:            # already painted? no credit
                painted.add(x)
                count += 1
        worklog.append(count)
    return worklog
```

**Why it's the natural first attempt:** it's a direct transcription of the problem — "for each cell you paint, was it new?" It's correct and it passes the small tests instantly.

**Why it's not enough:** the inner `range(start, end)` scans the whole segment *every day*, including cells that are already solid. Overlapping days on a wide region turn this into `O(n · range)` — up to ~2.5·10⁹ operations. It's not the counting that's slow; it's **re-walking runs we've already filled.** That's the Time Limit Exceeded.

**Complexity:** Time `O(n · range)` worst case, Space `O(range)` for the set.

---

## ② Optimised Solution

Keep a dict `parent` where `find(x)` returns **the next unpainted coordinate ≥ x**. To paint `[start, end)`: jump to the first free cell at or after `start`, paint it, point it at `x+1` so it's skipped forever, and repeat until we pass `end`. Painted runs collapse into single jumps.

```python
def amountPainted(paint):
    parent = {}                     # parent[x] = next free coordinate at or after x (lazily)

    def find(x):
        # walk the chain to the next unpainted cell, compressing as we go
        root = x
        while root in parent:
            root = parent[root]     # follow the "skip me" pointers
        # path compression: point every hop on the way straight at root
        while x in parent:
            parent[x], x = root, parent[x]
        return root

    worklog = []
    for start, end in paint:
        count = 0
        x = find(start)             # first free cell at or after start
        while x < end:              # still inside today's segment?
            count += 1              # paint it — it's brand new
            parent[x] = x + 1       # union x → x+1: future finds skip past x
            x = find(x + 1)         # teleport to the next free cell
        worklog.append(count)
    return worklog
```

**Walk the example** `paint = [[1,4],[4,7],[5,8]]`:

| Day | Segment | `find` hops | Cells painted (new) | `parent` after | `worklog` |
|---|---|---|---|---|---|
| 0 | `[1,4)` | find(1)=1→paint, find(2)=2→paint, find(3)=3→paint, find(4)=4 ✗ (≥ end) | 1, 2, 3 | 1→2, 2→3, 3→4 | 3 |
| 1 | `[4,7)` | find(4)=4→paint, find(5)=5→paint, find(6)=6→paint, find(7)=7 ✗ | 4, 5, 6 | +4→5, 5→6, 6→7 | 3 |
| 2 | `[5,8)` | find(5) **chains 5→6→7**=7→paint, find(8)=8 ✗ | 7 only | +7→8 | 1 |

The magic is Day 2: cell `5` is already painted, so `find(5)` doesn't step through 5 then 6 then 7 — it *follows the pointers* `5→6→7` in one collapsed hop and lands directly on the first free cell, `7`. We paint only `7`. Result `[3, 3, 1]`. ✅

**Why it's correct:** the invariant is that `find(x)` always returns the smallest unpainted coordinate `≥ x`. When we paint `x`, setting `parent[x] = x+1` says "x is now occupied — the next candidate is x+1," and path compression keeps future lookups short without changing where they land. So the `while x < end` loop paints *exactly* the cells in `[start, end)` that were free, and skips every already-painted cell without visiting it. Each coordinate gets `parent` set **at most once ever** (once painted, it stays painted), so across all days the total number of paint-steps equals the number of distinct cells ever painted — every unit of new area is counted exactly once.

**Complexity:** Time `O((total newly-painted cells + n) · α)` ≈ near-linear in the painted area (α = inverse Ackermann, effectively constant). Space `O(painted cells)` for the dict.

---

## ③ Space Optimization

The dict already holds only what's been painted — one entry per painted cell, nothing per *day* and nothing for untouched coordinates. That sparseness is the whole point of using a dict instead of an array: if coordinates were huge and sparse (say up to 10⁹ but only a few thousand painted), an array would waste `O(range)` while the dict stays at `O(painted)`.

```python
# The dict IS the space optimization vs. a size-`range` boolean array.
# It stores exactly the painted coordinates — O(painted cells), not O(range).
# There's no smaller representation: to know a cell is painted you must
# remember it, and every stored cell corresponds to real returned area.
```

**Complexity:** Time `O((painted + n)·α)`, Space `O(painted cells)`.

> Say it out loud: *"Space is O(number of painted cells), and that's optimal — I have to remember which cells are painted to avoid double-counting, and each stored cell maps to real area I returned. The dict beats a boolean array whenever the coordinate range is large and sparse."* An alternative with the *same* asymptotics is a sorted map of merged painted intervals (TreeMap in Java): store painted runs as `[lo, hi)` intervals and subtract overlaps. It's `O(n log n)` and stores `O(number of runs)` — often fewer entries — but the jump-pointer DSU is simpler to get right under pressure and has a better constant. I'd lead with the DSU and mention the interval-map as the alternative.

---

## Java (for Java interviewers)

```java
public int[] amountPainted(int[][] paint) {
    // parent.get(x) = next free coordinate at or after x (absent = x itself is free)
    Map<Integer, Integer> parent = new HashMap<>();
    int[] worklog = new int[paint.length];

    for (int i = 0; i < paint.length; i++) {
        int start = paint[i][0], end = paint[i][1];
        int count = 0;
        int x = find(parent, start);          // first free cell >= start
        while (x < end) {                      // still inside today's segment?
            count++;                           // brand-new cell
            parent.put(x, x + 1);              // union x -> x+1: skip x forever
            x = find(parent, x + 1);           // teleport to next free cell
        }
        worklog[i] = count;
    }
    return worklog;
}

// find with iterative path compression
private int find(Map<Integer, Integer> parent, int x) {
    int root = x;
    while (parent.containsKey(root)) root = parent.get(root);
    while (parent.containsKey(x)) {
        int next = parent.get(x);
        parent.put(x, root);                   // compress: point straight at root
        x = next;
    }
    return root;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (mark every cell each day) | O(n · range) | O(range) |
| Optimised (jump-pointer DSU) | O((painted + n) · α) ≈ near-linear | O(painted cells) |
| Alternative (sorted interval map) | O(n log n) | O(number of runs) |

*(n = number of days; range = max coordinate span; α = inverse Ackermann, effectively constant.)*

---

## Say it out loud (interview narration)

> *"Brute force is a set of painted cells — each day I walk the segment and count the new ones. Correct, but it re-scans already-painted runs every day, so overlapping days on a wide region blow up to O(n·range) and time out. The fix: instead of stepping through painted cells, I teleport past them. I keep a map where find(x) gives the next unpainted coordinate at or after x. To paint a segment, I jump to the first free cell, paint it, point it at the next coordinate so it's skipped forever, and repeat until I pass the end. Painted runs collapse into single jumps via path compression. Each cell is painted at most once ever, so total work is near-linear in the painted area. Space is O(painted cells) — I use a dict so sparse huge coordinates cost nothing. If you'd prefer, a sorted interval map merging painted runs is the O(n log n) alternative."*

Before you code, ask the one clarifying question that proves you read the spec: *"The intervals are half-open — `[start, end)`, so a segment `[4,7]` paints cells 4, 5, 6 and not 7, right?"* That off-by-one decides every boundary in the loop, and asking it early is exactly the General Cognitive Ability signal Google rewards.

## Related / follow-ups
- **Range Module (LC 715)** — add/remove/query painted ranges; the sorted-interval-map cousin of this problem.
- **Data Stream as Disjoint Intervals (LC 352)** — merge points into runs as they arrive; same interval-union idea.
- **Car Pooling / My Calendar series (LC 1094, 729, 731)** — sweep-line and interval-overlap counting.
- **Number of Increasing Paths / Smallest String With Swaps** — more Union-Find where `parent[x]` means something clever, not just "leader."
