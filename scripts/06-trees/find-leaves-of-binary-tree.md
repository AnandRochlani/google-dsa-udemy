# 🎬 Recording Script — Find Leaves of Binary Tree
**Pattern: Tree DFS (height grouping) · LeetCode 366 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** max-depth of a binary tree (that same `1 + max(left, right)` recursion) — watch it do a second job here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a small binary tree. Its outer leaves flash and vanish. Then the newly-exposed leaves flash and vanish. Repeat until empty. A stopwatch in the corner ticks up alarmingly.]**

> The interviewer says: *"Peel the leaves off this tree. Then peel the new leaves. Keep going till it's empty — give me each layer you peeled."*
>
> So you do exactly that. Find the leaves, delete them, scan again, delete again. It works. You submit… and on a big lopsided tree it crawls.
>
> Here's the twist: you don't need to peel round by round at all. There's one number hiding on every node that tells you — in a single pass — exactly which round it disappears in. By the end of this video that whole repeated-peeling loop collapses into one clean DFS. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, this exact tree:]**

```
        1
       / \
      2   3
     / \
    4   5
```

> The whole problem in one line: **repeatedly remove all the leaves, and return the list of what you removed each round.**
>
> Here's our tiny tree — five nodes. Keep your eye on it; we'll solve it by hand before we touch code.
>
> The answer is `[[4, 5, 3], [2], [1]]`. Don't chase why yet — just hold those three groups.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — let them feel the waste)*

**[VISUAL: the tree. A "full tree scans" counter, top-right, at 0. Each round: highlight current leaves, then grey them out.]**

> Let's do what your brain does first. **Round 1:** who are the leaves? `4`, `5`, `3` — no children. Record them, snip them off. Counter: one full scan.
>
> **[VISUAL: 4, 5, 3 grey out. Counter → 1.]**
>
> **Round 2:** rescan the *whole* survivng tree. Now `2` has lost both kids — it's a leaf. Record `2`, snip it. Counter: two.
>
> **[VISUAL: 2 greys out. Counter → 2.]**
>
> **Round 3:** rescan again. Only `1` is left. Record it. Done. `[[4,5,3],[2],[1]]`.
>
> Five nodes, three full scans. Fine here. But picture a tree that's basically a straight line — a thousand nodes deep.
>
> **[VISUAL: the tree stretches into a long vertical chain; the counter spins toward "n scans × n nodes".]**
>
> You peel *one* node per round, and you rescan everything every round. That's `n` rounds times `n` work — quadratic. That's your slow submission.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the chain tree. Spotlight the fact that each round re-walks every surviving node. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? Every round we re-walk the entire tree just to ask "who's a leaf *now*?" We keep rediscovering the shape we already knew.
>
> **LEARNER:** But isn't that unavoidable? A node only becomes a leaf *after* its children are gone — you can't know that until you've done the earlier rounds.
>
> **TEACHER:** That's the right instinct — and here's the crack in it. What if each node could figure out its own round *without* simulating the peeling? Pause the video. Look at `4,5,3` leaving in round 0, `2` in round 1, `1` in round 2. **What property of a node decides its round?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: each node gets a small badge. Fill them bottom-up: 4→0, 5→0, 3→0, 2→1, 1→2. Beside each, show the round it was removed in — the numbers match.]**

> **TEACHER:** Here's the move. Forget rounds. Ask each node one local question: **how far am I above the leaves?** Distance down to my deepest leaf.
>
> A leaf is zero above the leaves — it *is* one. Its parent is one above. And so on up.
>
> **[VISUAL: 4,5,3 badge "0". 2 badge "1". 1 badge "2".]**
>
> Now line those heights up against the rounds we peeled by hand. Height 0 → removed round 0. Height 1 → round 1. Height 2 → round 2. **They're the same number.** The round a node vanishes in *is* its height above the leaves.
>
> **LEARNER:** Wait — why *height* from the bottom? My gut said depth from the root. `1` is at the top, shouldn't it go first or something?
>
> **TEACHER:** Great misconception to kill right now. Depth-from-the-root is distance *down from `1`*. But leaves get peeled from the **outside in** — the bottom fringe goes first. A node can't leave until *both* its subtrees are already stripped, so what matters is how deep its *deepest* descendant is. That's height-from-the-bottom, not depth-from-the-top. The root leaves **last** precisely because it sits highest above the leaves.
>
> **[VISUAL: an arrow labeled "depth (from root)" points down and gets a red ✗; an arrow "height (from leaves)" points up and gets a green ✓.]**
>
> And height has a beautiful recursive shape: **my height = 1 + the taller of my two children's heights.** Bottom-up, computed once.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "removal round == height above the leaves = 1 + max(left, right)".]**

> Burn this one line in: **the round a node is removed in equals its height above the leaves — and height is `1 + max(left, right)`.**
>
> So instead of peeling layer by layer, I do **one** post-order pass, compute every node's height, and drop each node into a bucket by that height. One pass. Every node filed into the right round.

---

## 7. CODE IT — LIVE & CHUNKED — `5:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. We return a list of lists — `res` — and a helper that returns a node's height.

```python
def find_leaves(root):
    res = []

    def height(node):
```

> **[VISUAL: add chunk 2, highlight it.]** Base case — and this is the clever bit. An empty child returns **−1**, so that a real leaf comes out at exactly 0.

