# 🎬 Recording Script — Strings Differ by One Character
**Pattern: Hashing / Masking · LeetCode 1554 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hashing for duplicates (Group Anagrams / Two Sum) — but here we hash a *shape*, not a value.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean double `for` loop comparing string pairs is typed out. A LeetCode "Time Limit Exceeded — 62 / 74" banner slams in red.]**

> Interviewer slides you a list of words — all the same length — and asks: *"Are there two of them that differ in exactly one spot?"*
>
> Easy, right? Compare every pair, count the mismatches. You write it. It's *correct*. It passes the samples. You run the big test and — Time Limit Exceeded.
>
> Your code isn't wrong. It's just asking the wrong question `n²` times. By the end of this video you'll replace that whole nested loop with one idea — **blank out a character and hash what's left** — and turn a quadratic timeout into a single clean pass. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, three word-tiles stacked:]**

```
abcd
acbd
aacd
```

> The whole problem in one line: **find two strings that are identical everywhere except one position.**
>
> Same length always — that's promised. And it's *positional*: they must line up and disagree at exactly one index. Not anagrams. Not "one edit." One slot, different letter.
>
> Look at these three. There's a matching pair hiding here — two words that differ in a single spot. Don't hunt yet. Just hold that the answer is **true**.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the three words. A "pair comparisons" counter, top-right, at 0. Arrows link pairs as we check them, letters highlighting on each compare.]**

> Let's do what your brain does first: check every pair, count where they differ.
>
> `abcd` vs `acbd` — index 0 same, index 1 `b` vs `c` differ, index 2 `c` vs `b` differ. Two mismatches. Not it.
>
> **[VISUAL: arrow abcd↔acbd, two red slots light up; counter → 1.]**
>
> `abcd` vs `aacd` — index 0 same, index 1 `b` vs `a` differ, index 2 same, index 3 same. **One** mismatch. That's our pair.
>
> **[VISUAL: arrow abcd↔aacd, single red slot at index 1; counter → 2.]**
>
> Found it — but feel the cost. Three words was three pairs. Ten words is 45. A hundred thousand words? Five **billion** pairs, each a full character scan.
>
> **[VISUAL: counter morphs into "≈ n²/2 · m" with a red glow; "n = 10^5 → 5,000,000,000+".]**
>
> That's the Time Limit Exceeded. The `n²` is the wound.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the `abcd` ↔ `aacd` compare, the un-differing slots `a _ c d` glowing green, the one red slot dimmed. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste: comparing `abcd` to `aacd` taught us nothing we could reuse when we compared `abcd` to `acbd`. Every pair starts from scratch.
>
> **LEARNER:** But that's what the problem *is* — pairs. How do you find a matching pair without checking pairs?
>
> **TEACHER:** By flipping the question. Don't ask "which pairs differ by one?" Ask: **what do two words that differ only at index 1 have in common?** Look at the green slots — `a _ c d`. Pause the video. If you had to store *one thing* about each word so a future word could recognize its near-twin instantly… what would you store?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: `abcd` with index 1 physically erased and replaced by a `*`: `a*cd`. It drops into a "seen shapes" box.]**

> **TEACHER:** Here's the move. Take a word and **blank out one position** — swap it for a wildcard `*`. `abcd` with index 1 blanked becomes `a*cd`.
>
> Think of it like a fingerprint with one smudged digit. Two people whose prints match on *every* digit except the smudged one produce the **same smudged print**. So: if two words collapse to the same blanked-out shape, they're identical everywhere else — they differ only at the blanked slot.
>
> **[VISUAL: `aacd` blanks index 1 → `a*cd`. It floats toward the box and — CLINK — lands on the identical `a*cd` already there. Both glow green.]**
>
> Watch. `aacd`, blank index 1, becomes `a*cd` too. It's already in the box! Same shape, left there by `abcd`. That collision *is* the answer — those two differ in exactly one spot.
>
> **LEARNER:** But you don't know in advance *which* position is the different one. You'd have to blank every position.
>
> **TEACHER:** Exactly right — so we do. For each word, blank position 0, then 1, then 2, then 3 — `m` shapes per word. `abcd` gives `*bcd`, `a*cd`, `ab*d`, `abc*`. We toss all of them in a hash set. The instant any shape repeats, we've found the pair. One pass. The set remembers so we don't have to compare.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "erase the one difference → hash the rest → collision = the pair."]**

> Burn this line in: **to find things that match except for one controlled spot, erase that spot and hash what's left. Two that agree on the rest land in the same bucket.**
>
> That's the whole trick. It's the same reflex as Group Anagrams — there you erase *order* and hash the letters; here you erase *one slot* and hash the frame. Same family.

---

## 7. CODE IT — LIVE & CHUNKED — `5:05`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the memory — a set of shapes we've seen.

```python
def differ_by_one(dict):
    seen = set()
```

> **[VISUAL: add chunk 2, highlight it.]** Now walk each word, and for it, walk each position.

```python
    for word in dict:
        for i in range(len(word)):
```

> **[VISUAL: add chunk 3, spotlight the slicing line.]** Build the wildcard shape — everything before `i`, a `*`, everything after.

```python
            key = word[:i] + '*' + word[i + 1:]
```

> **[VISUAL: add chunk 4, highlight the check-before-add.]** Seen this shape already? That's our pair — return true. Otherwise remember it and move on.

```python
            if key in seen:
                return True
            seen.add(key)
    return False
```

