# 🎬 Recording Script — Swap Adjacent in LR String
**Pattern: Two Pointers / Invariants · LeetCode 777 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. A tidy BFS solution is typed out — a queue, a `seen` set, generating neighbor strings. A red "Time Limit Exceeded — 84 / 96" banner slams down.]**

> The interviewer writes two strings on the board — a jumble of L's, R's, and X's — and asks: *"Can you slide one into the other, given these two swap rules?"*
>
> You do the obvious thing. Every swap is a move, so you search: try all the swaps, see if you can reach the target. It's *correct*. It passes the small tests. Then the big one — Time Limit Exceeded.
>
> Here's the twist. You never needed to search at all. This whole problem collapses into **one linear scan** — once you see the one thing these swaps can *never* change. Let's find it.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, two short strings stacked:]**

```
start:  X L
end:    L X
```

> The whole problem in one line: **you have two moves — "XL" becomes "LX", and "RX" becomes "XR" — and you want to know if you can turn `start` into `end`.**
>
> Look at what those two moves actually *do*. `"XL" → "LX"` — the L hops one step **left**. `"RX" → "XR"` — the R hops one step **right**. That's it. An L drifts left, an R drifts right, and each one is just swapping places with an X.
>
> Tiny example: `start = "XL"`, `end = "LX"`. The L slides left past the X. Reachable — this one's a `true`. Hold onto that picture.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: a small string `"RXX"`. A tree of neighbor strings branches out below it — `"XRX"`, then `"XXR"` — with a "strings generated" counter climbing.]**

> Let's do what your brain does first: treat it as a search. From `start`, apply every legal swap to get new strings, then swap those, and so on — until you either hit `end` or run out.
>
> Start with `"RXX"`. The R can slide right: `"XRX"`. From there, slide again: `"XXR"`. Three strings from one tiny input.
>
> **[VISUAL: counter ticks 1 → 3. Now the input grows to length 8 with four X's; the tree explodes off-screen, counter spinning past thousands.]**
>
> Now make it realistic — a longer string with a handful of X's. Each L and each R can sit in *many* positions among those X's. The number of reachable strings blows up **exponentially**.
>
> **[VISUAL: counter morphs into "≈ exponential" glowing red.]**
>
> On a length-ten-thousand input, you're generating an ocean of strings just to answer one yes-or-no question. That's your TLE.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the exploding tree. A 4-second "🤔 your turn" timer. The two moves `XL→LX` and `RX→XR` pinned in the corner.]**

> **TEACHER:** So where's the waste? We're building millions of *intermediate* strings, but we only care about one bit of information: reachable or not. There has to be a property we can check *directly*.
>
> **LEARNER:** But the L's and R's move all over the place — how can anything stay fixed while they shuffle around?
>
> **TEACHER:** Beautiful question — because *one* thing is nailed down, and it's the key to everything. Pause the video. Look hard at the two moves and ask: **what can an L or an R swap with? And can an L and an R ever trade places?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a string `R X L`. The R tries to move onto the L — the arrow flashes red and snaps: "no such move." Then the X's fade to grey, leaving just `R … L`.]**

