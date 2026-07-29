# 🎬 Recording Script — House Robber
**Pattern: Dynamic Programming · LeetCode 198 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the two-back recurrence and rolling-variable trick from **Climbing Stairs** (previous DP lesson).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a row of houses, each with a dollar amount on the roof: 2, 7, 9, 3, 1. A cartoon robber. Red wires connect *adjacent* houses — "alarm links."]**

> You're robbing a street of houses. Each house has cash. One catch: hit **two houses in a row** and the connected alarms call the cops.
>
> So which houses do you take to walk away with the most money? Your gut says "grab the biggest ones" — grab the 9, grab the 7… but the 7 and 9 are neighbors. Now you're stuck.
>
> This is the problem that teaches the single most important word in DP: **decision.** By the end, you'll see that greedy fails, why "rob or skip" is the whole game, and how to solve it in one clean pass with *two variables*. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: the five houses `[2, 7, 9, 3, 1]`. One plain sentence: "Max money, no two adjacent houses."]**

> One line: **pick houses to rob for maximum total money, but you can never rob two adjacent houses.**
>
> Our tiny example: `[2, 7, 9, 3, 1]`. Let's eyeball a tempting-but-wrong answer first. Grab 7 and 3? They're not adjacent — that's 10. Feels fine.
>
> But watch: 2, then 9, then 1 — none adjacent — that's **12**. Better. The greedy "grab the biggest, the 9 and 7" is illegal, and even legal greedy misses it.
>
> **[VISUAL: two candidate selections drawn: {7,3}=10 crossed out, {2,9,1}=12 with a checkmark.]**
>
> Hold onto **12** — that's the answer we'll derive.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — find the decision)*

**[VISUAL: stand on the last house (value 1). A thought bubble: "Do I rob this one, or not?"]**

> Let's find the idea like you would in the room. Walk the houses left to right and stand on house `i`. You face exactly **one binary decision**: rob this house, or skip it.
>
> Case one — you **rob** house `i`. You pocket `nums[i]`. But now house `i-1` is off-limits — alarm. So the most you could've legally banked before is whatever was optimal up to house `i-2`.
>
> Case two — you **skip** house `i`. You take nothing here, and you carry forward whatever was optimal up to house `i-1`.
>
> You want the better of the two. There's the recurrence:
>
> **[VISUAL: boxed — `rob(i) = max( nums[i] + rob(i-2),  rob(i-1) )`.]**
>
> Rob-and-jump-two, versus skip-and-inherit-one. Take the max.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: the recursion tree for `rob(4)`: rob(4) → rob(3), rob(2); rob(3) → rob(2), rob(1)… nodes `rob(2)` and `rob(1)` light up repeatedly in the same color across branches.]**

> **TEACHER:** Write that recurrence as plain recursion and run it. `rob(4)` calls `rob(3)` and `rob(2)`. `rob(3)` calls `rob(2)` and `rob(1)`. See it? `rob(2)` shows up under *both* branches. And each re-expands the same way again.
>
> **LEARNER:** Hang on — this is the exact same doubling tree we saw in Climbing Stairs. Same overlapping subproblems, just with a `max` where the `+` was?
>
> **TEACHER:** That's *exactly* the connection, and spotting it is the whole point of this lesson. Different problem, identical skeleton. Two-back recurrence, exponential recomputation.
>
> So predict it before I show you: **what's the fix?** You already know it from last time. Pause and say it out loud.
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration — derive the table)*

**[VISUAL: the fat recursion tree deflates into a thin chain; then a dp array appears under the houses.]**

> **TEACHER:** You called it: remember each answer, solve each `rob(i)` once. Memoize the tree, then flip it bottom-up into a table. We fill `dp[i]` = *the max money robbable from houses 0 through i*.
>
> Seeds first. `dp[0]` — only one house, so you rob it: `dp[0] = nums[0] = 2`. `dp[1]` — two houses, adjacent, you can only take one, so the richer: `dp[1] = max(2, 7) = 7`.
>
> Now the recurrence fills the rest:
>
> **[VISUAL: dp array building under `[2,7,9,3,1]`, each cell showing its max(...) computation.]**
>
> `dp[2] = max(dp[1], nums[2] + dp[0]) = max(7, 9+2) = 11`.
> `dp[3] = max(dp[2], nums[3] + dp[1]) = max(11, 3+7) = 11`.
> `dp[4] = max(dp[3], nums[4] + dp[2]) = max(11, 1+11) = 12`.
>
> There it is — **12**. The number we spotted by hand. And notice `dp[4]` chose "rob house 4 plus the best up to house 2" — that's the 2, 9, 1 plan.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line — "dp[i] = max( skip: dp[i-1],  rob: nums[i] + dp[i-2] )".]**

> The one line to memorize: **at each house, take the max of skipping it — keep the best so far — or robbing it — its cash plus the best from two houses back.**
>
> That "include-this-item-and-jump, or exclude-it-and-inherit" shape is the beating heart of a whole family of DP problems. You just met it. You'll see it again in subset-sum and knapsack.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Table version first. Guard the single-house case and seed the first two.

```python
def rob_dp(nums):
    n = len(nums)
    if n == 1:
        return nums[0]
    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
```

