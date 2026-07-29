# 🎬 Recording Script — Combination Sum
**Pattern: Backtracking · LeetCode 39 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the choose→recurse→un-choose skeleton and the `start` index from **Subsets**.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a target "7" glowing at the top. Candidate tiles `2 3 6 7`. A tree starts exploding into hundreds of branches, most stamped with a red ✗.]**

> **TEACHER:** *"Find every combination of these numbers that adds up to seven — and you can reuse a number as many times as you want."* Sounds friendly. But watch the search tree — it explodes, and *most* of those branches shoot past seven and die.
>
> Here's the thing: a lazy solution explores all of them and throws the dead ones away. A *good* one refuses to even walk down a branch it can prove is doomed. That's **pruning** — the single most powerful idea in backtracking — and it's what this whole video is about. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: `candidates = [2, 3, 6, 7]`, `target = 7`. Answer shown: `[[2,2,3], [7]]`.]**

> One line: **every combination that sums to the target, and you may reuse numbers.**
>
> Tiny example: candidates 2, 3, 6, 7, target 7. Two answers hide in there. `2 + 2 + 3` — notice the 2 used *twice*, that's allowed. And `7` by itself. `[[2,2,3], [7]]`.
>
> Two twists versus subsets: numbers can *repeat*, and we only keep paths that hit an *exact* target. Both of those shape the tree.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: a decision tree from root rem=7. Each node branches on "which candidate to add." A "remaining" number rides each node, going 7 → 5 → 3 → 1 → -1 (red).]**

> Let's think in terms of what's *left to reach*. Call it `remaining`, starting at 7. Add a 2 — remaining drops to 5. Add another 2 — 3. Another — 1. Another — *minus one*. We overshot. Dead branch.
>
> **[VISUAL: many branches drawn all the way down to a negative leaf before turning red.]**
>
> The naive version keeps adding, and only *after* the recursive call comes back does it check "oh, remaining went negative, throw this away." We built the whole doomed branch just to discover it was doomed.
>
> And it keeps trying 6 and 7 as additions even when only 1 is left to fill — guaranteed overshoots, every one built before being rejected.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on a node with remaining=1, still trying to add 2, 3, 6, 7 — all overshoot. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look right here. Remaining is 1. We're about to try adding 2 — overshoot. Then 3 — overshoot. Then 6, then 7 — all overshoot. We *test each one*, descend, come back, reject. Four wasted descents from one node.
>
> **LEARNER:** But isn't that just how search works? You have to try them to know they don't fit… right? Isn't that unavoidable brute force?
>
> **TEACHER:** That's the exact instinct pruning kills. We *don't* have to try them one by one. Pause and predict: **if I sorted the candidates smallest-to-largest, and the smallest one I'm about to try already overshoots — what does that tell me about all the ones after it?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: candidates sort to `[2, 3, 6, 7]`. At a node with remaining=1, an arrow hits 2 → "2 > 1, and everything after is bigger" → whole rest of the row grayed out with one slash.]**

> **TEACHER:** Sort them: 2, 3, 6, 7 — ascending. Now stand at that node with remaining 1. Try 2 — it's bigger than 1, overshoot. But here's the leap: the candidates are *sorted*. If 2 already overshoots, then 3, 6, and 7 — every larger candidate — overshoots too. **Guaranteed.**
>
> So I don't skip just this one candidate. I `break` — I abandon the *entire* rest of the loop. One check kills four branches.
>
> **[VISUAL: the hand walks down a valid branch (2→2→3, remaining hits 0, record), then walks back up; at each level the "break" chops the grayed siblings.]**
>
> That's pruning: using a cheap fact — sorted order — to cut off whole subtrees *before* you walk into them. Instead of exploring and rejecting, you *reason* and refuse.
>
> Now, the reuse twist. Numbers can repeat. In subsets we recursed with `start = i + 1` — strictly forward, never reuse. Here we recurse with `start = i` — *same* index allowed, so the current candidate stays on the table — but we still never go *backward*. That "same or forward, never back" is what keeps `[2,2,3]` from also appearing as `[3,2,2]`. Same combination, generated once.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: two boxed lines: "Sort → break when candidate > remaining (PRUNE)." and "Reuse allowed → recurse with `i`, not `i+1`."]**

> Two lines to burn in. **Sort, then break the moment a candidate exceeds what's remaining** — that's the prune. And **recurse with `i`, not `i+1`, so a number can be reused** — but never go backward, which keeps combinations unique.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it. First — sort, so the prune works — and set up.

```python
def combination_sum(candidates, target):
    candidates.sort()                     # enables the break-prune
    result = []
    path = []
```

> **[VISUAL: add chunk 2, highlight the base case.]** The walker carries `remaining`. When it hits zero, we've got an answer.

```python
    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])        # exact hit — snapshot
            return
```

> **[VISUAL: add chunk 3, highlight the break line hard.]** The loop — and the prune. This one line is the whole lesson.

```python
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:  # PRUNE: this and all later overshoot
                break
```

> **[VISUAL: add chunk 4, highlight `i` in the recurse call.]** Choose, recurse *with `i`* for reuse, un-choose.

```python
            path.append(candidates[i])            # CHOOSE
            backtrack(i, remaining - candidates[i])  # RECURSE — i allows reuse
            path.pop()                            # UN-CHOOSE

    backtrack(0, target)
    return result
```

