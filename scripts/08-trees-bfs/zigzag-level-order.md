# 🎬 Recording Script — Binary Tree Zigzag Level Order Traversal
**Pattern: Tree BFS · LeetCode 103 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Level Order Traversal (102) — the `for _ in range(len(queue))` level loop. This is that, with one twist.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree with a green snake weaving down it — row 1 left-to-right, row 2 right-to-left, row 3 left-to-right. A red "Wrong Answer on test 6" banner sits below.]**

> You just nailed level-order traversal. Now the interviewer adds five words: *"but zigzag the direction each level."* Left-to-right, then right-to-left, snaking down.
>
> "Easy," you think, "I'll just enqueue the children in the *opposite* order on those rows." You run it… and it's wrong. Not just the row you flipped — the rows *below* it are scrambled too.
>
> There's a subtle trap here that catches almost everyone. By the end of this video you'll know exactly why flipping the queue poisons everything downstream — and the clean one-line fix. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: the tree, with each level annotated by its required direction.]**

```
        3          ← level 0: left→right
       / \
      9   20       ← level 1: right→left
         /  \
        15   7     ← level 2: left→right
```

> The whole problem in one line: **level order, but flip direction every other row.**
>
> Same tiny tree as last time. Level 0 stays `[3]`. Level 1 reverses to `[20, 9]`. Level 2 goes back to `[15, 7]`. Answer: `[[3], [20, 9], [15, 7]]`.
>
> Notice — the *only* thing that changed from plain level order is row 1 got reversed. That's the entire delta.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — feel the trap)*

**[VISUAL: the queue. On level 1, arrows show enqueuing 20's children BEFORE 9's children — right-to-left — to "fake" the flip.]**

> Here's the tempting move. "I want row 1 right-to-left? Fine — I'll dequeue 20 before 9, and enqueue *their* children right-to-left too." Feels natural: flip the traversal, get flipped output.
>
> So on level 1 I process 20 first, then 9. Output row: `[20, 9]`. 
>
> **[VISUAL: but now the queue for level 2 has filled in a scrambled order — 20's children and 9's children interleaved wrong. A red highlight over the queue: "order corrupted".]**
>
> But watch the queue I just built for level 2. Because I enqueued children in flipped order, they're now sitting in the wrong sequence. When I try to flip *again* for level 2, I'm flipping an already-scrambled line. Two wrongs don't make a right here — they make test case 6 fail.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Two tracks labeled: "TRAVERSAL ORDER" and "OUTPUT ORDER", currently tangled together. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the root cause. We tried to make one thing do two jobs: the queue's job is to *traverse the tree correctly*, but we hijacked it to also *control output direction*. Those are two different concerns, and tangling them breaks both.
>
> **LEARNER:** Okay so… if I can't flip the queue — how do I ever get a reversed row out?
>
> **TEACHER:** That's exactly the question. Pause and think: **what if the traversal stayed perfectly normal — always left-to-right — and I flipped something else entirely?** What's the *other* place a "reverse" could live?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: two clean, separate lanes. Lane A "traverse": always L→R, children enqueued normally. Lane B "record": a double-ended list where values land on the front OR back.]**

> **TEACHER:** Separate the two jobs. Keep the **traversal** dead simple — always dequeue left-to-right, always enqueue children in natural order. The queue stays pristine, so every level below is correctly ordered. We never touch it.
>
> The direction lives somewhere else: in **how we record** each value into the row's list. On a left-to-right row, append to the *back*. On a right-to-left row, append to the *front*.
>
> Think of it like writing on a strip of paper. You always *read* the tree left to right — but on flip rows, you write each new value at the *left end* of your strip, pushing the earlier ones right. Same reading order, reversed writing.
>
> **[VISUAL: level 1 — dequeue 9 (normal), write to FRONT → strip is [9]; dequeue 20, write to FRONT → strip is [20, 9]. Done, reversed, and the queue was never disturbed.]**
>
> **LEARNER:** Won't inserting at the front be slow — isn't that an O(n) shift every time?
>
> **TEACHER:** It would be, with a plain list. That's why the row uses a **deque** — `appendleft` is O(1). So we get the reversal for free, in one pass, and the traversal never gets corrupted. Best of both.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Traverse L→R always. Flip only the RECORDING end."]**

> The line to remember: **never flip the traversal — flip only which end you record to.**
>
> Traversal order and output order are separate concerns. Keep the queue honest; let a boolean flag decide front-or-back. That separation is the whole lesson, and it shows up far beyond trees.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Start with the same level-order skeleton, plus one flag.

