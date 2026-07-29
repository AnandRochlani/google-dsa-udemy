# 🎬 Recording Script — Path Sum
**Pattern: Tree DFS · LeetCode 112 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Maximum Depth (104) — the "what do I return up?" reflex. Minimum Depth (111) — the "leaf = both children null" rule.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree with a target "22" in a badge. One root-to-leaf path glows green; a sneaky internal node where the sum ALSO hits 22 flashes red with a "✗ not a leaf!" tag.]**

> "Is there a root-to-leaf path that sums to 22?" A yes/no question. Feels friendly.
>
> But there's a trap that fails a hidden test case: the running sum can hit your target at an *internal* node — not a leaf — and if you return true there, you're wrong. And a second trap: the values can be **negative**, so you can't prune a branch just because it already overshot.
>
> Two small gotchas, one clean DFS. By the end you'll carry a running remainder down the tree and know exactly *where* the success check is allowed to fire. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: the tree.]**

```
        5
       / \
      4   8
     /   / \
    11  13  4
   /  \       \
  7    2       1
```

> One line: **is there a path from root to a leaf whose values add up exactly to `targetSum`?**
>
> Target 22. The path 5 → 4 → 11 → 2 sums to 5+4+11+2 = 22, and 2 is a leaf. So the answer is **true**. The path must *end at a leaf* — a node with no children.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — the wasteful way)*

**[VISUAL: every root-to-leaf path being enumerated and listed, each summed separately: [5,4,11,7]=27, [5,4,11,2]=22 ✓, [5,8,13]=26, [5,8,4,1]=18.]**

> The literal first instinct: build *every* root-to-leaf path, sum each, check for 22.
>
> Path 5→4→11→7 = 27. Path 5→4→11→2 = 22 — match! But watch the work: I built four full lists of values and summed each from scratch.
>
> **[VISUAL: memory tiles piling up — each path stored as a list; a "re-summing" label over each.]**
>
> That's O(n·h) space storing paths, and re-adding numbers I've already added. I don't need the *paths* — I only need to know if *one* works. There's a leaner way to carry just enough state.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the piled-up path lists. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** We're hoarding whole paths when all we care about is a single running total. And DFS already walks one root-to-leaf path at a time — that's its natural shape.
>
> **LEARNER:** So instead of building the path and summing at the end… I carry the sum *as I go*?
>
> **TEACHER:** Right idea — and let's make it even cleaner. Pause and think: **instead of adding up as I descend, what if I *subtract* each node's value from the target? What would the target equal by the time I reach a leaf that works?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it)*

**[VISUAL: the target 22 shrinking as we descend: 22 → (−5) → 17 → (−4) → 13 → (−11) → 2 → (−2) → 0 at the leaf.]**

> **TEACHER:** Carry the **remaining** target down. At each node, subtract its value — now your children need to make up what's left. It's like paying off a bill node by node: start owing 22, pay 5 at the root (owe 17), pay 4 (owe 13), pay 11 (owe 2)… and at the leaf, if the bill is exactly paid — the leaf's value equals the remaining amount — you found it.
>
> So the recursion answers one question per node: *"can the subtree below me finish off this remaining amount along a root-to-leaf path?"* Each node asks its children the smaller version of the same question.
>
> **LEARNER:** Where does the leaf check actually go? Can't I just return true whenever remaining hits 0?
>
> **TEACHER:** That's the trap. You only declare victory **at a leaf** — where `remaining == node.val`. If you returned true the moment the running sum matched at an *internal* node, you'd accept a path that doesn't reach a leaf. The success check lives *at leaves only*.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Subtract down. Succeed ONLY at a leaf where remaining == node.val."]**

> The line: **carry the remaining target down; succeed only at a leaf whose value finishes it.**
>
> "What do I return up?" — a boolean: *can this subtree hit the remaining target?* Combine the two children with `or` — any winning branch is enough.

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Base case: empty tree can't have a path.

```python
def hasPathSum(root, targetSum):
    if not root:
        return False
```

> **[VISUAL: add chunk 2, highlight the leaf check.]** The leaf check — succeed iff what's left equals this leaf's value.

