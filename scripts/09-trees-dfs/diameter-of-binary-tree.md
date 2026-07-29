# 🎬 Recording Script — Diameter of Binary Tree
**Pattern: Tree DFS · LeetCode 543 · Easy · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Maximum Depth (104) — the `1 + max(left, right)` height. This problem *fuses* that with an answer tracked on the side.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree with the longest path glowing — bending at a node, NOT passing through the root. A big red "O(n²)" pulses, then collapses into a green "O(n)".]**

> "Diameter — the longest path between any two nodes." You already know how to compute height. So you write the obvious thing: at every node, add up the left height and right height, take the max.
>
> It's correct. It's also **O(n²)** — and on a big tree it times out. The maddening part? The fix is almost the *same code*, reorganized so height is computed *once* instead of over and over.
>
> This is the single best problem for one of the most important ideas in tree recursion: **return one thing up, track another thing on the side.** Get this and max-path-sum, balanced-tree, and a dozen others fall over. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: the tree.]**

```
        1
       / \
      2   3
     / \
    4   5
```

> One line: **the length of the longest path between any two nodes, counted in edges.** That path may or may not pass through the root.
>
> Longest path here: 4 → 2 → 1 → 3 — that's **3 edges**. Note 4 → 2 → 5 is only 2 edges. So the diameter is 3. And crucially — the winning path *bends* at node 1, going down one side and up... well, down the other.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — feel the O(n²) waste)*

**[VISUAL: at each node, height() being CALLED separately, re-walking the subtree. A "nodes touched" counter ballooning.]**

> Here's the key insight first: any path has one highest point — where it *bends*. At that bend node, the path dives as deep as it can left, and as deep as it can right. So its length is `height(left) + height(right)`. The answer is the best bend over all nodes.
>
> So the obvious code: for every node, call `height(left) + height(right)`, take the max. But watch — `height()` itself walks the *entire* subtree. And I'm calling it at *every* node.
>
> **[VISUAL: node 1 calls height on its whole left subtree; node 2 ALSO walks 4 and 5 again; the same nodes get re-walked at every ancestor. Counter climbing toward n².]**
>
> Node 4 gets visited by height-of-1, height-of-2… the same nodes re-walked at every ancestor. That's a traversal (O(n) nodes) with a full subtree walk *nested inside* it. **O(n²).** On a skewed tree, ~n²/2 operations.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Two nested loops highlighted: "traverse every node" × "height re-walks subtree". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is stark: I compute height over and over for nodes I've *already* walked. When I'm at node 1 computing its children's heights, I'm re-doing work I did when I visited node 2.
>
> **LEARNER:** But I need height at every node to check every bend. How do I avoid recomputing it?
>
> **TEACHER:** *That's* the question. Here's the nudge — I'm already doing a DFS that computes height. Pause and think: **while I'm computing a node's height and I have its left and right heights right there in my hands — what else could I compute for free, in that same moment?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it)*

**[VISUAL: ONE dfs pass. At each node: `left` and `right` heights arrive; two things happen — update a running `best = left+right`, and return `1+max` up.]**

> **TEACHER:** Fuse the two jobs into one DFS. I'm computing height anyway. The instant I know a node's left height and right height, I *already have* the diameter bending at that node — it's `left + right`. So update a running max right there, then return the height up as usual.
>
> Two different things happen at each node, and separating them is the whole trick:
> - **What I return up:** the height, `1 + max(left, right)` — so my parent can use it.
> - **What I record on the side:** the best bend, `max(best, left + right)` — a running global.
>
> **[VISUAL: node 2 — left=1 (from 4), right=1 (from 5). Record best = 1+1 = 2. Return up 1+max(1,1) = 2. Node 1 — left=2, right=1. Record best = 2+1 = 3. Return 3.]**
>
> Height gets computed exactly *once* per node, because each call directly uses its children's returned values — no re-walking. O(n).
>
> **LEARNER:** Wait — why can't I just *return* the diameter up like I return the height? Why does it have to be a side variable?
>
> **TEACHER:** Sharp, and this is the crux. The diameter at a node isn't built from the diameters of its children — it's built from their *heights*. If I returned diameter up, the parent couldn't reconstruct height from it. So I return the *composable* quantity (height) and stash the *answer* (diameter) on the side. Return one, track the other. That's the reusable pattern.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Return height UP. Track best = left + right ON THE SIDE."]**

> The line: **return the height up; track the answer on the side.**
>
> Whenever the thing you're asked for isn't composable from children but a *helper quantity* is — return the helper, record the answer in a running variable. Diameter, max-path-sum, balanced-check — all the same move.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> A `best` accumulator, and an inner height function.

```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
```

