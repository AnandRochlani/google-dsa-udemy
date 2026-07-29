# Step-By-Step Directions From a Binary Tree Node to Another

> **LeetCode:** 2096. Step-By-Step Directions From a Binary Tree Node to Another · **Difficulty:** 🟡 Medium · **Pattern:** Tree DFS / Lowest Common Ancestor · **Google frequency:** ⭐ high

---

## Problem

You're given the `root` of a binary tree with `n` nodes, and every node has a **unique** value. You're also handed a `startValue` and a `destValue`. Return the **shortest** path from the start node to the destination node as a string of moves, where each character is:

- `'L'` — go to the **left child**
- `'R'` — go to the **right child**
- `'U'` — go to the **parent**

In a tree the shortest path between any two nodes is unique: you walk **up** from the start to the two nodes' lowest common ancestor, then **down** to the destination. So the answer always looks like some run of `U`s followed by some run of `L`/`R`s.

**Example:** `root = [5,1,2,3,null,6,4]`, `startValue = 3`, `destValue = 6` → `"UURL"`

```
        5
       / \
      1   2
     /   / \
    3   6   4
```

*(From `3` you go up to `1`, up to `5` — that's `"UU"`. Then down: right to `2`, left to `6` — that's `"RL"`. Glue them: `"UURL"`.)*

