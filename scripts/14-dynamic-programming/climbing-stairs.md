# 🎬 Recording Script — Climbing Stairs
**Pattern: Dynamic Programming · LeetCode 70 · Easy · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the *first* DP lesson. It teaches the whole DP discovery path you'll reuse for every problem after it.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an interview screen. A tiny recursive function `climb(n): return climb(n-1) + climb(n-2)`. Someone types `climb(45)` and hits run. A spinner. Then a red "Time Limit Exceeded" banner.]**

> Here's a problem that looks like a joke. *"You climb stairs one or two steps at a time. How many ways to the top?"* Four lines of recursion and you're done.
>
> You run it on `n = 45`. And it just… hangs. Time Limit Exceeded on an *Easy* problem.
>
> That gap — between a correct idea and a fast one — is the entire subject of Dynamic Programming. And this little staircase is the cleanest place on earth to *see* why the naive version dies and exactly how DP resurrects it. Learn the pattern here, and I promise the scary DP problems later stop being scary. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: a staircase with 3 steps. One plain sentence on top: "Climb 1 or 2 steps at a time — how many distinct ways to the top?"]**

> The whole problem in one line: **you can step up 1 stair or 2 stairs at a time — how many distinct ways to reach the top of an `n`-step staircase?**
>
> Tiny example: `n = 3`. Let's just list them. `1+1+1`. `1+2`. `2+1`. That's **three** ways.
>
> **[VISUAL: the three paths drawn as little arrow sequences up the 3 steps.]**
>
> Hold that number — three — we'll see it fall out of the math in a minute.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — find the decision, then feel the waste)*

**[VISUAL: the top step glows. A thought bubble: "How did I get HERE?"]**

> Let's find the idea the way you actually would in the room. Stand on the top step, step `n`. Ask one question: *how did I arrive here?*
>
> There are only two possible last moves. Either your last move was a **single** step — so a second ago you were on step `n-1`. Or your last move was a **double** step — so you were on step `n-2`. There is no third way to land on `n`.
>
> **[VISUAL: two arrows into the top step — one curving from n-1, one from n-2.]**
>
> So the number of ways to reach `n` is the ways to reach `n-1`, **plus** the ways to reach `n-2`. Write that down, because it's the heart of everything:
>
> **[VISUAL: boxed — `ways(n) = ways(n-1) + ways(n-2)`.]**
>
> That's a *recurrence*. And the base cases: `ways(0) = 1` — there's exactly one way to stand at the bottom, which is to do nothing — and `ways(1) = 1`.
>
> Now watch me actually run it as pure recursion.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: the recursion tree for `ways(5)` grows node by node. ways(5) → ways(4), ways(3); ways(4) → ways(3), ways(2)… nodes for ways(3), ways(2) start lighting up in the SAME color, repeated across the tree.]**

> **TEACHER:** I call `ways(5)`. It needs `ways(4)` and `ways(3)`. `ways(4)` needs `ways(3)` and `ways(2)`. Look — `ways(3)` just showed up in **two** different places. And each of *those* re-expands into the same children again.
>
> **LEARNER:** Wait — so `ways(3)` gets computed from scratch every time it appears? It doesn't remember the answer it already found?
>
> **TEACHER:** Exactly right. That's the whole disease. The plain recursion has no memory. The same subproblems get recomputed exponentially — the tree roughly *doubles* each level, so it's O(2ⁿ) nodes. At `n = 45` that's tens of billions of calls.
>
> Pause the video. Here's your predict: **the answer to `ways(3)` never changes. So what's the single cheapest thing I could do the first time I compute it, so I never pay for it again?**
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the recursion tree again, but now each computed node gets a little sticky-note with its value pasted on it. Second time a node is needed, a hand just reads the sticky note instead of expanding.]**

> **TEACHER:** You said it: write the answer down. The first time we compute `ways(3)`, we stick a note on it — "this is 3." Next time anyone asks for `ways(3)`, we read the note. O(1). No re-expanding.
>
> That's **memoization** — a cache keyed by the input. And look what it does to the tree: all those duplicate branches get pruned to a single lookup. The ~2ⁿ tree collapses to just `n` distinct subproblems — `ways(0)` through `ways(n)`, each computed once.
>
> **[VISUAL: the fat tree visually deflates into a thin chain of n nodes.]**
>
> Now here's the leap that turns memoization into *real* DP. If I'm going to compute `ways(0), ways(1), ways(2), …` each exactly once anyway — why recurse top-down at all? Why not just fill them in order, bottom-up, smallest first?
>
> **[VISUAL: an array `dp` of cells. dp[0]=1, dp[1]=1 filled. Then dp[2] = dp[1]+dp[0] lights up = 2. dp[3]=dp[2]+dp[1]=3…]**
>
> `dp[0] = 1`, `dp[1] = 1`. Then each next cell is just the two before it added together. `dp[2] = 2`, `dp[3] = 3`, `dp[4] = 5`, `dp[5] = 8`. Same recurrence — just evaluated in dependency order, no recursion, no stack.
>
> And notice `dp[3] = 3`. There's the three ways we counted by hand at the start. Loop closed.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line — "ways(n) = ways(n-1) + ways(n-2). It's Fibonacci."]**

