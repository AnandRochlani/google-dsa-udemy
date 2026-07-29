# Reverse Nodes in k-Group

> **LeetCode:** 25. Reverse Nodes in k-Group · **Difficulty:** 🔴 Hard · **Pattern:** In-Place Linked-List Reversal · **Google frequency:** ⭐ high

---

## Problem

Given the `head` of a linked list, reverse the nodes **`k` at a time** and return the modified list. If the number of nodes isn't a multiple of `k`, the **leftover nodes at the end stay in their original order**. You may not alter the node values — only rewire pointers.

**Example:** `1 → 2 → 3 → 4 → 5`, `k = 2` → `2 → 1 → 4 → 3 → 5` *(pairs flip; the lone `5` is left alone).*
Same list with `k = 3` → `3 → 2 → 1 → 4 → 5` *(first triple flips; `4 → 5` is too short, left alone).*

**Constraints that matter:** up to `5000` nodes, `1 ≤ k ≤ n`, and the O(1)-space follow-up. Two things make this Hard: you must **check each group is full *before* reversing it** (so you don't accidentally reverse a short tail), and you must **stitch consecutive reversed groups together** correctly.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "I'll chop the list into chunks of `k`, reverse each chunk (I know how — problem 206), and glue them back together." The most literal version pushes each group's nodes onto a stack (or into an array), pops them reversed, and relinks. It works.
- **Where it hurts:** the stack is **O(k) extra space** per group, and you still have to solve the genuinely hard parts by hand: (a) detecting when a group is *incomplete* so you leave it untouched, and (b) connecting the **tail of one reversed group to the head of the next** — which you can't do until you've reversed the next group, because its head is the next group's *old* tail.
- **The leap:** do it in place. For each group, first **walk `k` nodes ahead to confirm the group is full** (if you run off the end, stop — leave the rest as-is). Then reverse exactly those `k` nodes with the standard prev/curr/next dance. The crucial bookkeeping: the node that was the group's **head becomes its tail**, and that tail must point to the head of the *next* reversed group. Track the previous group's tail (`group_prev`) and rewire on each pass.
- **Pattern trigger:** **"reverse in fixed-size blocks, keep the remainder"** → **in-place reversal of a bounded window + careful group-boundary stitching**. It's problem 92 generalised to repeat across the whole list.

---

## ① Brute Force

Collect each group of `k` nodes onto a stack; pop them to build the reversed order. Handle short tails by not reversing them.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_k_group_bruteforce(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    node = head
    while True:
        # gather up to k nodes
        stack, count, probe = [], 0, node
        while probe and count < k:
            stack.append(probe)
            probe = probe.next
            count += 1
        if count < k:                 # incomplete tail → leave as is
            group_prev.next = node
            break
        # relink group in reversed order
        while stack:
            group_prev.next = stack.pop()
            group_prev = group_prev.next
        group_prev.next = probe        # temporarily point past the group
        node = probe                   # advance to next group
    return dummy.next
```

**Why it's the natural first attempt:** a stack is the textbook "reverse order" structure, and it keeps the group-boundary logic relatively readable.

**Why it's not enough:** it holds up to `k` node references on the stack → **O(k) space**. The follow-up wants O(1), and the in-place version is what signals mastery on a Hard problem.

**Complexity:** Time `O(n)`, Space `O(k)`.

---

## ② Optimised Solution

In place: for each group, verify `k` nodes exist, reverse them with three pointers, then reconnect the boundaries. A dummy node anchors the head.

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

        group_next = kth.next          # first node of the NEXT group
        # 2. reverse the current group [group_prev.next .. kth]
        prev, curr = group_next, group_prev.next
        while curr is not group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        # 3. reconnect: old head (now tail) is group_prev.next; new head is kth
        tail = group_prev.next         # this node is now the group's tail
        group_prev.next = kth          # previous group points to new head
        group_prev = tail              # tail becomes anchor for the next group
```

**Walk `1 → 2 → 3 → 4 → 5`, `k = 2`:**

- **Group 1:** `group_prev = dummy`. `kth` = node `2` (2 hops). `group_next = 3`. Reverse `1 → 2` seeding `prev = 3`: get `2 → 1 → 3`. Reconnect: `dummy → 2`, and `tail` = node `1` becomes `group_prev`. List so far: `2 → 1 → 3 → 4 → 5`.
- **Group 2:** `group_prev = 1`. `kth` = node `4`. `group_next = 5`. Reverse `3 → 4` seeding `prev = 5`: get `4 → 3 → 5`. Reconnect: `1 → 4`, `group_prev` = node `3`. List: `2 → 1 → 4 → 3 → 5`.
- **Group 3:** from `group_prev = 3`, only node `5` remains — the `for` loop hits `None` before `k` hops → **return** `dummy.next`.

Result: `2 → 1 → 4 → 3 → 5` ✅.

**Why it's correct:** the "count `k` first" step guarantees we never reverse a partial group, satisfying the leftover rule. Seeding `prev = group_next` before reversing makes the group's old head automatically point at the next group, so the "after" join is free. Setting `group_prev.next = kth` fixes the "before" join, and advancing `group_prev = tail` sets up the next iteration.

**Complexity:** Time `O(n)` (each node is visited a constant number of times), Space `O(1)`.

---

## ③ Space Optimization

The in-place solution is the space payoff, and on a Hard problem it's the difference-maker:

- **Stack per group:** O(n) time, **O(k) space**.
- **Recursive** (reverse first group, recurse on the rest): O(n) time, **O(n/k) stack space**.
- **Iterative in-place:** O(n) time, **O(1) space** — a fixed set of pointers regardless of `k` or `n`.

The recurring lesson from this whole pattern holds: reversal is **pointer surgery**, so no auxiliary structure is required — you just need enough anchors (`group_prev`, `kth`, `group_next`, `tail`) to stitch the boundaries.

> *"I reverse each k-block in place with the standard three-pointer loop, but first I walk k nodes ahead to confirm the group is full — that's how the short tail is left alone. Seeding prev with the next group's head makes the boundary joins fall out automatically. O(1) space."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (stack per group) | O(n) | O(k) |
| Recursive | O(n) | O(n/k) stack |
| Optimised (iterative in-place) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"For each group I first walk k nodes ahead to check a full group exists — if not, I stop and leave the remainder in order, which is the rule for leftovers. If it's full, I reverse those k nodes in place with prev/curr/next, seeding prev with the next group's first node so the trailing join comes for free. Then I hook the previous group's tail to the new head and advance my anchor to the old head, which is now this group's tail. Every node is touched a constant number of times, so O(n) time, O(1) space."*

## Related / follow-ups
- **Reverse Linked List** (the k = n / single-group base case)
- **Reverse Linked List II** (reverse one bounded window — the sub-skill this repeats)
- **Swap Nodes in Pairs** (this exact problem with k = 2)
- **Rotate List** (more linked-list pointer surgery)
