# 🎬 Recording Script — Student Attendance Record II

**Pattern: Dynamic Programming (state-machine DP) · LeetCode 552 · Hard · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Maximum Number of Points with Cost (previous lesson) — there the DP state was obvious (`row, column`) and the *transition* was the hard part. Today it flips: the transition is trivial, and **finding the state is the whole problem.**

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a terminal counting up. `n=10` → 59,049 strings, done instantly. `n=15` → 14 million, a beat. `n=20` → 3,486,784,401, the counter crawls, the fan spins, a red "Time Limit Exceeded" slams over it. Then the constraint line fades in underneath: `1 ≤ n ≤ 100,000`.]**

> Here's a problem that looks like counting and is actually a trap.
>
> A student's attendance record is a string of A's, L's and P's. It earns a reward if there's **at most one A total**, and **never three L's in a row**. Question: for a record of length `n`, how many rewardable strings exist?
>
> Your brain says: generate them all, filter. And it works — for about twenty characters. At `n = 20` you're generating **three and a half billion** strings. And the constraint says `n` can be a **hundred thousand**. There are more valid records than atoms in the universe. You will never enumerate them.
>
> So we're not going to. By the end of this video, you'll be counting a hundred thousand characters' worth of strings using **six integers**. Six. That's the whole solution. Let's go find them.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: two rule cards at the top — "≤ 1 'A' in the whole string" and "no 'LLL' anywhere". Below, all nine two-character strings laid out in a 3×3 grid.]**

> One line: **count the length-`n` strings over A, L, P that break neither rule. Answer mod 1e9+7.**
>
> Let's make it tiny. `n = 2`. Nine possible strings — here they all are.

```
PP   PL   PA
LP   LL   LA
AP   AL   AA   ← two A's. Illegal.
```

> Eight survive. `"AA"` is the only casualty — two absences. So `n = 2` gives **8**. And `n = 1` obviously gives **3**: A, L, P, all fine.
>
> Hold onto those two numbers — 3 and 8. We're going to check every version of the solution against them.
>
> And before you'd write a line in a real interview, ask the question that proves you read the spec: *"At most one A in the **entire string** — not one per week — and LLL means three **consecutive**, so `"LLPLL"` is legal, right?"* Those two readings **are** the problem. Ten seconds to confirm, saves a full rewrite.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:40`
*(worked example — let them feel the waste)*

**[VISUAL: a tree growing from the empty string — level 1 branches to A, L, P; level 2 to nine; level 3 to twenty-seven. A "strings generated" counter ticking. Then it fast-forwards and the tree turns into a solid black wall.]**

> Let's do the literal thing and watch it die.

```python
from itertools import product

def checkRecord_brute(n):
    total = 0
    for combo in product("APL", repeat=n):      # all 3^n records
        record = "".join(combo)
        if record.count("A") <= 1 and "LLL" not in record:
            total += 1
    return total
```

> Every character has three choices, so the tree triples at every level. `n = 3` is 27 strings — I can draw those. `n = 10` is fifty-nine thousand. `n = 20` is **three point five billion**.
>
> **[VISUAL: the counter with a log-scale bar; 3^n plotted against a flat "one second of compute" line, crossing it around n = 18.]**
>
> And notice something painful. To check a string, I `.count("A")` and I search for `"LLL"` — I re-scan the **whole string** every single time. I built a 100,000-character record just to ask two tiny yes/no questions about it.
>
> Don't throw this code away though. It's slow, but it's **right** — and we're going to use it as our test oracle. Anything we write next has to agree with it at `n = 1, 2, 3`.

---

