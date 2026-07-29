# 🎬 Recording Script — Check if Word Can Be Placed In Crossword
**Pattern: Grid / Simulation · LeetCode 2018 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a crossword board, three cells wide. A hand tries to write "cat" starting one cell too early — it spills past a `#` wall and flashes red "ILLEGAL".]**

> Here's a problem that looks like a five-minute warm-up and quietly eats people alive in the interview.
>
> You've got a crossword board. Some cells are blank, some are walls, some already have letters. Can this word fit somewhere? Sounds easy. So you start writing the word at every cell, checking left, checking right, checking up, checking down…
>
> …and thirty minutes later you're drowning in "wait, do I check the cell *before* the start too?" bugs. There's a way to make every one of those boundary bugs *disappear* — and it hinges on one word in the problem you probably skimmed past. Let's find it.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a 3×3 board:]**

```
# . #
. . #
# . #
```

**[VISUAL: legend — `#` = wall, `.` = blank cell, a letter = already filled. Word chip on the side: "cat".]**

> The whole problem in one line: **can I place `word` into some empty strip on this board?**
>
> A cell is a wall `#`, a blank, or an already-placed letter. A *strip* — the crossword calls it a **slot** — is a run of non-wall cells, boxed in by walls or by the edge of the board. To drop the word in, two things must be true: the slot is **exactly** as long as the word, and every cell either is blank or already holds the right letter. Oh — and the word can go in **forwards or backwards**, across or down.
>
> Our word is `"cat"`. Keep your eye on this exact board. We'll solve it by hand before we write a line.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the 3×3 board. A "checks" counter, top-right, at 0. A cursor jumps cell to cell trying to lay "cat" rightward and downward.]**

> Let's do what your brain does first: pick a cell, try to write `"cat"` going right, then going down.
>
> Top-left is a wall — skip. The blank at top-middle: try right → next cell's a wall, too short. Try down → blank, blank… we get three cells. But wait — is this a *legal* start? I have to look at the cell **above** it too. If that were blank, this wouldn't be the real top of the slot.
>
> **[VISUAL: cursor at top-middle blank; an arrow pokes UP to the wall above it; a little "check before" badge lights up. Counter ticks up several times.]**
>
> See what just happened? To place at a cell I'm checking the run *and* the cell just before it *and* the cell just after it. Four directions, two orientations, boundary peeks on both ends — for every single cell.
>
> **[VISUAL: the same "check before / check after" badges flicker across many cells; the checks counter spins fast, turns amber.]**
>
> It's not that it's slow — it's that it's a **minefield**. One forgotten boundary peek and you'll happily jam `"cat"` into the first three cells of a four-cell slot. That's the bug that passes the sample and fails the hidden test.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight one blank cell with "check before?" and "check after?" question marks glowing on both sides. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So here's the pain: the hard part isn't matching letters — it's proving I'm looking at a *whole* slot and not some sub-strip inside a bigger one. That's what those before-and-after peeks are for, and they're where the bugs breed.
>
> **LEARNER:** Right, but I *have* to check the boundaries somehow. The walls are what define a slot. How do I get that for free?
>
> **TEACHER:** Great question — and the answer's hiding in the board itself. Pause the video. Look at where the `#` walls are. **What are they already doing to the rows and columns for you?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: take row 2 — `. . #` — and physically CUT it at the `#`, like scissors. Two pieces fall out: `. .` and the empty tail. Same for every row and column.]**

