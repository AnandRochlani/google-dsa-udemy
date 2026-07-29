# 🎬 Recording Script — Permutations
**Pattern: Backtracking · LeetCode 46 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the choose→recurse→un-choose skeleton and the `start` index from **Subsets** (last lesson).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: three cards labeled 1, 2, 3 being shuffled into different orders on a table. A counter: "orderings = ?"]**

> **TEACHER:** Last video, backtracking gave us every *subset* of a list. This one looks almost identical — *"give me every ordering of [1,2,3]"* — and interviewers love pairing them, because the tiny difference between them is exactly what they're testing.
>
> If you reach for the same `start`-index trick from subsets… it breaks. It'll quietly drop half your answers. By the end of this video you'll know the *one part* you swap out to go from subsets to permutations — and why. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: tiles `1 2 3`. Beside them, all six orderings listed: `[1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]`.]**

> One line: **return every possible ordering — every permutation.**
>
> Three numbers, and there are the six arrangements. Why six? First slot: 3 choices. Once you've placed one, second slot: 2 left. Then 1. So 3 times 2 times 1 — three factorial, six. That shrinking set of choices per slot is the tell.
>
> And notice — unlike subsets, every answer here has *length 3*. A permutation must use *every* element. Hold that; it changes where we record.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — surface the trap)*

**[VISUAL: the subsets code from last lesson pinned at the top, with its `start`-index loop. An arrow tries to reuse it here.]**

> Your instinct after last lesson: "I've got the skeleton — choose, recurse, un-choose, with a `start` index. Reuse it."
>
> **[VISUAL: trace it — start=0 picks 1, then start=1 can only pick 2 or 3… it can NEVER go back and pick 1 after 2. Orderings like [2,1,3] shown in red, unreachable.]**
>
> So we pick 1, then from *after* 1 we pick 2, then 3 — we get `[1,2,3]`. But when we pick 2 first, the `start` index says "only look *forward*," so we can never come back for the 1. `[2,1,3]` is unreachable. The forward-only rule that *saved* us in subsets now *destroys* us here.
>
> Feel that. The skeleton's right. One assumption inside it is wrong for this problem.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the unreachable orderings glowing red. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the exact clash. In subsets, `[1,2]` and `[2,1]` are the *same* subset, so forward-only was a *feature* — it killed the duplicate. In permutations they're *different* answers — both wanted. So "only look forward" is throwing away real answers.
>
> **LEARNER:** Okay, so just… let it look backward? Loop over the whole list every time?
>
> **TEACHER:** Close — but if you loop over the *whole* list every time with nothing stopping you, you'll pick `[1,1,1]`. You'd reuse element 1 three times. So pause and predict: **if I'm allowed to pick from anywhere, what one piece of bookkeeping stops me from reusing an element I've already placed?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a decision tree. Root branches 3 ways (1, 2, 3). Each child branches 2 ways (the remaining), each of those 1 way. Leaves at depth 3 are the 6 permutations.]**

> **TEACHER:** Here's the tree. The root branches *three* ways — which element goes first. Pick 1, and the next level branches *two* ways — 2 or 3, whatever's left. Then one way. Leaves at depth 3 are the six permutations.
>
> The answer to the bookkeeping question: instead of a `start` index, carry a **`used`** marker — a little checklist of which elements are already in your hand. At each slot you try every element that's *not* used. That's it. That's the one swapped part.
>
> **[VISUAL: an animated hand walks down: choose 1 (mark 1 used), choose 2 (mark 2 used), choose 3 → leaf. Then walk BACK UP, un-marking 3, un-marking 2, freeing them for the sibling branch.]**
>
> **LEARNER:** Wait — won't a plain `used` array make it *slower* than the tidy `start` index?
>
> **TEACHER:** It's the same asymptotic cost — we're visiting every node either way. The `used` array isn't overhead, it's the thing that lets us reach the answers `start` couldn't. And watch the rhythm — it's *identical* to subsets, just with a second thing to undo. **CHOOSE**: place an unused element, mark it used. **RECURSE**: fill the next slot. **UN-CHOOSE**: pop it *and* mark it unused. The un-choose now rewinds *two* things — the path and the `used` flag — but it's the same walk-down, walk-back-up.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "Subsets → `start` index. Permutations → `used` set." Below: "record only at the leaf."]**

> The one line to remember: **subsets use a `start` index; permutations use a `used` set.** That's the fork in the road for this whole family of problems.
>
> And one more: because a permutation must use *everything*, we only record at the **leaf** — when the path is full length — not at every node like subsets.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Setup — answers, the path, and the new piece: a `used` flag per element.

```python
def permute(nums):
    result = []
    path = []
    used = [False] * len(nums)
```

> **[VISUAL: add chunk 2, highlight.]** The leaf check — record only when the path is complete.

```python
    def backtrack():
        if len(path) == len(nums):        # leaf: a full ordering
            result.append(path[:])        # snapshot
            return
```

> **[VISUAL: add chunk 3, highlight the `used` guard.]** Now try every element that isn't already in our hand.

```python
        for i in range(len(nums)):
            if used[i]:
                continue                  # already placed — skip
```

> **[VISUAL: add chunk 4, highlight the paired mark/unmark.]** And the three-beat rhythm — now undoing *two* things.

```python
            path.append(nums[i])          # CHOOSE
            used[i] = True
            backtrack()                   # RECURSE
            path.pop()                    # UN-CHOOSE
            used[i] = False

    backtrack()
    return result
```

