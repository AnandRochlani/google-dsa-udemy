# 🎬 Recording Script — Validate Binary Search Tree
**Pattern: Tree DFS · LeetCode 98 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Maximum Depth (104) — "what do I return up?" Here we add: "what do I thread *down*?"

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree that looks locally fine everywhere — every parent bigger than its left child, smaller than its right — but one node glows red: it's illegal because of an ancestor three levels up.]**

> "Is this a valid binary search tree?" You write the obvious check: every node bigger than its left child, smaller than its right. You run it. It says *valid*.
>
> It's wrong. There's a tree where every parent-child pair looks perfect, yet the tree is *not* a BST — because a node violates a rule set by its **grandparent**, not its parent. Local checks can't see that far.
>
> The fix is a beautiful idea: as you walk down, each node lives inside a shrinking `(low, high)` window that carries *every* ancestor's constraint. By the end you'll thread that window down the tree and never get fooled by the local trap. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: the invalid tree.]**

```
        5
       / \
      1   4        ← 4 is in 5's RIGHT subtree → must be > 5. It isn't.
         / \
        3   6
```

> One line: a valid BST means **every node is strictly greater than *all* values in its left subtree and strictly less than *all* values in its right subtree** — recursively.
>
> This tree is **invalid**. Locally, `3 < 4 < 6` looks perfect. But 4 (and 3) sit in 5's *right* subtree, so they must all be greater than 5 — and they're not. Answer: **false**.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — the local-check trap)*

**[VISUAL: the local check running: 5 vs children 1,4 → "1<5<4 ✓". Then node 4 vs 3,6 → "3<4<6 ✓". A green "valid" — then a red BUZZER.]**