```python
from collections import deque

def zigzagLevelOrder(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    left_to_right = True
```

> **[VISUAL: add chunk 2, highlight.]** The outer loop, snapshot the size — identical to plain level order. The row itself is a `deque` now.

```python
    while queue:
        level = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
```

> **[VISUAL: add chunk 3, highlight the front/back branch.]** Here's the only new idea — record to the correct end.

```python
            if left_to_right:
                level.append(node.val)       # back
            else:
                level.appendleft(node.val)   # front → reversed
```

> **[VISUAL: add chunk 4.]** Enqueue children normally — always — then flip the flag for next row.

```python
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(list(level))
        left_to_right = not left_to_right
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight lines.]**

> Walk the *why*.
>
> The `queue.append(node.left/right)` lines — notice they're **always** in natural order, no matter the flag. That's the whole fix. The traversal is untouchable; only the recording moves.
>
> `level = deque()` and `appendleft` — this is what makes the reversal O(1). If you used a list and `insert(0, val)`, each front-insert shifts the whole row — O(width) per node, O(width²) per level. The deque keeps it O(1).
>
> `left_to_right = not left_to_right` — flip once per level, at the very bottom of the outer loop. One boolean carries the entire zigzag.
>
> **LEARNER:** Couldn't I skip all this and just do a normal level order, then reverse every odd row at the end?
>
> **TEACHER:** You absolutely could — same O(n), totally acceptable answer. The only cost is a second pass that re-touches half the nodes. The deque version folds it into one pass. In an interview, mention *both* — it shows range.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it)*

**[VISUAL: trace table; note the queue stays in natural order throughout.]**

| level | flag | dequeued (L→R) | recorded | result |
|---|---|---|---|---|
| 0 | True | 3 | `[3]` | `[[3]]` |
| 1 | False | 9, 20 → appendleft | `[20, 9]` | `[[3],[20,9]]` |
| 2 | True | 15, 7 | `[15, 7]` | `[[3],[20,9],[15,7]]` |

> Look at the "dequeued" column — always left-to-right, always natural. Only the "recorded" column flips. Output: `[[3], [20, 9], [15, 7]]`. Exactly right, one pass, queue never corrupted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: Time O(n); Space O(w) + O(n) output.]**

> Say it: *"Same as level order — each node enqueued and dequeued once, **O(n) time**. The queue holds at most one level, **O(w) space**. The `appendleft` on a deque is O(1), so the flip adds nothing."*
>
> Zigzag costs the same as plain level order. That's the point of doing it right.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: deque version vs list-insert version, with the O(width²) trap crossed out.]**

> Space is already optimal — bounded by the output you must return. The real refinement here is *time-constant*, and it's a strong detail to name.
>
> If you'd reached for `list.insert(0, val)` to reverse, each front-insert is O(width), turning a level into O(width²). The **deque's `appendleft` keeps it O(1)**. Say that out loud: *"I used a deque per level so the reverse is O(1) front-inserts, not an O(width²) shift."* That's the kind of detail that separates "it works" from "strong hire."

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → 199. Right Side View" and "107. Bottom-Up".]**

> Before the next video, warm up on **107 — Bottom-Up Level Order** (just reverse the outer list), then take a run at **199 — Right Side View**, which is our next lesson: same BFS, but you keep only *one* node per level.
>
> Try to write zigzag from scratch first. If you keep the traversal L→R and flip only the recording end without peeking, you've got it.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Separate traversal order from output order.** Never flip the queue to fake direction.
> 2. **A single boolean flag** flipped each level drives the whole zigzag.
> 3. **Use a deque per row** so front-inserts are O(1), not O(width²).
>
> The peg: **read the tree straight, write it crooked.** The queue always goes left-to-right; only your pen changes ends.

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a tree viewed from the right, only the rightmost node of each level glowing. Title blurred in: "Right Side View".]**

> So far we've kept every node in every level. Next problem strips it down: *"Stand to the right of the tree — what do you see?"* Your instinct will be "just follow the right pointers down." That instinct is wrong, and there's a sneaky case that proves it — a node with only a *left* child that's still visible. Same BFS loop, one clever index. Next video. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    boolean leftToRight = true;
    while (!queue.isEmpty()) {
        int size = queue.size();
        LinkedList<Integer> level = new LinkedList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (leftToRight) level.addLast(node.val);
            else             level.addFirst(node.val);   // O(1) front insert
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
        leftToRight = !leftToRight;
    }
    return result;
}
```
