# 🎬 Recording Script — Number of Matching Subsequences
**Pattern: Bucketing / Multiple Pointers · LeetCode 792 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the two-pointer subsequence check (Is Subsequence, LC 392) — we build straight on top of it.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A tidy per-word two-pointer loop is typed out. A LeetCode "Time Limit Exceeded — 44 / 61" banner slams in red.]**

> You know how to check if one string is a subsequence of another. Two pointers, walk both, done. So when the interviewer asks *"how many of these words are subsequences of `s`?"*, you loop that check over every word. Clean. Correct.
>
> You hit submit and — Time Limit Exceeded.
>
> Your code isn't *wrong*. It's re-reading the big string thousands of times. By the end of this video you'll fix it with one idea — parking each word in a bucket for the character it's waiting on — and sweep the whole thing in a single pass. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below it:]**

```
s = "abcde"
words = ["a", "bb", "acd", "ace"]
```

> The whole problem in one line: **count how many words in the list are subsequences of `s`.**
>
> A subsequence keeps the left-to-right order but can skip letters. So `"ace"` lives inside `"abcde"` — a, then c, then e, in order. `"aec"` does not.
>
> Keep your eye on these four words. The answer is **3** — hold that number. We'll earn it by hand before we write a line.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: `s = "abcde"`. A "scans of s" counter, top-right, at 0. For each word, a fresh arrow crawls left-to-right across all of `s`.]**

> Let's do what your brain does first. For each word, walk `s` from the start and tick off the word's letters in order.
>
> `"a"` — scan `s`, hit `a`, done. One full trip queued. **[counter → 1]**
>
> `"bb"` — scan `s` from the top again, find one `b`… then walk the rest of `s` looking for a second `b` that never comes. Whole string, wasted. **[counter → 2]**
>
> `"acd"` — start over at the top *again*: a, c, d. **[counter → 3]** `"ace"` — from the top *yet again*: a, c, e. **[counter → 4]**
>
> **[VISUAL: four separate full-width arrows stacked over the same `s`, all starting at index 0.]**
>
> Four words, four full sweeps of `s`. Now picture 5000 words and an `s` of 50000 characters. That's 250 million steps — all of it re-reading the same string.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. All four arrows highlighted, every one starting at index 0. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Spot the waste. Every word restarts its scan of `s` from the very beginning. `s` is the big expensive thing, and we're reading it front-to-back once per word.
>
> **LEARNER:** But the words need different letters at different times — don't they *have* to each look through `s` on their own?
>
> **TEACHER:** That's the assumption to break. Here's the thing: at any single moment, a word cares about exactly **one** character — its next unmatched one. So here's your think: instead of *"each word scans `s`,"* what if **`s` scans once**, and each word just waits for the letter it needs? Pause. Where would you *put* a word while it waits?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: 26 labelled mailboxes, a…z. Each word drops as a card into the mailbox of its FIRST letter.]**

> Here's the move — think of it like a mailroom. We line up 26 pigeonholes, one per letter. Each word waits in the pigeonhole of the character it needs **next**.
>
> Seed it: park every word on its *first* letter.
>
> **[VISUAL: cards land — `"a"`, `"acd"`, `"ace"` into box `a`; `"bb"` into box `b`. Boxes c–z empty.]**
>
> Now we walk `s` **once**. Each character we read is like calling out a mailbox number. Everyone waiting there wakes up, advances one letter, and gets re-filed under their *new* next letter.
>
> **[VISUAL: read `a` from `s`. Box `a` empties. `"a"` card flips to a green ✓. `"acd"` and `"ace"` re-file into box `c`.]**
>
> Read `a`. Everyone in box `a` steps forward. `"a"` had nothing left — it's a full match, green check. `"acd"` and `"ace"` now need `c`, so they move to box `c`.
>
> **LEARNER:** Wait — when a word re-files into a *later* box, could the same sweep hit it again and double-count it in one step?
>
> **TEACHER:** Sharp, and that's the one bug to avoid. The trick: **empty the mailbox first, then re-file.** We snapshot everyone waiting on `c` *right now*, clear the box, and only then drop the re-filed cards in. So a word that jumps from box `a` to box `c` waits for a *future* `c` in `s` — never the character we're standing on. Each word advances at most once per position. No double-count.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Park each word on its NEXT char. Sweep s once. Wake the bucket, advance, re-park."]**

> Burn this one line in: **bucket every word by the character it's waiting on, sweep `s` once, and each letter wakes its bucket — advance them, re-park them.**
>
> That's the whole pattern. Any time you'd re-scan one long stream once per query — invert it. Index by *what each item is waiting for*.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First the buckets — a dict of lists — and seed every word on its first character. We store a `(word, index)` pair: the word, and how far into it we've matched.

```python
from collections import defaultdict

def num_matching_subseq(s, words):
    waiting = defaultdict(list)
    for w in words:
        waiting[w[0]].append((w, 0))   # park each word on its first char
```

> **[VISUAL: add chunk 2, highlight it.]** Now the single sweep. For each character `c` in `s`, grab its bucket and — this is the load-bearing line — **clear it before we touch anyone.**

```python
    matched = 0
    for c in s:                        # ONE pass over s
        blocked = waiting[c]
        waiting[c] = []                # clear FIRST, so re-parks aren't re-seen now
```

