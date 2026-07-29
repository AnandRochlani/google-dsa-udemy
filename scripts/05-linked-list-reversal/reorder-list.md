# 🎬 Recording Script — Reorder List
**Pattern: In-Place Linked-List Reversal · LeetCode 143 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Middle of the Linked List (876) — fast/slow — and Reverse Linked List (206) — the flip dance.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: `1 → 2 → 3 → 4 → 5` rearranging into `1 → 5 → 2 → 4 → 3` — arcs jumping front, back, front, back. Then a red X over an attempt to walk *backward* through the singly linked list.]**

> Reorder a list so it weaves front and back together: first node, last node, second, second-last, and so on. `1 → 2 → 3 → 4 → 5` becomes `1 → 5 → 2 → 4 → 3`.
>
> In an array this is a trivial two-pointer walk from both ends. But this is a *singly* linked list — you **can't walk backward.** That one limitation is the whole puzzle. And the fix is beautiful: it's three problems you already solved, stacked. By the end you'll do it in O(1) space. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence: "Reorder in place to L₀ → Lₙ → L₁ → Lₙ₋₁ → … (values fixed, pointers only)." Below: `1 → 2 → 3 → 4` → `1 → 4 → 2 → 3`; `1 → 2 → 3 → 4 → 5` → `1 → 5 → 2 → 4 → 3`.]**

> The problem in one line: **reweave the list as front, back, front, back — in place, rewiring pointers only, not values.**
>
> Even list `1 → 2 → 3 → 4` → `1 → 4 → 2 → 3`. Odd list `1 → 2 → 3 → 4 → 5` → `1 → 5 → 2 → 4 → 3`.
>
> We'll trace the odd, five-node case by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: `1 → 2 → 3 → 4 → 5`. All five node references dropped into an array. Two indices `left=0`, `right=4` walk inward, relinking 1→5→2→4→3.]**

> The pattern *screams* two pointers from both ends. So the easy version: dump every node into an array, then walk `left` from the front and `right` from the back, relinking `left → right → left+1 → right−1 → …`.
>
> `left=0`, `right=4`: link `1 → 5`. Move in. Link `5 → 2`. `2 → 4`. `4 → 3`. Terminate at `3`.
>
> **[VISUAL: result `1 → 5 → 2 → 4 → 3`, the array of 5 node refs highlighted.]**
>
> It works perfectly. The array gave us random access — we could grab the *last* node instantly. But that array is the whole cost.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The array of node references, memory-meter at O(n). A red arrow tries to go from node 4 back to node 3 and fails — caption "singly linked: no backward pointer". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** That array is **O(n) extra space**, and the interviewer's "in place" is a direct challenge to it. But *why* did we even want the array? For one reason only: to reach the *back* of the list. A singly linked list has no backward pointer — you physically can't walk from `4` to `3`.
>
> **LEARNER:** Right, that's exactly the wall. The whole reorder needs me to pull nodes from the back, and the back is unreachable going forward. Without the array, how do I ever get at the tail end in the right order?
>
> **TEACHER:** Beautiful framing — the obstacle is *purely* "I can't go backward." Pause and predict: **if the problem is that the back half runs the wrong way for me, what could I do to the back half so it runs the *right* way — forward?**

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: three panels. (1) fast/slow finds the middle and splits: `1 → 2 → 3` | `4 → 5`. (2) reverse the second half: `4 → 5` becomes `5 → 4`. (3) merge alternately: 1,5,2,4,3.]**

> Here's the leap: **if walking the back half backward is the problem, reverse the back half so walking it *forward* gives you back-to-front order.** Then it's just two forward lists to zip together. And every piece is something you already own.
>
> **Step one — find the middle** with the fast/slow pointers from last chapter, and cut the list in two: `1 → 2 → 3` and `4 → 5`.
>
> **Step two — reverse the second half** in place with the prev/curr/next dance: `4 → 5` becomes `5 → 4`. Now its nodes come out *last-to-first* as you walk forward — exactly the order the reorder wants from the back.
>
> **Step three — merge alternately**: take one from the front half, one from the reversed back half, repeat. `1`, then `5`, then `2`, then `4`, then `3`.
>
> **[VISUAL: the merge zipping: 1 → 5 → 2 → 4 → 3.]**
>
> "Front, back, front, back" just became "front-half node, reversed-back-half node, repeat" — all forward traversal, no array. Three easy sub-problems stacked into one Medium.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed three-word line: "Middle → Reverse → Merge."]**

> Three words, in order: **middle, reverse, merge.** Find the midpoint, flip the back half so it runs forward, then zip the two halves together alternately.
>
> Recognising a hard reorder as three easy problems is the transferable skill.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor, `class ListNode` assumed. Type chunk 1 — guard + middle.]**

> Guard the tiny cases, then find the middle with fast/slow.

```python
def reorder_list(head):
    if not head or not head.next:
        return

    # 1. find the middle (slow ends at the first-half tail)
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
```

> **[VISUAL: add chunk 2 — cut + reverse.]** Cut the list into two halves, then reverse the second half with the dance.

```python
    # 2. reverse the second half
    second = slow.next
    slow.next = None            # cut the list into two halves
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    second = prev               # head of the reversed second half
```

> **[VISUAL: add chunk 3 — the alternating merge.]** Merge: interleave one node from each half.