> **TEACHER:** Here's the flip. Stop trying to *place* the word. Instead, **collect the slots**. And the walls do that job for me — for free.
>
> Think of each row as a sentence and `#` as the delimiter. Split on it. Whatever falls out between two walls *is* a slot — already boxed in, boundaries handled by the cut itself. Do the same down every column.
>
> **[VISUAL: the whole board dissolves into a tidy list of segments: from rows → `[.]`, `[. .]`, `[.]`; from columns → `[.]`, `[. . .]`, (col 2 is all walls → nothing).]**
>
> **LEARNER:** Wait — so I don't check "the cell before" and "the cell after" anymore?
>
> **TEACHER:** That's the whole payoff. When you split on the walls, every segment is *automatically* flanked by a wall or the border. The boundary check isn't skipped — it's **built into the cut**. The fragile part just evaporated.
>
> **[VISUAL: the "check before / check after" badges from beat 3 all fade out with a satisfying pop.]**
>
> Now look at our segments. The only one that's length **3** is that middle column — `. . .`. Three blanks. `"cat"` drops right in. Done.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Split rows & columns on `#` → each segment IS a slot. Match length + letters (both ways)."]**

> Burn this one line in: **don't place the word — split the board on the walls, and every piece you get is a slot with its boundaries already handled.**
>
> After that, a slot either works or it doesn't, and it's two boring checks: same length? and do the letters line up — forward or backward? That's the entire problem.

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the checker for a single slot — this is the heart.

```python
def can_place(seg, word):
    L = len(word)
    if len(seg) != L:              # length must match EXACTLY
        return False
```

> **[VISUAL: add chunk 2, highlight it.]** That length gate is the rule everyone forgets — a word can't half-fill a longer slot. Now the letter match, both directions at once.

```python
    fwd = all(c == ' ' or c == word[i]         for i, c in enumerate(seg))
    bwd = all(c == ' ' or c == word[L - 1 - i] for i, c in enumerate(seg))
    return fwd or bwd              # forwards OR backwards
```

> A cell is fine if it's blank *or* already the letter we want. `fwd` reads the word left-to-right, `bwd` reads it reversed. Either one passing means it fits.
>
> **[VISUAL: add chunk 3 — the sweep.]** Now walk every row, then every column, cutting on `#`.

```python
def placeWordInCrossword(board, word):
    m, n = len(board), len(board[0])

    def scan(get_cell, outer, inner):
        for a in range(outer):
            seg = []
            for b in range(inner):
                ch = get_cell(a, b)
                if ch == '#':
                    if can_place(seg, word):
                        return True
                    seg = []               # slot ended → reset
                else:
                    seg.append(ch)
            if can_place(seg, word):        # flush the last slot in the line
                return True
        return False
```

> **[VISUAL: add chunk 4, highlight the two `scan` calls.]** Run it once across rows, once down columns. The `get_cell` lambda is the only thing that changes — that's how we reuse one loop for both directions.

```python
    if scan(lambda r, c: board[r][c], m, n):   # horizontal slots
        return True
    if scan(lambda c, r: board[r][c], n, m):   # vertical slots (swap indices)
        return True
    return False
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full code; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `if len(seg) != L: return False` — the exact-length rule. This one line replaces all those boundary peeks from the brute force. A slot longer than the word can never take it; a slot shorter obviously can't. Only an exact match survives.
>
> `fwd` and `bwd` — we test both readings because the word can go either direction. `c == ' '` is the "blank accepts anything" clause; `c == word[i]` locks a pre-filled cell to the right letter.
>
> `if ch == '#': ... seg = []` — the wall ends the current slot. We check what we've got, then start fresh. And that `seg = []` reset is what makes each segment *maximal* and self-contained.
>
> **LEARNER:** Hold on — after the inner loop you call `can_place` *again*, outside the loop. Why the repeat?
>
> **TEACHER:** Sharp catch. Because a slot can run right up to the border with no wall after it — like row 1, `. . #`… or a whole row of blanks. If the line ends without a final `#`, nothing inside the loop flushes that last segment. That trailing `can_place` is the flush. Drop it and you'd miss any slot that touches the right edge or the bottom row. It's a classic off-by-one — the last group with no delimiter after it.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×3 board; a trace table filling row by row. Word = "cat".]**

```
# . #
. . #
# . #
```

> Let's run the real code. `L = 3`. Horizontal sweep first.

