# 🎬 Recording Script — Reverse Linked List
**Pattern: In-Place Linked-List Reversal · LeetCode 206 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the foundation the whole reversal chapter is built on.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: `1 → 2 → 3 → 4 → 5 → null`. Every arrow flips, one by one, until it reads `5 → 4 → 3 → 2 → 1 → null`. No new nodes appear — only the arrows move.]**

> Reverse a linked list. It sounds trivial, and it's the single most-asked linked-list question at Google — because it's the *atom*. Three harder problems in this chapter are just this move, repeated.
>
> The tempting answer copies everything into an array. But watch — the nodes never move. The *only* thing wrong is which way each arrow points. So we won't copy a thing. We'll just turn the arrows around, in place, with O(1) memory. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence: "Flip the list so it runs the other way; return the new head." Below: `1 → 2 → 3 → null` becoming `3 → 2 → 1 → null`.]**

> The problem in one line: **reverse the list and return the new head.**
>
> Tiny example — just three nodes: `1 → 2 → 3 → null` should become `3 → 2 → 1 → null`. The old tail `3` becomes the new head; the old head `1` becomes the new tail, pointing at `null`.
>
> We'll trace this exact list by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — let them feel the waste)*

**[VISUAL: `1 → 2 → 3`. An array fills: [1, 2, 3]. Then a second pass writes values back reversed into the same nodes.]**

> Your brain's first move: "reverse means collect everything and flip the order." So dump the values into an array — `[1, 2, 3]` — then walk the list again writing them back reversed: node one gets `3`, node two gets `2`, node three gets `1`.
>
> **[VISUAL: nodes now read 3, 2, 1 — but the arrows still point left-to-right.]**
>
> It works. The list now reads `3 → 2 → 1`. But look what we spent: a whole array the size of the list, just to rearrange numbers that were already sitting right there.

---

## 4. THE PAIN POINT + PREDICT — `1:55`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The array highlighted next to the list, memory-meter at O(n). The nodes glow — caption: "the nodes never moved. only the arrows are wrong." A 4-second "🤔 your turn" timer.]**

> **TEACHER:** That array is **O(n) extra space**. And here's the thing that should bug you: we already *have* every node. Nothing is missing. The list holds all five values in the right nodes — the only thing wrong is the *direction* of each `next` arrow.
>
> **LEARNER:** Okay, but if I flip node one's arrow to point back at `null`, I've just cut myself off from the rest of the list. Node two is gone. How do I flip an arrow without losing everything downstream?
>
> **TEACHER:** *That's* the real problem — not reversing, but not losing your place. Pause and predict: **before you overwrite a node's `next`, what's the one thing you must save first?**

---

## 5. BUILD THE INTUITION (the aha) — `2:45`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: three labelled hands over the list — `prev` (behind), `curr` (the node being rewired), `nxt` (saved ahead). They slide forward together, node by node, flipping each arrow.]**

> The fix is three fingers. Think of walking the list and, at each node, bending its arrow *backward* — to point at the node you just came from.
>
> To do that safely you need three references:
> - **`prev`** — the node behind you. That's where `curr.next` should now point.
> - **`curr`** — the node you're rewiring right now.
> - **`nxt`** — a saved copy of `curr.next`, grabbed *before* you overwrite it, so the rest of the list doesn't vanish.
>
> **[VISUAL: trace on `1 → 2 → 3`. curr=1: save nxt=2, flip 1→null, slide. curr=2: save nxt=3, flip 2→1, slide. curr=3: save nxt=null, flip 3→2, slide.]**
>
> The dance: **save `nxt`, flip `curr.next` to `prev`, slide `prev` up to `curr`, slide `curr` up to `nxt`.** One node moves from the untouched front to the reversed back, every step. That saved `nxt` is what answers the learner's worry — you never lose the remainder.

---

## 6. THE KEY MOVE (signaling) — `4:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "save next · flip arrow back · slide prev · slide curr".]**

> Burn in the four-beat rhythm: **save next, flip the arrow back, slide prev, slide curr.** Repeat until you fall off the end. `prev` is your new head.
>
> This little four-step dance is the atom of the entire chapter.

---

## 7. CODE IT — LIVE & CHUNKED — `4:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor, `class ListNode` assumed. Type chunk 1.]**

> Set up the two anchors. `prev` starts at `null` — because the old head becomes the new tail, pointing at `null`.

```python
def reverse_list(head):
    prev, curr = None, head
```

> **[VISUAL: add chunk 2, highlight the four lines as the "dance".]** Now the loop — the exact four beats, in order.

```python
    while curr:
        nxt = curr.next     # 1. save the rest of the list
        curr.next = prev    # 2. flip this arrow backward
        prev = curr         # 3. advance prev
        curr = nxt          # 4. advance curr
    return prev             # prev is the new head
```

