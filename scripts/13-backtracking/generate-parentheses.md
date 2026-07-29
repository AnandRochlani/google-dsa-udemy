# 🎬 Recording Script — Generate Parentheses
**Pattern: Backtracking · LeetCode 22 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** per-position choices from **Letter Combinations**; the *pruning* idea from **Combination Sum** — now the prune encodes a *rule*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: strings flash by: "(()", ")((", "()(" — a red ✗ stamps most of them. Title: "n = 3: only 5 of 64 are valid."]**

> **TEACHER:** *"Generate every balanced parentheses string with n pairs."* For n = 3, there are 64 ways to arrange six brackets — and only **five** are actually balanced. Fifty-nine are garbage.
>
> The lazy fix: build all 64, check each, keep the 5. But most of that garbage was doomed from the *first character* — a string starting with `)` can never recover. By the end of this video, you'll build a version that *never creates an invalid string in the first place* — so tight that there's no validity check at all. The rule lives inside the prune. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: `n = 2`. The two answers: "(())" and "()()". Beside them, invalid ones crossed out: ")(", "))((" …]**

> One line: **all well-formed parentheses strings with n pairs.**
>
> Tiny example: n = 2. Two valid answers — `(())` and `()()`. Everything else with two open and two close, like `)(` padded out, is unbalanced.
>
> "Balanced" means two things at once: you never close a bracket you didn't open, and by the end everything's matched. Those two rules are the entire problem — hold them.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: a full binary tree, each level choosing '(' or ')', depth 2n=4 for n=2. 16 leaves, most stamped ✗.]**

> Brute force: each of the `2n` positions is either `(` or `)`. Just generate all `2` to the `2n` strings and filter.
>
> **[VISUAL: the tree fills; a leaf like ")()(" gets built fully, THEN checked, THEN rejected.]**
>
> For n = 2 that's 16 strings. Build each one completely, then run a balance check, then throw most away.
>
> Now watch this specific branch: the very first character is `)`. That string is *already dead* — a close bracket with nothing to close. But brute force doesn't notice. It cheerfully builds `)(`, `))`, `)()`, all of it, before the final check rejects them. We did full work on strings that were hopeless at character one.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on a half-built ")(" glowing red. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is precise: we detect invalidity *only at the very end*, after building the whole string — even when it died at the first character.
>
> **LEARNER:** But hold on — isn't this just the phone-keypad problem again? Per-position choices, build them all? Why can't I just enumerate like last time?
>
> **TEACHER:** Because last time *every* branch was valid — nothing to reject. Here most branches are poison. Enumerate-all-then-filter drowns you. So pause and predict: **as I build the string left to right, what tiny fact could I track that tells me instantly whether adding a `(` or a `)` right now could still lead to a balanced string — before I commit?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a node showing counts (open, close). Two rules light up: "open < n → may add '('" and "close < open → may add ')'". A decision tree pruned by these — the whole ")" half of the root never drawn.]**

> **TEACHER:** Track two counts as we build: how many `(` we've placed — call it `open` — and how many `)` — `close`. Now, when is it safe to add each?
>
> Add a `(` — only if `open < n`. If we've already placed all n opens, another one overflows. And add a `)` — only if `close < open`. That's the crucial one: you can only close a bracket that's actually *open*. If closes have caught up to opens, there's nothing left to close — a `)` would go negative.
>
> **[VISUAL: at the root, open=0, close=0. Rule for ')': close < open → 0 < 0 → FALSE. The entire ")..." subtree is grayed out and never entered.]**
>
> Here's the magic. At the very root, `close < open` is `0 < 0` — false. So we *never even consider* starting with `)`. That entire poisoned half of the tree is pruned *before it exists.* We're not building and rejecting — we're refusing to build.
>
> **[VISUAL: hand walks down a valid path (→"(", →"((", →"(()", →"(())"), records at the leaf, walks back up.]**
>
> And the rhythm is our skeleton. **CHOOSE** a bracket the rules permit. **RECURSE** with the updated count. **UN-CHOOSE** — pop — to try the other bracket. The `open` and `close` counts ride along on the call stack, so they rewind automatically; only the shared buffer needs the explicit pop.
>
> The payoff: because the two rules keep *every* prefix valid, any string that reaches full length `2n` is *guaranteed* balanced. **No final validity check. Ever.**

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: two boxed rules, huge: "add '(' if open < n" and "add ')' if close < open".]**

> Two rules, and they *are* the algorithm: **add an open while `open < n`; add a close while `close < open`.** Those conditions encode the balance rule directly into the tree's shape, so no invalid string is ever born. The prune *is* the rule.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it. Setup.

```python
def generate_parenthesis(n):
    result = []
    path = []
```

> **[VISUAL: add chunk 2, highlight the leaf — note NO validity check.]** The walker carries the two counts. At full length, record — no check needed.

```python
    def backtrack(open_count, close_count):
        if len(path) == 2 * n:            # leaf: guaranteed balanced
            result.append(''.join(path))
            return
```

> **[VISUAL: add chunk 3, highlight the `open < n` guard.]** First rule — add an open if we haven't spent them all.

```python
        if open_count < n:                # can we add '('?
            path.append('(')              # CHOOSE
            backtrack(open_count + 1, close_count)  # RECURSE
            path.pop()                    # UN-CHOOSE
```

> **[VISUAL: add chunk 4, highlight `close < open`.]** Second rule — add a close only if there's an unmatched open.

