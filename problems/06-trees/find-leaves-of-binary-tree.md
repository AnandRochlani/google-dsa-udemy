# Find Leaves of Binary Tree

> **LeetCode:** 366. Find Leaves of Binary Tree · **Difficulty:** 🟡 Medium · **Pattern:** Tree DFS (height grouping) · **Google frequency:** ⭐ high

---

## Problem

You're given the root of a binary tree. Repeatedly do this: collect **all the current leaves** into a group, then **remove** them from the tree. Removing those leaves exposes a new layer of leaves. Collect and remove those too. Keep going until the tree is empty. Return a **list of lists** — each inner list is the set of node values you stripped off in that round, in order.

**Example:** `root = [1, 2, 3, 4, 5]` → `[[4, 5, 3], [2], [1]]`

```
        1
       / \
      2   3
     / \
    4   5
```

*(Round 1: the leaves are `4`, `5`, `3` → strip them. Round 2: with those gone, `2` is now a leaf → strip it. Round 3: only `1` remains → strip it.)*

**Constraints that matter:** the tree has up to `~10^4` nodes. The naive "prune a layer, rescan the whole tree, repeat" is `O(n)` per round and the tree can have `O(n)` rounds (a degenerate path), so it's `O(n²)` worst case. We want a **single pass**, `O(n)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** simulate exactly what the problem says. Find all leaves, record them, delete them, repeat until the tree's gone. It's a faithful translation of the words — and it works. The trouble is you re-walk the *entire* tree once per round just to peel off one thin layer.
- **Where it hurts:** every round rescans every surviving node to answer "are you a leaf now?" A tall skinny tree peels one node per round → `n` rounds × `n` work = quadratic. You're throwing away everything you learned about the tree's shape each round and rediscovering it.
- **The leap:** stop thinking about *rounds* and ask a per-node question instead — **"which round does *this* node get removed in?"** Look at the example. `4`, `5`, `3` leave in round 0. `2` (whose children are both leaves) leaves in round 1. `1` leaves in round 2. That number — the round a node is removed in — is exactly its **height above the leaves**: distance from the node down to its deepest descendant leaf. A leaf has height 0 (removed first), its parent height 1, and so on. So `round(node) = height(node) = 1 + max(height(left), height(right))`, with a missing child contributing `-1` so a real leaf lands at 0.
- **Pattern trigger:** **"peel layers off a tree from the outside in"** → **group nodes by height-from-the-bottom in one post-order DFS**. The transferable move is realizing a *repeated global operation* (strip the leaves, again and again) collapses into a *single local quantity* (each node's height). Compute the height bottom-up once, and bucket each node into `result[height]`. One pass, every node filed into the correct round.

---

## ① Brute Force

Literally do what the problem describes: repeatedly find every current leaf, record their values, detach them, and loop until the tree is empty.

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_leaves_brute(root: Optional[TreeNode]) -> List[List[int]]:
    res = []

    def collect_and_prune(node):
        # returns None if this node IS a leaf (so the parent detaches it),
        # otherwise returns the node with its leaf-children pruned.
        if node is None:
            return None
        if node.left is None and node.right is None:
            this_round.append(node.val)   # it's a current leaf → record it
            return None                    # tell the parent to drop this child
        node.left = collect_and_prune(node.left)
        node.right = collect_and_prune(node.right)
        return node

    while root:
        this_round = []
        root = collect_and_prune(root)     # one full sweep peels exactly one layer
        res.append(this_round)
    return res
```

**Why it's the natural first attempt:** it mirrors the problem statement word for word — find leaves, remove leaves, repeat. It's easy to reason about and obviously correct.

**Why it's not enough:** each `while` iteration walks *every remaining node* just to peel one layer. On a tree that's essentially a straight line — `1 → 2 → 3 → … → n` — you peel one node per sweep and do `n` sweeps, each touching up to `n` nodes. That's `O(n²)`. You keep re-deriving the tree's shape from scratch every round.

**Complexity:** Time `O(n²)` worst case (path-shaped tree), Space `O(h)` recursion.

---

## ② Optimised Solution

Reframe rounds as **heights**. Do one post-order DFS. Each node returns its height above the leaves — `1 + max(left_height, right_height)`, with a `None` child returning `-1` so a real leaf returns `0`. That returned height **is** the round the node is removed in, so append the node's value into `result[height]`. One pass files every node into the right bucket.

```python
from typing import Optional, List

def find_leaves(root: Optional[TreeNode]) -> List[List[int]]:
    res = []

    def height(node):
        if node is None:
            return -1                       # so a leaf: 1 + max(-1, -1) = 0
        h = 1 + max(height(node.left), height(node.right))
        if h == len(res):                   # first node we've seen at this height
            res.append([])                  # open a new bucket / round
        res[h].append(node.val)             # file this node into its round
        return h

    height(root)
    return res
```

**Walk the example** `root = [1, 2, 3, 4, 5]` (post-order: left subtree, right subtree, node):

| Visit | node | left h | right h | `h = 1+max` | Bucket | `res` after |
|---|---|---|---|---|---|---|
| 1 | `4` | −1 | −1 | 0 | `res[0]` | `[[4]]` |
| 2 | `5` | −1 | −1 | 0 | `res[0]` | `[[4,5]]` |
| 3 | `2` | 0 (`4`) | 0 (`5`) | 1 | `res[1]` | `[[4,5],[2]]` |
| 4 | `3` | −1 | −1 | 0 | `res[0]` | `[[4,5,3],[2]]` |
| 5 | `1` | 1 (`2`) | 0 (`3`) | 2 | `res[2]` | `[[4,5,3],[2],[1]]` |

Final: `[[4, 5, 3], [2], [1]]`. ✅ Note how the visit order (`4`, `5`, then later `3`) naturally lands `3` *after* `4,5` inside `res[0]` — the ordering falls out of the traversal for free.

**Why it's correct:** define `height(node)` = the number of edges from `node` down to its deepest descendant leaf. A leaf has height 0 and is removed in round 0. Any internal node can only be removed once **both** its subtrees are fully stripped away — which happens exactly `1 + max(height(left), height(right))` rounds in, because the deeper subtree governs when this node becomes a leaf. So `round == height` by induction, and since post-order computes a node's height only *after* both children's, each node is filed into `res[height]` exactly once, in the correct round. Using `h == len(res)` to open a new bucket works because we only ever discover a brand-new height when it's exactly one past the current maximum.

**Complexity:** Time `O(n)` — each node visited once. Space `O(n)` — the result holds all `n` values, plus `O(h)` recursion stack.

---

## ③ Space Optimization

**Already optimal — and here's the honest reason.** The output is a list of all `n` node values, just partitioned into rounds. You're *required to return* every value, so the `O(n)` for `res` is the deliverable, not overhead. The only auxiliary cost is the recursion stack, `O(h)` — `O(log n)` on a balanced tree, `O(n)` on a degenerate path. That stack is intrinsic to a DFS on a tree.

```python
# No smaller variant exists: the O(n) output IS the answer.
# You could convert the recursion to an explicit stack to dodge Python's
# recursion-depth limit on a pathological path — same O(h) space, just
# heap instead of call stack. It doesn't change the asymptotics.
```

**Complexity:** Time `O(n)`, Space `O(n)` output-bound (`O(h)` auxiliary beyond the result).

> Say it out loud: *"Space is O(n), but that's the list of values I'm asked to return — my only extra memory is the O(h) recursion stack, which is unavoidable for a tree DFS."* Naming why the floor is where it is beats pretending there's a trick.

---

## Java (for Java interviewers)

```java
public List<List<Integer>> findLeaves(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    height(root, res);
    return res;
}

// returns the node's height above the leaves; a null child is -1 so a leaf is 0
private int height(TreeNode node, List<List<Integer>> res) {
    if (node == null) return -1;
    int h = 1 + Math.max(height(node.left, res), height(node.right, res));
    if (h == res.size()) res.add(new ArrayList<>());  // first node at this height
    res.get(h).add(node.val);                          // file it into its round
    return h;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (peel a layer, rescan, repeat) | O(n²) | O(h) |
| Optimised (one post-order DFS, group by height) | O(n) | O(n) output-bound, O(h) auxiliary |
| Space-optimised | — (none exists) | O(n) output-bound |

*(n = number of nodes, h = tree height.)*

---

## Say it out loud (interview narration)

> *"The naive read of this is to literally strip leaves round by round, but that rescans the whole tree each round — O(n²) on a path-shaped tree. The insight is to flip it into a per-node question: which round does each node leave in? That's exactly its height above the leaves — a leaf is round 0, and a node leaves one round after its deeper subtree is gone. So I do a single post-order DFS returning height = 1 + max of the two child heights, with null as -1 so leaves come out 0, and I append each node's value into result[height]. One pass, O(n) time, and the O(n) space is just the answer I'm returning plus the recursion stack."*

Before coding, ask the one clarifying question that shows you read it: *"Within a round, does the order of the values matter?"* — it usually doesn't, and confirming it lets you lean on the natural traversal order instead of over-engineering.

## Related / follow-ups
- **Maximum Depth of Binary Tree (LC 104)** — the same `1 + max(left, right)` height recursion, without the bucketing.
- **Binary Tree Right Side View (LC 199)** — another "group nodes by a level-like key" tree problem.
- **Delete Leaves With a Given Value (LC 1325)** — post-order pruning where a node becomes a leaf after its children are removed.
- **Diameter of Binary Tree (LC 543)** — same post-order "return a height, combine at the node" shape.
