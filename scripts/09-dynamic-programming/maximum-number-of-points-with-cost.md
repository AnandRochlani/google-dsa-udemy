# 🎬 Recording Script — Maximum Number of Points with Cost

**Pattern: Row DP + directional prefix-max sweeps · LeetCode 1937 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** any row-by-row grid DP (Minimum Falling Path Sum). The DP part is easy here — this lesson is about making the *transition* fast. That's the whole theme of this section.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor with a short, clean, obviously-correct DP typed out. Green checkmarks on examples 1 and 2. Then a red banner slams in: "Time Limit Exceeded — 155 / 157".]**

> Here's the cruelest way to fail a Google interview: **with a correct answer.**
>
> This problem gives you a grid. Pick one cell from every row, add them up, and pay a penalty for every sideways step between rows. You write the textbook dynamic program. It's right. It passes the examples. You submit — Time Limit Exceeded on test 155.
>
> Nothing about your DP is wrong. Your *states* are perfect. It's the **transition** that's too slow — and one move takes it from a hundred million operations per row down to three quick passes. That move is a trick with the absolute-value sign, and once you see it you'll see it everywhere.
>
> This is the first video of the DP section, and it's the section's whole thesis: **writing the DP is the easy half. Making the transition fast is the interview.** Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence at the top. Below it, a 3×3 grid of tiles:]**

```
1  2  3
1  5  1
3  1  1
```

> One line: **pick exactly one cell from every row, add up what you picked — and for each pair of neighbouring rows, subtract how far you moved sideways.**
>
> If you pick column 1 in a row and column 0 in the next, that's one column of travel, so you pay one point. Move three columns, pay three. The penalty is `|c1 − c2|` — plain distance between the two column indexes.
>
> Here's our tiny example — nine cells, three rows. Keep your eye on this exact grid; we'll solve it by hand twice before we write any code.
>
> **[VISUAL: highlight the path 2 (row 0, col 1) → 5 (row 1, col 1) → 3 (row 2, col 0); penalty arrows appear: |1−1| = 0, then |1−0| = 1.]**
>
> The answer is **9**. Two plus five plus three is ten, minus one point of travel between the last two rows. Hold onto that nine.
>
> And before you write anything in a real room, ask the question that proves you read the spec: *"The penalty is only between **adjacent** rows, right — nothing charged between row 0 and row 2 directly?"* Cheap to ask, and it locks the DP structure before you commit to a line.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the 3×3 grid. Row 0 gets labels `[1, 2, 3]`. A "comparisons" counter, top-right, at 0. Arrows fan out from every cell in row 1 back to every cell in row 0.]**

