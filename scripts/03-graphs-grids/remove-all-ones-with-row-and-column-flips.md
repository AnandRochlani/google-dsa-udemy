# 🎬 Recording Script — Remove All Ones With Row and Column Flips
**Pattern: Invariant / XOR insight · LeetCode 2128 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a binary grid on screen. A hand-cursor frantically clicking rows and columns to flip them — the grid keeps lighting up new 1s as fast as it clears old ones. A timer in the corner ticks past 40 seconds.]**

> Google onsite. Interviewer draws a grid of zeros and ones and says: *"You can flip any whole row or any whole column, as many times as you want. Can you make it all zeros? Yes or no."*
>
> So you start flipping. Clear a row — but that breaks a column. Fix the column — now a row's dirty again. You're playing whack-a-mole with a matrix, the clock's running, and you can feel the panic.
>
> Here's the twist that ends the panic: **you never have to flip anything.** By the end of this video you'll answer this in one clean pass over the grid — no simulation, no search — because there's a hidden rule the flips can't break. Let's find it.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence up top. Below it a 3×3 grid:]**

```
0 1 0
1 0 1
0 1 0
```

> The whole problem in one line: **flip entire rows or entire columns, any number of times, and decide — can the grid become all zeros?**
>
> Here's our tiny example — nine cells. A "flip" means every `0` in that row or column becomes a `1`, and every `1` becomes a `0`. The whole line toggles at once.
>
> Hold onto this grid. The answer here is **yes** — and I'll show you the *one* flip that clears it, then the rule that let us know without trying.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the 3×3 grid. A "flips tried" counter top-right at 0. Arrows toggle a row, then a column, cells flickering back and forth.]**

> Let's do what your brain does first: just start flipping and hope.
>
> Flip row 1 — the middle row `1 0 1` becomes `0 1 0`. Counter ticks. But look — column 1 is now `1 1 1` all the way down. We made it worse.
>
> **[VISUAL: row 1 flips; column 1 lights up solid, glowing red.]**
>
> Okay, undo — flip column 1. Now the middle's dirty again somewhere else. Every fix spawns a new mess.
>
> **[VISUAL: counter climbs; the grid oscillates; a ghosted "2^(m+n) combinations" label fades in behind it.]**
>
> And how many flip combinations even *are* there? Each row and each column is either flipped or not — that's `2^(rows + columns)`. On a grid with a couple hundred rows and columns, that's more combinations than atoms in your coffee. You cannot search this. There has to be structure.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze the oscillating grid. Spotlight one cell. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the structure hiding? Here's a nudge. Watch **one cell.** What actually decides its final value? Only two things touch it: whether we flipped *its row*, and whether we flipped *its column*. Nothing else.
>
> **LEARNER:** Wait — but the *order* I flip them in matters, right? And flipping the same row five times versus once?
>
> **TEACHER:** Great instinct to check — and that's *exactly* the thing to pause on. Pause the video. Ask yourself: if I flip a row, then a column, is that any different from column-then-row? And what does flipping the same row **twice** do?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a single cell blown up big. Two toggle switches feed into it, labeled "row flip" and "col flip". Its value = starting bit ⊕ row switch ⊕ col switch.]**

> **TEACHER:** Here's the unlock, and it's two facts.
>
> **Fact one: a flip is its own undo.** Flip a row twice, you're exactly back where you started. So flipping a row *five* times is the same as flipping it *once*; flipping it *four* times is the same as *not at all*. The only thing that matters for each row and each column is **odd or even** — one single bit. Did I flip it, yes or no.
>
> **Fact two: order doesn't matter.** Look at this one cell. Its final value is just its **starting bit, XOR the row switch, XOR the column switch.** XOR doesn't care what order you apply it. Row-then-column, column-then-row — identical.
>
> **[VISUAL: the switches flip in both orders; the output bit is the same both times. A big "⊕ = XOR, order-free, self-cancelling" banner.]**
>
> **LEARNER:** So this whole "any number of times, any order" thing… collapses to just: which rows get a flip, which columns get a flip?
>
> **TEACHER:** Exactly. The scary search space was an illusion. Now here's the killer move — **look at row 0 and let it make our decision for us.**
>
> **[VISUAL: row 0 highlighted. Below each of its 1s, a column-flip switch clicks ON automatically.]**
>
> To zero out row 0, the column flips are **forced**: flip exactly the columns where row 0 has a 1. No choice about it. But columns are shared by *every* row — so that decision is now locked in for the whole grid. The question becomes: under those forced column flips, does every *other* row also go to zero?

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Clearable ⟺ every row EQUALS row 0, or is its EXACT COMPLEMENT."]**

> Here's the whole lesson in one line: **the grid is clearable if and only if every row is either identical to row 0, or the exact bit-for-bit opposite of row 0.**
>
> Why? After the forced column flips clear row 0, a row that was **identical** to row 0 also became all zeros — done. A row that was the **exact complement** became all *ones* — so flip that whole row once, and it's zero too. But a row that **mixes** — matches row 0 in some columns, opposes it in others — is stuck. One row flip toggles the *whole* line together; it can't fix the matches and the mismatches at the same time.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, grab row 0 as our reference — everything gets compared to it.

```python
def remove_ones(grid):
    m, n = len(grid), len(grid[0])
    first = grid[0]
```

> **[VISUAL: add chunk 2, highlight it.]** Now walk every *other* row and ask the two questions: is it the same as row 0 everywhere, or the opposite everywhere?