| Line | Segments cut on `#` | Length check | Result |
|---|---|---|---|
| Row 0 `# . #` | `[.]` | 1 ≠ 3 | skip |
| Row 1 `. . #` | `[. .]` | 2 ≠ 3 | skip |
| Row 2 `# . #` | `[.]` | 1 ≠ 3 | skip |
| Col 0 `# . #` | `[.]` | 1 ≠ 3 | skip |
| **Col 1 `. . .`** | `[. . .]` | **3 = 3** ✓ | all blank → `fwd` true → **return True** |

> The middle column is the first length-3 slot, all blanks, so `"cat"` fits — we return `True` and never even look at column 2. Loop closed, exactly the answer we promised at the top.
>
> **[VISUAL: quick contrast card — same board, word "cats". Every segment flashes "1, 2, 1, 1, 3" — no 4 anywhere → return False.]**
>
> And swap the word for `"cats"`? There's no length-4 slot on the whole board — every segment fails the length gate — so it's `False`. The exact-length rule doing its job.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(m·n·L). Ours: O(m·n). Note: "each cell seen twice — once per direction".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force tries to place at every cell, in two directions, both orientations — that's an O(m·n·L) pile of scans plus fiddly boundary checks. My sweep visits each cell once for rows and once for columns, and the matching work across all segments adds up to the number of cells. So it's O(m·n) time — I dropped the whole L factor."*
>
> That's the sentence that turns "I hacked something together" into "I picked the clean linear pass."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:40`
*(depth + honesty)*

**[VISUAL: the segment buffer `seg` filling and clearing; a thought bubble "copy all the columns first?" gets a red ✗.]**

> Quick space beat — and here honesty scores.
>
> The slick one-liner version of this uses `zip(*board)` to pull the columns out — but that **copies the whole grid**, O(m·n) extra memory. I don't need the copy. I read the columns in place with index arithmetic — that `lambda c, r: board[r][c]` just swaps the indices — and I only ever hold the *one* segment I'm building.
>
> **[VISUAL: highlight that only `seg` grows, up to max(m, n), then resets.]**
>
> A segment is at most `max(m, n)` long, so my auxiliary space is **O(max(m, n))**, not O(m·n). Say it out loud in the interview: *"I avoided materializing the transpose — I scan columns in place and carry just the current run."* Naming *why* you didn't copy is a stronger signal than silently copying.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Word Search (LC 79)". A grid with a word being traced diagonally… no wait, only up/down/left/right.]**

> Before the next video, try **Word Search, LeetCode 79**. Here's the twist that makes it a great contrast: there are **no walls cutting the board into neat slots**, so you *can't* split-and-match. You're forced back into searching from each cell — the very thing we escaped today. Feel where our trick stops working. That boundary is the lesson.
>
> Wrestle with it ten minutes before you peek. The struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Don't place — collect.** Split each row and column on `#`; every piece is a slot.
> 2. **The walls handle your boundaries for free** — the fragile before/after checks vanish.
> 3. **Two checks per slot:** exact length, then letters forward or backward (blank matches anything). And flush the last segment when a line ends with no wall.
>
> The memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Let the walls do the cutting."]**
>
> When a grid problem says "runs bounded by walls," your hand should already be reaching to split on the delimiter — not to search from every cell.
>
> *(GCA reminder — for the interview itself: Google scores *how you think out loud*, not just the final code. Ask the clarifying question early — "the slot has to be **exactly** the word's length, right?" — then narrate the jump from "place at every cell" to "let the walls cut the slots." Saying that leap out loud is the General Cognitive Ability signal the rubric rewards.)*

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Word Search II" — a board with a glowing tree of words overlaid, a red "TLE" ticking in the corner.]**

> Today the walls did our work. But what happens when there are no walls — and worse, when you're searching for **thousands** of words at once, and a plain search from every cell times out hard? There's a data structure built exactly for "match many words against a grid at the same time." That's where we're headed next: Word Search II, and the Trie that makes it fly. See you there.
