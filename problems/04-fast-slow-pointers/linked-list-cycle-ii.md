# Linked List Cycle II (Find the Cycle Start)

> **LeetCode:** 142. Linked List Cycle II · **Difficulty:** 🟡 Medium · **Pattern:** Fast & Slow Pointers · **Google frequency:** ⭐ high

---

## Problem

Given the `head` of a linked list, return the **node where the cycle begins**. If there is no cycle, return `None`. You should not modify the list, and the follow-up asks for **O(1) space**.

**Example:** `3 → 2 → 0 → -4`, with `-4.next` pointing back to the node `2` → return **the node `2`** *(that's where the loop closes).*

`1 → 2 → null` → return `None`.

**Constraints that matter:** up to `10⁴` nodes, and the O(1)-space follow-up. Detecting the cycle (problem 141) is only half the job — now you must pinpoint the *entry* node without a hash set.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** same as cycle detection — **hash set of visited nodes**. Walk from `head`, and the *first* node you see twice is exactly the entry of the cycle. Return it. Clean, correct, O(n) space.
- **Where it hurts:** the set costs O(n) memory. We already know (from problem 141) that a fast/slow pair *detects* a cycle in O(1) space — but the collision point where they meet is **not** the cycle's start. It's somewhere inside the loop. So the real question is: given where they met, how do I get back to the entrance without remembering anything?
- **The leap — the arithmetic that makes it magic:** Let `F` be the distance from `head` to the cycle entry, and `C` the cycle length. When slow enters the loop it has walked `F`; fast has walked `2F`, so fast is already `F` *into* the loop. Fast gains on slow by 1 node per step, so they meet after slow walks another `C − F` steps — i.e. the meeting point is `C − F` nodes *past* the entry, which is the same as `F` nodes *before* the entry (going around). **So the distance from the meeting point onward to the entry equals the distance from `head` to the entry.** Therefore: reset one pointer to `head`, advance both **one step at a time**, and they collide exactly at the cycle start.
- **Pattern trigger:** **cycle detection + locate the entry, O(1) space** → **Floyd's algorithm, phase 2** (the "reset to head and walk in lockstep" move).

---

## ① Brute Force

Hash set: the first node you encounter twice is the cycle's entry.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def detect_cycle_bruteforce(head):
    seen = set()
    node = head
    while node:
        if node in seen:      # first repeat = entry point
            return node
        seen.add(node)
        node = node.next
    return None
```

**Why it's the natural first attempt:** "the first place I loop back to *is* the start of the loop" is intuitively obvious, and a set makes "have I seen this node?" trivial.

**Why it's not enough:** **O(n) space.** The follow-up explicitly wants O(1), which rules this out.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

Floyd's two phases: **(1)** find a meeting point with fast/slow; **(2)** reset one pointer to `head` and walk both one step at a time until they meet — that meeting node is the entry.

```python
def detect_cycle(head):
    slow = fast = head
    # phase 1: detect a collision inside the loop
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None            # loop exited normally → no cycle

    # phase 2: find the entry
    slow = head                # reset one pointer to the head
    while slow is not fast:
        slow = slow.next       # both move ONE step now
        fast = fast.next
    return slow                # they meet exactly at the cycle start
```

*(The `while … else` runs the `else` only if the loop finished without `break` — i.e. fast fell off the end and there's no cycle.)*

**Walk an example** — `3 → 2 → 0 → -4 → (back to 2)`. Here `F = 1` (head→2), cycle is `2 → 0 → -4`, `C = 3`.

- **Phase 1:** slow/fast collide at node `-4` (as traced in problem 141).
- **Phase 2:** put `slow` back at `head` (node `3`); `fast` stays at `-4`.
  - step 1: `slow → 2`, `fast → 2` (from -4 wrapping to 2). They match → **return node `2`** ✅

**Why it's correct:** the algebra above shows meeting-point-to-entry distance ≡ head-to-entry distance (mod C). Two pointers starting those two equal distances away, moving at the same speed, land on the entry simultaneously.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

The optimised solution already *is* the O(1)-space answer, and it's the entire reason 142 is harder than 141:

- **Hash set:** O(n) time, **O(n) space**.
- **Floyd phase 1 + 2:** O(n) time, **O(1) space** — three node references (`head`, `slow`, `fast`), nothing that scales with `n`.

The insight worth stating out loud is *why* the reset works: the geometry of the loop makes the two distances equal, so you can find the entrance with pointers alone. That's the memory-for-math trade at the core of the pattern.

> *"Detecting the cycle is the tortoise and hare. To find the *start* in O(1) space, I use the distance identity: reset one pointer to head, walk both one step at a time, and they meet at the entry."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (hash set) | O(n) | O(n) |
| Optimised (Floyd, 2 phases) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"A hash set finds the first repeated node — the entry — in O(n) space. For O(1) space I run Floyd's: phase one, fast and slow collide inside the loop. That collision isn't the start, but there's a neat identity — the distance from the meeting point to the entry equals the distance from head to the entry. So I reset one pointer to head, advance both one step at a time, and where they meet is the cycle's start. O(n) time, O(1) space."*

## Related / follow-ups
- **Linked List Cycle** (just the detection half — problem 141)
- **Find the Duplicate Number** (map the array to a linked list; the duplicate is the cycle entry — same phase-2 trick)
- **Happy Number** (cycle detection on a numeric sequence)
