# 🎬 Recording Script — K Closest Points to Origin
**Pattern: Heaps & Top-K · LeetCode 973 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Kth Largest / Top K Frequent (size-k heap) — previous lessons.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a 2D plane, origin at center, a scatter of points. A caption: "Return the k nearest." A ghosted `math.sqrt()` call appears, then gets a red strike through it.]**

> Google, maps-flavored: *"Here are points on a plane. Return the k closest to the origin."*
>
> Two things trip people here. One — they sort everything, when they only need the closest k, which by now you can smell. Two — they reach for the distance formula and call square root on every point. That square root is both slower *and* a source of floating-point bugs, and we're going to delete it entirely.
>
> Same size-k heap you know, one flip, one clean shortcut. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: points [[3,3],[5,-1],[-2,4]], k = 2. Small dashed lines from origin to each. Answer: [[3,3],[-2,4]].]**

> The problem in one line: **return the k points closest to the origin (0, 0).** Any order.
>
> Tiny example: `[[3,3],[5,-1],[-2,4]]`, k = 2. Distances from origin: `[3,3]` and `[-2,4]` are the two nearest, `[5,-1]` is farthest. Answer: those first two. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — let them feel the waste)*

**[VISUAL: each point gets a distance label via √(x²+y²): [3,3]→√18, [5,-1]→√26, [-2,4]→√20. Then the three sort; the first 2 are sliced.]**

> The obvious move: compute each point's distance, sort by it, take the first k.
>
> `[3,3]` → root 18, `[5,-1]` → root 26, `[-2,4]` → root 20. Sort ascending → `[3,3], [-2,4], [5,-1]`. Take 2. Correct.
>
> Two problems. One — we sorted all n to keep k, the usual waste. Two — every one of those square roots is a floating-point operation that can round two nearly-equal distances the wrong way. Both are fixable.

---

## 4. THE PAIN POINT + PREDICT — `2:10`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The √ symbols pulse red. Below, "√18 < √26  ⟺  18 < 26". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** First the square root. Distance is root of x-squared plus y-squared. But root is *monotonic* — bigger input, bigger output. So ordering by `x² + y²` gives the identical ranking as ordering by the real distance.
>
> **LEARNER:** So I can just... never take the square root? Compare the squared distances as plain integers?
>
> **TEACHER:** Exactly — cheaper and no float error. Now the bigger question. Pause and predict: **I want the k *closest* — the k *smallest* distances. Last time a min-heap tracked the k largest. If I flip that intention, what kind of heap keeps the k smallest, and who sits at the top as the bouncer?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:55`
*(elaboration — derive it)*

**[VISUAL: a small triangle heap with the LARGEST distance at the root. A closer point arrives; the farthest root pops off and rolls away.]**

> **TEACHER:** To keep the k *closest*, use a **max-heap** — a triangle where the *largest* value sits at the top. Key it on squared distance, cap it at k. The top is the *farthest* of your current k closest.
>
> When a new point is nearer than that farthest one, it earns a spot — evict the top, push the newcomer. The bouncer, mirror image: last time it kept the biggest by evicting the smallest; now it keeps the smallest by evicting the biggest.
>
> **LEARNER:** But you said Python's `heapq` is a *min*-heap only. How do I get a max-heap out of it?
>
> **TEACHER:** One trick, and it's everywhere in interviews: **negate the value going in.** Store `-distance`. The most-negative number — the largest true distance — floats to the top of the min-heap. Pop it to evict the farthest. Negate back when you read. A min-heap of negatives *is* a max-heap.

---

## 6. THE KEY MOVE (signaling) — `3:55`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Compare squared distance. Size-k MAX-heap (negate). Evict the farthest."]**

> Two moves, one line each: **compare `x² + y²`, never the square root. Keep a size-k max-heap — negate the distance in Python — and evict the farthest when it overflows.**

---

## 7. CODE IT — LIVE & CHUNKED — `4:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1.]**

> Start empty. We'll store negated squared distances.

```python
import heapq

def k_closest(points, k):
    heap = []                                   # max-heap via negation
```

> **[VISUAL: chunk 2, highlight `dist = x*x + y*y` and the negation.]** For each point, compute squared distance — no sqrt — and push it negated.

```python
    for x, y in points:
        dist = x * x + y * y                    # squared distance, no sqrt
        heapq.heappush(heap, (-dist, x, y))     # negate → largest dist on top
        if len(heap) > k:                       # keep only k closest
            heapq.heappop(heap)                 # evict the farthest
```

> **[VISUAL: chunk 3.]** Strip the coordinates back out.