> **[VISUAL: add chunk 2, highlight.]** Grab both child heights — one recursive call each.

```python
        left = height(node.left)
        right = height(node.right)
```

> **[VISUAL: add chunk 3, highlight the two distinct lines.]** Record the bend on the side, return the height up.

```python
        best = max(best, left + right)   # longest path bending here (edges)
        return 1 + max(left, right)      # height for my parent
    height(root)
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:40`
*(elaboration — why each line exists)*

**[VISUAL: the function; spotlight the two "output" lines side by side.]**

> The *why*.
>
> `left = height(node.left)` — each child's height, computed *once* and captured. No second call, no re-walk. That single capture is what turns O(n²) into O(n).
>
> `best = max(best, left + right)` — the answer, tracked globally. `left + right` is the edge-count of the path bending at this node: left height is edges down the left, right height is edges down the right.
>
> `return 1 + max(left, right)` — the *composable* quantity handed to the parent. Note it uses `max` (the taller side, for height), while `best` used `+` (both sides, for the bend). Same two numbers, combined two different ways for two different purposes.
>
> **LEARNER:** Why does `left + right` give *edges* and not nodes? I keep second-guessing the off-by-one.
>
> **TEACHER:** Because empty returns 0. A leaf's children are empty → height 0 each. Its parent sees `left=1, right=1` (a leaf returns `1+max(0,0)=1`)... and `left+right = 2` counts the two edges down to those leaves. The heights are node-counts, but their *sum* lands exactly on the edge-count of the bent path. Trace node 1: left=2, right=1, sum=3 — the three edges 4-2-1-3. It works out.

---

## 9. DRY-RUN THE CODE — `7:30`
*(worked example — prove it)*

**[VISUAL: the tree with height returns and best updates annotated bottom-up.]**

> Trace it.
>
> - `height(4) = 1`, best = max(0, 0+0) = 0. Same for `height(5) = 1`.
> - `height(2)`: left=1, right=1. best = max(0, 2) = **2**. returns `1+max(1,1) = 2`.
> - `height(3) = 1`, best stays 2 (0+0 < 2).
> - `height(1)`: left=2, right=1. best = max(2, 3) = **3**. returns 3.
> - Answer: `best = 3`. ✅
>
> Height computed once per node; the answer accumulated on the side. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:10`
*(transfer to interview)*

**[VISUAL: Brute O(n²) vs Ours O(n); Space O(h).]**

> Say it: *"The naive height-at-every-node is **O(n²)** because height re-walks each subtree. Fusing height and diameter into one post-order pass computes each height once — **O(n) time**, **O(h) stack**."*
>
> That contrast — recompute versus single-pass — is exactly the sentence that earns the checkmark here.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:40`
*(depth + honesty)*

**[VISUAL: O(h) recursion; note "the real win was TIME, O(n²)→O(n)".]**

> Space is the O(h) recursion stack — the floor for a DFS reaching every leaf. But be honest about where the win actually was: **it wasn't a space trick, it was a time trick** — collapsing O(n²) into O(n) by fusing the two passes.
>
> If recursion depth worries you, an iterative post-order with an explicit stack and a height map hits the same O(n)/O(h) — more code, same idea. Say: *"The lesson here is spotting the recompute trap and folding it into one post-order pass."*

---

## 12. YOUR TURN (active recall) — `9:05`
*(retrieval practice)*

**[VISUAL: "Your turn → 124. Max Path Sum" and "110. Balanced Tree".]**

> Before next time: **110 — Balanced Binary Tree** — return height, flag imbalance on the side, one pass. Then the boss level, **124 — Binary Tree Maximum Path Sum** — same "return one side up, track the bend" with values instead of heights. If you can adapt today's code to those, you own the pattern.

---

## 13. LOCK IT IN — `9:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **The longest path bends at some node** — its length there is `leftHeight + rightHeight`.
> 2. **Return height up, track the answer on the side** — return the composable thing, stash the answer.
> 3. **Fusing height + answer turns O(n²) into O(n)** — spot the recompute trap.
>
> The peg: **return the ladder, keep the record.** Hand height up so parents can climb; quietly log the widest bend as you go.

---

## 14. CLIFFHANGER — `9:50`
*(open loop to next lesson)*

**[VISUAL: a BST with one node subtly out of place — locally fine, globally illegal. Title blurred: "Validate BST".]**

> You've mastered returning a value up. Next problem flips the flow: instead of only sending information *up*, you'll thread a constraint *down*. "Is this a valid binary search tree?" — and the trap is that checking each node against just its children is *wrong*. A node can look fine next to its parent yet violate a grandparent. The fix carries a shrinking `(low, high)` window down the tree. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
