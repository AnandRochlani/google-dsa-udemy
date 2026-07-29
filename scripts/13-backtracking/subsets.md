# 🎬 Recording Script — Subsets
**Pattern: Backtracking · LeetCode 78 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the *template*. Every other backtracking video points back here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an Google phone-screen chat window. Interviewer types: "Return every possible subset of [1,2,3]." Cursor blinks on an empty editor.]**

> **TEACHER:** Google phone screen. The interviewer says: *"Give me every subset of this list."* And your brain goes blank — not because it's hard, but because you don't know where to *start*. Do you loop? Loop how many times? The number of loops depends on the input.
>
> Here's the promise: by the end of this video you'll have one tiny code skeleton — choose, recurse, un-choose — that solves this, and the next six problems in this course. Learn it *once*, here. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, three tiles: `1  2  3`. To the side, all 8 subsets listed faintly: `[] [1] [2] [3] [1,2] [1,3] [2,3] [1,2,3]`.]**

> The whole problem in one line: **return every subset — the power set.**
>
> Our tiny example is just three numbers: 1, 2, 3. And there are the eight subsets it produces. Count them — eight. Hold onto that number. Notice the empty set counts, and the full set counts.
>
> Why eight? Three elements, and each one is either *in* or *out*. Two choices, three times — 2 times 2 times 2. That "in or out, per element" is the crack we pry the whole solution open with.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the shape)*

**[VISUAL: the three tiles. Under each, a tiny toggle switch flipping IN / OUT. A binary counter ticks 000, 001, 010, 011… beside it.]**

> Let's do what your brain reaches for first. "In or out per element" — that's just binary. Give each element a bit. `000` means nobody's in — the empty set. `001` means just element 1. `101` means 1 and 3.
>
> **[VISUAL: counter runs 000→111, each row lighting up the matching tiles and writing the subset next to it.]**
>
> Run the counter from `000` to `111` — that's 0 to 7 — and read off which bits are on. Eight numbers, eight subsets. It genuinely works.
>
> So we *can* just count in binary. Hold that — it's correct. But watch what happens the moment the problem gets one degree harder.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: a new constraint slides in red over the problem: "…only subsets that sum to ≤ 4." The binary counter keeps grinding through ALL 8 masks anyway, several highlighted as wasted.]**

> **TEACHER:** Now the interviewer adds a twist: *"only the subsets that sum to at most four."* Watch the binary counter. It *still* builds all eight masks, then throws away the bad ones at the end. It can't stop early — a full mask is all-or-nothing.
>
> **LEARNER:** Wait — isn't that fine, though? Eight is nothing. Isn't the binary trick just... the answer?
>
> **TEACHER:** For *plain* subsets, sure. But the binary counter has no way to say "this half-built pick is already doomed, don't finish it." The instant a problem needs to *prune* — abandon a bad branch early — the counter is stuck. Pause here: **what if, instead of numbering finished subsets, we *built* each subset one element at a time — so we could bail the moment it goes bad?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a decision tree grows from a root labeled `[]`. Left edge "skip 1", right edge "take 1". It keeps branching per element until leaves appear.]**

> **TEACHER:** Here's the mental model that unlocks everything. Draw a tree. At the root, you've picked nothing — the empty set. Then you walk *down*, and at each step you decide the fate of the next element.
>
> **[VISUAL: highlight one root-to-node path: take 1 → take 2 → gives node [1,2].]**
>
> Every path down the tree is you making choices. And here's the beautiful part for subsets — **every node you land on is itself a valid subset**, because a subset can be any length. So we don't just want the leaves; we want to *visit every node*.
>
> How do you walk a tree like this by hand? Depth-first. Go down one branch as far as it goes, then back up and try the next. Like exploring a maze with your hand on the wall — walk in, hit a wall, back out to the last fork, take the other passage.
>
> **[VISUAL: an animated hand walks DOWN a branch to a leaf, then walks BACK UP to the last fork, then down the sibling branch. Trail glows going down, dims coming back up.]**
>
> And that walk has a rhythm — three beats. **CHOOSE**: add an element to my current path. **RECURSE**: go deeper, decide the next one. **UN-CHOOSE**: on the way back up, *remove* that element, so the path is clean for the sibling branch. Choose, recurse, un-choose. That un-choose — the rewind — is the whole reason it's called *back*-tracking.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line, huge: "CHOOSE → RECURSE → UN-CHOOSE." Under it, smaller: "a depth-first walk of the decision tree."]**

> Burn this line in: **choose, recurse, un-choose.** That is the entire backtracking template — a depth-first walk of a decision tree, undoing each choice as you back out.
>
> One more piece for subsets specifically: to avoid making the same subset twice — like `[1,2]` and `[2,1]` — we only ever look *forward*. Once we've passed an element, we never reconsider it. We carry a `start` index that says "you may only pick from here on."

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First the setup — where answers go, and the path we're carrying.

```python
def subsets(nums):
    result = []
    path = []
```

> **[VISUAL: add chunk 2, highlight it.]** Now the recursive walker. The very first thing it does at *every* node: record the current path — because every node is a valid subset.

```python
    def backtrack(start):
        result.append(path[:])        # snapshot: every node is a subset
```

> **[VISUAL: add chunk 3, highlight the loop and the three commented beats.]** Now the three-beat rhythm. Loop over elements from `start` forward — choose, recurse, un-choose.

