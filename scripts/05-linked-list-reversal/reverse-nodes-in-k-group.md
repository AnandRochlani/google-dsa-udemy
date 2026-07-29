# 🎬 Recording Script — Reverse Nodes in k-Group
**Pattern: In-Place Linked-List Reversal · LeetCode 25 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Reverse Linked List (206) and Reverse Linked List II (92) — the flip dance and boundary stitching.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: `1 → 2 → 3 → 4 → 5`, k=2. Pairs flip: `2 → 1 → 4 → 3 → 5`. The lone `5` stays. Then a red "TLE / cycle" flash over a botched version where a group boundary got mis-joined.]**

> This is the Hard one — but it's not hard because the flip is hard. You already own the flip. It's hard for two brutal little reasons: you have to reverse the list in *chunks* of `k`, gluing each reversed chunk to the next, and you must **not** reverse a leftover chunk that's too short.
>
> `1 → 2 → 3 → 4 → 5` with `k = 2` becomes `2 → 1 → 4 → 3 → 5` — the lone `5` is left alone. By the end you'll do this in O(1) space, and the group-boundary bookkeeping will feel mechanical instead of terrifying. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence: "Reverse the list k nodes at a time; leftover shorter than k stays as-is." Below: k=2 → `2 → 1 → 4 → 3 → 5`; k=3 → `3 → 2 → 1 → 4 → 5`.]**

> The problem in one line: **reverse the list `k` nodes at a time; if the last chunk is shorter than `k`, leave it in original order.** And you may only rewire pointers — no touching values.
>
> Same list, `k = 2` → `2 → 1 → 4 → 3 → 5`. With `k = 3` → `3 → 2 → 1 → 4 → 5`: the first triple flips, but `4 → 5` is too short, so it stays.
>
> We'll trace the `k = 2` case by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: `1 → 2 → 3 → 4 → 5`, k=2. First group pushed onto a stack [1,2], popped as 2,1 and relinked. Then [3,4] → 4,3. Then just [5] — too short, left as-is.]**

> The literal approach: chop into chunks, reverse each, glue back. And the textbook "reverse order" tool is a **stack**.
>
> Push the first `k` nodes onto a stack — `[1, 2]`. Pop them off: `2`, then `1` — that's the reversed group, relink it. Next chunk `[3, 4]` → pop `4`, `3`. Last chunk: only `[5]` left. It's shorter than `k`, so *don't* reverse it — leave it.
>
> **[VISUAL: result `2 → 1 → 4 → 3 → 5`, with a stack of up to k nodes highlighted each round.]**
>
> It works, and honestly the stack keeps the group logic readable. But look what it costs each round.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The stack holding up to k node references, memory-meter at O(k). Two red trouble-spots labelled "(a) detect a short group" and "(b) join group-to-group". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The stack holds up to `k` node references every round — **O(k) extra space** — and the follow-up wants O(1). But even with the stack, you *still* have to solve the two genuinely hard parts by hand: **(a)** detecting when a group is too short so you leave it alone, and **(b)** connecting the tail of one reversed group to the head of the *next*.
>
> **LEARNER:** That second one melts my brain. To join group one to group two, I need group two's new head — but I don't *know* its head until I've reversed group two. It's a chicken-and-egg. How do I connect them in the right order?
>
> **TEACHER:** That is *the* question on this problem. Pause and predict two things: **how do you check a group is full *before* you touch it — and is there a way to make the group-to-group join fall out automatically, the way the dummy did last lesson?**

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: for one group — first, a "scout" pointer walks k nodes ahead to confirm the group is full. Then the standard prev/curr/next flip, but seeded with prev = the next group's first node. Anchors labelled: group_prev, kth, group_next, tail.]**

> Two moves crack it. Take them one at a time.
>
> **Move one — scout before you flip.** Before reversing a group, walk a pointer `k` nodes ahead. If it runs off the end before reaching `k`, the group is short — **stop, leave the rest untouched.** That single check enforces the leftover rule. No reversing a partial group by accident.
>
> **Move two — seed the flip so the join is free.** Here's the elegant part that answers the chicken-and-egg. When we reverse a group with the prev/curr/next dance, we normally seed `prev = None`. Instead, seed **`prev = group_next`** — the first node of the *next* group.
>
> **[VISUAL: reversing group `1 → 2` with k=2. group_next = 3. Seed prev=3. Flip: 1→3, then 2→1. Result chunk: 2 → 1 → 3. The "→3" join appeared for free.]**
>
> Watch: because we seeded `prev` with the next group's head, the group's *old head* — which becomes its tail — automatically ends up pointing at the next group. The trailing join writes itself. No chicken-and-egg.
>
> Then just two anchors to finish the leading join: the previous group's tail (`group_prev`) points at the new head (`kth`), and the old head becomes the new `group_prev` for the round after. Four little anchors — `group_prev`, `kth`, `group_next`, `tail` — and the whole thing marches.

