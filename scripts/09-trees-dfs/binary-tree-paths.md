# 🎬 Recording Script — Binary Tree Paths
**Pattern: Tree DFS (backtracking) · LeetCode 257 · Easy · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Path Sum (112) — root-to-leaf DFS. This one *records the trail* and introduces backtracking.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree; two path strings materialize: "1->2->5" and "1->3". Then a bug demo: a shared list showing "1,2,5" leaking into the right branch as "1,2,5,3".]**

> "Return every root-to-leaf path as a string." Last time we answered yes/no; now we want the actual trail — `"1->2->5"`, `"1->3"`.
>
> Here's the bug that bites everyone: you keep one list, append nodes as you go down, and after finishing the left branch… the leftover nodes *leak* into the right branch. Your paths come out corrupted.
>
> The fix is a two-move dance called **backtracking** — choose, then un-choose. Master it here and you've got the skeleton for permutations, subsets, combinations — the entire backtracking family. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: the tree.]**

```
    1
   / \
  2   3
   \
    5
```

> One line: **list every root-to-leaf path, formatted like `"1->2->5"`.**
>
> Two leaves here — 5 and 3 — so two paths: `"1->2->5"` and `"1->3"`. Order doesn't matter. The output is *every* path, so there's no short-circuiting; this is a full traversal that records as it descends.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — the leak)*

**[VISUAL: a single shared `path` list. Descend 1 → 2 → 5, path = [1,2,5], emit. Then WITHOUT cleanup, jump to node 3: path becomes [1,2,5,3] — red X.]**

> Say I keep one shared `path` list and just append as I walk. Down to 1 → path `[1]`. Down to 2 → `[1, 2]`. Down to 5, a leaf → `[1, 2, 5]`, emit `"1->2->5"`. 
>
> Now I back up to explore 3. But my list still says `[1, 2, 5]`. I append 3 → `[1, 2, 5, 3]`.
>
> **[VISUAL: the corrupted path "1->2->5->3" highlighted red — completely wrong.]**
>
> That's garbage. The 2 and 5 from the *left* branch polluted the *right* branch. The shared list remembered a trail I've already left behind. I need to *rewind* it when I back out of a node.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the corrupted list. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The problem: when I finish exploring a node and return to its parent, the shared list still holds *this* node. It should look exactly like it did *before* I entered.
>
> **LEARNER:** So after I'm done with a node's subtree, I just… remove it before returning?
>
> **TEACHER:** Exactly the move. Pause and name the rule: **if I `append` the node when I enter, what's the one line I must run right before I leave — so the list is restored for my sibling?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it)*

**[VISUAL: a breadcrumb trail — dropping a crumb entering each node, picking it back up when leaving. The list stays exactly correct for each branch.]**

> **TEACHER:** The move is **backtracking**: append on the way *in*, pop on the way *out*. Like breadcrumbs — you drop one entering a node, and you *pick it back up* when you leave, so the trail always reflects exactly where you are right now.
>
> The invariant is the whole thing: **when you enter `dfs(node)` and when you leave it, the `path` list is identical.** The `append`…`pop` pair guarantees it. So every leaf sees a `path` that's *exactly* its ancestor chain — nothing left over from a sibling.
>
> **[VISUAL: enter 1 → [1], enter 2 → [1,2], enter 5 → [1,2,5] emit, POP 5 → [1,2], POP 2 → [1], enter 3 → [1,3] emit, POP 3 → [1]. Clean.]**
>
> **LEARNER:** Is there a way to dodge the pop entirely — just pass a fresh copy down each call?
>
> **TEACHER:** There is — pass an immutable string like `path + "->" + val`. Each call gets its own copy, so there's nothing to undo; the "backtrack" is implicit in the copy. Cleaner to write, a bit more allocation. Both are legit — but the explicit push/pop is the skill that generalizes to permutations and subsets, so learn it as the main move.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Choose (append) → recurse → un-choose (pop)."]**

> The line — the backtracking heartbeat: **choose, recurse, un-choose.** Append entering, pop leaving.
>
> "What do I return up?" Here, nothing — the answer accumulates in a shared `result` list, emitted at each leaf. The interesting state flows *down* (the path) and gets *undone* on the way back.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Set up the result and the shared path, plus the inner DFS.

```python
def binaryTreePaths(root):
    result = []
    path = []
    def dfs(node):
        if not node:
            return
```

> **[VISUAL: add chunk 2, highlight append + leaf emit.]** Choose: append this node. If it's a leaf, join the trail into a string.

```python
        path.append(str(node.val))              # choose
        if not node.left and not node.right:
            result.append("->".join(path))      # leaf → record trail
        else:
            dfs(node.left)
            dfs(node.right)
```

> **[VISUAL: add chunk 3, highlight the pop.]** Un-choose — the line that fixes the leak — then kick off and return.

