# 🎬 Recording Script — Race Car
**Pattern: BFS over states → DP · LeetCode 818 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** *Shortest Path in a Grid with Obstacles Elimination* (Section 3) — we folded a budget into the BFS node there. Today we fold in **speed**… and then we delete the BFS entirely.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: black screen. One line types out: `target = 4`. Below it, a number line 0…8 with a small car at 0. Then a red banner: "Your answer: 6 · Correct answer: 5".]**

> **TEACHER:** Google onsite. The interviewer says: *"Car starts at zero, speed one. `A` moves you and doubles your speed. `R` flips your speed to plus or minus one. Shortest instruction string to land exactly on `target`. Go."*
>
> You reason it out: floor it until you pass the target, turn around, floor it back. For target **four** that's `A A A R A A` — six instructions. Clean. Logical. And **wrong** — the real answer is five.
>
> **[VISUAL: the string `A A R R A` appears in green, with the two Rs pulsing.]**
>
> Look at the sequence that wins. Two reverses, back to back. Two whole instructions where the car **does not move a single unit.** Your gut says that's a wasted move. Your gut is wrong, and understanding *why* is this entire lesson.
>
> We're solving this twice: once with a search you can actually derive under pressure, and once with a dynamic program that collapses that search into fourteen lines. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: two rule cards side by side, then a 5-row trace table filling in for target = 6.]**

> The rules, in full, take ten seconds. You start at **position 0**, **speed +1**. `'A'` — accelerate — adds your speed to your position, *then* doubles the speed. `'R'` — reverse — sets your speed to **−1** if it was positive, **+1** if it was negative. Position doesn't change.
>
> **[VISUAL: highlight the reverse card.]** Read that reverse rule again. It doesn't negate your speed — it *resets* it to one. Blast up to speed thirty-two, hit `R`, and you're crawling at minus one. Reverse throws away everything you built.
>
> Here's target **six**, solved in five:

```
        position   speed
start        0       +1
A            1       +2
A            3       +4
A            7       +8
R            7       −1
A            6       −2      ← landed
```

> `AAARA`. Overshoot to seven, flip, one backward step lands on six. Keep this tiny example in your head — we'll come back to it three times today.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — feel where it breaks)*

**[VISUAL: number line 0…8. Car animates the greedy run for target = 4, instruction counter ticking up.]**

> Let's run the greedy idea from the cold open properly, on target **four**, and watch it fail.
>
> Floor it: `A` → position 1. `A` → position 3. Still short. `A` → position **7**. Overshot. So `R`, now speed minus one. `A` → 6. `A` → 4. Arrived. **[VISUAL: counter freezes on 6, caption "AAARAA — 6 instructions".]** Six instructions, and it *feels* optimal — no backtracking, no dithering. But here's the winner:
>
> **[VISUAL: replay on the same number line — `A A R R A`, with the car sitting perfectly still through both Rs.]**
>
> `A` → 1. `A` → 3. Now `R` — speed becomes minus one. Then **`R` again** — speed becomes plus one. The car hasn't moved. It's still sitting on 3. But it's now facing forward at speed **one** instead of speed **four**, and from there a single `A` lands exactly on 4.
>
> Those two reverses didn't move the car. They **reset the speedometer.** That's what greedy could never see: sometimes the right play is to spend instructions buying back a slow, controllable speed.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — PAUSE #1)*

**[VISUAL: freeze on position 3 with two ghost cars stacked on the same tile — one labeled "speed +4", one labeled "speed +1". A 5-second "🤔 your turn" timer.]**

> **TEACHER:** So greedy is dead. We need to search. But look at this frame before you write a single line of BFS.
>
> Two cars. **Same position — position three.** One is doing speed plus four. One is doing speed plus one. Are those the same situation?
>
> **LEARNER:** No way. The fast one blows straight past 4 on its next move. The slow one lands on it. Same square, totally different futures.
>
> **TEACHER:** Exactly. So here's your think. This is a shortest-*sequence* problem, which means BFS — fewest instructions is fewest edges. But BFS needs nodes. **Pause the video and answer one question: what is a node here?** Not "where's the car." What *fully* describes the car's situation?
>
> *(pause — 5 seconds)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it)*

