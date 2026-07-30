# Detect Squares

> **LeetCode:** 2013. Detect Squares · **Difficulty:** 🟡 Medium · **Pattern:** Design / hash-map counting · **Google frequency:** ⭐ high

---

## Problem

Design a data structure that streams in 2-D points and, on demand, counts squares. Two operations:

- **`add([x, y])`** — record a point. Points can repeat, and **duplicates count** — if you add `[1,1]` three times, there are three copies sitting there.
- **`count([x, y])`** — given a *query* point, return how many **axis-aligned squares of positive area** you can form using the query point as one corner and **three previously added points** as the other three corners.

"Axis-aligned" means the sides run parallel to the x- and y-axes — no tilted squares. "Positive area" means the side length can't be zero.

**Example:**

```
add([3, 10])
add([11, 2])
add([3, 2])
count([11, 10])  → 1
count([14, 8])   → 0
```

*(For `count([11,10])`: the three stored points `(3,10)`, `(11,2)`, `(3,2)` plus the query `(11,10)` form one 8×8 square. For `count([14,8])`: no combination of stored points closes a square with it.)*

**Constraints that matter:** coordinates are small (`0 ≤ x, y ≤ 1000`), and you can call `add`/`count` up to `5000` times. That total-calls bound is the real target: `count` is allowed to scan the points you've stored, but it must **not** do a triple-nested loop over all points. We want `add` in `O(1)` and `count` in `O(number of stored points)` — linear per query, not cubic.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "To count squares at the query point, try every triple of stored points and check if the four points form a square." That's `add` in O(1) but `count` in `O(k³)` over `k` stored points — with thousands of points per query, that's hopeless. You immediately feel the waste: you're blindly testing triples that share no geometry with the query.
- **Where it hurts:** a square is over-specified by four corners. You're brute-forcing all four when the query already **hands you one for free**. Fixing one corner should slash the search — but a corner alone still leaves too many squares to enumerate (a corner touches two sides).
- **The leap:** fix **two** corners instead of one. The query point `(qx, qy)` is one corner; pick a stored point `(px, py)` to be the **diagonally opposite** corner. Here's the magic: *for an axis-aligned square, the two diagonal corners completely determine the other two.* If `(qx,qy)` and `(px,py)` are opposite corners, the remaining two corners are forced to be `(qx, py)` and `(px, qy)` — the two "swap one coordinate" points. So I don't search for the other two; I **compute** them and look up how many copies exist.
- **What makes a valid diagonal:** the diagonal of an axis-aligned square runs corner-to-corner, so its horizontal and vertical spans are equal: `|px − qx| == |py − qy|`. And positive area means that span can't be zero: `px ≠ qx`. Every stored point passing that test is a candidate diagonal — one loop, no triples.
- **Pattern trigger:** **"count configurations anchored at a query point + duplicates matter"** → **hash-map counting keyed by coordinate**. The transferable move: *when a shape is fixed by two of its points, iterate the second point and multiply lookups for the rest.* Duplicates just turn "does it exist?" into "how many?" — a product of multiplicities.

---

## ① Brute Force

Store every point in a list. For `count`, try all triples of stored points and check whether they plus the query form an axis-aligned square.

```python
from itertools import combinations

class DetectSquaresBrute:
    def __init__(self):
        self.points = []                       # raw list, duplicates kept

    def add(self, point):
        self.points.append(tuple(point))

    def count(self, point):
        qx, qy = point
        total = 0
        # try every triple of stored points as the other three corners
        for a, b, c in combinations(self.points, 3):
            corners = {a, b, c, (qx, qy)}
            xs = {x for x, _ in corners}
            ys = {y for _, y in corners}
            # a square has exactly 2 distinct x's and 2 distinct y's, equal gaps
            if len(xs) == 2 and len(ys) == 2:
                (x1, x2), (y1, y2) = sorted(xs), sorted(ys)
                if x2 - x1 == y2 - y1 and x2 > x1:
                    # and all four grid corners are actually present
                    if {(x1, y1), (x1, y2), (x2, y1), (x2, y2)} == corners:
                        total += 1
        return total
```