> Let's do what your brain does first, because it's genuinely good. Define `dp[r][c]` — **the best total I can have if my pick in row `r` is column `c`.** Row 0 is free, no travel yet, so `dp[0]` is just the row itself: one, two, three.
>
> Now row 1. To land on a cell, I came from *somewhere* in row 0 and paid the distance. So `dp[1][c] = points[1][c] + the best of (dp[0][j] − |c − j|)` over **every** column `j`.
>
> **[VISUAL: three arrows from row 0 into row 1 col 0, each labelled with its arithmetic; counter ticks 1, 2, 3.]**
>
> Let's grind it. Landing on **column 0**: from column 0, one with no travel — one. From column 1, two minus one — one. From column 2, three minus two — one. Best is one, so `dp[1][0] = 1 + 1 = 2`.
>
> **Column 1**: zero, two, two. Best two → `5 + 2 = 7`. **Column 2**: minus one, one, three. Best three → `1 + 3 = 4`.
>
> **[VISUAL: row 1 fills in as `[2, 7, 4]`. Counter reads 9.]**
>
> Nine comparisons — for one row of a three-wide grid. That's `n` cells times an `n`-column scan. `O(n²)` per row.
>
> **[VISUAL: the counter morphs — n = 10,000 → 100,000,000 per row → ×10 rows → 10⁹, glowing red.]**
>
> Now read the constraint. `m · n ≤ 10⁵`. Sounds small, right? But nothing stops the grid from being **wide**: ten rows by ten thousand columns. That's ten rows, each costing a hundred million comparisons. **A billion operations.** Dead on arrival.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The scans for row-1 column 0 and row-1 column 1 are drawn side by side, candidate values stacked. The candidate lists are nearly identical — only the penalties differ, each by exactly 1. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Look at two neighbouring cells' scans side by side. Column 0 asked about `dp[0][0]`, `dp[0][1]`, `dp[0][2]`. Column 1 asked about… the exact same three values. Same candidates. The *only* difference is the penalty each one pays, and every penalty shifted by exactly **one**.
>
> **LEARNER:** Hold on though — the constraint says `m · n ≤ 10⁵`. That's a tiny grid overall. Why isn't `O(n²)` per row just fine?
>
> **TEACHER:** That's the trap, and it's deliberately set. `m · n` is bounded, but `m · n²` isn't — it's `(m · n) · n`, so it scales with `n`, and `n` alone can be ten thousand or more. The problem setter chose that constraint *specifically* so a correct DP with a slow transition dies. They're not testing whether you can write the recurrence. They're testing whether you can make it cheap.
>
> **TEACHER:** So here's your think. We're recomputing almost the same maximum, `n` times per row, and each version differs by a predictable amount. **Pause the video.** What would you have to compute *once*, left to right, so that every cell could just read its answer instead of scanning?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the expression `max over j of ( prev[j] − |c − j| )` centred. The `|c − j|` bars pulse red.]**

> **TEACHER:** Everything painful in that expression lives inside those absolute-value bars — so let's kill them. An absolute value is just two cases wearing one costume: the predecessor column `j` is either **at or to the left** of me, or **at or to the right**. That's it.
>
> **[VISUAL: the expression splits into two boxed lines; the parenthesised parts glow gold, the lone `c` terms grey out.]**
>
> If `j ≤ c`, then `|c − j|` is simply `c − j` — so the candidate is `prev[j] − c + j`, which I'll write as **`(prev[j] + j) − c`**. And if `j ≥ c`, then `|c − j|` is `j − c` — the candidate is **`(prev[j] − j) + c`**.
>
> Stare at the gold. `prev[j] + j` and `prev[j] − j` **don't depend on `c` at all.** They're properties of the *predecessor*, not of me. So for the left case, every column wants the same thing: the biggest `prev[j] + j` seen so far. That's a running maximum — one sweep, left to right.
>
> And here's the picture that makes it stick. **Don't think "I scan backwards for a predecessor." Think: the previous row's values walk toward me, and every step costs them one point.**
>
> **[VISUAL: the row `[2, 7, 4]` as three glowing tokens. The `7` steps one cell left and dims to `6`; steps again and dims to `5`. A "−1 per step" tag follows it. Then a 4-second "🤔 predict" timer over a half-written line: `left[c] = max( ______ , prev[c] )`]**
>
> A seven one column away arrives as a six. Two columns away, a five. It fades as it travels. So the best value *arriving* at column `c` is either the value already parked at `c`, or whatever was walking toward me — one step more tired. **Pause again** and fill in that blank: what does `left[c]` need from `left[c−1]`?
>
> *(pause)*
>
> **[VISUAL: the blank fills in: `left[c] = max(left[c-1] - 1, prev[c])`]**
>
> There it is. **`left[c] = max(left[c−1] − 1, prev[c])`.** Either the traveller from the left, minus one for the step it just took — or the local value, which travelled zero and pays nothing.
>
> **LEARNER:** But that minus-one applies to the whole running max. If the winner has already walked five columns, this step decrements it a sixth time — while a fresh local value gets decremented zero times. Is that actually the right penalty for each candidate?
>
> **TEACHER:** It's exactly right, and that's the elegance. A candidate that entered the sweep at column `j` gets decremented **once per step it survives** — so by the time the running max reaches column `c`, it's been hit `c − j` times. That's `prev[j] − (c − j)`, which is precisely the penalty the brute force charges it. Every candidate pays for its own distance, automatically, because it's been carried that many steps. Induction on `c` — the sweep *is* the proof. Then do the mirror image right-to-left for predecessors on my right, and take the better of the two. **Two linear sweeps replace `n` full scans.**

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "|c − j| in a DP transition ⇒ split into j ≤ c and j ≥ c ⇒ two directional running maxes, decaying 1 per step."]**

