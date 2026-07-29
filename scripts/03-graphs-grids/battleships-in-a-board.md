# 🎬 Recording Script — Battleships in a Board
**Pattern: Grid counting (O(1)-space trick) · LeetCode 419 · Medium · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Number of Islands (flood-fill) — but watch what the extra structure lets us throw away.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean Number-of-Islands-style flood-fill is typed out with a `visited` grid. The interviewer's follow-up slides in as a red sticky note: "One pass. O(1) space. Don't touch the board."]**

> You get a grid problem. You nail it — flood-fill, count the components, done. The interviewer nods and says: *"Nice. Now do it in a single pass, constant extra space, and without modifying the board."*
>
> And your whole solution just… falls over. The visited set is O(m·n). Mutating the board is off the table. You're stuck.
>
> Here's the thing: there's a five-line answer that needs **no traversal, no visited set, and one integer of memory.** By the end of this video you'll see the one property of this board that makes it possible — and why you'll kick yourself for not spotting it. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence up top. Below, a 3×4 grid of tiles:]**

```
X . . X
. . . X
. . . X
```

> The whole problem in one line: **count the battleships on the board.** `X` is a piece of a ship, `.` is water.
>
> Two rules make ships special. One — every ship is a **straight line**: a horizontal row of `X`s or a vertical column, never an L or a blob. Two — **no two ships touch.** There's always at least one `.` between them.
>
> Look at our tiny grid. How many ships? A single `X` up top-left, and a vertical three-cell ship down the right edge. So the answer is **two.** Keep this exact grid in your eye — we'll solve it by hand before any code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the overkill)*

**[VISUAL: the 3×4 grid. A "flood-fill" wave animates out of each unvisited `X`, painting the component, dragging a `visited` overlay grid alongside.]**

> Let's do what your brain does first. This *is* Number of Islands, right? Find a group of connected `X`s, flood-fill the whole blob, mark everything visited, add one to the count. Then find the next unvisited `X` and repeat.
>
> Start at top-left `X`. Flood-fill — it's alone, one cell. Count = 1. Mark it visited.
>
> **[VISUAL: the lone top-left cell glows, gets a checkmark overlay.]**
>
> Now scan on… the `X` at top-right. Flood-fill down — it connects to the two below it. Paint all three, mark them visited. Count = 2.
>
> **[VISUAL: the right column lights up as one blob, three checkmarks drop onto a separate `visited` grid.]**
>
> Answer's right — two. But look at what it *cost*: a whole second grid just to remember what we've seen.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the `visited` overlay grid pulsing red. The red sticky note from the cold open returns: "O(1) space. Don't touch the board." A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the squeeze. To avoid double-counting a ship, flood-fill has to *remember* which cells it already swallowed — that's the `visited` grid, O(m·n) memory. The only way to drop it is to mutate the board, flipping `X` to `.` as you go. But the follow-up forbids *both*.
>
> **LEARNER:** But don't we *have* to remember something? If I count every `X`, a three-cell ship counts as three. How do I count each ship exactly once without tracking what I've seen?
>
> **TEACHER:** That is exactly the right question. And the answer hides in a rule we haven't used yet. Pause the video. **What's special about the shape of a ship that a random island blob doesn't have?** Think about it before I say it.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a single vertical ship and a single horizontal ship, side by side. On each, the FIRST cell — topmost / leftmost — gets a gold star badge.]**

> **TEACHER:** Here's the move. Instead of counting *every* cell of a ship, count it at **one special cell** — a spot that shows up exactly once per ship. For a straight line, the natural pick is its **top-left end.**
>
> Think of it like roll call. Each ship has one captain, and the captain is always the cell at the front — the top of a vertical ship, the left end of a horizontal one. Count the captains, you've counted the ships.
>
> **[VISUAL: gold star sits on the top cell of the vertical ship; on the left cell of the horizontal ship. The other cells stay plain.]**
>
> So how do I *recognize* the captain using only what's around a cell? Simple: the top-left end is the one `X` with **no `X` directly above it** and **no `X` directly to its left.** If something were above or to the left, the ship would keep going that way — so this wouldn't be the front.
>
> **LEARNER:** Wait — with two ships near each other, couldn't an `X` from a *different* ship sit right above mine and fool the test? Then I'd skip a real captain.
>
> **TEACHER:** Beautiful worry — and here's why it can't happen. Rule two: **no two ships ever touch.** There's always a `.` between them. So the cell directly above or left of my captain, if it's not part of *my* ship, is guaranteed to be water — never another ship's `X`. The separation rule makes the local test airtight.
>
> **[VISUAL: two ships with a `.` gap; try to draw a rogue `X` bridging them — it snaps red, "ships can't touch".]**

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Count a cell only if it's an X with no X above and no X to the left."]**

> Burn this one line in: **count a cell only when it's an `X`, with no `X` above it and no `X` to its left.** That's the top-left end. That's the captain. That's the whole trick.
>
> No traversal. No visited set. No touching the board. Just a local two-neighbor check as you scan.

---

## 7. CODE IT — LIVE & CHUNKED — `5:05`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the guard and the setup — dimensions and one counter.

```python
def count_battleships(board):
    if not board or not board[0]:
        return 0
    rows, cols = len(board), len(board[0])
    ships = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Scan every cell. Skip water immediately.

```python
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != 'X':
                continue
