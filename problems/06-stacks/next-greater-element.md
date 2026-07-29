# Next Greater Element I

> **LeetCode:** 496. Next Greater Element I · **Difficulty:** 🟡 Medium · **Pattern:** Stacks · **Google frequency:** medium

---

## Problem

You're given two arrays, `nums1` and `nums2`, where **`nums1` is a subset of `nums2`** and all values are distinct. For each value `x` in `nums1`, find its **next greater element** in `nums2`: standing at `x`'s position in `nums2`, the first element to its **right** that is strictly greater than `x`. If there is none, the answer is `-1`. Return the answers in the order of `nums1`.

**Example:** `nums1 = [4, 1, 2]`, `nums2 = [1, 3, 4, 2]` → `[-1, 3, -1]`.
- `4` is in `nums2` at index 2; nothing to its right is bigger → `-1`.
- `1` is at index 0; the first bigger element to the right is `3` → `3`.
- `2` is at index 3; nothing to its right → `-1`.

**Constraints that matter:** arrays are small here (`≤ 1000`), so even O(n·m) passes, but the intended lesson is the **monotonic-stack** technique that scales to O(n). All elements are **distinct**, which lets us key answers by value in a hash map.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** for each `x`, find it in `nums2`, then scan rightward until you see something bigger. Simple, and it directly encodes the definition. But it re-scans `nums2` for every query — O(n·m).
- **Where it hurts:** you keep re-walking the tail of `nums2` over and over. Every element gets looked at by many different queries. The "next greater to the right" relationship is a property of `nums2` alone — you should be able to compute it **once, in a single pass**, and just look answers up.
- **The leap:** sweep `nums2` left to right, holding a **stack of elements that are still waiting for their next-greater**. Keep that stack **monotonic decreasing** (each value smaller than the one below it). When a new element `cur` arrives, it is the "next greater" for **every stack element smaller than it** — so pop them all and record `cur` as their answer. Then push `cur` (it's now waiting for *its* next greater). A *monotonic stack* is one whose values are kept strictly increasing or strictly decreasing as you go from bottom to top; here we keep it decreasing.
- **Why a stack:** the elements still waiting are always the ones we've seen most recently and haven't yet "resolved" — and the newest small one gets resolved first. That's LIFO. And because they're in decreasing order, one incoming `cur` can clear a whole run of them cheaply.
- **Pattern trigger:** **"for each element, find the next larger/smaller one to a side"** → **monotonic stack**. Store answers in a **hash map** keyed by value (safe because values are distinct), then read off `nums1` in O(1) each.

---

## ① Brute Force

For each element of `nums1`, locate it in `nums2` and linearly scan right for the first bigger value.

```python
def next_greater_brute(nums1, nums2):
    res = []
    for x in nums1:
        j = nums2.index(x)          # find x in nums2
        nxt = -1
        for k in range(j + 1, len(nums2)):
            if nums2[k] > x:
                nxt = nums2[k]
                break
        res.append(nxt)
    return res
```

**Why it's the natural first attempt:** it's a literal transcription of the problem statement.

**Why it's not enough:** `nums2.index(x)` is itself O(m), and the inner scan is another O(m), repeated for all of `nums1` → **O(n·m)**. It repeatedly re-examines the same tail of `nums2`. Fine for n,m ≤ 1000, but it doesn't teach the scalable idea.

**Complexity:** Time `O(n · m)`, Space `O(n)` for the output.

---

## ② Optimised Solution

One monotonic-decreasing-stack pass over `nums2` builds a `value → next greater` map; then read off `nums1`.

```python
def next_greater(nums1, nums2):
    next_greater_of = {}          # value -> its next greater element
    stack = []                    # monotonic decreasing (bottom -> top)

    for cur in nums2:
        # cur is the next greater element for everything smaller on the stack
        while stack and stack[-1] < cur:
            next_greater_of[stack.pop()] = cur
        stack.append(cur)

    # anything still on the stack has no greater element to its right
    for leftover in stack:
        next_greater_of[leftover] = -1

    return [next_greater_of[x] for x in nums1]
```

**Walk `nums2 = [1, 3, 4, 2]`** (stack bottom → top):

| cur | pops (assign next greater) | stack after | map so far |
|---|---|---|---|
| 1 | none | `[1]` | `{}` |
| 3 | 3 > 1 → pop 1, map `1→3` | `[3]` | `{1:3}` |
| 4 | 4 > 3 → pop 3, map `3→4` | `[4]` | `{1:3, 3:4}` |
| 2 | 2 < 4, no pop | `[4, 2]` | `{1:3, 3:4}` |

Leftovers `4` and `2` never found a greater element → `4:-1`, `2:-1`. Final map `{1:3, 3:4, 4:-1, 2:-1}`. Reading `nums1 = [4, 1, 2]` gives `[-1, 3, -1]`. ✅

**Why it's correct:** the stack always holds, top-to-bottom, the not-yet-resolved elements in increasing-toward-the-bottom (decreasing top-down) order. When `cur` exceeds the top, `cur` is genuinely the *first* element to the right that's bigger than that top (nothing between them was bigger, or it would have popped the top earlier). Each element is pushed once and popped at most once.

**Complexity:** Time `O(n + m)` — every element of `nums2` enters and leaves the stack once, and each `nums1` lookup is O(1). Space `O(m)` for the map and stack.

---

## ③ Space Optimization

The **O(m) hash map + O(m) stack is inherent** to the one-pass approach: to answer `nums1` queries out of order in O(1), you must precompute and store every element's next-greater. You can't shrink that below O(m) without giving up either the single pass or the O(1) lookups.

```python
# The stack + map ARE the space cost of getting O(n+m) time.
# Trading it away means going back toward the O(n·m) brute force.
```

Honest tradeoff to state:

- **Keep the map (O(m) space)** → O(n + m) time. Best time.
- **Drop the map**, scan `nums2` fresh for each query → O(1) extra space but O(n·m) time. Worse time.

That's a classic **time–space tradeoff**, and for this problem the map is worth it. The stack itself is O(m) worst case (a strictly decreasing `nums2` never pops until the end) and that too is inherent — those elements genuinely all need to be remembered simultaneously.

**Complexity:** Time `O(n + m)`, Space `O(m)`.

---

## Java (for Java interviewers)

```java
public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> nextGreater = new HashMap<>();
    Deque<Integer> stack = new ArrayDeque<>();      // monotonic decreasing

    for (int cur : nums2) {
        while (!stack.isEmpty() && stack.peek() < cur) {
            nextGreater.put(stack.pop(), cur);
        }
        stack.push(cur);
    }
    // leftovers have no next greater element
    while (!stack.isEmpty()) nextGreater.put(stack.pop(), -1);

    int[] res = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        res[i] = nextGreater.get(nums1[i]);
    }
    return res;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (scan per query) | O(n · m) | O(n) |
| Optimised (monotonic stack + map) | O(n + m) | O(m) |
| Space-min (drop map, rescan) | O(n · m) | O(1) extra |

---

## Say it out loud (interview narration)

> *"Brute force finds each value in nums2 and scans right — O(n·m), and it re-walks the same tail repeatedly. Instead I compute next-greater for the whole of nums2 in one pass with a monotonic decreasing stack: I hold elements still waiting for a bigger neighbor, and when a new value comes in, it's the answer for every smaller element on top of the stack, so I pop and record them in a hash map keyed by value — safe since values are distinct. Whatever's left on the stack gets -1. Then each nums1 query is an O(1) map lookup. That's O(n+m) time; the map and stack are O(m) and that storage is inherent to getting the single-pass speed."*

## Related / follow-ups
- **Next Greater Element II** (LC 503) — circular array; iterate the array twice (mod n)
- **Daily Temperatures** (LC 739) — same monotonic stack, storing **indices** to get distances
- **Next Greater Element III** (LC 556) — next-greater *permutation* of a number
- **Largest Rectangle in Histogram** (LC 84) — monotonic stack, the harder sibling
- **Trapping Rain Water** (LC 42) — monotonic stack alternative to two pointers
