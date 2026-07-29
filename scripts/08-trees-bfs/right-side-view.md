# 🎬 Recording Script — Binary Tree Right Side View
**Pattern: Tree BFS · LeetCode 199 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Level Order Traversal (102) — the `for _ in range(len(queue))` level loop. Right Side View is that loop, keeping one node per level.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree, and a stick-figure standing to its right, eye-lines hitting only the rightmost node of each row. A thought bubble: "just follow the right pointers, right?"]**

> Google asks: *"Stand to the right of this tree. What nodes can you see?"*
>
> Almost everyone's first move: "Easy — start at the root, keep going right: `root`, `root.right`, `root.right.right`…" Clean, one line, feels obvious.
>
> It's wrong. There's a tree shape where the node you see from the right is reached through a *left* child — and the naive right-walk sails right past it. By the end of this video you'll know the reframe that makes this bulletproof, and why it's just level-order in disguise. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: the tree. Nodes 1, 3, 4 glow; 2 and 5 are dimmed "hidden behind" 3 and 4.]**

```
        1
       / \
      2   3
       \   \
        5   4
```

> One line: **return the rightmost node of each level, top to bottom.**
>
> From the right you see 1 (level 0), then 3 (level 1's rightmost), then 4 (level 2's rightmost). Nodes 2 and 5 are hidden behind them. Answer: `[1, 3, 4]`.
>
> Keep your eye on node 5 — it's a *right* child of 2, but it's hidden. And notice 4 is the only node on level 2 that's visible. That level-2 detail is about to matter.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — feel the trap)*

**[VISUAL: modify the tree — remove node 4, so level 2 is just node 5 (a right child of 2, but now the ONLY node on its level). The naive right-walk arrow: 1 → 3 → then 3.right is null → STOPS.]**

> Let's run the "just follow right pointers" idea — but on a slightly meaner tree. Say node 4 doesn't exist. Now level 2 is only node 5.
>
> Naive walk: start at 1. Go right to 3. Go right from 3… 3 has no right child. Stop. Answer: `[1, 3]`.
>
> **[VISUAL: node 5 glowing, ignored, with a red "MISSED" tag. From the right, 5 is clearly visible — nothing is to its right on level 2.]**
>
> But look from the right! Level 2 has exactly one node — 5 — and there's nothing beside it, so you absolutely see it. The right answer is `[1, 3, 5]`. The naive walk missed it because 5 hangs off a *left*-ish path, not a chain of right pointers. Following `.right` is not the same as "rightmost on the level."

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Cross out "follow .right pointers". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So the bug is a definition error. "Right side view" is *not* "the chain of right children." It's *"the last node on each level"* — whichever pointer you followed to get there.
>
> **LEARNER:** Wait — this is a *misconception* I definitely had. Why isn't "the rightmost node" always found by going right? Feels like it should be.
>
> **TEACHER:** Because a level's rightmost node can be an *only child* dangling off a left branch — like our node 5. "Right pointer" is about a single parent-child link; "rightmost on the level" is about horizontal position across the *whole* row. Different things. So pause: **if the answer is one node per level, what traversal already hands you levels?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: the tree with the horizontal band sweeping down again; on each band, only the LAST node in left-to-right order lights up.]**

> **TEACHER:** Reframe it and the whole thing collapses: **"rightmost of each level" = "the last node of each level in left-to-right order."** And "each level" is the trigger we know — that's **BFS with a queue.**
>
> Do a completely normal level-order traversal. Within each level, the nodes come out of the queue strictly left-to-right — because BFS enqueues left child before right, parents in order. So the *last* node you pop in a level is, by definition, the rightmost one. Grab it, discard the rest.
>
> **[VISUAL: level 1 queue = [2, 3], pop 2 (ignore), pop 3 (last → keep). Level 2 queue = [5, 4], pop 5 (ignore), pop 4 (last → keep).]**
>
> **LEARNER:** So I don't even care *which* child it came from — I just take whoever's last in the row?
>
> **TEACHER:** Exactly. Position in the level is all that matters. Node came via a left pointer? Doesn't matter — if it's last in the row, it's what you see. That's why this handles the node-5 case for free.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Right side view = last node of each level. Take index size−1."]**

