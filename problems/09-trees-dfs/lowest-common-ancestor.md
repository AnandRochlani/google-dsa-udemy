# Lowest Common Ancestor of a Binary Tree

> **LeetCode:** 236. Lowest Common Ancestor of a Binary Tree · **Difficulty:** 🟡 Medium · **Pattern:** Tree DFS · **Google frequency:** ⭐ high

---

## Problem

Given the root of a binary tree and two distinct nodes `p` and `q`, return their **lowest common ancestor (LCA)** — the deepest node that has *both* `p` and `q` as descendants. A node is allowed to be a descendant of itself.

**Example:**

```
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4
```

`p = 5`, `q = 1` → `3` (the root; 5 is in the left subtree, 1 in the right, so 3 is the lowest node containing both).
`p = 5`, `q = 4` → `5` (4 is under 5, and a node can be its own ancestor).

**Constraints that matter:** it's a **general** binary tree (no BST ordering to exploit — that's the easier problem 235), and both `p` and `q` are **guaranteed to exist** in the tree. Up to `10^5` nodes.

---

## 🧠 Intuition — how you'd actually arrive at this

- **What makes a node the LCA?** Exactly one of three situations makes node `X` the answer: (1) `p` is found in `X`'s left subtree and `q` in its right (they "split" at `X`), or (2) the symmetric split, or (3) `X` itself *is* `p` or `q` and the other lies somewhere below it. The LCA is the *deepest* node where `p` and `q` stop being on the same side.
- **The return-value thinking (the crux):** design one DFS that answers, for each node, *"did you find p or q anywhere in your subtree — and if so, report it up."* Concretely, `dfs(node)` returns:
  - `None` if neither `p` nor `q` is in this subtree,
  - the node itself if it *is* `p` or `q` (report the hit upward), or
  - whatever a child reports if only one side found something.
- **The magic moment:** at some node, the **left call returns non-None and the right call returns non-None** — meaning `p` was found on one side and `q` on the other. That node is the split point → it's the LCA, so return *itself*. Above that point, only one side ever reports non-None (the LCA bubbles up unchanged), so the first split you hit on the way up is the lowest one.
- **Why self-ancestor falls out for free:** if `node == p`, you return `node` immediately without descending. If `q` is below it, the parent sees "one child (this one) found something, the other didn't" and passes `p` up — and no higher split occurs, so `p` is the LCA. Correct.
- **Pattern trigger:** **"lowest common ancestor / where do two nodes meet" → post-order DFS that returns a found-node upward; the node where both sides come back non-null is the answer.**

---

## ① Brute Force

Find the **root-to-node path** for `p` and for `q` separately (two DFS searches that record the path), then walk both paths from the top and return the last node they share.

```python
def lowestCommonAncestor_paths(root, p, q):
    def find_path(node, target, path):
        if not node:
            return False
        path.append(node)
        if node is target:
            return True
        if find_path(node.left, target, path) or find_path(node.right, target, path):
            return True
        path.pop()                       # backtrack
        return False

    path_p, path_q = [], []
    find_path(root, p, path_p)
    find_path(root, q, path_q)

    lca = None
    for a, b in zip(path_p, path_q):     # walk both from root, last common node
        if a is b:
            lca = a
        else:
            break
    return lca
```

**Why it's the natural first attempt:** "common ancestor" literally means "shared prefix of the two root-to-node paths" — so build both paths and compare. Intuitive and clearly correct.

**Why it's heavier than needed:** two full traversals to build paths, plus O(h) storage for each path, plus a comparison pass. It works in O(n) time but is clunkier and uses O(h) extra path storage. A single post-order pass gets the answer directly.

**Complexity:** Time `O(n)`, Space `O(h)` (two path lists + recursion).

---

## ② Optimised Solution

One post-order DFS. Return `p`/`q` when found; the node whose left and right both return non-null is the LCA.

```python
def lowestCommonAncestor(root, p, q):
    if not root or root is p or root is q:
        return root                       # base: empty, or found p/q → report up
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root                       # p and q split here → this is the LCA
    return left or right                  # only one side found something → bubble it up
```

**Walk the example** with `p = 5`, `q = 1`:

- `dfs(3)`: not p/q. Recurse left (5) and right (1).
  - `dfs(5)`: `5 is p` → return `5` (don't descend further).
  - `dfs(1)`: `1 is q` → return `1`.
- Back at `3`: `left = 5` (truthy) and `right = 1` (truthy) → **both non-null → return 3.** ✅

Now `p = 5`, `q = 4`:

- `dfs(3)`: recurse. Left subtree eventually: `dfs(5)` sees `5 is p` → returns `5` immediately (never looks for 4 below). Right subtree `dfs(1)` returns `None`.
- Back at `3`: `left = 5`, `right = None` → return `left or right = 5`. ✅ (5 is 4's ancestor and its own ancestor.)

**Why it's correct:** the function returns non-null from a subtree iff that subtree contains `p` or `q`. If, at some node, *both* recursive calls return non-null, then one target is in the left subtree and the other in the right — this node is the shallowest such split, i.e. the LCA, so it returns itself. If only one side is non-null, that side's returned node is passed up unchanged; higher ancestors never see a second split, so the value propagates to the root as the LCA. The `root is p or root is q` base case handles the self-ancestor case (a target found high stops the descent and represents its subtree). Because `p` and `q` are guaranteed present, a split is guaranteed to occur exactly once.

**Complexity:** Time `O(n)` — each node visited once. Space `O(h)` recursion stack.

---

## ③ Space Optimization

Auxiliary space is the recursion stack, **O(h)** — O(log n) balanced, O(n) skewed — already optimal for a single tree traversal.

- Versus the brute-force path approach, this saves the two explicit O(h) path lists (still O(h) stack, but no separate storage and only one pass).
- If **parent pointers** were available on each node (a common follow-up variant), you could walk up from `p` and `q` and find the intersection like the "linked-list intersection" trick — O(1) auxiliary if you first equalize depths, or O(h) with a visited set. Worth mentioning as the "what if the tree had parent pointers?" follow-up.

> O(h) is the floor for a from-scratch traversal. The single-pass post-order is already the clean optimum; the only way to change the space profile is a different input model (parent pointers) or the BST version (LCA of a BST, LC 235, descends in O(h) using ordering — no full traversal).

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left  = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;   // split → LCA
    return left != null ? left : right;               // bubble up the found side
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Two root-to-node paths + compare | O(n) | O(h) |
| Single post-order DFS (optimised) | O(n) | O(h) |

---

## Say it out loud (interview narration)

> *"I do one post-order DFS where each call reports back whether p or q was found in its subtree. Base case: if the current node is null or is p or q, I return it. Otherwise I recurse both sides. If both sides come back non-null, p and q split at this node, so it's the lowest common ancestor — I return it. If only one side is non-null, I pass that up. The self-ancestor case falls out because finding p stops the descent and represents its whole subtree. One pass, O(n) time, O(h) stack. The alternative is building both root-to-node paths and taking the last shared node, but that's two passes and extra storage. If it were a BST I'd exploit ordering to descend in O(h) without visiting everything."*

## Related / follow-ups
- **235. LCA of a Binary Search Tree** (use BST ordering — descend left/right by value comparison)
- **1650. LCA III** (nodes have parent pointers — walk up like list intersection)
- **160. Intersection of Two Linked Lists** (same "where do two paths meet" idea)
- **257 / 112** (root-to-node path building, used by the brute-force variant)