> **TEACHER:** Here it is. Every move swaps a letter with an **X**. There is *no* rule that swaps an L with an R. So an L and an R can **never pass through each other.**
>
> That means the **order** of the real letters — reading left to right, ignoring the X's — can *never* change. If `start` reads `R, L, R` after you delete the X's, then `end` had better read `R, L, R` too. Different order? Impossible, full stop.
>
> **[VISUAL: think of the X's as empty seats and the letters as people who can slide between empty seats — but nobody can climb over another person.]**
>
> **LEARNER:** Okay, so same order is *necessary*. But two strings could have the same L-R order and still be unreachable, right? The letters have to actually be able to *get* where they're going.
>
> **TEACHER:** Exactly — and that's the second half. An L only ever moves **left**. So its position in `start` must be at the same spot or **further right** than in `end` — it needs room to slide left into place. An R only ever moves **right**, so its `start` position must be at the same spot or **further left** than in `end`.
>
> **[VISUAL: an L at index 5 in start, index 2 in end — a leftward arrow, green "5 ≥ 2 ✓". An R at index 1 in start, index 4 in end — rightward arrow, green "1 ≤ 4 ✓".]**
>
> Same order, plus each letter only moved its legal direction. That's the entire test.

---

## 6. THE KEY MOVE (signaling) — `4:40`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "Strip the X's → same L/R order · L only moves left (i ≥ j) · R only moves right (i ≤ j)."]**

> Burn this in: **delete the X's — the L/R sequences must match — and then each L's start index must be ≥ its end index, each R's start index ≤ its end index.**
>
> L for **L**eft, so it needs to be to the right and slide back. R for **R**ight, so it needs to be to the left and slide forward. Don't simulate the motion — just check the endpoints.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Two pointers, `i` on `start` and `j` on `end`. First, a length guard and the loop skeleton.

```python
def can_transform(start, end):
    if len(start) != len(end):
        return False
    n = len(start)
    i = j = 0
    while i < n or j < n:
```

> **[VISUAL: add chunk 2, highlight it.]** Inside the loop, jump both pointers forward to the next *real* letter — skip the X's on each side independently.

```python
        while i < n and start[i] == "X":
            i += 1
        while j < n and end[j] == "X":
            j += 1
```

> **[VISUAL: add chunk 3.]** Now handle the "did we run out?" cases. If both hit the end, every letter matched — `true`. If only one ran out, the sequences were different lengths of real letters — `false`. And if the letters themselves don't match, the order's wrong.

```python
        if i == n and j == n:
            return True
        if i == n or j == n:
            return False
        if start[i] != end[j]:
            return False
```

> **[VISUAL: add chunk 4, highlight the two direction checks.]** The heart of it — the direction rule. An L that would need to move right is illegal; an R that would need to move left is illegal.

```python
        if start[i] == "L" and i < j:      # L can only go LEFT → needs i >= j
            return False
        if start[i] == "R" and i > j:      # R can only go RIGHT → needs i <= j
            return False
        i += 1
        j += 1
    return True
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> The two inner `while` loops skip X's — because X's are just empty seats; only the real letters and their order matter.
>
> `if i == n and j == n: return True` — both sides emptied out at the same time, every letter lined up and passed. `if i == n or j == n` — one side had a leftover letter, so the L/R sequences differ. `if start[i] != end[j]` — same idea, caught mid-stream: an L facing an R means the order's broken.
>
> **LEARNER:** Wait — for the L you wrote `i < j` returns false. Why `<` and not `<=`? Isn't landing on the same spot a problem too?
>
> **TEACHER:** No — the same spot is totally fine. An L is *allowed* to stay put or move left, so `i == j` is legal and `i > j` is legal. The *only* illegal case is `i < j` — that would mean the L has to move **right**, which it can't. So we reject exactly `i < j`, and the mirror image for R is `i > j`. The direction of the inequality *is* the direction the letter is forbidden to travel.
>
> `i += 1; j += 1` — both letters checked out, step past them to the next pair.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: `start = "RXXLRXRXL"`, `end = "XRLXXRRLX"`, indices labeled. A trace table fills row by row; a leftover "false demo" card waits at the side.]**

```
start:  R X X L R X R X L
index:  0 1 2 3 4 5 6 7 8
end:    X R L X X R R L X
```

> Strip the X's first: `start` is `R L R R L`, `end` is `R L R R L`. Same order — good. Now the pointer walk checks each pair's positions.

| Pair | letter | `i` (start) | `j` (end) | rule | check |
|---|---|---|---|---|---|
| 1 | R | 0 | 1 | R needs `i ≤ j` | 0 ≤ 1 ✓ |
| 2 | L | 3 | 2 | L needs `i ≥ j` | 3 ≥ 2 ✓ |
| 3 | R | 4 | 5 | R needs `i ≤ j` | 4 ≤ 5 ✓ |
| 4 | R | 6 | 6 | R needs `i ≤ j` | 6 ≤ 6 ✓ |
| 5 | L | 8 | 7 | L needs `i ≥ j` | 8 ≥ 7 ✓ |

> Every pair passes → **`true`**. Loop closed.
>
> **[VISUAL: the "false demo" card flips up: `start = "LX"`, `end = "XL"`.]** And the failure case, so you feel it: `start = "LX"`, `end = "XL"`. Same letter, but the L sits at index `0` in start and index `1` in end — it'd have to move *right*. Check `L and i < j` → `0 < 1` → **`false`**. An L trying to go right gets caught instantly.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(2^n) time & space. Ours: O(n) time, O(1) space. Note: "each pointer crosses once."]**

> **TEACHER:** Say it the way you'd say it in the room: *"The BFS is exponential — the reachable set blows up with the number of X-gaps, so it times out. My two-pointer version scans each string once, so it's O(n) time. And I carry nothing but two integer indices, so it's O(1) space."*
>
> That's the sentence that turns a stall into a strong hire.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the two pointers `i` and `j` alone on screen; a "can we do better?" bubble gets a calm green ✓ "already O(1)".]**

> Quick one — and honesty scores here.
>
> Can we shrink the space? **No, and I can say exactly why: there's nothing being stored.** No `seen` set, no copy of either string, no array that grows with `n` — just two indices reading in place. O(1) is the floor, and we're already on it.
>
> Say that out loud: *"Space is O(1) — two pointers and nothing else. There's no structure to optimize away."* Naming the absence of a trick is a real signal, not a cop-out.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Backspace String Compare (LC 844)". A blank editor.]**

> Before the next video, try **Backspace String Compare**. Same muscle: walk two strings with pointers, *skip* the characters that don't count — backspaces this time instead of X's — and compare what's actually left, ideally in O(1) space.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Don't simulate a restricted move — find what it can't change.** Here, L's and R's never cross, so their order is fixed.
> 2. **Strip the filler, then check endpoints.** Same L/R sequence, and each letter only moved its legal way.
> 3. **The inequality direction is the movement direction.** L needs `i ≥ j` (it goes left), R needs `i ≤ j` (it goes right).
>
> The memory peg:
>
> **[VISUAL: big box → "L slides Left (i ≥ j) · R slides Right (i ≤ j) · order never breaks."]**
>
> When a problem lets pieces move only *one way* and *never past each other*, don't search the moves — check the invariant with two pointers.
>
> *(GCA reminder — for the interview itself: state the brute-force search, say out loud "these swaps can't reorder the letters," then derive the two inequalities before you touch code. Google's General Cognitive Ability signal isn't the final trick — it's you narrating the jump from "search everything" to "check the invariant." Ask the clarifying question — "L only left, R only right, and they never cross?" — first.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Backspace String Compare" — two strings with `#` characters eating letters backward.]**

> We got to skip the X's because they were just inert filler sitting still. But what happens when the characters you skip **delete the letters behind them** — when the filler reaches *backward* and erases what you already passed? Now the two-pointer scan has to walk from the *end*, and the order you read in suddenly matters. That's the next one. See you there.
