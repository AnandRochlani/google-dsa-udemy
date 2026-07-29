# 🎬 Recording Script — Linked List Cycle II (Find the Cycle Start)
**Pattern: Fast & Slow Pointers · LeetCode 142 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Linked List Cycle (141) — the tortoise-and-hare detection from last lesson.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: the list `3 → 2 → 0 → -4 ⤴2`. Last video's two pointers collide on `-4`, which flashes green. Then a red question mark jumps to node `2` with the caption "but the loop starts HERE."]**

> Last video, our tortoise and hare caught the cycle — they collided right here, on `-4`.
>
> But the interviewer isn't done. *"Great, you found the loop. Now tell me which node it **starts** at."* And the meeting point isn't the start. They met at `-4`; the loop actually begins at `2`.
>
> Here's the wild part: you get from the collision to the entrance by resetting one pointer to the head and walking both forward — and they land *exactly* on the start. No memory. By the end of this video you'll not only do it, you'll know *why* it works. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence: "Return the node where the cycle begins (or null)." Below: `3 → 2 → 0 → -4 ⤴2`, node `2` circled and labelled "answer".]**

> The problem in one line: **return the node where the cycle begins — or `null` if there's no cycle.**
>
> Same little list. `-4` points back to `2`, so the loop is `2 → 0 → -4 → 2`. The entrance is `2`. That node is what we return — not `True`, the actual node.
>
> Hold that: **answer is node `2`.**

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: the cyclic list with a "seen" box. Cursor drops 3, 2, 0, -4 into the box, then lands on `2` which is already glowing.]**

> The brute force is the same friend from last time: remember every node.
>
> Walk `3`, box it. `2`, box it. `0`, box it. `-4`, box it. Follow `-4.next` → `2`.
>
> **[VISUAL: "2 already seen — this IS the entrance!" flag.]**
>
> `2` is the *first* node we hit twice — and that's not a coincidence. The first repeat is *exactly* where the loop closes back on itself. So the hash set doesn't just detect the cycle, it hands you the entrance for free. Return node `2`.
>
> Correct and easy. But that box…

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The "seen" box swells to O(n). Beside it, last lesson's tortoise-and-hare meeting point on `-4` — with the caption "detects the loop in O(1)… but meets at the WRONG node."]**

> **TEACHER:** The box is O(n) space again. And we already have an O(1)-space *detector* from last lesson. So why not just use it? Because — look — the tortoise and hare meet at `-4`, *inside* the loop. Not at `2`. The collision point is not the entrance.
>
> **LEARNER:** Right, so the O(1) tool gives us the wrong node. It feels like we're stuck choosing between "correct entrance but O(n) memory" and "O(1) memory but wrong node." How do we get both?
>
> **TEACHER:** That's the whole puzzle. Pause here and predict: **given only where they collided, is there some fixed relationship between that spot and the true entrance?** Something we could exploit with pointers alone?

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the list drawn as a "rho" (ρ) shape: a straight tail of length F into a ring of length C. Label the tail `F`, the ring `C`. Mark head, entry, and meeting point.]**

> Let's name distances. Call `F` the distance from the **head** to the **entrance** of the loop. Call `C` the length of the loop.
>
> Now the arithmetic — go slow, it's worth it. When **slow** first reaches the entrance, it has walked `F` steps. In that same time **fast** walked `2F`, so fast is already `F` steps *deep into the loop*.
>
> Inside the ring, fast gains one node on slow every step. The gap it needs to close is `C − F`. So they meet after another `C − F` steps — which puts the meeting point `C − F` nodes *past* the entrance.
>
> **[VISUAL: highlight that `C − F` past the entrance == `F` before the entrance, walking around the ring.]**
>
> Here's the punchline: being `C − F` past the entrance is the *same as* being `F` steps *away from* the entrance if you keep walking around. So from the meeting point, the entrance is exactly **`F` steps ahead** — and the head is also exactly **`F` steps** from the entrance.
>
> **[VISUAL: two runners — one starting at head, one at the meeting point — both advance one step at a time, converging on the entry node `2`.]**
>
> Same distance, `F`, from two different starting points. So: reset one pointer to the head, leave the other at the collision, and walk them **one step at a time each**. They cover `F` steps together and meet — right at the entrance. That's the magic.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed two-line rule: "Phase 1: fast/slow until they collide.  Phase 2: reset slow to head, step both by 1 — they meet at the start."]**

> Two phases, one line to remember: **collide with the tortoise and hare, then reset one pointer to the head and walk both by one — where they meet is the entrance.**
>
> Phase one is last lesson. Phase two is the new trick.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor, `class ListNode` assumed. Type chunk 1 — phase 1.]**

