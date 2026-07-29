# 🎬 Recording Script — Next Greater Element I
**Pattern: Stacks (Monotonic) · LeetCode 496 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the plain stack from Valid Parentheses & Min Stack — now we make it *decide*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. Two arrays: `nums2 = [1, 3, 4, 2]`. A pointer sits on a value and an arrow scans rightward, again and again, for each query.]**

> Google question: *"For each number, find the next number to its right that's bigger."*
>
> You write the natural thing — for each value, walk right until you hit something larger. It works. But watch your arrow.
>
> **[VISUAL: the rightward arrow re-scanning the same tail of the array over and over, a "re-scans" counter climbing.]**
>
> For every query, you re-walk the same tail of the array. Over and over. It's O(n·m), and on a big input it crawls. Here's the twist: you can compute *every* answer in a single left-to-right pass — using a stack that pops a whole run of elements the moment a bigger one shows up. By the end of this video that "pops a whole run at once" idea will click. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: `nums1 = [4, 1, 2]` above, `nums2 = [1, 3, 4, 2]` below. Answer slots `[ ?, ?, ? ]`.]**

> The problem in one line: **for each value in `nums1`, find its next greater element to the right inside `nums2`.** If there's none, the answer is `-1`.
>
> `nums1` is just a subset of `nums2`, and all values are distinct. Tiny example: for `4` — it sits in `nums2` at the end, nothing bigger to its right, so `-1`. For `1` — the first bigger thing to its right is `3`. For `2` — it's last, nothing to the right, `-1`.
>
> **[VISUAL: answer slots fill: `[-1, 3, -1]`.]**
>
> Answer: `[-1, 3, -1]`. Notice the real work is entirely about `nums2` — "next greater to the right" is a property of `nums2` alone. `nums1` is just which answers we read off.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — let them feel the waste)*

**[VISUAL: `nums2 = [1, 3, 4, 2]`. For each query, find it, then scan right.]**

> Let's do the brute force by hand. For `4`: find it in `nums2` — index 2 — then scan right: only `2` is left, not bigger, so `-1`. For `1`: find it — index 0 — scan right, `3` is bigger, stop, answer `3`. For `2`: index 3, scan right, nothing, `-1`.
>
> **[VISUAL: a "work" counter ticking; the same tail elements getting re-visited by different queries.]**
>
> It's correct. But feel it: finding each value is a scan, *and* the rightward hunt is another scan — repeated for every query. Same elements, re-examined again and again. O(n·m). We're recomputing a fact about `nums2` that never changes.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the repeated re-scanning of `nums2`'s tail. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is clear: "next greater to the right" is fixed for `nums2`, but we recompute it per query, re-walking the same tail.
>
> **LEARNER:** Okay — but the numbers are in random order. To know what's the *next bigger* one, don't I just have to look ahead every time? What could I precompute?
>
> **TEACHER:** That's the instinct to flip. Here's the reframe — pause and sit with it: as I sweep left to right, some elements are **still waiting** for a bigger neighbor. **When a new, big value arrives, which of the waiting elements does it answer — and can it answer several at once?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a stack column labeled "waiting for a bigger neighbor". Sweep `nums2 = [1, 3, 4, 2]` left to right.]**

> Here's the move. Sweep `nums2` left to right, and keep a stack of the elements that are **still waiting** for their next-greater. Watch what a big incoming value does.
>
> **[VISUAL: `1` arrives → push. Column: `[1]`.]**
>
> See `1`. Nobody's waiting yet. It's now waiting. Push it.
>
> **[VISUAL: `3` arrives. It's bigger than top `1`. The `1` tile lights up — "found it! next greater of 1 is 3" — pops off. Then push 3. Column: `[3]`.]**
>
> See `3`. Look at the top — `1`. Is `3` bigger? Yes! So `3` is the next-greater *for* `1`. Record `1 → 3`, pop the `1`. Now push `3` — it starts waiting for *its* bigger neighbor.
>
> **[VISUAL: `4` arrives. Bigger than top `3` → pop 3, record `3→4`. Push 4. Column: `[4]`.]**
>
> See `4`. Top is `3`, `4` is bigger — record `3 → 4`, pop. Push `4`.
>
> **[VISUAL: `2` arrives. Smaller than top `4`. No pop. Push. Column: `[4, 2]`.]**
>
> See `2`. Top is `4`, `2` is *not* bigger. So `2` doesn't answer anyone. It just joins the line — push. Column is `[4, 2]`, and notice: from bottom to top it's **decreasing**, 4 then 2.
>
> That decreasing property has a name. A **monotonic stack** is a stack we deliberately keep in sorted order — values only ever increasing, or only ever decreasing, from bottom to top. Here we keep it decreasing. And that's exactly what lets one big incoming value clear a whole *run* of smaller waiting elements in one shot — because they're stacked smallest-on-top.
>
> **[VISUAL: leftovers 4 and 2 in the column → both stamped "-1", no bigger neighbor ever came.]**
>
> Whatever's still on the stack at the end never found a bigger neighbor — they all get `-1`.

---

## 6. THE KEY MOVE (signaling) — `4:55`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Keep a decreasing stack. New value pops everything smaller — it's their next-greater."]**

> Burn this in: **keep a decreasing stack of the waiting elements; when a new value arrives, it's the next-greater for everything smaller on top — pop them all and record it.**
>
> That's the monotonic-stack pattern, and you'll reuse it constantly: "for each element, find the next larger or smaller one to a side" → monotonic stack.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. A map from value to its answer, and the stack.

```python
def next_greater(nums1, nums2):
    next_greater_of = {}          # value -> its next greater element
    stack = []                    # monotonic decreasing (bottom -> top)
```

> **[VISUAL: add chunk 2, highlight it. The stack column on the right.]** The one-pass sweep — the whole engine.

```python
    for cur in nums2:
        # cur is the next greater for everything smaller on the stack
        while stack and stack[-1] < cur:
            next_greater_of[stack.pop()] = cur
        stack.append(cur)
```

> **[VISUAL: add chunk 3.]** Leftovers get `-1`, then read off `nums1`.

```python
    for leftover in stack:
        next_greater_of[leftover] = -1

    return [next_greater_of[x] for x in nums1]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:35`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as named.]**