```python
        path.pop()                              # un-choose (backtrack)
    dfs(root)
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: the function; spotlight lines.]**

> The *why*.
>
> `path.append` / `path.pop` — the matched pair. Every entry has exactly one exit, so the list is always restored. That's the invariant that keeps branches from bleeding into each other.
>
> `"->".join(path)` — we build the string *once*, at the leaf, from the complete trail. No repeated string concatenation on the way down.
>
> Note the `pop` is *outside* the if/else — it runs on **every** node, leaf or internal, always undoing this node's append before returning to the parent.
>
> **LEARNER:** Why append `str(node.val)` and not the node itself?
>
> **TEACHER:** Small but real — joining with `"->"` needs strings, and stringifying once on entry beats converting the whole list at every leaf. Minor, but it keeps the leaf emit a clean single `join`.

---

## 9. DRY-RUN THE CODE — `7:15`
*(worked example — prove it)*

**[VISUAL: trace table with path and result columns.]**

| action | `path` | `result` |
|---|---|---|
| enter 1 | `[1]` | `[]` |
| enter 2 | `[1, 2]` | `[]` |
| enter 5 (leaf) | `[1, 2, 5]` → emit | `["1->2->5"]` |
| pop 5, pop 2 | `[1]` | `["1->2->5"]` |
| enter 3 (leaf) | `[1, 3]` → emit | `["1->2->5", "1->3"]` |
| pop 3, pop 1 | `[]` | done ✅ |

> Watch the pops after the left branch restore `path` to `[1]`, so node 3 starts clean and produces `"1->3"` — not the corrupted `"1->2->5->3"`. Backtracking doing its job. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:00`
*(transfer to interview)*

**[VISUAL: Time O(n·h); Space O(h) aux + output.]**

> Say it: *"Every node visited once; joining a path at a leaf costs up to O(h), and total characters emitted is the real bound — so **O(n·h)** time. Auxiliary space is the shared path plus the recursion stack, **O(h)**, on top of the output."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:30`
*(depth + honesty)*

**[VISUAL: backtracking list O(h) aux vs immutable-string O(h²) transient.]**

> Output dominates — the returned strings total O(n·h) characters, unavoidable. The lever is *auxiliary* space.
>
> The **backtracking list**: one shared `path` of size O(h) plus O(h) stack = **O(h)** auxiliary. The **immutable-string** version: each of the O(h) stack frames holds its own partial string of length up to O(h) → **O(h²)** transient, plus allocation churn.
>
> So backtracking is strictly better on auxiliary space — that's *why* it's the "optimised" answer even though both produce identical output. Say: *"One mutated list is O(h); copying a growing string down every branch is O(h²) transient."*

---

## 12. YOUR TURN (active recall) — `9:00`
*(retrieval practice)*

**[VISUAL: "Your turn → 113. Path Sum II" and "78. Subsets".]**

> Before next time: **113 — Path Sum II** — paths summing to a target, same choose/un-choose. Then jump to arrays: **78 — Subsets** or **46 — Permutations** run the *exact same* backtracking skeleton. Recognizing that this dance isn't a tree trick — it's a general technique — is the real win.

---

## 13. LOCK IT IN — `9:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Enumerate ALL paths / combinations" → DFS that records and undoes** (backtracking).
> 2. **Invariant: `path` is identical on enter and exit** — guaranteed by matched append/pop.
> 3. **Backtracking (O(h) aux) beats copying strings down (O(h²))** — same output, less memory.
>
> The peg: **choose, recurse, un-choose** — drop the breadcrumb entering, pick it up leaving.

---

## 14. CLIFFHANGER — `9:50`
*(open loop to next lesson)*

**[VISUAL: a tree with the longest path bending at an internal node, glowing. Title blurred: "Diameter of Binary Tree". A red "O(n²) trap" ghost.]**

> You can now walk and record whole paths. Next problem asks for the *longest* path between any two nodes — the diameter — and it hides one of the classic traps in all of trees: the obvious solution recomputes height over and over and blows up to **O(n²)**. The fix reuses the max-depth reflex you already have, plus one clever twist: return height up, track the answer on the side. One pass. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// Definition: class TreeNode { int val; TreeNode left, right; }
public List<String> binaryTreePaths(TreeNode root) {
    List<String> result = new ArrayList<>();
    if (root == null) return result;
    dfs(root, new StringBuilder(), result);
    return result;
}
private void dfs(TreeNode node, StringBuilder path, List<String> result) {
    int len = path.length();                    // remember state to restore
    if (path.length() > 0) path.append("->");
    path.append(node.val);
    if (node.left == null && node.right == null) {
        result.add(path.toString());            // leaf
    } else {
        if (node.left != null)  dfs(node.left, path, result);
        if (node.right != null) dfs(node.right, path, result);
    }
    path.setLength(len);                         // backtrack
}
```
