# 🎬 Recording Script — Middle of the Linked List
**Pattern: Fast & Slow Pointers · LeetCode 876 · Easy · Target length ~8 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the tortoise-and-hare setup from Linked List Cycle (141).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a list `1 → 2 → 3 → 4 → 5`. A cursor walks it, hits `null`, then sighs and walks it *again* halfway. A "pass 1… pass 2…" counter ticks.]**

> Find the middle of a linked list. Easy, right? Count the nodes, then walk halfway in. Two passes, done.
>
> But there's a version where one pointer moving twice as fast lands on the middle in a **single sweep** — no counting at all. The speed ratio literally *is* the division by two. Let me show you the trick, because it's the same tortoise-and-hare you already know, pointed at a new target. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one sentence: "Return the middle node (if two middles, the second)." Below: `1 → 2 → 3 → 4 → 5` with `3` circled; and `1 → 2 → 3 → 4 → 5 → 6` with `4` circled.]**

> The problem in one line: **return the middle node — and if the list is even-length with two middles, return the second one.**
>
> Odd list `1 → 2 → 3 → 4 → 5` → the middle is `3`. Even list `1 → 2 → 3 → 4 → 5 → 6` → two middles, `3` and `4`, and we want the **second**, `4`.
>
> Keep both in your eye — we need our trick to nail both parities.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:00`
*(worked example — let them feel the waste)*

**[VISUAL: `1 → 2 → 3 → 4 → 5`. Pass 1: cursor walks all five, a counter shows n=5. Pass 2: cursor restarts, walks n//2 = 2 steps, lands on `3`.]**

> The textbook definition: middle is at index `n/2`. So the literal approach — count first, then walk.
>
> **Pass one:** walk the whole list counting. `1, 2, 3, 4, 5` — `n = 5`.
>
> **Pass two:** go back to the head, walk `n // 2 = 2` steps: `1 → 2 → 3`. Land on `3`. Correct.
>
> It works. But notice — we walked the list, then walked it *again*. And we had to compute and hold `n` just to divide it.

---

## 4. THE PAIN POINT + PREDICT — `2:00`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Two full sweeps of the list highlighted, side by side, labelled "pass 1" and "pass 2". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** It's not *wrong* — it's O(n) time, O(1) space, perfectly fine. But it makes **two passes**, and it only knows where to stop *after* counting the whole thing. An interviewer wants the one-pass answer that shows you know the pointer trick.
>
> **LEARNER:** But the middle is defined by the total length — I literally can't know where the middle is until I've seen the end. How could one pass possibly work?
>
> **TEACHER:** That's the exact instinct to break. Pause and predict: **if I had a second pointer that reaches the end when the first is only halfway, what would the first pointer be sitting on?** You already met this pair last lesson.

---

## 5. BUILD THE INTUITION (the aha) — `2:45`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two runners on the straight list. Slow (1 step) and fast (2 steps). When fast reaches the end at `5`, slow is exactly on `3`.]**

> Remember the tortoise and hare? Same two runners — but this track is *straight*, so nobody laps anybody. Watch where they land.
>
> Slow takes one step, fast takes two. Fast covers the list twice as fast, so when fast reaches the **end**, slow has covered exactly **half** the distance. Slow is sitting on the middle.
>
> **[VISUAL: trace on `1 → 2 → 3 → 4 → 5`: slow 1→2→3, fast 1→3→5. Fast at end, slow on 3.]**
>
> No counting. No second pass. The 2-to-1 speed ratio *is* the "divide by two" — the geometry does the arithmetic for us. When the hare hits the wall, the tortoise is on the midpoint.

---

## 6. THE KEY MOVE (signaling) — `3:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Slow +1, fast +2. When fast reaches the end, slow is the middle."]**

> One line: **slow steps one, fast steps two — when fast runs off the end, slow is standing on the middle.**
>
> Same tortoise and hare as cycle detection. There we stopped when they *met*; here we stop when fast hits the *end*.

---

## 7. CODE IT — LIVE & CHUNKED — `4:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor, `class ListNode` assumed. Type chunk 1.]**

> Both pointers start at the head.

```python
def middle_node(head):
    slow = fast = head
```

> **[VISUAL: add chunk 2, highlight the condition.]** Loop while fast can take a full two-step hop — so `fast` and `fast.next` both exist.