```python
    # 3. merge the two halves alternately
    first = head
    while second:
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each phase. An inset shows the merge stopping cleanly because `second` is the shorter/equal half.]**

> Why each phase.
>
> **Middle:** `while fast.next and fast.next.next` — note this is the "first middle" variant. For `1 → 2 → 3 → 4 → 5`, slow stops on `3`, so the first half is `1 → 2 → 3` and the second is `4 → 5`. That split makes the first half equal-length or one *longer* — which is exactly what "front, back, front, back" needs for both parities.
>
> **Reverse:** `slow.next = None` is the cut — without it the two halves stay tangled and you'd build a cycle. Then it's problem 206, verbatim, on the second half. `second = prev` grabs the reversed head.
>
> **LEARNER:** In the merge, `second` is the *shorter* half. Why loop `while second` and not `while first`? Won't we drop the last front node?
>
> **TEACHER:** That's the exact reason we loop on `second`. Because the first half is equal or one longer, `second` runs out first — or at the same time. When `second` becomes `None`, the front half's leftover node is *already* linked in from the previous step and still correctly points at what follows or at `None`. Looping on `second` stops us at precisely the right moment; looping on `first` would take one step too many and try to splice a node that isn't there.

---

## 9. DRY-RUN THE CODE — `8:30`
*(worked example — prove it, close the loop)*

**[VISUAL: `1 → 2 → 3 → 4 → 5`, three-phase snapshots.]**

> Run all three phases on `1 → 2 → 3 → 4 → 5`.
>
> **Middle:** slow stops on `3`. Cut → first half `1 → 2 → 3`, second half `4 → 5`.
>
> **Reverse second half:** `4 → 5` becomes `5 → 4`. `second` = node `5`.
>
> **Merge** `1 → 2 → 3` with `5 → 4`:

| take from first | splice from second | list so far |
|---|---|---|
| 1 | 5 | `1 → 5 → 2 → 3` |
| 2 | 4 | `1 → 5 → 2 → 4 → 3` → `second` is `None` → stop |

> Result: `1 → 5 → 2 → 4 → 3` ✅. And the even case `1 → 2 → 3 → 4`: halves `1 → 2` and reversed `4 → 3`, merge → `1 → 4 → 2 → 3` ✅. Loop closed on both parities.

---

## 10. COMPLEXITY, OUT LOUD — `9:40`
*(transfer to interview)*

**[VISUAL: two rows — Node array: O(n) time, O(n) space. Middle+reverse+merge: O(n) time, O(1) space.]**

> Say it out loud: *"The array approach is O(n) time, O(n) space. The three-phase in-place approach is also O(n) time — each phase is a single linear pass — but **O(1) space**, just a handful of pointers across all three."*
>
> Same time, and we deleted the array entirely. That's the interview answer.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:15`
*(depth + honesty — make the space beat shine)*

**[VISUAL: the node array (O(n)) crossed out; a few pointer arrows labelled O(1). Each of the three phases tagged "O(1)".]**

> This is why 143 is a favourite interview problem, so let it land.
>
> The elegant realisation: the array existed for *one job only* — to fake backward traversal so we could reach the tail. Reverse the second half in place and that job disappears — now you walk the back half *forward* during the merge. No array needed.
>
> And each phase is independently O(1): fast/slow midpoint is two pointers, the reversal is three, the merge is a few. Stack three constant-space passes and the whole thing is constant space. Say it in the room: *"The array was only there to walk the back half backward. Reverse it in place instead, and I can merge forward — O(1) space. It's three sub-problems I already know: middle, reverse, merge."* Decomposing a hard problem into owned pieces is the senior signal.

---

## 12. YOUR TURN (active recall) — `10:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Palindrome Linked List (LC 234)". A blank editor.]**

> Before the next video, try **Palindrome Linked List**. Same decomposition: find the middle, reverse the second half — then instead of merging, you *compare* the two halves node by node. If they match, it's a palindrome.
>
> Try it first. Reusing "middle + reverse-half" for a totally different goal is what proves you own the pattern, not just this problem.

---

## 13. LOCK IT IN — `11:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **The array only ever faked backward traversal** — reverse the back half and it's unnecessary.
> 2. **Decompose:** middle (fast/slow) + reverse (206) + alternating merge.
> 3. **Cut with `slow.next = None`, and loop the merge on the shorter half (`second`).**
>
> Memory peg: **"Middle, reverse, merge."** When a singly linked list needs its back half, don't reach for an array — flip the back half so it runs forward.

---

## 14. CLIFFHANGER — `12:05`
*(open loop to next lesson)*

**[VISUAL: a grid/matrix and a tree fading in behind a linked list, with pointer-arrows generalising into edges.]**

> Look what just happened: two entire chapters — fast/slow pointers and in-place reversal — collapsed into *one* problem, because you could see the sub-patterns inside it. That's the real skill: not memorising a hundred problems, but recognising the handful of moves they're built from.
>
> Next chapter, we take pointers off the straight line and into branching structures — trees and graphs — where "which way do I go?" becomes the whole game. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public void reorderList(ListNode head) {
    if (head == null || head.next == null) return;

    // 1. find the middle
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    // 2. reverse the second half
    ListNode second = slow.next, prev = null;
    slow.next = null;
    while (second != null) {
        ListNode nxt = second.next;
        second.next = prev;
        prev = second;
        second = nxt;
    }
    second = prev;

    // 3. merge alternately
    ListNode first = head;
    while (second != null) {
        ListNode f = first.next, s = second.next;
        first.next = second;
        second.next = f;
        first = f;
        second = s;
    }
}
```
