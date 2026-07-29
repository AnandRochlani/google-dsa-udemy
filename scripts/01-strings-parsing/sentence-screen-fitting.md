# 🎬 Recording Script — Sentence Screen Fitting
**Pattern: Strings / Simulation · LeetCode 418 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A tidy row-by-row simulation is typed out. A LeetCode "Time Limit Exceeded — 32 / 51" banner slams in red.]**

> The interviewer says: *"You've got a screen, so many rows tall and so many columns wide. Tile this sentence across it, over and over. How many full copies fit?"*
>
> Easy, you think. You write the obvious thing — fill each row word by word, wrap around, count the copies. It's *correct*. It passes the small tests. You run the big one and… Time Limit Exceeded.
>
> Here's the twist: the screen is twenty thousand by twenty thousand, and your code is placing words into hundreds of millions of cells — but the sentence tiling across it is the **same short pattern repeating**. By the end of this video you'll replace that whole simulation with **one pointer** sliding along a string, and the cost will depend on rows only, not rows times columns. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence up top. Below, the words `["a", "bcd", "e"]`, and an empty 3-row × 6-column grid of cells.]**

> The whole problem in one line: **lay the sentence left-to-right, top-to-bottom, repeating it — no word ever split across a line, exactly one space between words — and count how many complete copies fit.**
>
> Tiny example. Sentence is three words: `a`, `bcd`, `e`. Screen is **3 rows, 6 columns wide**. Keep your eyes on this grid — we'll fill it by hand before we write a line of code.
>
> The answer is going to be **two**. Don't chase why yet — just hold that number: two.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the 3×6 grid. A "cells touched" counter, top-right, starting at 0. Words drop into cells one character at a time.]**

> Let's do what your brain does first: fill each row greedily. Place a word if it fits, then a space, then the next word.
>
> **Row 0.** Six columns. Drop `a` — one cell. Space. Drop `bcd` — three cells. That's five used. Next is `e`, needs a space plus one more — no room. Row 0 is `a bcd`.
>
> **[VISUAL: row 0 fills to `a bcd `; counter climbs to 6.]**
>
> **Row 1.** We continue with `e`. Drop `e`, space — that finishes one whole copy of the sentence, tick a counter. Wrap back to `a`, drop it, space. Now `bcd` needs three — no room. Row 1 is `e a`.
>
> **[VISUAL: row 1 fills to `e a `; a "copies: 1" badge flashes.]**
>
> **Row 2.** Continue with `bcd`, space, then `e`, space — that finishes the **second** copy. Row 2 is `bcd e`.
>
> **[VISUAL: row 2 fills to `bcd e `; "copies: 2". The cells-touched counter reads ~18.]**
>
> Two copies. But feel what we did — we touched *every cell*. On a full-size screen that's `rows × cols` — up to four hundred million placements. And every row is us re-deciding the same wrap over and over.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The three filled rows stack up and visibly repeat: `a bcd e` … `a bcd e`. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at what actually happened. The sentence `a bcd e` just streamed across the rows like one long ribbon, wrapping at the edges. The *words* barely matter — it's the same character pattern tiling forever.
>
> **LEARNER:** Okay, but the wrap point is different on every row — row 0 stopped after `bcd`, row 1 after `a`. Doesn't that force me to walk each row?
>
> **TEACHER:** That's the exact right doubt — the wrap *does* shift each row. But here's your think: **what if I glue the sentence into one string and just track a single position in it — how many characters I've laid down total?** Pause the video. If each row adds `cols` characters, what's the one thing that could go wrong at the end of a row?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the words fuse into a ribbon: `a bcd e ` — with a highlighted trailing space. Below it, the same ribbon repeated three times, faded, running off-screen.]**