> Let's run the tempting local check: each node greater than its left child, less than its right.
>
> Node 5: left child 1, right child 4. Is `1 < 5 < 4`? Well `1 < 5` yes, `5 < 4`... hmm, actually here 4 < 5, so *this* particular check would catch it. Let me show the real killer: imagine 4 were instead a 6 with children 3 and 7 — every *local* triple passes, but 3 is still less than the ancestor 5 and sits in its right subtree.
>
> **[VISUAL: the classic failure — a node like 3 that's a perfectly valid right-then-left descendant locally, but < its grandparent 5, which it must exceed. Local checks all green, tree still illegal.]**
>
> The point: comparing a node only to its *immediate* children misses constraints from *ancestors*. Node 3 must be greater than 5 — because it lives in 5's right subtree — but 5 is its grandparent, invisible to a parent-child check.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the ancestor→descendant constraint arrows spanning multiple levels. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So validity isn't a *local* property — it's about the whole subtree, which means every ancestor imposes a constraint on every descendant. A parent-child check only sees one level.
>
> **LEARNER:** Wait — this feels like the diameter trap. Do I have to scan the whole subtree at each node to enforce it? Isn't that O(n²) again?
>
> **TEACHER:** You *could* — and it would be O(n²). But there's a much slicker way. Pause and think: **as I walk down and turn left, or turn right, what range of values is a node still *allowed* to have — given every turn I made to get here?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it)*

**[VISUAL: descending the tree, a `(low, high)` window shown at each node, tightening. Root (−∞, +∞); go left → high drops to parent's value; go right → low rises.]**

> **TEACHER:** Here's the unlock. Every node lives inside an **allowed range** `(low, high)`. The root can be anything: `(−∞, +∞)`.
>
> Now the two turns:
> - Go **left**: everything down here must be *smaller* than the current node. So the upper bound tightens — new range `(low, node.val)`.
> - Go **right**: everything must be *larger*. Lower bound rises — `(node.val, high)`.
>
> The magic: that window *accumulates* every ancestor's rule automatically. By the time you reach a deep node, its `(low, high)` is the intersection of *all* the turns above it. A node is valid iff `low < node.val < high`.
>
> **[VISUAL: node 4 in the example — reached by going right at 5, so its range is (5, +∞). Check 5 < 4? NO → false, instantly.]**
>
> Watch our invalid tree: node 4 is in 5's right subtree, so it inherits range `(5, +∞)`. Check `5 < 4`? False. Caught immediately — the range encoded the grandparent rule that the local check missed.
>
> **LEARNER:** Why `±infinity` and not just use INT_MIN and INT_MAX?
>
> **TEACHER:** Because node values can *be* INT_MIN or INT_MAX. If your sentinel is INT_MIN and a real node equals INT_MIN, your strict comparison breaks at the boundary. `±infinity` (or Python's `float('inf')`, or `null` sentinels in Java) sidesteps the whole overflow trap.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Left tightens high. Right raises low. Valid iff low < val < high."]**

> The line: **going left caps the high at the parent; going right raises the low. A node is valid inside its window.**
>
> "What do I thread *down*?" — the `(low, high)` window. "What do I return *up*?" — a boolean, combined with `and`. That down-and-up split is the new idea here.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> An inner helper carrying the window; kick it off with infinities.

```python
def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True                       # empty subtree is a valid BST
```

> **[VISUAL: add chunk 2, highlight the strict check.]** The node must fit strictly inside its window.

```python
        if not (low < node.val < high):       # strict bounds
            return False
```

> **[VISUAL: add chunk 3, highlight the two tightened recursions.]** Recurse, tightening the correct bound on each side, combined with `and`.

```python
        return (valid(node.left,  low, node.val) and   # left: cap high
                valid(node.right, node.val, high))     # right: raise low
    return valid(root, float('-inf'), float('inf'))
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the function; spotlight lines.]**

> The *why*.
>
> `if not node: return True` — an empty subtree trivially satisfies any range. Seeds the recursion.
>
> `low < node.val < high` — **strict** less-than on both sides, because a BST here forbids duplicates and equal values across the boundary. If you used `<=`, you'd wrongly accept a duplicate.
>
> `valid(node.left, low, node.val)` — going left, the *upper* bound becomes this node's value: everything left must be smaller. `valid(node.right, node.val, high)` — going right, the *lower* bound becomes this node's value. Each recursion narrows exactly one side.
>
> The `and` — both subtrees must be valid *under their tightened windows* for the whole thing to be valid.
>
> **LEARNER:** Why pass `node.val` as the new bound and not something derived from the child?
>
> **TEACHER:** Because the constraint comes from *this* node onto everything below. Left descendants must beat *this* value; the window carries it down so even a great-grandchild is still checked against it. That's how the range accumulates every ancestor without re-scanning subtrees.

---

## 9. DRY-RUN THE CODE — `8:10`
*(worked example — prove it)*

**[VISUAL: the invalid tree; window annotated at each node.]**

> Trace the invalid example.
>
> - `valid(5, −∞, +∞)`: `−∞ < 5 < +∞` ✓. Recurse left with `(−∞, 5)`, right with `(5, +∞)`.
> - Left `valid(1, −∞, 5)`: `−∞ < 1 < 5` ✓. Children null → ok.
> - Right `valid(4, 5, +∞)`: check `5 < 4`? **False → return False.**
>
> The whole tree returns **false**. The range `(5, +∞)` encoded the ancestor rule a parent-child check would have missed. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:50`
*(transfer to interview)*

**[VISUAL: Brute re-scan O(n²) vs bounds DFS O(n); Space O(h).]**

> Say it: *"Re-scanning each subtree to verify bounds would be **O(n²)**. Threading the range down checks each node exactly once — **O(n) time**, **O(h) stack**."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:20`
*(depth + honesty — the in-order alternative)*

**[VISUAL: an in-order traversal producing a sequence; a check "strictly increasing?"]**

> Here's the elegant alternative worth knowing: **an in-order traversal of a BST is strictly increasing.** So walk in-order, and verify each value exceeds the previous one.

```python
def isValidBST_inorder(root):
    prev = float('-inf')
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if node.val <= prev:        # must be STRICTLY increasing
            return False
        prev = node.val
        node = node.right
    return True
```

> - **Bounds DFS:** O(h) stack. Simplest, most common.
> - **Iterative in-order:** O(h) explicit stack.
> - **Morris in-order:** rewires threads for **O(1)** extra space — the only true constant-space route. Fiddly; mention it if pushed.
>
> Say: *"For a balanced tree O(h) is fine; Morris is the O(1) escape hatch if they insist on constant space."*

---

## 12. YOUR TURN (active recall) — `10:20`
*(retrieval practice)*

**[VISUAL: "Your turn → 230. Kth Smallest in BST" and "99. Recover BST".]**

> Before next time: **230 — Kth Smallest in a BST** leans on the same in-order-is-sorted fact — stop at the k-th. Then **99 — Recover BST**: two nodes got swapped; find them via in-order. Both cement "in-order of a BST is sorted."

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Local parent-child checks are WRONG** — validity depends on all ancestors.
> 2. **Thread a `(low, high)` window down** — left caps high, right raises low.
> 3. **Or: in-order of a BST is strictly increasing** — verify each value beats the last.
>
> The peg: **every node lives in a window its ancestors shrank.** Left turn lowers the ceiling; right turn raises the floor.

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a general (non-BST) tree with two marked nodes p and q; a glowing node where their paths split. Title blurred: "Lowest Common Ancestor".]**

> You just threaded information *down* the tree. Our finale threads a found-node *up*: "given two nodes, find their lowest common ancestor." No BST ordering to exploit this time — just one elegant post-order pass where the node whose left and right both come back non-null is the answer. It's the perfect capstone for the "what do I return up?" reflex. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public boolean isValidBST(TreeNode root) {
    return valid(root, null, null);   // null sentinels dodge INT_MIN/MAX overflow
}
private boolean valid(TreeNode node, Integer low, Integer high) {
    if (node == null) return true;
    if (low != null && node.val <= low)   return false;
    if (high != null && node.val >= high) return false;
    return valid(node.left, low, node.val)
        && valid(node.right, node.val, high);
}
```
