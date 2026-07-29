# 🎬 Recording Script — Best Time to Buy and Sell Stock (I & II)
**Pattern: Dynamic Programming (state machine) · LeetCode 121 (Easy) & 122 (Medium) · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** rolling variables from Climbing Stairs / House Robber — here the whole DP *is* rolling variables.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a price chart: 7, 1, 5, 3, 6, 4. A hand tries to draw a buy-low/sell-high line, second-guesses, redraws.]**

> You've got a week of stock prices. Buy on one day, sell on a later day — what's your best profit? Feels like you have to compare every buy against every later sell. That's O(n²), and at a hundred-thousand days it times out.
>
> But there's a way to do it in a **single pass** with **one variable**. And then a twist — what if you can trade *unlimited* times? — that turns into a beautiful little **state machine**, the DP idea behind almost every trading and game problem. Two problems, one lesson, and by the end both collapse to a clean scan. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: `prices = [7, 1, 5, 3, 6, 4]`. Two boxes: "121: one trade → 5" and "122: unlimited → 7".]**

> Two versions, same prices `[7, 1, 5, 3, 6, 4]`.
>
> **LC 121 — one transaction:** buy once, sell once later. Best is buy at 1, sell at 6 → profit **5**.
>
> **LC 122 — unlimited transactions:** trade as often as you like, one share at a time. Buy 1 sell 5 (+4), buy 3 sell 6 (+3) → **7**. More freedom, more profit.
>
> Hold both numbers — **5** and **7**. Watch how the *same idea* handles both.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — find the decision, problem 121)*

**[VISUAL: for 121, every buy/sell pair drawn as an arc; a "comparisons" counter climbs fast.]**

> Start with 121. Brute force: try every buy day paired with every later sell day, track the max profit. Six days, and you're already drawing a fistful of arcs — that's O(n²), re-checking overlapping ranges constantly.
>
> Now the insight. To sell on day `i` for the best profit, you'd have bought at the **cheapest price before day `i`**. So sweep left to right carrying one fact — the minimum price seen so far. On each day, "profit if I sold today" is `today − minSoFar`. Keep the best of those.
>
> **[VISUAL: boxed — "best = max(best, price − minSoFar); then update minSoFar".]**
>
> One pass, one running minimum. No pairs.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: switch to 122. The single-min trick is shown FAILING — it can't capture two separate up-runs. A "???" appears.]**

> **TEACHER:** That min-tracking trick nails 121. But now 122 hands you unlimited trades — and suddenly "one cheapest buy, one best sell" isn't enough, because the best plan makes *several* separate trades. The single-variable trick breaks.
>
> **LEARNER:** So do I need a whole DP table now, indexed by day and by how many trades I've made?
>
> **TEACHER:** That's the natural fear — and the elegant answer is *no*. The trick is to stop tracking "trades" and instead track **what state you're in** each day: are you **holding** a share, or **not holding** one? Just two states.
>
> Predict before I reveal: on any given day, you're in one of those two states. **What's the best way to be in each state today, given yesterday's two states?** Pause and sketch it.
>
> *(4-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:40`
*(elaboration — derive the state machine, problem 122)*

**[VISUAL: two labeled boxes, "cash" (no share) and "hold" (own a share), with arrows between them: buy (cash→hold), sell (hold→cash), and self-loops for "wait".]**

> **TEACHER:** Here's the state machine. Two states each day:
> - **`cash`** = the most money I can have **not holding** a share today.
> - **`hold`** = the most money I can have **while holding** a share today (money already spent to buy it, so this is often negative).
>
> Now the transitions — each state is the better of "act" or "wait":
>
> **[VISUAL: the two update lines appear, arrows animating buy/sell/wait.]**
>
> - `cash` today = max of *(stay in cash)* or *(sell the share I was holding)* → `max(cash, hold + price)`.
> - `hold` today = max of *(keep holding)* or *(buy today, spending from cash)* → `max(hold, cash − price)`.
>
> Every day just updates these two numbers from yesterday's two. No table of days, no count of trades — the two rolling scalars *are* the entire DP. At the end, the answer is `cash` — you never want to finish still holding a share.
>
> **[VISUAL: walk [7,1,5,3,6,4]; cash climbs 0→0→4→4→7→7; final cash = 7.]**
>
> Run our prices and `cash` lands on **7** — matching the hand answer.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "cash = max(cash, hold + p); hold = max(hold, cash − p)."]**

> The line for 122: **each day, cash is the better of staying out or selling; hold is the better of staying in or buying.** Two states, two updates.
>
> That "model the states, transition each day, keep only yesterday" pattern is the **state-machine DP** — it powers stock problems with cooldowns, fees, and trade limits, plus tons of game DPs. This is the reusable jewel.

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build both, small pieces)*

**[VISUAL: editor. Type 121 first.]**

> 121 — one pass, running minimum.

```python
def max_profit_one(prices):
    min_price = float('inf')
    best = 0
    for p in prices:
        best = max(best, p - min_price)   # sell today at best buy-so-far
        min_price = min(min_price, p)     # or update cheapest buy
    return best
```

> **[VISUAL: new function; type 122.]** 122 — the state machine.

```python
def max_profit_many(prices):
    cash, hold = 0, float('-inf')         # no share yet; holding is "impossible" at start
    for p in prices:
        cash = max(cash, hold + p)        # sell today, or stay in cash
        hold = max(hold, cash - p)        # buy today, or keep holding
    return cash
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: both functions; spotlight lines as named.]**