> Burn this one line in: **an absolute-value distance penalty inside a DP transition splits into two directional prefix sweeps.** Left sweep handles predecessors at or to your left; right sweep handles at or to your right. Each is a running max that fades by one per step it travels. The overlap at `j = c` is harmless — both sweeps see it, and it's the same value.
>
> That's not a trick for this problem. That's a reflex: whenever a transition says *"take the best previous state, minus how far away it is,"* your hand should reach for two sweeps.

---

## 7. CODE IT — LIVE & CHUNKED — `5:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Dimensions, and the base row — row 0 is free.

```python
def maxPoints(points):
    m, n = len(points), len(points[0])
    dp = [[0] * n for _ in range(m)]
    dp[0] = points[0][:]                       # row 0: no penalty yet
```

> **[VISUAL: add chunk 2, highlight the recurrence line.]** Now, for each row, grab the previous row and run the left sweep.

```python
    for r in range(1, m):
        prev = dp[r - 1]

        # left[c] = best of (prev[j] - (c - j)) for all j <= c
        left = [0] * n
        left[0] = prev[0]
        for c in range(1, n):
            left[c] = max(left[c - 1] - 1, prev[c])   # carried value fades by 1 per step
```

> **[VISUAL: add chunk 3, mirrored — the loop counter runs backwards, highlighted.]** Same thing, other direction. Start at the far right, walk left.

```python
        # right[c] = best of (prev[j] - (j - c)) for all j >= c
        right = [0] * n
        right[n - 1] = prev[n - 1]
        for c in range(n - 2, -1, -1):
            right[c] = max(right[c + 1] - 1, prev[c])
```

> **[VISUAL: add chunk 4.]** And the payoff: every cell just reads its two answers. No scan. Three linear passes per row — that's the whole algorithm.

```python
        for c in range(n):
            dp[r][c] = points[r][c] + max(left[c], right[c])

    return max(dp[m - 1])
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:20`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Now *why*, line by line.
>
> `dp[0] = points[0][:]` — row 0 has no row above it, so there's no travel to pay for. And note the slice: copy it, don't alias the input.
>
> `left[0] = prev[0]` — column 0 has nobody to its left, so the only left-or-equal candidate is the value directly above. Seed it with that and the recurrence takes over. Same reasoning, mirrored, for `right[n-1]`.
>
> `max(left[c - 1] - 1, prev[c])` — the entire optimization in one line. `left[c-1] - 1` is "whatever was winning, one step more tired." `prev[c]` is "the value right above me, which travelled nothing." Drop the `- 1` and you'd stop charging for distance. Drop the `prev[c]` and a fresh, closer candidate could never enter the race.
>
> `max(left[c], right[c])` — the best predecessor could be on either side, so we take the better sweep. And yes, the cell directly above appears in *both* sweeps. That's fine: it's the same number, and `max` doesn't care about duplicates.
>
> **LEARNER:** Why do we need two sweeps at all? Couldn't I just find the single largest value in `prev`, and subtract its distance to `c`? The biggest number is surely the best predecessor.
>
> **TEACHER:** That's the tempting one, and it's wrong — the penalty is what breaks it. Take a previous row of ten columns: a `10` at column 0, and a `12` at column 9, ones in between. Now compute column 0. Your rule says take the global max, twelve, minus nine columns of travel — three. But the boring `10` sitting right there pays nothing and delivers **ten**. A slightly smaller value that's *close* beats a bigger one that's *far*. That's exactly why the answer depends on `c` and you can't collapse it to a single global winner. The sweeps solve it because they compare `prev[j] − distance`, not `prev[j]`.
>
> One last thing you must say out loud in a Java room: values go up to `10⁵` and there can be `10⁵` rows, so the total can hit **`10¹⁰`** — that overflows a 32-bit `int`. Use `long`. LeetCode's Java signature literally returns `long` for exactly this reason.

