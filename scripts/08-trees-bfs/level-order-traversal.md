# 🎬 Recording Script — Binary Tree Level Order Traversal
**Pattern: Tree BFS · LeetCode 102 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the *root* pattern for the whole BFS unit. Everything else (zigzag, right-side-view) leans on the idiom you learn here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an Google interview room. A tree on the whiteboard. The prompt: "Return the node values level by level." A cursor blinks in an empty editor.]**

> Google phone screen. They draw a tree and say: *"Give me the values, one row at a time, top to bottom."*
>
> And here's what most people do — they panic, reach for recursion, and start passing a `depth` counter around, appending into lists by index. It works… but it's fighting the problem.
>
> There's one word in that prompt that should've decided your entire approach before you wrote a single line. By the end of this video, you'll hear that word and your hand will already be reaching for a queue. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: the tree drawn cleanly.]**

```
        3
       / \
      9   20
         /  \
        15   7
```

> The whole problem in one line: **return the values grouped by level** — a list of lists, one inner list per row.
>
> Tiny example — five nodes. Level 0 is just `[3]`. Level 1 is `[9, 20]`. Level 2 is `[15, 7]`. So the answer we're chasing is `[[3], [9, 20], [15, 7]]`.
>
> Hold that shape in your head — grouped by row. That grouping *is* the whole problem.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the awkwardness)*

**[VISUAL: the tree, with a DFS pointer diving down 3 → 9, then back up to 3 → 20 → 15. A `result` list being built with index labels [0], [1], [2].]**

> Let's do what the brain reaches for first: recursion. Dive down, carry a `depth` number, and append each value into `result[depth]`.
>
> Start at 3, depth 0 — put it in bucket 0. Go left to 9, depth 1 — but bucket 1 doesn't exist yet, so create it, then append. Back up, go right to 20, depth 1 — bucket 1 exists, append. Down to 15, depth 2, create bucket 2… down to 7, depth 2, append.
>
> **[VISUAL: the recursion path zig-zagging depth-first, buckets being lazily created; a little "did bucket exist?" check flashing each time.]**
>
> It gets the right answer. But look at what you're juggling: a depth counter, a "does this bucket exist yet" check, and you're walking the tree *depth-first* to reconstruct a *breadth-first* answer. You're translating between two orders in your head.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the mismatch: the DFS arrow goes DOWN a branch, but the desired output goes ACROSS a row. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So what's awkward here? The traversal direction and the answer direction don't match. We want *rows*, but DFS gives us *branches*. We're doing bookkeeping just to bridge that gap.
>
> **LEARNER:** Wait — is that actually a problem though? It's still O(n), it still works. Why not just ship it?
>
> **TEACHER:** Fair — it's correct and it's linear. But an interviewer watching you fumble a depth-index into lazily-created buckets reads *"doesn't see the natural structure."* Pause the video: **if the answer is organized by rows, what traversal visits the tree row by row in the first place?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: the tree. A horizontal band sweeps down: first covers `[3]`, then `[9, 20]`, then `[15, 7]`. Beside it, a queue drawn as a horizontal FIFO line.]**

> **TEACHER:** Here's the unlock. If you want the tree *row by row*, use the traversal that naturally goes row by row: **breadth-first search.** BFS visits all the distance-0 nodes, then all the distance-1 nodes, then distance-2 — that ordering *is* level order. No translation needed.
>
> And the tool for BFS is a **queue** — first in, first out, like a line at a coffee counter. You serve the front, and as you serve each person you send their kids to the back of the line. A whole generation gets served before the next one starts.
>
> **LEARNER:** But if I just pour everything into one queue, don't all the levels blur together? How do I know where row 1 ends and row 2 begins?
>
> **TEACHER:** *That's* the one trick — and it's beautiful. At the very top of each round, **snapshot the queue's size.** Right now it holds exactly one level and nothing else. That count tells you precisely how many to pop for this row. Pop that many, collect them, enqueue their children — and now the queue holds exactly the *next* level.
>
> **[VISUAL: queue shows `[9, 20]`, a label "size = 2 → this is one whole level", pop both, children 15,7 flow in, queue becomes `[15, 7]`.]**

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Snapshot the queue size = one level. Pop exactly that many."]**

> Burn this line in: **the queue's size at the top of the loop is exactly one level.**
>
> That `for _ in range(len(queue))` idiom is the heartbeat of every level-based tree problem. You'll reuse this exact loop in zigzag, in right-side-view, in every variant. Learn it here once.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it in pieces. First, the guard and the setup — a queue seeded with the root.

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    result = []
    queue = deque([root])
