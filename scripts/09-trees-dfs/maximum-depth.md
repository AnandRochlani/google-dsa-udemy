# 🎬 Recording Script — Maximum Depth of Binary Tree
**Pattern: Tree DFS · LeetCode 104 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the BFS unit (queues, levels). This flips to DFS recursion — and introduces the one question that runs the whole DFS unit.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree, and a three-line Python function beside it. A caption: "This is the DNA of every tree-recursion problem."]**

> Maximum depth of a binary tree. The answer is *three lines*. But don't let the size fool you — this is the single most important tree problem you'll learn, because it teaches the one question that unlocks *every* DFS tree problem after it.
>
> That question is: **"what value do I return up from each node?"** Get that reflex here, and diameter, validate-BST, lowest-common-ancestor all become variations on a theme. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: the tree.]**

```
        3
       / \
      9   20
         /  \
        15   7
```

> One line: **the number of nodes on the longest root-to-leaf path.**
>
> Longest path here: 3 → 20 → 15 (or 3 → 20 → 7) — three nodes. So the answer is **3**.
>
> Unlike *minimum* depth, there's no shortcut — the deepest leaf could be anywhere, so we have to consider every one.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — the heavier way)*

**[VISUAL: a BFS queue counting levels: level 1 = [3], level 2 = [9,20], level 3 = [15,7]; a counter ticking 1, 2, 3.]**

> If you just came from the BFS unit, your reflex is: count the levels. Sweep level by level, tick a counter — 1, 2, 3. Three levels, depth 3. Correct!
>
> **[VISUAL: the BFS code with its queue and `for _ in range(len(queue))` loop — highlight how much machinery it is.]**
>
> But look at all that machinery — a queue, a level-size snapshot, an inner loop — just to count how deep the tree goes. For a problem this simple, that's a lot of moving parts. There's a far tidier expression of "how deep does this go."

---

## 4. THE PAIN POINT + PREDICT — `2:00`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the BFS machinery. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The BFS works, but the problem isn't really about *levels* — it's a **reduction**: squeeze the whole tree down to one number. And reductions on trees have a much cleaner shape.
>
> **LEARNER:** Cleaner how? If BFS already gives the right answer, what's left to improve?
>
> **TEACHER:** Elegance and space — and a mental model you'll reuse forever. Pause and think: **stand at any node. If your two children could just *tell* you how deep their subtrees are, what one number would you report to your own parent?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:40`
*(elaboration + analogy — derive it)*

**[VISUAL: a node with two children showing returned numbers; the node computes 1 + max and passes it up. Values bubble upward from leaves.]**

> **TEACHER:** Here's the reframe. Stand at a node and assume your children already did their job — each hands you the depth of their subtree. What do you report up? **One plus the deeper of the two.** Your own node, plus the taller side.
>
> `depth = 1 + max(left depth, right depth)`. That's the entire solution.
>
> The base case makes it bottom out: an empty subtree — `None` — has depth 0. So a leaf reports `1 + max(0, 0) = 1`. Then its parent adds itself to the taller child, and so on. The numbers *bubble up*: leaves say 1, each parent adds one to its deeper side, and the root ends up holding the whole tree's height.
>
> **LEARNER:** That "assume the children already solved it" move — that feels like a leap of faith.
>
> **TEACHER:** It's the leap of faith recursion is *built* on. You trust the smaller calls, define how to combine them, and nail the base case. Get those two — combine rule and base case — and the recursion is correct by induction. This is the reflex; everything in this unit reuses it.

---

## 6. THE KEY MOVE (signaling) — `4:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Return up: 1 + max(left, right). Base: None → 0."]**

> The line: **each node returns `1 + max(left, right)`; empty is 0.**
>
> And the meta-line for the whole unit — **"what do I return up from each node?"** Ask that at every DFS tree problem. Here the answer is height. Later it'll be a boolean, or a node, or a height-plus-a-side-effect.

---

## 7. CODE IT — LIVE & CHUNKED — `4:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type the base case.]**

> Base case first — the thing that stops the recursion.

```python
def maxDepth(root):
    if not root:
        return 0
```

> **[VISUAL: add the combine line, highlight.]** Then the whole recurrence in one line.