**Why it's the natural first attempt:** it mirrors the definition — "three other points that make a square" — literally, testing every possible three.

**Why it's not enough:** with `k` stored points, `count` is `O(k³)`. At 5000 calls with thousands of points each, this times out instantly. Worse, it fumbles duplicates: `combinations` over a list double-counts in a way that's hard to reason about, and the `set` of corners silently collapses repeats. You're doing enormous work to rediscover geometry the query already gave you.

**Complexity:** `add` `O(1)`; `count` `O(k³)`. Space `O(k)`.

---

## ② Optimised Solution

Keep a **counter keyed by `(x, y)`** so duplicates become multiplicities. For `count`, loop over each distinct stored point as the **diagonal** corner; the other two corners are then forced, so just multiply their counts.

```python
from collections import Counter

class DetectSquares:
    def __init__(self):
        self.cnt = Counter()                   # (x, y) -> how many copies added

    def add(self, point):
        self.cnt[tuple(point)] += 1            # O(1); duplicates increment

    def count(self, point):
        qx, qy = point
        total = 0
        # each stored point is a candidate DIAGONAL corner (px, py)
        for (px, py), c in self.cnt.items():
            # valid diagonal of an axis-aligned square:
            #   equal horizontal & vertical span, and non-zero (positive area)
            if abs(px - qx) == abs(py - qy) and px != qx:
                # the two diagonal corners force the other two corners:
                #   (qx, py) and (px, qy)  — swap one coordinate each
                total += c * self.cnt[(qx, py)] * self.cnt[(px, qy)]
        return total
```

**Walk the example** — `add([3,10])`, `add([11,2])`, `add([3,2])`, then `count([11,10])`. The counter holds `{(3,10):1, (11,2):1, (3,2):1}`. Query `(qx,qy) = (11,10)`:

| Candidate diagonal `(px,py)` | `abs(px−11)==abs(py−10)`? | `px≠11`? | Other corners `(qx,py)`,`(px,qy)` | Contribution |
|---|---|---|---|---|
| `(3,10)` | `abs(-8)=8` vs `abs(0)=0` → no | — | — | 0 |
| `(11,2)` | `abs(0)=0` vs `abs(-8)=8` → no (also `px==qx`) | no | — | 0 |
| `(3,2)` | `abs(-8)=8` vs `abs(-8)=8` → **yes** | yes | `(11,2)` and `(3,10)` | `1 · cnt[(11,2)] · cnt[(3,10)]` = `1·1·1` = **1** |

Total = **1**. ✅ The one square is `(11,10)–(3,10)–(3,2)–(11,2)`, an 8×8.

**Why it's correct:** an axis-aligned square is uniquely pinned down by its **two diagonal corners** — once you fix `(qx,qy)` and an opposite corner `(px,py)`, the remaining corners *must* be `(qx,py)` and `(px,qy)`, no choice. The test `abs(px−qx)==abs(py−qy)` guarantees the diagonal spans a real square (equal legs), and `px≠qx` rules out the degenerate zero-area case (which also excludes `py==qy`, since the spans are equal). Every square with a corner at the query has exactly **one** diagonal partner among the corners, so looping candidate diagonals counts each square exactly once — no double counting. Multiplying the three multiplicities `c · cnt[(qx,py)] · cnt[(px,qy)]` counts every *combination* of duplicate copies, which is exactly what "duplicates count" demands.

**Complexity:** `add` `O(1)`; `count` `O(d)` where `d` is the number of **distinct** stored points. Space `O(d)`.

---

## ③ Space Optimization

**Already optimal — and here's the honest why.** You have to remember every point you've been given, because any future `count` might need it as a corner. So `O(d)` distinct points (plus their multiplicities in one integer each) is the floor — there's nothing to roll away or recompute on the fly.

There *is* a **time** refinement worth naming, though. Instead of one flat counter, group points **by column**: a dict `x → Counter of y-values seen at that x`. Then `count` only scans the y's that share the query's column-partners, shrinking the constant factor when points cluster. It doesn't change the `O(d)` worst case, but it's the natural "by-column" optimization an interviewer may nudge you toward.

