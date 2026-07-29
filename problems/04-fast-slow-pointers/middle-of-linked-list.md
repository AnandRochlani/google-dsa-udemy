# Middle of the Linked List

> **LeetCode:** 876. Middle of the Linked List · **Difficulty:** 🟢 Easy · **Pattern:** Fast & Slow Pointers · **Google frequency:** medium

---

## Problem

Given the `head` of a singly linked list, return the **middle node**. If there are two middle nodes (even length), return the **second** one.

**Example:** `1 → 2 → 3 → 4 → 5` → returns the node `3` *(and everything after: `3 → 4 → 5`).*
`1 → 2 → 3 → 4 → 5 → 6` → returns the node `4` *(second of the two middles).*

**Constraints that matter:** a singly linked list — you can only move forward, and you **don't know the length up front**. That "no random access, unknown length" combination is exactly what the fast/slow trick is built for.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "The middle is at index `n/2`, so I need `n`." Walk the list once to count the nodes, then walk again `n/2` steps to reach the middle. **Two passes.** It works and it's easy to explain.
- **Where it hurts:** it's not *wrong*, but you're traversing the list twice, and you had to compute and store the length just to divide it. There's a slicker way to reach the halfway mark in a single sweep.
- **The leap:** if one pointer moves **twice as fast** as another, then when the fast pointer reaches the **end**, the slow pointer has covered exactly **half** the distance — it's sitting on the middle. No counting, no second pass. The speed ratio *is* the division by two.
- **Pattern trigger:** **need the midpoint of a linked list in one pass** → **Fast & Slow Pointers**. (Same tool as cycle detection; here you stop when fast hits the end instead of when the pointers meet.)

---

## ① Brute Force

Count the nodes, then walk halfway back in.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def middle_node_bruteforce(head):
    n = 0
    node = head
    while node:                 # pass 1: count
        n += 1
        node = node.next
    node = head
    for _ in range(n // 2):     # pass 2: walk to the middle
        node = node.next
    return node
```

**Why it's the natural first attempt:** "middle = index n/2" is the textbook definition; counting then walking is the literal implementation.

**Why it's not enough:** it makes **two passes** over the list. Fine, but an interviewer wants the one-pass answer that shows you know the pointer trick.

**Complexity:** Time `O(n)` (two passes), Space `O(1)`.

---

## ② Optimised Solution

One pass: slow moves one step, fast moves two. When fast runs off the end, slow is at the middle.

```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # +1
        fast = fast.next.next     # +2
    return slow                   # fast hit the end → slow at middle
```

**Walk both parities:**

*Odd* `1 → 2 → 3 → 4 → 5`:

| slow | fast | note |
|---|---|---|
| 1 | 1 | start |
| 2 | 3 | |
| 3 | 5 | `fast.next` is null → stop → **return 3** ✅ |

*Even* `1 → 2 → 3 → 4 → 5 → 6`:

| slow | fast | note |
|---|---|---|
| 1 | 1 | start |
| 2 | 3 | |
| 3 | 5 | |
| 4 | null | `fast` is null → stop → **return 4** (the second middle) ✅ |

**Why it's correct:** fast covers ground twice as fast, so it reaches the end when slow has gone half the length. The loop condition `while fast and fast.next` naturally lands slow on the *second* middle for even lengths — exactly what the problem wants. (Want the *first* middle instead? Use `while fast.next and fast.next.next`.)

**Complexity:** Time `O(n)` (single pass), Space `O(1)`.

---

## ③ Space Optimization

Space is already **O(1)** in both approaches — we only ever hold a couple of node references, nothing that grows with `n`. So the win here isn't memory, it's **passes**: the fast/slow version finds the middle in **one** traversal instead of two.

> Already O(1) space — only two pointers, nothing scales with the input. The optimisation over brute force is halving the number of passes, not the memory.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (count + walk) | O(n), two passes | O(1) |
| Optimised (fast & slow) | O(n), one pass | O(1) |

---

## Say it out loud (interview narration)

> *"I could count the nodes then walk n/2 in — but that's two passes. Instead I use two pointers: slow moves one node, fast moves two. When fast reaches the end, slow is at the middle — one pass, O(1) space. For even length this condition naturally returns the second of the two middles, which is what's asked."*

## Related / follow-ups
- **Reorder List** (uses this exact trick to split the list before reversing the second half)
- **Palindrome Linked List** (find the middle, reverse the second half, compare)
- **Linked List Cycle** (same fast/slow setup; stop on collision instead of end)
