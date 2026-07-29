# 🎬 Recording Script — Letter Combinations of a Phone Number
**Pattern: Backtracking · LeetCode 17 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the choose→recurse→un-choose skeleton from **Subsets**; the pruning from **Combination Sum** (which we deliberately *don't* need here).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an old flip-phone keypad. Finger taps "2", then "3". Letters cascade: abc, def. Title: "How many words can 23 spell?"]**

> **TEACHER:** Old-school texting. On a keypad, 2 is a-b-c, 3 is d-e-f. Type "23" and it could spell a whole bunch of two-letter combos. Google asks: *"Give me every one."*
>
> Your first instinct is nested loops — one per digit. But how many loops? You don't know until you see the input. You can't hand-write a loop-per-digit when the digit count is a variable. By the end of this video you'll see why that's a *recursion* in disguise — and why this problem is the gentlest one in the whole backtracking family. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: `digits = "23"`. Mapping shown: 2→abc, 3→def. Answer grid: ad ae af / bd be bf / cd ce cf.]**

> One line: **every string the number could spell**, using the keypad mapping.
>
> Tiny example: "23". The 2 gives us a, b, or c. The 3 gives us d, e, or f. Pair each letter of the first with each of the second — 3 times 3, nine strings: ad, ae, af, bd, be, bf, cd, ce, cf.
>
> That "each with each" is a **Cartesian product**. Keep that word — it's the whole shape of the problem.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — surface the shape)*

**[VISUAL: two nested for-loops typed out for "23": `for ch1 in 'abc': for ch2 in 'def':`. Then a third digit "4" appears and a THIRD loop has to be added by hand.]**

> Do it the obvious way for "23": a loop over a, b, c, and *inside* it a loop over d, e, f. Nine combos, done. Clean.
>
> **[VISUAL: input changes to "234". The code physically can't keep up — a third nested loop gets jammed in, then a fourth for "2345".]**
>
> But now the input is "234" — you need a *third* nested loop. "2345"? A *fourth*. The number of loops is `len(digits)`, which is an input. You literally cannot write it with fixed nesting.
>
> Feel the itch: "a loop, nested to a depth I don't know at write-time." That itch has a name.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: the stack of nested loops, with "?? levels deep" flashing. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The pain is precise: **the number of nested loops equals the number of digits, and that's not known until runtime.** Fixed `for` loops can't express a variable depth.
>
> **LEARNER:** So is this a totally different technique from subsets? It doesn't have a `start` index *or* a `used` set — feels like neither.
>
> **TEACHER:** Sharp — it's neither, and that's the clue. Pause and predict: **what tool naturally gives you "a loop, nested as deep as the input is long," where each level picks from a different set of options?**
>
> *(pause)* … It's recursion. One recursive call *per digit* — the recursion depth becomes your loop nesting.

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a decision tree for "23". Root branches 3 ways (a, b, c). Each branches 3 ways (d, e, f). Leaves at depth 2 spell the 9 words.]**

> **TEACHER:** Here's the tree. Level 0 is digit "2" — the root branches three ways: a, b, c. Level 1 is digit "3" — each of those branches into d, e, f. A path from root to a leaf at depth 2 spells one word. Nine leaves, nine words.
>
> **[VISUAL: hand walks down a→d (leaf "ad"), back up to a, down a→e ("ae"), a→f, back up to root, down b…]**
>
> And walking it is our exact rhythm. **CHOOSE** a letter for the current digit. **RECURSE** to the next digit. **UN-CHOOSE** — pop the letter — to try the next one. Same choose-recurse-un-choose.
>
> But here's what makes this the *easy* one: **there's nothing to prune.** In combination sum, most branches overshot and died. Here? *Every* letter choice is legal. Every branch reaches a valid leaf. This is pure enumeration — the skeleton with the pruning muscle completely relaxed.
>
> One more difference from subsets and permutations: no `start` index, no `used` set. What you're allowed to pick is decided purely by *which digit you're on* — your position. You advance by index, and at each index you loop over *that digit's* letters.

---

## 6. THE KEY MOVE (signaling) — `4:00`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "Advance by index; loop over THIS position's options. No prune — every leaf is valid."]**

> The line to remember: **advance by index, and at each index loop over that position's choices.** Recursion depth replaces your nested loops. And because every choice is valid, there's *no prune and no final check* — every leaf is an answer.

---

## 7. CODE IT — LIVE & CHUNKED — `4:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it. Edge case first — empty input means no combinations — then the keypad map.

```python
def letter_combinations(digits):
    if not digits:
        return []
    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl',
               '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = []
    path = []
```

> **[VISUAL: add chunk 2, highlight the leaf.]** The walker advances by `index`. When it runs off the end, the path is a complete word — glue it into a string.

```python
    def backtrack(index):
        if index == len(digits):          # leaf: one full combination
            result.append(''.join(path))  # materialize the string
            return
```

