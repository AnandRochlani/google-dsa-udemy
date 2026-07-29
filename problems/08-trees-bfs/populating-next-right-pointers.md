# Populating Next Right Pointers in Each Node

> **LeetCode:** 116. Populating Next Right Pointers in Each Node · **Difficulty:** 🟡 Medium · **Pattern:** Tree BFS · **Google frequency:** medium

---

## Problem

You're given a **perfect binary tree** (every internal node has exactly two children, all leaves on the same level). Each node has an extra pointer `next`. Populate every `next` to point to the node immediately to its **right on the same level**; the rightmost node of each level points to `null` (`next` starts out `null`).

**Node definition:**
```python
class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val, self.left, self.right, self.next = val, left, right, next
```

**Example:**

```
        1                    1 → null
       / \                  / \
      2   3      →         2 → 3 → null
     / \ / \              / \ / \
    4  5 6  7            4→5→6→7 → null
```

`root = [1, 2, 3, 4, 5, 6, 7]` → each node's `next` wired left-to-right within its level.

**Constraints that matter:** the tree is **perfect** — that's the gift. Every node either has both children or none, and all levels are full. Up to `2^12 - 1 ≈ 4096` nodes. The follow-up asks for **O(1) extra space** (recursion/implicit stack aside), which the perfectness makes possible.

---

## 🧠 Intuition — how you'd actually arrive at this

- **"Same level, node to the right" screams level order.** You're connecting each node to its right neighbor within a level — that's a BFS observation. The straightforward solution: BFS level by level, and within each level, wire `node.next = the next node in the queue`.
- **Where BFS feels wasteful:** BFS needs an O(w) queue — up to ~n/2 nodes at the bottom level. But the problem *hands you next pointers*, and asks for O(1) space. That's a nudge: **can the level you just finished wiring serve as the "linked list" you walk to build the next level?**
- **The leap (the perfect-tree trick):** once level `k` is fully connected via `next`, you can traverse level `k` left-to-right using those very pointers — no queue needed. For each node on level `k`, wire its own two children: `node.left.next = node.right` (siblings), and `node.right.next = node.next.left` (bridge across different parents, using the parent's already-built `next`). Because the tree is *perfect*, `node.next.left` always exists when `node.next` does. You build level `k+1`'s links using only level `k`'s links plus O(1) pointers.
- **Pattern trigger:** **"connect nodes within a level" → BFS; but if the structure lets one finished level thread the next, you get O(1) space.** The perfect-tree guarantee is what unlocks the space-free version.

---

## ① Brute Force

BFS with a queue. Standard level-order, but instead of collecting values, link each dequeued node to the next one in the same level.

```python
from collections import deque

def connect_bfs(root):
    if not root:
        return None
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i < level_size - 1:
                node.next = queue[0]     # the next node in this level (now at front)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return root
```

**Why it's the natural first attempt:** it's plain level order; the only twist is `node.next = queue[0]` — after popping `node`, the front of the queue is its right neighbor on this level (for all but the last node). Works on *any* binary tree, not just perfect ones.

**Why it's not enough (for the follow-up):** the queue costs **O(w) = O(n)** space. The problem explicitly asks for O(1). We can exploit the perfect structure to drop the queue entirely.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

Use the `next` pointers you're building as the traversal mechanism. Walk each level via `next`, wiring the level below. **O(1) extra space.**

```python
def connect(root):
    if not root:
        return None
    leftmost = root
    while leftmost.left:                 # while there's a next level (perfect tree ⇒ check .left)
        head = leftmost
        while head:                      # walk current level left-to-right via next
            head.left.next = head.right              # (a) siblings
            if head.next:
                head.right.next = head.next.left     # (b) bridge across parents
            head = head.next
        leftmost = leftmost.left          # drop to the next level's leftmost
    return root
```

**Walk the example** (root = perfect tree of 1..7):

- **Level 0** (`leftmost = 1`): `head = 1`. `1.left(2).next = 1.right(3)`. `1.next` is null → no bridge. Level 1 now: `2 → 3 → null`. Drop `leftmost = 2`.
- **Level 1** (`leftmost = 2`):
  - `head = 2`: `2.left(4).next = 2.right(5)`; `2.next` is 3 → `2.right(5).next = 3.left(6)`. So far `4 → 5 → 6`.
  - `head = 3` (via `2.next`): `3.left(6).next = 3.right(7)`; `3.next` null → stop bridge. Now `4 → 5 → 6 → 7 → null`.
  - `head = null` → level done. Drop `leftmost = 4`.
- **Level 2** (`leftmost = 4`): `4.left` is null → outer loop ends. Leaves need no wiring beyond what's done.

Final: every `next` set correctly with no queue.

**Why it's correct:** induction on levels. Before processing level `k`, all `next` pointers *on* level `k` are already set (base case: level 0 has a single node, `next = null`). Walking level `k` via those pointers, rule (a) links siblings and rule (b) links a node's right child to its parent's-next's left child — which is precisely the right neighbor across the parent boundary. Perfectness guarantees `head.next.left` exists whenever `head.next` does. After the pass, level `k+1` is fully linked, satisfying the invariant for the next iteration.

**Complexity:** Time `O(n)` — each node visited once as a parent. Space **O(1)** — only a couple of pointers, no queue, no recursion.

---

## ③ Space Optimization

This *is* the space optimization — from BFS's O(n) queue down to **O(1)** by reusing the `next` pointers as a level-linked-list.

- **BFS version:** O(w) = O(n) auxiliary. Simpler, works on any tree.
- **Optimised version:** O(1) auxiliary. Requires the perfect-tree guarantee (so `node.next.left` is always present).

If the tree were **not** perfect (that's the sequel, **117. Populating Next Right Pointers II**), the same O(1) idea still works but you must scan for the next *available* child across gaps and use a dummy head per level — a bit more bookkeeping. Mention that you know 116's perfectness is doing real work here.

> The O(1) solution is the intended final answer. Recursion would reintroduce O(h) implicit stack space, so the iterative two-loop form is what fully achieves the O(1) target.

---

## Java (for Java interviewers)

```java
// Definition: class Node { int val; Node left, right, next; }
public Node connect(Node root) {
    if (root == null) return null;
    Node leftmost = root;
    while (leftmost.left != null) {           // perfect tree: left exists ⇒ next level exists
        Node head = leftmost;
        while (head != null) {                // walk this level via next
            head.left.next = head.right;                       // (a) siblings
            if (head.next != null)
                head.right.next = head.next.left;              // (b) bridge across parents
            head = head.next;
        }
        leftmost = leftmost.left;
    }
    return root;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| BFS with queue | O(n) | O(n) |
| Reuse next pointers (optimised) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"'Connect each node to its right neighbor on the same level' is a level-order task, so my first pass is BFS: wire each node to the next one in the queue. That's O(n) time but O(n) space for the queue. The follow-up wants O(1) — and since the tree is perfect I can get it: once a level is fully linked by next, I traverse that level using those pointers and wire the level below. Left child points to right child, and right child points across to the parent's-next's left child. Perfectness guarantees that neighbor exists. Each node visited once, O(n) time, O(1) space — no queue, no recursion."*

## Related / follow-ups
- **117. Populating Next Right Pointers II** (tree is *not* perfect — same idea, handle gaps with a dummy head)
- **102. Level Order Traversal** (the BFS base pattern)
- **199. Right Side View** (rightmost per level — the nodes whose `next` is null)