> Nine lines. That nested loop from the cold open is gone.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:35`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `word[:i] + '*' + word[i+1:]` — this rebuilds the word with exactly one slot erased. The `*` is safe because the input is lowercase letters — a `*` can never be a real character, so it can never cause a fake match.
>
> `if key in seen` **before** `seen.add(key)` — order matters. We check first, add second. So a word never matches *itself* — its own shapes aren't in the set yet when we look. Only a *different, earlier* word can trigger the hit.
>
> **LEARNER:** Wait — what if the list has two *identical* words, like `abcd` and `abcd`? They'd collapse to the same shapes too. Wouldn't that wrongly return true? They differ by *zero*, not one.
>
> **TEACHER:** Sharp catch — and the honest answer is: on LeetCode 1554 the strings are distinct, so it's fine. But in a real interview I'd *say that assumption out loud*, and if duplicates were allowed I'd dedupe first, or store the original word next to each shape and confirm they actually differ. Naming that edge case is free interview points.
>
> `seen.add(key)` — the whole word's `m` shapes accumulate here, so every future word gets checked against every past shape in `O(1)`.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: the three words; a trace table filling row by row; the "seen" set growing on the side.]**

```
abcd
acbd
aacd
```

> Let's run the real code and watch the set fill.

| Word | Shapes generated | Any already in `seen`? | Result |
|---|---|---|---|
| `abcd` | `*bcd`, `a*cd`, `ab*d`, `abc*` | no — set was empty | add all four |
| `acbd` | `*cbd`, `a*bd`, `ac*d`, `acb*` | no — none match | add all four |
| `aacd` | `*acd`, **`a*cd`**, `aa*d`, `aac*` | **yes — `a*cd`!** | **return `true`** |

> `a*cd` was stamped by `abcd` when it blanked index 1. `aacd` blanks the *same* index and lands on it. Collision. Loop closed — and the pair is `abcd` / `aacd`, differing only at index 1, exactly the pair we spotted by hand at the start.

---

## 10. COMPLEXITY, OUT LOUD — `8:30`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n² · m). Ours: O(n · m²). A note: "n·m shapes, each O(m) to slice".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is `O(n²·m)` — every pair, every character. My masking version generates `n·m` shapes total, and slicing each shape costs `O(m)`, so it's `O(n·m²)` time. Space is the set of shapes."*
>
> That kills the `n²`. For most inputs, done. But `n·m²` still has an `m²` lurking — and a good interviewer will poke at it. So let's beat it.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:05`
*(depth + honesty)*

**[VISUAL: the slicing line `word[:i]+'*'+word[i+1:]` gets a red underline; beside it, a formula "hash − char·BASEⁱ" in green.]**

> The `O(m)` slicing is doing double damage — it's our time cost *and* it stores a full `m`-length string per shape. Both shrink with one idea: a **rolling hash**.
>
> Hash the whole word once. Then "blanking position `i`" isn't a rebuild — it's *arithmetic*: subtract that one character's contribution from the hash in `O(1)`. Tag each key with the slot index `i` so a blank at slot 2 can't collide with a blank at slot 5. Now it's `O(n·m)` time and `O(n·m)` space — integer keys, not strings.
>
> **LEARNER:** But two different strings can hash to the same number. Couldn't a collision make it return true when there's no real pair?
>
> **TEACHER:** Yes — and *that* is the strong-hire moment. On a hash hit, don't trust the number blindly: **verify** the two actual strings differ by exactly one char before returning true. With a 61-bit prime the odds of collision are astronomically small, but saying *"I'd confirm on a match to be safe"* is precisely the rigor Google's rubric rewards. Name the risk, then handle it.

---

## 12. YOUR TURN (active recall) — `9:55`
*(retrieval practice)*

**[VISUAL: "Your turn → One Edit Distance (LC 161)". A blank editor.]**

> Before the next video, try **One Edit Distance**. Two strings, differ by exactly one *edit* — but now an edit can be a replace **or** an insert **or** a delete, and the lengths can differ by one. Same "one controlled difference" flavor, one dimension harder.
>
> Wrestle with it for ten minutes before you peek. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Comparing every pair is `O(n²)` — that's the timeout.** Flip it into a single remembering pass.
> 2. **Blank one slot, hash the rest.** Two words that collapse to the same shape differ in exactly that slot.
> 3. **Rolling hash makes each blank `O(1)`** — and *verify on a hash hit*, because hashes can lie.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "erase the difference, hash the rest."]**
>
> When you're hunting near-twins that match *except* for one controlled spot, your hand should already be reaching to erase that spot and drop the rest in a set.
>
> *(GCA reminder — for the interview itself: ask the clarifying question first — "one differing index, same length, not anagrams?" — then say the brute force, name the wasted `n²`, then reach for the mask. Google's General Cognitive Ability signal isn't the trick; it's you narrating the path from naive to optimal out loud.)*

---

## 14. CLIFFHANGER — `11:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "One Edit Distance" — two words of *different* lengths sliding past each other, one slot glowing.]**

> Here we had it easy: same length, so positions lined up and we just blanked one. But what happens when the two strings are **different lengths** — when the "one difference" might be an inserted or deleted character that shoves everything after it out of alignment? The mask trick alone won't save you. That's the next one. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean differByOne(String[] dict) {
    Set<String> seen = new HashSet<>();
    for (String word : dict) {
        char[] chars = word.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            char original = chars[i];
            chars[i] = '*';                 // blank position i in place
            String key = new String(chars);
            if (!seen.add(key)) {           // add returns false if already present
                return true;                // collision → differ by exactly one slot
            }
            chars[i] = original;            // restore for the next position
        }
    }
    return false;
}
```
