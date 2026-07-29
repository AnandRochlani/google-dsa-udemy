# 🎬 Recording Script — Happy Number
**Pattern: Fast & Slow Pointers · LeetCode 202 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the tortoise-and-hare cycle detection from Linked List Cycle (141).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: `19` on screen. It transforms: `1² + 9² = 82`, then `82 → 68 → 100 → 1`. A green "HAPPY ✅". Then `2 → 4 → 16 → 37 → … → 4` snaps into a red loop.]**

> Take a number. Square its digits, add them up, repeat. `19` becomes `82`, becomes `68`, becomes `100`, becomes… `1`. It's a "happy" number.
>
> But `2`? It spirals `4 → 16 → 37 → …` and eventually loops back to `4` — never reaching `1`. Not happy.
>
> Here's the thing: there's no linked list anywhere in this problem. And yet the *perfect* solution is the tortoise and hare you already know. By the end you'll see the linked list hiding inside plain arithmetic. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence: "Repeatedly sum the squares of digits. Reaches 1 → happy. Loops → not." Below: the `19` chain ending in 1, and the `2` chain looping.]**

> The problem in one line: **keep replacing the number with the sum of the squares of its digits — if you reach `1`, it's happy; if you fall into a loop, it's not.**
>
> `19 → 82 → 68 → 100 → 1` → **True**. `2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → …` → loops on `4` → **False**.
>
> Hold onto both chains.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: the `2` chain running, each value dropped into a "seen" box: {2}, {2,4}, {2,4,16}… until `4` reappears.]**

> First question when you simulate: *when do I give up?* The process is deterministic, so it either hits `1` or repeats a value forever — there's no running off to infinity, because the sums stay bounded.
>
> So the brute force: remember every value. Start at `2`. Box it. `4` — box it. `16, 37, 58, 89, 145, 42, 20` — box them. Then `20 → 4`.
>
> **[VISUAL: cursor lands on `4`, already glowing in the box. "SEEN — it's a loop, never reaches 1."]**
>
> `4` is back. We've looped without hitting `1`. Return **False**. And for `19`, we'd just hit `1` and return **True**.
>
> Correct. But look at that growing box.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The "seen" box holding all the intermediate values, a memory-meter climbing to O(k). A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The set grows with however many values appear before something repeats — **O(k) extra space.** But here's the reframe I want you to see. Look at this sequence again: each number *points to* exactly one next number. `2` points to `4`. `4` points to `16`. That's a `next` pointer.
>
> **LEARNER:** Wait — you're saying this chain of numbers is *literally a linked list*? There are no nodes, no `.next` fields anywhere.
>
> **TEACHER:** No explicit nodes — but the *structure* is identical. Each value has exactly one successor. Pause and predict: **if this is a linked list, and the question is "does it reach 1 or loop" — what O(1)-space tool do you already own for exactly that?**

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the `2` chain redrawn as list nodes: `2 → 4 → 16 → 37 → … → 4`, curling into a ring. The `19` chain redrawn ending at `1`, with `1 → 1` as a self-loop.]**

> Redraw the chain as a linked list. Each number is a node; `next` is "sum of squared digits." Suddenly the whole problem is familiar.
>
> "Reaches `1`" means the list ends at a special node — `1`, whose successor is `1` itself, a tight self-loop. "Never reaches `1`" means there's a genuine cycle somewhere *else*.
>
> **[VISUAL: tortoise and hare released onto the number-list. Slow steps one `next_num`, fast steps two. On the `2` chain they collide mid-ring; on the `19` chain fast reaches `1` and sticks.]**
>
> And detecting whether a linked list loops — with no memory — is the tortoise and hare. Slow does one step of the process; fast does two. If fast reaches `1`, happy. If the two pointers meet on any *other* value, that's a real cycle — not happy. The faster runner discovers the loop on its own. No set.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Sequence where each value has one successor = a linked list. Reach 1 or cycle → tortoise & hare."]**

> One line: **any deterministic sequence — each value has exactly one next — is a linked list, so "terminates or loops?" is tortoise and hare.**
>
> Spotting the *implicit* list is the transferable move. That's the whole lesson.

---

## 7. CODE IT — LIVE & CHUNKED — `4:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 — the "next pointer".]**

> First, the `next` function — sum of squared digits. This *is* our `next` pointer.

```python
def is_happy(n):
    def next_num(x):
        total = 0
        while x:
            x, d = divmod(x, 10)   # peel off the last digit
            total += d * d
        return total
```

> **[VISUAL: add chunk 2, highlight the two starting positions.]** Now tortoise and hare. Slow starts at `n`; fast starts one step ahead.

```python
    slow = n
    fast = next_num(n)
```

> **[VISUAL: add chunk 3, highlight the loop.]** Loop until fast reaches `1` or the two meet. Slow steps once, fast steps twice.

