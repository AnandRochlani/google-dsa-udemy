# 🎬 Recording Script — Min Stack
**Pattern: Stacks · LeetCode 155 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the plain-stack warm-up from Valid Parentheses (previous lesson).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. A class skeleton `class MinStack:` with `push`, `pop`, `top`, `getMin`. A red badge on `getMin`: "O(1) required".]**

> Google design round. *"Build me a stack. Push, pop, top — the usual. But add one method: `getMin`. It returns the smallest element in the stack. And every single operation — including `getMin` — has to be O(1)."*
>
> You shrug. Easy. For `getMin`, just scan the stack and return the smallest. You write it. And the interviewer taps the screen: *"That scan is O(n). I said O(1)."*
>
> **[VISUAL: the `min(stack)` line highlighted red, an "O(n)" tag next to it.]**
>
> How can you know the minimum *instantly*, without ever looking through the stack — even as elements come and go? By the end of this video that'll feel obvious. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: a stack column. Three pushes animate in: -2, then 0 on top, then -3 on top.]**

> The whole problem in one line: **a stack where you can also ask for the minimum, in constant time, at any moment.**
>
> Tiny example. Push `-2`. Push `0`. Push `-3`. Now `getMin` should say `-3` — smallest of the three. Then `pop` — that removes `-3`, the top. Now `top` is `0`. And `getMin`… should say `-2`.
>
> **[VISUAL: -3 tile lifts off; the min answer flips from -3 back to -2.]**
>
> Freeze right there. The minimum just *changed* — from `-3` back to `-2` — because we removed an element. Hold that: the min isn't one fixed number. It moves as the stack grows and shrinks.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: a normal stack column. `getMin` is called; an arrow sweeps top-to-bottom over every tile, comparing.]**

> First honest idea: keep a plain stack, and for `getMin`, scan everything and return the smallest. Let's do it by hand.
>
> Stack is `[-2, 0, -3]`. Call `getMin` — sweep all three, smallest is `-3`. Correct! Call it again — sweep all three again. And again.
>
> **[VISUAL: a "comparisons" counter climbing each time getMin is called.]**
>
> It's *correct*, but watch: every `getMin` walks the whole stack. If the interviewer calls `getMin` after every push — a totally normal pattern — the whole sequence becomes O(n²). The spec said O(1). This fails the bar.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. A single variable `min = -3` appears, tempting. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So the obvious patch: cache the min in one variable. On each push, if the new value is smaller, update it. `getMin` just reads the variable — O(1). Done?
>
> **LEARNER:** Yeah, that's what I'd write. Keep a `min` variable, update it on push. Where's the catch?
>
> **TEACHER:** Here's the catch. Watch what happens when you `pop` the current minimum. Your cached min is `-3`. You pop `-3` off. Now the real min is `-2` — but your variable still says `-3`, and worse, *you have no record of what the previous minimum was.* One variable can't remember history.
>
> Pause the video. **The min isn't one number — it's a different number at every stack depth. How do you remember all of them, cheaply?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two stack columns side by side. Left labeled "stack", right labeled "min-stack". They rise and fall together, locked in step.]**

> Here's the leap. If the minimum changes with depth, then store *one minimum per depth*. Keep a **second stack** — a min-stack — that moves in lockstep with the main one.
>
> The rule: **every time you push a value, also push the smallest value seen so far** onto the min-stack. So each slot of the min-stack answers, "what's the minimum of everything up to this depth?"
>
> Think of two elevators wired together. Every floor the main one stops at, the min-elevator stops too — and its display always shows the smallest number so far. They never move independently.
>
> **[VISUAL: push -2 → both columns get a tile: stack `-2`, min-stack `-2`. Push 0 → stack `0`, min-stack `min(0,-2) = -2`. Push -3 → stack `-3`, min-stack `min(-3,-2) = -3`.]**
>
> Push `-2`: main gets `-2`, min-stack gets `-2`. Push `0`: main gets `0`, min-stack gets `min(0, -2)` which is still `-2`. Push `-3`: main gets `-3`, min-stack gets `min(-3, -2)` which is `-3`.
>
> Now the magic. The top of the min-stack is *always* the current minimum. `getMin` is just "peek the top of the min-stack." No scan.
>
> **[VISUAL: pop -3 → BOTH columns drop a tile. Min-stack top flips from -3 back to -2 automatically.]**
>
> And popping? Pop *both* stacks together. When `-3` leaves the main stack, its min-stack partner leaves too — and the min-stack top is `-2` again. The previous minimum reappears **for free.** That's the history the single variable couldn't keep.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Push value + running-min together. Pop both together. getMin = min-stack top."]**

> Here's the line to keep: **push the value and the running minimum together; pop both together; getMin is just the min-stack's top.**
>
> The whole trick is that the min-stack carries the answer at every depth, so restoring the old min costs nothing.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Two stacks in the constructor.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []          # running minimum, in lockstep
```

> **[VISUAL: add chunk 2, highlight it. Both columns on the right.]** Push: add to the main stack, and push the smaller of the new value and the current running min.

```python
    def push(self, val):
        self.stack.append(val)
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)
```

> **[VISUAL: add chunk 3.]** Pop: remove from *both* — that's the whole restore-the-old-min mechanism.

```python
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()         # pop both together
```

> **[VISUAL: add chunk 4.]** And the two O(1) reads.

```python
    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]    # current min is always on top
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full class; spotlight each method as named.]**

