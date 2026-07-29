# 🎬 Recording Script — Populating Next Right Pointers in Each Node
**Pattern: Tree BFS → O(1) space · LeetCode 116 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Level Order Traversal (102) — the BFS queue. Here we *delete* the queue.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a perfect binary tree of 1..7. Dashed horizontal arrows appear between siblings, then a hard requirement flashes red: "O(1) extra space."]**

> "Wire each node to its right neighbor on the same level." Sounds like level order — throw it in a queue, link them up. Easy.
>
> Then the interviewer adds the killer follow-up: *"Now do it in **constant** extra space. No queue."*
>
> And that feels impossible — how do you go level by level with *nothing* to hold a level? The answer is one of the most elegant tricks in trees: **use the pointers you're building as the thing you walk on.** By the end of this video you'll see how a finished level threads the next one, for free. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: the perfect tree, with the target next-wiring shown.]**

```
        1                    1 → null
       / \                  / \
      2   3      ⇒         2 → 3 → null
     / \ / \              / \ / \
    4  5 6  7            4→5→6→7 → null
```

> One line: **set every node's `next` to the node immediately to its right on the same level;** the rightmost points to `null`.
>
> The gift in the fine print: it's a **perfect** binary tree — every internal node has exactly two children, all leaves on one level. That perfectness is what makes the O(1) trick possible. Hold onto it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — the queue works but costs O(n))*

**[VISUAL: BFS queue processing level 2: [4,5,6,7]. Each node links to the next one in the queue. A memory meter fills to ~n/2.]**

> The obvious solution is level-order BFS. Process each level; wire each node to the *next* one still in the queue.
>
> Level 2: queue holds `[4, 5, 6, 7]`. Pop 4, its right neighbor is the new front — 5 — so `4.next = 5`. Pop 5, `5.next = 6`. Pop 6, `6.next = 7`. Pop 7, it's last → `7.next = null`.
>
> **[VISUAL: memory meter highlighted — "queue holds ~n/2 nodes at the bottom level = O(n) space".]**
>
> It's correct, and it works on *any* tree. But look at that memory meter — the bottom level of a perfect tree is ~n/2 nodes. That queue is O(n) space. The follow-up explicitly bans it.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Level 1 is fully wired: 2 → 3 → null. It glows like a linked list. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The queue exists only to remember "who's next on this level." But look — after we finish level 1, the nodes 2 → 3 → null are *already linked to each other* by the next pointers we just set. That's a linked list. For free.
>
> **LEARNER:** Oh — so the level I *just finished* could tell me the order of the level I'm *about to do*?
>
> **TEACHER:** That's the whole leap. Pause and think: **if level 1 is already threaded left-to-right by `next`, can I walk it with just one pointer — and wire level 2 as I go — without any queue at all?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it)*

**[VISUAL: a `head` pointer walking level 1 via next arrows. For each parent, two wiring moves are drawn on level 2.]**

> **TEACHER:** Here's the trick. Once level `k` is fully linked by `next`, I traverse level `k` using those pointers — one `head` pointer, no queue — and from each parent I wire its two children below. Two rules:
>
> **(a) Siblings:** a node's left child sits directly left of its right child. So `parent.left.next = parent.right`. Easy.
>
> **(b) The bridge:** the tricky one — connecting across two different parents. My right child needs to point to the *next parent's* left child. And I *have* the next parent — it's `parent.next`, which level `k` already wired! So `parent.right.next = parent.next.left`.
>
> **[VISUAL: parent 2 → wire 4.next=5 (siblings), then 5.next = 2.next.left = 3.left = 6 (bridge). Then head moves to 3 via 2.next.]**
>
> **LEARNER:** But `parent.next.left` — what if `parent.next` exists but has no left child? Doesn't that crash?
>
> **TEACHER:** In a general tree, yes — that's the sequel's whole headache. But here the tree is **perfect**: if `parent.next` exists, it's an internal node, so it *definitely* has a left child. Perfectness guarantees the bridge never dangles. That's the gift paying off.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: two boxed lines: "left.next = right  (siblings)" and "right.next = node.next.left  (bridge)".]**

> Two moves, memorize them: **left child points to right child; right child points to the next node's left child.** Siblings, then bridge.
>
> And the meta-move: **a finished level is a linked list — walk it to build the next one.** That's how you kill the queue.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Guard, and a `leftmost` pointer that tracks the start of the current level.

```python
def connect(root):
    if not root:
        return None
    leftmost = root
```

> **[VISUAL: add chunk 2, highlight the outer condition.]** Outer loop drops one level at a time. In a perfect tree, "is there a next level?" is just "does the leftmost have a left child?"

```python
    while leftmost.left:
        head = leftmost          # walk this level via next
```

> **[VISUAL: add chunk 3, highlight the two wiring rules.]** Walk the current level with `head`, wiring the level below.

```python
        while head:
            head.left.next = head.right              # (a) siblings
            if head.next:
                head.right.next = head.next.left     # (b) bridge across parents
            head = head.next
```

