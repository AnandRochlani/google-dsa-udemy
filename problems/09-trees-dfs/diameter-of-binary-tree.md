# Diameter of Binary Tree

> **LeetCode:** 543. Diameter of Binary Tree · **Difficulty:** 🟢 Easy · **Pattern:** Tree DFS · **Google frequency:** ⭐ high

---

## Problem

The **diameter** of a binary tree is the length of the **longest path between any two nodes**, measured in **edges**. That path may or may not pass through the root.

**Example:**

```
        1
       / \
      2   3
     / \
    4   5
```

`root = [1, 2, 3, 4, 5]` → `3`

The longest path is 4 → 2 → 5 → ... actually 4 → 2 → 1 → 3 (or 5 → 2 → 1 → 3), which is 3 edges. The path 4 → 2 → 5 is only 2 edges. So the diameter is 3.

**Constraints that matter:** up to `10^4` nodes. The key insight: the longest path **bends at some node** — going down its left subtree and down its right subtree. So at each node, the candidate path length is `leftHeight + rightHeight`. This is *the* problem for illustrating the **O(n²) recompute vs O(n) single-pass** contrast.

---

## 🧠 Intuition — how you'd actually arrive at this

- **Where can the longest path live?** Any path has a single highest point — the node where it "bends." At that apex node, the path goes as deep as possible into the left subtree and as deep as possible into the right subtree. Its edge-length is therefore `height(left) + height(right)` (heights counted in edges, where empty = -1 edges or, equivalently, node-count height with the formula adjusted).
- **So the plan:** for every node, compute `leftHeight + rightHeight` and take the max over all nodes. The answer is the best apex.
- **The naive way and its pain:** compute `height()` as a separate function, and at each node call it twice. But `height()` itself walks the whole subtree — so you re-walk the same nodes over and over. That's **O(n²)**: height computation nested inside a traversal that also computes height.
- **The leap — fuse the two:** you're already doing a DFS to compute height. During that *same* recursion, once you know the left and right heights of a node, you can update a running `max_diameter = max(max_diameter, left + right)` right there. The height is *returned up* (so the parent can use it); the diameter is *recorded on the side* (a running max). One pass computes both.
- **The return-value thinking:** *"what do I return up? The height. What do I record along the way? The best bend seen so far."* Separating "the thing I return" from "the global answer I track" is a reusable trick (also used in max-path-sum, and validate-tree-with-a-flag problems).
- **Pattern trigger:** **"longest path / widest span through a bend" → DFS returning height, while updating a global max of `left + right` at each node.**

---

## ① Brute Force — O(n²)

Define `height()` separately. At every node, `diameter-through-here = height(left) + height(right)`; recurse over all nodes taking the max. The waste: `height` re-traverses each subtree every time it's called.

```python
def diameterOfBinaryTree_brute(root):
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    def diameter(node):
        if not node:
            return 0
        # path bending at this node, in edges = height(left) + height(right)
        through = height(node.left) + height(node.right)
        return max(through,
                   diameter(node.left),
                   diameter(node.right))
    return diameter(root)
```

**Why it's the natural first attempt:** it's a literal translation of the definition — "for each node, longest path through it = left height + right height; answer = max over nodes."

**Why it's not enough:** `diameter` visits every node (O(n)), and at each it calls `height`, which itself is O(subtree size). Summed over the tree that's **O(n²)** — for a skewed tree, ~n²/2 operations. On 10^4 nodes that's ~10^8, borderline; on larger it times out. The waste is recomputing heights that overlap massively.

**Complexity:** Time `O(n²)`, Space `O(h)`.

---

## ② Optimised Solution — O(n)

Compute height **once** per node with DFS, and update a global diameter as you go. Return height up; record `left + right` on the side.

```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0                     # empty subtree: 0 edges "below"
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)   # longest path bending here (in edges)
        return 1 + max(left, right)      # height to hand to my parent
    height(root)
    return best
```

**Walk the example:**

- `height(4) → 1`, records `best = max(0, 0+0) = 0`. Same for `height(5) → 1`.
- `height(2)`: left = 1 (from 4), right = 1 (from 5). `best = max(0, 1+1) = 2`. returns `1 + max(1,1) = 2`.
- `height(3) → 1`, `best` stays (0+0=0 < 2).
- `height(1)`: left = 2 (from 2), right = 1 (from 3). `best = max(2, 2+1) = 3`. returns `1 + max(2,1) = 3`.
- Answer: `best = 3`. ✅

Note `left + right` at a node equals the number of *edges* on the path bending there: 2's subtrees each have height 1 (one edge down each side) → 2 edges; 1's give 2 + 1 = 3 edges — the true diameter.

**Why it's correct:** every path in the tree bends at exactly one node — its shallowest node. At that node, the path's edge count is `height(left) + height(right)`, which is exactly the value we compare into `best`. Since we do this at *every* node, we consider every possible apex, so `best` ends as the global maximum. Height is computed once per node because each `height(node)` call directly uses the returned values of its children — no recomputation.

**Complexity:** Time `O(n)` — one visit per node. Space `O(h)` recursion stack.

---

## ③ Space Optimization

Space is the recursion stack, **O(h)** — O(log n) balanced, O(n) skewed. That's already the floor for a DFS that must reach every leaf.

- The real optimization was **time**: fusing height + diameter into one pass took us from **O(n²) → O(n)**. That's the headline, and the classic teaching moment of this problem.
- An iterative post-order traversal with an explicit stack + a height map achieves the same O(n) time and O(h) space without recursion — worth mentioning if recursion depth is a concern, but it's more code.

> Space is already O(h)-optimal. The lesson here isn't a space trick — it's recognizing the O(n²) recompute trap and collapsing it into a single post-order pass by returning height while tracking the answer on the side.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
class Solution {
    private int best = 0;
    public int diameterOfBinaryTree(TreeNode root) {
        height(root);
        return best;
    }
    private int height(TreeNode node) {
        if (node == null) return 0;
        int left = height(node.left);
        int right = height(node.right);
        best = Math.max(best, left + right);   // path bending here (edges)
        return 1 + Math.max(left, right);      // height for the parent
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Recompute height at each node (brute) | O(n²) | O(h) |
| Single-pass DFS (optimised) | O(n) | O(h) |

---

## Say it out loud (interview narration)

> *"The longest path bends at some node, going down its left and right subtrees, so at each node the candidate length is leftHeight + rightHeight. The naive way computes height as a separate function and calls it at every node — but height re-walks the subtree, so it's O(n²). The fix is to fuse them: I do one DFS that returns height, and while I have a node's left and right heights I update a running max of left + right. Height goes up to the parent; the diameter is tracked on the side. One pass, O(n) time, O(h) stack."*

## Related / follow-ups
- **104. Maximum Depth** (the height subroutine, standalone)
- **124. Binary Tree Maximum Path Sum** (same "return one side up, track the bend" pattern with values)
- **687. Longest Univalue Path** (diameter variant constrained to equal values)
- **110. Balanced Binary Tree** (height + balance flag in one pass — same fusion trick)