---

## 9. DRY-RUN THE CODE — `8:45`
*(worked example — prove it, close the loop)*

**[VISUAL: the 3×3 grid on the left; a trace table filling row by row on the right; the sweep arrays animate as tokens walking and dimming.]**

> Run the real code on our grid — `[[1,2,3],[1,5,1],[3,1,1]]`.

| Step | left sweep | right sweep | dp row |
|---|---|---|---|
| Row 0 | — | — | `[1, 2, 3]` |
| Row 1 (prev `[1,2,3]`) | `[1, max(0,2)=2, max(1,3)=3]` | `[max(1,1)=1, max(2,2)=2, 3]` | `1+1, 5+2, 1+3` → `[2, 7, 4]` |
| Row 2 (prev `[2,7,4]`) | `[2, max(1,7)=7, max(6,4)=6]` | `[max(6,2)=6, max(3,7)=7, 4]` | `3+6, 1+7, 1+6` → `[9, 8, 7]` |

> Row 1 lands on `[2, 7, 4]` — identical to the nine comparisons we ground out by hand, but with three passes instead of nine scans.
>
> **[VISUAL: zoom on row 2, column 0. The `7` token in `prev` steps one cell left, dims to `6`, and lands on the `3`.]**
>
> Now the money moment: **row 2, column 0.** The left sweep says two — just the value above. But the right sweep says **six**: the seven parked at column 1 walked one step left and faded to six. Add the cell's own three — **nine**. No scan. The seven *came to us*.
>
> Final row is `[9, 8, 7]`. Take the max — **9**. Exactly the nine we promised in minute one. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:50`
*(transfer to interview)*

**[VISUAL: comparison table — Brute force: O(m · n²) time, O(n) space. Ours: O(m · n) time, O(m · n) space. A note: "3 linear passes per row".]**

> Say it the way you'd say it in the room: *"The brute force is `O(m · n²)` — every cell scans every previous column. My version does three linear passes per row: a left sweep, a right sweep, and a combine. So the transition is `O(1)` per cell and the whole thing is `O(m · n)` time. Space is `O(m · n)` right now, for the full table."*
>
> With `m · n ≤ 10⁵`, that's a hundred thousand operations instead of a billion — four orders of magnitude, from one algebraic observation about absolute value.

---

## 11. CAN WE USE LESS MEMORY? — `10:20`
*(depth + honesty)*

**[VISUAL: the full `dp` table; every row except the last two greys out and dissolves. A single rolling `prev` array remains.]**

> Look at what the transition actually reads. Only `prev` — the row immediately above. Row 5 never asks about row 2. So the full 2-D table is dead weight; keep **one rolling row**.

```python
def maxPoints(points):
    n = len(points[0])
    prev = points[0][:]                        # rolling: only the last row's totals
    for row in points[1:]:
        left = [0] * n
        left[0] = prev[0]
        for c in range(1, n):
            left[c] = max(left[c - 1] - 1, prev[c])
        right = [0] * n
        right[n - 1] = prev[n - 1]
        for c in range(n - 2, -1, -1):
            right[c] = max(right[c + 1] - 1, prev[c])
        prev = [row[c] + max(left[c], right[c]) for c in range(n)]
    return max(prev)
```

> Same time, `O(m · n)`. Space drops to **`O(n)`**. Can we go below that? **No — and say why.** Every new row needs the best delivered value at *every one* of the `n` columns, and those `n` numbers are genuinely distinct pieces of state. `O(n)` is the floor for this transition. Naming the floor out loud is a stronger signal than silently accepting it — and the rolling-row move you just made is one you'll reuse in every remaining video of this section.

---

## 12. YOUR TURN (active recall) — `10:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Falling Path Sum II (LC 1289)". A blank editor.]**