> **[VISUAL: add chunk 4.]** Level done — drop to the next level's leftmost.

```python
        leftmost = leftmost.left
    return root
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:15`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight lines.]**

> The *why*.
>
> `while leftmost.left` — the outer loop's stop condition. We only descend if there's a level below. Because the tree is perfect, checking `.left` is enough: if a left child exists, a full next level exists.
>
> `head = leftmost` then `head = head.next` — this inner walk is the queue's replacement. We stride across the whole current level using the `next` pointers *we already built*. No storage.
>
> `head.left.next = head.right` — rule (a), always safe: an internal node in a perfect tree has both children.
>
> `if head.next: head.right.next = head.next.left` — rule (b). The guard `if head.next` handles the rightmost node of the level — it has no next, so its right child stays pointing at `null`, which is exactly what we want.
>
> **LEARNER:** How do we know level `k`'s next pointers are set *before* we walk it? Feels circular.
>
> **TEACHER:** Induction. Level 0 is one node — `root.next` is already `null`, done. Each pass uses level `k`'s finished links to build level `k+1`'s links completely. So when the loop drops down, the new level is already fully threaded, ready to be walked. The base case seeds it; each level hands the next one a finished linked list.

---

## 9. DRY-RUN THE CODE — `8:30`
*(worked example — prove it)*

**[VISUAL: the perfect tree; wiring drawn level by level.]**

> Trace it on 1..7.
>
> - **Level 0** (`leftmost=1`, `head=1`): `1.left(2).next = 1.right(3)`. `1.next` is null → no bridge. Level 1 is now `2 → 3 → null`. Drop `leftmost = 2`.
> - **Level 1** (`leftmost=2`):
>   - `head=2`: `4.next = 5` (siblings); `2.next` is 3 → `5.next = 3.left = 6` (bridge). Now `4 → 5 → 6`.
>   - `head=3` (via `2.next`): `6.next = 7`; `3.next` is null → stop bridge. Now `4 → 5 → 6 → 7 → null`.
>   - `head=null` → level done. Drop `leftmost = 4`.
> - **Level 2** (`leftmost=4`): `4.left` is null → outer loop ends. Leaves need no wiring.

> Every `next` set correctly, and the queue meter never moved past a couple of pointers. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:45`
*(transfer to interview)*

**[VISUAL: Time O(n); Space O(1).]**

> Say it: *"Each node is visited once as a parent, so **O(n) time**. And the space is the headline — just a couple of pointers, `leftmost` and `head`, no queue, no recursion. **O(1) extra space.** That's what the follow-up wanted."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:15`
*(depth + honesty)*

**[VISUAL: BFS O(n) queue vs this O(1); a note about recursion reintroducing O(h).]**

> This *is* the space optimization — from the BFS queue's O(n) down to O(1) by reusing next as the level's linked list.
>
> One honesty note: if you solved it *recursively*, you'd quietly reintroduce O(h) stack space. So the iterative two-loop form is what actually hits the O(1) target — mention that.
>
> And name the sequel: **117 — Populating Next Right Pointers II** drops the perfect guarantee. Same idea, but now `node.next.left` might be missing, so you scan across gaps for the next available child and use a dummy head per level. Saying *"I know 116's perfectness is doing real work for me here"* is a strong-hire detail.

---

## 12. YOUR TURN (active recall) — `11:00`
*(retrieval practice)*

**[VISUAL: "Your turn → 117. Next Right Pointers II".]**

> Before next time, take on **117** — the non-perfect version. You'll need a dummy node to anchor each level and a scan for the next real child across gaps. It's the same insight under harder conditions — and it's where this pattern really tests you.

---

## 13. LOCK IT IN — `11:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Connect within a level" → BFS;** but structure can let you drop the queue.
> 2. **A finished level is a linked list** — walk it with one pointer to build the next.
> 3. **Two wirings:** `left.next = right`, `right.next = node.next.left`. Perfectness makes the bridge safe.
>
> The peg: **each level, once wired, becomes the rail you ride to wire the level below.**

---

## 14. CLIFFHANGER — `11:55`
*(open loop to next lesson)*

**[VISUAL: switching sections — a tree with a recursion arrow diving down and a value bubbling back up. Title blurred: "Maximum Depth — the DFS reflex".]**

> We've squeezed everything we can from BFS and queues. Next unit flips the whole mindset: **DFS recursion**, where the magic question stops being "which level" and becomes *"what value do I return up from each node?"* We start with the simplest one — maximum depth — and that one question will carry you through diameter, validate-BST, and lowest common ancestor. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class Node { int val; Node left, right, next; }
public Node connect(Node root) {
    if (root == null) return null;
    Node leftmost = root;
    while (leftmost.left != null) {           // perfect: left exists ⇒ next level exists
        Node head = leftmost;
        while (head != null) {                // walk this level via next
            head.left.next = head.right;                       // (a) siblings
            if (head.next != null)
                head.right.next = head.next.left;              // (b) bridge across parents
            head = head.next;
        }
        leftmost = leftmost.left;
    }
    return root;
}
```