```python
    return [[x, y] for (_, x, y) in heap]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> Walk the *why*.
>
> `dist = x*x + y*y` — squared distance, integers, exact. The ranking is identical to real distance and there's zero float error.
>
> `(-dist, x, y)` — negating flips the min-heap into a max-heap so the *farthest* point sits at the top, ready to be evicted. We carry `x, y` along so we can rebuild the point at the end.
>
> **LEARNER:** If two points tie on distance, does the tuple fall through to comparing `x`, then `y`? Any crash risk there like we'll see with linked-list nodes?
>
> **TEACHER:** Good instinct, and here you're safe — `x` and `y` are plain integers, so ties resolve harmlessly on them. It only bites when the fall-through would compare *uncomparable* objects. Keep that antenna up; it matters in the very next lesson.
>
> `heappop` on overflow — removes the current farthest, exactly the point least deserving of a top-k slot.

---

## 9. DRY-RUN THE CODE — `6:55`
*(worked example — prove it, close the loop)*

**[VISUAL: the three points; the heap triangle showing negated distances updating.]**

> Run it, k = 2.

| point | dist² | push | size > 2? pop farthest |
|---|---|---|---|
| [3,3] | 18 | (-18,3,3) | no |
| [5,-1] | 26 | (-26,5,-1) | no |
| [-2,4] | 20 | (-20,-2,4) | yes → top is -26 (dist 26) → pop [5,-1] |

> Heap holds `(-20,-2,4)` and `(-18,3,3)` → **`[[-2,4],[3,3]]`** (any order). ✅ The farthest point, `[5,-1]`, got bounced. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:55`
*(transfer to interview)*

**[VISUAL: "Sort: O(n log n). Heap: O(n log k). Quickselect: O(n) avg."]**

> Out loud: *"I compare squared distances to skip the sqrt — same ranking, no float error. Sorting is O(n log n); the size-k max-heap is O(n log k), O(k) space. In Python I negate to fake a max-heap. If they want average linear time and I can reorder the input, quickselect partitions by distance — O(n) average."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:30`
*(depth + honesty)*

**[VISUAL: quickselect partitioning points by distance around a pivot; one side grayed out.]**

> The heap is O(k). For average O(n) *time* with O(1) extra space, and if you may reorder the input, **quickselect** on squared distance:

```python
import random

def k_closest_quickselect(points, k):
    def dist(p):
        return p[0] ** 2 + p[1] ** 2

    lo, hi = 0, len(points) - 1
    while lo < hi:
        pivot = dist(points[random.randint(lo, hi)])
        i, lt, gt = lo, lo, hi
        while i <= gt:                          # 3-way partition by distance
            d = dist(points[i])
            if d < pivot:
                points[lt], points[i] = points[i], points[lt]; lt += 1; i += 1
            elif d > pivot:
                points[gt], points[i] = points[i], points[gt]; gt -= 1
            else:
                i += 1
        if k <= lt:      hi = lt - 1
        elif k > gt + 1: lo = gt + 1
        else:            break                  # rank k lands in the pivot block
    return points[:k]
```

> Trade-off out loud: **heap = O(n log k), O(k), worst-case-safe; quickselect = O(n) average but O(n²) worst and it mutates the input.** The heap is also the natural fit if points *stream in* and you can't hold them all. Heap as default, quickselect as the average-linear upgrade.

---

## 12. YOUR TURN (active recall) — `9:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Find K Closest Elements (LC 658)". A blank editor.]**

> Before the next video, try **Find K Closest Elements** — the k values closest to a target `x` in a *sorted* array. Twist: because it's already sorted, a heap is overkill — binary search plus two pointers beats it. Great reminder that "closest k" doesn't *always* mean heap; the input's structure can offer something faster.

---

## 13. LOCK IT IN — `9:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Never take the square root** — compare `x² + y²`. Monotonic, exact, faster.
> 2. **k closest → size-k MAX-heap**, evict the farthest.
> 3. **Python max-heap = min-heap of negated values.**
>
> The peg: **k closest → max-heap of squared distances; negate to flip heapq.**

---

## 14. CLIFFHANGER — `10:20`
*(open loop to next lesson)*

**[VISUAL: three sorted linked lists side by side, their heads glowing. A blurred title: "Merge k Sorted Lists".]**

> So far the heap held plain numbers or coordinate tuples. But what if each thing in the heap is the *head of a whole sorted linked list*, and popping one means you have to push its *successor* back in? That's how you merge k sorted lists in one elegant sweep — and it's where that tuple-comparison crash I warned you about finally bites. That's the next one, our first Hard: Merge k Sorted Lists. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.PriorityQueue;

public int[][] kClosest(int[][] points, int k) {
    // max-heap by squared distance (largest distance on top)
    PriorityQueue<int[]> heap = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1]));
    for (int[] p : points) {
        heap.offer(p);
        if (heap.size() > k) heap.poll();       // evict the farthest
    }
    int[][] result = new int[k][2];
    for (int i = 0; i < k; i++) result[i] = heap.poll();
    return result;
}
```