```python
    if not root.left and not root.right:
        return targetSum == root.val
```

> **[VISUAL: add chunk 3, highlight the or.]** Otherwise subtract and recurse both sides — `or` short-circuits on the first win.

```python
    remaining = targetSum - root.val
    return (hasPathSum(root.left, remaining) or
            hasPathSum(root.right, remaining))
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:00`
*(elaboration — why each line exists)*

**[VISUAL: the function; spotlight lines.]**

> The *why*.
>
> `if not root.left and not root.right` — both children null: this is a genuine leaf. Same leaf definition as minimum depth. The check `targetSum == root.val` asks "does this leaf's value exactly finish the remaining target?"
>
> `remaining = targetSum - root.val` — pay off this node, pass the smaller debt down.
>
> The `or` — a qualifying path just needs to exist in *one* subtree. The moment the left call returns true, Python short-circuits and never even explores the right. Efficient and correct.
>
> **LEARNER:** Since values can be negative, can I prune a branch once the running sum blows past the target?
>
> **TEACHER:** No — and that's the second trap. With negative values, a path that looks "too big" now can be dragged back down by a negative node later. So you can't prune on overshoot; you genuinely explore every root-to-leaf path until an `or` returns true. If all values were positive, pruning would be fair game — but the problem doesn't promise that.

---

## 9. DRY-RUN THE CODE — `6:55`
*(worked example — prove it)*

**[VISUAL: the tree; the winning descent traced with remaining values.]**

> Trace target 22.
>
> - `5`: not a leaf. remaining = 22−5 = 17. Try left (4).
> - `4`: not a leaf. remaining = 17−4 = 13. Try left (11).
> - `11`: not a leaf. remaining = 13−11 = 2. Try left (7): leaf, `2 == 7`? no. Try right (2): leaf, `2 == 2`? **yes → True.**
>
> That true short-circuits all the way up the `or` chain. We never explore 8's subtree. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:35`
*(transfer to interview)*

**[VISUAL: Time O(n); Space O(h).]**

> Say it: *"Each node visited at most once — **O(n) time**. Space is the recursion stack, **O(h)**. No path lists, no re-summing — I carry a single integer down."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:05`
*(depth + honesty)*

**[VISUAL: recursion O(h) vs iterative stack O(h) of (node, remaining) pairs.]**

> Auxiliary space is O(h), and that's the floor — any traversal that might descend to the deepest leaf needs O(h). The win over brute force is carrying one integer instead of whole path lists.
>
> If recursion depth is a concern, an **iterative** version with an explicit stack of `(node, remaining)` pairs hits the same O(h) and dodges recursion limits:

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

---

## 12. YOUR TURN (active recall) — `8:30`
*(retrieval practice)*

**[VISUAL: "Your turn → 113. Path Sum II" and "257. Binary Tree Paths".]**

> Before next time: **113 — Path Sum II** wants *all* qualifying paths, so now you actually store the path and backtrack — which is exactly our next lesson, **257 — Binary Tree Paths**. Also try **129 — Sum Root to Leaf Numbers**: same DFS, build a number down each path instead of checking a sum.

---

## 13. LOCK IT IN — `8:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Root-to-leaf path with property X" → DFS carrying an accumulator**, test at leaves.
> 2. **Success fires only at a leaf** — matching the sum at an internal node doesn't count.
> 3. **Negative values ⇒ no overshoot pruning** — you must explore every path.
>
> The peg: **pay the target down node by node; you win only when a leaf settles the bill exactly.**

---

## 14. CLIFFHANGER — `9:15`
*(open loop to next lesson)*

**[VISUAL: a tree with two root-to-leaf paths written as strings "1->2->5" and "1->3". Title blurred: "Binary Tree Paths". A push/pop animation on a shared list.]**

> Path Sum only needed yes or no. Next problem wants the *actual* list of every root-to-leaf path, printed as strings. That means carrying the trail with you — and the crucial move of *undoing* it as you back out, so the left branch's tail doesn't pollute the right. That push-then-pop dance is **backtracking**, and it's the skill behind permutations and subsets too. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
