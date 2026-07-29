# Minimum Time Difference

> **LeetCode:** 539. Minimum Time Difference · **Difficulty:** 🟡 Medium · **Pattern:** Sorting / Pigeonhole · **Google frequency:** ⭐ high

---

## Problem

Given a list of times in `"HH:MM"` 24-hour format, return the **smallest difference in minutes** between any two of them. The catch: these are times **on a clock**, so the day wraps — `"23:59"` and `"00:00"` are only **one minute** apart, not 1439.

**Example:** `["23:59","00:00"]` → `1` *(they straddle midnight, so the short way round the clock is one minute, not the long way of 1439)*

**Example:** `["00:00","23:59","00:00"]` → `0` *(two identical times → zero minutes apart)*

**Constraints that matter:** times are `"00:00"`…`"23:59"`, so there are only **1440 possible distinct values** (minutes in a day). That single fact does two things: it lets you shortcut to `0` the instant you have more than 1440 entries (pigeonhole → a duplicate must exist), and it means the input, however large, only ever spans a fixed 1440-slot space. `n` can be big, but the *value range* is tiny and bounded.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Compare every pair, convert each to a number of minutes, take the smallest gap." That's `O(n²)` and it works — but it also quietly ignores the part that actually makes this problem a problem: the clock **wraps around**.
- **Where it hurts:** two places. First, `O(n²)` pairwise comparison is wasteful when the values live in a tiny fixed range. Second — and this is the real trap — if you just take `abs(a − b)` you'll call `"23:59"` and `"00:00"` a difference of `1439`. The true answer is `1`, going the *short way* around the dial. Miss the wraparound and you pass the easy tests and fail the interview.
- **The leap:** convert every time to **minutes since midnight** (a number in `0..1439`) and **sort**. Once sorted, the closest pair *the normal way* is always two **adjacent** entries — no need to check all pairs. Then handle the clock: the last time and the first time are also "adjacent" across midnight, and their wrap distance is `(first + 1440) − last`. The answer is the min over all adjacent gaps **plus** that one wraparound gap.
- **Pattern trigger:** **"values live in a small fixed range + find the closest pair"** → **sort, then scan neighbors**. And **"more items than possible distinct values"** → **pigeonhole → a duplicate exists → answer is 0**. The transferable move: when the value space is bounded and tiny, stop thinking `O(n²)` and start thinking *sort the line up and look next-door*.

---

## ① Brute Force

Convert each time to minutes, then compare **every pair**, taking the clock-aware min of each gap.

```python
def find_min_difference_brute(timePoints):
    def to_min(t):
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    mins = [to_min(t) for t in timePoints]
    best = float("inf")
    for i in range(len(mins)):
        for j in range(i + 1, len(mins)):
            diff = abs(mins[i] - mins[j])
            # clock-aware: the short way is min(diff, a full day - diff)
            best = min(best, diff, 1440 - diff)
    return best
```

**Why it's the natural first attempt:** "smallest difference between any two" reads like "check all pairs." And folding the wraparound into `min(diff, 1440 - diff)` per pair is a clean way to respect the clock.

**Why it's not enough:** it's `O(n²)`. When `n` is large that's too slow — and it's *needlessly* slow, because the values only ever occupy 1440 slots. We're comparing far-apart times that could never be the closest pair. Sorting throws all that wasted comparison away.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution

Two moves. **First, the pigeonhole shortcut:** if there are more than 1440 times, two must land on the same minute — return `0` without any work. **Then sort** the minute values; the closest pair is adjacent, and the only "hidden" pair is the wraparound between last and first.

```python
def find_min_difference(timePoints):
    # ── pigeonhole shortcut: >1440 times can't all be distinct ──
    if len(timePoints) > 1440:
        return 0

    def to_min(t):
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    mins = sorted(to_min(t) for t in timePoints)

    # ── smallest gap between adjacent sorted times ──
    best = min(b - a for a, b in zip(mins, mins[1:]))

    # ── the wraparound pair: last → first, across midnight ──
    wrap = (mins[0] + 1440) - mins[-1]

    return min(best, wrap)
```

**Walk the example** `["23:59","00:00"]`:

| Step | Value |
|---|---|
| Convert | `"23:59"` → `1439`, `"00:00"` → `0` |
| Sort | `[0, 1439]` |
| Adjacent gaps | `1439 - 0 = 1439` → `best = 1439` |
| Wraparound | `(0 + 1440) - 1439 = 1` |
| Answer | `min(1439, 1) = ` **`1`** ✅ |

The naive adjacent scan alone would have shouted `1439`. The wraparound term is the whole reason we land on `1`.