> Phase one: detect the collision, exactly like problem 141, but we `break` on the meeting instead of returning.

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None            # loop exited normally → no cycle
```

> **[VISUAL: highlight the `while … else`.]** That `else` on the `while` is Python's quiet gem — it runs only if the loop finished *without* a `break`. No break means fast fell off the end. No cycle. Return `None`.
>
> **[VISUAL: add chunk 2 — phase 2.]** Now the entrance. Reset `slow` to the head; leave `fast` where they collided. Step both by **one**.

```python
    slow = head                # reset one pointer to the head
    while slow is not fast:
        slow = slow.next       # both move ONE step now
        fast = fast.next
    return slow                # they meet exactly at the cycle start
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line.]**

> Let's walk the *why*.
>
> Phase one is unchanged from detection — the only edit is `break` instead of `return True`, because we need to *keep* the meeting node in `fast` for phase two.
>
> `slow = head` — this is the entire second-phase idea in one line. We proved head-to-entrance equals collision-to-entrance, both `F`. Resetting slow to head sets up two pointers `F` apart from the entrance.
>
> **LEARNER:** Hang on — in phase two, why does `fast` suddenly move only *one* step? It was the double-speed pointer the whole time.
>
> **TEACHER:** Great catch, and it trips a lot of people. The "double speed" was only a tool for phase one — to *force* a collision. In phase two the job is different: two pointers `F` apart need to arrive together, so they must move at the *same* speed. If fast kept doubling, it'd overshoot. Same distance, same speed, they meet. The name "fast" is just a leftover variable.
>
> And `return slow` — when `slow is fast`, they're on the same node: the entrance.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: `3 → 2 → 0 → -4 ⤴2`. Note F = 1 (head→2), loop `2 → 0 → -4`, C = 3. Trace tables.]**

> Run it on our list. Here `F = 1` and the loop length `C = 3`.
>
> **Phase 1** — identical to last video:

| step | slow | fast | meet? |
|---|---|---|---|
| start | 3 | 3 | no |
| 1 | 2 | 0 | no |
| 2 | 0 | 2 | no |
| 3 | -4 | -4 | **collide → break** |

> **Phase 2** — reset `slow` to head (`3`); `fast` stays on `-4`. Step both by one:

| step | slow | fast | same? |
|---|---|---|---|
| start | 3 | -4 | no |
| 1 | 2 | 2 *(from -4 wrapping to 2)* | **yes → return node 2** ✅ |

> One step and they land on `2` — the entrance. Exactly the node we said was the answer. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Hash set: O(n) time, O(n) space. Floyd two-phase: O(n) time, O(1) space.]**

> Say it out loud: *"The hash set finds the first repeated node — the entrance — in O(n) time and O(n) space. Floyd's two phases are also O(n) time: phase one is at most a couple of laps, phase two walks at most the length of the list. But it's **O(1) space** — three pointers, nothing that grows."*
>
> Same time as the set, none of the memory. That's the whole trade.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty — make the space beat shine)*

**[VISUAL: the hash set (O(n)) crossed out; three little pointer arrows labelled O(1). Beside them, the "F = F" distance identity glowing.]**

> This is the beat that matters. The hash set stored every node just to recognise the first repeat — O(n) memory that scales with the list.
>
> Floyd's trick remembers *nothing*. It replaces memory with **geometry**: the distance from the head to the entrance equals the distance from the collision to the entrance. That fact is doing the work the hash set used to do — and a fact costs zero bytes.
>
> Say it in the room: *"I don't need to store visited nodes. The loop's geometry gives me the entrance — reset one pointer to head, walk both by one, they meet at the start. O(1) space."* Naming *why* the reset works — not just that it does — is what separates a memorised answer from an understood one.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Find the Duplicate Number (LC 287)". A blank editor.]**

> Before the next video, try **Find the Duplicate Number**. It looks like an array problem — but if you treat each value as a `next` pointer, the array *becomes* a linked list with a cycle, and the duplicate is the cycle's **entrance**. Same phase-two trick, in disguise.
>
> Wrestle with it before peeking. Recognising the hidden list is the real skill.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Detection ≠ location.** The tortoise and hare meet *inside* the loop, not at its start.
> 2. **The distance identity:** head-to-entrance equals collision-to-entrance. That's the whole engine.
> 3. **Phase two moves both pointers by ONE** — same distance, same speed, they meet at the entrance.
>
> Memory peg: **"Detect, then reset."** Catch them anywhere in the ring, send one back to the start line, and let them walk into the entrance together.

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: a numeric sequence `19 → 82 → 68 → 100 → 1`, drawn as list nodes with arrows. Then `4 → 16 → 37 → … → 4` curling into a loop.]**

> We've done cycles on *real* linked lists. But what if there's no list at all — just a number, spitting out the next number, forever? Does it settle on `1`, or spin in a loop?
>
> Turns out that's the *same* problem — a linked list hiding inside arithmetic. Next video: Happy Number. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {          // collision → find entry
            ListNode ptr = head;
            while (ptr != slow) {
                ptr = ptr.next;
                slow = slow.next;
            }
            return ptr;
        }
    }
    return null;                      // no cycle
}
```