> Two things make this problem itself: the `break` on line one of the loop, and the `i` — not `i+1` — in the recurse. Everything else is the skeleton you already know.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:15`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> The *why*.
>
> `candidates.sort()` — this is the *foundation of the prune*. Without sorting, "this candidate overshoots" tells you *nothing* about the next one, because the next could be smaller. Sorted, an overshoot guarantees every later one overshoots too. That's what upgrades a `continue` (skip one) into a `break` (skip all).
>
> `if candidates[i] > remaining: break` — the prune. We chop off every larger sibling in one stroke.
>
> **LEARNER:** Hold on — why `break` and not `continue`? Aren't you scared you'll skip a candidate that *could* have worked?
>
> **TEACHER:** Great fear, and the answer is *because it's sorted*. If candidate `i` is already bigger than what's remaining, everything to its right is bigger still — none of them can fit. There's nothing valid past this point in the row, so bailing entirely is safe. If the list *weren't* sorted, you'd be right — you'd have to `continue` and keep checking. Sorting is what earns the `break`.
>
> `backtrack(i, remaining - candidates[i])` — passing `i`, not `i+1`, keeps the current number available to use again. But we never pass anything *less* than `i`, so we never go backward — that's the uniqueness guarantee.

---

## 9. DRY-RUN THE CODE — `8:30`
*(worked example — prove it, close the loop)*

**[VISUAL: decision tree for [2,3,6,7], target 7, with break-chops shown as scissors and a hand walking down/up.]**

> Run it. Sorted candidates 2, 3, 6, 7, target 7.

```
backtrack(0, rem=7)
  choose 2 → backtrack(0, rem=5)
    choose 2 → backtrack(0, rem=3)
      choose 2 → backtrack(0, rem=1)
        2 > 1 → break ✂ (kills 2,3,6,7)   → dead, back up
      choose 3 → backtrack(1, rem=0)       → record [2,2,3] ✅
      6 > 3 → break ✂
    choose 3 → backtrack(1, rem=2)
      3 > 2 → break ✂                      → dead
  choose 3 → backtrack(1, rem=4) …         → no hit
  choose 6 → backtrack(2, rem=1) → 6>1 break ✂
  choose 7 → backtrack(3, rem=0)           → record [7] ✅
```

> See the scissors fire every time a candidate outgrows `remaining`. We reach exactly two zeros — `[2,2,3]` and `[7]`. Our two answers. Loop closed, and look how few nodes we actually touched.

---

## 10. COMPLEXITY, OUT LOUD — `9:30`
*(transfer to interview)*

**[VISUAL: "Time: O(n^(target/min)) worst case — pruning slashes the constant." "Auxiliary: O(target/min)."]**

> Out loud: *"Worst case the tree is exponential — branching factor n, depth bounded by target over the smallest candidate — so roughly n-to-the-target-over-min. The output can be exponential too, and that's inherent. But the sort-and-break pruning cuts the number of nodes I actually visit *dramatically* — same big-O ceiling, a tiny fraction of the work in practice."*
>
> The honest line interviewers respect: pruning usually doesn't change the *worst-case* big-O — it demolishes the *typical* running time. Say both.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:10`
*(depth + honesty — output vs auxiliary)*

**[VISUAL: box "OUTPUT: O(k · #combos) — inherent." box "AUXILIARY: O(target/min) — path depth + stack."]**

> Output versus auxiliary. The output stores every valid combination — `O(k · number-of-combinations)`, inherent, it's the answer.
>
> Auxiliary: just the recursion stack plus the single `path` list. How deep can recursion go? The deepest path is all-smallest-candidate — `target / min(candidates)` levels. So auxiliary is `O(target / min)`. Nothing else grows.
>
> Say it: *"My only extra memory is the recursion depth — capped at target over the smallest candidate — plus the one path I mutate and undo. Everything else is the required output. Oh, and the sort is O(n log n) time for basically free pruning."*

---

## 12. YOUR TURN (active recall) — `10:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Combination Sum II (LC 40)". Editor: `candidates = [10,1,2,7,6,1,5]`, `target = 8`.]**

> Try **Combination Sum II** — now each number can be used *only once*, and the input can have *duplicates*.
>
> Two changes from today: recurse with `i + 1` (no reuse), and after sorting, skip a duplicate candidate *at the same level* so you don't repeat a combination. It's this exact skeleton with the reuse turned off and one dedup line added. Ten minutes before you peek.

---

## 13. LOCK IT IN — `11:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Sort unlocks the prune** — `break` when a candidate exceeds `remaining`.
> 2. **Reuse = recurse with `i`; no-reuse = `i+1`.** Never go backward — that's uniqueness.
> 3. **`remaining == 0` is the goal; `remaining < 0` is death** — and pruning stops us before we ever get there.
>
> The peg: **sort, then chop.** The moment a sorted candidate overshoots, take the scissors to the whole rest of the row.

---

## 14. CLIFFHANGER — `11:55`
*(open loop to next lesson)*

**[VISUAL: a phone keypad blurred in; "2 → abc, 3 → def". Title: "Letter Combinations".]**

> We just used pruning to *cut* branches. Next problem does the opposite — it's the one member of this family where you *can't* prune, because *every* branch is valid. It's the old phone keypad: 2 spells a-b-c, 3 spells d-e-f, and you generate every word the number could type. Pure enumeration, the skeleton with the pruning muscle switched off — a clean palate cleanser before things get hard again. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    Arrays.sort(candidates);                          // enables break-prune
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, 0, target, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] c, int start, int remaining,
                       List<Integer> path, List<List<Integer>> result) {
    if (remaining == 0) {
        result.add(new ArrayList<>(path));            // valid leaf
        return;
    }
    for (int i = start; i < c.length; i++) {
        if (c[i] > remaining) break;                  // PRUNE
        path.add(c[i]);                               // CHOOSE
        backtrack(c, i, remaining - c[i], path, result); // RECURSE (i => reuse)
        path.remove(path.size() - 1);                 // UN-CHOOSE
    }
}
```
