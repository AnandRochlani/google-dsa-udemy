# Daily Temperatures

> **LeetCode:** 739. Daily Temperatures · **Difficulty:** 🟡 Medium · **Pattern:** Stacks · **Google frequency:** ⭐ high

---

## Problem

Given an array `temperatures` where `temperatures[i]` is the temperature on day `i`, return an array `answer` such that `answer[i]` is the **number of days you must wait** after day `i` to get a **warmer** temperature. If no future day is warmer, `answer[i] = 0`.

**Example:** `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]` → `[1, 1, 4, 2, 1, 1, 0, 0]`.
- Day 0 (73): day 1 is 74 → wait `1`.
- Day 2 (75): the next warmer day is day 6 (76) → wait `6 − 2 = 4`.
- Day 6 (76): nothing warmer after → `0`.

**Constraints that matter:** `1 ≤ n ≤ 10⁵`, so an O(n²) double loop (~10¹⁰ ops) times out. Temperatures are in `[30, 100]` — a small fixed range, which even opens a niche alternate approach. This is "next greater element" reframed as a **distance**, so we store **indices** on the stack rather than values.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** for each day, scan forward until you find a warmer day, and record how many steps that took. Direct, obvious, and O(n²).
- **Where it hurts:** on a long cold stretch, every day re-scans almost the entire rest of the array looking for warmth. Days that turn out to have *no* warmer future day cost a full scan each. You keep re-walking the same future over and over.
- **The leap:** turn it around and process left to right, holding a stack of **days that are still waiting for a warmer day**. Keep that stack **monotonically decreasing in temperature** (a *monotonic stack* = one whose values only ever increase, or only ever decrease, from bottom to top). When today's temperature arrives, it **resolves** every waiting day on top of the stack that was colder than today: for each, the wait is `today's index − that day's index`. Pop them, then push today (it's now the newest day waiting for warmth).
- **Why indices, not values:** the answer is a *distance in days*, so each stack entry must remember **which day** it was — you subtract indices to get the wait. (Store the index; look up the temperature via the array when comparing.)
- **Pattern trigger:** **"for each element, how far until the next greater one"** → **monotonic decreasing stack of indices**. It's Next Greater Element with the answer expressed as a gap.

---

## ① Brute Force

For each day, walk forward to the first warmer day.

```python
def daily_temperatures_brute(temperatures):
    n = len(temperatures)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i
                break
    return answer
```

**Why it's the natural first attempt:** it's a word-for-word encoding of "count days until it gets warmer."

**Why it's not enough:** worst case (temperatures strictly decreasing, e.g. `[100, 99, 98, …]`) every inner loop runs to the end → **O(n²)**. At n = 10⁵ that's ~10¹⁰ comparisons → **Time Limit Exceeded**.

**Complexity:** Time `O(n²)`, Space `O(1)` extra (ignoring the output).

---

## ② Optimised Solution

One pass with a monotonic decreasing stack of **indices**.

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []                       # indices, temps decreasing bottom -> top

    for i, temp in enumerate(temperatures):
        # today resolves every colder waiting day on top of the stack
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            answer[prev] = i - prev  # distance in days
        stack.append(i)

    # indices left on the stack never saw a warmer day -> stay 0
    return answer
