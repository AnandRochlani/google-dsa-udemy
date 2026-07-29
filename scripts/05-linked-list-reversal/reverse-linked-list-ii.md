# 🎬 Recording Script — Reverse Linked List II (Reverse a Sublist)
**Pattern: In-Place Linked-List Reversal · LeetCode 92 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Reverse Linked List (206) — the prev/curr/next flip-and-slide dance.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: `1 → 2 → 3 → 4 → 5`. Positions 2 through 4 highlighted. The chunk `2 → 3 → 4` flips to `4 → 3 → 2`, and the ends snap back on: `1 → 4 → 3 → 2 → 5`. Then a red X flashes over a version where `1` got dropped.]**

> You know how to reverse a whole list. Now the interviewer narrows it: *"Reverse only positions two through four. Leave everything else exactly where it is."*
>
> The flip itself is last lesson's dance. The trap is the **stitching** — the node before the chunk has to reconnect to the new front, and the old front has to reconnect to what came after. Get one join wrong and you drop half the list or make a cycle.
>
> By the end you'll do it in one pass, O(1) space, with a tiny dummy-node trick that erases the nastiest edge case. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence: "Reverse nodes from position left to right, in place, one pass." Below: `1 → 2 → 3 → 4 → 5`, left=2, right=4, result `1 → 4 → 3 → 2 → 5`.]**

> The problem in one line: **reverse just the nodes from position `left` to position `right` — one-indexed — and reattach the ends.**
>
> Tiny example: `1 → 2 → 3 → 4 → 5`, `left = 2`, `right = 4`. Only `2 → 3 → 4` flips, into `4 → 3 → 2`. Result: `1 → 4 → 3 → 2 → 5`. The `1` and the `5` never move — they just point to new neighbours.
>
> Hold that target: `1 → 4 → 3 → 2 → 5`.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: walk to position 2, collect [2, 3, 4] into an array, reverse to [4, 3, 2], write values back into the same three nodes.]**

> The obvious reuse: "I can reverse an array." So walk to position `left`, copy the sublist's *values* into an array — `[2, 3, 4]` — reverse it to `[4, 3, 2]`, then write those back into the three nodes.
>
> **[VISUAL: nodes 2,3,4 now read 4,3,2; arrows untouched. Result reads 1 → 4 → 3 → 2 → 5.]**
>
> It works, and it sidesteps all the scary pointer surgery by only touching `val` fields. But it cost us an array the size of the sublist — and it quietly assumes we're *allowed* to overwrite values.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The array highlighted (O(k) space). Then a variant where nodes carry identity/objects — the value-swap trick breaks with a red X. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Two problems. One: that array is **O(k) extra space.** Two, and worse: it only works because we cheated and rewrote values. In a variant where nodes carry identity — or the interviewer says "don't touch the values" — this collapses. They want *pointer* surgery.
>
> **LEARNER:** But pointer surgery is exactly what scares me here. The node *before* position two has to end up pointing at `4`, and the old node `2` has to end up pointing at `5`. Those are two separate joins on opposite ends of the chunk. How do I keep both straight?
>
> **TEACHER:** That *is* the whole problem — the two boundary joins. Pause and predict: **is there a way to reverse the chunk so that both joins happen automatically, instead of me hunting for them afterward?**

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: anchors placed — `prev` on node 1 (just before left), `curr` on node 2 (first of the sublist). Then repeated "plucking": grab the node after curr, lift it to the front of the reversed section, right behind prev.]**

> Don't extract anything. Reverse in place — but with a smarter move called **head-insertion**, and two anchors pinned down first.
>
> Pin **`prev`** on the node *just before* `left` — that's node `1`. Pin **`curr`** on the first node of the sublist — node `2`. Here's the key insight: **`curr` never moves. It's going to end up as the *tail* of the reversed chunk**, so we just leave it there and let everything slide past it.
>
> Now repeatedly *pluck*: take the node right after `curr`, unhook it, and splice it to the very front of the reversed part — right behind `prev`.
>
> **[VISUAL: trace on `1 → 2 → 3 → 4 → 5`, left=2, right=4:
> Pluck 1: grab 3, unlink → 2→4, insert 3 behind prev → 1 → 3 → 2 → 4 → 5.
> Pluck 2: grab 4, unlink → 2→5, insert 4 behind prev → 1 → 4 → 3 → 2 → 5.]**
>
> Because `prev` sits *outside* the chunk, the "front" join is always correct. Because `curr` trails as the pinned tail, its `next` keeps pointing at the untouched remainder — the "back" join stays correct for free. Both joins, automatic. That's the aha the learner was asking for.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Pin prev before the chunk & curr as the tail. Pluck the node after curr to the front — repeat (right − left) times."]**

> One line: **pin the node before the sublist and the sublist's first node; then keep plucking the node after `curr` to the front.** Do that `right − left` times and the chunk is reversed, joins included.
>
> The plucking — head-insertion — is the transferable move.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor, `class ListNode` assumed. Type chunk 1 — the dummy + walk.]**

> First, a **dummy node** in front of the head, and walk `prev` to just before `left`.

```python
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):     # prev = node just before `left`
        prev = prev.next
```

> **[VISUAL: add chunk 2 — pin curr.]** Pin `curr` on the first node of the sublist. It becomes the tail and stays put.