> **TEACHER:** Here's the move. Forget words — build one string: `s = " ".join(sentence) + " "`. For us that's `a bcd e ` — note the **trailing space** on the end. I'll come back to why that space matters; it's not decoration.
>
> Now picture that ribbon repeated *infinitely*. Laying the sentence on the screen is just cutting this ribbon into pieces `cols` long — one piece per row. Keep a single pointer, `start`: how many ribbon-characters we've validly placed so far.
>
> **[VISUAL: a pointer at position 0. It jumps forward by `cols` = 6, landing on a cell.]**
>
> Each row, jump the pointer forward by `cols`. Then ask **one** question: what character did I land on?
>
> **[VISUAL: two branches. Landed on a space → green check. Landed on a letter → red, an arrow rewinds left to the previous space.]**
>
> If I landed on a **space**, beautiful — the last word ended exactly at the line edge. I just step over that one space. If I landed on a **letter**, I've chopped a word in half — illegal. So I rewind the pointer back to the previous space, which drags that whole partial word down to the next line.
>
> **LEARNER:** Wait — why the trailing space you added at the end? Feels like a throwaway detail.
>
> **TEACHER:** It's the linchpin. Without it, when a copy ends right at the line edge, the last word `e` would sit against a wrap with no separator, and my "did I land on a space?" check would misfire at every copy boundary. The trailing space guarantees *every* word — including the last — is followed by a separator, so the clean-break case always fires correctly. That one space is what makes the whole trick honest.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Flatten to a ribbon (+trailing space). Jump by cols. On a space → step over; on a letter → rewind to the last space."]**

> Burn this one line in: **glue the sentence into a string with a trailing space, jump a pointer forward by `cols` each row, and the character under the pointer tells you everything — space means clean break, letter means back up to the last space.**
>
> That's the entire algorithm. One pointer, one character lookup per row. No grid.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it in pieces. First, the ribbon and the pointer.

```python
def words_typing(sentence, rows, cols):
    s = " ".join(sentence) + " "   # trailing space = every word ends in a separator
    length = len(s)                # one full copy of the sentence, in characters
    start = 0                      # pointer into the INFINITE repetition of s
```

> **[VISUAL: add chunk 2, highlight it.]** Now the per-row loop. Jump forward by `cols`.

```python
    for _ in range(rows):
        start += cols              # tentatively claim a full row's width
```

> **[VISUAL: add chunk 3 — the clean-break branch, highlighted.]** Did we land on a space? Note the `% length` — that's what makes the ribbon *infinite*; we wrap the index around one copy.

```python
        if s[start % length] == " ":
            start += 1             # clean break — step over the separator
```

> **[VISUAL: add chunk 4 — the rewind branch.]** Otherwise we're mid-word. Back up until the character *before* the pointer is a space.

```python
        else:
            while start > 0 and s[(start - 1) % length] != " ":
                start -= 1         # pull the split word onto the next line
```

> **[VISUAL: add chunk 5, highlight the return.]** Each complete copy is exactly `length` characters, so divide.

```python
    return start // length
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `s = " ".join(sentence) + " "` — the flatten, plus the trailing space that keeps copy boundaries clean. We covered that; it's the quiet hero.
>
> `start += cols` — `start` is a running count of validly-placed characters. Adding `cols` says "claim this whole row," and then we fix up the end.
>
> `s[start % length]` — the `% length` is the infinity trick. The real ribbon is finite, but modulo lets one copy stand in for endless repetition. No giant string ever gets built.
>
> **LEARNER:** In that rewind loop — why do you check `s[(start - 1) % length]`, the character *before* the pointer, instead of `s[start]` itself?
>
> **TEACHER:** Because `start` is a *count*, not a landing cell — it points to the next character we'd place. We back up until the thing we just placed is a space, meaning everything up to `start` ends on a completed word. Checking `start - 1` asks "is the last placed char a separator yet?" And the `start > 0` guard just stops us walking off the front — it can't actually trigger here, but it's the safe habit that saves you when a word is longer than a whole line.
>
> `start += 1` in the clean branch — we landed *on* a space, so that space is wasted padding at the line's end; step over it so the next row starts on a real word.
>
> `start // length` — total characters placed, divided by one copy's length, is how many whole copies fit. Integer division drops any partial copy hanging off the end. Exactly what we want.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: the ribbon `a bcd e ` with indices 0–7 labeled; a trace table filling row by row.]**

