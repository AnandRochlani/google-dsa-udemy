# 🎬 Recording Script — Coin Change
**Pattern: Dynamic Programming (Unbounded Knapsack) · LeetCode 322 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the "find the last decision → recurrence → table" recipe from **Climbing Stairs** and **House Robber**.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: coins `1, 3, 4` on screen. A target: "make 6 with the fewest coins." A greedy hand grabs 4, then 1, then 1 — "3 coins!" A red X. Then two 3-coins slide in — "2 coins."]**

> Quick gut check. Coins of 1, 3, and 4. Make **6** with the fewest coins. Your brain does the obvious thing — grab the biggest coin, the 4, then two 1s. Three coins.
>
> Wrong. Two 3s make 6 in **two** coins. Greedy just lied to you.
>
> That's the trap this problem is famous for. The moment greedy fails, you need something that actually *considers every option* — and that's DP. Stick with me: we'll turn a hopeless exponential search into a clean linear-ish table, and you'll know exactly why greedy breaks. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: `coins = [1, 2, 5]`, `amount = 11`. One line: "Fewest coins to make the amount. Infinite supply of each. Impossible → -1."]**

> The problem: given coin denominations — **infinite supply of each** — and a target `amount`, return the **fewest coins** that sum to it. If it can't be done, return `-1`.
>
> Working example: coins `[1, 2, 5]`, amount `11`. The answer is **3**, because `5 + 5 + 1 = 11`. Hold that.
>
> And note "infinite supply" — you can reuse a coin as many times as you want. That detail shapes everything.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — find the decision)*

**[VISUAL: target 11 at the top. A thought bubble: "What was my LAST coin?"]**

> Here's how you find the recurrence. Don't think about the first coin — think about the **last** coin you place to hit the amount.
>
> If my last coin was the 5, then before it I must have optimally made `11 - 5 = 6`. If my last coin was the 2, I'd optimally made `9`. If it was the 1, I'd made `10`. One of those last-coin choices is best — but I don't know which. So I **try them all** and take the minimum, then add 1 for that last coin:
>
> **[VISUAL: boxed — `minCoins(a) = 1 + min over each coin c of minCoins(a - c)`.]**
>
> Base case: `minCoins(0) = 0` — zero coins make amount zero. And if no choice leads anywhere, it's impossible — we'll carry that as infinity while we compute.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: recursion tree for `minCoins(11)`. Branches to 10, 9, 6. `minCoins(9)` appears under multiple parents, lighting the same color repeatedly. Tree explodes fast.]**

> **TEACHER:** Run that as recursion. `minCoins(11)` branches into `minCoins(10), minCoins(9), minCoins(6)`. And `minCoins(10)` *also* needs `minCoins(9)`. And `minCoins(9)` reappears again deeper down. Same amount, recomputed everywhere.
>
> **LEARNER:** So it's the overlapping-subproblems thing again — but this time each node branches *more* than two ways, once per coin. This tree is way bushier than House Robber's.
>
> **TEACHER:** Exactly. It branches `len(coins)` ways at every level, down to depth `amount`. That's `O(coins^amount)` — astronomically worse than the two-way trees. But the *cure* is identical.
>
> Predict it: **the answer to `minCoins(9)` is the same no matter which path reaches it. So what do we do?** Pause.
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration — derive the table)*

**[VISUAL: the bushy tree collapses into a single row of cells indexed 0…11.]**

> **TEACHER:** Right — remember each amount's answer once. Memoize, then go bottom-up. Here the subproblems are literally the amounts `0, 1, 2, …, up to 11`, so the table is a **1-D array** `dp`, where `dp[a]` = fewest coins to make amount `a`.
>
> Seed: `dp[0] = 0`. Everything else starts at infinity — "unknown / impossible so far."
>
> Now fill left to right. For each amount `a`, try every coin `c` that fits, and see if going through `dp[a-c]` beats what we have:
>
> **[VISUAL: dp array filling. Show `dp[5]` becoming 1 via coin 5; `dp[6] = dp[5]+1 = 2` or `dp[4]+1`; …]**
>
> `dp[1] = 1` (one 1-coin). `dp[2] = 1` (one 2-coin). `dp[5] = 1` (one 5-coin). `dp[6] = min(dp[5], dp[4], dp[1]) + 1 = 2`. And so on up to `dp[11]`.
>
> Each cell just asks the recurrence — "over every last coin, what's the cheapest?" — but reads *already-finished* smaller answers instead of recomputing them.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "dp[a] = min over coins c of ( dp[a - c] + 1 )". Subtitle: "unbounded knapsack."]**

> The line: **the best way to make `a` is one coin `c`, plus the best way to make the rest, `a − c` — minimized over every coin.**
>
> This shape — "pick an item, add it, recurse on the remainder, and you may reuse items freely" — is called the **unbounded knapsack**. Coin Change is its poster child. Recognize the shape and half the battle's done.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Set up the table — `dp[0] = 0`, the rest infinity.

```python
def coin_change(coins, amount):
    dp = [0] + [float('inf')] * amount   # dp[0]=0, rest = "impossible so far"
```

> **[VISUAL: add chunk 2, highlight.]** For each amount, try every coin that fits and relax the minimum.

