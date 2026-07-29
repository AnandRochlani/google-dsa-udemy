# Binary Tree Level Order Traversal

> **LeetCode:** 102. Binary Tree Level Order Traversal · **Difficulty:** 🟡 Medium · **Pattern:** Tree BFS · **Google frequency:** ⭐ high

---

## Problem

Given the root of a binary tree, return the values of its nodes **level by level**, from top to bottom, left to right — as a list of lists, one inner list per level.

**Example:**

```
        3
       / \
      9   20
         /  \
        15   7
```

`root = [3, 9, 20, null, null, 15, 7]` → `[[3], [9, 20], [15, 7]]`

Level 0 is `[3]`, level 1 is `[9, 20]`, level 2 is `[15, 7]`.

**Constraints that matter:** up to `2000` nodes, values fit in an int. The output shape — **grouped by level** — is the whole point. "Group by level" is the signal that decides the entire approach.

---

## 🧠 Intuition — how you'd actually arrive at this

> The single most useful trigger to memorize for trees: **the word "level" (or "row", or "depth-by-depth") means BFS with a queue.**

- **What does the problem ask?** It doesn't ask about a path, or a height, or whether something is valid. It asks you to *visit nodes in horizontal layers*. That's breadth, not depth.
- **Why BFS fits:** BFS processes nodes in the exact order they sit from the root outward — all distance-0 nodes, then all distance-1 nodes, and so on. That ordering **is** the level ordering the problem wants. A queue naturally gives you FIFO: you enqueue children as you dequeue parents, so a whole generation comes out before the next begins.
- **The one trick that makes it clean:** a plain queue mixes all levels together. To know *where one level ends and the next begins*, snapshot the queue's size at the start of each level — that count is exactly how many nodes are on the current level. Process precisely that many, collecting their values into one list, while enqueuing their children for the next round.
- **Pattern trigger:** **"return nodes grouped by level / row / depth" → BFS with a queue + level-size loop.** Burn in the `for _ in range(len(queue))` idiom; you'll reuse it in zigzag, right-side-view, and every level-based variant.

---

## ① Brute Force

You *can* solve this with DFS: recurse with a `depth` parameter and append each value into `result[depth]`. It works and it's O(n) — but it's the "naive framing" here because it fights the problem's shape. You have to carry a depth counter, create the sublist lazily when you first reach a new depth, and mentally reconstruct level order from a depth-first walk.

```python
def levelOrder_dfs(root):
    result = []
    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):     # first time we reach this depth
            result.append([])
        result[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)
    dfs(root, 0)
    return result
```

**Why it's the natural-but-awkward attempt:** most people are comfortable recursing on trees, so they reach for DFS reflexively. It gives the right answer.

**Why it's not the clean fit:** the problem is *inherently* breadth-first — you're forcing a depth-first traversal to emulate level order via an index bookkeeping trick. It also uses O(h) recursion stack. For a "level" problem, BFS reads more directly and is what an interviewer expects to see first.

**Complexity:** Time `O(n)`, Space `O(n)` (result) + `O(h)` recursion stack.

---

## ② Optimised Solution

BFS with a queue. Snapshot the level size, process that many nodes, collect their values, enqueue their children.

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)          # nodes on THIS level
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**Walk the example** (`[3, 9, 20, null, null, 15, 7]`):

| queue before | level_size | pop & collect | enqueue children | result so far |
|---|---|---|---|---|
| `[3]` | 1 | `[3]` | 9, 20 | `[[3]]` |
| `[9, 20]` | 2 | `[9, 20]` | 15, 7 (9 has none) | `[[3], [9, 20]]` |
| `[15, 7]` | 2 | `[15, 7]` | none | `[[3], [9, 20], [15, 7]]` |
| `[]` | — | — | — | done |

**Why it's correct:** at the top of each `while` iteration the queue holds *exactly* the nodes of one level and nothing else (we only ever enqueue children after finishing a full level's dequeues via the fixed `level_size` count). So each inner `for` loop collects one complete level, left to right, and no node is ever miscounted into the wrong level.

**Complexity:** Time `O(n)` — each node enqueued and dequeued once. Space `O(n)` for the queue (up to the widest level).

---

## ③ Space Optimization

The output itself is O(n), so you can't beat O(n) total. But the *auxiliary* space is worth stating precisely:

- **BFS queue** holds at most one level at a time → **O(w)** where `w` is the maximum width. For a balanced tree the bottom level has ~n/2 nodes, so worst case O(n).
- **DFS recursion** uses **O(h)** stack where `h` is height. For a balanced tree that's O(log n); for a degenerate (linked-list-shaped) tree it's O(n).

So there's a genuine trade-off: **BFS costs width, DFS costs height.** For a wide, bushy tree DFS's O(h) auxiliary space is actually smaller; for a tall skinny tree BFS's O(w) is smaller. Neither is universally cheaper — mention this contrast out loud; it shows you understand *why* you picked BFS (output shape) rather than just defaulting to it.

> Already optimal given the required output. The only real lever is queue-width vs recursion-height, which depends on the tree's shape, not on any cleverness you can add.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| DFS with depth index | O(n) | O(n) output + O(h) stack |
| BFS with queue (optimised) | O(n) | O(n) output + O(w) queue |

---

## Say it out loud (interview narration)

> *"The output is grouped by level, so this is textbook BFS. I push the root into a queue, then loop: at the top of each pass I record the queue's current size — that's exactly one level's worth of nodes — pop that many, collect their values into a sublist, and enqueue their children for the next pass. Each node is touched once, so O(n) time; the queue holds at most the widest level, so O(w) space. You could do it with DFS carrying a depth index, but BFS matches the level-shaped output most directly."*

## Related / follow-ups
- **103. Zigzag Level Order** (same BFS, alternate direction per level)
- **199. Right Side View** (last node of each level)
- **107. Level Order Bottom-Up** (reverse the result list)
- **515. Find Largest Value in Each Row** (max per level instead of the full list)
