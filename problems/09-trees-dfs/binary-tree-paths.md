# Binary Tree Paths

> **LeetCode:** 257. Binary Tree Paths · **Difficulty:** 🟢 Easy · **Pattern:** Tree DFS (backtracking) · **Google frequency:** medium

---

## Problem

Given the root of a binary tree, return **all root-to-leaf paths** as strings, each formatted like `"1->2->5"`.

**Example:**

```
    1
   / \
  2   3
   \
    5
```

`root = [1, 2, 3, null, 5]` → `["1->2->5", "1->3"]`

Two leaves (5 and 3), so two paths. Order of the paths doesn't matter.

**Constraints that matter:** up to `100` nodes. The output is *every* path, so you can't short-circuit — this is a full traversal that **records the trail** as it descends and **unwinds** it on the way back up. That unwinding is the backtracking flavor.

---

## 🧠 Intuition — how you'd actually arrive at this

- **What's asked?** Not a yes/no or a number — the *actual list of paths*. So unlike Path Sum, you must carry the trail of nodes with you as you go down, and emit it when you hit a leaf.
- **The DFS + trail idea:** descend depth-first, pushing the current node onto a `path` list. When you reach a leaf, the `path` holds a complete root-to-leaf sequence — join it into a string and save it. Then, crucially, **remove the node from `path` before returning** so a sibling branch doesn't inherit this branch's tail. That push-before-recurse / pop-after-recurse dance is **backtracking**.
- **Why backtracking matters here:** `path` is a single shared list mutated in place. Without the pop, after exploring the left branch the leftover nodes would pollute the right branch's path. The pop restores `path` to exactly the state it had when you entered the node — the defining invariant of backtracking.
- **The tidy alternative:** pass an immutable string down (`path + "->" + val`). No explicit pop needed because each call gets its own copy — the "backtracking" is implicit in the copy. Cleaner to write, marginally more allocation. Both are fine; know both.
- **Pattern trigger:** **"enumerate ALL root-to-leaf paths / combinations" → DFS that appends on the way down and undoes on the way up (backtracking), emitting at leaves.**

---

## ① Brute Force

The "naive" framing is the **immutable-string** version: carry the path so far as a string, and because strings are copied, you never manage a stack manually. It's clean and correct — the only cost is building many intermediate strings.

```python
def binaryTreePaths_strings(root):
    result = []
    def dfs(node, path):
        if not node:
            return
        path = path + str(node.val) if not path else path + "->" + str(node.val)
        if not node.left and not node.right:
            result.append(path)                 # leaf → emit the built string
            return
        dfs(node.left, path)
        dfs(node.right, path)
    dfs(root, "")
    return result
```

**Why it's the natural first attempt:** it needs no explicit backtracking — each recursive call receives its own string copy, so there's nothing to undo. Easiest to get right under pressure.

**Why the backtracking version is "the point":** it teaches the reusable push/pop skill, and it avoids repeatedly copying growing strings — it builds each path once at the leaf. Same O(n·h) total output cost, but the technique generalizes to combinations/permutations problems.

**Complexity:** Time `O(n·h)` (string building along each path), Space `O(n·h)` output + `O(h)` stack.

---

## ② Optimised Solution

DFS with an explicit `path` list and **backtracking** — append on entry, pop on exit, stringify only at leaves.

```python
def binaryTreePaths(root):
    result = []
    path = []
    def dfs(node):
        if not node:
            return
        path.append(str(node.val))              # choose
        if not node.left and not node.right:
            result.append("->".join(path))      # leaf → record the trail
        else:
            dfs(node.left)
            dfs(node.right)
        path.pop()                              # un-choose (backtrack)
    dfs(root)
    return result
```

**Walk the example:**

| action | `path` | `result` |
|---|---|---|
| enter 1 | `[1]` | `[]` |
| enter 2 | `[1, 2]` | `[]` |
| enter 5 (leaf) | `[1, 2, 5]` → emit | `["1->2->5"]` |
| pop 5, pop 2 | `[1]` | `["1->2->5"]` |
| enter 3 (leaf) | `[1, 3]` → emit | `["1->2->5", "1->3"]` |
| pop 3, pop 1 | `[]` | done |

Notice how after finishing the left branch, the pops restore `path` to `[1]` so the right branch (3) starts clean — that's backtracking doing its job.

**Why it's correct:** the invariant is *"on entering and leaving `dfs(node)`, `path` is identical."* The `append`…`pop` pair guarantees it. So every leaf sees a `path` equal to exactly the sequence of ancestors from root to itself, and we emit one string per leaf — precisely the set of root-to-leaf paths.

**Complexity:** Time `O(n·h)` (the join at each leaf costs up to O(h); there are up to O(n) leaves — but total characters emitted is the real bound). Space `O(h)` for `path` + recursion, plus the output.

---

## ③ Space Optimization

Output dominates: the returned strings total up to O(n·h) characters — unavoidable, it's the answer. Auxiliary (non-output) space:

- **Backtracking list version:** one shared `path` of size O(h) + O(h) recursion stack = **O(h)** auxiliary. Best.
- **Immutable-string version:** each stack frame holds its own partial string of length up to O(h), so O(h) frames × O(h) = **O(h²)** transient auxiliary in the worst case, plus more allocation churn.

So the backtracking version is *strictly better on auxiliary space* — that's exactly why it's the "optimised" one, even though both are correct and produce identical output.

> Can't beat the output size. The lever is auxiliary space, where a single mutated `path` (O(h)) beats copying strings down every branch (O(h²) transient).

---

## Java (for Java interviewers)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<String> binaryTreePaths(TreeNode root) {
    List<String> result = new ArrayList<>();
    if (root == null) return result;
    dfs(root, new StringBuilder(), result);
    return result;
}
private void dfs(TreeNode node, StringBuilder path, List<String> result) {
    int len = path.length();                    // remember state to restore
    if (path.length() > 0) path.append("->");
    path.append(node.val);
    if (node.left == null && node.right == null) {
        result.add(path.toString());            // leaf
    } else {
        if (node.left != null)  dfs(node.left, path, result);
        if (node.right != null) dfs(node.right, path, result);
    }
    path.setLength(len);                         // backtrack
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) |
|---|---|---|
| Immutable string down each branch | O(n·h) | O(h²) transient |
| DFS + backtracking list (optimised) | O(n·h) | O(h) |

---

## Say it out loud (interview narration)

> *"I need every root-to-leaf path, so it's a full DFS that records the trail. I keep one path list, append the node when I enter, and when I hit a leaf I join it into a string. The key move is popping the node before I return — backtracking — so after finishing the left branch the path is restored and the right branch starts clean. That shared list is O(h) auxiliary versus copying a growing string down every branch. The output itself is O(n·h) characters, which is unavoidable."*

## Related / follow-ups
- **113. Path Sum II** (paths summing to a target — same backtracking)
- **112. Path Sum** (just yes/no — no need to store paths)
- **46. Permutations / 78. Subsets** (the same choose / un-choose backtracking skeleton on arrays)
- **129. Sum Root to Leaf Numbers** (build a number instead of a string)