```python
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
```

> **[VISUAL: add chunk 3.]** Finally, translate a leftover infinity into "impossible."

```python
    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line.]**

> The *why*:
>
> `dp[0] = 0` — the anchor. It costs zero coins to make nothing. Every real answer eventually bottoms out here.
>
> Infinity for the rest — a sentinel meaning "not reachable yet." Adding 1 to infinity stays infinity, so unreachable amounts never falsely win a `min`.
>
> `if c <= a` — you can't use a coin bigger than the amount you're making; `dp[a-c]` would go negative.
>
> `dp[a-c] + 1` — the recurrence: cost to make the remainder, plus this one coin.
>
> The final ternary — if `dp[amount]` never dropped below infinity, no combination worked, so `-1`.
>
> **LEARNER:** Here's what nags me — greedy failed, but *why* does the table succeed where greedy didn't? What's it actually doing differently?
>
> **TEACHER:** The best question in this problem. Greedy commits to the biggest coin and never reconsiders. The table, at every amount, tries **every** coin as the last one and keeps the best — it never commits early. `dp[6]` genuinely compares "5 then dp[1]" against "3 then dp[3]" against "1 then dp[5]" and picks the winner. Considering all options is precisely the thing greedy skips — and precisely why DP is correct.

---

## 9. DRY-RUN THE CODE — `7:45`
*(worked example — prove it, close the loop)*

**[VISUAL: full dp row for coins [1,2,5], amount 11, filling cell by cell.]**

> Run coins `[1,2,5]`, amount `11`:

| a | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dp[a] | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 3 | 2 | **3** |

> Look at `dp[11] = min(dp[10]+1, dp[9]+1, dp[6]+1) = min(2+1, 3+1, 2+1) = 3`. Return **3** — that's `5 + 5 + 1`. Exactly what we promised.

---

## 10. COMPLEXITY, OUT LOUD — `8:30`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(coins^amount). DP: O(amount × coins) time, O(amount) space.]**

> To the interviewer: *"Naive recursion is exponential — it branches per coin down to depth amount, recomputing remainders. The table has amount-plus-one cells, and each does O(number-of-coins) work, so it's O(amount × coins) time and O(amount) space."*
>
> That "O(value of the input)" flavor has a name — **pseudo-polynomial** — worth saying, it signals you know the amount drives the cost, not just the coin count.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:00`
*(depth + honesty — the strong beat)*

**[VISUAL: the dp array; an arrow from dp[11] reaching ALL the way back to dp[0] via coin size 1. No fixed window.]**

> Now the honest space beat — and honesty *is* a skill here. In Climbing Stairs we dropped the array to two variables because the recurrence only reached **two** rows back. Can we do that here?
>
> **LEARNER:** I want to say yes… but a coin can be size 1, so `dp[a]` might read `dp[a-1]`, and another coin size 5 reads `dp[a-5]`… the reach isn't fixed, is it?
>
> **TEACHER:** Nailed it — and that's the whole point. The dependency window spans the *entire* array: with a 1-coin, `dp[a]` can trace all the way back to `dp[0]`. There's no fixed-size window to slide, so `O(amount)` space is the **floor**. You cannot collapse this to O(1), and the mature move is to *say so out loud* rather than fumble for an optimization that doesn't exist.
>
> *"Space is O(amount) and that's the floor — a coin of 1 means dp[a] can reference all the way back to dp[0]. No fixed window to roll, unlike Fibonacci-style DPs."*
>
> One *genuine* refinement: swap the loop order — coins outer, amounts inner. Same time, same space, but it's the exact template for the *count-combinations* cousin, Coin Change II:

```python
def coin_change(coins, amount):
    dp = [0] + [float('inf')] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Coin Change II (LC 518)". Subtitle: "count combinations, not minimize."]**

> Before the next video: **Coin Change II.** Same coins, same amount — but now *count the number of combinations* that make it, instead of minimizing. Here's your hint and your warning: put **coins on the outer loop, amounts inner** (the template I just showed). That order is what stops you from counting `1+2` and `2+1` as different — it enforces combinations, not permutations. Flip the loops and you'd solve a *different* problem.
>
> Wrestle with why the loop order matters. That's the lesson.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Greedy fails on coins** — always reach for DP when "grab the biggest" can backfire.
> 2. **The decision is "what was my last coin?"** → `dp[a] = min(dp[a−c] + 1)` over all coins.
> 3. **Space floor is O(amount)** — a small coin reaches the whole array; name the absence of a rolling trick.
>
> Memory peg — *"fewest / how-many ways to hit an exact total, reusing items freely"* → **unbounded knapsack: pick a last item, add one, recurse on the remainder.**

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Longest Increasing Subsequence". A jagged number sequence with a rising subsequence highlighted.]**

> Every DP so far had an obvious linear order — steps, houses, amounts. Next problem breaks that comfort: the answer can *end anywhere* in the array, and the naive DP is O(n²)… until a gorgeous trick with binary search drops it to n-log-n. That's Longest Increasing Subsequence. It'll stretch how you even define the subproblem. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);   // sentinel "infinity" (any real answer < this)
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int c : coins) {
            if (c <= a) {
                dp[a] = Math.min(dp[a], dp[a - c] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```