> Look at the choose and the un-choose. `append` + `used = True` going in; `pop` + `used = False` coming back out. They mirror each other perfectly. That symmetry is how you know your backtracking is correct.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line.]**

> The *why*.
>
> `if len(path) == len(nums)` — a permutation must use every element, so a partial path is never an answer. We only snapshot at full length. Contrast subsets, where we recorded at *every* node.
>
> `if used[i]: continue` — this is what replaced the `start` index. It lets us look in *every* direction — backward included, so `[2,1,3]` is reachable — while forbidding the *one* thing we must forbid: reusing an element already in the path.
>
> **LEARNER:** So why do we need both the `pop` *and* the `used[i] = False`? Feels redundant.
>
> **TEACHER:** They undo two different pieces of state. `pop` shortens the path back to what it was. `used[i] = False` frees element i for a *sibling* branch to grab. Skip the `pop` and your path grows forever. Skip the `used = False` and once you've used an element in one branch, it's poisoned for every branch after — you'd get only one permutation and then dead ends. Both undos, every time. That's the discipline.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: decision tree for [1,2,3] with a hand walking it; used-array shown as [F/T,F/T,F/T] updating live.]**

> Run it on 1, 2, 3.

```
path=[], used=[F,F,F]
  choose 1 → path=[1], used=[T,F,F]
    choose 2 → path=[1,2], used=[T,T,F]
      choose 3 → path=[1,2,3]  LEAF → record; undo 3
    undo 2  (used→[T,F,F])
    choose 3 → path=[1,3]
      choose 2 → [1,3,2]  LEAF → record; undo
    undo
  undo 1  (used→[F,F,F])
  choose 2 → path=[2] …  → [2,1,3], [2,3,1]
  choose 3 → path=[3] …  → [3,1,2], [3,2,1]
```

> Watch the un-choose free things up. After `[1,2,3]`, we undo the 3, undo the 2 — `used` goes back to `[T,F,F]` — and *now* the freed 3 is available so `[1,3,...]` can grab it. That's the rewind working. Six leaves, six permutations. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: "n! leaves × O(n) copy = O(n · n!) time." Beside it: "auxiliary O(n)."]**

> Out loud: *"There are n-factorial orderings, and each costs O(n) to copy at the leaf, so time is O(n times n-factorial). The factorial is inherent — the output itself has n-factorial permutations, so nothing beats it."*
>
> Same headline as subsets, different exponential: subsets was 2-to-the-n, permutations is n-factorial. Both **inherent to the output.** That phrase again — say it in the room.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty — output vs auxiliary + the swap trick)*

**[VISUAL: box "OUTPUT: O(n·n!) — inherent." box "AUXILIARY: O(n) — path + used + stack." Then a small board showing in-place swaps.]**

> Output versus auxiliary, again. The output is `O(n · n!)` — inherent. The auxiliary is the `used` array (n), the path (n), and the recursion depth (n) — all `O(n)`. Already lean.
>
> But there's a tidy trick worth naming: you can drop the `used` array entirely by permuting `nums` *in place* with swaps — the array *becomes* the path.

```python
def permute_inplace(nums):
    result = []
    def backtrack(first):
        if first == len(nums):
            result.append(nums[:])
            return
        for i in range(first, len(nums)):
            nums[first], nums[i] = nums[i], nums[first]   # CHOOSE (swap in)
            backtrack(first + 1)                          # RECURSE
            nums[first], nums[i] = nums[i], nums[first]   # UN-CHOOSE (swap back)
    backtrack(0)
    return result
```

> The swap-back *is* the un-choose. Say it: *"I can permute the array in place with swaps instead of carrying a used-array, undoing each swap on the way back up."* Auxiliary space is still `O(n)` — the stack dominates — but it's a slick detail that shows depth.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Permutations II (LC 47)". Editor with `nums = [1, 1, 2]`.]**

> Try **Permutations II** — permutations when the input has *duplicates*, like `[1, 1, 2]`. You don't want the same ordering twice.
>
> Hint: sort first, then skip a duplicate at the same level *unless* its twin was just used. It's the `used` array plus one clever skip condition. Wrestle with that skip line — it's the trickiest one in this whole family.

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **`start` index → `used` set** is the *only* structural change from subsets.
> 2. **Record at the leaf**, because permutations use every element.
> 3. **Un-choose undoes everything you chose** — pop the path *and* free the `used` flag.
>
> The peg: **subsets look forward; permutations remember what's used.** Same walk down the tree, different bookkeeping.

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a new title blurred: "Combination Sum". A target number "7" glowing, with candidates that can repeat.]**

> So far our trees have been *fixed* shape — n elements, clean levels. Next problem changes the game: you're hunting for combinations that hit a *target sum*, numbers can *repeat as many times as you like*, and most branches *overshoot and die*. That's where we meet the most powerful weapon in backtracking — **pruning**: cutting off whole branches before we waste a step on them. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, new ArrayList<>(), new boolean[nums.length], result);
    return result;
}

private void backtrack(int[] nums, List<Integer> path, boolean[] used, List<List<Integer>> result) {
    if (path.size() == nums.length) {
        result.add(new ArrayList<>(path));            // snapshot at leaf
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        path.add(nums[i]); used[i] = true;            // CHOOSE
        backtrack(nums, path, used, result);          // RECURSE
        path.remove(path.size() - 1); used[i] = false; // UN-CHOOSE
    }
}
```