And the duplicate case `["00:00","23:59","00:00"]`: convert → `[0, 1439, 0]`, sort → `[0, 0, 1439]`. Adjacent gap `0 - 0 = 0` → `best = 0`. Answer is `0`. ✅ *(here the pigeonhole shortcut doesn't fire — only 3 entries — but sorting surfaces the duplicate as a zero-gap neighbor.)*

**Why it's correct:** after sorting, any two non-adjacent times have at least one time *between* them, so their gap is no smaller than one of the adjacent gaps — the minimum "normal" difference must be between neighbors. That covers every pair except the one that crosses midnight, and there's exactly one such pair to worry about: earliest and latest. Its short-way distance is `(first + 1440) − last`. Take the min of the adjacent scan and that single wrap term and you've considered every clock-distance that could be the answer. The pigeonhole check is just an early exit: with 1440 possible minute-values, a 1441st entry forces a collision, so the answer is provably `0`.

**Complexity:** Time `O(n log n)` for the sort, Space `O(n)` for the minute list.

---

## ③ Space Optimization

We can drop the `O(n)` sort. Because every value is an integer in `0..1439`, use a **1440-slot boolean bucket array** instead — mark each minute as seen, and while marking, if a slot is already taken you've found a duplicate and return `0`. Then sweep the buckets in order, which gives the times *pre-sorted* for free.

```python
def find_min_difference_bucket(timePoints):
    seen = [False] * 1440
    for t in timePoints:
        h, m = t.split(":")
        minute = int(h) * 60 + int(m)
        if seen[minute]:      # duplicate → zero gap
            return 0
        seen[minute] = True

    prev = first = last = -1
    best = 1440
    for minute in range(1440):     # sweep in sorted order
        if not seen[minute]:
            continue
        if prev != -1:
            best = min(best, minute - prev)
        else:
            first = minute
        prev = last = minute

    best = min(best, (first + 1440) - last)   # wraparound
    return best
```

**Complexity:** Time `O(n + 1440)` = `O(n)`, Space `O(1440)` = `O(1)` — the bucket array is a fixed size, independent of `n`.

> The trade is real: the bucket version is `O(n)` time and `O(1)` extra space (a constant 1440 booleans), beating the sort's `O(n log n)`. It only works *because* the value range is fixed and small — which is exactly the property the problem hands you. In an interview, lead with the sort (it's shorter and obviously correct), then mention the bucket array as "if I exploit the 1440-value range, I can get it to linear time and constant space." Naming that upgrade is the strong-hire signal.

---

## Java (for Java interviewers)

```java
public int findMinDifference(List<String> timePoints) {
    // pigeonhole: >1440 times must contain a duplicate
    if (timePoints.size() > 1440) return 0;

    int[] mins = new int[timePoints.size()];
    for (int i = 0; i < timePoints.size(); i++) {
        String t = timePoints.get(i);
        int h = Integer.parseInt(t.substring(0, 2));
        int m = Integer.parseInt(t.substring(3, 5));
        mins[i] = h * 60 + m;
    }
    Arrays.sort(mins);

    int best = Integer.MAX_VALUE;
    for (int i = 1; i < mins.length; i++) {
        best = Math.min(best, mins[i] - mins[i - 1]);   // adjacent gap
    }
    // wraparound: last → first across midnight
    best = Math.min(best, (mins[0] + 1440) - mins[mins.length - 1]);
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all pairs) | O(n²) | O(n) |
| Optimised (sort + neighbor scan) | O(n log n) | O(n) |
| Space-optimised (1440 bucket array) | O(n) | O(1) — fixed 1440 slots |

---

## Say it out loud (interview narration)

> *"First a clarifying question: these are clock times, so `23:59` and `00:00` are one minute apart, not 1439 — the difference wraps around midnight, right? Good. So my plan: convert each `HH:MM` to minutes since midnight, a number from 0 to 1439. Brute force compares all pairs — `O(n²)` — but I can do better. There are only 1440 possible values, so if I have more than 1440 times, two must collide by pigeonhole and the answer is instantly zero. Otherwise I sort, and the closest pair is always adjacent — one linear scan. The one pair a plain scan misses is the wraparound between the earliest and latest time, which is `(first + 1440) − last`. Min of the adjacent gaps and that wrap term is the answer. That's `O(n log n)`. If you want linear, I can bucket into a 1440-boolean array instead of sorting — `O(n)` time, `O(1)` space, because the value range is fixed."*

The wraparound is the detail interviewers are watching for. Say it *before* you write code — that clarifying question is exactly what Google's rubric rewards.

## Related / follow-ups
- **Minimum Absolute Difference (LC 1200)** — same "sort, then closest pair is adjacent" move, without the clock wrap.
- **Contains Duplicate / Contains Duplicate II** — the pigeonhole "a collision must exist" instinct.
- **Maximum Gap (LC 164)** — sorted neighbors again, but now you want the *largest* adjacent gap (and bucket/pigeonhole gets you linear).
- **Add Binary / valid time formats** — sibling `HH:MM` parsing problems where the conversion-to-a-number step is the unlock.