> Let's walk the *why*.
>
> In `push`, `min(val, self.min_stack[-1])` is the heart — the new running min is either the new value or the old running min, whichever is smaller. The `if self.min_stack` handles the very first push, when there's no previous min to compare against.
>
> In `pop`, popping *both* is what makes the old minimum come back. The min-stack returns to exactly the state it had at that depth before — no computation, just removal.
>
> `getMin` is a single array read. That's the O(1) the spec demanded.
>
> **LEARNER:** Wait — isn't storing a full copy of the min at *every* level wasteful? If I push a thousand things, I've got a thousand min entries, most of them duplicates.
>
> **TEACHER:** Totally fair — and you've just found the space cost: we've doubled the memory to 2n. That's the honest tradeoff, and there's a leaner version we'll get to in a second. But notice what those "duplicates" buy you: pop becomes a dumb, instant operation. No recomputation, no edge cases. Simplicity is worth memory here — and we'll show how to trim it when it matters.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: both columns; a trace table filling row by row. Tops on the right.]**

> Let's run the real sequence: push -2, push 0, push -3, getMin, pop, top, getMin.

| op | `stack` | `min_stack` | returns |
|---|---|---|---|
| push(-2) | `[-2]` | `[-2]` | |
| push(0) | `[-2, 0]` | `[-2, -2]` | *(min(0,-2)=-2)* |
| push(-3) | `[-2, 0, -3]` | `[-2, -2, -3]` | |
| getMin | | | **-3** |
| pop | `[-2, 0]` | `[-2, -2]` | |
| top | | | **0** |
| getMin | | | **-2** |

> The payoff is the last `getMin`. Popping `-3` also popped its min-stack entry, so the top is `-2` again — the previous minimum, restored with zero work. Loop from the cold open closed: instant min, no scanning, ever.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: table — Brute: getMin O(n). Two-stack: all ops O(1), space O(n) ~2n.]**

> Say it in the room: *"A plain stack gives O(1) push, pop, and top, but getMin would be an O(n) scan. With a parallel min-stack, all four operations are O(1) — including getMin, which is just the top of the min-stack. The cost is O(n) extra space, roughly 2n."*
>
> Naming that cost out loud is the move — it shows you know exactly what you traded.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: two variants side by side — "pairs in one stack" and "only push record-breakers".]**

> Can we shrink the 2n? Two honest options — great to offer unprompted.
>
> **Option A:** instead of two stacks, store `(value, running_min)` pairs in one stack. Same total storage, but a single structure — no risk of the two stacks drifting out of sync. A readability win, not a space win.
>
> **Option B — the real space-saver:** only push to the min-stack when a value *ties or beats* the current min. Then the min-stack holds just the record-breakers, often far fewer entries.

```python
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:   # <= is critical
            self.min_stack.append(val)

    def pop(self):
        x = self.stack.pop()
        if x == self.min_stack[-1]:        # only pop min-stack if we removed the min
            self.min_stack.pop()
```

> **LEARNER:** Why `<=` and not `<`? If it's equal, why bother pushing a duplicate?
>
> **TEACHER:** This is the subtle trap. Say the min is `-3` and you push another `-3`. With strict `<`, you skip it — the min-stack has only one `-3`. Now you pop *one* `-3`… and your code removes that single min-stack entry, exposing a wrong, larger min while a `-3` is still in the stack. Using `<=` records *both* copies, so each pop is accounted for. Get that wrong and it fails only on duplicate minimums — a nasty, hard-to-spot bug.
>
> Honest verdict: you can't get below O(n) — you must retain every value to serve arbitrary pops. Option B just makes the constant smaller on typical data.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Max Stack (LC 716)". A blank editor.]**

> Before the next video, try **Max Stack**, LC 716. Same idea flipped to a maximum — but there's a twist: it also wants a `popMax` that removes the max from *anywhere*, which a plain stack can't do alone. See how far the min-stack idea carries you, and where it cracks.
>
> Struggle first. Ten minutes minimum before you look anything up.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **The min is per-depth, not one number** — a single variable can't remember history.
> 2. **A parallel min-stack carries the running min at every level** — getMin is O(1).
> 3. **Pop both together** and the old minimum restores itself for free.
>
> And the peg — when a stack problem needs an *extra quantity kept consistent with push and pop*, don't scan: **shadow the stack with a second stack that carries the answer.**

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Next Greater Element". Two arrays and a single mysterious stack that pops several tiles at once.]**

> So far the stack just remembered things. Next, we make it *decide* — a stack that pops several elements at once the instant a bigger one walks in. It's called a **monotonic stack**, and it turns "for each element, find the next bigger one" from O(n²) into a single sweep. That's next: Next Greater Element. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class MinStack {
    private Deque<Integer> stack = new ArrayDeque<>();
    private Deque<Integer> minStack = new ArrayDeque<>();

    public void push(int val) {
        stack.push(val);
        if (minStack.isEmpty()) minStack.push(val);
        else minStack.push(Math.min(val, minStack.peek()));
    }

    public void pop()    { stack.pop(); minStack.pop(); }
    public int  top()    { return stack.peek(); }
    public int  getMin() { return minStack.peek(); }
}
```