> The *why* on 122:
>
> `cash = 0` — start flat, no profit, no share. `hold = -infinity` — you can't be holding on day zero before buying, so make that state "impossible" until a real buy overwrites it.
>
> `cash = max(cash, hold + p)` — either you were already out (keep `cash`), or you sell now, turning your `hold` position into `hold + p` dollars.
>
> `hold = max(hold, cash - p)` — either keep holding, or buy today, paying `p` out of your best `cash`.
>
> **LEARNER:** Subtle one — line two updates `cash`, then line three uses that **just-updated** `cash` to compute `hold`. Isn't that buying and selling on the *same* day? Should I use yesterday's cash instead?
>
> **TEACHER:** Beautiful catch, and it's actually *fine* — here's why. If `cash` improved this line by selling today, then `hold = cash - p` would be "sell today and rebuy today," which nets zero change versus just keeping the old hold — so it can never inflate the answer. Same-day buy-sell is a no-op with unlimited free trades. The sequential update is safe and even a hair cleaner. (If there were a transaction *fee*, you'd be more careful — that's a real follow-up.)

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close both loops)*

**[VISUAL: two trace tables side by side.]**

> 121 on `[7,1,5,3,6,4]`:

| price | min_price (before) | p − min | best |
|---|---|---|---|
| 7 | ∞ | — | 0 |
| 1 | 7 | −6 | 0 |
| 5 | 1 | 4 | 4 |
| 3 | 1 | 2 | 4 |
| 6 | 1 | 5 | **5** |
| 4 | 1 | 3 | 5 |

> Answer **5** — buy at 1, sell at 6. And 122's `cash` walks `0 → 0 → 4 → 4 → 7 → 7`, landing on **7**. Both hand-answers confirmed.

---

## 10. COMPLEXITY, OUT LOUD — `8:45`
*(transfer to interview)*

**[VISUAL: rows — Brute (121): O(n²). One-pass / state machine: O(n) time, O(1) space.]**

> To the interviewer: *"Brute force on 121 is O(n²) over all buy/sell pairs. The running-minimum pass is O(n) time, O(1) space. For 122, the two-state machine is also O(n) time, O(1) space — each day only reads yesterday's two states."*
>
> Linear time, constant space, both — that's the whole win, and it comes from realizing you never needed a table at all.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:15`
*(depth + honesty — the strong beat)*

**[VISUAL: a full dp[day][holding] grid drawn, then it deflates to just two scalars, "cash" and "hold".]**

> Here's the honest, and satisfying, space beat: both are **already O(1)** — and *that's the teaching point*. The "textbook" DP for 122 is a 2-D table `dp[day][0 or 1]` — profit on each day in each state. But each day depends only on the **previous** day. Fixed window of one. So it collapses instantly to two scalars, `cash` and `hold`. The table never needed to exist.
>
> And there's an even slicker view of 122 — the famous shortcut. With no trade limit, the optimal profit is just the **sum of every upward day-to-day move**:

```python
def max_profit_many_greedy(prices):
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
```

> **LEARNER:** Why on earth does "add up every uphill step" equal doing real, planned trades?
>
> **TEACHER:** Because gains telescope. A rising run `a → b → c` gives `(b−a) + (c−b) = c − a` — summing the little adjacent steps equals the one big trade from `a` to `c`. With unlimited free trades you're allowed to decompose any profitable climb into its daily pieces, so grabbing every up-step captures exactly the same total. `[7,1,5,3,6,4]` → up-steps `1→5` (+4) and `3→6` (+3) → **7**. Same answer, one line.
>
> Crucial caveat, and it's *why the two problems live together*: this shortcut works **only** for 122. For 121 you're capped at one transaction, so you can't sum multiple climbs — you're stuck with the single running-min scan. Confusing the two is a classic trap.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Best Time to Buy and Sell Stock with Cooldown (LC 309)". A 'rest' day after each sell.]**

> Before the next video: **Buy and Sell with Cooldown.** After you sell, you must **rest one day** before buying again. The move: add a **third state** — `cooldown` — to the machine, and route the transitions through it (`hold` can only be entered from `cooldown`, not directly from `cash`). Draw the three-box diagram first, *then* code it. It's the exact skill you just learned, one state richer.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **121: one pass, track the cheapest price so far** — `best = max(best, price − min)`. O(1).
> 2. **122: model two states, cash and hold,** update each from yesterday. State-machine DP.
> 3. **Transitions depend only on yesterday → no table, just scalars.** And 122 = "sum every uphill step."
>
> Memory peg — *"decisions over time where you're in one of a few states"* → **state machine: write the states, transition each day, keep only yesterday.**

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson / section close)*

**[VISUAL: a montage of the section's tables — staircase, houses, coins, grids — then a title: "You now speak DP."]**

> Look back at everything: staircases, houses, coins, subsequences, grids, strings, stock states. Every single one was the same four moves — **find the decision, write the recurrence, spot the overlap, fill a table** — and then squeeze the space. That recipe is dynamic programming, and you now own it. Next section, we take these instincts into problems that *disguise* themselves as something else entirely — and your job is to see the DP hiding inside. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// LC 121 — at most one transaction
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, best = 0;
    for (int p : prices) {
        best = Math.max(best, p - minPrice);
        minPrice = Math.min(minPrice, p);
    }
    return best;
}

// LC 122 — unlimited transactions (sum every uphill step)
public int maxProfitII(int[] prices) {
    int profit = 0;
    for (int i = 1; i < prices.length; i++) {
        if (prices[i] > prices[i - 1]) {
            profit += prices[i] - prices[i - 1];
        }
    }
    return profit;
}
```