> **[VISUAL: add chunk 3, highlight the loop over THIS digit's letters.]** Loop over the current digit's letters — choose, recurse to the next digit, un-choose.

```python
        for ch in mapping[digits[index]]: # options for THIS digit
            path.append(ch)               # CHOOSE
            backtrack(index + 1)          # RECURSE to next digit
            path.pop()                    # UN-CHOOSE

    backtrack(0)
    return result
```

> No prune, no validity test at the leaf. Every path is automatically a legal word. That's what "the easy one" looks like in code.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:10`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> The *why*.
>
> `if not digits: return []` — the spec says empty input returns an empty list, *not* a list containing the empty string. Easy point to drop; easy point to catch.
>
> `if index == len(digits)` — this is our leaf, and it's driven by *position*, not by a count of used elements or a target. When we've placed one letter per digit, we're done.
>
> `for ch in mapping[digits[index]]` — the branching set changes per level, and it's dictated entirely by which digit we're standing on. That's the structural signature of this problem.
>
> **LEARNER:** Quick one — why `''.join(path)` at the leaf instead of building the string as we go? Wouldn't carrying a string be simpler?
>
> **TEACHER:** You *could* pass a string down and add a character each call. But strings are immutable — every "add a char" makes a fresh copy, so you'd copy at every node. Instead I keep one mutable list buffer, push and pop into it, and only pay for a string *once*, at the leaf, when I actually have an answer. It's the leaner choice — one buffer, materialized only when it matters.

---

## 9. DRY-RUN THE CODE — `7:15`
*(worked example — prove it, close the loop)*

**[VISUAL: decision tree for "23", hand walking down and up, buffer contents shown live.]**

> Run it on "23".

```
backtrack(0), path=[]
  choose 'a' → path=['a']
    backtrack(1)
      choose 'd' → "ad"  record; pop
      choose 'e' → "ae"  record; pop
      choose 'f' → "af"  record; pop
    pop 'a'
  choose 'b' → path=['b']  → "bd","be","bf"
  choose 'c' → path=['c']  → "cd","ce","cf"
```

> Watch one buffer serve the whole tree: finish all of a's children, *pop* the a, push b, go again. Down, up, down. Nine strings: ad ae af bd be bf cd ce cf. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:00`
*(transfer to interview)*

**[VISUAL: "Time: O(4ⁿ · n) — up to 4 letters/digit, n digits, O(n) to join each." "Auxiliary: O(n)."]**

> Out loud: *"Each digit maps to up to 4 letters — 7 and 9 have four — so with n digits there are up to 4-to-the-n combinations, each length n to build. Time is O(4-to-the-n times n). That's inherent — the output itself is that many strings."*
>
> Same refrain: the exponential is the *output*, not wasted work. There's no faster way to *list* an exponential number of things.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:35`
*(depth + honesty — output vs auxiliary)*

**[VISUAL: box "OUTPUT: O(4ⁿ · n) — inherent." box "AUXILIARY: O(n) — one buffer + stack." Contrasted with iterative version holding a whole frontier layer.]**

> Output versus auxiliary. Output is `O(4ⁿ · n)` — inherent. Auxiliary is just the one `path` buffer, length ≤ n, plus recursion depth ≤ n → `O(n)`.
>
> Here's a sharp contrast to name. You *could* solve this iteratively — start with `['']` and, per digit, rebuild the whole list by tacking on each letter. But that keeps a whole *layer* of partial strings alive at once — up to `4ⁿ⁻¹` of them — that's exponential *working* memory, on top of the output.
>
> Say it: *"The iterative product keeps a full frontier of partial strings in memory; my recursion keeps just one buffer and the O(n) call stack — strictly leaner on auxiliary space."*

---

## 12. YOUR TURN (active recall) — `9:10`
*(retrieval practice)*

**[VISUAL: "Your turn → Generate Parentheses (LC 22)". Editor with `n = 3`.]**

> Next up is your turn *and* the next lesson rolled together: **Generate Parentheses.** Generate all balanced bracket strings with n pairs. It's per-position choices again — add a `(` or a `)` — but this time, unlike today, *not every choice is valid.*
>
> Try it before the next video. You'll feel exactly where "no pruning" stops working and you're forced to bring the scissors back.

---

## 13. LOCK IT IN — `9:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Variable-depth nesting → recursion.** One recursive call per position.
> 2. **The branching set comes from your position** — no `start`, no `used`.
> 3. **No prune here** — every branch is valid, so this is pure enumeration.
>
> The peg: **recursion is a for-loop whose depth you don't know yet.** When the nesting depends on the input, reach for it.

---

## 14. CLIFFHANGER — `10:05`
*(open loop to next lesson)*

**[VISUAL: a bracket string "(()" with a red "?" — is it still savable? Title: "Generate Parentheses".]**

> Today every branch was a winner. Next problem yanks that away: build bracket strings, but a `)` with nothing to close is *instant death*. If you enumerate all of them and filter — like the phone problem — you drown in garbage. The trick is two little counters that make every prefix *provably* valid, so tight there's no final check at all. Pruning returns, sharper than ever. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
private static final String[] MAP = {
    "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
};

public List<String> letterCombinations(String digits) {
    List<String> result = new ArrayList<>();
    if (digits == null || digits.isEmpty()) return result;
    backtrack(digits, 0, new StringBuilder(), result);
    return result;
}

private void backtrack(String digits, int index, StringBuilder path, List<String> result) {
    if (index == digits.length()) {
        result.add(path.toString());                  // materialize at leaf
        return;
    }
    String letters = MAP[digits.charAt(index) - '0'];
    for (char ch : letters.toCharArray()) {
        path.append(ch);                              // CHOOSE
        backtrack(digits, index + 1, path, result);   // RECURSE
        path.deleteCharAt(path.length() - 1);         // UN-CHOOSE
    }
}
```
