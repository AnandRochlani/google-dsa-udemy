# Reverse Linked List

> **LeetCode:** 206. Reverse Linked List · **Difficulty:** 🟢 Easy · **Pattern:** In-Place Linked-List Reversal · **Google frequency:** ⭐ high

---

## Problem

Given the `head` of a singly linked list, reverse it and return the new head.

**Example:** `1 → 2 → 3 → 4 → 5 → null` → `5 → 4 → 3 → 2 → 1 → null`.

An empty list (`head = null`) returns `null`.

**Constraints that matter:** up to `5000` nodes, and the follow-up asks you to do it **both iteratively and recursively**. The iterative version is the O(1)-space workhorse and the foundation for every harder reversal problem (92, 25, 143), so it's worth owning cold.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "Reversed order means last-in-first-out — I'll dump the values into an array (or stack), then rebuild the list backwards." Copy all node values out, then write them back in reverse. It works and it's easy to picture.
- **Where it hurts:** you allocate an **O(n) array** just to flip pointers you already have. The list *already* holds every node — the only thing wrong is which direction each `next` points. So why copy anything? Just **turn the arrows around**.
- **The leap:** walk the list once and, at each node, point its `next` **backward** to the node you just came from. To do that safely you need three references: `prev` (the node behind you, where `next` should now point), `curr` (the node you're rewiring), and a saved `nxt` (so you don't lose the rest of the list the instant you overwrite `curr.next`). Slide all three forward, one node at a time.
- **Pattern trigger:** **"reverse / rewire a linked list in place"** → the **prev / curr / next three-pointer dance**. This is the atom that problems 92, 25, and 143 are all built from.

---

## ① Brute Force

Copy every value into an array, then reassign the values back in reverse order.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list_bruteforce(head):
    vals = []
    node = head
    while node:
        vals.append(node.val)
        node = node.next
    node = head
    for v in reversed(vals):     # overwrite values in reverse
        node.val = v
        node = node.next
    return head
```

**Why it's the natural first attempt:** "reverse" screams "collect everything, flip the order," and an array makes that concrete.

**Why it's not enough:** it uses **O(n) extra space** to store values you already have in the list. You're rewriting `val` fields when the real fix is just re-pointing `next`.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

Iteratively re-point each node's `next` to its predecessor, sliding `prev`/`curr` forward.

```python
def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next     # 1. save the rest of the list
        curr.next = prev    # 2. flip this arrow backward
        prev = curr         # 3. advance prev
        curr = nxt          # 4. advance curr
    return prev             # prev is the new head
```

**Walk `1 → 2 → 3 → null`:**

| step | prev | curr | nxt | after `curr.next = prev` |
|---|---|---|---|---|
| start | null | 1 | — | — |
| 1 | 1 | 2 | 2 | `1 → null` |
| 2 | 2 | 3 | 3 | `2 → 1` |
| 3 | 3 | null | null | `3 → 2` |

`curr` is null → stop, return `prev` = node `3`. Result: `3 → 2 → 1 → null` ✅.

**Why it's correct:** the invariant is "everything from `prev` backward is already reversed; everything from `curr` forward is still original." Each iteration moves exactly one node from the front of the untouched part to the front of the reversed part, and saving `nxt` first means we never lose the untouched remainder.

**Complexity:** Time `O(n)`, Space `O(1)`.

**Recursive variant** (the follow-up) — reverse the tail, then hook the current node onto its end:

```python
def reverse_list_recursive(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head   # the node after me now points back to me
    head.next = None        # I become the new tail
    return new_head
```

It's elegant but uses **O(n) stack space**, so the iterative version is preferred when space matters.

---

## ③ Space Optimization

The iterative solution *is* the space win:

- **Array of values:** O(n) time, **O(n) space**.
- **Recursive:** O(n) time, **O(n) space** (call stack).
- **Iterative three-pointer:** O(n) time, **O(1) space** — three references, nothing that grows with `n`.

The key realisation: reversing a linked list is a **pointer-rewiring** problem, not a data-copying one. The nodes stay put; only the arrows change. That's what makes O(1) space possible.

> *"I don't need to copy anything — I'll flip each `next` in place with prev/curr pointers. O(1) space, versus O(n) for an array or the recursion stack."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (value array) | O(n) | O(n) |
| Recursive | O(n) | O(n) stack |
| Optimised (iterative in-place) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"I could copy the values into an array and write them back reversed, but that's O(n) space for pointers I already have. Instead I reverse in place: walk the list keeping prev, curr, and a saved next, and at each node flip curr.next to point at prev, then slide both forward. When curr hits null, prev is the new head. O(n) time, O(1) space. Recursively it's clean too but costs O(n) stack, so I'd default to iterative."*

## Related / follow-ups
- **Reverse Linked List II** (reverse only a sublist between two positions)
- **Reverse Nodes in k-Group** (reverse in chunks of k)
- **Reorder List** (reverse the second half, then interleave)
- **Palindrome Linked List** (reverse half and compare)