---

## 6. THE KEY MOVE (signaling) — `5:10`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed two-line rule: "Scout k ahead — short? stop. Reverse seeding prev = next group's head — trailing join is free. Then group_prev.next = kth."]**

> Two lines to burn in: **scout `k` nodes ahead first — if the group's short, stop.** Then **reverse it, but seed `prev` with the next group's head, so the trailing join comes free — and hook the previous group's tail to the new head.**
>
> Scout, seed, stitch. That's the whole Hard problem.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor, `class ListNode` assumed. Type chunk 1 — dummy + the scout.]**

> Dummy node up front, `group_prev` on it. Then the scout: find the `k`-th node; bail if fewer than `k` remain.

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # 1. find the k-th node from group_prev; bail if fewer than k remain
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next      # incomplete group → leave untouched
```

> **[VISUAL: add chunk 2 — grab group_next, do the seeded flip.]** Grab the first node of the *next* group, then reverse this group seeding `prev` with it.

```python
        group_next = kth.next          # first node of the NEXT group
        # 2. reverse the current group [group_prev.next .. kth]
        prev, curr = group_next, group_prev.next
        while curr is not group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
```

> **[VISUAL: add chunk 3 — the reconnect.]** Now stitch the leading join and advance the anchor for the next round.

```python
        # 3. reconnect: old head (now tail) is group_prev.next; new head is kth
        tail = group_prev.next         # this node is now the group's tail
        group_prev.next = kth          # previous group points to new head
        group_prev = tail              # tail becomes anchor for the next group
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:30`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each block. An inset animates the seeded-prev trick producing the trailing join.]**

> Why each piece — this is where the Hard problem is won.
>
> The **scout loop** — `for _ in range(k)` advancing `kth`, checking `is None` — is move one. If it ever hits `None`, fewer than `k` nodes remain, so we `return dummy.next` immediately and the leftover stays in original order. That's the entire leftover rule, in four lines.
>
> The **reverse loop** looks like problem 206 with one change: `prev` starts at `group_next` instead of `None`, and we stop when `curr is group_next` instead of `None`. That seeding is move two — it's *why* the old head ends up pointing at the next group with no extra code.
>
> **LEARNER:** Wait — after reversing, why is `kth` the new head, and why does `group_prev.next = kth` reconnect the front correctly?
>
> **TEACHER:** Because reversing a chunk swaps its ends. The node that was *last* in the group — `kth` — is now *first*. So the previous group's tail, `group_prev`, must point at `kth`. And the node that was *first* — `group_prev.next` before we touched it, which we saved as `tail` — is now the group's *last* node. That `tail` becomes the next round's `group_prev`, so the following group hooks onto it. Every join is just "old first and old last swapped roles."
>
> **LEARNER:** And there's no `return` at the bottom of the `while True` — is that a bug?
>
> **TEACHER:** No — the *only* way out is the scout hitting `None` and returning `dummy.next`. Every list eventually runs out of full groups, so that return always fires. The loop is intentionally infinite until then.

---

## 9. DRY-RUN THE CODE — `9:15`
*(worked example — prove it, close the loop)*

**[VISUAL: `dummy → 1 → 2 → 3 → 4 → 5`, k=2. Snapshots per group.]**

> Run it on `1 → 2 → 3 → 4 → 5`, `k = 2`.
>
> **Group 1:** `group_prev = dummy`. Scout: `kth` = node `2`. `group_next = 3`. Reverse `1 → 2` seeding `prev = 3`: node `1` flips to point at `3`, node `2` flips to point at `1` → chunk is `2 → 1 → 3`. Reconnect: `dummy → 2`; `tail` = node `1` becomes `group_prev`. List: `2 → 1 → 3 → 4 → 5`.
>
> **Group 2:** `group_prev = 1`. Scout: `kth` = node `4`. `group_next = 5`. Reverse `3 → 4` seeding `prev = 5`: → chunk `4 → 3 → 5`. Reconnect: `1 → 4`; `group_prev` = node `3`. List: `2 → 1 → 4 → 3 → 5`.
>
> **Group 3:** `group_prev = 3`. Scout: only node `5` remains — the `for` loop hits `None` before `k` hops → **return `dummy.next`.**
>
> Result: `2 → 1 → 4 → 3 → 5` ✅. The lone `5` untouched, both group joins clean. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:45`
*(transfer to interview)*

