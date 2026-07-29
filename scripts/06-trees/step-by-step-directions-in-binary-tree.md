# 🎬 Recording Script — Step-By-Step Directions From a Binary Tree Node to Another
**Pattern: Tree DFS / Lowest Common Ancestor · LeetCode 2096 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** root-to-node DFS (Binary Tree Paths) and the LCA idea (LC 236) — we're about to fuse them.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a binary tree drawn clean. Two nodes pulse — one green (start), one orange (dest). A cursor tries to draw a squiggly path between them and keeps second-guessing.]**

> Google interview. The interviewer draws a tree, points at two nodes, and says: *"Give me the directions to walk from this one to that one. Up, left, right — as a string."*
>
> Your brain immediately goes: *"Okay… I need the path between them. Which means the lowest common ancestor. Which means… the LCA algorithm, then walk down twice, then—"* and you feel the code getting complicated before you've written a line.
>
> Here's the twist: you don't have to find the LCA at all. There's a move that makes it vanish — you'll compute two simple paths, delete their shared beginning, and the answer falls out. By the end of this video that trick will feel obvious. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below it, this exact tree:]**

```
        5
       / \
      1   2
     /   / \
    3   6   4
```

> The whole problem in one line: **return the shortest path from the start node to the dest node, written as `U` = go to parent, `L` = go to left child, `R` = go to right child.**
>
> Here's our tiny tree. Start value is `3` — bottom left. Dest value is `6` — bottom middle. Every value is **unique**, which matters: search for a value and you land on exactly one node.
>
> Hold this: the answer is `"UURL"`. Four moves. Don't work out why yet — just keep it in your pocket. We'll earn it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — feel the moving parts)*

**[VISUAL: three labeled boxes appear one at a time: "1. find LCA", "2. walk LCA→start", "3. walk LCA→dest". Arrows trace each on the tree.]**

> Let's do what the brain reaches for first: the literal three-step plan.
>
> **Step one — find the lowest common ancestor** of `3` and `6`. `3` is down the left, `6` is down the right, so the node where they meet is the root, `5`.
>
> **[VISUAL: node `5` glows as the LCA.]**
>
> **Step two — walk from the LCA down to the start**, `3`. That's `5` → left `1` → left `3`. Two steps down.
>
> **Step three — walk from the LCA down to the dest**, `6`. That's `5` → right `2` → left `6`.
>
> Now to *get* from `3` up to the LCA, I reverse those two down-steps — two climbs, `"UU"`. Then the walk down to `6` is `"RL"`. Answer `"UURL"`. It works!
>
> **[VISUAL: the three boxes stack up, a small "3 traversals" tag blinks.]**
>
> But look how many pieces that is — a whole LCA search, *plus* two separate downward DFS walks. Three passes, three chances to slip.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The "find LCA" box gets a spotlight and a 🤔 4-second timer.]**

> **TEACHER:** So here's the itch. That first step — explicitly hunting down the LCA node — is the fiddliest part, and it feels *separate* from finding the paths. What if it isn't separate? What if finding the paths already tells us where the LCA is, for free?
>
> **LEARNER:** How would the path *know* where the LCA is? The path to `3` doesn't mention `6` at all.
>
> **TEACHER:** Right — on its own it doesn't. But what if I had *both* paths, measured from the same starting point? Pause the video: if I write down the route from the **root** to `3`, and the route from the **root** to `6`, what do those two routes have in common — and what does the common part represent?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two strings write out under the tree as arrows trace them from the root: path to 3 = "LL", path to 6 = "RL".]**