```python
        for i in range(start, len(nums)):
            path.append(nums[i])      # CHOOSE nums[i]
            backtrack(i + 1)          # RECURSE — only elements after i
            path.pop()                # UN-CHOOSE — undo, try the next i
```

> **[VISUAL: add chunk 4.]** And kick it off from index zero.

```python
    backtrack(0)
    return result
```

> That's the whole thing. Nine lines. Stare at that loop body — `append`, `backtrack`, `pop` — that's choose, recurse, un-choose, and you'll see it in every problem after this.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk the *why*.
>
> `result.append(path[:])` at the top — this records a subset at *every* node, not just leaves, because every prefix is a legitimate subset.
>
> **LEARNER:** Hold on — why `path[:]`? Why not just append `path`? It's the same list.
>
> **TEACHER:** That's the bug that bites everyone. `path` is *one* mutable list we keep editing. If you append `path` itself, every entry in `result` is a pointer to that same list — and by the end, after all the pops, it's empty. So `result` becomes a stack of empty lists. `path[:]` takes a *snapshot* — a copy frozen at this moment. Say it out loud when you code: "snapshot, not the live list."
>
> `range(start, len(nums))` and recursing with `i + 1` — this is the forward-only rule. By only ever picking elements *after* the current one, each subset is generated in exactly one increasing order. `[1,2]` yes; `[2,1]` never happens. No duplicates, none missed.
>
> And `path.pop()` — the un-choose. After I've fully explored "take 1, then take 2," I pop the 2 so I can explore "take 1, then take 3" with a clean path. One shared list, mutated and rewound. That pop is backtracking.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: the decision tree for [1,2,3], and a trace list filling as the walker descends and pops. An animated pointer walks the tree in sync with the table.]**

> Let's run it on 1, 2, 3 and watch the tree fill.

```
backtrack(0), path=[]        → record []
  choose 1 → path=[1]
    backtrack(1)             → record [1]
      choose 2 → path=[1,2]
        backtrack(2)         → record [1,2]
          choose 3 → [1,2,3] → record [1,2,3]; pop → [1,2]
        pop → [1]
      choose 3 → path=[1,3]  → record [1,3]; pop → [1]
    pop → []
  choose 2 → path=[2] …      → records [2], [2,3]
  choose 3 → path=[3] …      → records [3]
```

> Follow the down-then-up: we dive to `[1,2,3]`, record it, then *pop* back up to `[1,2]`, up to `[1]`, and branch into `[1,3]`. Every pop is the hand walking back to the last fork.
>
> Output: `[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]`. That's our eight. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: "2ⁿ nodes × O(n) copy = O(n · 2ⁿ) time." Beside it: "auxiliary O(n)."]**

> Say it the way you'd say it in the room: *"There are 2-to-the-n subsets, and at each I make an O(n) copy for the snapshot, so time is O(n times 2-to-the-n). That exponential is inherent — the output alone has 2-to-the-n subsets, so no algorithm beats it."*
>
> The key phrase that scores points: **the output is exponential by definition.** You're not being asked to beat 2-to-the-n — you can't. You're being asked to enumerate *without waste*.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty — output vs auxiliary)*

**[VISUAL: two labeled boxes. Big box "OUTPUT: O(n·2ⁿ) — inherent, it's the answer." Small box "AUXILIARY: O(n) — one path + recursion depth."]**

> This is the beat that separates good from great: **output space versus auxiliary space.**
>
> The output holds all 2-to-the-n subsets — that's `O(n · 2ⁿ)`, and you *cannot* shrink it. It's the answer, not overhead.
>
> But your *auxiliary* space — the extra memory the algorithm burns beyond the output — is just the one `path` list, at most length n, plus the recursion stack, depth at most n. That's `O(n)`. Nothing else grows.
>
> So when the interviewer asks "can you do better on space," the strong-hire answer is: *"The output is exponential and that's inherent — but my auxiliary space is only O(n): one path I mutate in place and undo, plus O(n) recursion depth. Nothing else scales with the input."* Naming that distinction is the move.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Subsets II (LC 90)". A blank editor with `nums = [1, 2, 2]`.]**

> Before the next video, try **Subsets II** — same problem, but now the input can have *duplicates*, like `[1, 2, 2]`. You don't want `[2]` listed twice.
>
> Hint from today's skeleton: sort first, then at each level skip an element equal to the one you just tried. Same choose-recurse-un-choose, one skip line added. Struggle with it ten minutes before you peek. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Backtracking = choose, recurse, un-choose** — a depth-first walk of a decision tree.
> 2. **Snapshot with `path[:]`**, never the live list.
> 3. **`start` index = forward-only**, which kills duplicate subsets for free.
>
> And the memory peg — the hand on the maze wall: **walk down making choices, walk back up undoing them.** That image *is* backtracking.

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Permutations". A tree where order suddenly matters — [1,2] and [2,1] both wanted.]**

> One catch we leaned on hard today: the `start` index, "only look forward," which stopped `[2,1]` from being a duplicate of `[1,2]`. But the next problem — permutations — *wants* both `[1,2]` and `[2,1]`. Order matters now. So the forward-only trick breaks. What replaces it? That's next. Same skeleton, one swapped part. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> path, List<List<Integer>> result) {
    result.add(new ArrayList<>(path));            // snapshot current subset
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);                        // CHOOSE
        backtrack(nums, i + 1, path, result);     // RECURSE
        path.remove(path.size() - 1);             // UN-CHOOSE
    }
}
```