**Constraints that matter:** `n` can be up to `10^5`, so anything worse than a couple of linear passes is trouble. The values are **unique**, which is what lets us search for a value and trust there's exactly one node holding it. The path string itself can be `O(n)` long (a skewed tree), so the answer is inherently linear in size — you can't beat `O(n)`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "I need the path *between* two nodes. In a tree, two nodes meet at their **lowest common ancestor** — so let me find the LCA, then figure out how to get from start up to it, and from it down to dest." That instinct is correct and it's the whole problem. The only question is how cleanly you execute it.
- **Where it hurts:** the literal version does three separate jobs — run a classic LCA search to find the meeting node, then a DFS from the LCA down to `startValue` to count how far up you climb, then another DFS from the LCA down to `destValue`. Three traversals, three chances to fumble the recursion. It works, but it's more moving parts than you need.
- **The leap:** forget finding the LCA node explicitly. Instead, record the path **from the root** to `startValue` as a string of `L`/`R`, and the path from the root to `destValue` the same way. Both paths start at the root, so they **share a common prefix** — and that shared prefix is *exactly* the path down to the LCA. Strip it off. What's left of the start path is how far below the LCA the start node sits; what's left of the dest path is how to get from the LCA down to dest. **Every leftover step on the start side becomes a `'U'`** (you're undoing those downward moves by climbing back up), and the dest leftovers stay as-is. The LCA never has to be named — the strip *is* the LCA.
- **Pattern trigger:** **"shortest path between two tree nodes"** → **root-to-node paths + strip the common prefix**. The transferable move: when two things branch from a common origin, comparing their full paths and discarding the shared head is often cleaner than hunting for the branch point directly.

---

## ① Brute Force

Do it the literal three-step way: find the LCA node with the classic recursive algorithm, then DFS from the LCA down to each target, then combine.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def getDirections_brute(root, startValue, destValue):
    # step 1: classic lowest-common-ancestor search
    def lca(node):
        if not node or node.val == startValue or node.val == destValue:
            return node
        left = lca(node.left)
        right = lca(node.right)
        if left and right:      # start & dest split here → this is the LCA
            return node
        return left or right

    ancestor = lca(root)

    # step 2: DFS from a node down to `target`, recording L/R moves
    def path_to(node, target, acc):
        if not node:
            return False
        if node.val == target:
            return True
        acc.append('L')
        if path_to(node.left, target, acc):
            return True
        acc[-1] = 'R'
        if path_to(node.right, target, acc):
            return True
        acc.pop()               # dead end — backtrack this step
        return False

    up, down = [], []
    path_to(ancestor, startValue, up)     # LCA → start (these become U's)
    path_to(ancestor, destValue, down)    # LCA → dest (stay as L/R)

    return 'U' * len(up) + ''.join(down)
```

**Why it's the natural first attempt:** it's a direct translation of the mental model — "meet at the LCA, climb up, walk down." Each piece is a textbook subroutine you already know.

**Why it's not enough:** it *works* and it's even the same big-O, but it's three traversals and two different recursive helpers doing very similar things. That's surface area for bugs — a mishandled `None`, a forgotten backtrack — under interview pressure. We can fold the LCA discovery into the path-finding itself and cut the whole thing to two clean passes.

**Complexity:** Time `O(n)` (a constant number of full traversals), Space `O(n)` for the recursion and path strings.

---

## ② Optimised Solution

One helper: find the root-to-target path as an `L`/`R` string. Call it for start and for dest. Strip the shared prefix. Turn the start leftovers into `U`s and append the dest leftovers.

```python
def getDirections(root, startValue, destValue):
    # DFS from root to `target`, building the L/R path in `acc`.
    # Returns True once found so the caller stops; backtracks on dead ends.
    def find(node, target, acc):
        if not node:
            return False
        if node.val == target:
            return True
        acc.append('L')
        if find(node.left, target, acc):
            return True
        acc[-1] = 'R'                 # reuse the slot: try right instead
        if find(node.right, target, acc):
            return True
        acc.pop()                     # neither subtree had it — undo this step
        return False

    start_path, dest_path = [], []
    find(root, startValue, start_path)
    find(root, destValue, dest_path)

    # strip the common prefix — that shared head is the path down to the LCA
    i = 0
    while (i < len(start_path) and i < len(dest_path)
           and start_path[i] == dest_path[i]):
        i += 1

    # start leftovers → climb up (U's); dest leftovers → walk down (unchanged)
    return 'U' * (len(start_path) - i) + ''.join(dest_path[i:])
```

**Walk the example** `root = [5,1,2,3,null,6,4]`, `startValue = 3`, `destValue = 6`:

| Step | What happens | Result |
|---|---|---|
| Find path to `3` | root `5` → left to `1` → left to `3` | `start_path = "LL"` |
| Find path to `6` | root `5` → right to `2` → left to `6` | `dest_path = "RL"` |
| Strip common prefix | compare `L` vs `R` at index 0 → already differ | `i = 0` (LCA is root `5`) |
| Build `U`s | start leftovers `"LL"` has length 2 | `"UU"` |
| Append dest leftovers | `dest_path[0:]` = `"RL"` | `"RL"` |
| Glue | `"UU"` + `"RL"` | **`"UURL"`** ✅ |

Here the paths diverge immediately, so the LCA is the root and nothing is stripped. To see the strip actually bite: for `startValue = 3`, `destValue = 4`, the paths are `"LL"` and `"RR"` — still divergent at index 0. But for two nodes on the same side, say start `3` (`"LL"`) and dest a deeper left node, the shared `"L"` would be consumed by the `while` and only the *below-LCA* portion would survive. That common `"L"` is precisely the walk down to their LCA — which neither node needs to include.

**Why it's correct:** `find` records the exact sequence of left/right turns from the root to a node, and because values are unique that node is unique. Two root-paths share a prefix iff they pass through the same ancestors; the **last** shared position is the lowest common ancestor. Everything after the shared prefix on the start side are downward moves *below* the LCA — to get from start to the LCA you reverse them, and reversing any downward move (`L` or `R`) is a single `U`, so their **count** is all that matters (that's why we emit `'U' * (len - i)` and throw the actual letters away). Everything after the prefix on the dest side is the fresh descent from the LCA to dest, kept verbatim. Concatenated, that's the unique shortest path.

**Complexity:** Time `O(n)` — two root-to-node searches, each at most a full traversal, plus an `O(len)` prefix scan. Space `O(n)` for the path strings and recursion stack.

---

## ③ Space Optimization

**Already optimal — and here's the honest reason.** The two things consuming space are the recursion stack (up to `O(h)`, and `h` can be `n` in a skewed tree) and the path strings (up to `O(n)`). But the **answer itself** can be `O(n)` characters long — climb up half the tree and back down the other half — so you can't return the result without materializing `O(n)` characters. The path buffers *are* the deliverable in disguise.

```python
# No smaller variant exists. The output string is O(n) in the worst case,
# so O(n) space is the floor. We hold two L/R buffers instead of building
# and reversing an explicit LCA path — the strip trick already avoids any
# third traversal, which is the only real waste there was to cut.
```

You could shave a constant by finding both paths in a single DFS that stops once it has located both values, but that doesn't change the asymptotics — both time and space stay `O(n)`.

**Complexity:** Time `O(n)`, Space `O(n)` (output-bound; the path string you must return sets the floor).

> Say it out loud: *"Space is O(n), but that's the length of the path I'm required to return — a skewed tree forces a linear-length answer — so O(n) is the floor, not overhead."* Naming why you can't shrink it is the strong-hire move.

---

## Java (for Java interviewers)

```java
public String getDirections(TreeNode root, int startValue, int destValue) {
    StringBuilder startPath = new StringBuilder();
    StringBuilder destPath  = new StringBuilder();
    find(root, startValue, startPath);
    find(root, destValue,  destPath);

    // strip the shared prefix (the path down to the LCA)
    int i = 0;
    int min = Math.min(startPath.length(), destPath.length());
    while (i < min && startPath.charAt(i) == destPath.charAt(i)) i++;

    // start leftovers → U's; dest leftovers → kept as-is
    StringBuilder ans = new StringBuilder();
    for (int k = i; k < startPath.length(); k++) ans.append('U');
    ans.append(destPath.substring(i));
    return ans.toString();
}

// DFS from node to target, recording L/R; backtracks on dead ends.
private boolean find(TreeNode node, int target, StringBuilder path) {
    if (node == null) return false;
    if (node.val == target) return true;

    path.append('L');
    if (find(node.left, target, path)) return true;
    path.setCharAt(path.length() - 1, 'R');   // reuse slot: try right
    if (find(node.right, target, path)) return true;
    path.deleteCharAt(path.length() - 1);       // undo this step
    return false;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (explicit LCA + two descents) | O(n) | O(n) |
| Optimised (two root-paths, strip prefix) | O(n) | O(n) |
| Space-optimised | — (none exists) | O(n) output-bound |

*(n = number of nodes; the answer string is itself up to O(n) long.)*

---

## Say it out loud (interview narration)

> *"The shortest path between two tree nodes goes up to their lowest common ancestor, then down to the target — so the answer is a run of U's then a run of L/R's. Instead of finding the LCA explicitly, I'll record the root-to-start path and the root-to-dest path as L/R strings. They share a common prefix, and that prefix is exactly the walk down to the LCA — so I strip it. Whatever's left on the start side are downward moves I now have to undo by climbing, and reversing any single move is one U, so I just count them. Whatever's left on the dest side is the descent from the LCA down, kept as-is. Concatenate and I'm done. Two traversals plus a prefix scan — O(n) time, O(n) space, and that space is the answer's own length so it's optimal."*

Before you code, ask the clarifying question that proves you understood the shape: *"Values are unique, right? So searching by value lands on exactly one node?"* That's the assumption the whole approach leans on, and surfacing it early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Lowest Common Ancestor of a Binary Tree (LC 236)** — the core subroutine; this problem is LCA wearing a costume.
- **Binary Tree Paths (LC 257)** — the same root-to-node path-building DFS, without the strip.
- **Path Sum II (LC 113)** — DFS that accumulates a path and backtracks, same skeleton.
- **Smallest String Starting From Leaf (LC 988)** — build root-to-leaf strings and compare, a cousin of the path-string idea.