**[VISUAL: the node draws itself as a two-part tile: `(position, speed)`. Then a BFS tree grows outward from `(0, +1)`, two edges per node labeled A and R.]**

> **TEACHER:** The node is the pair — **`(position, speed)`**. That's the whole modelling insight, and it's the same reflex we built in the obstacles-elimination lesson: when something you're carrying changes what you can do *next*, it belongs **inside the node**. There it was leftover eliminations. Here it's your speedometer.
>
> Now BFS is honest. Every node has exactly two out-edges — `A` and `R` — and every edge costs one instruction. First time we pop the target position, that's the shortest string.
>
> **[VISUAL: BFS levels for target = 6 fill in, one row per depth.]**

```
depth 0:  (0, +1)
depth 1:  (1, +2)   (0, −1)
depth 2:  (3, +4)   (1, −1)
depth 3:  (7, +8)   (3, −1)   (0, −2)   (1, +1)
depth 4:  (7, −1)   (2, −2)   (3, +1)   (2, +2)
depth 5:  (6, −2)   ← target! → 5 instructions, path AAARA
```

> Five levels, fourteen nodes expanded, and out pops **AAARA**. The same answer we hand-traced. BFS works.
>
> **LEARNER:** Hold on. The number line is infinite and the speed *doubles* forever. That's an infinite graph. How does the queue not just run away?
>
> **TEACHER:** Sharp — and that's the real cost of the BFS answer. You have to fence it, and you have to *justify* the fence. **[VISUAL: number line with the milestones 1, 3, 7, 15 marked; target sits between 3 and 7; a dashed wall drops at 2 × target.]** Here's the argument, short enough to say out loud in the room. From a standing start, `k` accelerations always land you on exactly `1 + 2 + 4 + … = 2^k − 1`. Let `k` be the **smallest** one of those milestones at or past your target. Smallest means the previous one, `2^(k-1) − 1`, is *below* target — so `2^(k-1) ≤ target`, so `2^k − 1 < 2 × target`. That first milestone past the target is always inside twice the target. Driving further right than that is pure waste — every extra unit is a unit you must undo. So: clamp position to `[0, 2·target]`, clamp speed magnitude to `2·target`, and the graph becomes finite. BFS terminates, and it's correct.

---