> Four lines inside the loop. That order is not negotiable — we'll see why next.

---

## 8. EXPLAIN THE CODE (the WHY) — `5:20`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each of the four lines in sequence, showing what breaks if reordered.]**

> Why the order matters — this is where people slip.
>
> `nxt = curr.next` **first.** The very next line overwrites `curr.next`. If we hadn't saved it, the rest of the list would be gone forever. This line is the learner's "don't lose your place" insurance.
>
> `curr.next = prev` — the actual reversal. This one node's arrow now points backward.
>
> `prev = curr`, then `curr = nxt` — slide both forward. Note we set `prev` *before* `curr`, using the old `curr`, then move `curr` to the saved `nxt`.
>
> **LEARNER:** Why does `prev` start at `None` and not at `head`? Every other pointer problem we start at the head.
>
> **TEACHER:** Because `prev` represents "the node behind the current one," and for the very first node, there *is* nothing behind it — the original head must end up pointing at `null`. Starting `prev = None` makes that fall out automatically on the first flip. And when the loop ends, `curr` is `null` but `prev` is sitting on the last real node — the new head. That's why we `return prev`, not `curr`.

---

## 9. DRY-RUN THE CODE — `6:20`
*(worked example — prove it, close the loop)*

**[VISUAL: `1 → 2 → 3 → null` with a trace table filling row by row.]**

> Run the real code on our three nodes.

| step | prev | curr | nxt | after `curr.next = prev` |
|---|---|---|---|---|
| start | null | 1 | — | — |
| 1 | 1 | 2 | 2 | `1 → null` |
| 2 | 2 | 3 | 3 | `2 → 1` |
| 3 | 3 | null | null | `3 → 2` |

> `curr` is `null` → stop. Return `prev` = node `3`. Result: `3 → 2 → 1 → null`. Exactly what we predicted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:00`
*(transfer to interview)*

**[VISUAL: three rows — Value array: O(n) time, O(n) space. Recursive: O(n) time, O(n) stack. Iterative: O(n) time, O(1) space.]**

> Say it out loud: *"The array approach is O(n) time, O(n) space. Recursion is elegant but costs O(n) stack. The iterative three-pointer is O(n) time and **O(1) space** — just three references. I'd default to iterative."*
>
> Same time everywhere; the iterative version is the one that spends no extra memory.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:30`
*(depth + honesty — make the space beat shine)*

**[VISUAL: the value array (O(n)) and the recursion call stack (O(n)) both crossed out; three little pointer arrows labelled O(1).]**

> This is the beat that defines the whole chapter, so let it land.
>
> The key realisation: **reversing a linked list is a pointer-rewiring problem, not a data-copying one.** The array existed only to hold values we already had. The recursion's O(n) cost is the call stack — hidden memory, but memory all the same.
>
> The iterative dance moves *nothing* but three little pointers. The nodes stay exactly where they are; only the arrows change. That's what makes O(1) space possible. Say it in the room: *"I don't copy anything — I flip each `next` in place with prev and curr. O(1) space, versus O(n) for an array or the recursion stack."* That sentence is the reason this is the chapter's foundation.

---

## 12. YOUR TURN (active recall) — `8:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Reverse Linked List II (LC 92)". A blank editor.]**

> Before the next video, try **Reverse Linked List II** — reverse only the nodes between positions `left` and `right`, and stitch the ends back on. The reversal is *today's* dance; the challenge is the boundary surgery.
>
> Try it before peeking. Feeling where the joins go wrong is exactly what the next lesson fixes.

---

## 13. LOCK IT IN — `8:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Reversal is rewiring, not copying** — the nodes never move.
> 2. **The four-beat dance:** save next, flip arrow, slide prev, slide curr.
> 3. **`prev` starts at `null` and ends as the new head.**
>
> Memory peg: **"prev, curr, next — flip and slide."** When you see any linked-list reversal, your hand should already be typing those three pointers.

---

## 14. CLIFFHANGER — `9:00`
*(open loop to next lesson)*

**[VISUAL: `1 → 2 → 3 → 4 → 5` with only the middle `2 → 3 → 4` highlighted and flipping, while `1` and `5` stay put — then a red flash on the two spots where the reversed chunk must reconnect.]**

> Reversing the *whole* list is easy now. But what if the interviewer says "reverse only positions two through four, and leave the rest attached"?
>
> Now the hard part isn't the flip — it's *stitching the reversed piece back in* without dropping half the list. And there's one tiny trick — a dummy node — that makes the ugliest edge case disappear. That's the next video. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode nxt = curr.next;
        curr.next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}
```

**Recursive variant** (the follow-up — elegant, but O(n) stack):

```java
public ListNode reverseListRecursive(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode newHead = reverseListRecursive(head.next);
    head.next.next = head;   // the node after me now points back to me
    head.next = null;        // I become the new tail
    return newHead;
}
```