> Let's walk the *why*.
>
> The `while stack and stack[-1] < cur` is the monotonic move. As long as the top is smaller than `cur`, `cur` is its next-greater — record it and pop. This is a `while`, not an `if`, because one big value can resolve a *whole run* of smaller waiting elements.
>
> `stack.append(cur)` — after clearing everyone smaller, `cur` joins as the newest waiter. This is what keeps the stack decreasing: `cur` is now the largest near the top.
>
> The leftover loop: anything never popped never met a bigger neighbor → `-1`.
>
> We key the map by *value*, which is only safe because the values are distinct. Then each `nums1` lookup is O(1).
>
> **LEARNER:** Quick one — `stack[-1] < cur`, strict less-than. Since values are distinct here, does `<` versus `<=` even matter?
>
> **TEACHER:** Sharp — and for *this* problem, no, distinct values mean they're never equal, so it can't differ. But the choice is a real fork in sibling problems. When duplicates are allowed, `<` versus `<=` decides whether an equal element counts as "greater" — and that flips answers. Worth noticing now so it doesn't bite you in the histogram problem later, where it genuinely matters.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: `nums2 = [1, 3, 4, 2]`; the stack column growing/shrinking; a trace table filling row by row.]**

> Let's run the real code on `nums2 = [1, 3, 4, 2]`.

| cur | pops → assign | stack after | map so far |
|---|---|---|---|
| 1 | none | `[1]` | `{}` |
| 3 | 3>1 → pop 1, `1→3` | `[3]` | `{1:3}` |
| 4 | 4>3 → pop 3, `3→4` | `[4]` | `{1:3, 3:4}` |
| 2 | 2<4, no pop | `[4, 2]` | `{1:3, 3:4}` |

> Leftovers `4` and `2` → `4:-1`, `2:-1`. Final map `{1:3, 3:4, 4:-1, 2:-1}`. Read `nums1 = [4, 1, 2]` → `[-1, 3, -1]`. Loop closed — every answer computed in **one** pass over `nums2`, no re-scanning.

---

## 10. COMPLEXITY, OUT LOUD — `8:35`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n·m). Ours: O(n + m) time, O(m) space.]**

> Say it in the room: *"Brute force is O(n·m) — it re-scans nums2's tail for every query. The monotonic stack computes all of nums2's answers in one pass: every element is pushed once and popped at most once, so that's O(m). Each nums1 lookup is O(1). Total O(n + m) time, O(m) space for the map and stack."*
>
> "Pushed once, popped once" is the phrase that proves the linear bound — say it explicitly.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:15`
*(depth + honesty)*

**[VISUAL: a strictly decreasing nums2 `[5,4,3,2,1]`; every tile stacks up, tall column.]**

> Can we cut the O(m)? Here it's a genuine time–space tradeoff, and being honest about it is the point.
>
> Keep the map — O(m) space — and you get O(n + m) time, the best. Drop the map and rescan `nums2` per query — O(1) extra space, but you're back to O(n·m) time. For this problem the map is worth it.
>
> And the stack itself is O(m) worst case: a strictly decreasing `nums2` never pops until the end, so every element sits there at once. That's inherent — those elements genuinely all need remembering simultaneously.

---

## 12. YOUR TURN (active recall) — `9:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Next Greater Element II (LC 503)". A circular array wrapping around.]**

> Before the next video, try **Next Greater Element II**, LC 503. Same monotonic stack — but the array is *circular*, so the next-greater can wrap around past the end. The trick: iterate the array twice using modulo. Same engine, one clever twist.
>
> Ten minutes of struggle before you peek. That's the part that sticks.

---

## 13. LOCK IT IN — `10:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **"Next greater/smaller to a side"** is the trigger → **monotonic stack.**
> 2. **A monotonic stack** stays sorted; a new value **pops everything it beats** — that's the `while`.
> 3. **Leftovers get the default** (`-1` here) — they never met their match.
>
> And the peg: **we pop while the new element beats the top.** Picture a big kid walking in and clearing out everyone shorter waiting in line — all at once.

---

## 14. CLIFFHANGER — `10:40`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Daily Temperatures". A row of temperatures with day-numbers underneath.]**

> Same exact stack — but now the interviewer doesn't want the next bigger *value*. They want *how many days until it's warmer*. A distance. Suddenly you can't store values on the stack anymore — you have to store something else, or the math breaks. That's next: Daily Temperatures. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
    while (!stack.isEmpty()) nextGreater.put(stack.pop(), -1);

    int[] res = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        res[i] = nextGreater.get(nums1[i]);
    }
    return res;
}
```