```python
    curr = prev.next              # curr = first sublist node (its future tail)
```

> **[VISUAL: add chunk 3 — the pluck loop, highlight the three re-wires.]** Now pluck `right − left` times: unlink the node after `curr`, and splice it behind `prev`.

```python
    for _ in range(right - left):
        nxt = curr.next           # node to pull to the front
        curr.next = nxt.next      # unlink nxt from its spot
        nxt.next = prev.next      # nxt points to current front of reversed part
        prev.next = nxt           # prev now points at nxt (new front)
    return dummy.next
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line, and a small inset showing the left=1 case with and without the dummy.]**

> Why each piece.
>
> The three re-wire lines are one atomic pluck: **`curr.next = nxt.next`** unhooks `nxt` from its current spot; **`nxt.next = prev.next`** points `nxt` at the current front of the reversed section; **`prev.next = nxt`** makes `nxt` the new front. Order matters — same discipline as last lesson.
>
> The loop runs `right − left` times, not `right − left + 1`, because the first sublist node (`curr`) is already in place as the tail — we only need to move the *other* `k−1` nodes in front of it.
>
> **LEARNER:** Why the dummy node? On the full-reverse problem we didn't need one.
>
> **TEACHER:** Because of `left = 1`. If we reverse starting at the very first node, there *is* no "node before the sublist" — `prev` would have nothing to point to, and every join would need a special case. The dummy is a fake node glued in front of the head, so there's *always* a real node before position one. `prev` starts on the dummy, the code stays one uniform loop, and we `return dummy.next` — whatever the head ended up being. One tiny node erases the whole edge case.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: `dummy → 1 → 2 → 3 → 4 → 5`, left=2, right=4. Step-by-step list snapshots.]**

> Run it. `left = 2`, `right = 4`, so `right − left = 2` plucks. `prev` walks to node `1`; `curr` pins on node `2`.

| pluck | nxt | after unlink (`curr.next=nxt.next`) | after splice | list now |
|---|---|---|---|---|
| 1 | 3 | `2 → 4` | `3` behind prev | `1 → 3 → 2 → 4 → 5` |
| 2 | 4 | `2 → 5` | `4` behind prev | `1 → 4 → 3 → 2 → 5` |

> Two plucks, done. `return dummy.next` → `1 → 4 → 3 → 2 → 5`. Exactly the target. And notice `curr` (node `2`) never moved — it just ended up the tail of the flipped chunk, still pointing at `5`. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Value array: O(n) time, O(k) space. In-place: O(n) time, O(1) space.]**

> Say it out loud: *"The value-copy approach is O(n) time but O(k) space and needs to mutate values. The in-place head-insertion is one pass, O(n) time, **O(1) space**, and only rewires pointers."*
>
> One pass, constant space, no value mutation — that's the answer they're after.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty — make the space beat shine)*

**[VISUAL: the array (O(k)) crossed out; a handful of pointer arrows labelled O(1). The dummy node glowing beside "kills the left=1 edge case".]**

> This is why 92 is harder than 206, so let it land. Two ideas make O(1) possible.
>
> **One:** reversing is pointer-rewiring, not copying — the same lesson as last video. No array needed; we pluck and splice the actual nodes.
>
> **Two:** the **dummy node** removes the "what's before position one?" edge case, so a single uniform loop handles *every* input — including `left = 1` — without branching. That's not just a space trick; it's a correctness trick that keeps the code clean enough to *be* O(1).
>
> Say it in the room: *"I reverse the sublist in place by plucking the node after the head to the front, and a dummy node handles left equals one. One pass, O(1) space."* Naming *why* the dummy earns its keep is the senior move.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Swap Nodes in Pairs (LC 24)". A blank editor.]**

> Before the next video, try **Swap Nodes in Pairs** — reverse every *adjacent pair*. It's this exact head-insertion idea with the window fixed at size two, repeated down the list. A dummy node makes it clean.
>
> Try it first. Feeling the pluck-and-splice on a tiny window is what preps you for the Hard one.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **The first sublist node is the pinned tail** — leave `curr` still, slide everything past it.
> 2. **Head-insertion (plucking) reverses in place** and makes both boundary joins automatic.
> 3. **A dummy node kills the `left = 1` edge case** — always a real node before position one.
>
> Memory peg: **"Pin the tail, pluck to the front."** When you reverse a *slice* of a list, that's the whole move.

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: `1 → 2 → 3 → 4 → 5 → 6 → 7` chopped into groups of 3: `[1 2 3][4 5 6][7]`, each full group flipping, the lone `7` left alone.]**

> We just reversed *one* slice. What if the interviewer wants the list reversed in *chunks* — every three nodes flipped, again and again, with any short leftover left untouched?
>
> Now you're stitching group after group together, and you have to check each group is *full* before you dare reverse it. That's Reverse Nodes in k-Group — the Hard boss of this chapter. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

public ListNode reverseBetween(ListNode head, int left, int right) {
    ListNode dummy = new ListNode(0, head);
    ListNode prev = dummy;
    for (int i = 0; i < left - 1; i++) prev = prev.next;

    ListNode curr = prev.next;
    for (int i = 0; i < right - left; i++) {
        ListNode nxt = curr.next;
        curr.next = nxt.next;
        nxt.next = prev.next;
        prev.next = nxt;
    }
    return dummy.next;
}
```