```python
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

> That's it. Two lines of logic. The `max` picks the taller subtree; the `1 +` adds the current node.

---

## 8. EXPLAIN THE CODE (the WHY) — `5:30`
*(elaboration — why each line exists)*

**[VISUAL: the function; spotlight each part.]**

> The *why*.
>
> `if not root: return 0` — the seed. Without it, the recursion never terminates, and it correctly encodes "an empty subtree contributes zero depth." This is where the leaf trap from *minimum* depth would live — but for *max*, treating a missing side as 0 is exactly right, because `max` ignores the shorter (or absent) side anyway.
>
> `max(...)` — we want the *longest* path, so we take the deeper child. `1 +` — add ourselves.
>
> **LEARNER:** In minimum depth we needed special cases for one-child nodes. Why doesn't max need them?
>
> **TEACHER:** Great callback. In *min*, a missing child would wrongly report 0 and `min` would grab it — so we guarded against it. In *max*, `max` naturally *discards* the 0 from an empty side in favor of the real subtree. So the same base case that's a trap for min is harmless for max. The operator you combine with — `min` vs `max` — changes everything.

---

## 9. DRY-RUN THE CODE — `6:20`
*(worked example — prove it)*

**[VISUAL: the tree with return values annotated bottom-up.]**

> Trace it, leaves first.
>
> - `maxDepth(15) = 1 + max(0,0) = 1`. Same for `maxDepth(7) = 1`.
> - `maxDepth(20) = 1 + max(1, 1) = 2`.
> - `maxDepth(9) = 1 + max(0,0) = 1`.
> - `maxDepth(3) = 1 + max(1, 2) = 3`. ✅
>
> Watch it bubble: leaves report 1, node 20 becomes 2, and the root adds itself to its deeper child (20's side) → 3. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:00`
*(transfer to interview)*

**[VISUAL: Time O(n); Space O(h).]**

> Say it: *"One call per node, so **O(n) time**. Space is the recursion stack — **O(h)**, the height. That's O(log n) for a balanced tree, O(n) for a degenerate chain."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:30`
*(depth + honesty)*

**[VISUAL: O(h) recursion vs O(h) explicit stack vs O(w) BFS.]**

> Space is the O(h) recursion stack. Options if pushed:
>
> - **Iterative DFS with an explicit stack** of `(node, depth)` — same O(h), but off the call stack, handy if recursion limits are a worry on a 10⁵-deep skewed tree.
> - **BFS** trades height for width — O(w).
> - **Morris traversal** could hit O(1), but it's overkill and error-prone for a plain depth count.
>
> For a balanced tree O(h) = O(log n) is already excellent. Say: *"Recursion is the clean answer; I'd only switch to an explicit stack if the interviewer bans recursion or flags stack overflow on a deep skewed tree."*

---

## 12. YOUR TURN (active recall) — `7:55`
*(retrieval practice)*

**[VISUAL: "Your turn → 111. Minimum Depth" and "543. Diameter".]**

> Before next time: revisit **111 — Minimum Depth** and feel the min/max contrast (min gets an early exit, max doesn't). Then peek at **543 — Diameter**, our next lesson — it *reuses this exact height computation* but tracks something extra on the side.
>
> Write max depth from memory. If "what do I return up?" comes automatically, you're ready.

---

## 13. LOCK IT IN — `8:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Height / depth / reduce to a number" → DFS**, return a value up and combine.
> 2. **`1 + max(left, right)`, base `None → 0`** — the whole recurrence.
> 3. **The operator carries the meaning** — `max` here, `min` in minimum depth, and the base case that's a trap for one is safe for the other.
>
> The peg — the question that runs the entire DFS unit: **"what value do I return up from each node?"** For height, it's `1 + max`.

---

## 14. CLIFFHANGER — `8:40`
*(open loop to next lesson)*

**[VISUAL: a tree with the longest path NOT through the root, glowing — bending at an internal node. Title blurred: "Diameter of Binary Tree". A red "O(n²)" ghost hovering.]**

> You now compute height in three lines. Next problem asks for the *diameter* — the longest path between any two nodes, which can bend anywhere, not just at the root. The obvious approach calls this height function at every node… and quietly explodes into **O(n²)**. The fix is gorgeous: return height up while tracking the answer *on the side*, all in one pass. That contrast — recompute versus single-pass — is the whole next lesson. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```