```

**Walk `[73, 74, 75, 71, 69, 72, 76, 73]`** (stack holds indices; temps shown for clarity):

| i | temp | pops → assign | stack (indices) after | answer so far |
|---|---|---|---|---|
| 0 | 73 | — | `[0]` | `[0,0,0,0,0,0,0,0]` |
| 1 | 74 | pop 0 (73<74) → `ans[0]=1` | `[1]` | `[1,0,…]` |
| 2 | 75 | pop 1 (74<75) → `ans[1]=1` | `[2]` | `[1,1,…]` |
| 3 | 71 | — (71<75) | `[2,3]` | unchanged |
| 4 | 69 | — (69<71) | `[2,3,4]` | unchanged |
| 5 | 72 | pop 4 →`ans[4]=1`, pop 3 →`ans[3]=2` (72<75 stop) | `[2,5]` | `[1,1,0,2,1,0,0,0]` |
| 6 | 76 | pop 5 →`ans[5]=1`, pop 2 →`ans[2]=4` | `[6]` | `[1,1,4,2,1,1,0,0]` |
| 7 | 73 | — (73<76) | `[6,7]` | unchanged |

Leftover indices `6` and `7` never got resolved → stay `0`. Final: `[1, 1, 4, 2, 1, 1, 0, 0]`. ✅

**Why it's correct:** the stack always holds, top-down, the still-unresolved days in increasing-toward-the-bottom temperature order. When day `i` is warmer than the top day `p`, day `i` is the *first* warmer day after `p` — anything between them was colder than `p` (or it would have popped `p` already), so `i − p` is exactly the wait. Each index is pushed once and popped at most once.

**Complexity:** Time `O(n)` — amortized, since total pushes + pops ≤ 2n. Space `O(n)` for the stack (worst case a strictly decreasing array puts every index on it).

---

## ③ Space Optimization

The stack is O(n) and, for the general monotonic-stack solution, that's **inherent** — a strictly decreasing temperature array forces all n indices onto the stack at once because none get resolved until the very end.

But this problem has a special structure worth naming: **temperatures are bounded to `[30, 100]`** — only 71 distinct values. That enables an O(1)-*extra*-space variant (beyond the output) that scans **right to left**, remembering, for each possible temperature, the nearest warmer day seen so far:

```python
def daily_temperatures_bounded(temperatures):
    n = len(temperatures)
    answer = [0] * n
    hottest = 0                      # highest temperature seen to the right

    for i in range(n - 1, -1, -1):
        if temperatures[i] >= hottest:
            hottest = temperatures[i]
            continue                 # nothing to the right is warmer
        # step forward day by day; bounded range keeps this near-constant work
        days = 1
        while temperatures[i + days] <= temperatures[i]:
            days += answer[i + days] # jump using already-computed answers
        answer[i] = days
    return answer
```

Because we **jump ahead using answers already computed** (skipping over runs that can't help), and the value range is tiny, the total work stays O(n) while the *only* real extra memory is the `hottest` scalar. This is the honest "can we beat O(n) space?" answer: **yes, via the jump trick / bounded range — the explicit stack isn't strictly required, though the plain stack version is what you'd write first and is perfectly acceptable.**

> Interview-honest verdict: *"The stack is O(n) and inherent for the general problem. But temperatures are bounded to 71 values, so I can scan right-to-left and jump using answers I've already filled in — O(n) time with O(1) extra space beyond the output."*

**Complexity:** stack version — Time `O(n)`, Space `O(n)`; jump version — Time `O(n)`, Space `O(1)` extra.

---

## Java (for Java interviewers)

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();     // indices, temps decreasing

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {
            int prev = stack.pop();
            answer[prev] = i - prev;
        }
        stack.push(i);
    }
    return answer;    // unresolved indices already 0
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Optimised (monotonic stack of indices) | O(n) | O(n) |
| Right-to-left jump (bounded range) | O(n) | O(1) extra |

---

## Say it out loud (interview narration)

> *"Brute force scans forward from each day — O(n²), which dies at 10⁵ on a decreasing array. Instead I keep a monotonic decreasing stack of day indices that are still waiting for a warmer day. When today is warmer than the day on top, today resolves it: the wait is today's index minus that day's index, so I store indices, not temperatures. I pop every colder waiting day, then push today. Each index is pushed and popped once, so it's O(n) time and O(n) stack space — and the stack is inherent for the general case. As a bonus, since temperatures only span 30 to 100, I can scan right-to-left and jump over runs using answers I've already computed, getting O(1) extra space."*

## Related / follow-ups
- **Next Greater Element I / II** (LC 496 / 503) — same stack, values instead of distances; II is circular
- **Online Stock Span** (LC 901) — monotonic stack counting *backwards*
- **Largest Rectangle in Histogram** (LC 84) — monotonic stack, both directions
- **Trapping Rain Water** (LC 42) — monotonic stack of decreasing bars
- **Sum of Subarray Minimums** (LC 907) — monotonic stack over subarray boundaries