```python
    while fast != 1 and slow != fast:
        slow = next_num(slow)             # +1 step
        fast = next_num(next_num(fast))   # +2 steps
    return fast == 1
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line.]**

> Why each piece.
>
> `divmod(x, 10)` — peels off the last digit `d` and shrinks `x`, digit by digit, until `x` is `0`. Square each, sum them. That's one hop along our implicit list.
>
> `slow = n`, `fast = next_num(n)` — we deliberately start fast one step ahead so the loop condition `slow != fast` isn't accidentally true at the very start (they'd both be `n`). Small but important.
>
> The loop condition `while fast != 1 and slow != fast` — two exit doors. Door one: `fast` reaches `1`, so it's happy. Door two: `slow == fast`, they collided on some other value, so it's a cycle.
>
> **LEARNER:** But `1`'s next is `1` — a self-loop. Doesn't that mean the "cycle" check and the "reached 1" check fight each other? How do we know which one wins?
>
> **TEACHER:** Sharp. We check `fast != 1` *first*. The moment fast lands on `1`, that condition is false and we exit **before** the `slow != fast` collision logic can misfire. Then `return fast == 1` reports the truth: exited because of `1` → happy; exited because they met elsewhere → not. The ordering is doing real work.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it, close the loop)*

**[VISUAL: two trace tables — happy and unhappy.]**

> Run both.
>
> *Happy* `n = 19`:

| slow | fast | note |
|---|---|---|
| 19 | 82 | start (fast one ahead) |
| 82 | 100 | slow→82, fast→68→100 |
| 68 | 1 | slow→68, fast→1→1 → **fast == 1 → stop, return True** ✅ |

> *Unhappy* `n = 2` (chain `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 …`): fast and slow both circle this ring and eventually land on the same value with neither ever equal to `1` — the loop exits on `slow == fast`, and `fast == 1` is false → **False** ✅.
>
> Loop closed — happy detected by reaching `1`, unhappy detected by collision.

---

## 10. COMPLEXITY, OUT LOUD — `7:20`
*(transfer to interview)*

**[VISUAL: two rows — Hash set: O(log n) per step, O(k) space. Fast/slow: O(log n) per step, O(1) space.]**

> Say it out loud: *"Each step costs O(log n) — that's the number of digits. The set version stores every value it sees, O(k) space. The tortoise and hare runs the same steps but stores nothing — **O(1) space**."*
>
> Same work per hop, but we deleted the growing set. That's the trade.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:50`
*(depth + honesty — make the space beat shine)*

**[VISUAL: the hash set of intermediate values (O(k)) crossed out; two integer variables labelled O(1).]**

> This is the point of using the pattern here, so let's make it land.
>
> The hash set stored every value the sequence produced, just to notice a repeat — O(k) memory. But *nothing about the sequence needs remembering.* A second pointer, running twice as fast, discovers the loop entirely on its own — because a faster runner on a ring always catches the slower one.
>
> Two integers. O(1) space. Say it in the room: *"The digit-square sequence is really a linked list, so I run tortoise and hare instead of a hash set — fast reaching 1 means happy, meeting elsewhere means an unhappy cycle. Constant space."* Recognising the hidden list *is* the unlock.

---

## 12. YOUR TURN (active recall) — `8:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Find the Duplicate Number (LC 287)". A blank editor.]**

> Before the next video, try **Find the Duplicate Number**. Same move: an array where each value points to an index is an *implicit* linked list, and the duplicate sits at a cycle. Spot the hidden list, unleash tortoise and hare.
>
> Struggle first. Seeing the list where there isn't one is the whole skill.

---

## 13. LOCK IT IN — `8:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **A deterministic sequence is a linked list** — each value has exactly one successor.
> 2. **"Terminates or loops?" = cycle detection.** Reach `1` → happy; meet elsewhere → not.
> 3. **Check `fast == 1` before the collision** — the self-loop at `1` must win.
>
> Memory peg: **"Numbers with a `next` are a list in disguise."** When a process spits out one value after another, draw the arrows — and the tortoise and hare shows up.

---

## 14. CLIFFHANGER — `9:05`
*(open loop to next lesson)*

**[VISUAL: a list `1 → 2 → 3 → 4 → 5` with every arrow slowly flipping to point the other way: `5 → 4 → 3 → 2 → 1`.]**

> We've spent this chapter *reading* lists with two pointers — detecting loops, finding middles — never changing them.
>
> Next chapter, we start *rewiring* them. First up: reverse a linked list in place, flipping every arrow with O(1) space. It's the atom that three harder problems are built from. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean isHappy(int n) {
    int slow = n, fast = next(n);
    while (fast != 1 && slow != fast) {
        slow = next(slow);
        fast = next(next(fast));
    }
    return fast == 1;
}

private int next(int x) {
    int total = 0;
    while (x > 0) {
        int d = x % 10;
        total += d * d;
        x /= 10;
    }
    return total;
}
```