## 4. THE PAIN POINT + PREDICT — `2:50`
*(close loop #1 + generation effect — pause #1)*

**[VISUAL: two long records side by side — `"PPLAPPLP"` and `"LPPPALPP"`. Both highlight: one A used, zero trailing L's. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Look at these two records. Totally different strings. Now ask the only question that matters: **which characters am I allowed to append next?**
>
> Both have spent their one A — so no more A's. Both end in a P — so zero L's trailing, meaning an L is fine. Identical answers. Every legal ending for the first one is a legal ending for the second one. They are, for all future purposes, **the same string**.
>
> **LEARNER:** So the string itself is mostly noise. Only some tiny summary of it actually constrains what comes next.
>
> **TEACHER:** That's exactly it. So here's your job — pause the video. **What is the smallest set of facts about a prefix that fully determines which characters can legally follow it?** Not "the string." Something much smaller. And then count: how many possible values does that summary have?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:45`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the two records collapse into a single badge: `(A used: 1, trailing L's: 0)`. Then a 2×3 grid of six badges materializes and locks into place.]**

> **TEACHER:** Two facts. That's it.
>
> **One — have I spent my A?** Zero or one. It can never be two, because two is illegal. **Two options.**
>
> **Two — how many L's are sitting at the end right now?** Zero, one, or two. It can never be three, because three is illegal — that state simply doesn't exist. **Three options.**
>
> Two times three. **Six states.** For `n = 5`. For `n = 100,000`. Six, forever.
>
> **[VISUAL: the 2×3 grid labelled — top row `a=0`: `l=0, l=1, l=2`; bottom row `a=1`: `l=0, l=1, l=2`. Each cell shows a counter, all zero except the top-left showing 1.]**
>
> Think of it like a queue at a counter with six windows. You don't track *people* — you track **how many people are standing at each window**. Every new character, everyone takes a step, and you just update six numbers.
>
> So: don't count strings. **Count how many strings are sitting in each of the six buckets.** Start with one string — the empty one — in bucket `(0 A's, 0 trailing L's)`.
>
> Now append a character and watch the buckets flow.
>
> **[VISUAL: arrows animate one at a time as each is named — P arrows collapsing to the l=0 column, L arrows stepping rightward, A arrows dropping from the top row into `(1,0)`.]**
>
> - Append **P** — an L-streak just got broken. Whatever your A-count, you land in trailing-L **zero**.
> - Append **L** — trailing count goes up by one. But **only if it's currently 0 or 1**. From trailing-two, that arrow doesn't exist. That's how "no LLL" gets enforced: not with an if-check, but by **deleting the arrow**.
> - Append **A** — only legal if your A-count is zero. You land in `(1, 0)`: one A spent, streak broken.
>
> **LEARNER:** Hang on. Where's the check for "is this string valid"? I don't see one anywhere.
>
> **TEACHER:** There isn't one — and that's the beautiful part. **Every state in the grid is a valid record, and every arrow leads to another valid record.** Illegal strings aren't rejected; they're never built. The rules stopped being a filter and became the **shape of the machine**.

---

## 6. THE KEY MOVE (signaling) — `5:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line, held on screen.]**

> Burn this in: **when the legality of the next character depends only on a bounded summary of the past, that summary *is* your DP state — and you count states, not strings.**
>
> Here the summary is "A's used, L's trailing" → six states. The reusable recipe is three steps: **enumerate the states, draw the legal arrows, add up the counts.** That's state-machine DP, and it's a whole family — Knight Dialer, Domino Tiling, Count Vowels Permutation. Different alphabets. Same machine.

---

## 7. CODE IT — LIVE & CHUNKED — `5:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1 only.]**

> Version one — a literal table, so you can *see* the states. `dp[i][a][l]` is: how many length-`i` prefixes are sitting in state `(a, l)`.

```python
MOD = 10**9 + 7

def checkRecord_table(n):
    dp = [[[0] * 3 for _ in range(2)] for _ in range(n + 1)]
    dp[0][0][0] = 1          # one string of length 0: the empty record
```

> **[VISUAL: chunk 2 lands; each transition line highlights as it's spoken.]** Now the loop. For every position, for every state, push its count forward along the three arrows.

```python
    for i in range(1, n + 1):
        for a in range(2):
            for l in range(3):
                cur = dp[i - 1][a][l]
                if cur == 0:
                    continue
                dp[i][a][0] = (dp[i][a][0] + cur) % MOD              # append 'P'
                if l < 2:
                    dp[i][a][l + 1] = (dp[i][a][l + 1] + cur) % MOD  # append 'L'
                if a == 0:
                    dp[i][1][0] = (dp[i][1][0] + cur) % MOD          # append 'A'
```

> **[VISUAL: chunk 3.]** And the answer is every bucket added up — because, again, every state is a valid record.

```python
    return sum(dp[n][a][l] for a in range(2) for l in range(3)) % MOD
```

> Three transition lines. Two guard conditions. That's the entire Hard problem.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the finished function; each region spotlights as it's named.]**

> Why each piece exists.
>
> **`dp[0][0][0] = 1`** — the empty string is one real record, with zero A's and zero trailing L's. Seed it with zero instead and every count downstream is zero. The seed *is* the base case.
>
> **`if l < 2`** — this single line is the entire "no LLL" rule. From trailing-two, the L-arrow doesn't exist. We never generate `LLL`, so we never have to detect it.
>
> **`if a == 0`** — the entire "at most one A" rule. And notice the target is `dp[i][1][0]`, not `dp[i][a+1][0]`: an A always lands you in A-count one, and it always resets the L-streak.
>
> **`% MOD` on every addition** — and here's why it's not optional.
>
> **LEARNER:** Isn't that just ceremony? Take the modulus once at the end and be done.
>
> **TEACHER:** Try it and you'll get a wrong answer, not a slow one. The true count grows about 1.84 to the `n`. By `n = 40` it's past a 32-bit int. By `n` around **90** it's past 64 bits — and `n` goes to a hundred thousand. If you only mod at the end there's nothing left to mod; the number overflowed eighty-nine thousand steps ago. We can mod as we go because we only ever **add**, and addition plays nicely with modulus. If this problem had a subtraction in it, that's where you'd need a `+ MOD` guard to keep things non-negative.
>
> **The final `sum` over all six** — not just one lucky cell. There's no "finished" state here. A record that ends mid-L-streak is perfectly valid; it just ended. So every bucket counts.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the six-bucket grid, filling row by row alongside the table below. The running total ticks: 1 → 3 → 8 → 19.]**

> Run it by hand for three days. Six columns, one row per character appended.

| Day | `a0l0` | `a0l1` | `a0l2` | `a1l0` | `a1l1` | `a1l2` | Total |
|---|---|---|---|---|---|---|---|
| 0 (empty) | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| 1 | 1 | 1 | 0 | 1 | 0 | 0 | **3** |
| 2 | 2 | 1 | 1 | 3 | 1 | 0 | **8** |
| 3 | 4 | 2 | 1 | 8 | 3 | 1 | **19** |

> Day 1 you can literally read off: the `1` in `a0l0` is `"P"`. The `1` in `a0l1` is `"L"`. The `1` in `a1l0` is `"A"`. Total **3** — matches.
>
> Day 2 totals **8** — that's nine minus `"AA"`. Matches our hand count from the top of the video. Loop closed.
>
> Day 3 totals **19**. Check it independently: 27 total strings, minus `"LLL"`, minus the seven strings holding two or more A's — 27 minus 8 is 19. ✅
>
> **[VISUAL: split screen — brute force and the DP printing identical numbers 3, 8, 19, 43, 94 for n = 1 through 5.]**
>
> And that's the habit worth stealing: **run the brute force against the DP on small inputs.** A recurrence that's subtly wrong looks exactly like a recurrence that's right — until you diff them.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: comparison table — Brute: O(n · 3ⁿ) time. Table DP: O(n) time, O(n) space. Rolling: O(n) time, O(1) space.]**

> Say it the way you'd say it in the room: *"Time is `O(n)` — six states, three transitions each, so constant work per character; the constant factor is six. Space is `O(n)` for the table. That's down from `O(n · 3^n)`, which is the difference between a hundred thousand steps and a number with fifty thousand digits."*
>
> Notice what changed and what didn't. The **states** collapsed from "every possible string" to six. The **length** still costs us one pass. That's the trade this whole DP section keeps making.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:50`
*(depth + honesty — pause #2)*

**[VISUAL: the full dp table with row i highlighted, an arrow pointing back only to row i−1; all earlier rows grey out and dissolve. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at the loop body one more time. `dp[i]` reads exactly one thing: `dp[i - 1]`. Nothing else. So — pause — **what is that entire table doing in memory?**
>
> *(pause)*
>
> Nothing. Row `i − 2` is garbage the moment row `i` starts. Throw the table away and keep six variables.

```python
MOD = 10**9 + 7

def checkRecord(n):
    a0l0, a0l1, a0l2 = 1, 0, 0      # empty record: 0 absences, 0 trailing L's
    a1l0, a1l1, a1l2 = 0, 0, 0

    for _ in range(n):
        n0l0 = (a0l0 + a0l1 + a0l2) % MOD                       # 'P' from any a=0 state
        n0l1 = a0l0                                             # 'L' onto 0 trailing L's
        n0l2 = a0l1                                             # 'L' onto 1 trailing L
        n1l0 = (a0l0 + a0l1 + a0l2 + a1l0 + a1l1 + a1l2) % MOD  # 'A' from a=0, 'P' from a=1
        n1l1 = a1l0
        n1l2 = a1l1

        a0l0, a0l1, a0l2 = n0l0, n0l1, n0l2
        a1l0, a1l1, a1l2 = n1l0, n1l1, n1l2

    return (a0l0 + a0l1 + a0l2 + a1l0 + a1l1 + a1l2) % MOD
```

> Read `n1l0` out loud, because it's the busiest line: you reach state "one A, no trailing L's" either by **spending your A** from any A-free state, or by **appending a P** from any state that already spent it. All six feed in.
>
> **LEARNER:** Why the six `n`-prefixed temporaries? Why not just assign straight into `a0l1` and save the clutter?
>
> **TEACHER:** Because `n0l1 = a0l0` needs the **old** `a0l0`. If you'd already overwritten it on the line above, you're reading this character's value while computing this character's value — one day of history, silently duplicated. It won't crash. It won't even look wrong. It'll just print a number that isn't the answer. **Compute all six from the old six, then commit all six.** That's the rule for every rolling-DP you'll ever write.
>
> So: `O(n)` time, **`O(1)` space**. Six integers for a hundred thousand characters.
>
> And if the interviewer pushes — *"now `n` is ten to the eighteenth"* — here's the sentence that ends the round: *"That six-variable update is a fixed linear map, so it's a 6×6 matrix. Binary-exponentiate the matrix and it's `O(6³ log n)`."* You don't have to write it. Naming it is the signal.

---

## 12. YOUR TURN (active recall) — `11:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Knight Dialer (LC 935)" — a phone keypad with a knight on the 6, arrows fanning out to 1, 7, and 0.]**

> Before the next video, go do **Knight Dialer, LeetCode 935**. A chess knight starts on a phone keypad and jumps `n − 1` times — count the distinct numbers it can dial, mod 1e9+7.
>
> It's today's lesson wearing a different shirt. Ask the same three questions: **what's the state?** (which digit you're standing on — ten states). **What are the legal arrows?** (the knight moves from that key). **What's the answer?** (sum all ten at the end). Then roll it down to ten variables.
>
> Fifteen minutes, no peeking. And test it against a brute force at `n = 1, 2, 3` — same habit as today. If you can build the state machine from scratch, this pattern is yours for good.

---

## 13. LOCK IT IN — `11:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **`3^n` enumeration dies around n = 20.** When the answer is a count over an exponential space, the answer is never "generate them."
> 2. **The state is the smallest summary that decides what's legal next.** Here: A's used (2 values) × trailing L's (3 values) = **six states**, independent of `n`. Illegal states don't get rejected — they don't exist.
> 3. **If row `i` only reads row `i−1`, the table is dead weight.** Roll it into variables — `O(n)` space becomes `O(1)`. Compute all new values before committing any.
>
> The memory peg:
>
> **[VISUAL: big box → "Don't count the strings. Count the buckets they land in."]**
>
> When a problem says *"how many sequences never break rule X,"* your hand should already be drawing a state machine.
>
> *(GCA reminder — Google scores **how** you approach a novel problem, not just the final code. Say the `3^n` brute force out loud. Then say the sentence that earns the hire: *"Let me figure out what I actually need to remember about a prefix."* Enumerate the states aloud, draw the arrows on the whiteboard, **then** code. The examiner is grading the path, so make the path audible.)*

---

## 14. CLIFFHANGER — `12:20`
*(open loop to next lesson)*

**[VISUAL: a blurred title card — "Filling Bookcase Shelves" — a row of books of different thicknesses and heights, a shelf line, and a book hovering ambiguously between staying on this shelf and starting a new one.]**

> Today the state set was small, fixed, and finite — six buckets, and you could draw all of them.
>
> Next problem: you're placing books on shelves in order, each shelf has a width limit, and the shelf's height is the tallest book on it. Minimise the total height. And here's the twist that breaks today's approach — **the "state" isn't a badge you can enumerate up front.** Whether this book should start a new shelf depends on books you haven't decided about yet. Greedy is going to feel obviously right, and it's going to be obviously wrong.
>
> So what do you index the DP on when the state won't sit still? That's **Filling Bookcase Shelves**. See you there.
