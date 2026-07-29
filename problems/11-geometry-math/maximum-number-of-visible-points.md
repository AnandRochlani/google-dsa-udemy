# Maximum Number of Visible Points

> **LeetCode:** 1610. Maximum Number of Visible Points · **Difficulty:** 🔴 Hard · **Pattern:** Angles + Sliding Window · **Google frequency:** ⭐ high

---

## Problem

You're standing at a fixed `location = [x, y]`. You have eyes with a fixed field of view of `angle` **degrees**, and you can rotate freely — but you can't move. Given a list of `points`, count the **most** points you can see at once from some single rotation.

Two rules decide visibility:
- A point that sits at **exactly** your location is *always* visible, no matter which way you face (it's right on top of you).
- Every other point sits at some **angle** relative to you. You see it if that angle falls inside your `angle`-wide viewing wedge. The wedge is inclusive on both edges.

Return the maximum number of points visible from one rotation.

**Example:** `points = [[2,1],[2,2],[3,3]]`, `angle = 90`, `location = [1,1]` → **3**

The three points sit at 0°, 45°, and 45° relative to you. A 90°-wide wedge easily swallows all three at once, so you see all three.

**Example (wraparound):** `points = [[-1,-1],[-1,1]]`, `angle = 90`, `location = [0,0]` → **2**

Those two points sit at −135° and +135°. Naively they look 270° apart — way outside a 90° wedge. But if you face straight *backwards* (toward 180°), both are only 45° off your center line. The short way around is 90°. Face that way and you see both. *(Drop `angle` to 89° and you can only catch one — this is the razor's edge the wraparound has to get right.)*

**Constraints that matter:** `points.length` can be up to **10⁵**. That single number kills the obvious O(n²) "try every wedge against every point" idea — 10¹⁰ operations times out. The target is **O(n log n)**, which screams *sort something*. The thing you sort is the angles.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each possible facing direction, count how many points land in the wedge, keep the best." But there are infinitely many directions. So you narrow it: the *best* wedge can always be nudged until its left edge lines up with some actual point's angle — sliding it further would only lose points, never gain them. So you only need to try `n` starting directions, one per point. For each, scan all points → **O(n²)**. Correct, but too slow for 10⁵.
- **Where it hurts:** every one of those `n` wedge-placements re-scans the whole point set from scratch. You're throwing away the fact that the points, if you'd just **sorted them by angle**, form a line you could sweep once instead of re-scanning `n` times.
- **The leap:** turn each point into a single number — its **polar angle** from your location, via `atan2(dy, dx)`. Sort those angles. Now "points inside a wedge" becomes "a contiguous run of sorted angles spanning at most `angle` degrees" — and *contiguous run within a width limit* is textbook **sliding window**. One pass with two pointers instead of `n` full scans.
- **The wraparound catch:** angles live on a circle, not a line. A wedge can straddle the ±180° seam (the −135° / +135° case above). The clean fix: after sorting, **append every angle + 360**. Now a window that wraps around the seam shows up as an ordinary contiguous window in the extended array — no special-casing.
- **Pattern trigger:** **"points around a center + a fixed angular width"** → **convert to angles, sort, slide a window**. And whenever angles are involved, the reflex is: *handle the circular wraparound by duplicating +360*, and *guard the float comparison with an epsilon*.

---

## ① Brute Force

Turn every point into an angle, then try aligning the **left edge** of the wedge with each point's angle. For each alignment, count how many points fall within `angle` degrees (going clockwise, with wraparound via `% 360`). Keep the best.

```python
import math

def visiblePoints_brute(points, angle, location):
    same = 0
    angs = []
    lx, ly = location
    for x, y in points:
        if x == lx and y == ly:
            same += 1                       # on top of you → always visible
            continue
        angs.append(math.degrees(math.atan2(y - ly, x - lx)))

    best = 0
    for start in angs:                      # try left edge = each point's angle
        count = 0
        for a in angs:
            diff = (a - start) % 360        # clockwise distance from the edge
            if diff <= angle + 1e-9:        # inside the wedge? (epsilon for floats)
                count += 1
        best = max(best, count)
    return best + same
```

**Why it's the natural first attempt:** it mirrors the honest instinct — a wedge only needs to start at some real point, so try each real point as the wedge's leading edge and count what fits. The `% 360` even handles wraparound correctly.

**Why it's not enough:** it's a nested loop — `n` alignments, each scanning all `n` points → **O(n²)**. At 10⁵ points that's 10¹⁰ comparisons and a guaranteed Time Limit Exceeded. It re-counts the same neighborhoods over and over instead of sweeping them once.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution

Same angle idea — but instead of `n` independent scans, **sort the angles once** and slide a single window across them. Duplicate every angle `+ 360` first so a window that wraps the seam is just a normal contiguous window.

```python
import math

def visiblePoints(points, angle, location):
    same = 0
    angles = []
    lx, ly = location
    for x, y in points:
        if x == lx and y == ly:
            same += 1                        # sits on you → always visible
            continue
        # polar angle of this point, in degrees, relative to where you stand
        angles.append(math.degrees(math.atan2(y - ly, x - lx)))

    angles.sort()
    # duplicate every angle + 360 so a wedge can wrap past the ±180° seam
    angles += [a + 360 for a in angles]

    best = 0
    left = 0
    for right in range(len(angles)):
        # shrink from the left while the arc is wider than our field of view
        while angles[right] - angles[left] > angle + 1e-9:   # epsilon: float safety
            left += 1
        best = max(best, right - left + 1)   # widest arc that still fits

    return best + same                       # plus the always-visible on-you points
```

**Walk the first example** `points = [[2,1],[2,2],[3,3]]`, `angle = 90`, `location = [1,1]`.

Angles: `[2,1]→` `atan2(0,1)=0°`, `[2,2]→atan2(1,1)=45°`, `[3,3]→atan2(2,2)=45°`. No point sits on you, so `same = 0`.
Sorted: `[0, 45, 45]`. Extended `+360`: `[0, 45, 45, 360, 405, 405]`.

| `right` | `angles[right]` | shrink `left` while gap > 90 | window `[left..right]` | size | `best` |
|---|---|---|---|---|---|
| 0 | 0 | — | `[0]` | 1 | 1 |
| 1 | 45 | 45−0=45 ✓ | `[0,45]` | 2 | 2 |
| 2 | 45 | 45−0=45 ✓ | `[0,45,45]` | 3 | **3** |
| 3 | 360 | 360−0>90 → left→1,2,3 | `[360]` | 1 | 3 |
| 4 | 405 | 405−360=45 ✓ | `[360,405]` | 2 | 3 |
| 5 | 405 | 45 ✓ | `[360,405,405]` | 3 | 3 |

`best = 3`, `same = 0` → **3**. ✅ A 90° wedge from 0° to 45° catches all three.

**Why the wraparound duplication works:** take the seam case `angles = [-135, 135]`, `angle = 90`. Extended array: `[-135, 135, 225, 495]`. The pair `135` and `225` has gap `90 ≤ 90` — a window of size 2. But `225` is just `-135 + 360`, so that window is really "the point at 135° and the point at −135°, viewed through the 180° seam." Duplicating `+360` lets the linear sliding window discover circular windows for free — no seam special-case, no modular arithmetic in the hot loop.

**Why it's correct:** sorting makes "points within an `angle`-wide wedge" identical to "a contiguous run of sorted angles whose span ≤ `angle`." The two-pointer sweep visits every maximal such run exactly once — `left` only ever moves forward, so it's a true O(n) sweep, not a re-scan. Every valid circular wedge appears as a linear window in the `+360` extension, so we never miss the wraparound optimum. The on-you points are always visible regardless of facing, so they're counted once at the end, outside the window.

**Watch the floating point:** `atan2` returns floats, so an angle that *should* sit exactly on the wedge edge can come back as `angle + 1e-14` and get wrongly dropped. Comparing against `angle + 1e-9` keeps genuine edge points inside. Miss this and you fail a boundary test case — a classic silent Hard-problem bug.

**Complexity:** Time `O(n log n)` (the sort dominates; the sweep is O(n)), Space `O(n)`.

---

## ③ Space Optimization

**Already optimal at O(n) — and here's the honest why.** You must convert every point to an angle and sort them, so you're holding `n` angles no matter what; that `O(n)` is intrinsic, not overhead. The one visible "extra" is the `+360` duplication, which doubles the array — but `2n` is still `O(n)`, just a constant factor.

If you truly wanted to shave that constant, you *could* avoid materializing the duplicate: keep the single sorted array and let the window index wrap with modulo, comparing against `angle` with a `+360` correction when `right` laps past the end. It saves a copy but muddies the loop with wrap logic and an easy-to-botch modular comparison — a bad trade in an interview, where a clean, obviously-correct O(n) beats a clever O(n) with a lurking off-by-one.

```python
# The +360 duplicate is the readable choice. It's still O(n) space.
# A modulo-based single-array sweep saves one copy but not the asymptotic class,
# and it trades clarity for a bug-prone wrap condition. Not worth it here.
```

**Complexity:** Time `O(n log n)`, Space `O(n)`.

> Say it out loud: *"Space is O(n) and that's the floor — I have to store an angle per point to sort them. The +360 duplicate is a 2× constant, not a new order. I could sweep a single array with modular indexing to drop the copy, but it wouldn't change O(n) and it invites a wrap-around off-by-one, so I'll keep the clear version."*

---

## Java (for Java interviewers)

```java
public int visiblePoints(List<List<Integer>> points, int angle, List<Integer> location) {
    int same = 0;
    List<Double> angles = new ArrayList<>();
    int lx = location.get(0), ly = location.get(1);
    for (List<Integer> p : points) {
        int x = p.get(0), y = p.get(1);
        if (x == lx && y == ly) { same++; continue; }        // on you → always seen
        angles.add(Math.toDegrees(Math.atan2(y - ly, x - lx)));
    }

    Collections.sort(angles);
    int n = angles.size();
    for (int i = 0; i < n; i++) angles.add(angles.get(i) + 360);  // +360 wraparound

    int best = 0, left = 0;
    for (int right = 0; right < angles.size(); right++) {
        // shrink while the arc exceeds the field of view (epsilon for float edges)
        while (angles.get(right) - angles.get(left) > angle + 1e-9) left++;
        best = Math.max(best, right - left + 1);
    }
    return best + same;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (each point as wedge edge) | O(n²) | O(n) |
| Optimised (sort angles + sliding window) | O(n log n) | O(n) |
| Space-optimised | O(n log n) | O(n) — already the floor |

*(n = number of points.)*

---

## Say it out loud (interview narration)

> *"I can't move, only rotate, so each point is really just an angle relative to me — I'll get those with atan2 and convert to degrees. Points sitting exactly on my location are always visible, so I count them aside. The brute force tries every point as the wedge's leading edge and counts what fits — that's O(n²), too slow at 10⁵. The win: sort the angles, and 'points in a wedge' becomes 'a contiguous run within an angle-wide span' — a sliding window, O(n) after the sort. Two gotchas I'll call out. One: angles are circular, so a wedge can straddle the ±180° seam; I handle that by appending every angle plus 360 so wraparound windows look linear. Two: atan2 gives floats, so I compare against angle plus a tiny epsilon so edge points aren't wrongly dropped. Total: O(n log n) time, O(n) space, dominated by the sort."*

Before coding, ask the one clarifying question that shows you read the spec: *"Points exactly at my location — those are always visible regardless of which way I face, right?"* That's the detail people skip, and surfacing it early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Points That Intersect With Cars / interval-coverage variants** — same "sort + sweep a window" spine, on 1-D intervals instead of angles.
- **Minimum Number of Arrows to Burst Balloons** — sort by a coordinate, sweep, greedily cover; the angular cousin of this problem.
- **Employee Free Time / Merge Intervals** — the circular-vs-linear framing shows up again once you fold intervals onto a timeline.
- **Erect the Fence (convex hull)** — another "polar angle around a point" geometry problem where `atan2` ordering is the core move.