> **TEACHER:** Here's the move. Both routes start at the **same root**. Route to `3`: left, left — `"LL"`. Route to `6`: right, left — `"RL"`.
>
> Think of it like two people leaving the same front door with driving directions. As long as their directions read the same — "left, left, left" — they're still on the same road, driving together. The moment the directions **differ**, that's the fork where they split. That fork *is* the lowest common ancestor.
>
> **[VISUAL: analogy — two cars leaving one house, driving together, then splitting at an intersection that gets labeled "LCA".]**
>
> So the **shared prefix** of the two paths is exactly the drive down to the LCA. Strip it off both. Whatever's left on `3`'s side is how far below the fork `3` sits — and whatever's left on `6`'s side is the fresh road down to `6`.
>
> **LEARNER:** Wait — but the leftover on the start side is `L`s and `R`s. The answer needs `U`s. Where does the `U` come from?
>
> **TEACHER:** Beautiful question — that's the crux. Those leftover `L`/`R`s are the steps that went **down** from the fork to `3`. But we're not going down to `3`, we're *starting* at `3` and climbing back **up** to the fork. Reverse a "go left" and you get "go to parent." Reverse a "go right" — also "go to parent." **Every downward step, going backwards, is just a `U`.** So we don't even care whether it was an `L` or an `R` — we only count them.
>
> **[VISUAL: the leftover "LL" on the start side flips into "UU"; a caption: "reverse any down-step → U".]**

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "root→start path + root→dest path, strip shared prefix: start leftovers → U's, dest leftovers → kept."]**

> Burn this one line in: **write both root-to-node paths, delete the shared prefix — the start's leftovers become that many `U`s, and the dest's leftovers stay as they are.**
>
> The LCA never gets named. The strip *is* the LCA. That's the whole trick.

---

## 7. CODE IT — LIVE & CHUNKED — `5:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. One helper — walk from the root to a target value, recording `L`/`R` as we go. It returns `True` the moment it finds the node.

```python
def find(node, target, acc):
    if not node:
        return False
    if node.val == target:
        return True
```

> **[VISUAL: add chunk 2, highlight it.]** Try left. Append `'L'`, recurse. If left found it, stop.

```python
    acc.append('L')
    if find(node.left, target, acc):
        return True
```

> **[VISUAL: add chunk 3.]** Left failed — reuse that slot as `'R'` and try the right subtree. And if *neither* side has it, pop the step off and report failure. That pop is the backtrack.

```python
    acc[-1] = 'R'
    if find(node.right, target, acc):
        return True
    acc.pop()
    return False
```

> **[VISUAL: add chunk 4 — the driver — highlight the while loop.]** Now call it twice, then strip the common prefix and assemble.

```python
def getDirections(root, startValue, destValue):
    start_path, dest_path = [], []
    find(root, startValue, start_path)
    find(root, destValue, dest_path)

    i = 0
    while (i < len(start_path) and i < len(dest_path)
           and start_path[i] == dest_path[i]):
        i += 1

    return 'U' * (len(start_path) - i) + ''.join(dest_path[i:])
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:55`
*(elaboration — why each line exists)*

