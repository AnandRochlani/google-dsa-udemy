# 🎬 Recording Script — Top K Frequent Elements
**Pattern: Heaps & Top-K · LeetCode 347 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Kth Largest (size-k heap) — previous lesson.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a search-log firehose scrolling. A caption: "Return the 2 most-searched terms." Then a LeetCode note flashes: "must be better than O(n log n)".]**

> Google, product-flavored: *"Here's a stream of search terms. Give me the k most frequent."*
>
> And this time the problem itself throws down a gauntlet — right there in the constraints: *"your algorithm must be better than O(n log n)."* So the lazy "count them, sort by frequency" answer is explicitly ruled out.
>
> Two ideas beat it. One you already know — the size-k heap. One is a slick linear-time trick that only works because of something special about frequencies. By the end you'll have both. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: tiles `1 1 1 2 2 3`, k = 2. Count badges: 1→3×, 2→2×, 3→1×. Answer: [1, 2].]**

> The problem in one line: **return the k most frequent elements.** Any order.
>
> Tiny example: `[1,1,1,2,2,3]`, k = 2. One appears three times, two appears twice, three appears once. The two most frequent are `1` and `2`. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — let them feel the waste)*

**[VISUAL: a count map building: {1:3, 2:2, 3:1}. Then the distinct keys sorting by count: [1, 2, 3]. A finger slices the first 2.]**

> Step one is *forced* — you can't rank by frequency without counting, so one O(n) pass builds the count map `{1:3, 2:2, 3:1}`. No avoiding that.
>
> Step two, the obvious move: sort the *distinct* elements by count, take the top k. Sorted: `[1, 2, 3]`, slice 2 → `[1, 2]`. Correct.
>
> But that sort is O(m log m) in the number of distinct elements — up to O(n log n). That's the exact wall the problem told us to beat. We fully ordered when we only needed the top two.

---

## 4. THE PAIN POINT + PREDICT — `2:10`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The sorted-by-count list, top-2 green, the rest grayed "didn't need this order". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Same waste as last lesson, one layer up. I don't want a full frequency ranking — just the top k by count.
>
> **LEARNER:** So this is Kth Largest again… except the "size" I'm comparing isn't the number itself, it's its frequency. Can the heap sort by a computed key like that?
>
> **TEACHER:** It absolutely can. Pause and predict: **if I keep a size-k min-heap but key it on frequency instead of value — what does the top of that heap represent, and who do I evict when it overflows?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:50`
*(elaboration — derive it)*

**[VISUAL: a small triangle heap holding (freq, element) pairs, the smallest FREQUENCY at the root. A new element with higher freq arrives; the low-freq root pops off.]**

> **TEACHER:** Count first — that's forced. Then keep a **min-heap keyed on frequency**, capped at size k. Each entry is a `(freq, element)` pair, and Python compares tuples by the first field, so the *lowest-frequency* pair sits at the top.
>
> That top is the weakest member of your current top-k — the least frequent of the ones you're keeping. When a more frequent element shows up, evict the top and push it in. Exactly the bouncer from last lesson, now guarding by count.
>
> Process all m distinct elements → O(m log k). The heap never fully orders anything; it just maintains the k strongest.

---

## 6. THE KEY MOVE (signaling) — `3:45`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Count, then size-k min-heap keyed on frequency. Evict the least frequent."]**

> The key move: **count frequencies, then keep a size-k min-heap of `(freq, element)`; when it overflows, evict the lowest frequency.** What survives is your top k.

---

## 7. CODE IT — LIVE & CHUNKED — `4:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1.]**

> `Counter` does the forced counting pass in one line.

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)                       # O(n)
    heap = []                                   # min-heap of (freq, element)
```

> **[VISUAL: chunk 2, highlight the tuple `(freq, element)`.]** Push each distinct element keyed on its frequency; trim to size k.

```python
    for element, freq in count.items():
        heapq.heappush(heap, (freq, element))
        if len(heap) > k:                       # keep only k most frequent
            heapq.heappop(heap)                 # evict lowest frequency
```

> **[VISUAL: chunk 3.]** Whatever's left in the heap is the answer — strip off the elements.

```python
    return [element for freq, element in heap]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> Walk the *why*.
>
> `(freq, element)` — order matters inside the tuple. Frequency comes *first* so the heap sorts by count. Put the element first and you'd be ranking by value — a silent bug that passes the tiny example and fails the real one.
>
> `if len(heap) > k: heappop` — same push-then-trim as Kth Largest, evicting the least-frequent survivor.
>
> **LEARNER:** The final result comes out of the heap in some scrambled order — `[2, 1]` maybe, not `[1, 2]`. Isn't that wrong?
>
> **TEACHER:** Read the problem line: *"answer may be returned in any order."* So heap order is fine. If they *did* want it sorted by frequency, you'd pop the heap k times into a list and reverse — but here, don't waste the work.

