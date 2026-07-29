# 🎬 Recording Script — Count Words Obtained After Adding a Letter
**Pattern: Bitmask / Hash Set · LeetCode 2135 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hash-set membership (Two Sum's "have I seen it?") — plus a tiny bit of bit-flipping.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: editor with a clean nested-loop solution. A LeetCode "Time Limit Exceeded — 34 / 41" banner slams in red.]**

> You read the problem. It says: take a start word, add one letter, shuffle it, does it spell the target? Easy — for every target, loop over every start word and check. You write it. It's *correct*. It passes 34 tests.
>
> Then test 35 — fifty thousand start words, fifty thousand targets — and the screen goes red. Time Limit Exceeded.
>
> Your logic is fine. It's just doing *billions* of comparisons. By the end of this video you'll turn each word into a **single integer**, and the whole check becomes one hash lookup. The trick is spotting *why* you're allowed to. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, two little columns:]**

```
startWords:  ant   act   tack
targetWords: tack  act   acti
```

> The whole problem in one line: **a target counts if you can take some start word, add exactly one brand-new letter, rearrange, and spell the target.**
>
> Tiny example. Three starts, three targets. And one gift the problem hands us, underlined in the fine print: **every word has all-distinct letters.** No word repeats a letter. Hold onto that — it's the whole ballgame.
>
> The answer here is **two**. Don't chase it yet. Just hold: two of these three are obtainable.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the two columns. A "checks" counter, top-right, starting at 0. Arrows fan from each target to every start word.]**

> Let's do what your brain does first. Take a target, and test it against *every* start word. The rule: a start qualifies if it's exactly one letter shorter and all its letters live in the target.
>
> Target `tack`. Check against `ant`… against `act` — yes! `act` plus a `k`, rearranged, is `tack`. Counter ticks. That's one.
>
> **[VISUAL: arrows tack→ant, tack→act light up; checks counter climbs to 2.]**
>
> Next target, `acti`. Check `ant`… `act` — yes again, `act` plus `i`. But look what I just did — I scanned the *whole start list a second time.*
>
> **[VISUAL: the same three start words glow again for the second target; counter jumps.]**
>
> Three targets, each re-scanning all the starts. Now picture fifty thousand of each.
>
> **[VISUAL: counter morphs into "≈ |target| × |start| ≈ 2.5 × 10⁹" with a red glow.]**
>
> Billions of checks. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight one target re-scanning the entire start list. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste. For every target I walk the *entire* start list, just to answer one yes/no question: *does a matching start exist?* That's a **membership** question. And we have a tool that answers membership instantly — no scanning.
>
> **LEARNER:** Sure, a hash set — but a set of *what*? The words are different lengths, different orders. `act` and `cat` and `tca` are the "same" for this problem. What do I even put in the set?
>
> **TEACHER:** That is *exactly* the right question. Pause the video. If order doesn't matter and letters never repeat… what's the smallest thing that captures a word's identity?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the word `act` sitting above a row of 26 light switches labeled a…z. Switches a, c, t flip ON; the rest stay off.]**

> **TEACHER:** Two facts save us. **One: we're allowed to rearrange** — so the *order* of letters is pure noise. **Two: every word has distinct letters** — so a word is just the *set* of letters in it, nothing lost.
>
> And there are only 26 lowercase letters. So picture a row of **26 light switches**, one per letter. A word flips ON the switches for its letters. `act` → switches a, c, t are on. That's it. That row of on/off switches is a **26-bit number** — one integer that *is* the word.
>
> **[VISUAL: the switches collapse into a binary number, then a single tidy integer badge on `act`.]**
>
> Now watch what "add one new letter" becomes. Adding a letter that wasn't there = **flipping one OFF switch to ON.** So going *backwards* — from target to start — is **flipping one ON switch to OFF.**
>
> **[VISUAL: `tack` = {a,c,t,k}. Its `k` switch clicks OFF → {a,c,t}. A label: "= act!"]**
>
> Take target `tack` — switches a, c, t, k. Click *off* the `k` → a, c, t → that's `act`, which is a start word! So `tack` is obtainable. The whole test is: **can I turn off one switch of the target and land on a start word?**
>
> **LEARNER:** Wait — but I don't know *which* letter was the added one. Do I have to guess?
>
> **TEACHER:** You don't guess — you *try them all*. A target has at most 26 letters, so you try clearing each ON bit, one at a time, and ask the set: "is this a start word?" At most 26 cheap lookups per target. That's the trade — 26 lookups instead of fifty thousand.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "distinct letters + rearrange allowed ⇒ word = 26-bit mask; 'add a letter' = clear one bit and look it up."]**

> Burn this in: **when letters are distinct and order doesn't matter, a word is a 26-bit mask — and "add exactly one new letter" reverses into "clear one set bit and check the start set."**
>
> That's the entire lesson. The instant you see *small fixed alphabet + rearrange + distinct*, your hand reaches for a bitmask and a hash set.

---

## 7. CODE IT — LIVE & CHUNKED — `5:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Piece one — turn a word into its mask. For each letter, switch on its bit.

```python
def mask(word):
    m = 0
    for ch in word:
        m |= 1 << (ord(ch) - ord('a'))   # switch on this letter's bit
    return m
```

> **[VISUAL: add chunk 2, highlight it.]** Piece two — throw every start word's mask into a set. This is our instant-lookup table.

```python
starts = {mask(w) for w in startWords}
```

> **[VISUAL: add chunk 3, the loop skeleton.]** Piece three — for each target, build its mask, then try clearing each of its letters.