```python
        if close_count < open_count:      # can we add ')'?
            path.append(')')              # CHOOSE
            backtrack(open_count, close_count + 1)  # RECURSE
            path.pop()                    # UN-CHOOSE

    backtrack(0, 0)
    return result
```

> Two `if`s, each wrapping a choose-recurse-un-choose. Notice there's no `valid()` call anywhere. The guards make it unnecessary.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> The *why*.
>
> `if len(path) == 2 * n` records with *no* validity test — because the two guards guaranteed balance the whole way down. That absence of a check is the point, not an oversight.
>
> `if open_count < n` — never place more than n opens. `if close_count < open_count` — never close more than you've opened. Together they're exactly the invariant of a balanced *prefix*.
>
> **LEARNER:** Wait — the two counts are just passed as arguments, and I don't see them being reset anywhere. Don't I need to un-choose them like the buffer?
>
> **TEACHER:** Beautiful catch, and no — and here's the difference. `open_count` and `close_count` are plain integers passed *by value*. Each recursive call gets its own copy; the parent's copy is never touched. So when recursion returns, they're automatically back to what they were. The `path` buffer is different — it's *one shared list* everyone mutates, so *it* needs the explicit `pop`. Rule of thumb: state passed by value auto-rewinds; shared mutable state needs a manual un-choose.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: decision tree for n=2, hand walking, counts (open,close) on each node, the ")" half never drawn.]**

> Run it for n = 2.

```
backtrack(0,0) path=""
  add '(' → backtrack(1,0) path="("
    add '(' → backtrack(2,0) path="(("
      open==n, no more '('; close<open → add ')' → "(()"
        add ')' → "(())"  LEAF record ✅
    close<open → add ')' → backtrack(1,1) path="()"
      add '(' → backtrack(2,1) path="()("
        add ')' → "()()"  LEAF record ✅
      close==open → no ')'
  (root: close<open is 0<0 → false, so ')' is never even tried)
```

> The root refuses `)` outright — that whole invalid half never gets drawn. We reach exactly `(())` and `()()`. Our two answers, and we never built a single piece of garbage. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: "Brute: O(2²ⁿ · n)." "Pruned: O(4ⁿ / √n) — the Catalan number." "Auxiliary: O(n)."]**

> Out loud: *"Brute force is 2-to-the-2n strings times O(n) to validate each. The pruned version only ever touches valid prefixes, so the node count collapses to the Catalan number — about 4-to-the-n over root-n — times O(n) to build each string. The output is Catalan-many strings, and that's inherent."*
>
> The interviewer's takeaway: pruning here didn't just shave a constant — it changed the *base* of the exponential, from `2²ⁿ` down to Catalan. That's a real win, and worth stating plainly.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty — output vs auxiliary)*

**[VISUAL: box "OUTPUT: O(Catalan · n) — inherent." box "AUXILIARY: O(n) — buffer + stack; counters are free ints."]**

> Output versus auxiliary. Output holds Catalan-many strings of length `2n` — inherent. Auxiliary: one `path` buffer, length ≤ `2n`, plus recursion depth ≤ `2n` → `O(n)`.
>
> And the two counters cost nothing — they're just integers riding the call stack, one copy per frame, already counted in the `O(n)` depth.
>
> Say it: *"Auxiliary space is O(n) — one shared buffer plus the call stack — and the balance counters are just two ints on the stack. The exponential part is only the required output."* Already optimal; nothing to trim.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Remove Invalid Parentheses (LC 301)". Editor: `s = "()())()"`.]**

> Try **Remove Invalid Parentheses** — given a messy string, remove the *fewest* brackets to make it valid, and return all such results. It flips today's problem: instead of *building* valid strings, you *prune down* an invalid one, still with backtracking and a balance-style rule. Ten minutes before you peek.

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Two counters — `open < n`, `close < open`** — encode the balance rule into the tree.
> 2. **Valid-by-construction** means *no final check* — the prune replaced it.
> 3. **By-value state auto-rewinds; shared buffers need a manual un-choose.**
>
> The peg: **make the rule the prune.** Don't build-then-check — build only what *can* be valid, and the check disappears.

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a 3×4 grid of letters, a snaking arrow spelling a word. Title: "Word Search".]**

> Every problem so far built a string or a list, top to bottom. Next we leave the number line entirely and backtrack across a *2-D grid* — hunting a word by stepping to neighboring cells, up-down-left-right, no cell reused. The un-choose gets physical: you'll *un-mark a square* on the way back out. Same skeleton, new terrain. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<String> generateParenthesis(int n) {
    List<String> result = new ArrayList<>();
    backtrack(new StringBuilder(), 0, 0, n, result);
    return result;
}

private void backtrack(StringBuilder path, int open, int close, int n, List<String> result) {
    if (path.length() == 2 * n) {
        result.add(path.toString());                  // balanced leaf
        return;
    }
    if (open < n) {                                   // can add '('
        path.append('(');                             // CHOOSE
        backtrack(path, open + 1, close, n, result);  // RECURSE
        path.deleteCharAt(path.length() - 1);         // UN-CHOOSE
    }
    if (close < open) {                               // can add ')'
        path.append(')');                             // CHOOSE
        backtrack(path, open, close + 1, n, result);  // RECURSE
        path.deleteCharAt(path.length() - 1);         // UN-CHOOSE
    }
}
```