## 6. THE KEY MOVE (signaling) + PREDICT — `5:00`
*(signaling + generation effect — PAUSE #2)*

**[VISUAL: a boxed line: "Shortest sequence of moves → BFS over states. Then: if the states have structure, the search collapses into a DP."]**

> **TEACHER:** Burn in the first half of that box: **shortest sequence of moves means BFS over states.** That reflex alone gets you a working Hard solution.
>
> Now the second half — this is where the lesson earns its place in the DP section. Look at what BFS actually spent its time on. Almost every node it expanded was junk. The only nodes that ever mattered were the **milestones**, `2^k − 1` — the only places worth turning around.
>
> And here's the beautiful part: the *moment* you turn around, the problem restarts. You're somewhere on the line, at speed one, needing to cover some **smaller distance**. That's the same problem in a smaller box. The line doesn't care where zero is, and it doesn't care which way is "forward."
>
> **[VISUAL: `dp[t] = fewest instructions to cover distance t, starting from speed 1` in a box. Timer: 6 seconds.]**
>
> So define `dp[t]` — fewest instructions to cover a distance of `t`, starting from speed one. **Pause here.** You've got `k` A's that land you exactly on `2^k − 1`. If that's not your target, you have two choices: you went **too far**, or you stopped **too short**. Predict both: what does each cost, in terms of `dp` of something smaller?
>
> *(pause — 6 seconds)*

---

## 7. CODE IT — LIVE & CHUNKED — `5:50`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1 only.]**

> Three cases. Let's build them one at a time. Skeleton first — and `t.bit_length()` is exactly the `k` we want, because for any `t` in `2^(k-1) … 2^k − 1` it returns `k`.

```python
def racecar(target):
    dp = [0] * (target + 1)          # dp[0] = 0 — distance zero, no instructions
    for t in range(1, target + 1):
        k = t.bit_length()           # smallest k with 2^k - 1 >= t
```

> **[VISUAL: add chunk 2, highlight.]** **Case one — you land exactly.** If the milestone *is* the target, `k` A's and you're done. Nothing to optimise.

```python
        if (1 << k) - 1 == t:
            dp[t] = k
            continue
```

> **[VISUAL: add chunk 3, with the number line showing an overshoot arrow from `2^k − 1` back to `t`.]** **Case two — overshoot.** Run `k` A's past the target. Spend one `R` to flip around. Now you're facing a fresh, smaller journey of length `2^k − 1 − t`, from speed one. That's `dp` of that gap.

```python
        dp[t] = k + 1 + dp[(1 << k) - 1 - t]
```

> **[VISUAL: add chunk 4, the number line showing: stop short → R → back up → R.]** **Case three — undershoot.** Stop one milestone early at `2^(k-1) − 1`. Reverse. Back up for `j` accelerations — that's `2^j − 1` units backward. Reverse again, so you're facing forward at speed one. Then cover what's left.

```python
        for j in range(k - 1):       # j = 0 .. k-2
            rest = t - ((1 << (k - 1)) - 1) + ((1 << j) - 1)
            dp[t] = min(dp[t], k + j + 1 + dp[rest])
    return dp[target]
```

> That's the whole solution. Fourteen lines, no queue, no visited set, no fence to defend.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:30`
*(elaboration — derive the arithmetic, don't assert it)*

**[VISUAL: case three drawn as a four-row ledger, filling in as it's narrated.]**

> Case three is the one people get wrong, so let's **derive** the index instead of trusting it. Four phases:

```
k−1 × A   →  cost k−1   position 2^(k-1) − 1  =: P    speed 2^(k-1)
R         →  cost 1     position P                    speed −1
j   × A   →  cost j     position P − (2^j − 1)        speed −2^j
R         →  cost 1     position P − (2^j − 1)        speed +1
```

> Add the costs: `(k−1) + 1 + j + 1` = **`k + j + 1`**. Now the distance still to cover, forward, from speed one: target minus where we're standing, so `t − [P − (2^j − 1)]`, which is `t − (2^(k-1) − 1) + (2^j − 1)`. That's the `rest` in the code. No hand-waving — it's just the ledger.
>
> **LEARNER:** Why does `j` stop at `k − 2`? And honestly — `j = 0` means `R` then `R` with nothing between. That's two instructions that do nothing. Why is that even in the loop?
>
> **TEACHER:** Two great questions, and they're the same question. `j = k − 1` would back you up exactly `P` units — right back to position zero at speed one, the state you *started* in. You've burned `2k` instructions to go nowhere. Genuinely useless, so we cut it. But `j = 0` — the double reverse — is the opposite. It looks useless because the car doesn't move. It isn't. It's the only way to **reset your speed to one without changing position.** That's the target-four answer from the cold open: `AA` puts you on 3 at speed four, `RR` keeps you on 3 but drops you to speed one, one `A` lands on 4. Five instructions. Loop closed.
>
> **[VISUAL: `AARRA` replays, the RR pair highlighted with the caption "speed reset — position unchanged".]**
>
> Last thing: why can we fill this table left to right? Because both lookups are **strictly smaller than `t`**. Case two reads `2^k − 1 − t`, and since `2^(k-1) − 1 < t` we get `2^k − 1 < 2t`, so that index is below `t`. Case three reads at most `t − 2^(k-2)`. Every entry we read is already final. Simple ascending loop, no recursion needed.

---

## 9. DRY-RUN THE CODE — `9:10`
*(worked example — prove it)*

**[VISUAL: the dp table builds row by row, `t = 1` through `6`, winning case highlighted in green each row.]**

> Let's run it for real, target six. Build up from one.

| `t` | `k` | case 1 | case 2 (overshoot) | case 3 (undershoot) | `dp[t]` |
|---|---|---|---|---|---|
| 1 | 1 | `2¹−1 = 1` ✅ | — | — | **1** |
| 2 | 2 | `3 ≠ 2` | `2+1+dp[1] = 4` | `j=0`: `3+dp[1] = 4` | **4** |
| 3 | 2 | `2²−1 = 3` ✅ | — | — | **2** |
| 4 | 3 | `7 ≠ 4` | `3+1+dp[3] = 6` | `j=0`: `4+dp[1] = 5` · `j=1`: `5+dp[2] = 9` | **5** |
| 5 | 3 | `7 ≠ 5` | `3+1+dp[2] = 8` | `j=0`: `4+dp[2] = 8` · `j=1`: `5+dp[3] = 7` | **7** |
| 6 | 3 | `7 ≠ 6` | `3+1+dp[1] = 5` | `j=0`: `4+dp[3] = 6` · `j=1`: `5+dp[4] = 10` | **5** |

> `dp[6] = 5` — case two wins. Overshoot to seven, one `R`, then `dp[1]` is a single `A`. That's `AAA` + `R` + `A` — **`AAARA`**. The exact string our BFS popped at depth five, and the exact string we hand-traced at the start. Three independent routes, one answer. And look at row four: `dp[4] = 5`, won by **case three with `j = 0`** — the double reverse. The cold-open mystery, sitting right there in the table.

---

## 10. COMPLEXITY, OUT LOUD — `10:15`
*(transfer to interview)*

**[VISUAL: two rows — "BFS: O(target · log target) time AND space" vs "DP: O(target · log target) time, O(target) space".]**

> Say it the way you'd say it in the room: *"The outer loop runs `target` times. The inner loop runs `k` times, and `k` is at most log-base-two of target plus one. So it's `O(target log target)` time and `O(target)` space. For target ten thousand that's about fourteen iterations per entry — a hundred and forty thousand operations. Instant."*
>
> The BFS is the *same* time complexity — but its space is `O(target log target)`, because every position carries a fan of possible speeds, and it needs that fence argument to be correct at all. The DP needs neither. That's the upgrade you're selling.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:50`
*(depth + honesty)*

**[VISUAL: the dp array for t = 0…10 with arrows shooting from `dp[10]` to scattered earlier cells — not a neat window.]**

> **LEARNER:** Every other DP in this section rolled down to one or two variables. Can't we do the same here and get `O(1)`?
>
> **TEACHER:** No — and being able to say *why* is worth more than the trick would be. Rolling works when `dp[t]` only reads a **fixed-width window** behind it, like `dp[t-1]` and `dp[t-2]`. Look at ours.
>
> **[VISUAL: highlight `dp[6] → dp[1], dp[3], dp[4]`, then `dp[10000] → dp[6383], dp[1809], …`]**
>
> `dp[6]` reaches back to `dp[1]`, `dp[3]`, `dp[4]`. `dp[10000]` reaches all the way back to `dp[6383]` and to a spray of indices starting around `dp[1809]`. The overshoot case jumps to `2^k − 1 − t`, which can land **anywhere** in the range. The subproblems are reached out of order and the reach is unbounded. There's no window to slide — `O(target)` is the floor, and the whole table stays live.
>
> Say it out loud in the interview: *"I can't roll this one — the dependencies are scattered across the whole range, not confined to a window."* Naming the absence of a trick is a strong-hire move. The memory win was already banked when we dropped the BFS's speed dimension: `O(target log target)` down to `O(target)`.

---

## 12. YOUR TURN (active recall) — `11:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Perfect Squares (LC 279)". Blank editor.]**

> Before the next video: **Perfect Squares, LeetCode 279.** Fewest perfect squares that sum to `n`. And the assignment isn't "solve it" — it's **solve it twice.** Once as a BFS: nodes are remaining values, edges are "subtract a square," fewest edges wins. Then again as a one-dimensional DP over `n`. Same problem, both shapes, and you'll *feel* today's collapse in miniature.
>
> That's the muscle. Not memorizing Race Car's three cases — recognising when a search has enough structure to become a table.

---

## 13. LOCK IT IN — `12:05`
*(retrieval + memory peg)*

**[VISUAL: three bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Shortest *sequence of moves* = BFS over states** — and the state is whatever fully describes your future. Here, `(position, speed)`, because same square at different speeds is a different life.
> 2. **When the reachable states have structure, the search collapses.** `k` accelerations always land on `2^k − 1`; those milestones are the only turn-around points; after a turn it's the same problem, smaller. That's your `dp[t]`.
> 3. **A move that changes nothing can still be optimal.** `RR` doesn't move the car — it resets the speedometer. That's `dp[4] = 5`.
>
> The memory peg:
>
> **[VISUAL: big box → "Search first. Then look for the powers of two."]**
>
> When a problem screams "shortest sequence" and you can't see the DP, **start with BFS on the honest state.** Get something correct on the board. Then stare at which states actually matter — and if they line up on a pattern, that's your table.
>
> *(GCA reminder — for the interview itself: this is a two-act narration and both acts score. Act one: "shortest sequence, so BFS, and my node is position **and** speed, because speed changes what I can do next." Act two: "but let me look for structure — `k` A's always lands on `2^k − 1`, so I can define `dp` over remaining distance." Google isn't grading the final fourteen lines. It's grading you moving from a working answer to a better one, out loud. And ask the clarifying question early: **"Reverse sets speed to exactly ±1, not just negates it, right?"** That one question is what unlocks the double-reverse move.)*

---

## 14. CLIFFHANGER — `12:45`
*(open loop to next lesson)*

**[VISUAL: a new title blurs in — "Longest String Chain" — with words `a → ba → bda → bdca` chaining together, and a giant question mark over the arrow between them.]**

> Today the states lived on a number line, and "smaller subproblem" meant a smaller distance. Nice and orderly. Next problem, the states are **words**: `"bdca"` comes from `"bda"` comes from `"ba"` comes from `"a"`. Same DP instinct — build the answer from smaller pieces — but there's no number line to sort them on, and the predecessors aren't sitting at a tidy index. So what does "smaller" even mean, and how do you find a state's predecessors when there are `n` of them hiding in the input?
>
> That's **Longest String Chain**, and the answer is a sorting trick you'll reuse for the rest of your career. See you there.

---

## Appendix — the BFS version (for the board, before the DP)

```python
from collections import deque

def racecar_bfs(target):
    limit = 2 * target                      # fence: first milestone past target is < 2*target
    seen = {(0, 1)}
    queue = deque([(0, 1, 0)])              # position, speed, instructions used

    while queue:
        pos, spd, steps = queue.popleft()
        if pos == target:                   # first pop of the goal = shortest sequence
            return steps
        nxt = ((pos + spd, spd * 2),                # 'A': move, then double
               (pos, -1 if spd > 0 else 1))         # 'R': reset speed, stay put
        for npos, nspd in nxt:
            if 0 <= npos <= limit and abs(nspd) <= limit and (npos, nspd) not in seen:
                seen.add((npos, nspd))
                queue.append((npos, nspd, steps + 1))
    return -1
```

## Appendix — Java version (drop-in for Java tracks)

```java
public int racecar(int target) {
    int[] dp = new int[target + 1];                    // dp[0] = 0

    for (int t = 1; t <= target; t++) {
        int k = 32 - Integer.numberOfLeadingZeros(t);  // smallest k with 2^k - 1 >= t

        if ((1 << k) - 1 == t) {                       // case 1: lands exactly
            dp[t] = k;
            continue;
        }

        // case 2: overshoot to 2^k - 1, one R, cover the gap coming back
        dp[t] = k + 1 + dp[(1 << k) - 1 - t];

        // case 3: stop short at 2^(k-1) - 1, R, back up 2^j - 1, R again
        for (int j = 0; j < k - 1; j++) {              // j = 0 .. k-2
            int rest = t - ((1 << (k - 1)) - 1) + ((1 << j) - 1);
            dp[t] = Math.min(dp[t], k + j + 1 + dp[rest]);
        }
    }
    return dp[target];
}
```
