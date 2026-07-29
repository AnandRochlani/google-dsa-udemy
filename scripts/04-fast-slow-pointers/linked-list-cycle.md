# 🎬 Recording Script — Linked List Cycle
**Pattern: Fast & Slow Pointers · LeetCode 141 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the first fast/slow lesson. It seeds the whole pattern.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a linked list `3 → 2 → 0 → -4`, then an arrow curls from `-4` back to `2`. A cursor starts walking the arrows and never stops — it loops forever. A tiny "still running…" spinner spins in the corner.]**

> Here's a linked list. You start at the head and follow `next`, `next`, `next`, waiting to hit `null` and stop.
>
> Except this one never stops. The last node points *backward*, into the middle, and now your loop runs forever.
>
> Google loves this question because the naive fix — "just remember everywhere I've been" — is the answer they *don't* want. By the end of this video you'll detect that loop using two pointers and **zero extra memory**. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top: "Does the list loop back on itself?" Below, two tiny lists side by side: `1 → 2 → null` labelled "no cycle → False", and `3 → 2 → 0 → -4 ⤴` (arrow back to 2) labelled "cycle → True".]**

> The whole problem in one line: **does following `next` ever loop back, or does it reach `null`?**
>
> Two tiny examples. On the left, `1 → 2 → null` — a clean ending, so **False**. On the right, `3 → 2 → 0 → -4`, and `-4` points back to `2` — you loop `2 → 0 → -4 → 2` forever, so **True**.
>
> Keep that four-node loop in your eye. We'll solve it two ways.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the cyclic list. A growing "seen" box on the right. The cursor visits each node and drops a copy into the box: {3}, {3,2}, {3,2,0}, {3,2,0,-4}…]**

> Let's do what your brain does first. How do you know you're going in circles? You *remember where you've been.*
>
> Walk from `3`. Never seen it — drop it in the "seen" box. Then `2` — new, box it. Then `0` — box it. Then `-4` — box it. Follow `-4.next`… and it's `2`.
>
> **[VISUAL: cursor lands on `2`, which is already glowing inside the box. A big "SEEN BEFORE!" flag pops.]**
>
> `2` is already in the box. We've been here. That's the cycle — return **True**.
>
> It works. It's clean. But look at that box.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The "seen" box balloons to hold every node of a huge list. A memory-meter climbs toward O(n). A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** Here's the catch. That box holds a reference to *every node* we visit — for a list of ten thousand nodes, that's ten thousand stored pointers. **O(n) extra memory.** And the classic Google follow-up is exactly: *"Now do it in O(1) space."*
>
> **LEARNER:** But wait — the whole reason it works is that I *remember* the past. If I'm not allowed to store anything, how could I possibly know I've looped? I'd have nothing to compare against.
>
> **TEACHER:** That's the exact wall we have to climb. Pause the video and sit with it: **is there a way to catch a loop without remembering a single node you've visited?** Think about two runners on a track.

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a circular running track. Two runners: a slow tortoise (1 step) and a fast hare (2 steps). On a straight track the hare just reaches the finish line. On the circular track, the hare keeps lapping and closes in on the tortoise.]**

> Forget nodes for a second. Picture two runners on a track.
>
> A **slow** runner takes one step at a time. A **fast** runner takes two. On a *straight* track, the fast one just reaches the end first and it's over — no loop.
>
> But on a *circular* track? The fast runner laps around and starts gaining on the slow one from behind — one step of gap closed every tick. They *must* eventually collide. There's nowhere for the fast runner to escape to.
>
> **[VISUAL: overlay the runners onto the `3 → 2 → 0 → -4 ⤴` list. Slow steps 3→2→0. Fast steps 3→0→2 (wrapping). They converge on -4.]**
>
> So map it onto the list. Slow moves one node, fast moves two. If the list ends, fast hits `null` — no cycle. If it loops, fast gets trapped in the ring with slow and rear-ends it. "Is there a loop?" just became "do these two pointers ever land on the same node?" No memory required — the second runner *is* our detector.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Two speeds. Fast hits null → no cycle. Fast meets slow → cycle."]**

> Burn this one line in: **run two pointers at different speeds — if fast falls off the end, there's no cycle; if fast ever catches slow, there is.**
>
> That's Floyd's tortoise and hare, and it's the seed for this entire chapter.

---

## 7. CODE IT — LIVE & CHUNKED — `4:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. `class ListNode` with `val`/`next` is assumed. Type chunk 1 only.]**

> Let's build it. Both pointers start at the head.