```
index:  0    1    2    3    4    5    6    7
char:   a   ' '   b    c    d   ' '   e   ' '
length = 8
```

> Run the real code on our example — `rows = 3`, `cols = 6`. Watch the pointer.

| Row | `start += cols` | `s[start % 8]` | Branch | `start` after |
|---|---|---|---|---|
| 0 | `0 + 6 = 6` | `s[6] = 'e'` → letter | rewind: `s[5]=' '` already before it → stop | `6` |
| 1 | `6 + 6 = 12` | `s[12%8]=s[4]='d'` → letter | rewind through `c`,`b` to space at `1` | `10` |
| 2 | `10 + 6 = 16` | `s[16%8]=s[0]='a'` → letter | rewind: `s[7]=' '` already before it → stop | `16` |

> Final `start = 16`. `16 // 8 = ` **two**. And the loop is closed — that's the exact two copies we drew with our hands at the very start. Row 0 swallowed `a bcd`, row 1 `e a`, row 2 `bcd e`. It all lines up.

---

## 10. COMPLEXITY, OUT LOUD — `8:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(rows × cols). Ours: O(rows) after O(C) build. A note: "memory doesn't depend on the screen".]**

> **TEACHER:** Say it the way you'd say it in the room: *"The simulation is O(rows × cols) — it touches every cell, and that times out. Flattening to a ribbon makes it O(rows): one pointer jump per row, and the rewind across all rows is bounded by word lengths. Building the string is O(C), the total characters in the sentence. Space is O(C) for that string."*
>
> That's the sentence that turns a Medium from "I hope this passes" into "here's my complexity, and here's why it's tight."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:20`
*(depth + honesty)*

**[VISUAL: the ribbon `s`; a "shrink it?" thought bubble appears, then a green ✓ next to "already a floor".]**

> Quick, and honesty scores here. Can we drop below `O(C)`? **No — and I can say why.** The ribbon `s` is just the sentence's own characters, once. I have to *see* those characters to know where words end, so that storage isn't overhead — it's the raw material.
>
> But here's the real prize: notice the memory is `O(C)` — the size of the *sentence*, not the *screen*. The brute force implicitly worked over `rows × cols` cells. Ours doesn't grow with rows or cols at all.
>
> Say that out loud: *"Space is O(C) for the flattened sentence, which is a floor, and crucially it's independent of the screen dimensions."* Naming *why* it can't shrink — and *what* it's independent of — is the strong-hire signal.

---

## 12. YOUR TURN (active recall) — `9:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Rearrange Spaces Between Words (LC 1592)". A blank editor.]**

> Before the next video, try **Rearrange Spaces Between Words**. Same muscle: you count characters and spaces, then do the arithmetic of laying words out with the right gaps — no per-cell simulation.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Per-cell simulation is O(rows × cols) → it times out.** The screen is mostly repetition.
> 2. **Flatten the sentence to a ribbon with a trailing space**, slide one pointer, jump by `cols` each row.
> 3. **The character under the pointer decides it** — space means clean break, letter means rewind to the last space.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Don't tile the grid — slide a pointer along the ribbon."]**
>
> When you see a repeating string laid onto a fixed-width screen, your hand should reach for a flattened string and a modular pointer — not a nested loop over cells.
>
> *(GCA reminder — for the interview itself: state the simulation first, say out loud "the screen is just the sentence repeating," and *then* reach for the ribbon. Google's General Cognitive Ability signal isn't the trick — it's you narrating the path from naive to optimal, and asking the one clarifying question up front: "exactly one space, and no word ever split — right?")*

---

## 14. CLIFFHANGER — `11:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Text Justification" — a paragraph with spaces stretching unevenly between words.]**

> Here every line had exactly one space between words. But what if the interviewer says every line must be **exactly** `maxWidth` wide, fully justified — so you have to *stretch* the spaces, and the leftover spaces go to the leftmost gaps? Same "pack words onto lines" instinct, a whole new pile of edge cases. That's the next one: Text Justification — Google's favorite "can you write clean code under pressure" string problem. See you there.