> Burn this in: **to reach step n, your last move came from n-1 or n-2 — so add those two.** That's it. This is literally the Fibonacci sequence wearing a staircase costume.
>
> And here's the bigger meta-move, the one you'll reuse on every DP problem: **find the last decision, write the recurrence, spot the repeated subproblems, fill a table.** That four-step recipe *is* dynamic programming.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build the table version first — it's the clearest. Handle the tiny base case, then set up the array.

```python
def climb_dp(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
```

> **[VISUAL: add chunk 2, highlight it.]** Now the one loop that does all the work — each cell is the two before it.

```python
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

> That's the whole thing. O(n) time, O(n) space. But we can do better on space, and that's the part interviewers love — hold on.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:15`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `if n <= 1: return 1` — for a 0 or 1-step staircase there's exactly one way. It also keeps us from indexing `dp[1]` when the array's too short.
>
> `dp[0], dp[1] = 1, 1` — the seeds. Everything else is grown from these two.
>
> `dp[i] = dp[i-1] + dp[i-2]` — the recurrence, verbatim. The loop *starts at 2* because 0 and 1 are already known.
>
> **LEARNER:** Quick one — why is `dp[0] = 1` and not `0`? Zero steps feels like zero ways.
>
> **TEACHER:** Great instinct, and it's the classic trap. "Ways to reach the bottom" means "ways to make no progress" — and there's exactly one: stand still. If you set `dp[0] = 0`, then `dp[2] = dp[1] + dp[0] = 1`, but we *know* two steps has two ways: `1+1` and `2`. Setting it to 1 makes the whole chain come out right. Base cases aren't decoration — one wrong seed poisons every value after it.

---

## 9. DRY-RUN THE CODE — `7:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the dp array for n=5 filling cell by cell, left to right, each new cell flashing = sum of the two to its left.]**

> Run it on `n = 5`, watch the table fill:

| i | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| dp[i] | 1 | 1 | 2 | 3 | 5 | 8 |

> `dp[2] = 1+1 = 2`. `dp[3] = 2+1 = 3`. `dp[4] = 3+2 = 5`. `dp[5] = 5+3 = 8`. Return **8**. Eight ways to climb a 5-step staircase. Fibonacci, exactly.

---

## 10. COMPLEXITY, OUT LOUD — `7:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute recursion: O(2ⁿ) time. DP table: O(n) time, O(n) space.]**

> Say it the way you'd say it to the interviewer: *"Naive recursion is O(2ⁿ) because it recomputes the same subproblems all over the tree. Memoizing or tabulating solves each of the n subproblems once, so it's O(n) time. The table costs O(n) space."*
>
> That contrast — exponential to linear, purely by *remembering* — is the one-sentence pitch for what DP even is.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:15`
*(depth + honesty — the strong beat)*

**[VISUAL: the dp array with a spotlight window covering only the last two cells; everything to the left greys out and crumbles away.]**

> Now the move that gets the nod. Look at the recurrence again: `dp[i] = dp[i-1] + dp[i-2]`. It only ever reaches **two** cells back. `dp[0]`, once we're past it, is *dead weight* — nothing will ever read it again.
>
> So why keep the whole array? Keep **two variables** and slide them forward.

```python
def climb(n):
    prev, curr = 1, 1          # ways(0), ways(1)
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

> Trace `n = 5`: `(prev, curr)` goes `(1,1) → (1,2) → (2,3) → (3,5) → (5,8)`. Return 8. Same answer, and now it's **O(1) space.**
>
> Say this out loud in the room: *"Since the recurrence only looks two rows back, I don't need the array — two rolling variables suffice, O(1) space."* That "sliding window over the table" instinct shows up in half of all DP problems. Whenever your recurrence reaches back a **fixed** number of rows, you can drop the table.

---

## 12. YOUR TURN (active recall) — `8:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Min Cost Climbing Stairs (LC 746)". A blank editor.]**

> Before the next video, try **Min Cost Climbing Stairs**. Same two-back skeleton — but now each step charges a toll, and you want the *cheapest* way up instead of the *count*. The recurrence barely changes: swap the `+` for a `min` and add the step's cost.
>
> Don't peek at the solution. Struggle with the recurrence for ten minutes. That struggle is what converts "I watched it" into "I own it."

---

## 13. LOCK IT IN — `9:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Find the last decision** → it hands you the recurrence. Here: last move was +1 or +2.
> 2. **Repeated subproblems in the tree = the DP signal.** Memoize, then tabulate.
> 3. **Recurrence reaches back k rows → you only need k variables.** O(n) → O(1).
>
> And the memory peg — when a problem asks *"how many ways to reach the end, one small step at a time,"* your brain should whisper: **that's Fibonacci. Add the last two.**

---

## 14. CLIFFHANGER — `9:50`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "House Robber". A row of houses with dollar signs.]**

> Here's the twist that's coming. What if each step isn't just *counted* — what if it's *worth money*, and grabbing one step forbids you from grabbing its neighbor? Same two-back skeleton, but now instead of adding, you're choosing the *maximum*. That's House Robber — the exact same bones, one sharper decision. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// O(1) space — rolling variables
public int climbStairs(int n) {
    int prev = 1, curr = 1;      // ways(0), ways(1)
    for (int i = 2; i <= n; i++) {
        int next = prev + curr;
        prev = curr;
        curr = next;
    }
    return curr;
}
```