> **[VISUAL: add chunk 2, highlight.]** Now the loop — the recurrence, verbatim.

```python
    for i in range(2, n):
        dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
    return dp[n - 1]
```

> The answer's the last cell — best over all houses. O(n) time, O(n) space. Space comes down next.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:20`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line.]**

> Walk the *why*.
>
> `dp[0] = nums[0]` — one house, no rules to break, take it.
>
> `dp[1] = max(nums[0], nums[1])` — two adjacent houses, you may take only one, so the bigger. This seed quietly bakes in the "no two adjacent" rule at the boundary.
>
> `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` — the two options. Skip: `dp[i-1]`. Rob: `nums[i]` plus `dp[i-2]`, jumping over the forbidden neighbor.
>
> **LEARNER:** Objection — when I rob house `i`, why `dp[i-2]` and not just `dp[i-1] minus that neighbor's money`? Can't I just subtract the neighbor out?
>
> **TEACHER:** Sharp, and it's the trap that ruins people's code. `dp[i-1]` is a single number — the *best* answer up to `i-1`. You have no idea whether that best plan actually *used* house `i-1` or not, so you can't cleanly "subtract it out." That's why we jump to `dp[i-2]`: it's the best answer from a range that's *guaranteed* to exclude the forbidden neighbor entirely. Clean, no bookkeeping.

---

## 9. DRY-RUN THE CODE — `7:30`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row under the houses.]**

> Run it on `[2, 7, 9, 3, 1]`:

| i | nums[i] | computation | dp[i] |
|---|---|---|---|
| 0 | 2 | seed | 2 |
| 1 | 7 | max(2, 7) | 7 |
| 2 | 9 | max(7, 9+2) | 11 |
| 3 | 3 | max(11, 3+7) | 11 |
| 4 | 1 | max(11, 1+11) | **12** |

> Return `dp[4] = 12`. Exactly the 2-plus-9-plus-1 plan we spotted at the very start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:20`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(2ⁿ). DP table: O(n) time, O(n) space.]**

> To the interviewer: *"Brute force explores rob-or-skip at every house — O(2ⁿ), and it recomputes the same suffixes. Tabulating solves each of the n houses once, O(n) time, O(n) space for the array."*
>
> Same story as Climbing Stairs — exponential to linear by remembering. The difference is a `max` instead of a `+`. That's the spacing lesson: recognize when a new problem is an old skeleton.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:50`
*(depth + honesty — the strong beat)*

**[VISUAL: dp array with a two-cell spotlight window; older cells crumble away.]**

> The recurrence reads only `dp[i-1]` and `dp[i-2]` — two rows back, a *fixed* window. Same observation as last lesson, so same payoff: drop the array, keep two rolling variables.

```python
def rob(nums):
    prev2, prev1 = 0, 0        # best up to i-2, best up to i-1
    for x in nums:
        prev2, prev1 = prev1, max(prev1, x + prev2)
    return prev1
```

> Trace `[2, 7, 9, 3, 1]` — `prev1` after each house: `2 → 7 → 11 → 11 → 12`. Return **12**. O(1) space.
>
> **LEARNER:** Neat — and starting both at 0 means you didn't even need the `n == 1` special case anymore?
>
> **TEACHER:** Right. `prev2 = prev1 = 0` makes the first house compute `max(0, nums[0]+0) = nums[0]` for free, and one house just returns that. The base cases fall out of the initialization. Cleaner *and* less memory.
>
> Say it in the room: *"Only ever two houses back, so two scalars — O(1) space."*

---

## 12. YOUR TURN (active recall) — `10:00`
*(retrieval practice)*

**[VISUAL: "Your turn → House Robber II (LC 213)". Houses arranged in a CIRCLE now.]**

> Before the next video: **House Robber II.** Same street, but now it's a **circle** — the first and last houses are neighbors too. Here's the whole trick, so you can chew on it: a circle means you can't rob *both* the first and last. So run this exact line-DP **twice** — once on houses `[0 … n-2]`, once on `[1 … n-1]` — and take the max. Two linear passes, done.
>
> Try to code it before you look anything up.

---

## 13. LOCK IT IN — `10:40`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **The decision is the recurrence.** "Rob or skip" *is* `max(dp[i-1], nums[i] + dp[i-2])`.
> 2. **Rob → jump two** (the neighbor's forbidden); **skip → inherit one.** Never try to "subtract out" a neighbor.
> 3. **Two-back recurrence → two rolling variables.** O(n) → O(1), same as Fibonacci.
>
> The memory peg — when a problem says *"pick items for a max total, but you can't take two next to each other,"* hear it as: **rob or skip, jump the neighbor.**

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a blurred title — "Coin Change". A pile of coins: 1, 3, 4.]**

> So far the "decision" branched just *two* ways — rob or skip. But what if at every step you had to choose among *many* options — say, which coin to spend to hit an exact amount — and greedy actively **lies** to you? Next up: Coin Change, where "grab the biggest" gives the wrong answer and the recurrence has to try them all. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// O(1) space — rolling variables
public int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;    // best up to i-2, best up to i-1
    for (int x : nums) {
        int cur = Math.max(prev1, x + prev2);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```
