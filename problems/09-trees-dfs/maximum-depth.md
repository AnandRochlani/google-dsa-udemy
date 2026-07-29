# Maximum Depth of Binary Tree

> **LeetCode:** 104. Maximum Depth of Binary Tree · **Difficulty:** 🟢 Easy · **Pattern:** Tree DFS · **Google frequency:** ⭐ high

---

## Problem

Return the **maximum depth** of a binary tree: the number of nodes along the longest path from the root down to the farthest leaf.

**Example:**

```
        3
       / \
      9   20
         /  \
        15   7
```

`root = [3, 9, 20, null, null, 15, 7]` → `3`

The longest root-to-leaf path is 3 → 20 → 15 (or 3 → 20 → 7), which has 3 nodes.

**Constraints that matter:** up to `10^4` nodes. Unlike *minimum* depth, you must consider **every** leaf — the deepest one could be anywhere — so there's no early exit. This is the canonical "reduce a tree to one number via recursion" problem.

---

## 🧠 Intuition — how you'd actually arrive at this

> This is the archetype for the DFS question every tree-recursion answer imitates: **"what do I return up from each node?"**

- **What does the problem ask?** Not levels, not a path listing — a single scalar summarizing the whole tree. That's a reduction, and reductions on trees are DFS: solve the subproblems (subtrees) and combine.
- **The return-value thinking:** stand at any node and ask *"if my children already told me the max depth of their subtrees, what do I report to my parent?"* Answer: `1 + max(left depth, right depth)` — my own node plus the deeper of my two sides. This is the entire solution; everything else is boilerplate.
- **The base case:** an empty subtree (`None`) has depth `0`. A leaf then reports `1 + max(0, 0) = 1`. The recursion bottoms out cleanly.
- **Why not BFS?** BFS *can* do it (count levels), but max depth needs *all* nodes visited regardless, so DFS's tidy `1 + max(...)` recurrence is the natural expression. Contrast with **minimum** depth, where BFS's early exit genuinely helps.
- **Pattern trigger:** **"height / depth / reduce the tree to a number" → DFS, return a value up from each node and combine with a `max`/`min`/`+`.** Learn the "what do I return up?" reflex here; you'll reuse it in diameter, validate-BST, balanced-tree, and LCA.

---

## ① Brute Force

There isn't a meaningfully *worse* correct approach here — every node must be visited once, so O(n) is the floor. The "naive framing" is doing it the verbose way: an explicit helper that checks for null, recurses both sides, and combines. (Or BFS counting levels — also O(n), but heavier machinery for a pure reduction.)

```python
from collections import deque

def maxDepth_bfs(root):           # correct but heavier than needed
    if not root:
        return 0
    depth, queue = 0, deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
    return depth
```

**Why it's a reasonable first attempt:** if you're primed on level-order BFS, counting levels is a direct read of "depth = number of levels."

**Why the DFS is cleaner:** BFS needs an O(w) queue and explicit level bookkeeping; the recursion below is three lines and O(h) space. Both are O(n) time — this is a rare case where the "optimised" version is about *elegance and space*, not asymptotic time.

**Complexity:** Time `O(n)`, Space `O(w)`.

---

## ② Optimised Solution

DFS. Each node returns `1 + max(depth of left, depth of right)`.

```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

**Walk the example:**

- `maxDepth(15)` → `1 + max(0, 0) = 1`. Same for `maxDepth(7) = 1`.
- `maxDepth(20)` → `1 + max(maxDepth(15)=1, maxDepth(7)=1) = 2`.
- `maxDepth(9)` → `1 + max(0, 0) = 1`.
- `maxDepth(3)` → `1 + max(maxDepth(9)=1, maxDepth(20)=2) = 3`. ✅

The value bubbles up: leaves report 1, each parent adds itself to the taller side, the root reports the overall height.

**Why it's correct:** by induction — assume each recursive call correctly returns its subtree's depth. Then a node's longest downward path is its own node (`+1`) plus the longer of its two children's longest paths (`max`). The base case `None → 0` seeds it. So the root returns the true maximum depth.

**Complexity:** Time `O(n)` — one call per node. Space `O(h)` recursion stack.

---

## ③ Space Optimization

Space is the recursion stack, **O(h)** — O(log n) for a balanced tree, O(n) for a degenerate chain. Options:

- **Iterative DFS with an explicit stack** (of `(node, depth)` pairs): same O(h) worst case, just moves the stack off the call stack — useful in languages/environments with tight recursion limits.
- **Morris traversal** could reach O(1) space, but it's overkill and error-prone for a simple depth count; not worth it in an interview unless explicitly pushed.
- **BFS** trades stack-height for queue-width (O(w)).

> For a balanced tree O(h) = O(log n) is already excellent. The recursion is the clean answer; only reach for iterative or Morris if the interviewer bans recursion or flags stack-overflow on a 10^5-deep skewed tree.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| BFS level count | O(n) | O(w) |
| DFS recursion (optimised) | O(n) | O(h) |
| Iterative DFS with stack | O(n) | O(h) |

---

## Say it out loud (interview narration)

> *"Max depth is a reduction of the whole tree to one number, so I use DFS. At each node I ask: given my children's depths, what do I report? It's one plus the max of my two subtrees, with an empty subtree being depth 0. That's a three-line recursion, O(n) time, O(h) stack. Every node has to be visited because the deepest leaf could be anywhere — unlike minimum depth, there's no early exit. If recursion depth were a concern on a skewed tree I'd switch to an explicit stack or BFS level-counting."*

## Related / follow-ups
- **111. Minimum Depth** (BFS with early exit — the mirror image)
- **543. Diameter of Binary Tree** (reuse this height computation, track the widest span)
- **110. Balanced Binary Tree** (height + a balance check in one pass)
- **111 / 104 pair** teaches "min ⇒ BFS early-exit, max ⇒ full DFS."
