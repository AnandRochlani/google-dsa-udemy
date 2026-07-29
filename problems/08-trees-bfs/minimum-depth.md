# Minimum Depth of Binary Tree

> **LeetCode:** 111. Minimum Depth of Binary Tree · **Difficulty:** 🟢 Easy · **Pattern:** Tree BFS · **Google frequency:** medium

---

## Problem

Return the **minimum depth** of a binary tree: the number of nodes along the shortest path from the root down to the **nearest leaf**. A leaf is a node with no children.

**Example:**

```
        3
       / \
      9   20
         /  \
        15   7
```

`root = [3, 9, 20, null, null, 15, 7]` → `2`

The shortest root-to-leaf path is 3 → 9 (9 is a leaf at depth 2). The path to 15 or 7 is depth 3, but 9 is closer.

**The gotcha that matters:** min depth is to the nearest **leaf**, not the nearest null. For a node with only one child (e.g. root has only a left subtree), that node is **not** a leaf — you must go down the side that exists. `min(left, right)` naively would return 1 for a one-sided chain, which is wrong.

**Constraints that matter:** up to `10^5` nodes. And critically — **BFS can stop the instant it finds the first leaf**, which is what makes it attractive here.

---

## 🧠 Intuition — how you'd actually arrive at this

- **Two valid mindsets, and one is faster on lopsided trees.** "Depth to nearest leaf" is a shortest-path-to-a-target question. Shortest path in an unweighted graph/tree → **BFS**, because BFS explores level by level and the *first* leaf it encounters is guaranteed to be at the minimum depth. The moment you see it, you're done — no need to explore deeper levels.
- **Why the early exit is the whole point:** for *maximum* depth you must visit every node (any node could be the deepest). For *minimum* depth you don't — the nearest leaf might be near the top, and BFS finds it first. On a tree that's shallow on one side and enormously deep on the other, BFS returns almost immediately while DFS would grind through the deep side.
- **The leaf trap:** a leaf has *both* children null. A node with one child is on the path to a deeper leaf; you cannot treat its missing side as depth-0. In BFS this is automatic — you only "finish" when you dequeue a node with no children at all.
- **Pattern trigger:** **"shortest path / nearest / minimum depth to a target" → BFS with early termination.** Contrast with maximum-depth, which is a full DFS. Recognizing "min ⇒ BFS early-exit, max ⇒ full traversal" is the transferable lesson.

---

## ① Brute Force

DFS every root-to-leaf path and take the minimum. It's correct but explores the *entire* tree — no early exit — so the deep side is fully walked even when a shallow leaf exists near the root.

```python
def minDepth_dfs(root):
    if not root:
        return 0
    # a node with a missing child is NOT a leaf — recurse the side that exists
    if not root.left:
        return 1 + minDepth_dfs(root.right)
    if not root.right:
        return 1 + minDepth_dfs(root.left)
    return 1 + min(minDepth_dfs(root.left), minDepth_dfs(root.right))
```

**Why it's the natural first attempt:** it mirrors the elegant max-depth recursion (`1 + min(left, right)`), just with `min`. Note the two special cases guarding against the leaf trap — without them, a one-sided node wrongly contributes a 0-depth "empty" side.

**Why it's not ideal here:** it visits *all* n nodes even when the answer is tiny. Correct and O(n), but it wastes work that BFS's early stop avoids on unbalanced trees.

**Complexity:** Time `O(n)`, Space `O(h)` recursion stack.

---

## ② Optimised Solution

BFS level by level; the first time you dequeue a **leaf**, its depth is the answer — return immediately.

```python
from collections import deque

def minDepth(root):
    if not root:
        return 0
    queue = deque([(root, 1)])       # (node, depth)
    while queue:
        node, depth = queue.popleft()
        if not node.left and not node.right:   # first leaf reached = shallowest
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0   # unreachable for a valid tree
```

**Walk the example:**

| dequeued (depth) | leaf? | action |
|---|---|---|
| (3, 1) | no (has children) | enqueue (9,2), (20,2) |
| (9, 2) | **yes** (no children) | **return 2** ✅ |

BFS never even looks at 15 or 7 — it stops at the first leaf, 9, at depth 2.

**Why it's correct:** BFS dequeues nodes in nondecreasing depth order. The first leaf it pops is therefore at the smallest depth of any leaf — that *is* the minimum depth. The leaf trap is handled naturally: a one-child node isn't a leaf, so we don't stop there; we enqueue its existing child and continue.

**Complexity:** Time `O(n)` worst case (a tree with all leaves at the bottom level, e.g. perfectly balanced), but often far less due to early exit. Space `O(w)` for the queue.

---

## ③ Space Optimization

Two axes:

- **BFS** uses **O(w)** queue but gains the **early exit** — best when the nearest leaf is shallow and the tree is lopsided.
- **DFS** uses **O(h)** stack, no early exit — best when the tree is balanced (small h) and you don't mind visiting everything.

There's no universal winner: on a tree that's a long chain on one side and a shallow leaf on the other, BFS is dramatically faster in practice; on a balanced tree they're the same O(n). The honest interview answer names both and picks BFS *specifically because "minimum" enables the early return.*

> Auxiliary space is already minimal for each style (queue-width or stack-height). The real optimization is *time* via BFS's early termination — a property unique to the "minimum" framing, not available to maximum-depth.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public int minDepth(TreeNode root) {
    if (root == null) return 0;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    int depth = 1;
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (node.left == null && node.right == null) return depth;  // first leaf
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        depth++;
    }
    return depth;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| DFS all paths | O(n) | O(h) |
| BFS with early exit (optimised) | O(n) worst, often ≪ n | O(w) |

---

## Say it out loud (interview narration)

> *"Minimum depth is the shortest root-to-leaf path, so I use BFS: it explores level by level, so the first leaf I dequeue is guaranteed to be the shallowest — I return its depth immediately. That early exit is why BFS beats DFS here on lopsided trees; for maximum depth I couldn't stop early. The one trap is that a node with a single child isn't a leaf — I only stop when both children are null — otherwise a one-sided root would wrongly report depth 1. O(n) worst case, O(w) queue space."*

## Related / follow-ups
- **104. Maximum Depth** (must visit all nodes — full DFS, no early exit)
- **112. Path Sum** (root-to-leaf with the same leaf definition)
- **102. Level Order Traversal** (the base BFS pattern)
