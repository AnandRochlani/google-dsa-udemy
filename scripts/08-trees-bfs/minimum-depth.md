# 🎬 Recording Script — Minimum Depth of Binary Tree
**Pattern: Tree BFS · LeetCode 111 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Level Order Traversal (102) — the BFS queue. This one adds *early exit*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a wildly lopsided tree — a shallow leaf two nodes down on the left, and a giant chain of thousands of nodes plunging down the right. A stopwatch ticking.]**

> "Minimum depth — shortest path from the root to the nearest leaf." Sounds like a twin of maximum depth. Same recursion, swap `max` for `min`, done… right?
>
> Two traps. One: that `min` swap gives the *wrong answer* on some trees. Two: even when it's right, it wastes enormous effort — on this lopsided monster, the answer is 2, but you'd walk the entire deep-right chain to find it.
>
> There's a traversal that returns almost instantly here, and a subtle definition of "leaf" you have to get exactly right. Let's go.

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

> One line: **the number of nodes on the shortest root-to-leaf path.** A leaf is a node with *no* children.
>
> Here, 9 is a leaf sitting at depth 2 — path 3 → 9. Nodes 15 and 7 are leaves too, but deeper, at depth 3. The nearest leaf wins, so the answer is **2**.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — expose the leaf trap)*

**[VISUAL: a NEW tiny tree — root 1, only a right child 2, only a right child 3. A pure one-sided chain.]**

```
    1
     \
      2
       \
        3
```

> Let's try the "swap max for min" recursion: `min depth = 1 + min(left, right)`. Watch it on this one-sided chain.
>
> At node 1: left subtree is empty → depth 0. Right subtree… let's say it returns something. `1 + min(0, something)`. The `min` grabs the **0** from the empty left side. So node 1 reports `1 + 0 = 1`.
>
> **[VISUAL: red flash — answer "1" — but the only leaf is node 3, at depth 3!]**
>
> That says minimum depth is 1. But node 1 *isn't a leaf* — it has a child. The real nearest leaf is 3, at depth 3. The naive `min` treated the *missing* left child as a leaf at depth 0. That's the leaf trap.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight: "a null child is NOT a leaf." A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Two problems surfaced. First, the leaf trap: a node with one child is *not* a leaf — you can't count its missing side as depth-0. Second, even a *correct* recursion visits every node, so on a lopsided tree it grinds through the huge deep side for nothing.
>
> **LEARNER:** For minimum, can't I just… stop as soon as I find *a* leaf? Why does maximum depth force me to see everything but this one wouldn't?
>
> **TEACHER:** That's *exactly* the insight. Pause on it: **which traversal reaches the shallowest leaf first — so I can stop the instant I see it?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:55`
*(elaboration + analogy — derive it)*

**[VISUAL: BFS band sweeping down the lopsided tree; it hits the shallow leaf on level 2 and a big green "STOP" stamp lands — the deep chain never gets touched.]**

> **TEACHER:** "Shortest path to a target" in an unweighted tree is a **shortest-path** question — and shortest-path means **BFS**. BFS explores level by level, closest first. So the *first leaf it dequeues* is guaranteed to be the shallowest leaf in the whole tree. The moment you pop a leaf, you're done.
>
> That's the payoff maximum depth can't have. For *max*, the deepest leaf could be anywhere, so you must see them all. For *min*, BFS finds the nearest one early and quits — on our lopsided monster, it returns at level 2 and never touches the deep chain.
>
> **LEARNER:** And the leaf trap — does BFS dodge it automatically?
>
> **TEACHER:** Cleanly. You only "finish" when you dequeue a node with **both** children null. A one-child node isn't a leaf, so you don't stop there — you just enqueue its one real child and keep going. The trap can't fire.

---

## 6. THE KEY MOVE (signaling) — `4:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "min ⇒ BFS, stop at first leaf. max ⇒ full DFS."]**

> The line to burn in: **minimum means BFS with an early exit; maximum means a full DFS.**
>
> And "leaf" means *both* children null — never a single null side. Those two facts are the whole problem.

---

## 7. CODE IT — LIVE & CHUNKED — `4:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Guard, then a queue holding pairs of `(node, depth)` so each node carries its own depth.

```python
from collections import deque

def minDepth(root):
    if not root:
        return 0
    queue = deque([(root, 1)])       # (node, depth)
```

