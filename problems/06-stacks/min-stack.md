# Min Stack

> **LeetCode:** 155. Min Stack · **Difficulty:** 🟡 Medium · **Pattern:** Stacks · **Google frequency:** ⭐ high

---

## Problem

Design a stack that supports `push`, `pop`, `top`, and **`getMin`** — retrieving the minimum element currently in the stack — where **every operation runs in O(1)** time.

**Example:**
```
push(-2); push(0); push(-3);
getMin();  -> -3      # min of {-2, 0, -3}
pop();                # removes -3
top();     -> 0
getMin();  -> -2      # min of {-2, 0}
```

**Constraints that matter:** the whole challenge is the phrase **"O(1) `getMin`"**. A plain stack gives O(1) push/pop/top for free; the min is the twist. Also note `pop`/`top`/`getMin` are only called on a non-empty stack, and values fit in a signed 32-bit int (`-2³¹ … 2³¹-1`).

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Keep the values in a normal stack; for `getMin`, just scan all of them and return the smallest." Correct, but `getMin` is O(n) — and the problem explicitly demands O(1).
- **Next instinct:** "Cache the minimum in a single variable, updated on push." That works for `push`... until you `pop` the current minimum. Now the cached min is wrong and you have no record of the *previous* minimum. A single variable can't recover history.
- **Where it hurts:** The min isn't one number — it's a number **per stack depth**. When you pop back to depth 2, you need the min *as it was* at depth 2. That's a value that changes as the stack grows and shrinks, and must be restored on the way back down.
- **The leap:** Keep a **second stack that tracks the minimum in lockstep** with the main stack. Every time you push a value, also push "the smallest value seen so far up to this point" onto the min-stack. Now the min-stack's top is *always* the current minimum, and popping both stacks together automatically restores the previous min. `getMin` is just "peek the min-stack" — O(1).
- **Pattern trigger:** **"I need an auxiliary quantity that must stay consistent with a stack's push/pop history"** → **carry the extra info alongside each element** (a parallel stack, or a `(value, running_min)` pair per slot). The min is bookkeeping attached to stack depth.

---

## ① Brute Force

Store values in one stack; compute the min by scanning on each `getMin`.

```python
class MinStackBrute:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return min(self.stack)      # O(n) scan every call
```

**Why it's the natural first attempt:** it's the minimal amount of code, and `min()` is right there.

**Why it's not enough:** `getMin` is **O(n)**. If an interviewer calls `getMin` after every push (a common access pattern), the whole sequence degrades to O(n²). The spec asked for O(1) — this fails the bar.

**Complexity:** push/pop/top `O(1)`, **getMin `O(n)`**. Space `O(n)`.

---

## ② Optimised Solution

Keep a parallel **min-stack**: `min_stack[i]` holds the minimum of the main stack's first `i+1` elements.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []          # running minimum, in lockstep

    def push(self, val):
        self.stack.append(val)
        # new running min = smaller of val and the previous running min
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()         # pop both together

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]    # O(1): current min is always on top
```

**Walk the example** `push(-2), push(0), push(-3), getMin, pop, top, getMin` (tops on the right):

| op | `stack` | `min_stack` | returns |
|---|---|---|---|
| push(-2) | `[-2]` | `[-2]` | |
| push(0) | `[-2, 0]` | `[-2, -2]` | *(min(0, -2) = -2)* |
| push(-3) | `[-2, 0, -3]` | `[-2, -2, -3]` | *(min(-3, -2) = -3)* |
| getMin | | | **-3** (top of min_stack) |
| pop | `[-2, 0]` | `[-2, -2]` | |
| top | | | **0** |
| getMin | | | **-2** (min restored automatically) |

The key moment is the last `getMin`: popping `-3` also popped its min-stack entry, so the top is `-2` again — the previous minimum reappears **for free**, no rescanning.

**Why it's correct:** invariant — after any sequence of ops, `min_stack[-1]` equals `min(stack)`. It holds on push (new min is `min(val, old_min)`) and on pop (removing the top of both stacks returns min_stack to exactly the state it had at that depth before). All four operations are constant-time array ops.

**Complexity:** all operations `O(1)`. Space `O(n)`.

---

## ③ Space Optimization

The min-stack **doubles the memory** to 2 · n slots. Two ways to trim it — this is the tradeoff worth discussing out loud.

**Option A — store `(value, running_min)` pairs in one stack.** Same total storage, but a single structure instead of two — cleaner, no risk of the stacks desyncing:

```python
class MinStackPairs:
    def __init__(self):
        self.stack = []                     # list of (val, current_min)

    def push(self, val):
        cur_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, cur_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]
```

This is still 2n numbers of storage — it's a readability win, not a space win.

**Option B — only push to the min-stack when a value ties-or-beats the current min.** Now the min-stack holds *fewer* entries (just the "record-breakers"), so it can be much smaller in practice:

```python
class MinStackLean:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:   # <= handles duplicate mins
            self.min_stack.append(val)

    def pop(self):
        x = self.stack.pop()
        if x == self.min_stack[-1]:        # only pop the min-stack if we removed the min
            self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
```

The `<=` (not `<`) is the subtle correctness point: with duplicate minimums, you must push each copy, or popping one will prematurely expose a wrong min. Worst case (a strictly decreasing input) this still stores 2n, but on typical data it's leaner.

> Honest verdict: **you cannot get below O(n)** total — you must retain every value to serve arbitrary pops. Option A trades two stacks for one clean structure; Option B trades a little bookkeeping for fewer min entries on average. In an interview, *offer* Option B as the space-conscious variant and call out the `<=` duplicate trap.

**Complexity:** all ops `O(1)`; space `O(n)` (Option B often `< 2n` in practice, `O(n)` worst case).

---

## Java (for Java interviewers)

```java
class MinStack {
    private Deque<Integer> stack = new ArrayDeque<>();
    private Deque<Integer> minStack = new ArrayDeque<>();

    public void push(int val) {
        stack.push(val);
        if (minStack.isEmpty()) minStack.push(val);
        else minStack.push(Math.min(val, minStack.peek()));
    }

    public void pop()      { stack.pop(); minStack.pop(); }
    public int  top()      { return stack.peek(); }
    public int  getMin()   { return minStack.peek(); }
}
```

---

## Complexity Summary

| Approach | push | pop | top | getMin | Space |
|---|---|---|---|---|---|
| Brute (scan for min) | O(1) | O(1) | O(1) | **O(n)** | O(n) |
| Two stacks / pairs | O(1) | O(1) | O(1) | **O(1)** | O(n) (~2n) |
| Lean min-stack (Option B) | O(1) | O(1) | O(1) | **O(1)** | O(n) (≤ 2n) |

---

## Say it out loud (interview narration)

> *"A plain stack makes push, pop, and top O(1), but getMin would be an O(n) scan. A single cached-min variable breaks the moment I pop the current minimum — I lose the previous one. The fix is a parallel min-stack that records the running minimum at each depth: on push I store min(val, previous min), and on pop I pop both stacks so the earlier minimum is restored automatically. getMin is just the top of the min-stack — O(1) everything. If space matters I can store (value, min) pairs in one stack, or only push record-breaking minimums, being careful to use `<=` so duplicate minimums are all recorded."*

## Related / follow-ups
- **Max Stack** (LC 716) — symmetric; getMax and a popMax that needs more than a stack
- **Sliding Window Maximum** (LC 239) — monotonic deque, the "min/max under mutation" cousin
- **Implement Queue using Stacks** (LC 232) / **Stack using Queues** (LC 225)
- **Valid Parentheses** (LC 20) — the plain-stack warm-up
