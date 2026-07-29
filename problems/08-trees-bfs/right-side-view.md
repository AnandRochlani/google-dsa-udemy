# Binary Tree Right Side View

> **LeetCode:** 199. Binary Tree Right Side View · **Difficulty:** 🟡 Medium · **Pattern:** Tree BFS · **Google frequency:** ⭐ high

---

## Problem

Imagine standing to the **right** of a binary tree. Return the values of the nodes you can see, ordered top to bottom — i.e. the **rightmost node of each level**.

**Example:**

```
        1
       / \
      2   3
       \   \
        5   4
```

`root = [1, 2, 3, null, 5, null, 4]` → `[1, 3, 4]`

From the right you see 1 (level 0), 3 (level 1, rightmost), 4 (level 2, rightmost). Node 2 and 5 are hidden behind 3 and 4.

**Constraints that matter:** up to `100` nodes. The key realization: "right side view" is not about right children — it's about the **last node of each level**. A node with only a left child is still visible if nothing is to its right on that level.

---

## 🧠 Intuition — how you'd actually arrive at this

- **Reframe the ask:** "what do I see from the right?" sounds geometric, but it reduces to a crisp statement: **for each level, the node farthest to the right.** In left-to-right order, that's the *last* node of the level. The common wrong instinct — "just keep going right: root, root.right, root.right.right…" — fails whenever a level's rightmost node is reached via a left child (like node 5 → 4 above, where 4 is a right child but 5 would be visible if 4 didn't exist).
- **Level → BFS:** the moment you rephrase it as "one node per level," the trigger fires: **anything phrased per-level is BFS with a queue.** Do a normal level-order traversal; on each level, the value you want is simply the last one you dequeue.
- **DFS alternative worth knowing:** you can also DFS **right child first**, tracking depth; the *first* node you reach at each new depth is the rightmost. That's elegant and O(h) space. Both are legitimate; BFS maps most obviously to "per level."
- **Pattern trigger:** **"rightmost/leftmost/last node of each level" → BFS, take the boundary element of each level** (last for right view, first for left view).

---

## ① Brute Force

The tempting-but-wrong "just walk right pointers" is not even correct, so it doesn't count as a valid brute force. The honest naive approach is: **compute the full level-order traversal (list of lists), then take the last element of each level.** Correct, but it materializes every level in full when we only need one value from each.

```python
from collections import deque

def rightSideView_naive(root):
    if not root:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        levels.append(level)
    return [level[-1] for level in levels]   # last of each level
```

**Why it's the natural first attempt:** if you already know level-order (102), this is a two-line addition — build all levels, keep the last of each.

**Why it's wasteful:** it stores O(n) values across all levels just to keep O(number-of-levels) of them. We can capture only the rightmost as we go.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

BFS, but only record the **last node of each level** — no full-level lists.

```python
from collections import deque

def rightSideView(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:      # last node in this level
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

**Walk the example:**

| queue before | level_size | last node dequeued | result |
|---|---|---|---|
| `[1]` | 1 | 1 | `[1]` |
| `[2, 3]` | 2 | 3 | `[1, 3]` |
| `[5, 4]` | 2 | 4 | `[1, 3, 4]` |

At level 1 the queue is `[2, 3]` (2 enqueued before 3 because it's the left child), so the last dequeued is 3 — correct. At level 2 it's `[5, 4]` (5 is 2's right child, 4 is 3's right child), last is 4.

**Why it's correct:** within each level the queue holds nodes strictly left-to-right (BFS enqueues left child before right, parents left-to-right), so index `level_size - 1` is by definition the rightmost node — exactly what's visible from the right. Nodes reached via left children are handled correctly because we key off *position in the level*, not off which pointer we followed.

**Complexity:** Time `O(n)`, Space `O(w)` — the queue, and a result of size O(height).

---

## ③ Space Optimization

The DFS variant lowers auxiliary space when the tree is tall and thin. Recurse **right before left**, and record a node the first time you reach a new depth:

```python
def rightSideView_dfs(root):
    result = []
    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):     # first node seen at this depth
            result.append(node.val)  # ...and since we go right-first, it's the rightmost
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)
    dfs(root, 0)
    return result
```

- **BFS:** O(w) queue — worst case O(n) for a balanced tree's wide bottom level.
- **DFS:** O(h) recursion stack — O(log n) balanced, O(n) degenerate.

Same **BFS-width vs DFS-height** trade-off as level order. For a bushy tree, DFS's O(h) is cheaper; for a tall skinny tree, BFS's O(w) is. Say which and why.

> Output is O(number of levels) either way; the choice is purely queue-width vs stack-height. Naming that trade-off is the strong signal.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (i == size - 1) result.add(node.val);   // rightmost of level
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
    }
    return result;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Full level order + take last | O(n) | O(n) |
| BFS, keep last per level (optimised) | O(n) | O(w) |
| DFS right-first | O(n) | O(h) |

---

## Say it out loud (interview narration)

> *"The trick is realizing 'right side view' means the last node of each level, not just following right pointers — a left child can be visible if nothing's to its right. Since it's per-level, I use BFS: for each level I loop over exactly that many nodes and grab the one at the last index. O(n) time, O(w) queue space. If the tree's tall and skinny I'd instead DFS right-child-first and record the first node I hit at each new depth — O(h) stack, which can be cheaper."*

## Related / follow-ups
- **102. Level Order Traversal** (all nodes per level)
- **513. Find Bottom Left Tree Value** (first node of the last level)
- **515. Largest Value in Each Row** (max per level)
- **Left Side View** (symmetric — take the *first* node of each level)