> Before the next video, go do **Minimum Falling Path Sum II** — LeetCode 1289. Same disease: a row DP whose transition looks at *every* column of the previous row, so the naive version is `O(n²)` per row. But the cure is **different**. There's no distance penalty this time; the only rule is "don't pick the same column twice in a row." Sweeps won't help you — something much simpler will. Ten minutes, no peeking. Find the cure yourself and you've learned the real lesson: *diagnose the slow transition first, then choose the tool.* (Want an easier on-ramp? **Minimum Falling Path Sum, LC 931** — same shape, but the reach is only three neighbours, so no compression is needed at all.)

---

## 13. LOCK IT IN — `11:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **The states were never the problem — the transition was.** `dp[r][c]` = best total ending at column `c` in row `r` is correct on the first try. `m · n ≤ 10⁵` is a booby trap aimed straight at `O(m · n²)`.
> 2. **Absolute value is two cases in a trench coat.** `|c − j|` splits into `(prev[j] + j) − c` and `(prev[j] − j) + c` — and the parenthesised part never depends on `c`, which is exactly what makes a running max legal.
> 3. **Two sweeps, decaying one per step, then roll the row.** `O(m · n)` time, `O(n)` space — and in Java, `long`, because `10¹⁰` doesn't fit in an `int`.
>
> **[VISUAL: big box → "The best value walks toward you, losing one point per step."]**
>
> And the memory peg — the one line that recalls the whole pattern: **the best value walks toward you, losing one point per step.** When a transition charges you for *distance*, stop scanning backwards. Let the previous row walk to you and fade.
>
> *(GCA reminder — for the interview itself: Google scores the path, not just the destination. Say the row DP out loud first, name it as correct, then point at the constraint and say "but this transition is `O(n²)` per row and `m·n ≤ 10⁵` is telling me that's the point of the problem." **Then** split the absolute value. That narration — naive, diagnose, fix — is the actual signal being graded.)*

---

## 14. CLIFFHANGER — `12:05`
*(open loop to next lesson)*

**[VISUAL: a blurred title — "Student Attendance Record II". A grid fades out and is replaced by a tiny state machine: three circles labelled P, A, L, with arrows looping between them.]**

> Every DP so far has had an obvious "where am I" — a cell, a column, an index. The state was a *place*. The next problem breaks that. You're counting attendance records of length `n` that stay eligible for an award — at most one absence total, never three lates in a row. There's no grid. There's no position to sweep. So what's the state?
>
> The answer is the idea that unlocks half of all hard DP: **the state isn't where you are — it's what you're still carrying.** That's Student Attendance Record II. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public long maxPoints(int[][] points) {
    int n = points[0].length;
    long[] prev = new long[n];                 // rolling: previous row's best totals
    for (int c = 0; c < n; c++) prev[c] = points[0][c];

    long[] left = new long[n];
    long[] right = new long[n];
    for (int r = 1; r < points.length; r++) {
        // left[c] = best of (prev[j] - (c - j)) for j <= c
        left[0] = prev[0];
        for (int c = 1; c < n; c++)
            left[c] = Math.max(left[c - 1] - 1, prev[c]);

        // right[c] = best of (prev[j] - (j - c)) for j >= c
        right[n - 1] = prev[n - 1];
        for (int c = n - 2; c >= 0; c--)
            right[c] = Math.max(right[c + 1] - 1, prev[c]);

        long[] cur = new long[n];
        for (int c = 0; c < n; c++)
            cur[c] = points[r][c] + Math.max(left[c], right[c]);
        prev = cur;
    }

    long best = 0;
    for (long v : prev) best = Math.max(best, v);
    return best;
}
```

*(The `long` is not optional: `10⁵` rows × `10⁵` per cell = `10¹⁰`, which overflows `int`. LeetCode's own signature returns `long` — treat that as a hint the graders left you.)*
