# Validate Binary Search Tree

> **LeetCode:** 98. Validate Binary Search Tree · **Difficulty:** 🟡 Medium · **Pattern:** Tree DFS · **Google frequency:** ⭐ high

---

## Problem

Given the root of a binary tree, return `true` if it is a valid **binary search tree (BST)**. A valid BST requires: every node's value is **strictly greater than all values in its left subtree** and **strictly less than all values in its right subtree** — recursively, for every node.

**Example (invalid):**

```
        5
       / \
      1   4        ← 4 is in 5's RIGHT subtree, so it must be > 5. It isn't.
         / \
        3   6
```

`root = [5, 1, 4, null, null, 3, 6]` → `false`. Locally `3 < 4 < 6` looks fine, but 3 and 4 sit in 5's right subtree and are less than 5 — a violation.

**Example (valid):** `[2, 1, 3]` → `true`.

**Constraints that matter:** up to `10^4` nodes; values can be as extreme as the full 32-bit range (including `INT_MIN`/`INT_MAX`), so sentinel bounds must use `±infinity`, not integer limits. The subtle trap: **checking only parent-child (`left < node < right`) is wrong** — validity is about the *entire* subtree, not immediate children.

---

## 🧠 Intuition — how you'd actually arrive at this

- **The tempting wrong answer first:** "check each node is greater than its left child and less than its right child." The example above kills it: node 3 is a valid *right*-then-left descendant of 5 but violates the BST because it's less than an *ancestor* (5). Local checks miss ancestor constraints.
- **The real invariant:** as you walk *down* the tree, each node lives inside an **allowed range** `(low, high)`. The root can be anything: `(-∞, +∞)`. Going **left**, everything must be smaller than the current node, so the upper bound tightens to `node.val`: new range `(low, node.val)`. Going **right**, everything must be larger, so the lower bound tightens: `(node.val, high)`. A node is valid iff `low < node.val < high`, and both subtrees are valid under their tightened ranges.
- **Why ranges (not just parent compares):** the range *accumulates* every ancestor constraint. When we reach 3, its allowed range has been squeezed to `(low=?, high=5)` inherited from the left-turn at 5 — wait, 3 is under 5's *right*, so its range is `(5, +∞)` region... and 3 < 5 fails immediately. The bounds carry the ancestor rule down automatically.
- **The return-value thinking:** *"what do I return up? A boolean: is my whole subtree a valid BST given the range I inherited?"* Combine children with `and`. What flows *down* is the (low, high) window; what flows *up* is validity.
- **Alternative lens:** an **in-order traversal of a BST is strictly increasing.** So another correct approach is: do in-order, verify each value is strictly greater than the previous. Equivalent, and elegant.
- **Pattern trigger:** **"validate a global tree property that depends on ancestors" → DFS carrying tightening (low, high) bounds** — or in-order + monotonic check.

---

## ① Brute Force

The naive framing is either (a) the **wrong** local-only check, or (b) a genuinely correct but heavier approach: for each node, scan its entire left subtree to confirm all are smaller and its entire right subtree to confirm all are larger. Correct, but re-scans subtrees repeatedly → **O(n²)**.

```python
def isValidBST_brute(root):
    def all_less(node, val):
        if not node: return True
        return node.val < val and all_less(node.left, val) and all_less(node.right, val)
    def all_greater(node, val):
        if not node: return True
        return node.val > val and all_greater(node.left, val) and all_greater(node.right, val)

    def check(node):
        if not node:
            return True
        # verify EVERY node in left subtree < node.val, every node in right > node.val
        if not all_less(node.left, node.val):    return False
        if not all_greater(node.right, node.val): return False
        return check(node.left) and check(node.right)
    return check(root)
```

**Why it's the natural (correct) first attempt:** it directly encodes the definition — "everything in the left subtree is smaller, everything in the right is larger."

**Why it's not enough:** `all_less`/`all_greater` walk whole subtrees, nested inside `check` which also visits every node → **O(n²)**. Same recompute trap as diameter. We can pass bounds down instead of re-scanning.

**Complexity:** Time `O(n²)`, Space `O(h)`.

---

## ② Optimised Solution

DFS carrying an open interval `(low, high)`. Tighten it going down; a node is valid iff it fits its window and both subtrees are valid.

