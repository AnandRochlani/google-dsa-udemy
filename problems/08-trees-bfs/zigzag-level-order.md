# Binary Tree Zigzag Level Order Traversal

> **LeetCode:** 103. Binary Tree Zigzag Level Order Traversal · **Difficulty:** 🟡 Medium · **Pattern:** Tree BFS · **Google frequency:** ⭐ high

---

## Problem

Given the root of a binary tree, return its node values level by level, but **alternating direction**: level 0 left-to-right, level 1 right-to-left, level 2 left-to-right, and so on (a boustrophedon / "snake" order).

**Example:**

```
        3
       / \
      9   20
         /  \
        15   7
```

`root = [3, 9, 20, null, null, 15, 7]` → `[[3], [20, 9], [15, 7]]`

Level 0 → `[3]` (L→R). Level 1 → `[20, 9]` (R→L, reversed). Level 2 → `[15, 7]` (L→R again).

**Constraints that matter:** up to `2000` nodes. Same as plain level order — the *only* new requirement is flipping direction every other level.

---

## 🧠 Intuition — how you'd actually arrive at this

- **Start from what you know:** this is [Level Order Traversal (102)](level-order-traversal.md) with one twist. The traversal itself is identical BFS — you still visit the tree in horizontal layers. So reach for the same queue + level-size loop.
- **The twist:** every odd-indexed level must be reversed. The naive instinct — "traverse right-to-left by enqueuing children in the opposite order" — is a trap: it corrupts the queue ordering for *subsequent* levels because children get enqueued out of natural order. Keep the **traversal** left-to-right and consistent; only flip **how you record** each level.
- **The clean move:** always dequeue left-to-right (so children go in normally), but track a `left_to_right` boolean. On left-to-right levels append values to the end of the level list; on right-to-left levels prepend to the front (or just build normally and reverse). A `deque` for the level list makes append-front O(1) and avoids an explicit reverse.
- **Pattern trigger:** **"level order but zigzag / snake / alternating" → plain BFS, flip only the collection order per level.** Never mess with the queue's enqueue order to fake direction — separate *traversal order* from *output order*.

---

## ① Brute Force

Do a completely ordinary level-order traversal (collect every level L→R), then post-process: walk the result and reverse every odd-indexed level.

```python
from collections import deque

def zigzag_bruteish(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    for i in range(len(result)):
        if i % 2 == 1:
            result[i].reverse()     # extra O(width) pass per odd level
    return result
```

**Why it's the natural first attempt:** "just do level order, then fix it up" is the obvious decomposition, and it's genuinely fine — same O(n) asymptotics.

**Why we can do slightly better in one pass:** the separate reversal pass re-touches half the nodes. We can fold the direction into the single BFS pass so no second loop is needed — cleaner, and it shows you thought about it.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

One BFS pass. Traverse consistently L→R; use a `deque` per level and append to whichever end the current direction dictates.

```python
from collections import deque

def zigzagLevelOrder(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    left_to_right = True
    while queue:
        level = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)      # add to back
            else:
                level.appendleft(node.val)  # add to front → reversed
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(list(level))
        left_to_right = not left_to_right
    return result
```

**Walk the example:**

| level | left_to_right | dequeued L→R | recorded | result so far |
|---|---|---|---|---|
| 0 | True | 3 | `[3]` | `[[3]]` |
| 1 | False | 9, 20 → appendleft each | `[20, 9]` | `[[3], [20, 9]]` |
| 2 | True | 15, 7 | `[15, 7]` | `[[3], [20, 9], [15, 7]]` |

Note the queue always enqueued children in natural left-to-right order (9's/20's children); only the *recording* end flipped.

**Why it's correct:** the BFS visitation order never changes, so levels are always correctly partitioned and children always in natural order. The `left_to_right` flag only controls *which end of the level list* each value lands on — `appendleft` on odd levels produces exactly the reversed sequence, in one pass, without disturbing anything downstream.

**Complexity:** Time `O(n)` — one visit per node, and `appendleft` on a `deque` is O(1). Space `O(n)`.

---

## ③ Space Optimization

Output is O(n), so total space can't drop below that. Auxiliary space is the BFS queue at **O(w)** (max width) — identical to plain level order; zigzag adds nothing.

Using a `deque` for the per-level list is the key detail: if you used a plain Python `list` and called `insert(0, val)`, each front-insert is O(width), making a level O(width²). The `deque.appendleft` keeps it O(1). The brute-force `list.reverse()` version is also fine (O(width) per level, O(n) total) — the deque version just avoids the extra pass.

> Space is already optimal (bounded by the required output). The refinement here is *time-constant* — one pass instead of two, and O(1) front-inserts via `deque`.

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    boolean leftToRight = true;
    while (!queue.isEmpty()) {
        int size = queue.size();
        LinkedList<Integer> level = new LinkedList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (leftToRight) level.addLast(node.val);
            else             level.addFirst(node.val);
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
        leftToRight = !leftToRight;
    }
    return result;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Level order + reverse odd levels | O(n) | O(n) |
| One-pass BFS with deque (optimised) | O(n) | O(n) output + O(w) queue |

---

## Say it out loud (interview narration)

> *"It's plain level-order BFS with one twist — alternate levels are reversed. The mistake to avoid is enqueuing children right-to-left to fake the direction; that corrupts ordering for later levels. Instead I keep the traversal strictly left-to-right and just flip a boolean each level. On left-to-right levels I append to the back of the level list; on right-to-left levels I append to the front of a deque, which is O(1). One pass, O(n) time, O(w) queue space. Alternatively I'd do a normal level order and reverse every odd level at the end — same complexity, one extra pass."*

## Related / follow-ups
- **102. Level Order Traversal** (the base pattern, no flipping)
- **199. Right Side View** (last node per level)
- **107. Level Order Bottom-Up** (reverse the outer list)