> **[VISUAL: add chunk 2, highlight the leaf check.]** Pop from the front; if it's a real leaf, that depth *is* the answer — return immediately.

```python
    while queue:
        node, depth = queue.popleft()
        if not node.left and not node.right:   # first leaf = shallowest
            return depth
```

> **[VISUAL: add chunk 3.]** Otherwise enqueue whichever children exist, at depth+1.

```python
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0    # unreachable for a valid tree
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight lines.]**

> The *why*.
>
> `deque([(root, 1)])` — we bundle depth *with* each node instead of tracking levels separately. Depth 1 because the root itself counts as one node on the path.
>
> `if not node.left and not node.right` — **both** must be null. This is the leaf trap defused. A one-child node fails this test, so we never mistake it for a leaf; we fall through and enqueue its real child.
>
> `return depth` — the instant we pop a leaf, we return. Because BFS pops in nondecreasing depth order, this leaf is the shallowest possible. No need to look further — that's the early exit that beats DFS here.
>
> **LEARNER:** Why `popleft` and not `pop`? Does the end matter?
>
> **TEACHER:** Critically. `popleft` is FIFO — it drains the queue front-to-back, so shallow nodes come out before deep ones. If you `pop` from the *right*, you'd get LIFO — that's a stack, that's DFS, and you'd lose the "shallowest first" guarantee that makes the early exit correct.

---

## 9. DRY-RUN THE CODE — `7:00`
*(worked example — prove it)*

**[VISUAL: original tree; trace table.]**

| popped (depth) | leaf? | action |
|---|---|---|
| (3, 1) | no — has children | enqueue (9,2), (20,2) |
| (9, 2) | **yes** — no children | **return 2** ✅ |

> BFS never even looks at 20, 15, or 7. It pops 9 — a genuine leaf at depth 2 — and returns. Shortest path found, deep side untouched. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:45`
*(transfer to interview)*

**[VISUAL: Time O(n) worst, often ≪ n; Space O(w).]**

> Say it: *"Worst case **O(n)** — a balanced tree with all leaves at the bottom forces us to scan the last level. But on lopsided trees the early exit returns far sooner. Space is **O(w)**, the queue width."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:15`
*(depth + honesty)*

**[VISUAL: BFS O(w) + early exit vs DFS O(h) no early exit.]**

> The honest trade. **DFS** uses O(h) stack but has *no early exit* — it walks the whole tree. **BFS** uses O(w) queue but *gains the early exit*, which is the entire reason we're here.
>
> On a balanced tree they're both O(n) time. On a lopsided tree — shallow leaf on one side, deep chain on the other — BFS is dramatically faster in practice. Say it out loud: *"I chose BFS specifically because 'minimum' enables an early return that DFS can't exploit."* Naming *why* you picked it is the signal.

---

## 12. YOUR TURN (active recall) — `8:40`
*(retrieval practice)*

**[VISUAL: "Your turn → 104. Maximum Depth" and "112. Path Sum".]**

> Before next time: do **104 — Maximum Depth** and feel the contrast — no early exit, full DFS, `1 + max(...)`. Then **112 — Path Sum**, which uses this exact "both-children-null" leaf definition. The min/max pair is the lesson: *min ⇒ BFS early-exit, max ⇒ full traversal.*

---

## 13. LOCK IT IN — `9:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Minimum / nearest / shortest" → BFS with early exit.** First leaf popped is the answer.
> 2. **A leaf has BOTH children null** — a one-child node is not a leaf.
> 3. **min ⇒ BFS, max ⇒ full DFS** — the defining contrast of this pair.
>
> The peg: **for "nearest," race down level by level and stop the second you touch a real leaf.**

---

## 14. CLIFFHANGER — `9:20`
*(open loop to next lesson)*

**[VISUAL: a perfect binary tree with dashed horizontal "next" arrows waiting to be drawn between siblings. Title blurred: "Populating Next Right Pointers".]**

> BFS with a queue costs O(w) memory. Next problem hands you a *perfect* tree and dares you to solve it in **O(1) extra space** — no queue at all. The trick: use the pointers you're *building* as the very thing you walk on. It bends your brain the first time. Next video. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public int minDepth(TreeNode root) {
    if (root == null) return 0;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    int depth = 1;
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (node.left == null && node.right == null) return depth;  // first leaf
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        depth++;
    }
    return depth;
}
```