```python
def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True                       # empty subtree is a valid BST
        if not (low < node.val < high):       # strict bounds
            return False
        return (valid(node.left,  low, node.val) and   # left: cap high at node.val
                valid(node.right, node.val, high))     # right: raise low to node.val
    return valid(root, float('-inf'), float('inf'))
```

**Walk the invalid example** `[5, 1, 4, null, null, 3, 6]`:

- `valid(5, -∞, +∞)`: `-∞ < 5 < +∞` ✅. Recurse left with `(-∞, 5)`, right with `(5, +∞)`.
- Left `valid(1, -∞, 5)`: `-∞ < 1 < 5` ✅. Its children null → ok.
- Right `valid(4, 5, +∞)`: check `5 < 4 < +∞` → `5 < 4` is **false** → returns **False**. ✅ (Caught immediately: 4 must exceed 5 because it's in 5's right subtree.)

The whole tree returns `False`. The range `(5, +∞)` encoded the ancestor rule that pure parent-child checks would have missed.

**Why it's correct:** the invariant is *"`valid(node, low, high)` is true iff the subtree at `node` is a BST whose every value lies strictly in `(low, high)`."* Turning left tightens `high` to the parent's value (left descendants must be smaller than the parent); turning right tightens `low`. So by construction the window at any node equals the intersection of all ancestor constraints. A node passing `low < val < high` therefore satisfies *all* ancestors, not just its parent.

**Complexity:** Time `O(n)` — each node checked once. Space `O(h)` recursion stack.

---

## ③ Space Optimization

Recursion is **O(h)**. The in-order approach can reach **O(1)** auxiliary via Morris traversal, and it's a genuinely nice alternative here:

**In-order + previous value** (O(h) stack, but no bounds bookkeeping):

```python
def isValidBST_inorder(root):
    prev = float('-inf')
    stack = []
    node = root
    while stack or node:
        while node:                 # go left as far as possible
            stack.append(node)
            node = node.left
        node = stack.pop()
        if node.val <= prev:        # must be STRICTLY increasing
            return False
        prev = node.val
        node = node.right
    return True
```

- **Bounds DFS:** O(h) stack. Simple, most common answer.
- **Iterative in-order:** O(h) explicit stack; relies on the "in-order of a BST is sorted" fact.
- **Morris in-order:** rewires threads to traverse in **O(1)** extra space — the only way to truly beat O(h). Mention it if pushed for constant space; it's fiddly and rarely required.

> For a balanced tree O(h) = O(log n) is already fine. Morris is the O(1) escape hatch if the interviewer insists on constant auxiliary space.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public boolean isValidBST(TreeNode root) {
    return valid(root, null, null);   // use Long bounds or null sentinels
}
private boolean valid(TreeNode node, Integer low, Integer high) {
    if (node == null) return true;
    if (low != null && node.val <= low)  return false;
    if (high != null && node.val >= high) return false;
    return valid(node.left, low, node.val)
        && valid(node.right, node.val, high);
}
```

*(Using `Integer` bounds with `null` sentinels avoids the `INT_MIN`/`INT_MAX` overflow trap that `long` bounds also solve.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Re-scan subtrees (brute) | O(n²) | O(h) |
| Bounds DFS (optimised) | O(n) | O(h) |
| Iterative in-order | O(n) | O(h) |
| Morris in-order | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"The trap is that checking each node against just its children is wrong — validity depends on all ancestors. So I carry a range down: root is (-∞, +∞); going left I tighten the upper bound to the current value, going right I raise the lower bound. A node is valid if it's strictly inside its window and both subtrees are valid under their tightened windows. That catches an ancestor violation like a node in the right subtree being smaller than a grandparent. O(n) time, O(h) stack. Alternatively, an in-order traversal of a BST is strictly increasing, so I could verify each value exceeds the previous — and Morris makes that O(1) space."*

## Related / follow-ups
- **94. Binary Tree Inorder Traversal** (the sorted-order fact this leans on)
- **99. Recover Binary Search Tree** (find the two swapped nodes via in-order)
- **230. Kth Smallest in a BST** (in-order, stop at k)
- **235. LCA of a BST** (exploit BST ordering to descend)