> **[VISUAL: add chunk 3, highlight the `i + 1`.]** Advance each waiting word by one. If it ran off its end, it's a full subsequence — count it. Otherwise re-park it on its new next character.

```python
        for w, i in blocked:
            i += 1                     # c matched this word's char
            if i == len(w):
                matched += 1           # ran off the end → full match
            else:
                waiting[w[i]].append((w, i))   # re-park on next needed char
    return matched
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:55`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `waiting[w[0]].append((w, 0))` — the seed. Every word starts life waiting on its first letter. The invariant we're protecting all the way through: *a word sits in `waiting[c]` exactly when `c` is the character it needs next.*
>
> `waiting[c] = []` — **clear before advancing.** This is the whole correctness trick.
>
> **LEARNER:** Right, why does clearing there matter so much? Couldn't I just loop the bucket and re-append?
>
> **TEACHER:** If you re-append into the *same* list you're iterating, a word that advances from `c` onto a later `c` could get picked up again in this very step — matched twice against one position of `s`. By snapshotting into `blocked` and resetting the bucket to empty, the re-parked cards land in a *fresh* list that this step never revisits. One position of `s`, at most one advance per word.
>
> `if i == len(w): matched += 1` — running off the end means every character was found, in order. That *is* the definition of a subsequence.
>
> And the cost: each character of `s` is read once, and a word is only ever touched when the exact letter it's waiting for shows up. So across the whole run, each word-character is processed exactly once.

---

## 9. DRY-RUN THE CODE — `8:05`
*(worked example — prove it, close the loop)*

**[VISUAL: the buckets on the left, `s = "abcde"` scanning on the right, a trace table filling row by row.]**

> Let's run the real code. Seed: box `a` = `["a", "acd", "ace"]`, box `b` = `["bb"]`.

| Read `c` | Bucket taken | Advance | Result / re-park |
|---|---|---|---|
| `a` | `("a",0),("acd",0),("ace",0)` | →1 each | `"a"` ends → **matched=1**; `"acd"`,`"ace"` → box `c` |
| `b` | `("bb",0)` | →1 | `"bb"` → box `b` (still needs another `b`) |
| `c` | `("acd",1),("ace",1)` | →2 each | `"acd"` → box `d`; `"ace"` → box `e` |
| `d` | `("acd",2)` | →3 | `"acd"` ends → **matched=2** |
| `e` | `("ace",2)` | →3 | `"ace"` ends → **matched=3** |

> `"bb"` is still stranded in box `b` at the end — there was never a second `b` — so it's never counted. Final answer: **3**. Exactly the three we promised. Loop closed.
>
> And notice — we read `s` **once**, not four times. That's the win, made concrete.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(|words| · |s|). Ours: O(|s| + Σ|words|). Note: "each word-char processed once".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is O(words times length of `s`) — we re-scan `s` for every word. My bucket version reads `s` exactly once, and every character across all the words is processed exactly once, because a word is only touched when its next letter appears. So it's O(length of `s` plus total word length). Space is O(total word length) for the pairs in the buckets."*
>
> That's the sentence that turns a Medium from "I think" into "I've got this."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: a `(word, i)` card zooming in — an arrow to the word, a small integer `i`. A red ✗ over a `w[i:]` substring copy.]**

> Quick, and here honesty scores points.
>
> Can we shrink the space? **Not really — and I can say exactly why.** I have to remember where every unfinished word is up to, so `O(total word length)` is the floor. But there's a real trap to *avoid*: store an **index**, not a substring. If you re-park with `w[i:]` — a fresh slice each time — every move copies characters and you blow up both time and space. Storing `(word, i)` — a reference plus an int — keeps re-parking O(1).
>
> Say it out loud: *"Space is O(total word length) and that's optimal — I must track every live word's progress — but I store an index, never a substring copy, so re-parking stays constant time."* Naming *why* it can't shrink is the strong-hire move.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Longest Word in Dictionary through Deleting (LC 524)". A blank editor.]**

> Before the next video, try **Longest Word in Dictionary through Deleting**. Same muscle — subsequence checks over a word list — but now you return the *longest* word that's a subsequence of `s`, with a tiebreak on smaller lexicographic order.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Per-word scanning re-reads `s` thousands of times → too slow.** Invert the loop: sweep `s` once.
> 2. **A word waits on exactly one character** — its next one. Bucket it there; wake it when that letter appears.
> 3. **Clear the bucket before re-parking** — that's what stops a word matching twice against one position.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "One stream, many waiters → bucket by next char, sweep once."]**
>
> When you see many small patterns matched against one long string, your hand should already be reaching for buckets keyed on the next needed character.
>
> *(GCA reminder — for the interview itself: state the per-word brute force first, name out loud that it re-scans `s` per word, *then* reach for buckets. Google's General Cognitive Ability signal isn't the trick — it's you narrating the path from naive to optimal, and asking "how many words, how long is `s`?" before you commit.)*

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Is Subsequence — follow-up: a STREAM of billions of queries" with a firehose icon.]**

> We beat the "many words at once" version by bucketing. But what if the words never stop coming — a *stream* of billions of queries, one at a time, against a fixed `s`? Buckets don't fit that shape. There's a different weapon: precompute, for each letter, every position it appears in `s`, then binary-search each query's characters. Same problem, flipped constraints — and it's the next one. See you there.
