# Linked List Cycle

> **LeetCode:** 141. Linked List Cycle · **Difficulty:** 🟢 Easy · **Pattern:** Fast & Slow Pointers · **Google frequency:** ⭐ high

---

## Problem

Given the `head` of a singly linked list, determine whether the list has a **cycle** — i.e. some node's `next` points back to an earlier node so that following `next` forever never reaches `null`. Return `True` if there's a cycle, `False` otherwise.

**Example:** `3 → 2 → 0 → -4`, where `-4.next` points back to the node `2` → `True` *(you loop 2 → 0 → -4 → 2 → … forever).*

A list with no back-pointer, e.g. `1 → 2 → null`, returns `False`.

**Constraints that matter:** the list can have up to `10⁴` nodes, and you're asked (as the classic follow-up) to solve it in **O(1) space**. That follow-up is the whole point — it's what rules out the obvious hash-set answer.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "How do I know I'm going in circles? I'll remember every node I've visited. If I ever arrive at a node I've already seen, there's a cycle." That's a **hash set of visited nodes** — walk the list, add each node, and if `node in seen` you've found the loop. It works, and it's a perfectly good first answer.
- **Where it hurts:** you're storing a pointer to *every* node — **O(n) extra space**. For a 10⁴-node list that's fine in practice, but the interviewer will immediately ask "can you do it without the extra memory?" The set is doing real work (remembering the past), so how do you detect a loop while remembering *nothing*?
- **The leap:** think of two runners on a circular track. A **slow** runner takes one step at a time; a **fast** runner takes two. On a straight track the fast one just reaches the end (`null`) first — no cycle. But on a *loop*, the fast runner keeps lapping the track and will eventually catch up to the slow one **from behind**. They must meet. Two pointers moving at different speeds turn "is there a loop?" into "do these two ever land on the same node?" — no memory required.
- **Pattern trigger:** **linked list + detect a cycle / find a repeat with O(1) space** → **Fast & Slow Pointers** (Floyd's tortoise and hare). The signal is "cyclic structure, constant space."

---

## ① Brute Force

Walk the list and remember every node you've seen in a hash set. A repeat means a cycle.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle_bruteforce(head):
    seen = set()
    node = head
    while node:
        if node in seen:      # arrived somewhere we've already been
            return True
        seen.add(node)
        node = node.next
    return False              # reached null → no cycle
```

**Why it's the natural first attempt:** "have I been here before?" maps directly onto a set. It's obviously correct and easy to reason about.

**Why it's not enough:** it uses **O(n) space** to store references to every visited node. The interviewer's follow-up ("O(1) space?") is specifically designed to push you off this solution.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

Two pointers, one moving twice as fast as the other. If they ever meet, there's a cycle; if the fast one hits `null`, there isn't.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # +1 per step
        fast = fast.next.next     # +2 per step
        if slow is fast:          # they collided → cycle
            return True
    return False                  # fast fell off the end → no cycle
```

**Walk an example** — `3 → 2 → 0 → -4 → (back to 2)`:

| step | slow (val) | fast (val) | meet? |
|---|---|---|---|
| start | 3 | 3 | no |
| 1 | 2 | 0 | no |
| 2 | 0 | 2 | no *(fast lapped past -4 back to 2)* |
| 3 | -4 | -4 | **yes → return True** ✅ |

For a straight list `1 → 2 → null`, `fast` reaches `null` almost immediately and the loop exits with `False`.

**Why it's correct:** if there's no cycle, `fast` reaches the end (`null`) and we return `False`. If there *is* a cycle, both pointers eventually enter the loop; from then on the gap between them shrinks by exactly **1 node per step** (fast gains 2, slow gains 1, net −1 around the ring), so it can never jump *over* slow without landing on it — they're guaranteed to collide within one lap.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

This *is* the space optimization — it's the reason the problem exists. Compare the two O(n)-time solutions:

- **Hash set:** O(n) time, **O(n) space** — you literally store the whole list.
- **Fast & slow pointers:** O(n) time, **O(1) space** — just two node references, nothing grows with the input.

The tortoise-and-hare replaces "remember every node I've seen" with "let a faster runner catch me on the loop." That trade — memory for a second pointer at a different speed — is the transferable trick behind this entire pattern.

> *"I can detect the loop with a hash set in O(n) space, but I'll use two pointers at different speeds — same O(n) time, O(1) space."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (hash set) | O(n) | O(n) |
| Optimised (fast & slow) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"The obvious way is a hash set of visited nodes — if I revisit one, there's a cycle, O(n) time but O(n) space. To get O(1) space I'll use Floyd's tortoise and hare: a slow pointer moving one step and a fast pointer moving two. If the fast one hits null, no cycle; if there's a loop, the fast pointer laps around and collides with the slow one. That's O(n) time, O(1) space."*

## Related / follow-ups
- **Linked List Cycle II** (find where the cycle *starts* — Floyd's phase 2)
- **Happy Number** (same cycle detection, on a sequence of digit-square sums)
- **Find the Duplicate Number** (treat the array as a linked list and run tortoise & hare)
- **Middle of the Linked List** (fast/slow, but stop when fast hits the end)