```python
from collections import Counter, defaultdict

class DetectSquaresByColumn:
    def __init__(self):
        self.cnt = Counter()                       # (x,y) -> multiplicity
        self.cols = defaultdict(Counter)           # x -> Counter of y's in that column

    def add(self, point):
        x, y = point
        self.cnt[(x, y)] += 1
        self.cols[x][y] += 1

    def count(self, point):
        qx, qy = point
        total = 0
        # only walk points that share the query's column — same (px,py) role
        for py, c in self.cols[qx].items():
            side = abs(py - qy)
            if side == 0:                          # zero area — skip
                continue
            # the diagonal corner sits `side` to the left or right
            for px in (qx - side, qx + side):
                total += c * self.cnt[(px, qy)] * self.cnt[(px, py)]
        return total
```

**Complexity:** `add` `O(1)`; `count` `O(h)` where `h` is the number of distinct y-values in the query's column (`≤ d`). Space `O(d)`.

> Say it out loud: *"Space is O(distinct points) and that's the floor — I can't forget a point I might need as a corner later. If you want a tighter constant, I'd bucket points by column so count only scans one column's y-values, but the worst case is still linear in the points."*

---

## Java (for Java interviewers)

```java
class DetectSquares {
    // encode (x, y) as one key x*1001 + y since 0 <= x, y <= 1000
    private final Map<Integer, Integer> cnt = new HashMap<>();

    public DetectSquares() {}

    public void add(int[] point) {
        int key = point[0] * 1001 + point[1];
        cnt.merge(key, 1, Integer::sum);           // duplicates increment
    }

    public int count(int[] point) {
        int qx = point[0], qy = point[1];
        int total = 0;
        // iterate a copy of the entries; each stored point is a candidate diagonal
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            int px = e.getKey() / 1001, py = e.getKey() % 1001;
            // valid diagonal: equal span both ways, non-zero (positive area)
            if (Math.abs(px - qx) == Math.abs(py - qy) && px != qx) {
                int c = e.getValue();
                int a = cnt.getOrDefault(qx * 1001 + py, 0);   // corner (qx, py)
                int b = cnt.getOrDefault(px * 1001 + qy, 0);   // corner (px, qy)
                total += c * a * b;
            }
        }
        return total;
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all triples) | `add` O(1), `count` O(k³) | O(k) |
| Optimised (counter + diagonal corner) | `add` O(1), `count` O(d) | O(d) |
| By-column refinement | `add` O(1), `count` O(h ≤ d) | O(d) |

*(k = total points stored, d = distinct points, h = distinct y's in the query's column.)*

---

## Say it out loud (interview narration)

> *"First let me clarify: axis-aligned squares only, positive area, and duplicate points each count separately — right? Good. The naive move is to try every triple of stored points, but that's cubic per query and it times out. The key insight is that a square is pinned down by its two **diagonal** corners — so I fix the query as one corner, then loop over each stored point as the opposite corner. The moment I pick that diagonal, the other two corners are forced to `(qx, py)` and `(px, qy)`, so I just multiply how many copies of each exist. A valid diagonal needs `abs(dx) == abs(dy)` and `dx ≠ 0` for positive area. I'll store points in a hash-map keyed by coordinate with a multiplicity count — add is O(1), count is linear in the distinct points. If you want a tighter constant I'd bucket by column so I only scan one column's y-values."*

Ask the clarifying question first — *"do duplicate points count as separate corners?"* — before you write anything. That one question is a General Cognitive Ability signal, and it changes the code from `+= 1` to `+= c * a * b`.

## Related / follow-ups
- **Number of Boomerangs (LC 447)** — same "anchor at a point, hash the geometry, count configurations" DNA, with distances instead of squares.
- **Max Points on a Line (LC 149)** — anchor + hash-map counting, keyed by slope.
- **Minimum Area Rectangle (LC 939)** — axis-aligned rectangles from a point set; the diagonal-corners idea generalizes.
- **Rectangle Area / Detect overlapping shapes** — more coordinate-hashing geometry under interview time pressure.