```python
def has_cycle(head):
    slow = fast = head
```

> **[VISUAL: add chunk 2, highlight the loop condition.]** Now the loop. We keep going while fast can *safely* take two steps — so `fast` and `fast.next` both have to exist.

```python
    while fast and fast.next:
        slow = slow.next          # +1 per step
        fast = fast.next.next     # +2 per step
```

> **[VISUAL: add chunk 3, highlight the `is` check.]** After each move, check for a collision. If they're the same node, we've found the loop.

```python
        if slow is fast:          # they collided → cycle
            return True
    return False                  # fast fell off the end → no cycle
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `slow = fast = head` — both start together. If they ever meet *again* after moving, that reunion can only happen inside a loop.
>
> `while fast and fast.next` — this is the guard that makes "two steps" legal. Fast is the one doing `fast.next.next`, so both `fast` and `fast.next` must be real nodes, or that line crashes.
>
> **LEARNER:** Quick one — why check identity with `slow is fast` and not `slow.val == fast.val`? Two different nodes could hold the same value.
>
> **TEACHER:** Exactly why we use `is`. We care whether they're the *same node in memory*, not whether their values match. Two nodes both holding `2` are not a cycle. `is` compares identity — that's the correct test.
>
> And `return False` after the loop — if fast reached `null`, the list had an end, so no cycle. Clean.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it, close the loop)*

**[VISUAL: `3 → 2 → 0 → -4 ⤴2` with a trace table filling row by row.]**

> Let's run the real code on our four-node loop.

| step | slow (val) | fast (val) | meet? |
|---|---|---|---|
| start | 3 | 3 | no |
| 1 | 2 | 0 | no |
| 2 | 0 | 2 | no *(fast lapped past -4 back to 2)* |
| 3 | -4 | -4 | **yes → return True** ✅ |

> Three steps and they collide on `-4`. And for `1 → 2 → null`? `fast` jumps straight to `null`, the loop never runs its check, and we return **False**. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:20`
*(transfer to interview)*

**[VISUAL: two rows — Hash set: O(n) time, O(n) space. Fast/slow: O(n) time, O(1) space.]**

> Say it the way you'd say it in the room: *"The hash-set version is O(n) time but O(n) space. The tortoise and hare is still O(n) time — the fast pointer covers at most a couple of laps before it catches up — but only **O(1) space**, just two pointers."*
>
> Same speed, and we deleted all the memory. That contrast is what earns the nod.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:50`
*(depth + honesty — this is the whole point)*

**[VISUAL: side by side — the hash set storing every node (O(n)) crossed out; two little pointer arrows labelled O(1).]**

> This beat *is* the point of the pattern, so let's make it shine.
>
> The hash set was doing real work: remembering the entire past so it could spot a repeat. That memory grows with the list — O(n).
>
> The tortoise and hare remembers *nothing*. It replaces "store every node I've seen" with "let a faster runner lap the track and crash into me." The loop reveals itself through *motion*, not memory. Two pointers, O(1) space, forever — no matter how big the list gets.
>
> Say it out loud: *"I trade the hash set for a second pointer at double speed. Same time, constant space."* That single sentence is the strong-hire signal.

---

## 12. YOUR TURN (active recall) — `8:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Linked List Cycle II (LC 142)". A blank editor.]**

> Before the next video, try **Linked List Cycle II**. Same tortoise and hare — but now, after you detect the loop, you have to return the *node where the cycle begins.* The detection is identical; finding the entrance is a beautiful twist.
>
> Struggle with it first. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `8:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Detecting a loop with memory is easy — a hash set of visited nodes.** Know it, then improve on it.
> 2. **Two speeds beat memory.** Fast hits `null` → no cycle; fast catches slow → cycle.
> 3. **Use `is`, not `==`** — you're comparing node *identity*, not values.
>
> And the memory peg — when you hear *"cycle in a linked list, O(1) space,"* picture it: **tortoise and hare on a circular track. The hare always laps the tortoise.**

---

## 14. CLIFFHANGER — `9:20`
*(open loop to next lesson)*

**[VISUAL: the loop from `-4` back to `2`. A big glowing question mark hovers over node `2` with the caption "where does the loop START?"]**

> We can now *detect* the loop. But here's the itch: our two pointers meet at `-4` — somewhere *inside* the ring — not at `2`, where the loop actually begins.
>
> So how do you find the exact entrance, still with no extra memory? There's a piece of arithmetic so clean it feels like a magic trick. That's the next video. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```