```

> **[VISUAL: add chunk 3, highlight the two neighbor checks.]** Now the captain test. If there's an `X` above, this isn't the top end — skip. If there's an `X` to the left, not the left end — skip. Notice the edge guards: `r > 0` and `c > 0` so we don't read off the board.

```python
            if r > 0 and board[r - 1][c] == 'X':   # X above → not the top
                continue
            if c > 0 and board[r][c - 1] == 'X':   # X to left → not the front
                continue
```

> **[VISUAL: add chunk 4, highlight `ships += 1`.]** If we survived both checks, no `X` above, no `X` left — it's a captain. Count it.

```python
            ships += 1
    return ships
```

> That's it. Five real lines of logic. No recursion, no queue, no second grid.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:35`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `if board[r][c] != 'X': continue` — water can't be a ship's captain, so don't even bother.
>
> `if r > 0 and board[r-1][c] == 'X'` — the `r > 0` is the edge guard: row zero has nothing above it, so it *auto-passes* this test. Otherwise, an `X` above means the ship extends upward — I'm not the top.
>
> **LEARNER:** Why `continue` on a found neighbor instead of counting? Feels backwards.
>
> **TEACHER:** Because I want to count the captain *exactly once* — so I count only when I *fail* to find a ship-cell above or left. Every non-captain cell of a ship has an `X` right above it or right beside it, so it hits a `continue` and gets suppressed. Only the front survives to `ships += 1`.
>
> `ships += 1` — reached only by the one top-left cell of each ship. And because ships never touch, no neighbor `X` ever belongs to a *different* ship — so the test can't merge two ships or split one. One captain, one count.

---

## 9. DRY-RUN THE CODE — `7:35`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×4 grid; a trace table fills row by row. The counted cells get a gold star.]**

```
X . . X
. . . X
. . . X
```

> Let's run the actual code on our grid and watch the count.

| Cell | Value | `X` above? | `X` left? | Counted? | ships |
|---|---|---|---|---|---|
| (0,0) | `X` | edge → no | edge → no | ✅ captain | 1 |
| (0,3) | `X` | edge → no | `.` → no | ✅ captain | 2 |
| (1,3) | `X` | (0,3) is `X` → yes | — | ❌ skip | 2 |
| (2,3) | `X` | (1,3) is `X` → yes | — | ❌ skip | 2 |

> Every other cell is `.` and gets skipped on line one. The lone top-left `X` is a captain. The vertical ship counts once, at its *top* cell — its two lower cells each see an `X` right above and bail. Final count: **two.** Loop closed — exactly the answer we promised at the start.

---

## 10. COMPLEXITY, OUT LOUD — `8:20`
*(transfer to interview)*

**[VISUAL: two rows — Flood-fill: Time O(m·n), Space O(m·n). Ours: Time O(m·n), Space O(1). A note: "visit each cell once, read 2 neighbors".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Time is O(m·n) either way — I have to look at every cell. But the flood-fill needs O(m·n) space for a visited grid or it mutates the board. My scan keeps one integer and reads two neighbors per cell, so it's O(1) extra space and it never touches the input."*
>
> Same time, but the space goes from O(m·n) down to O(1). That's the sentence that turns the follow-up from a stumble into a strong-hire moment.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:55`
*(depth + honesty)*

**[VISUAL: the counter `ships` sitting alone; a "shrink it more?" thought bubble appears, then gets a green ✓ "already O(1)".]**

> Quick and honest: can we do better than O(1) space? **No — and I can say exactly why.** We're already down to a single integer counter and two local neighbor reads. Nothing scales with `m` or `n`. And time can't beat O(m·n) either — you *must* look at every cell at least once, or you could miss a captain hiding in the corner.
>
> Say that out loud in the interview: *"Space is O(1) and that's optimal — one counter, no visited set, no board mutation — and O(m·n) time is a hard floor because every cell has to be checked."* Naming *why* it can't shrink is a stronger signal than staying quiet.

---

## 12. YOUR TURN (active recall) — `9:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Islands (LC 200)". A blank editor.]**

> Before the next video, go do **Number of Islands** — the parent problem. Here's the twist that makes it a great contrast: islands can be *any* blobby shape and there's *no* "can't touch" rule. So the captain trick **breaks** — you genuinely need the flood-fill and the visited set back.
>
> Wrestle with *why* the local test fails there for ten minutes before you peek. Feeling where the trick stops working is what locks in *when* it works.

---

## 13. LOCK IT IN — `9:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Flood-fill works but costs O(m·n) space** — a visited set, or you mutate the board. The follow-up forbids both.
> 2. **Count each ship at one captain cell** — its top-left end: an `X` with no `X` above and none to the left.
> 3. **The "ships can't touch" rule** is what makes the local test airtight — no neighbor `X` ever belongs to another ship.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Count the captains: X with no X above, no X left."]**
>
> When a grid's pieces have a rigid shape *and* a separation guarantee, your hand should reach for a local corner-count — not a traversal.
>
> *(GCA reminder — for the interview itself: state the flood-fill first, name out loud why it fails the follow-up, then ask "are ships guaranteed non-adjacent?" and reach for the captain trick. Google's General Cognitive Ability signal isn't the five lines — it's you narrating the path from the obvious solution to the one that clears every constraint.)*

---

## 14. CLIFFHANGER — `10:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Number of Islands" — a grid with a jagged, L-shaped blob that clearly has no single "top-left end".]**

> Our whole trick leaned on two gifts: straight ships, and no touching. But what happens when the shapes go *wild* — an island bends into an L, wraps around, and two blobs can sit one cell apart? Suddenly there's no captain to count, and the local test lies to you. That's the next one: Number of Islands — where we finally *earn* the flood-fill we threw away today. See you there.
