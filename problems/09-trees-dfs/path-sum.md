# Path Sum

> **LeetCode:** 112. Path Sum · **Difficulty:** 🟢 Easy · **Pattern:** Tree DFS · **Google frequency:** ⭐ high

---

## Problem

Given the root of a binary tree and an integer `targetSum`, return `true` if there exists a **root-to-leaf** path whose node values add up exactly to `targetSum`. A leaf is a node with no children.

**Example:**

```
        5
       / \
      4   8
     /   / \
    11  13  4
   /  \       \
  7    2       1
```

`targetSum = 22` → `true` (path 5 → 4 → 11 → 2 sums to 22).

**Constraints that matter:** up to `5000` nodes; values (and `targetSum`) can be **negative**, so you can't prune a branch just because the running sum already exceeded the target. The path must end at a **leaf** — not just any node where the sum happens to match.

---

## 🧠 Intuition — how you'd actually arrive at this

- **What shape is the answer?** A yes/no about a *root-to-leaf path*. "Path from root to leaf" is the DFS signature — you follow a single branch all the way down, and DFS naturally walks one root-to-leaf path at a time.
- **The return-value thinking:** stand at a node with a target you still need to reach. Subtract the node's value — now your children need to make up `target - node.val`. Recurse. The recursion answers *"can the subtree rooted here hit this remaining amount along a root-to-leaf path?"* Each node just asks its children the smaller version of the same question.
- **Where the leaf condition lives:** the success check fires **only at a leaf**: "am I a leaf *and* is the remaining target now exactly my value?" You must not return true at an internal node even if the running sum matches — the path has to reach a leaf.
- **Why not prune on overshoot?** Because values can be negative, a path that's "too big" now can be pulled back down later. So you genuinely explore every root-to-leaf path (unless you get an early true).
- **Pattern trigger:** **"does a root-to-leaf path satisfy property X?" → DFS carrying an accumulator (running sum or remaining target), test the property at leaves.**

---

## ① Brute Force

Enumerate **every** root-to-leaf path explicitly (build the list of values down each branch), sum each, and check for a match. Correct but it materializes full paths and sums them separately — redundant work and O(n·h) in the worst case for building path lists.

```python
def hasPathSum_bruteish(root, targetSum):
    if not root:
        return False
    paths = []
    def collect(node, path):
        path = path + [node.val]                # new list each step (copy)
        if not node.left and not node.right:
            paths.append(path)
            return
        if node.left:  collect(node.left, path)
        if node.right: collect(node.right, path)
    collect(root, [])
    return any(sum(p) == targetSum for p in paths)
```

**Why it's the natural first attempt:** "find a path that sums to X" → literally build the paths and sum them. Direct and obviously correct.

**Why it's wasteful:** it stores every path (up to O(n) paths of length up to O(h) → O(n·h) space) and re-sums each from scratch. We don't need the paths themselves — only whether *one* works — so we can carry a running remainder and short-circuit.

**Complexity:** Time `O(n·h)` (copying/summing paths), Space `O(n·h)`.

---

## ② Optimised Solution

DFS carrying the **remaining** target. At each node subtract its value; succeed exactly at a leaf whose value finishes the target.

```python
def hasPathSum(root, targetSum):
    if not root:
        return False
    # leaf: succeed iff the remaining target equals this node's value
    if not root.left and not root.right:
        return targetSum == root.val
    remaining = targetSum - root.val
    return (hasPathSum(root.left, remaining) or
            hasPathSum(root.right, remaining))
```

**Walk the example** (`targetSum = 22`):

- `5`: not a leaf. remaining = 22 − 5 = 17. Try left subtree (4) with 17.
- `4`: not a leaf. remaining = 17 − 4 = 13. Try left (11) with 13.
- `11`: not a leaf. remaining = 13 − 11 = 2. Try left (7) with 2 → 7 is a leaf, `2 == 7`? no. Try right (2) with 2 → 2 is a leaf, `2 == 2`? **yes → True**, which short-circuits all the way up. ✅

The `or` means the moment any branch returns true, we stop exploring the rest.

**Why it's correct:** define the recursion's contract as "returns true iff some root-to-leaf path *within this subtree* sums to `targetSum`." At a leaf that reduces to a single equality check. At an internal node, a qualifying path must go through one of the children with the target reduced by this node's value — exactly the `or` of the two recursive calls. Induction closes it.

**Complexity:** Time `O(n)` — each node visited at most once. Space `O(h)` recursion stack. No path lists, no re-summing.

---

## ③ Space Optimization

Auxiliary space is the recursion stack, **O(h)** — O(log n) balanced, O(n) skewed. That's already optimal for a DFS that must be able to reach any leaf.

- We carry a single integer (`remaining`) rather than path lists — that's the improvement over brute force.
- An **iterative** version with an explicit stack of `(node, remaining)` pairs achieves the same O(h) and sidesteps recursion limits:

```python
def hasPathSum_iter(root, targetSum):
    if not root:
        return False
    stack = [(root, targetSum)]
    while stack:
        node, rem = stack.pop()
        if not node.left and not node.right and rem == node.val:
            return True
        if node.left:  stack.append((node.left, rem - node.val))
        if node.right: stack.append((node.right, rem - node.val))
    return False
```

> O(h) is the floor for any traversal that may descend to the deepest leaf. Nothing to shave beyond choosing recursion vs an explicit stack.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public boolean hasPathSum(TreeNode root, int targetSum) {
    if (root == null) return false;
    if (root.left == null && root.right == null)
        return targetSum == root.val;                 // leaf check
    int remaining = targetSum - root.val;
    return hasPathSum(root.left, remaining)
        || hasPathSum(root.right, remaining);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Enumerate all paths | O(n·h) | O(n·h) |
| DFS with running remainder (optimised) | O(n) | O(h) |
| Iterative DFS | O(n) | O(h) |

---

## Say it out loud (interview narration)

> *"It's a root-to-leaf path question, so DFS. Instead of building paths and summing them, I carry the remaining target down: subtract each node's value, and at a leaf I check whether the remainder equals that leaf's value. Any child returning true short-circuits via the or. The one subtlety is that success is only valid at a leaf — matching the sum at an internal node doesn't count. And because values can be negative I can't prune on overshoot. O(n) time, O(h) stack."*

## Related / follow-ups
- **113. Path Sum II** (return *all* qualifying paths — now you do carry the path + backtrack)
- **437. Path Sum III** (any node to any downward node — prefix-sum hashmap)
- **129. Sum Root to Leaf Numbers** (same DFS, build a number down each path)
- **257. Binary Tree Paths** (list every root-to-leaf path — backtracking)