```python
    while fast and fast.next:
        slow = slow.next          # +1
        fast = fast.next.next     # +2
    return slow                   # fast hit the end → slow at middle
```

> That's the whole function. Three lines of logic.

---

## 8. EXPLAIN THE CODE (the WHY) — `4:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line, plus a side note showing the even case ending with `fast = None`.]**

> Why each piece exists.
>
> `while fast and fast.next` — this guard is doing double duty. It keeps `fast.next.next` legal, *and* it's what decides the even-length tiebreak. Let me show you.
>
> **LEARNER:** That's what I'd want to check — for an even list, does this land on the first middle or the second? Those are different nodes.
>
> **TEACHER:** Let's prove it. Even list `1 → 2 → 3 → 4 → 5 → 6`. Slow goes 1→2→3→4; fast goes 1→3→5→null. When fast becomes `null`, the condition `fast` is false, we stop, and slow is on `4` — the **second** middle. Exactly what the problem asks. If you ever wanted the *first* middle instead, you'd change the condition to `while fast.next and fast.next.next`. Same pointers, different stop line.

---

## 9. DRY-RUN THE CODE — `5:40`
*(worked example — prove it, close the loop)*

**[VISUAL: two trace tables side by side, odd and even.]**

> Both parities, real code.
>
> *Odd* `1 → 2 → 3 → 4 → 5`:

| slow | fast | note |
|---|---|---|
| 1 | 1 | start |
| 2 | 3 | |
| 3 | 5 | `fast.next` is null → stop → **return 3** ✅ |

> *Even* `1 → 2 → 3 → 4 → 5 → 6`:

| slow | fast | note |
|---|---|---|
| 1 | 1 | start |
| 2 | 3 | |
| 3 | 5 | |
| 4 | null | `fast` is null → stop → **return 4** (second middle) ✅ |

> Odd gives `3`, even gives `4`. Both correct, one pass each. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `6:20`
*(transfer to interview)*

**[VISUAL: two rows — Count + walk: O(n), two passes, O(1). Fast/slow: O(n), one pass, O(1).]**

> Say it out loud: *"Counting then walking is O(n) time but two passes. The fast/slow version is O(n) time in a **single** pass, O(1) space. Same Big-O, but half the traversals and no length bookkeeping."*
>
> The interviewer isn't just checking the Big-O here — they're checking whether you reach for the pointer trick.

---

## 11. CAN WE USE LESS MEMORY? (space) — `6:50`
*(depth + honesty — name the absence)*

**[VISUAL: both approaches shown with just two pointer arrows, both labelled O(1). A callout: "the win here is PASSES, not space."]**

> Here's an honest twist on the usual space beat: **both** approaches are already O(1) space. We only ever hold a couple of pointers — nothing grows with the list.
>
> So the win *isn't* memory this time — it's **passes**. Fast/slow finds the middle in one traversal instead of two. And naming that precisely is itself a skill: *"Space is already constant in both; the fast/slow version's advantage is halving the number of passes, not the memory."* Saying exactly what you're optimising — and what you're *not* — reads as senior.

---

## 12. YOUR TURN (active recall) — `7:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Palindrome Linked List (LC 234)". A blank editor.]**

> Before the next video, try **Palindrome Linked List**. Step one is *this* — find the middle. Then you reverse the second half and compare it to the first. It stacks today's trick onto the next chapter's.
>
> Try it before you peek. Feeling where the middle-finding slots in is the point.

---

## 13. LOCK IT IN — `7:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **A 2:1 speed ratio divides the list in half** — no counting needed.
> 2. **Stop condition sets the tiebreak.** `while fast and fast.next` gives the *second* middle on even lists.
> 3. **Same tortoise and hare** as cycle detection — just stop at the end, not at a collision.
>
> Memory peg: **"When the hare hits the wall, the tortoise is at the middle."** Straight track, no lapping — the finish line is the stop signal.

---

## 14. CLIFFHANGER — `8:05`
*(open loop to next lesson)*

**[VISUAL: a number `19` morphing into `82`, then `68`, then `100`, then `1` — arrows between them like a linked list.]**

> We've used fast/slow on real lists — cycles, middles. But the pattern's sneakiest use is when there's *no list at all*: just a number generating the next number. Does it reach `1`, or loop forever?
>
> That's a linked list hiding inside arithmetic — and the same tortoise and hare cracks it. Next video: Happy Number. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;   // second middle for even length
}
```
