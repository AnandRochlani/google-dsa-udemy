# Reorder List

> **LeetCode:** 143. Reorder List · **Difficulty:** 🟡 Medium · **Pattern:** In-Place Linked-List Reversal · **Google frequency:** ⭐ high

---

## Problem

Given the `head` of a singly linked list `L₀ → L₁ → … → Lₙ₋₁ → Lₙ`, reorder it in place to:

`L₀ → Lₙ → L₁ → Lₙ₋₁ → L₂ → Lₙ₋₂ → …`

That is, interleave the list from the front with the list from the back. You may **not** change node values — only rewire pointers. Modify the list **in place**.

**Example:** `1 → 2 → 3 → 4` → `1 → 4 → 2 → 3`.
`1 → 2 → 3 → 4 → 5` → `1 → 5 → 2 → 4 → 3`.

**Constraints that matter:** up to `5×10⁴` nodes, in-place, values fixed. "In place + fixed values" is what forces the elegant three-step pointer solution instead of copying to an array.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** the pattern is "first, last, second, second-last, …" — that's just **two pointers walking inward from both ends**. In an array you'd do exactly that. So: dump all nodes into an array, then use `left`/`right` indices to relink `left → right → left+1 → right−1 → …`. Totally correct.
- **Where it hurts:** a singly linked list has **no way to walk backwards** — that's the whole reason the array is tempting. But the array is **O(n) extra space**, and the interviewer's "in place" is a direct challenge to it. The obstacle is purely "I can't go backward," so the fix is: make the back half go *forward*.
- **The leap — decompose into three tools you already own:**
  1. **Find the middle** (fast/slow pointers) and split the list into two halves.
  2. **Reverse the second half** in place (problem 206) so its nodes now run in reverse order.
  3. **Merge the two halves** by alternating one node from each. Now "front then back" is just "front-half node, reversed-back-half node, repeat" — all forward traversal, no array.
- **Pattern trigger:** **"interweave front and back of a singly linked list in place"** → **middle-finding + in-place reversal + merge**. Recognising that a hard reorder is three easy sub-problems stacked is the transferable skill.

---

## ① Brute Force

Store node references in an array, then relink with two indices walking inward.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reorder_list_bruteforce(head):
    if not head:
        return
    nodes = []
    node = head
    while node:
        nodes.append(node)
        node = node.next
    left, right = 0, len(nodes) - 1
    while left < right:
        nodes[left].next = nodes[right]      # front → back
        left += 1
        if left == right:
            break
        nodes[right].next = nodes[left]      # back → next front
        right -= 1
    nodes[left].next = None                  # terminate the list
```

**Why it's the natural first attempt:** with random access (the array), "interleave from both ends" is a trivial two-pointer loop — it sidesteps the "can't go backward" problem entirely.

**Why it's not enough:** it uses **O(n) extra space** for the node references, which the in-place requirement rules out.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

Three phases, all in place: find the middle, reverse the second half, merge the two halves alternately.

```python
def reorder_list(head):
    if not head or not head.next:
        return

    # 1. find the middle (slow ends at the first-half tail / start of 2nd half)
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

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

    # 3. merge the two halves alternately
    first = head
    while second:
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next
```

**Walk `1 → 2 → 3 → 4 → 5`:**

- **Middle:** slow stops at node `3` (first half `1 → 2 → 3`). Cut: `1 → 2 → 3` and `4 → 5`.
- **Reverse 2nd half:** `4 → 5` becomes `5 → 4`.
- **Merge** `1 → 2 → 3` with `5 → 4`:
  - take `1`, splice `5`: `1 → 5 → 2 → 3`; advance.
  - take `2`, splice `4`: `1 → 5 → 2 → 4 → 3`; `second` becomes null → stop.

Result: `1 → 5 → 2 → 4 → 3` ✅. (For even `1 → 2 → 3 → 4`: halves `1 → 2` and reversed `4 → 3`, merge → `1 → 4 → 2 → 3` ✅.)

**Why it's correct:** after reversing, the second half's nodes come out in exactly last-to-first order, so alternating "one from the front half, one from the reversed back half" reproduces `L₀, Lₙ, L₁, Lₙ₋₁, …`. The `while fast.next and fast.next.next` condition puts the split so the first half is the same length or one longer, which matches the required output for both parities.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

The three-phase solution *is* the space optimisation — it's why 143 is a favourite interview problem:

- **Node array + two pointers:** O(n) time, **O(n) space**.
- **Middle + reverse + merge, in place:** O(n) time, **O(1) space** — only a handful of pointers across all three phases.

The elegant part is realising the array existed *only* to fake backward traversal, and that **reversing the second half in place removes the need for it**. Every phase — fast/slow midpoint, prev/curr/next reversal, alternating merge — is O(1) space, so the whole thing is.

> *"The array was only there so I could walk the back half backward. If I reverse the back half in place instead, I can merge the two halves forward — O(1) space. It's three sub-problems I already know: find the middle, reverse, merge."*

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (node array) | O(n) | O(n) |
| Optimised (middle + reverse + merge) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"The pattern is front, back, front, back — two pointers from both ends, which is easy in an array but a singly linked list can't go backward. So instead of an O(n) array, I do three in-place steps: find the middle with fast/slow, reverse the second half, then merge the two halves alternately. Reversing the back half is exactly what lets me walk it forward during the merge. All three steps are O(1) space, so O(n) time and O(1) space overall."*

## Related / follow-ups
- **Middle of the Linked List** (phase 1 in isolation — problem 876)
- **Reverse Linked List** (phase 2 in isolation — problem 206)
- **Merge Two Sorted Lists** (the alternating-merge mechanic)
- **Palindrome Linked List** (middle + reverse-half + compare — same decomposition)