> The line: **right side view is the last node of each level — not the right-pointer chain.**
>
> In code, that's grabbing the node at index `level_size - 1` in your BFS loop. Same loop as level order; you just keep one node instead of all of them.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Same BFS skeleton. Guard and setup.

```python
from collections import deque

def rightSideView(root):
    if not root:
        return []
    result = []
    queue = deque([root])
```

> **[VISUAL: add chunk 2, highlight the index check.]** Snapshot the size, and this time track our position `i` so we know who's last.

```python
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:      # last node in this level
                result.append(node.val)
```

> **[VISUAL: add chunk 3.]** Enqueue children exactly as before.

```python
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight lines.]**

> The *why*.
>
> `for i in range(level_size)` — we count our position now, because we need to know when we've hit the last one. `i == level_size - 1` is "this is the final node of the row."
>
> Why is the last-dequeued node guaranteed to be the rightmost? Because BFS preserves left-to-right order within a level: we always enqueue left child before right, and we process parents in order, so the queue holds each level strictly L→R. The last pop is the far-right position — full stop, regardless of which pointer led there.
>
> **LEARNER:** Could I skip the index and just overwrite a variable with every node's value, keeping whatever's last?
>
> **TEACHER:** Yes — that also works: set `rightmost = node.val` every iteration, append it after the loop. Same result. The `i == size - 1` version just makes the intent explicit and appends once. Either is fine; know both.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it)*

**[VISUAL: original tree; trace table.]**

| queue before | level_size | last node popped | result |
|---|---|---|---|
| `[1]` | 1 | 1 | `[1]` |
| `[2, 3]` | 2 | 3 | `[1, 3]` |
| `[5, 4]` | 2 | 4 | `[1, 3, 4]` |

> Level 1: queue is `[2, 3]` — 2 first (it's the left child), 3 last → keep 3. Level 2: `[5, 4]` — 5 is 2's right child, 4 is 3's right child, 4 is last → keep 4. Output `[1, 3, 4]`. And on the mean tree where 4 was gone, level 2 would be just `[5]`, last node 5 — caught correctly. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: Time O(n); Space O(w).]**

> Say it: *"Every node enqueued and dequeued once — **O(n) time**. Queue holds at most one level — **O(w) space**. The output is one value per level, so O(height) for the result."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty — the DFS alternative)*

**[VISUAL: a compact DFS that recurses RIGHT child first; the first node hit at each new depth glows.]**

> Here's the space alternative, and it's elegant. DFS, but **recurse the right child first**, tracking depth. The *first* node you reach at each new depth is — because you went right-first — the rightmost. Record it once per depth.

```python
def rightSideView_dfs(root):
    result = []
    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):     # first node seen at this depth
            result.append(node.val)  # right-first ⇒ it's the rightmost
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)
    dfs(root, 0)
    return result
```

> Now the trade-off: **BFS costs O(w) queue width; DFS costs O(h) stack height.** Tall skinny tree? DFS's O(h) wins. Wide bushy tree? BFS's O(w) can be smaller. Say which and why — that's the signal you *chose*.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → 513. Bottom Left Value" and "Left Side View".]**

> Before next time: **Left Side View** — the mirror. Take the *first* node of each level instead of the last. Then **513 — Find Bottom Left Tree Value**: the leftmost node of the *deepest* level. Both are this same loop with the index tweaked.
>
> Write right-side-view from memory first. If you reach for `i == size - 1` instead of `.right`, you've internalized the reframe.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Right side view" = last node of each level** — never "the right-pointer chain."
> 2. **Position in the level is all that matters** — not which child pointer you followed.
> 3. **BFS index `size−1`, or DFS right-first** — same answer, width-vs-height trade.
>
> The peg: **it's not about right pointers — it's about who's standing last in each row.**

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a lopsided tree — shallow leaf near the root on the left, a huge deep chain on the right. Title blurred: "Minimum Depth".]**

> Every BFS problem so far walked the whole tree. Next one lets you *quit early*. "Minimum depth — shortest path to the nearest leaf." On a tree that's shallow on one side and enormous on the other, BFS can return almost instantly while DFS grinds through the deep side. But there's a trap in the word "leaf" that returns a wrong answer if you're sloppy. Next video. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (i == size - 1) result.add(node.val);   // rightmost of level
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
    }
    return result;
}
```