```python
    for i in range(1, m):
        row = grid[i]
        same    = all(row[j] == first[j] for j in range(n))
        flipped = all(row[j] != first[j] for j in range(n))
```

> **[VISUAL: add chunk 3, highlight the return-False line.]** If a row is *neither* — it's a mix — we're done, it's impossible.

```python
        if not (same or flipped):
            return False
    return True
```

> That's the entire algorithm. No flipping, no grid mutation. Just "equal or opposite?" down the rows.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:35`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk the *why*.
>
> `first = grid[0]` — row 0 is our anchor. We decided the column flips by looking at it, so every other row is judged against it.
>
> `same = all(row[j] == first[j] …)` — true only if this row matches row 0 in **every** column. That's the "already zero after column flips" case.
>
> `flipped = all(row[j] != first[j] …)` — true only if it differs in **every** column: the exact complement. That's the "flip the whole row once" case.
>
> **LEARNER:** Hold on — do we ever actually check row 0 against itself? We start the loop at `i = 1`.
>
> **TEACHER:** Sharp catch, and no — we don't need to. Row 0 is *defined* as clearable; the forced column flips zero it out by construction. So we skip it and only test rows 1 through m−1 against it. Starting at 1 isn't a bug, it's the point.
>
> `if not (same or flipped): return False` — the instant one row is a mix, the whole grid is impossible, so we bail early. If every row passes, we fall through to `return True`.

---

## 9. DRY-RUN THE CODE — `7:35`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×3 grid with row 0 boxed as `first`; a trace table filling row by row.]**

```
0 1 0   ← first
1 0 1
0 1 0
```

> Run the real code. `first = [0,1,0]`.

| i | row | vs `[0,1,0]` | same? | flipped? | verdict |
|---|---|---|---|---|---|
| 1 | `[1,0,1]` | differs in **every** column | no | **yes** | complement — OK |
| 2 | `[0,1,0]` | matches in **every** column | **yes** | no | identical — OK |

> Both rows pass — return **True**. And remember the promise from the top: flip **column 1** alone and this grid goes all zeros. The rule said yes without us flipping a thing.
>
> **[VISUAL: quick cut to the counter-example.]**

```
1 1 0   ← first
0 0 0
0 0 0
```

> Now `first = [1,1,0]`. Row 1 is `[0,0,0]`: it matches row 0 in the last column — `0 == 0` — but opposes it in the first two. Not all-same, not all-different. A **mix**. `return False`. No amount of flipping saves it.

---

## 10. COMPLEXITY, OUT LOUD — `8:30`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(2^(m+n) · m·n). Ours: O(m·n). A note: "every cell read once".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force enumerates all `2^(m+n)` flip combinations — hopeless. My solution reads each row once and compares it to row 0 cell by cell, so it's `O(m·n)` time — I touch every cell a constant number of times. And space is `O(1)`: I only hold row 0 as a reference and two booleans."*
>
> That jump — from exponential to a single linear pass — is the sentence that turns this Medium into a strong-hire moment.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:05`
*(depth + honesty)*

**[VISUAL: the code; a thought bubble "store the complemented row?" appears, then gets a red ✗.]**

> Quick space beat — and honesty scores here.
>
> Can I do better than my extra memory? **There's nothing to cut — and I can say why.** I never build the flipped row, never store a mask, never copy the grid. I check "is this the complement?" on the fly, cell by cell, as `row[j] != first[j]`. The only extra memory is two booleans per row. That's already `O(1)`.
>
> Say it out loud in the interview: *"Auxiliary space is O(1) — I compare each row against row 0 in place, so there's genuinely nothing to optimize away."* Naming that you never allocated anything is a stronger signal than inventing a trick you don't need.

---

## 12. YOUR TURN (active recall) — `9:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Flip Columns For Maximum Number of Equal Rows (LC 1072)". A blank editor.]**

> Before the next video, try **Flip Columns For Maximum Number of Equal Rows.** Same DNA: rows are interesting only up to "equal or exact complement." But instead of a yes/no, you **count** — how many rows can you make all-equal by flipping columns?
>
> Don't peek. Wrestle with it for ten minutes. That's what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:10`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **"Any number of flips, any order" = XOR.** So only parity matters — one bit per row, one per column — and order is irrelevant. Don't simulate.
> 2. **Let row 0 force the column flips.** Then every other row must land at zero on its own.
> 3. **The invariant:** every row equals row 0 or is its exact complement — else it's impossible.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Flip = XOR ⇒ only parity matters ⇒ every row equals row 0 or its opposite."]**
>
> When a problem says *"toggle any number of times, any order,"* your hand should reach for **XOR and an invariant**, not a search.
>
> *(GCA reminder — for the interview itself: don't jump to the answer. Say the brute force out loud, name the `2^(m+n)` blowup, then narrate the two facts — flips are self-cancelling, flips commute — that collapse it. Google's General Cognitive Ability score is you walking the path from naive to invariant. Ask the clarifying question — "so only odd-vs-even flips matter, right?" — before you write a line.)*

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Transform to Chessboard" — a binary grid with rows and columns being *swapped*, not flipped.]**

> We got a clean yes/no because flips are pure XOR — parity, no order. But what if you can also **swap** whole rows and columns around, and the goal is a perfect checkerboard? Now it's flips *and* permutations tangled together, and the invariant gets sneakier. That's the next one: Transform to Chessboard. Same "find the property the operations can't change" instinct — turned up a notch. See you there.
