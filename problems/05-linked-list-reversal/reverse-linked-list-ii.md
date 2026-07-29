# Reverse Linked List II (Reverse a Sublist)

> **LeetCode:** 92. Reverse Linked List II · **Difficulty:** 🟡 Medium · **Pattern:** In-Place Linked-List Reversal · **Google frequency:** ⭐ high

---

## Problem

Given the `head` of a singly linked list and two positions `left` and `right` (1-indexed, `left ≤ right`), reverse the nodes from position `left` to position `right` **in place**, and return the head. Do it in **one pass**.

**Example:** `1 → 2 → 3 → 4 → 5`, `left = 2`, `right = 4` → `1 → 4 → 3 → 2 → 5` *(only the middle chunk `2 → 3 → 4` flips; the ends stay attached).*

`left == right` → the list is unchanged.

**Constraints that matter:** up to `500` nodes, `1 ≤ left ≤ right ≤ n`. The hard part isn't the reversal — it's **stitching the reversed sublist back into the surrounding list correctly**, especially when `left = 1` (no node before the reversed part). A **dummy node** makes that edge case vanish.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "I know how to reverse a whole list (problem 206). So: walk to position `left`, collect the `left..right` nodes (maybe into an array), reverse them, and splice them back." Copying the sublist out works and is easy to reason about.
- **Where it hurts:** the array is **O(k) extra space**, and worse, the *real* difficulty is the surgery: the node **before** `left` must now point to what was position `right`, and the original `left` node must point to what was **after** `right`. Get either stitch wrong and you drop half the list or create a cycle.
- **The leap:** you don't need to extract anything. Reverse the sublist **in place** with the same prev/curr/next dance, but hold onto two anchors first: `prev` = the node just before position `left`, and `curr` = the node at `left` (which will become the *tail* of the reversed chunk). Then repeatedly "pluck the node after `curr` and move it to the front of the reversed section." After `right − left` plucks, everything is rewired — no copying, and the boundary joins happen automatically.
- **Pattern trigger:** **"reverse a *portion* of a linked list, reattach the ends"** → **in-place reversal + a dummy node** to kill the `left = 1` edge case. The head-insertion ("plucking") technique is the transferable move.

---

## ① Brute Force

Copy the sublist values into an array, reverse it, and write them back.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_between_bruteforce(head, left, right):
    node = head
    for _ in range(left - 1):        # walk to position `left`
        node = node.next
    start = node
    vals = []
    for _ in range(right - left + 1):  # collect sublist values
        vals.append(node.val)
        node = node.next
    node = start
    for v in reversed(vals):          # write them back reversed
        node.val = v
        node = node.next
    return head
```

**Why it's the natural first attempt:** it reuses "reverse an array" and sidesteps tricky pointer surgery by only touching `val` fields.

**Why it's not enough:** **O(k) extra space**, and it quietly assumes you can rewrite values — in a variant where nodes carry identity (or you're told not to touch values) it breaks. The pointer solution is the one interviewers want.

**Complexity:** Time `O(n)`, Space `O(k)` where `k = right − left + 1`.

---

## ② Optimised Solution

One pass, in place. Use a dummy node, walk to just before `left`, then head-insert each following node to reverse the chunk.

```python
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):     # prev = node just before `left`
        prev = prev.next

    curr = prev.next              # curr = first node of the sublist (its future tail)
    for _ in range(right - left):
        nxt = curr.next           # node to pull to the front
        curr.next = nxt.next      # unlink nxt from its spot
        nxt.next = prev.next      # nxt points to current front of reversed part
        prev.next = nxt           # prev now points at nxt (new front)
    return dummy.next
```

**Walk `1 → 2 → 3 → 4 → 5`, `left = 2`, `right = 4`:**

- `prev` lands on node `1`; `curr` = node `2` (stays the tail).
- **Pluck 1:** `nxt = 3`. Unlink → `2 → 4`. Insert `3` after `prev`: `1 → 3 → 2 → 4 → 5`.
- **Pluck 2:** `nxt = 4` (it's `curr.next` again). Unlink → `2 → 5`. Insert `4` after `prev`: `1 → 4 → 3 → 2 → 5`.
- Done (`right − left = 2` plucks). Result: `1 → 4 → 3 → 2 → 5` ✅.

**Why it's correct:** `curr` is pinned as the sublist's tail; each iteration takes the node right after `curr` and splices it directly behind `prev`, which is the front of the growing reversed section. Because `prev` sits *outside* the reversed region, the "before" join is always correct, and `curr` trailing behind keeps the "after" join (`curr.next`) pointing at the untouched remainder. The dummy means `left = 1` needs no special case.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

The in-place version is the space win, and it's the whole reason 92 is harder than 206:

- **Value-array approach:** O(n) time, **O(k) space**.
- **In-place head-insertion:** O(n) time, **O(1) space** — a handful of pointers, nothing that scales with the sublist size.

Two ideas make O(1) possible: **(1)** reversing is pointer-rewiring, not copying; **(2)** the **dummy node** removes the "what's before position 1?" edge case so a single uniform loop handles every input.

> *"I reverse the sublist in place by repeatedly plucking the node after the sublist's head and moving it to the front. A dummy node handles left = 1 cleanly. One pass, O(1) space."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (value array) | O(n) | O(k) |
| Optimised (in-place, one pass) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"Reversing the whole list is problem 206; here I only reverse positions left to right and reattach the ends. I add a dummy node so left = 1 isn't a special case, walk prev to just before left, then repeatedly pluck the node after the sublist's head and splice it to the front of the reversed part. After right minus left plucks it's done — one pass, O(1) space. The tricky bit is the two boundary joins, which the dummy and the pinned tail handle automatically."*

## Related / follow-ups
- **Reverse Linked List** (the full-list base case — problem 206)
- **Reverse Nodes in k-Group** (repeatedly reverse fixed-size chunks)
- **Swap Nodes in Pairs** (k = 2 special case)
- **Rotate List** (pointer surgery with a dummy)