---

## 9. DRY-RUN THE CODE — `6:30`
*(worked example — prove it, close the loop)*

**[VISUAL: `[1,1,1,2,2,3]`, k=2; count map, then the heap triangle updating.]**

> Run it, k = 2. `count = {1:3, 2:2, 3:1}`.

| push | heap (by freq) | size > 2? pop |
|---|---|---|
| (3,1) | [(3,1)] | no |
| (2,2) | [(2,2),(3,1)] | no |
| (1,3) | [(1,3),(3,1),(2,2)] | yes → pop (1,3) |

> Heap ends `[(2,2),(3,1)]`. Strip elements → `[2, 1]` → **`[1, 2]`** (any order). ✅ Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:30`
*(transfer to interview)*

**[VISUAL: "Sort: O(n log n). Heap: O(n + m log k). Buckets: O(n)."]**

> Out loud: *"Counting is O(n), forced. The size-k heap over m distinct elements is O(m log k), so O(n + m log k) total — under the O(n log n) wall. If they want strictly linear, I'd bucket sort: O(n)."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:00`
*(depth + honesty — the O(n) bucket trick)*

**[VISUAL: an array of buckets indexed by frequency; elements dropping into bucket[freq]; a scan from the high end collecting k.]**

> Space is dominated by the count map — O(m distinct elements), unavoidable. But we can drop the `log k` from *time* entirely with a beautiful trick: **bucket sort.**
>
> The insight: a frequency is an integer between 1 and n. Bounded. So instead of *comparing* frequencies, *index* by them — make n+1 buckets, drop each element into `bucket[its frequency]`, then walk buckets from high to low collecting until you have k.

```python
from collections import Counter

def top_k_frequent_buckets(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
    for element, freq in count.items():
        buckets[freq].append(element)

    result = []
    for freq in range(len(nums), 0, -1):           # high frequency → low
        for element in buckets[freq]:
            result.append(element)
            if len(result) == k:
                return result
    return result
```

> No comparisons, no log factor → **O(n) time, O(n) space.** The trade-off to voice: **heap = O(n log k) time, O(k) auxiliary; buckets = O(n) time but O(n) buckets.** When k is tiny the heap's memory edge matters; when you want guaranteed linear time, buckets win — and here the problem's "beat O(n log n)" hint is practically *asking* for buckets.

---

## 12. YOUR TURN (active recall) — `9:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Top K Frequent Words (LC 692)". A blank editor.]**

> Before the next video, try **Top K Frequent Words.** Same count-then-top-k skeleton, with one wrinkle: ties break *lexicographically*. That forces you to think carefully about heap direction — when two words tie on frequency, which one should the min-heap consider "weaker" and evict? Ten minutes; it's a great tie-breaking workout.

---

## 13. LOCK IT IN — `9:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Count is forced** — then it's "top k by a score."
> 2. **Size-k min-heap keyed on frequency** → O(n + m log k). Put frequency first in the tuple.
> 3. **Bounded integer score → bucket sort** kills the log → O(n).
>
> The peg: **top K by a score → heap; when the score is a small bounded int → buckets.**

---

## 14. CLIFFHANGER — `10:15`
*(open loop to next lesson)*

**[VISUAL: scattered 2D points around an origin dot. A circle of the k nearest glows. A blurred title: "K Closest Points to Origin".]**

> Frequency was one number per element. But what if the "score" is something you have to *compute geometrically* — like the distance of a point from the origin — and you want the k *closest*? Now you want the k *smallest* scores, which flips the heap upside down into a max-heap. And there's a sneaky "never take the square root" detail. That's next: K Closest Points to Origin. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.*;

public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> count = new HashMap<>();
    for (int n : nums) count.merge(n, 1, Integer::sum);

    // min-heap by frequency
    PriorityQueue<int[]> heap =
        new PriorityQueue<>((a, b) -> a[1] - b[1]);   // [element, freq]
    for (Map.Entry<Integer, Integer> e : count.entrySet()) {
        heap.offer(new int[]{e.getKey(), e.getValue()});
        if (heap.size() > k) heap.poll();
    }

    int[] result = new int[k];
    for (int i = 0; i < k; i++) result[i] = heap.poll()[0];
    return result;
}
```