**[VISUAL: three rows — Stack per group: O(n) time, O(k) space. Recursive: O(n) time, O(n/k) stack. Iterative in-place: O(n) time, O(1) space.]**

> Say it out loud: *"Every node is scouted once and reversed once — a constant number of touches — so O(n) time. The stack version is O(k) space, the recursive version is O(n/k) stack, but the iterative in-place version is **O(1) space** — a fixed set of anchors no matter how big `k` or `n` is."*
>
> On a Hard problem, that O(1)-space answer is the difference-maker.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:20`
*(depth + honesty — make the space beat shine)*

**[VISUAL: the per-group stack (O(k)) and the recursion stack (O(n/k)) both crossed out; four labelled anchor pointers — group_prev, kth, group_next, tail — glowing at O(1).]**

> This is the payoff, and on a Hard problem it's what earns the hire. The stack existed only to produce reversed order — but reversal is **pointer surgery**, so it never needed a stack at all. The recursion hides its cost in the call stack, `O(n/k)` frames.
>
> The in-place version carries exactly **four anchors** — `group_prev`, `kth`, `group_next`, `tail` — regardless of `k` or `n`. That's it. O(1) space.
>
> And the elegant reason it's *possible*: seeding `prev` with the next group's head means the trailing join needs no storage — the flip itself writes the connection. Say it in the room: *"I reverse each k-block in place, seeding prev with the next group's head so the boundary join falls out automatically, and I scout k ahead to leave short tails alone. Constant space."* That sentence is a strong-hire signal.

---

## 12. YOUR TURN (active recall) — `12:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Swap Nodes in Pairs (LC 24)". A blank editor.]**

> Before the next video, try **Swap Nodes in Pairs** — this *exact* problem with `k = 2`, hardcoded. Solve it fresh, without the general-`k` machinery, and you'll feel how the group-join and the scout collapse into something small.
>
> Struggle with it first. Re-deriving the join on the simplest case locks the general one in.

---

## 13. LOCK IT IN — `12:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Scout `k` ahead before reversing** — that check *is* the leftover rule.
> 2. **Seed `prev` with the next group's head** — the trailing join writes itself.
> 3. **After a flip, old-last is new-head, old-first is new-tail** — that's every reconnect.
>
> Memory peg: **"Scout, seed, stitch."** Count the group, seed the reversal with the next group's head, stitch the previous tail to the new head. The Hard problem, in three words.

---

## 14. CLIFFHANGER — `13:20`
*(open loop to next lesson)*

**[VISUAL: `1 → 2 → 3 → 4 → 5` morphing into `1 → 5 → 2 → 4 → 3` — front, back, front, back — with a fast/slow pointer finding the middle and the back half flipping.]**

> You've now reversed whole lists, slices, and chunks. The last problem in this chapter combines *everything*: reorder a list to weave front and back together — `first, last, second, second-last`.
>
> The catch? A singly linked list can't walk backward. So you'll find the middle with the fast/slow pointers from the last chapter, reverse the second half with the dance from this one, and merge. Three patterns, one problem. That's Reorder List. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

public ListNode reverseKGroup(ListNode head, int k) {
    ListNode dummy = new ListNode(0, head);
    ListNode groupPrev = dummy;

    while (true) {
        ListNode kth = groupPrev;
        for (int i = 0; i < k && kth != null; i++) kth = kth.next;
        if (kth == null) return dummy.next;   // incomplete group

        ListNode groupNext = kth.next;
        ListNode prev = groupNext, curr = groupPrev.next;
        while (curr != groupNext) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        ListNode tail = groupPrev.next;
        groupPrev.next = kth;
        groupPrev = tail;
    }
}
```