```python
count = 0
for w in targetWords:
    t = mask(w)
    for ch in w:                         # try removing each letter of the target
        b = 1 << (ord(ch) - ord('a'))
        if (t ^ b) in starts:            # does clearing it land on a start word?
            count += 1
            break                        # obtainable — stop, don't double-count
```

> **[VISUAL: highlight the `t ^ b` line, then the `break`.]** `t ^ b` flips off exactly that one bit. If the result is in `starts`, we found a valid start word — count it and **break**, so we never count the same target twice. Then just `return count`.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `m |= 1 << (ord(ch) - ord('a'))` — `ord(ch) - ord('a')` maps `a`→0, `b`→1, up to `z`→25. `1 << that` is the switch for that letter; `|=` flips it on. This is where a string becomes an int.
>
> `starts = {mask(w) ...}` — a **set**, not a list. That's the whole point: `in` on a set is O(1), not a scan.
>
> `t ^ b` — XOR with a single set bit *clears* it. Since `b` is a letter that's definitely in `t`, this is exactly "remove that one letter."
>
> **LEARNER:** Why XOR and not just subtract, or an AND with a mask? Feels fragile.
>
> **TEACHER:** Because `b` is guaranteed to be ON in `t` — we built `b` from a letter of the word itself. XOR of an on-bit with itself is off. So `t ^ b` reliably clears exactly that bit and touches nothing else. Clean and exact.
>
> **LEARNER:** And the `break` — why is that safe?
>
> **TEACHER:** A target only needs *one* valid start word to count. The moment we find one, we're done with this target — breaking stops us from adding it again if a second start also happens to match.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the start masks listed as switch-rows, then a trace table filling row by row.]**

> Build the start set first: `ant`→{a,n,t}, `act`→{a,c,t}, `tack`→{a,c,t,k}. Now run the targets.

| Target | Mask `t` | Try clearing each letter | In `starts`? | count |
|---|---|---|---|---|
| `tack` | {a,c,t,k} | −a, −c, −t… **−k → {a,c,t}** | ✅ (`act`) | 1 |
| `act` | {a,c,t} | −a→{c,t}, −c→{a,t}, −t→{a,c} | ❌ none | 1 |
| `acti` | {a,c,t,i} | −a, −c, −t… **−i → {a,c,t}** | ✅ (`act`) | 2 |

> `tack` clears its `k` and hits `act` — count 1. `act` tries all three removals, nothing's a start word — there's no 2-letter start to grow from — so it's skipped. `acti` clears its `i` and hits `act` — count 2. Final answer **two**, exactly what we promised. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(|target|·|start|·26). Ours: O((|start|+|target|)·26). Note: "26 = alphabet, the word cap".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Building every mask is `(|start| + |target|) × 26`. Each target then does at most 26 hash lookups. So total time is `O((|start| + |target|) × 26)` — linear in the input. Space is `O(|start|)` for the set of masks."*
>
> Compare to brute force's `|target| × |start|` — that's the jump from ten billion operations to a couple million. Same answer, different universe.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: the mask set; a "shrink it?" thought bubble appears, gets a red ✗.]**

> Can we cut the `O(|start|)` space? **No — and I can say exactly why.** To answer targets in constant time I need to *remember* every start word, and a mask is already the leanest possible memory of one — a single 26-bit int. The set of masks isn't overhead, it **is** the algorithm.
>
> Say it out loud in the interview: *"Space is `O(|start|)` and that's the floor — I need one mask per start word for O(1) lookups, and a mask is the most compact form a distinct-letter word has."* Naming *why* it can't shrink scores more than silently shrugging.

---

## 12. YOUR TURN (active recall) — `10:05`
*(retrieval practice)*

**[VISUAL: "Your turn → Maximum Product of Word Lengths (LC 318)". A blank editor.]**

> Before the next video, try **Maximum Product of Word Lengths**. Same reflex: turn each word into a 26-bit mask. But now the question is whether two words share *no* letters — so you check `maskA & maskB == 0`. Same tool, new bitwise move.
>
> Don't peek. Wrestle with it ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Pairwise scanning is `|target|·|start|` → timeout.** Replace the scan with a hash-set lookup.
> 2. **Distinct letters + rearrange allowed ⇒ a word is a 26-bit mask.** Order is noise.
> 3. **"Add one letter" reverses to "clear one set bit."** Try clearing each bit of the target; if it's in the start set, it counts.
>
> The memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "distinct letters + rearrange ⇒ think bits, not strings."]**
>
> When you see a small fixed alphabet, rearranging allowed, and no repeated letters — your hand should already be reaching for a bitmask and a set.
>
> *(GCA reminder — for the interview itself: don't jump to bitmasks silently. Ask "the letters in each word are all distinct, right?" out loud, then say *why* that lets you treat a word as a set of bits. Google's General Cognitive Ability signal isn't the trick — it's you narrating the leap from the naive scan to the mask. Say the "order doesn't matter" insight before you write a single `<<`.)*

---

## 14. CLIFFHANGER — `11:05`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Group Anagrams" — the word `aabb` flashing with a red "letter repeats!" tag.]**

> This whole trick leaned on one gift: **no repeated letters.** That's what let one bit stand for one letter. But what happens when a word is `aabb` — when letters *can* repeat, and a single on/off switch can't tell "one a" from "two a's"? The bitmask breaks. Next up: Group Anagrams — same "order doesn't matter" spirit, but now we need a richer fingerprint than a bag of bits. See you there.