```python
        if node is None:
            return -1                    # leaf becomes 1 + max(-1,-1) = 0
```

> **[VISUAL: add chunk 3.]** The recursion — my height is one more than my taller child.

```python
        h = 1 + max(height(node.left), height(node.right))
```

> **[VISUAL: add chunk 4, highlight the two res lines.]** File this node into its bucket. If this height is brand new, open a bucket for it first. Then append and return the height up to my parent.

```python
        if h == len(res):                # first node ever seen at this height
            res.append([])
        res[h].append(node.val)
        return h

    height(root)
    return res
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `return -1` for `None` — this is the trick that makes leaves land on 0. A leaf has two null children, so `1 + max(-1, -1)` = 0. Return 0 there instead and every height is off by one.
>
> `1 + max(height(left), height(right))` — the **taller** child decides, because a node can't become a leaf until its *deeper* side is fully peeled. That side governs the timeline.
>
> **LEARNER:** Hold on — `if h == len(res)`. Why does a simple equality check know when to open a new bucket? Feels fragile.
>
> **TEACHER:** It's airtight, and here's why. We only ever *discover* a new height when it's exactly one past the biggest we've seen — because a node's height is one more than a child we already processed. So the first time height `h` appears, `res` currently has buckets `0..h-1`, meaning `len(res) == h`. That single check opens each bucket exactly once, in order. No node ever skips ahead to a height whose bucket doesn't exist yet.
>
> `res[h].append(node.val)` — post-order guarantees we reach this line only *after* both children are done, so every node is filed exactly once into its correct round.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the tree with badges; a trace table filling row by row, post-order.]**

```
        1
       / \
      2   3
     / \
    4   5
```

> Let's run the real code, post-order — left subtree, right subtree, then the node.

| Call | left h | right h | `h` | files into | `res` after |
|---|---|---|---|---|---|
| height(4) | −1 | −1 | 0 | res[0] | `[[4]]` |
| height(5) | −1 | −1 | 0 | res[0] | `[[4,5]]` |
| height(2) | 0 | 0 | 1 | res[1] | `[[4,5],[2]]` |
| height(3) | −1 | −1 | 0 | res[0] | `[[4,5,3],[2]]` |
| height(1) | 1 | 0 | 2 | res[2] | `[[4,5,3],[2],[1]]` |

> `[[4,5,3],[2],[1]]` — exactly the three groups we promised at the start. And notice `3` slots into `res[0]` *after* `4` and `5` all on its own — the ordering falls out of the traversal for free. Loop closed. One pass, no re-scanning.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²). Ours: O(n). A note: "each node visited exactly once".]**

> **TEACHER:** Say it the way you'd say it in the room: *"The peel-and-rescan brute force is O(n²) on a path-shaped tree — n rounds, each re-walking the tree. My height version visits each of the n nodes exactly once, so it's O(n) time. Space is O(n) for the output list, plus O(h) recursion stack."*
>
> That's the jump from a slow submission to a clean one — and you narrated *why*, which is the part Google actually scores.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: the res list of lists; a "shrink it?" thought bubble gets a red ✗.]**

> Quick and honest. Can we shrink the `O(n)`? **No — and I can say exactly why.** The output *is* every node's value, just grouped into rounds. I'm required to return all of it, so that space is the deliverable, not overhead.
>
> The only extra is the `O(h)` recursion stack — `O(log n)` balanced, `O(n)` on a degenerate path — and that's intrinsic to any tree DFS. If the path is so deep it'd blow Python's recursion limit, swap to an explicit stack: same `O(h)`, just heap instead of call stack.
>
> Say it out loud: *"Space is O(n) output-bound; my only auxiliary cost is the O(h) stack, which is unavoidable for a tree walk."* Naming the floor beats inventing a fake trick.

---

## 12. YOUR TURN (active recall) — `10:05`
*(retrieval practice)*

**[VISUAL: "Your turn → Delete Leaves With a Given Value (LC 1325)". A blank editor.]**

> Before the next video, try **Delete Leaves With a Given Value**. Same post-order shape: a node can only be checked *after* its children, and removing children can turn a parent into a new leaf. Feel how the bottom-up order carries the logic.
>
> Don't peek. Wrestle with it for ten minutes — that struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Peel-and-rescan is O(n²)** — you re-walk the whole tree every round.
> 2. **A node's removal round == its height above the leaves** — compute it once, bottom-up.
> 3. **`height = 1 + max(left, right)`, null = −1** — file each node into `res[height]` in one post-order pass.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "removal round = height from the bottom."]**
>
> When a problem says *"peel the outer layer, again and again,"* your hand should already be reaching for one bottom-up height DFS — not a loop.
>
> *(GCA reminder — for the interview itself: state the O(n²) peel first, name the repeated rescans out loud, *then* reach for the height insight. Google's General Cognitive Ability signal isn't the final code — it's you narrating naive → optimal, and asking the one clarifying question up front: "does order within a round matter?")*

---

## 14. CLIFFHANGER — `11:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Binary Tree Maximum Path Sum" — a path snaking through a tree, some nodes glowing negative-red.]**

> Here, each node returned *one* clean number up to its parent — its height. But what if a node has to return one thing to its parent while secretly tracking a *different* best answer that bends through it and back down? That's the next one: Binary Tree Maximum Path Sum — same post-order skeleton, one sneaky twist that trips up almost everyone. See you there.