**[VISUAL: the full code; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `acc[-1] = 'R'` — notice we don't append a second character. We **overwrite** the `'L'` we just tried. A node's step to its child is one move, and it's either left or right, never both. Reusing the slot keeps the path exactly one character per level.
>
> `acc.pop()` — this is the unsung hero. If a subtree was a dead end, we have to **remove** the step we tentatively wrote, or it pollutes the path. Forget this pop and your string fills with garbage from wrong branches.
>
> **LEARNER:** Why `'U' * (len(start_path) - i)` — why throw the actual `L`/`R` letters away and just multiply?
>
> **TEACHER:** Because past the shared prefix `i`, those start-side letters are all downward moves *below* the LCA — and we're climbing back up through every one of them. Up is up regardless of whether you came from a left or a right child. So the **letters carry no information anymore — only the count does.** `len(start_path) - i` is that count. Meanwhile `dest_path[i:]` is the real descent from the LCA to the dest, so *that* we keep verbatim.
>
> **LEARNER:** And the `while` — that's doing the LCA search in disguise?
>
> **TEACHER:** Exactly. It walks both paths together while they agree. The index where they stop agreeing is the fork — the LCA. We never build an LCA function; the prefix scan *is* it.

---

## 9. DRY-RUN THE CODE — `8:10`
*(worked example — prove it, close the loop)*

**[VISUAL: the tree, and a trace table filling row by row.]**

```
        5
       / \
      1   2
     /   / \
    3   6   4
```

> Let's run the real code on start `3`, dest `6`.

| Stage | Action | State |
|---|---|---|
| `find(3)` | `5`→L→`1`, `1`→L→`3` ✓ | `start_path = "LL"` |
| `find(6)` | `5`→R→`2`, `2`→L→`6` ✓ | `dest_path = "RL"` |
| strip prefix | compare index 0: `L` vs `R` → differ immediately | `i = 0` |
| build U's | `len("LL") - 0` = 2 | `"UU"` |
| append dest | `dest_path[0:]` = `"RL"` | `"RL"` |
| glue | `"UU" + "RL"` | **`"UURL"`** ✅ |

> There's the `"UURL"` we promised at second thirty. Loop closed.
>
> **[VISUAL: quick second trace — start `3`, dest `4`. start="LL", dest="RR", still differ at index 0 → "UURR".]**
>
> And to *see the strip actually eat something*: if both nodes lived down the left side, their paths would share a leading `"L"`, the `while` would swallow it, and only the part **below** their real LCA would survive. That swallowed `L` is the drive down to the fork — which neither node should include.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: two rows — Brute: "3 traversals, O(n)". Ours: "2 finds + prefix scan, O(n)". Space: "O(n) path strings + recursion".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Each `find` is at most one full traversal — O(n). I do two, plus an O(length) prefix scan, so it's O(n) time overall. Space is O(n): the two path strings, and the recursion stack, which in a skewed tree is the tree's height — up to n."*
>
> Same big-O as the three-step version, but half the moving parts and no separate LCA routine to get wrong. In an interview, fewer parts means fewer bugs — and that reads as competence.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:50`
*(depth + honesty)*

**[VISUAL: the O(n) path string; a "shrink it?" thought bubble gets a red ✗.]**

> Can we beat O(n) space? **No — and I can say exactly why.**
>
> The **answer itself** can be O(n) characters long. Picture a path that climbs halfway up the tree and back down the other side — that's a linear-length string, and you're *required to return it*. So O(n) is the floor, not waste. The path buffers are just the answer in progress.
>
> **[VISUAL: a tall skewed tree; the output string stretches long beside it.]**
>
> Say that out loud: *"Space is O(n), but that's the length of the path I have to return — a skewed tree forces a linear answer — so it's optimal, not overhead."* Naming *why* it can't shrink is a stronger signal than staying quiet.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Lowest Common Ancestor of a Binary Tree (LC 236)". A blank editor.]**

> Before the next video, go do **Lowest Common Ancestor of a Binary Tree**, LC 236 — the routine this problem was hiding all along. Build the LCA node explicitly this time.
>
> Then a stretch: solve today's problem again but find *both* paths in a **single** DFS that stops once it's seen both values. Same big-O, tighter code. Wrestle with it for ten minutes before you peek — that struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Shortest path between two tree nodes = up to the LCA, then down.** So the answer is always some `U`s then some `L`/`R`s.
> 2. **Two root-to-node paths share a prefix — that prefix is the LCA.** Strip it; you never build an LCA function.
> 3. **Start-side leftovers become `U`s — count them, don't keep the letters.** Reverse of any down-step is just "go up."
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Two paths from the root — delete the shared start."]**
>
> When you see "path between two nodes in a tree," your hand should already be reaching for two root-paths and a prefix strip.
>
> *(GCA reminder — for the interview itself: state the three-step LCA plan first, say out loud "the fiddly part is finding the LCA," *then* reach for the strip trick that removes it. Google's General Cognitive Ability signal isn't the clever line — it's you narrating the path from the obvious solution to the clean one. Ask "values are unique, right?" before you write anything.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Lowest Common Ancestor of a Binary Tree" — the LCA node pulsing red, no parent pointers in sight.]**

> We got the LCA for *free* today because we cheated — we searched from the root twice and let the shared prefix hand it to us. But what if the interviewer asks for the LCA node *directly*, and doesn't let you re-walk from the root each time? Now you need the real one-pass algorithm — the recursion that bubbles the answer up from the leaves. That's next: Lowest Common Ancestor of a Binary Tree. The idea we hid inside today's strip, out in the open. See you there.