```

> **[VISUAL: add chunk 2, highlight it.]** Now the outer loop — one iteration per level. First thing inside: snapshot the size.

```python
    while queue:
        level_size = len(queue)      # nodes on THIS level
        level = []
```

> **[VISUAL: add chunk 3.]** The inner loop pops exactly that many, collects values, and sends children to the back.

```python
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
```

> **[VISUAL: add chunk 4, highlight.]** After the inner loop, one full row is done — stash it and return at the end.

```python
        result.append(level)
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `deque` — not a plain list. `popleft` on a list is O(n) because everything shifts; on a deque it's O(1). Use the right tool.
>
> `level_size = len(queue)` — this single line is the whole trick. We freeze the count *before* we start adding children, so the inner loop can't accidentally eat into the next level. Everything we add during this pass waits for the next round.
>
> **LEARNER:** Quick one — why grab `level_size` into a variable? Why not just loop `while queue`?
>
> **TEACHER:** Sharp — and this is the classic bug. If you loop `while queue`, you keep popping as you also keep pushing children, and all the levels smear into one flat list. The frozen count is the fence between rows. Snapshot it, then don't trust `len(queue)` again until next round.
>
> The two `if node.left / node.right` — we only enqueue real children, never `None`, so the queue never holds phantom nodes.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: the tree beside a trace table filling row by row; the queue redrawn each pass.]**

> Let's run the real code on our five nodes.

| queue before | level_size | pop & collect | enqueue | result so far |
|---|---|---|---|---|
| `[3]` | 1 | `[3]` | 9, 20 | `[[3]]` |
| `[9, 20]` | 2 | `[9, 20]` | 15, 7 | `[[3],[9,20]]` |
| `[15, 7]` | 2 | `[15, 7]` | none | `[[3],[9,20],[15,7]]` |
| `[]` | — | done | — | ✅ |

> Output: `[[3], [9, 20], [15, 7]]`. Exactly the shape we promised at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: two lines — Time O(n); Space O(w) queue + O(n) output.]**

> Say it the way you'd say it in the room: *"Every node is enqueued once and dequeued once, so **O(n) time**. The queue holds at most one level — its maximum width `w` — so **O(w) space** on top of the O(n) output."*
>
> Name both numbers. Interviewers listen for the space term as much as the time term.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: side by side — "BFS: O(w) width" vs "DFS: O(h) height".]**

> Can we do better than O(w)? Honestly — it depends on the tree's *shape*, and that's the mature answer.
>
> BFS's queue costs **width**. The DFS-with-depth-index version we started with costs **height** — O(h) recursion stack. For a wide bushy tree, the bottom row alone is ~n/2 nodes, so BFS's width is expensive and DFS's height is cheaper. For a tall skinny tree, it flips.
>
> So neither wins universally. Say that out loud: *"BFS costs width, DFS costs height — I picked BFS because the output is level-shaped, not because it's always cheaper."* That sentence shows you *chose*, you didn't default.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → 107. Level Order Bottom-Up" and "515. Largest Value in Each Row".]**

> Before the next video, try **107 — Level Order Bottom-Up**. Same exact BFS; the only change is you reverse the outer list at the end. And if you want a second rep, **515 — Largest Value in Each Row**: instead of collecting the whole level, keep the max.
>
> Don't peek. If you can reproduce the `for _ in range(len(queue))` loop from memory, you own the pattern.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **"Level / row / depth-by-depth" → BFS with a queue.** That word is the trigger.
> 2. **Snapshot `len(queue)` at the top of each pass** — that's one level, exactly.
> 3. **BFS costs width, DFS costs height** — know the trade so you can defend your choice.
>
> The memory peg: **the queue at the top of the loop is one whole level, gift-wrapped.** Snapshot the size, and the rows unwrap themselves.

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Zigzag Level Order" with a snake weaving left-right-left down the levels.]**

> You've got level order cold. Now here's the twist that trips people: what if they want the *same* rows, but alternating direction — left-to-right, then right-to-left, snaking down like a boustrophedon? The obvious fix is to flip how you enqueue the children… and that quietly corrupts every level below it. Next video: why that trap fails, and the one-line flag that does it cleanly. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int levelSize = queue.size();          // snapshot = one level
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```
